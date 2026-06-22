"""
Index Manager for Delobotomize RAG Server
Handles indexing of codebases, findings, and incremental updates.

Supports three indexing phases:
- Phase 1 (MVP): Pre-compute embeddings for findings only
- Phase 2 (v1.5): Lazy code indexing - embed file on first access
- Phase 3 (v2.0): Full pre-index with incremental updates
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
import logging


class IndexManager:
    """
    Manages RAG indexing with support for incremental updates and multiple phases.
    """

    def __init__(self, index_path: str = "/app/rag-index"):
        self.index_path = Path(index_path)
        self.index_path.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self.logger = logging.getLogger(__name__)

        # Index metadata
        self.metadata_file = self.index_path / "metadata" / "index_metadata.json"
        self.metadata_file.parent.mkdir(parents=True, exist_ok=True)

        # File hash cache for incremental updates
        self.hash_cache_file = self.index_path / "metadata" / "file_hashes.json"

        # Load existing metadata
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load index metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass

        # Default metadata
        return {
            "version": "1.0",
            "created_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "index_phase": "none",
            "total_chunks": 0,
            "total_files": 0,
            "file_types": {},
            "chunk_types": {},
            "embeddings_version": "unknown",
        }

    def _save_metadata(self):
        """Save index metadata"""
        self.metadata["last_updated"] = datetime.utcnow().isoformat()

        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def index_findings(self, findings: List[Dict[str, Any]], run_id: str) -> Dict[str, Any]:
        """
        Index findings for RAG retrieval (Phase 1).
        Creates embeddings for security findings and code issues.
        """
        self.logger.info(f"Indexing {len(findings)} findings for run {run_id}")

        chunks = []
        for finding in findings:
            chunk = {
                "id": f"finding_{finding['id']}",
                "content": finding.get("description", ""),
                "metadata": {
                    "type": "finding",
                    "run_id": run_id,
                    "severity": finding.get("severity", "unknown"),
                    "category": finding.get("category", "unknown"),
                    "file_path": finding.get("file_path", ""),
                    "line_number": finding.get("line_number", 0),
                    "confidence": finding.get("confidence_score", 0),
                    "remediation": finding.get("remediation_template", ""),
                },
            }
            chunks.append(chunk)

        # Save chunks to disk
        chunks_file = self.index_path / "data" / f"findings_{run_id}.json"
        chunks_file.parent.mkdir(parents=True, exist_ok=True)

        with open(chunks_file, "w") as f:
            json.dump(chunks, f, indent=2)

        # Update metadata
        self.metadata["index_phase"] = "findings_only"
        self.metadata["total_chunks"] = len(chunks)
        self.metadata["chunk_types"]["findings"] = len(chunks)
        self._save_metadata()

        self.logger.info(f"Indexed {len(chunks)} finding chunks")
        return {"chunks_indexed": len(chunks), "phase": "findings_only", "run_id": run_id}

    def index_codebase(
        self, codebase_path: str, run_id: str, incremental: bool = False
    ) -> Dict[str, Any]:
        """
        Index codebase for RAG retrieval (Phase 2/3).
        Supports incremental updates based on file changes.
        """
        self.logger.info(f"Indexing codebase at {codebase_path} for run {run_id}")

        # Get file list
        files_to_index = self._get_files_to_index(Path(codebase_path), incremental)

        chunks = []
        for file_path in files_to_index:
            try:
                file_chunks = self._process_file(file_path, codebase_path)
                chunks.extend(file_chunks)
            except Exception as e:
                self.logger.warning(f"Failed to process {file_path}: {e}")

        # Save chunks
        chunks_file = self.index_path / "data" / f"codebase_{run_id}.json"
        chunks_file.parent.mkdir(parents=True, exist_ok=True)

        with open(chunks_file, "w") as f:
            json.dump(chunks, f, indent=2)

        # Update metadata
        phase = "lazy" if not incremental else "full"
        self.metadata["index_phase"] = phase
        self.metadata["total_files"] = len(files_to_index)
        self.metadata["total_chunks"] += len(chunks)
        self.metadata["chunk_types"]["code"] = len(chunks)
        self._save_metadata()

        # Update hash cache for incremental updates
        if incremental:
            self._update_hash_cache(files_to_index, Path(codebase_path))

        self.logger.info(f"Indexed {len(chunks)} code chunks from {len(files_to_index)} files")
        return {
            "files_indexed": len(files_to_index),
            "chunks_indexed": len(chunks),
            "phase": phase,
            "run_id": run_id,
        }

    def _get_files_to_index(self, codebase_path: Path, incremental: bool) -> List[str]:
        """Get list of files to index, respecting incremental updates"""
        codebase_path = Path(codebase_path)

        # Supported file extensions
        extensions = {
            ".py",
            ".js",
            ".ts",
            ".java",
            ".cpp",
            ".c",
            ".cs",
            ".php",
            ".rb",
            ".go",
            ".rs",
        }

        files_to_index = []
        for ext in extensions:
            files_to_index.extend(codebase_path.rglob(f"*{ext}"))

        # Convert to strings
        files_to_index = [str(f) for f in files_to_index]

        if incremental:
            # Filter to only changed files
            files_to_index = self._filter_changed_files(files_to_index, Path(codebase_path))

        return files_to_index

    def _filter_changed_files(self, files: List[str], codebase_path: Path) -> List[str]:
        """Filter to only files that have changed since last index"""
        hash_cache = self._load_hash_cache()
        changed_files = []

        for file_path in files:
            try:
                current_hash = self._calculate_file_hash(file_path)
                cached_hash = hash_cache.get(file_path)

                if current_hash != cached_hash:
                    changed_files.append(file_path)
            except Exception:
                # If we can't hash the file, include it
                changed_files.append(file_path)

        return changed_files

    def _process_file(self, file_path: str, codebase_path: str) -> List[Dict[str, Any]]:
        """Process a single file into chunks using hierarchical chunking"""
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        relative_path = str(Path(file_path).relative_to(codebase_path))

        # Simple chunking strategy (could be enhanced with AST parsing)
        chunks = []

        # Split by functions/classes (basic heuristic)
        lines = content.split("\n")
        current_chunk = []
        chunk_start = 0

        for i, line in enumerate(lines):
            current_chunk.append(line)

            # Check for function/class definitions (language-specific)
            if self._is_chunk_boundary(line, file_path):
                if current_chunk:
                    chunk_content = "\n".join(current_chunk)
                    if len(chunk_content.strip()) > 50:  # Minimum chunk size
                        chunks.append(
                            {
                                "id": f"code_{relative_path}_{chunk_start}_{i}",
                                "content": chunk_content,
                                "metadata": {
                                    "type": "code",
                                    "file_path": relative_path,
                                    "start_line": chunk_start,
                                    "end_line": i,
                                    "language": self._detect_language(file_path),
                                    "chunk_type": "function"
                                    if self._is_function_definition(line)
                                    else "block",
                                },
                            }
                        )

                current_chunk = []
                chunk_start = i + 1

        # Add remaining content
        if current_chunk:
            chunk_content = "\n".join(current_chunk)
            if len(chunk_content.strip()) > 50:
                chunks.append(
                    {
                        "id": f"code_{relative_path}_{chunk_start}_{len(lines)}",
                        "content": chunk_content,
                        "metadata": {
                            "type": "code",
                            "file_path": relative_path,
                            "start_line": chunk_start,
                            "end_line": len(lines),
                            "language": self._detect_language(file_path),
                            "chunk_type": "remainder",
                        },
                    }
                )

        return chunks

    def _is_chunk_boundary(self, line: str, file_path: str) -> bool:
        """Check if line represents a chunk boundary (function/class definition)"""
        line = line.strip()

        # Python
        if file_path.endswith(".py"):
            return line.startswith(("def ", "class ", "async def "))

        # JavaScript/TypeScript
        if file_path.endswith((".js", ".ts", ".jsx", ".tsx")):
            return (
                line.startswith(("function ", "const ", "let ", "var ", "class ")) or "=>" in line
            )

        # Java
        if file_path.endswith(".java"):
            return line.startswith(("public ", "private ", "protected ", "class ", "interface "))

        # C/C++
        if file_path.endswith((".c", ".cpp", ".h", ".hpp")):
            return line.startswith(("void ", "int ", "char ", "class ", "struct "))

        # Default: split every 50 lines
        return False

    def _is_function_definition(self, line: str) -> bool:
        """Check if line is a function definition"""
        line = line.strip()
        return (
            "def " in line
            or "function " in line
            or ("(" in line and ")" in line and ("{" in line or ":" in line))
        )

    def _detect_language(self, file_path: str) -> str:
        """Detect programming language from file extension"""
        ext = Path(file_path).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".java": "java",
            ".cpp": "cpp",
            ".c": "c",
            ".cs": "csharp",
            ".php": "php",
            ".rb": "ruby",
            ".go": "go",
            ".rs": "rust",
        }
        return language_map.get(ext, "unknown")

    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file content"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def _load_hash_cache(self) -> Dict[str, str]:
        """Load file hash cache for incremental updates"""
        if self.hash_cache_file.exists():
            try:
                with open(self.hash_cache_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {}

    def _update_hash_cache(self, files: List[str], codebase_path: Path):
        """Update hash cache after indexing"""
        hash_cache = self._load_hash_cache()

        for file_path in files:
            try:
                hash_cache[file_path] = self._calculate_file_hash(file_path)
            except Exception:
                pass

        with open(self.hash_cache_file, "w") as f:
            json.dump(hash_cache, f, indent=2)

    def get_index_stats(self) -> Dict[str, Any]:
        """Get comprehensive index statistics"""
        return {
            "metadata": self.metadata,
            "index_path": str(self.index_path),
            "has_findings_index": (self.index_path / "embeddings" / "findings.faiss").exists(),
            "has_code_index": any((self.index_path / "data").glob("codebase_*.json")),
            "total_size_mb": self._calculate_index_size(),
        }

    def _calculate_index_size(self) -> float:
        """Calculate total size of index in MB"""
        total_size = 0
        for file_path in Path(self.index_path).rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return round(total_size / (1024 * 1024), 2)

    def cleanup_old_indexes(self, keep_runs: int = 5):
        """Clean up old run indexes, keeping only the most recent N"""
        data_dir = self.index_path / "data"
        if not data_dir.exists():
            return

        # Find all run indexes
        run_files = {}
        for file_path in data_dir.glob("*.json"):
            if "_" in file_path.name:
                run_id = file_path.name.split("_", 1)[1].rsplit(".", 1)[0]
                if run_id not in run_files:
                    run_files[run_id] = []
                run_files[run_id].append(file_path)

        # Sort by run ID (assuming timestamp-based naming)
        sorted_runs = sorted(run_files.keys(), reverse=True)

        # Remove old runs
        for old_run in sorted_runs[keep_runs:]:
            for file_path in run_files[old_run]:
                file_path.unlink()
                self.logger.info(f"Removed old index file: {file_path}")
