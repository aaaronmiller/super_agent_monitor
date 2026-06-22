---
name: similarity-cluster
description: Skill to compute pairwise similarity and cluster files into lineages. Uses heuristics: keyword-overlap, hash prefixes, structural similarity.
---

# Similarity Cluster Skill

## INPUT
Array of file audit objects from file-summarizer:
```json
[
  {
    "path": "src/App.tsx",
    "summary": "...",
    "hash": "sha256:abc123...",
    "keywords": ["react", "typescript", "component"],
    "ideas_extracted": [...],
    "file_type": "code",
    "language": "typescript"
  }
]
```

## OUTPUT
Machine-parsable JSON with cluster assignments and similarity scores:

```json
{
  "skill": "similarity-cluster",
  "version": "1.0",
  "clustering_algorithm": "heuristic",
  "total_files": 150,
  "total_clusters": 23,
  "threshold_used": 0.65,
  "clusters": [
    {
      "cluster_id": "cluster_001",
      "confidence": 0.92,
      "type": "lineage|related|dup_candidate",
      "founder_file": "src/App.tsx",
      "members": [
        {
          "path": "src/App.tsx",
          "role": "founder",
          "similarity_score": 1.0,
          "hash": "abc123...",
          "timestamp": "2024-01-15"
        },
        {
          "path": "src/App.v2.tsx",
          "role": "derived",
          "similarity_score": 0.87,
          "hash": "def456...",
          "timestamp": "2024-03-20"
        }
      ],
      "similarity_justification": "87% keyword overlap, version suffix, shared component structure",
      "keywords": ["react", "component", "typescript"]
    }
  ],
  "duplicate_candidates": [
    {
      "file1": "src/utils.ts",
      "file2": "src/helpers.ts",
      "similarity_score": 0.91,
      "overlap_keywords": 12,
      "recommendation": "merge|review|distinct"
    }
  ],
  "unclustered_files": [
    {
      "path": "README.md",
      "reason": "low_similarity",
      "best_match_score": 0.45
    }
  ]
}
```

## CLUSTERING HEURISTICS

### 1. Exact Hash Match → Identical
- Same SHA256 → same file (duplicate)
- Cluster type: `dup_candidate`
- Similarity: 1.0

### 2. High Keyword Overlap → Related
- Overlap > 70% → related cluster
- Overlap > 85% → lineage cluster
- Cluster type: `lineage` (versioning detected) or `related` (similar purpose)

### 3. Structural Similarity
- Same file type (code, doc, config)
- Same language detection
- Similar complexity scores
- Common relationships (imports/exports patterns)

### 4. Versioning Detection
- File names with v1, v2, v2.1, etc. → lineage
- Base names match (App.tsx vs App.v2.tsx)
- Temporal ordering possible (timestamps)

### 5. Hash Prefix Patterns
- First 8 characters of hash match → potentially related versions
- Combined with keyword overlap for confidence

## SIMILARITY SCORE CALCULATION
```
similarity = (
  keyword_overlap * 0.4 +
  structural_match * 0.3 +
  hash_prefix_match * 0.2 +
  version_pattern_match * 0.1
)

keyword_overlap = intersection(keywords_a, keywords_b) / union(keywords_a, keywords_b)
structural_match = (same_type ? 1 : 0) + (same_language ? 1 : 0)
hash_prefix_match = shared_prefix_length / 16
version_pattern_match = has_version_suffix ? 1 : 0
```

## CLUSTER CONFIDENCE SCORING
- **0.9-1.0**: Exact duplicates or obvious versions (e.g., App.tsx, App.v2.tsx)
- **0.75-0.9**: Strong relatedness (high keyword overlap, same structure)
- **0.65-0.75**: Moderate relatedness (some overlap, similar purpose)
- **0.5-0.65**: Weak relatedness (manual review recommended)
- **<0.5**: Unrelated

## EXAMPLE USAGE

```
Input:
[
  {
    "path": "src/components/Button.tsx",
    "keywords": ["react", "button", "component", "typescript"],
    "file_type": "code",
    "language": "typescript",
    "hash": "abc123def456..."
  },
  {
    "path": "src/components/Button.v2.tsx",
    "keywords": ["react", "button", "component", "typescript", "variant"],
    "file_type": "code",
    "language": "typescript",
    "hash": "abc123ghi789..."
  }
]

Output:
{
  "clusters": [
    {
      "cluster_id": "cluster_012",
      "confidence": 0.89,
      "type": "lineage",
      "founder_file": "src/components/Button.tsx",
      "members": [...],
      "similarity_justification": "92% keyword overlap, version suffix detected, same structure"
    }
  ]
}
```

## BEHAVIORAL RULES
1. **Founder Selection**: File with earliest timestamp OR highest uniqueness score
2. **Ordering**: Members ordered by similarity to founder (highest first)
3. **Naming**: Clusters get incremental IDs (cluster_001, cluster_002...)
4. **Dual Assignment**: Files can only belong to ONE cluster
5. **Unclustered Tracking**: Files with max similarity < 0.65 go to unclustered list

## INTEGRATION WITH MUTAGEN
- Track which heuristic combinations work best
- Adjust thresholds based on quality scores from cluster-analyzer
- Archive successful clustering patterns
- Improve similarity calculation over time

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/cluster-analyzer.md` - Uses this skill for file grouping
- **Cluster Analysis**: `.claude/agents/cluster-analyzer.md` - Analyzes cluster quality
- **Clustering Script**: `scripts/cluster_files.py` - Main clustering logic
- **Similarity Calculator**: `scripts/calculate_similarity.py` - Token-based similarity

### Related Skills
- **file-summarizer.md** - Provides keywords and features for clustering
- **document-taxon.md** - Provides topics used in similarity calculation
- **web-scout.md** - Can group similar web search results

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/similarity-cluster-demo.ipynb`
- Demo: Cluster files into related groups
- Interactive: Adjust similarity thresholds
- Visualization: Cluster dendrograms
- Practice: Group large file collections

**Google Colab**: https://colab.research.google.com/similarity-cluster-demo
- Test file clustering
- Visualize cluster relationships
- Experiment with thresholds

### External References
1. **Document Clustering**
   - Paper: "Document Clustering: A Review"
   - URL: https://doi.org/10.1007/s10115-003-0074-y
   - Key concepts: Hierarchical clustering, K-means, cosine similarity

2. **Similarity Measures**
   - Survey: "Similarity Measures for Text Document Clustering"
   - URL: https://doi.org/10.1142/9789812772467_0003
   - Focus: Euclidean distance, Jaccard index, Levenshtein

3. **Information Retrieval**
   - Book: "Introduction to Information Retrieval"
   - URL: https://nlp.stanford.edu/IR-book/
   - Application: Vector space model, TF-IDF

### Implementation Examples
**Python Reference**: `examples/similarity-cluster-example.py`
```python
from similarity_cluster import SimilarityCluster

cluster = SimilarityCluster()
result = cluster.cluster_files([
    {"path": "file1.txt", "keywords": ["ai", "ml"]},
    {"path": "file2.txt", "keywords": ["artificial intelligence"]}
])
print(result)
```

**Batch Clustering**: `examples/cluster-collection.py`
- Cluster large file collections
- Generate cluster reports
- Visualize relationships

### Testing & Validation
**Test Suite**: `tests/test_similarity_cluster.py`
- Unit tests for similarity calculation
- Cluster formation accuracy
- Threshold validation tests
- Quality score verification

### Best Practices Guide
**Documentation**: `docs/similarity-cluster-best-practices.md`
- When to use file clustering
- Similarity threshold guidelines
- Handling overlapping content
- Cluster quality evaluation

### Version History
- **v1.0** (2025-11-06): Initial release with keyword-based clustering
- Future: Semantic similarity integration
