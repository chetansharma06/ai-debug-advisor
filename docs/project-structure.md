# Project Structure

This document provides a detailed overview of the project structure and explains the purpose of each directory and key file in the AI Bug & Debugging Advisor system.

## Root Directory

```
ai-debug-advisor/
├── .github/
├── .vscode/
├── docs/
├── eval/
├── prompts/
├── samples/
├── src/debug_advisor/
├── tests/
├── app.py
├── Makefile
├── pyproject.toml
├── requirements.txt
├── README.md
└── .env.example
```

## Directory Breakdown

### 1. `.github/`
Contains GitHub-specific configuration files and instructions.

```
.github/
├── copilot-instructions.md
└── workflows/
    └── ci.yml
```

**Files:**
- **`copilot-instructions.md`**: Instructions for GitHub Copilot to understand the project context and coding standards
- **`workflows/ci.yml`**: GitHub Actions workflow for continuous integration, including automated testing and linting

### 2. `.vscode/`
Contains Visual Studio Code workspace configuration files.

```
.vscode/
├── extensions.json
├── launch.json
├── settings.json
└── tasks.json
```

**Files:**
- **`extensions.json`**: Recommended VS Code extensions for the project
- **`launch.json`**: Debug configurations for running and debugging the application
- **`settings.json`**: Project-specific VS Code settings
- **`tasks.json`**: Automated tasks for common development operations

### 3. `docs/`
Contains comprehensive documentation for the project.

```
docs/
├── architecture.md
├── eval.md
├── hint_ladder.md
├── rules_catalog.md
├── technical-architecture.md
└── system-architecture.md
```

**Files:**
- **`architecture.md`**: High-level system architecture overview
- **`eval.md`**: Evaluation methodology and performance metrics
- **`hint_ladder.md`**: Documentation of the five-level hint system
- **`rules_catalog.md`**: Catalog of all analysis rules
- **`technical-architecture.md`**: Detailed technical architecture and design patterns
- **`system-architecture.md`**: Complete system architecture, deployment, and integration details

### 4. `eval/`
Contains evaluation dataset and scripts for measuring system performance.

```
eval/
├── dataset.jsonl
└── run_eval.py
```

**Files:**
- **`dataset.jsonl`**: JSON Lines file containing labeled buggy code samples for evaluation
- **`run_eval.py`**: Script to run the evaluation pipeline and generate performance metrics

### 5. `prompts/`
Contains Jinja2 templates for LLM prompt generation.

```
prompts/
├── explain.v1.jinja
├── hint_level_1.v1.jinja
├── hint_level_2.v1.jinja
├── hint_level_3.v1.jinja
├── hint_level_4.v1.jinja
├── hint_level_5.v1.jinja
└── optimize.v1.jinja
```

**Files:**
- **`explain.v1.jinja`**: Template for generating human-readable explanations
- **`hint_level_1.v1.jinja`**: Template for Level 1 hints (gentlest)
- **`hint_level_2.v1.jinja`**: Template for Level 2 hints
- **`hint_level_3.v1.jinja`**: Template for Level 3 hints
- **`hint_level_4.v1.jinja`**: Template for Level 4 hints
- **`hint_level_5.v1.jinja`**: Template for Level 5 hints (most explicit)
- **`optimize.v1.jinja`**: Template for code optimization suggestions

### 6. `samples/`
Contains sample Python code files for testing and demonstration purposes.

```
samples/
├── buggy_mutable_default.py
├── buggy_off_by_one.py
└── clean_but_slow.py
```

**Files:**
- **`buggy_mutable_default.py`**: Example code with mutable default argument bug
- **`buggy_off_by_one.py`**: Example code with off-by-one error
- **`clean_but_slow.py`**: Example of clean but inefficient code

### 7. `src/debug_advisor/`
Contains the main source code for the application.

```
src/debug_advisor/
├── __init__.py
├── __main__.py
├── cli.py
├── config.py
├── models.py
├── orchestrator.py
├── session.py
├── agents/
├── guardrails/
└── llm/
```

#### `agents/`
Contains the AI agents responsible for different aspects of the debugging pipeline.

```
agents/
├── __init__.py
├── explanation.py
├── hints.py
├── optimization.py
└── analysis/
    ├── __init__.py
    ├── agent.py
    ├── linters.py
    ├── metrics.py
    ├── syntax.py
    └── rules/
        ├── __init__.py
        ├── base.py
        ├── logic.py
        ├── registry.py
        ├── structural.py
        └── style.py
```

**Files:**
- **`explanation.py`**: Explanation agent that converts findings to human-readable format
- **`hints.py`**: Hint agent that generates progressive hint levels
- **`optimization.py`**: Optimization agent that generates corrected code versions
- **`analysis/agent.py`**: Main analysis agent coordinating the analysis pipeline
- **`analysis/linters.py`**: Integration with external linters (Ruff, Pyflakes)
- **`analysis/metrics.py`**: Code metrics and complexity analysis
- **`analysis/syntax.py`**: Syntax validation using Python's AST
- **`analysis/rules/base.py`**: Base classes for analysis rules
- **`analysis/rules/logic.py`**: Logic error detection rules
- **`analysis/rules/registry.py`**: Rules registry for managing and executing rules
- **`analysis/rules/structural.py`**: Structural code analysis rules
- **`analysis/rules/style.py`**: Style and naming convention rules

#### `guardrails/`
Contains safety and validation mechanisms.

```
guardrails/
├── __init__.py
├── leak_detector.py
└── output_validator.py
```

**Files:**
- **`leak_detector.py`**: Prevents hints from revealing complete solutions
- **`output_validator.py`**: Validates LLM outputs against expected schemas

#### `llm/`
Contains LLM integration components.

```
llm/
├── __init__.py
├── base.py
├── copilot_client.py
├── prompts.py
└── stub_client.py
```

**Files:**
- **`base.py`**: Abstract base class/interface for LLM clients
- **`copilot_client.py`**: GitHub Copilot API integration
- **`prompts.py`**: Prompt management and template loading
- **`stub_client.py`**: Offline stub client for testing

### 8. `tests/`
Contains the test suite for the application.

```
tests/
├── fixtures/
├── integration/
└── unit/
```

**Files:**
- **`fixtures/sample_code.py`**: Sample code used in tests
- **`integration/test_pipeline.py`**: End-to-end pipeline integration tests
- **`unit/test_guardrails.py`**: Tests for guardrail functionality
- **`unit/test_hints.py`**: Tests for hint generation
- **`unit/test_logic_rules.py`**: Tests for logic rule detection
- **`unit/test_syntax.py`**: Tests for syntax analysis

### 9. `app.py`
The Streamlit web application entry point.

### 10. `Makefile`
Contains development commands and shortcuts.

### 11. `pyproject.toml`
Project configuration file containing:
- Project metadata
- Dependencies
- Build system configuration
- Linting configuration
- Testing configuration

### 12. `requirements.txt`
List of Python package dependencies.

### 13. `README.md`
Main project documentation file.

### 14. `.env.example`
Template for environment variables and configuration.

## File Relationships

### Data Flow Through Files

```
app.py (User Input)
    ↓
src/debug_advisor/cli.py (Input Processing)
    ↓
src/debug_advisor/orchestrator.py (Pipeline Coordination)
    ↓
src/debug_advisor/agents/analysis/agent.py (Static Analysis)
    ↓
src/debug_advisor/agents/explanation.py (Explanation)
    ↓
src/debug_advisor/agents/hints.py (Hint Generation)
    ↓
src/debug_advisor/agents/optimization.py (Optimization)
    ↓
src/debug_advisor/session.py (Session Tracking)
    ↓
src/debug_advisor/guardrails/ (Validation)
```

### Key Dependencies

- **`orchestrator.py`** depends on:
  - `agents/analysis/agent.py`
  - `agents/explanation.py`
  - `agents/hints.py`
  - `agents/optimization.py`
  - `session.py`
  - `guardrails/`

- **`agents/analysis/agent.py`** depends on:
  - `agents/analysis/syntax.py`
  - `agents/analysis/linters.py`
  - `agents/analysis/metrics.py`
  - `agents/analysis/rules/registry.py`

- **`agents/analysis/rules/registry.py`** depends on:
  - `agents/analysis/rules/base.py`
  - `agents/analysis/rules/logic.py`
  - `agents/analysis/rules/structural.py`
  - `agents/analysis/rules/style.py`

- **`llm/`** depends on:
  - `llm/base.py` (interface)
  - `llm/prompts.py` (template management)

## Configuration Files

### `.env.example`
Template for environment variables:
```
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name
```

### `pyproject.toml`
Main project configuration:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "debug-advisor"
version = "0.1.0"
description = "AI-powered code debugging advisor with graded hints"
requires-python = ">=3.11"
dependencies = [
    "typer>=0.9",
    "rich>=13",
    "jinja2>=3.1",
    "python-dotenv>=1.0",
    "ruff>=0.4",
    "radon>=6",
    "pyflakes>=3",
]

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### `Makefile`
Development commands:
```makefile
install:
	pip install -e ".[dev]"

test:
	pytest

lint:
	ruff check src/

format:
	ruff format src/
```

## Summary

The project is organized following a clean architecture pattern with:

1. **Presentation Layer**: `app.py`, `cli.py`
2. **Application Layer**: `orchestrator.py`, `session.py`
3. **Domain Layer**: `agents/`, `models.py`
4. **Infrastructure Layer**: `llm/`, `guardrails/`
5. **Supporting**: `docs/`, `tests/`, `eval/`, `prompts/`, `samples/`

This structure ensures maintainability, testability, and extensibility for future enhancements.

---

*Co-authored-by: Claude Code <noreply@anthropic.com>*

🤖 Generated with [Claude Code](https://claude.com/claude-code)