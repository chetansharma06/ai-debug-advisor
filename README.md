# AI Bug & Debugging Advisor

A debugging advisor that analyzes buggy code and produces a graded hint ladder (levels 1–5) so developers can fix issues without the fix being leaked in earlier hints.

## Quick Start

```bash
source venv/bin/activate   # or venv\\Scripts\\activate on Windows
pip install -e ".[dev]"
python -m debug_advisor --help
```

## Streamlit UI

```bash
streamlit run streamlit_app.py
```

## Project Overview

The AI Bug & Debugging Advisor is an innovative AI-powered tool designed to help developers identify and fix code bugs while providing educational guidance. The system analyzes Python code snippets, detects issues using static analysis, and provides a structured hint system that gradually reveals the solution without giving away the complete fix.

## Key Features

- **Static Analysis**: Comprehensive bug detection using AST parsing, linting, and code metrics
- **Graded Hint System**: Five-level hint ladder (Level 1 = gentle nudge, Level 5 = complete solution)
- **Code Explanations**: Human-readable explanations of detected issues
- **Leak Detection**: Security-conscious hints that never reveal complete fixes in early levels
- **Session Tracking**: Persists hint progress across multiple interactions
- **Multi-LLM Support**: Works with various LLM backends (GitHub Copilot, stub clients)

## Installation

1. Clone this repository
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\\Scripts\\activate on Windows
   ```
3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
4. Configure environment variables (see `.env.example`)

## Usage

### Command Line Interface

```bash
python -m debug_advisor analyze "buggy_code.py"
```

### Streamlit Web Interface

```bash
streamlit run streamlit_app.py
```

## How It Works

The advisor runs a four-stage pipeline on Python snippets:

1. **Static Analysis** (`src/debug_advisor/agents/analysis/`)
   - Syntax analysis using Python's `ast` module
   - Linting with Ruff/Pyflakes integration
   - Code metrics with Radon complexity analysis
   - Rule engine for Logic, Structural, and Style violations

2. **Explanation** (`src/debug_advisor/agents/explanation.py`)
   - Generates human-readable explanations of detected issues
   - Uses LLM templates for natural language explanations

3. **Hint Ladder** (`src/debug_advisor/agents/hints.py`)
   - Produces five graded hint levels
   - Level 1: Gentle nudges toward the fix
   - Level 5: Complete corrected code (with proper leak detection)

4. **Optimization** (`src/debug_advisor/agents/optimization.py`)
   - Generates optimized/fixed code versions
   - Currently provides comment-based improvements

## Technology Stack

- **Core Language**: Python 3.11+
- **Static Analysis**: Python's `ast` module, Ruff, Radon, Pyflakes
- **LLM Integration**: GitHub Copilot API, custom stub clients
- **Web Interface**: Streamlit
- **Configuration**: `.env` files, Python-dotenv
- **Testing**: pytest, ruff for linting
- **Build System**: Hatch
- **Version Control**: Git

## Project Structure

```
ai-debug-advisor/
├── .github/              # GitHub workflows and instructions
├── docs/                 # Documentation (architecture, rules, evaluation)
├── eval/                 # Evaluation dataset and scripts
├── prompts/              # LLM prompt templates (Jinja2)
├── samples/              # Example buggy and clean code
├── src/debug_advisor/    # Main source code
│   ├── agents/          # AI agents for different tasks
│   ├── llm/             # LLM client implementations
│   ├── guardrails/      # Safety and validation systems
│   ├── session.py       # Session management
│   └── orchestrator.py  # Pipeline coordination
├── tests/                # Test suite
├── app.py                # Streamlit web app
├── Makefile              # Development commands
├── pyproject.toml        # Project configuration
├── README.md             # This file
└── .env.example          # Environment configuration template
```

## Architecture

### System Architecture

The system follows a microservices-like architecture with clear separation of concerns:

**Frontend Layer (Web/UI)**
- Streamlit interface for user interaction
- Command-line interface for programmatic access
- Session management for persistent user state

**AI Processing Layer**
- Static Analysis Agent: Detects bugs using multiple techniques
- Explanation Agent: Generates human-readable descriptions
- Hint Generation Agent: Creates educational hints with progressive disclosure
- Optimization Agent: Produces fixed code versions

**Integration Layer**
- Orchestrator: Coordinates the entire pipeline
- Session Manager: Tracks user progress and state
- Guardrails: Ensures safety and prevents information leakage

**LLM Layer**
- Provider interfaces for different LLM backends
- Prompt templates for consistent interactions
- Response validation and processing

### Technical Architecture

The technical architecture is built around:

1. **Pipeline Processing**: Sequential stages where each stage builds on previous results
2. **Rule-Based Detection**: Extensive rule engine for code analysis
3. **Progressive Disclosure**: Educational approach through hint levels
4. **Security by Design**: Comprehensive leak detection and validation
5. **Extensibility**: Modular design allowing for new analysis techniques and LLMs

### Key Components

#### 1. Static Analysis Engine
Located in `src/debug_advisor/agents/analysis/`:

- **Syntax Analyzer**: `src/debug_advisor/agents/analysis/syntax.py`
  - Uses Python's `ast` module for syntax validation
  - Provides precise error location and type detection

- **Linter Adapter**: `src/debug_advisor/agents/analysis/linters.py`
  - Integration with Ruff and Pyflakes
  - Configurable linting rules and severity levels

- **Metrics Agent**: `src/debug_advisor/agents/analysis/metrics.py`
  - Complexity analysis using Radon
  - Cyclomatic complexity calculations
  - Performance metrics

- **Rules Registry**: `src/debug_advisor/agents/analysis/rules/`
  - Logic rules: Mutable default arguments, etc.
  - Structural rules: Unused imports, dead code
  - Style rules: Naming conventions, formatting

#### 2. Hint Generation System
Located in `src/debug_advisor/agents/hints.py`:

- **Hint Levels**: Five-tiered hint system (1-5)
- **Leak Detection**: `src/debug_advisor/guardrails/leak_detector.py`
  - Regex-based validation to prevent fix disclosure
  - Content filtering and security checks
- **Session Tracking**: `src/debug_advisor/session.py`
  - Persistent hint level tracking per session
  - User progress management

#### 3. LLM Integration
Located in `src/debug_advisor/llm/`:

- **Base Interface**: `src/debug_advisor/llm/base.py`
  - Abstract `LLMClient` protocol
  - Common interface for all providers

- **Implementations**:
  - `StubLLMClient`: Deterministic offline client for testing
  - `CopilotClient`: GitHub Copilot API integration

- **Prompt Templates**: `src/debug_advisor/llm/prompts.py`
  - Jinja2 templates for consistent LLM interactions
  - Template versioning for reproducibility

#### 4. Guardrails and Validation
Located in `src/debug_advisor/guardrails/`:

- **Leak Detector**: Prevents hint leakage
- **Output Validator**: Validates LLM responses against schemas

## Security

The system incorporates several security measures:

1. **Leak Detection**: All hints are validated to ensure they don't reveal complete fixes
2. **Input Validation**: Code snippets are validated before processing
3. **Output Sanitization**: LLM responses are sanitized and validated
4. **Access Controls**: Environment-based configuration for different deployment scenarios

## Development

### Project Setup

1. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Lint code:
   ```bash
   ruff check src/
   ```

4. Format code:
   ```bash
   ruff format src/
   ```

### Running Tests

```bash
pytest
pytest tests/unit/
pytest tests/integration/
```

### Code Standards

- **Linting**: ruff with line length 88
- **Testing**: pytest with comprehensive test coverage
- **Documentation**: Markdown files with architectural diagrams
- **Code Quality**: Type hints, comprehensive error handling

## Evaluation

The project includes an evaluation system in the `eval/` directory:

- **Dataset**: `eval/dataset.jsonl` containing labeled buggy code samples
- **Evaluation Scripts**: `eval/run_eval.py` for testing system performance
- **Metrics**: Quantitative assessment of hint quality and effectiveness

## Configuration

Copy `.env.example` to `.env` and configure your LLM API keys:

```bash
# Example .env file
LLM_API_KEY=your_api_key_here
LLM_MODEL=your_model_name
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Run linting and tests
6. Submit a pull request

## License

This project is licensed under the terms of the MIT license.

## Contact

For questions, issues, or feedback, please visit the repository or contact the maintainers.

---

*Co-authored-by: Claude Code <noreply@anthropic.com>*

🤖 Generated with [Claude Code](https://claude.com/claude-code)