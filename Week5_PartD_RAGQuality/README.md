# Week 5 — Part D: RAG Quality & Hallucination Reduction

## Key Learnings
1. **Retrieval Quality vs. Answer Quality:**
   - Always diagnose which component failed before attempting a fix.
   - If chunks lack the answer $\rightarrow$ Retrieval failure.
   - If chunks have the answer but response is wrong/hallucinated $\rightarrow$ Prompting/Generation failure.
2. **Grounding Prompt:**
   - Adding explicit negative constraint: *"If the answer is not contained in the context, say 'I don't have that information.' Do not use outside knowledge."* drastically minimizes false assertions.
3. **Chunk Size Tuning:**
   - Overly large chunks $\rightarrow$ dilutes vector signal, wastes context window tokens.
   - Overly small chunks $\rightarrow$ isolates individual phrases, destroys context continuity.
