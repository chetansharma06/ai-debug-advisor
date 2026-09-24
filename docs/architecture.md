# Architecture

## Pipeline

1. **Syntax analysis** — `ast.parse` and tokenization fallback
2. **Linting** — Ruff/Pyflakes adapter
3. **Metrics** — Radon complexity
4. **Rule engine** — Logic, Structural, Style rules
5. **Explanation** — LLM-generated human-readable explanations
6. **Hint ladder** — 5 graded hints with leak detection
7. **Optimization** — LLM-generated corrected code

## Sessions

Hint levels are tracked per `(session, finding)` pair in `session.py`.