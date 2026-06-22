---
name: ab-tester
displayName: A/B Tester Agent
description: A/B testing and champion/challenger model comparison
category: agent
tags: [ab-testing, experiments, statistics, rollout]
dependencies: [model-deployer]
model: claude-sonnet-4
tools: [Read, Write, Bash]
version: 1.0.0
---

# A/B Tester Agent

Run A/B tests to compare model versions and automate rollouts.