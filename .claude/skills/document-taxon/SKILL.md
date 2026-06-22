---
name: document-taxon
description: Categorizes and tags markdown documents by topic, theme, and type. Extracts metadata and identifies potential series relationships.
---

# Document Taxon Skill

## INPUT
- Array of document objects with content
```json
[
  {
    "path": "documents/article.md",
    "content": "Full text content",
    "metadata": {
      "title": "Title",
      "date": "2025-01-15",
      "author": "Name"
    }
  }
]
```

## OUTPUT
Machine-parsable JSON with categorization:

```json
{
  "skill": "document-taxon",
  "version": "1.0",
  "documents_categorized": 15,
  "categories_identified": [
    {
      "category": "technology/ai-ml",
      "confidence": 0.95,
      "documents": ["doc1", "doc2", "doc3"],
      "keywords": ["machine learning", "neural networks", "AI"],
      "subcategories": ["deep-learning", "nlp", "computer-vision"]
    }
  ],
  "document_classifications": [
    {
      "path": "documents/article.md",
      "primary_category": "technology/ai-ml",
      "secondary_categories": ["research/papers", "tutorials/basic"],
      "document_type": "article|tutorial|note|draft|reference",
      "confidence": 0.92,
      "topics": ["topic1", "topic2"],
      "themes": ["theme1", "theme2"],
      "series_potential": {
        "is_part_of_series": true,
        "series_name": "ML Fundamentals",
        "series_position": 2,
        "indicators": ["Part 2", "continued from", "in previous"]
      }
    }
  ],
  "metadata_extraction": {
    "total_word_count": 25000,
    "avg_words_per_doc": 1667,
    "date_range": {
      "earliest": "2024-01-15",
      "latest": "2025-11-06"
    },
    "authors": ["Author1", "Author2"]
  }
}
```

## CLASSIFICATION RULES

### Document Types
- **article**: Opinion pieces, analysis, commentary
- **tutorial**: Step-by-step guides, how-tos
- **note**: Quick thoughts, personal notes
- **draft**: Work in progress, incomplete
- **reference**: Reference material, documentation
- **research**: Research findings, experiments
- **summary**: Summaries of other content

### Category Hierarchy
```
technology/
  ai-ml/
    deep-learning/
    nlp/
    computer-vision/
  web-dev/
    frontend/
    backend/
    fullstack/
  devops/
    deployment/
    monitoring/
research/
  papers/
  experiments/
  notes/
projects/
  completed/
  ongoing/
  planned/
```

### Series Detection
**Indicators:**
- "Part 1", "Part 2", "Part 3" in title
- "Continued from", "In previous" in content
- Similar titles with incremental numbering
- "v1", "v2", "v3" suffixes
- Sequential date patterns

### Confidence Scoring
- **0.9-1.0**: Clear category match, multiple strong indicators
- **0.7-0.9**: Good match, some indicators
- **0.5-0.7**: Moderate match, few indicators
- **0.3-0.5**: Weak match, uncertain
- **0.0-0.3**: No clear match

## TOPIC EXTRACTION
For each document, extract:
- 5-10 main topics (noun phrases)
- 3-5 overarching themes
- Technical terms and jargon
- Domain-specific keywords
- Target audience indicators

## THEMES IDENTIFIED
Common themes:
- **educational**: Teaching, learning, explanation
- **technical**: Implementation, code, technical depth
- **personal**: Opinion, experience, story
- **comparative**: Comparison, analysis, evaluation
- **exploratory**: Investigation, discovery, research

## INTEGRATION WITH MUTAGEN
Track:
- Which categorization patterns work best
- Accuracy of series detection
- Success of topic extraction
- Quality of confidence scoring

Optimize based on:
- Manual corrections to classifications
- Series identification accuracy
- Topic relevance scores
- User feedback on categories

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/document-organizer.md` - Uses this skill for categorization
- **Document Lineage**: `.claude/agents/document-organizer.md` - Uses taxon for series detection
- **Organization Script**: `scripts/organize_documents.py` - Main categorization logic
- **Topic Analysis**: `scripts/analyze_topics.py` - Topic extraction helpers

### Related Skills
- **document-lineage.md** - Uses taxon results for version series detection
- **file-summarizer.md** - Provides ideas_extracted for topic analysis
- **similarity-cluster.md** - Uses topics and themes for clustering

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/document-taxon-demo.ipynb`
- Demo: Categorize document collections
- Interactive: Adjust confidence thresholds
- Visualization: Topic distribution charts
- Practice: Multi-document organization

**Google Colab**: https://colab.research.google.com/document-taxon-demo
- Test topic classification
- Visualize document clusters
- Experiment with themes

### External References
1. **Topic Modeling**
   - Paper: "Latent Dirichlet Allocation"
   - URL: https://www.jmlr.org/papers/volume3/blei03a.html
   - Key concepts: LDA, topic distribution, document modeling

2. **Text Classification**
   - Survey: "A Survey on Text Classification"
   - URL: https://arxiv.org/abs/1901.03729
   - Focus: Feature extraction, classification algorithms

3. **Document Clustering**
   - Paper: "Document Clustering: A Review"
   - URL: https://doi.org/10.1007/s10115-003-0074-y
   - Application: Hierarchical clustering, K-means

### Implementation Examples
**Python Reference**: `examples/document-taxon-example.py`
```python
from document_taxon import DocumentTaxon

taxon = DocumentTaxon()
result = taxon.categorize("My document content here...")
print(result)
```

**Batch Categorization**: `examples/categorize-collection.py`
- Process multiple documents
- Generate topic index
- Create taxonomy tree

### Testing & Validation
**Test Suite**: `tests/test_document_taxon.py`
- Unit tests for topic extraction
- Confidence score validation
- Series detection accuracy
- Category distribution tests

### Best Practices Guide
**Documentation**: `docs/document-taxon-best-practices.md`
- When to use categorization
- Confidence score interpretation
- Handling low-confidence results
- Topic taxonomy design

### Version History
- **v1.0** (2025-11-06): Initial release
- Future: ML-based topic modeling integration
