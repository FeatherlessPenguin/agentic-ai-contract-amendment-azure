# Agentic AI Contract Amendment System (Azure Hybrid Architecture)

## Overview
Hybrid multi-agent system that drafts contract amendments using Ontario + Federal Canadian law snippets (curated corpus) and a hypothetical AI disclosure requirement.

**Pipeline**
1) Deterministic section extractor (no LLM)
2) Planner/Router agent (cheap)
3) Retrieve + compress legal snippets
4) Clause agents (parallel)
5) Consistency reviewer (patch-based)
6) Patch application (deterministic)
7) Redline side-by-side diff (deterministic)

## Tech Stack (target)
- Azure Functions (API)
- Azure AI Search (Free tier)
- Blob Storage
- Static Web Apps (UI)
- Hybrid agent orchestration (Planner + Clause Agents + Reviewer)

## Disclaimer
For demonstration only. Not legal advice. Includes a *hypothetical* AI disclosure requirement.
