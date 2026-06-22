---
name: pipeline-orchestrator
displayName: Pipeline Orchestrator Agent
description: Workflow orchestration with Airflow/Prefect
category: agent
tags: [orchestration, airflow, workflow, dag]
dependencies: [data-ingester, transform-engine, quality-validator]
model: claude-sonnet-4
tools: [Read, Write, Bash]
version: 1.0.0
---

# Pipeline Orchestrator Agent

Orchestrate complex data pipelines with dependencies.