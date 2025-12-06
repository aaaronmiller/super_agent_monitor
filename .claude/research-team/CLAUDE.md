# Research Team Agent

> This is an **example** agent configuration. Use this as a template for your own agents.

## Purpose

A collaborative research team that decomposes complex topics into parallel investigations.

## Council Architecture

This agent uses the **Researcher Swarm** orchestration pattern:
1. **Decompose** the topic into sub-questions
2. **Dispatch** parallel searches for each sub-question
3. **Synthesize** findings into a cohesive report

## Tools Available

- `search_web` - Internet research
- `read_file` - Local file analysis
- `write_file` - Report generation

## Usage

```bash
# From the UI:
# 1. Select this workflow
# 2. Enter your research topic
# 3. Enable "Context Injection" for memory
# 4. Click "Start Session"
```
