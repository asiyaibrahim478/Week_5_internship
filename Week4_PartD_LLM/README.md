# Week 4 — Part D: LLM APIs in Depth

**Author:** Asiya  
**Project:** AI Foundations & Deep Dive

## Core LLM API Principles

### 1. Model Hyperparameters
- **`temperature`:**
  - Range: `0.0` (greedy, deterministic, factual, reproducible) to `1.0`+ (creative, varied, exploratory).
  - Use `0.0` for structured extraction, SQL queries, and classification; use `0.7`–`1.0` for creative writing and brainstorming.
- **`max_tokens`:**
  - Hard cap on the maximum output tokens generated in a single completion to control cost and avoid runaway generation.

### 2. Statelessness & Conversation History
- LLM APIs maintain zero memory across requests.
- To simulate continuous dialogue, the application must pass the complete message history array (`[{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]`) on every request.

### 3. Token Streaming
- Instead of blocking until generation completes, streams tokens via Server-Sent Events (SSE) or iterators to deliver immediate UI feedback.

### 4. Structured JSON Output
- Instructing the LLM to output valid JSON conforming to a specific schema, combined with strict client-side deserialization and fallback parsing.

---

## Python Demonstration Script
See [`llm_deep_dive.py`](file:///d:/Internship/Week4_PartD_LLM/llm_deep_dive.py) for practical implementations of conversation loops, streaming emulation, temperature comparisons, and JSON schema extraction.
