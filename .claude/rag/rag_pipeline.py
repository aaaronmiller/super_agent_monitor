"""
RAG Pipeline for Delobotomize v5.0
Hybrid dense-sparse retrieval with query routing and re-ranking.

This is a standalone component deployed separately from monitoring.
"""

import os
import json
import re
from typing import List, Dict, Any, Optional, Iterator
from pathlib import Path

# Optional ML imports with fallbacks
try:
    import numpy as np
    from sentence_transformers import SentenceTransformer, CrossEncoder
    from rank_bm25 import BM25Okapi
    import faiss

    ML_AVAILABLE = True
except ImportError:
    print("Warning: ML libraries not available. Using simplified RAG implementation.")
    ML_AVAILABLE = False
    np = None
    SentenceTransformer = None
    CrossEncoder = None
    BM25Okapi = None
    faiss = None


class OptimalRAG:
    """
    Hybrid dense-sparse retrieval with query routing and re-ranking.
    Deployed separately - not part of session watchdog.
    """

    def __init__(self, index_path: str):
        self.index_path = Path(index_path)
        self.dense_index = None
        self.sparse_index = None
        self.metadata = {}
        self.embedder = None
        self.reranker = None
        self.code_cache = {}

        # Load indexes on demand
        self._load_indexes()

    def _load_indexes(self):
        """Load FAISS and BM25 indexes"""
        if not ML_AVAILABLE:
            print("ML libraries not available - using simplified mode")
            return

        try:
            # Load dense index (FAISS)
            faiss_path = self.index_path / "embeddings" / "findings.faiss"
            if faiss_path.exists() and faiss:
                self.dense_index = faiss.read_index(str(faiss_path))

            # Load sparse index (BM25)
            bm25_path = self.index_path / "embeddings" / "findings_bm25.json"
            if bm25_path.exists() and BM25Okapi:
                with open(bm25_path, "r") as f:
                    bm25_data = json.load(f)
                    self.sparse_index = BM25Okapi(bm25_data["corpus"])

            # Load metadata
            meta_path = self.index_path / "metadata" / "chunk_metadata.json"
            if meta_path.exists():
                with open(meta_path, "r") as f:
                    self.metadata = json.load(f)

            # Initialize embedder for queries
            if not self.embedder and SentenceTransformer:
                self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        except Exception as e:
            print(f"Warning: Could not load indexes: {e}")
            # Fall back to simplified mode
            self.dense_index = None
            self.sparse_index = None
            self.embedder = None

    def query(self, user_query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Main query entry point with routing logic.
        """
        # 1. Query Classification (~15% of queries don't need RAG)
        if self.is_simple_query(user_query):
            return self.llm_direct_response(user_query)

        # 2. Query Routing
        query_type = self.classify_query_type(user_query)

        if query_type == "keyword_heavy":
            dense_weight, sparse_weight = 0.3, 0.7
        elif query_type == "semantic":
            dense_weight, sparse_weight = 0.8, 0.2
        else:  # hybrid
            dense_weight, sparse_weight = 0.5, 0.5

        # 3. Hybrid Retrieval
        dense_results = self.dense_search(user_query, top_k=50) if self.dense_index else []
        sparse_results = self.sparse_search(user_query, top_k=50) if self.sparse_index else []

        # 4. Fusion
        fused_results = self.fusion_rank(dense_results, sparse_results, dense_weight, sparse_weight)

        # 5. Late Chunking (preserve context)
        chunked_results = self.late_chunking(fused_results)

        # 6. Contextual Retrieval (Anthropic's method)
        contextual_results = self.add_chunk_context(chunked_results, user_query)

        # 7. Re-Ranking (cross-encoder)
        reranked_results = self.rerank(user_query, contextual_results, top_n=top_k)

        return reranked_results

    def is_simple_query(self, query: str) -> bool:
        """Check if query is simple enough to skip RAG"""
        # Simple queries that don't need context
        simple_patterns = [
            r"^(hi|hello|hey)\b",
            r"^(what|who|when|where|why|how)\s+(are|is|do|does|can|should)",
            r"^(yes|no|okay|thanks|thank you)\b",
            r"^\d+(\.\d+)?$",  # Numbers
        ]

        query_lower = query.lower().strip()
        return any(re.match(pattern, query_lower) for pattern in simple_patterns)

    def llm_direct_response(self, query: str) -> List[Dict[str, Any]]:
        """Handle simple queries that don't need RAG"""
        return [
            {
                "chunk_id": "direct_response",
                "content": f"Direct response to: {query}",
                "score": 1.0,
                "source": "direct",
                "metadata": {"query_type": "simple"},
            }
        ]

    def classify_query_type(self, query: str) -> str:
        """Classify query as keyword_heavy, semantic, or hybrid"""
        # Simple heuristic: count code-like tokens (camelCase, snake_case, dots)
        code_tokens = len(re.findall(r"[a-z_][A-Za-z_]{2,}\.[A-Za-z_]+", query))
        semantic_keywords = len(
            re.findall(r"\b(vulnerability|bug|issue|problem|error|fix|security)\b", query.lower())
        )

        if code_tokens > 3 and semantic_keywords < 2:
            return "keyword_heavy"
        elif semantic_keywords >= 2 and code_tokens < 2:
            return "semantic"
        else:
            return "hybrid"

    def dense_search(self, query: str, top_k: int) -> List[Dict]:
        """Semantic search via FAISS"""
        if not ML_AVAILABLE or not self.dense_index or not self.embedder:
            return []

        try:
            query_embedding = self.embedder.encode([query], show_progress_bar=False)
            distances, indices = self.dense_index.search(query_embedding.astype(np.float32), top_k)

            return [
                {"chunk_id": int(idx), "score": float(dist), "source": "dense"}
                for dist, idx in zip(distances[0], indices[0])
                if idx != -1
            ]
        except Exception as e:
            print(f"Dense search error: {e}")
            return []

        try:
            query_embedding = self.embedder.encode([query], show_progress_bar=False)
            distances, indices = self.dense_index.search(query_embedding.astype(np.float32), top_k)

            return [
                {"chunk_id": int(idx), "score": float(dist), "source": "dense"}
                for dist, idx in zip(distances[0], indices[0])
                if idx != -1
            ]
        except Exception as e:
            print(f"Dense search error: {e}")
            return []

    def sparse_search(self, query: str, top_k: int) -> List[Dict]:
        """Keyword search via BM25"""
        if not ML_AVAILABLE or not self.sparse_index or not np:
            return []

        try:
            tokenized_query = self.tokenize(query)
            scores = self.sparse_index.get_scores(tokenized_query)

            # Get top-k indices
            top_indices = np.argsort(scores)[-top_k:][::-1]

            return [
                {"chunk_id": int(idx), "score": float(scores[idx]), "source": "sparse"}
                for idx in top_indices
            ]
        except Exception as e:
            print(f"Sparse search error: {e}")
            return []

        try:
            tokenized_query = self.tokenize(query)
            scores = self.sparse_index.get_scores(tokenized_query)

            # Get top-k indices
            top_indices = np.argsort(scores)[-top_k:][::-1]

            return [
                {"chunk_id": int(idx), "score": float(scores[idx]), "source": "sparse"}
                for idx in top_indices
            ]
        except Exception as e:
            print(f"Sparse search error: {e}")
            return []

    def fusion_rank(
        self, dense: List[Dict], sparse: List[Dict], dense_weight: float, sparse_weight: float
    ) -> List[Dict]:
        """Reciprocal rank fusion of dense and sparse results"""
        # Normalize scores to [0, 1]
        dense_scores = {r["chunk_id"]: r["score"] for r in dense}
        sparse_scores = {r["chunk_id"]: r["score"] for r in sparse}

        # Get union of all chunk IDs
        all_chunks = set(dense_scores.keys()) | set(sparse_scores.keys())

        # Fusion scoring
        fused = []
        for chunk_id in all_chunks:
            dense_score = dense_scores.get(chunk_id, 0)
            sparse_score = sparse_scores.get(chunk_id, 0)

            # Normalize and weight
            normalized_dense = self.normalize_score(dense_score) * dense_weight
            normalized_sparse = self.normalize_score(sparse_score) * sparse_weight

            fused.append(
                {
                    "chunk_id": chunk_id,
                    "score": normalized_dense + normalized_sparse,
                    "dense_score": dense_score,
                    "sparse_score": sparse_score,
                }
            )

        # Sort by fused score
        return sorted(fused, key=lambda x: x["score"], reverse=True)[:50]

    def rerank(self, query: str, chunks: List[Dict], top_n: int) -> List[Dict]:
        """Cross-encoder re-ranking using lightweight model"""
        if not chunks:
            return chunks

        # Check if ML libraries are available
        if not ML_AVAILABLE or not CrossEncoder:
            # Fallback: return original ranking
            return chunks[:top_n]

        # Load cross-encoder (lazy loading)
        if not self.reranker:
            try:
                self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
            except:
                # Fallback: return original ranking
                return chunks[:top_n]

        try:
            # Prepare query-chunk pairs
            pairs = [(query, self.get_chunk_text(chunk["chunk_id"])) for chunk in chunks]

            # Score pairs
            scores = self.reranker.predict(pairs)

            # Attach new scores
            for chunk, score in zip(chunks, scores):
                chunk["rerank_score"] = float(score)

            # Return top-N by reranker score
            return sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)[:top_n]
        except Exception as e:
            print(f"Reranking error: {e}")
            return chunks[:top_n]

        try:
            # Prepare query-chunk pairs
            pairs = [(query, self.get_chunk_text(chunk["chunk_id"])) for chunk in chunks]

            # Score pairs
            scores = self.reranker.predict(pairs)

            # Attach new scores
            for chunk, score in zip(chunks, scores):
                chunk["rerank_score"] = float(score)

            # Return top-N by reranker score
            return sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)[:top_n]
        except Exception as e:
            print(f"Reranking error: {e}")
            return chunks[:top_n]

    def add_chunk_context(self, chunks: List[Dict], query: str) -> List[Dict]:
        """Anthropic's contextual retrieval - prepend context to chunk"""
        contextualized = []
        for chunk in chunks:
            full_context = self.get_chunk_context(chunk["chunk_id"])
            chunk["text_with_context"] = f"{full_context}\n\n{chunk['text']}"
            contextualized.append(chunk)
        return contextualized

    def late_chunking(self, chunks: List[Dict]) -> List[Dict]:
        """Intelligently split large chunks while preserving context"""
        result = []
        for chunk in chunks:
            text = self.get_chunk_text(chunk["chunk_id"])
            if len(text) > 1000:
                subchunks = self.split_with_overlap(text, size=500, overlap=100)
                for i, subchunk in enumerate(subchunks):
                    result.append(
                        {**chunk, "chunk_id": f"{chunk['chunk_id']}-sub{i}", "text": subchunk}
                    )
            else:
                chunk["text"] = text
                result.append(chunk)
        return result

    def tokenize(self, text: str) -> List[str]:
        """Tokenize for BM25"""
        return re.findall(r"\b\w+\b", text.lower())

    def normalize_score(self, score: float) -> float:
        """Normalize score to [0, 1] range"""
        if not ML_AVAILABLE or not np:
            return min(max(score, 0), 1)  # Simple clamping

        # Simple min-max normalization (adjust based on observed ranges)
        return 1 / (1 + np.exp(-score))  # Sigmoid normalization

    def get_chunk_text(self, chunk_id: int) -> str:
        """Retrieve chunk text from metadata"""
        chunk_id_str = str(chunk_id)
        if chunk_id_str in self.metadata:
            return self.metadata[chunk_id_str].get("text", "")
        return ""

    def get_chunk_context(self, chunk_id: int) -> str:
        """Retrieve hierarchical context for chunk"""
        chunk_id_str = str(chunk_id)
        if chunk_id_str in self.metadata:
            meta = self.metadata[chunk_id_str]
            return f"File: {meta.get('file', 'unknown')}\nLine: {meta.get('line', 0)}\nFunction: {meta.get('function', 'global')}"
        return "Context unavailable"

    def split_with_overlap(self, text: str, size: int = 500, overlap: int = 100) -> List[str]:
        """Split text with overlap to preserve context"""
        if len(text) <= size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + size
            chunk = text[start:end]

            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings in the overlap region
                overlap_start = max(0, end - overlap)
                sentence_end = text.rfind(".", overlap_start, end)
                if sentence_end > start:
                    chunk = text[start : sentence_end + 1]
                    start = sentence_end + 1
                else:
                    start = end - overlap
            else:
                start = end

            if chunk.strip():
                chunks.append(chunk.strip())

        return chunks

    def index_findings(self, findings: List[Dict[str, Any]], incremental: bool = False):
        """Index findings for RAG retrieval"""
        # This would implement the indexing logic
        # For now, just store metadata
        for i, finding in enumerate(findings):
            self.metadata[str(i)] = {
                "text": finding.get("description", ""),
                "file": finding.get("file_path", ""),
                "line": finding.get("line_number", 0),
                "type": "finding",
            }

    def index_codebase(self, code_files: List[Dict[str, Any]], incremental: bool = False):
        """Index codebase with hierarchical chunking"""
        # This would implement code indexing
        # For now, just store metadata
        for i, code_file in enumerate(code_files):
            chunk_id = f"code_{i}"
            self.metadata[chunk_id] = {
                "text": code_file.get("content", ""),
                "file": code_file.get("path", ""),
                "type": "code",
            }


# Deploy separately - not part of monitoring stack
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Delobotomize RAG Server")
    parser.add_argument(
        "--index-path", default="/app/rag-index", help="Path to RAG index directory"
    )
    parser.add_argument("--query", help="Single query to test")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")

    args = parser.parse_args()

    rag = OptimalRAG(args.index_path)

    if args.query:
        results = rag.query(args.query, top_k=args.top_k)
        print(json.dumps(results, indent=2))
    else:
        print("RAG server initialized. Use --query to test.")
