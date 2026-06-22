#!/usr/bin/env python3
"""
RAG Server Skeleton

Minimal implementation of the RAG (Retrieval-Augmented Generation) server
for the Super Agent Monitor. Uses SQLite for simplicity (can be upgraded
to PostgreSQL + pgvector for production).

Features:
- Document ingestion with chunking
- Vector embeddings via OpenAI or local
- Semantic search with relevance ranking
- Memory persistence between sessions

Usage:
    # Start server
    python scripts/rag_server.py serve --port 8200
    
    # Ingest documents
    python scripts/rag_server.py ingest --path /path/to/docs
    
    # Search
    python scripts/rag_server.py search --query "agent orchestration"
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


@dataclass
class Document:
    """A document chunk with embedding."""
    doc_id: str
    source: str
    content: str
    chunk_index: int
    embedding: Optional[List[float]] = None
    metadata: Optional[Dict] = None
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow().isoformat()


class RAGServer:
    """
    Minimal RAG server implementation.
    
    Architecture:
    - SQLite for document storage (upgradable to pgvector)
    - OpenAI embeddings or local fallback
    - Cosine similarity for search
    """
    
    DB_PATH = Path(".super_agent_monitor/rag.db")
    CHUNK_SIZE = 1000  # Characters per chunk
    CHUNK_OVERLAP = 100
    
    def __init__(self):
        self.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._embedding_fn = self._get_embedding_fn()
    
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(str(self.DB_PATH))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_id TEXT PRIMARY KEY,
                source TEXT,
                content TEXT,
                chunk_index INTEGER,
                embedding TEXT,
                metadata TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_source ON documents(source)
        """)
        conn.commit()
        conn.close()
    
    def _get_embedding_fn(self):
        """Get embedding function (OpenAI or fallback)."""
        try:
            import openai
            client = openai.OpenAI()
            
            def embed(text: str) -> List[float]:
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return response.data[0].embedding
            
            return embed
        except Exception:
            # Fallback: simple hash-based pseudo-embedding
            def fallback_embed(text: str) -> List[float]:
                h = hashlib.sha256(text.encode()).hexdigest()
                return [int(h[i:i+2], 16) / 255.0 for i in range(0, 64, 2)]
            
            return fallback_embed
    
    def _chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.CHUNK_SIZE
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - self.CHUNK_OVERLAP
        
        return chunks
    
    def ingest(self, path: Path, metadata: Dict = None) -> int:
        """Ingest a file or directory."""
        count = 0
        
        if path.is_file():
            count = self._ingest_file(path, metadata)
        elif path.is_dir():
            for file_path in path.rglob("*.md"):
                count += self._ingest_file(file_path, metadata)
            for file_path in path.rglob("*.txt"):
                count += self._ingest_file(file_path, metadata)
        
        return count
    
    def _ingest_file(self, path: Path, metadata: Dict = None) -> int:
        """Ingest a single file."""
        try:
            content = path.read_text()
        except Exception:
            return 0
        
        chunks = self._chunk_text(content)
        conn = sqlite3.connect(str(self.DB_PATH))
        
        for idx, chunk in enumerate(chunks):
            doc_id = hashlib.sha256(f"{path}:{idx}".encode()).hexdigest()[:16]
            embedding = self._embedding_fn(chunk)
            
            doc = Document(
                doc_id=doc_id,
                source=str(path),
                content=chunk,
                chunk_index=idx,
                embedding=embedding,
                metadata=metadata or {}
            )
            
            conn.execute("""
                INSERT OR REPLACE INTO documents 
                (doc_id, source, content, chunk_index, embedding, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                doc.doc_id,
                doc.source,
                doc.content,
                doc.chunk_index,
                json.dumps(doc.embedding),
                json.dumps(doc.metadata),
                doc.created_at
            ))
        
        conn.commit()
        conn.close()
        return len(chunks)
    
    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for relevant documents."""
        query_embedding = self._embedding_fn(query)
        
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute("SELECT doc_id, source, content, embedding FROM documents")
        
        results = []
        for row in cursor:
            doc_id, source, content, embedding_json = row
            doc_embedding = json.loads(embedding_json)
            
            # Cosine similarity
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            
            results.append({
                "doc_id": doc_id,
                "source": source,
                "content": content[:200] + "..." if len(content) > 200 else content,
                "score": similarity
            })
        
        conn.close()
        
        # Sort by similarity
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(a) != len(b):
            return 0.0
        
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot / (norm_a * norm_b)
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        conn = sqlite3.connect(str(self.DB_PATH))
        cursor = conn.execute("SELECT COUNT(*) FROM documents")
        total_docs = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT COUNT(DISTINCT source) FROM documents")
        total_sources = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_chunks": total_docs,
            "total_sources": total_sources,
            "db_path": str(self.DB_PATH)
        }
    
    def clear(self):
        """Clear all documents."""
        conn = sqlite3.connect(str(self.DB_PATH))
        conn.execute("DELETE FROM documents")
        conn.commit()
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description='RAG Server for Super Agent Monitor',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Serve command
    serve_parser = subparsers.add_parser('serve', help='Start HTTP server')
    serve_parser.add_argument('--port', '-p', type=int, default=8200, help='Port')
    serve_parser.add_argument('--host', default='127.0.0.1', help='Host')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest documents')
    ingest_parser.add_argument('--path', '-p', required=True, help='Path to ingest')
    ingest_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search documents')
    search_parser.add_argument('--query', '-q', required=True, help='Search query')
    search_parser.add_argument('--limit', '-n', type=int, default=5, help='Max results')
    search_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('--json', action='store_true', help='JSON output')
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear all documents')
    
    args = parser.parse_args()
    server = RAGServer()
    
    if args.command == 'serve':
        print(f"🚀 Starting RAG server on {args.host}:{args.port}")
        print("   Note: HTTP server not implemented in skeleton")
        print("   Use 'ingest' and 'search' commands directly")
    
    elif args.command == 'ingest':
        path = Path(args.path)
        print(f"📥 Ingesting from {path}")
        count = server.ingest(path)
        
        if args.json:
            print(json.dumps({"success": True, "chunks": count}))
        else:
            print(f"✅ Ingested {count} chunks")
    
    elif args.command == 'search':
        results = server.search(args.query, args.limit)
        
        if args.json:
            print(json.dumps({"results": results}, indent=2))
        else:
            print(f"🔍 Results for '{args.query}':")
            for r in results:
                print(f"  [{r['score']:.3f}] {r['source']}")
                print(f"          {r['content'][:100]}...")
    
    elif args.command == 'stats':
        stats = server.get_stats()
        
        if args.json:
            print(json.dumps(stats, indent=2))
        else:
            print("📊 RAG Statistics:")
            print(f"  📄 Total chunks: {stats['total_chunks']}")
            print(f"  📁 Total sources: {stats['total_sources']}")
            print(f"  💾 Database: {stats['db_path']}")
    
    elif args.command == 'clear':
        server.clear()
        print("🗑️ Cleared all documents")


if __name__ == "__main__":
    main()
