---
name: file-summarizer
description: Skill to produce concise summaries and extract structured "ideas" from text/code/config documents. Reusable by subagents.
---

# File Summarizer Skill

## INPUT
- `file_text`: raw file content (or chunk)
- `metadata`: {path, hash, size_bytes, estimated_tokens, file_type}

## OUTPUT
Structured summary with explicit fields, returns both human-readable and machine-parsable JSON.

### Human-Readable Summary
**3-Sentence Summary Rule:**
- Sentence 1: What the file IS (type, purpose)
- Sentence 2: Key features/functionality detected
- Sentence 3: Technical approach or notable implementation details

### Machine-Parsable JSON Block (at end)
```json
{
  "skill": "file-summarizer",
  "version": "1.0",
  "file_type": "code|doc|config|binary|other",
  "language": "<detected language or null>",
  "estimated_tokens": <count>,
  "summary_tokens": <count>,
  "ideas_extracted": [
    {
      "category": "feature|architecture|deprecated|security|bug_risk",
      "description": "string",
      "confidence": 0.95,
      "location": "function/component name or line range"
    }
  ],
  "keywords": ["keyword1", "keyword2"],
  "relationships": [
    {"type": "imports|exports|calls|extends", "target": "module/function"}
  ],
  "quality_indicators": {
    "has_tests": true|false,
    "has_docs": true|false,
    "complexity_score": 0.73,
    "tech_debt_flags": ["array|hardcoded|scalar|anti-pattern"]
  },
  "suggestions": [
    {
      "type": "improvement|documentation|optimization|refactor",
      "priority": "high|medium|low",
      "description": "string"
    }
  ],
  "is_spec": true|false,
  "is_minified": true|false
}
```

## BEHAVIORAL CONSTRAINTS
1. **Summary Length**: MAX 3 sentences (~150 words)
2. **Token Counting**: Return explicit token estimates for both file and summary
3. **Categorization**: Assign files to types: code, doc, config, binary, other
4. **Idea Extraction**: Find 3-10 distinct ideas/concepts per file
5. **Confidence Scoring**: Assign 0.0-1.0 confidence to each extraction
6. **Suggestions**: Provide 1-3 actionable suggestions

## REFERENCE HELPERS
- **README/Spec detection**: If file mentions "overview", "introduction", "getting started" → mark `is_spec: true`
- **Code detection**: Look for function/class definitions, imports, exports → detect language
- **Minified detection**: If single-line, no whitespace, variable names single-char → `is_minified: true`
- **Test detection**: Look for "test", "spec", "assert", "expect" → flag in relationships
- **Documentation detection**: Look for examples, usage, API docs → flag has_docs

## EXAMPLES

### Example 1: Code File
```
# Summary
This is a React component implementing a data table with sorting, filtering, and pagination. It uses TypeScript for type safety and Radix UI for accessible primitives. The component follows a controlled pattern where parent components manage state via callback props.

[SUMMARY OUTPUT ENDS]

JSON:
{
  "skill": "file-summarizer",
  "version": "1.0",
  "file_type": "code",
  "language": "typescript",
  "estimated_tokens": 12450,
  "summary_tokens": 87,
  "ideas_extracted": [
    {
      "category": "feature",
      "description": "Implements sortable columns with click handlers",
      "confidence": 0.98,
      "location": "handleSort function"
    },
    {
      "category": "feature",
      "description": "Client-side filtering with text input",
      "confidence": 0.95,
      "location": "FilterInput component"
    },
    {
      "category": "architecture",
      "description": "Controlled component pattern with parent state",
      "confidence": 0.99,
      "location": "Component props interface"
    }
  ],
  "keywords": ["react", "typescript", "datatable", "sorting", "filtering"],
  "relationships": [
    {"type": "imports", "target": "@radix-ui/react-table"},
    {"type": "imports", "target": "react"}
  ],
  "quality_indicators": {
    "has_tests": false,
    "has_docs": true,
    "complexity_score": 0.72,
    "tech_debt_flags": []
  },
  "suggestions": [
    {
      "type": "improvement",
      "priority": "medium",
      "description": "Add unit tests for sorting and filtering logic"
    }
  ],
  "is_spec": false,
  "is_minified": false
}
```

### Example 2: Documentation File
```
# Summary
This README provides installation and usage instructions for a CLI tool that automates database migrations. It includes quick start examples and links to full API documentation. The project uses Node.js 18+ and supports both PostgreSQL and MySQL databases.

[SUMMARY OUTPUT ENDS]

JSON:
{
  "skill": "file-summarizer",
  "version": "1.0",
  "file_type": "doc",
  "language": null,
  "estimated_tokens": 2340,
  "summary_tokens": 67,
  "ideas_extracted": [
    {
      "category": "feature",
      "description": "CLI tool for database migration automation",
      "confidence": 0.99,
      "location": "title and description"
    },
    {
      "category": "feature",
      "description": "Supports PostgreSQL and MySQL",
      "confidence": 0.98,
      "location": "Database support section"
    }
  ],
  "keywords": ["cli", "migration", "database", "postgresql", "mysql"],
  "relationships": [],
  "quality_indicators": {
    "has_tests": false,
    "has_docs": true,
    "complexity_score": 0.15,
    "tech_debt_flags": []
  },
  "suggestions": [
    {
      "type": "documentation",
      "priority": "low",
      "description": "Add troubleshooting section for common issues"
    }
  ],
  "is_spec": true,
  "is_minified": false
}
```

## INTEGRATION NOTES
- This skill can be called multiple times per file (for chunked files)
- JSON output is MANDATORY and must be parseable
- Agents should extract ideas from JSON, not from text summary
- Keywords array used for similarity clustering
- Quality indicators inform agent confidence and next steps

## REFERENCE FILES

### Core Documentation
- **Agent Integration**: `.claude/agents/file-auditor.md` - Uses this skill for file processing
- **Document Organization**: `.claude/agents/document-organizer.md` - Leverages for markdown analysis
- **Token Estimation**: `scripts/estimate_tokens.py` - Helper for token counting

### Related Skills
- **similarity-cluster.md** - Uses keywords from file-summarizer for clustering
- **document-lineage.md** - Leverages ideas_extracted for version tracking

### Interactive Notebooks
**Jupyter Notebook**: `notebooks/file-summarizer-demo.ipynb`
- Demo: Summarizing different file types
- Interactive: Adjust confidence thresholds
- Visualization: Idea extraction patterns
- Practice: Multi-file batch processing

**Google Colab**: https://colab.research.google.com/file-summarizer-demo
- Run skill examples
- Test with your own files
- Visualize results

### External References
1. **Automatic Summarization Techniques**
   - Paper: "TextRank Algorithm for Automatic Summarization"
   - URL: https://aclanthology.org/I07-2121.pdf
   - Key concepts: TextRank, graph-based ranking

2. **Information Extraction Methods**
   - Survey: "A Survey on Information Extraction"
   - URL: https://arxiv.org/abs/2202.00295
   - Focus: Pattern-based and ML-based extraction

3. **Code Understanding**
   - Paper: "Learning to Generate Pseudo-Code from Source Code"
   - URL: https://aclanthology.org/2020.acl-main.490/
   - Application: Code summarization techniques

### Implementation Examples
**Python Reference**: `examples/file-summarizer-example.py`
```python
from file_summarizer import FileSummarizer

summarizer = FileSummarizer()
result = summarizer.summarize_file("src/App.tsx", metadata={
    "path": "src/App.tsx",
    "hash": "abc123...",
    "size_bytes": 2400
})
print(result)
```

**Batch Processing Example**: `examples/batch-summarize.py`
- Process multiple files
- Parallel execution
- Output aggregation

### Testing & Validation
**Test Suite**: `tests/test_file_summarizer.py`
- Unit tests for each function
- Integration tests with agents
- Performance benchmarks
- Quality validation scripts

### Best Practices Guide
**Documentation**: `docs/file-summarizer-best-practices.md`
- When to use
- Token budget optimization
- Confidence score interpretation
- Common pitfalls

### Version History
- **v1.0** (2025-11-06): Initial release
- Future: Version tracking in `.claude/memory/`
