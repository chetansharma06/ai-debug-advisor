"""Project-local Streamlit application entry point with autonomous agent panel.

The app provides a split-view editor: the left column holds the code editor,
the right column is an autonomous "Agent" panel that shows live status,
findings, explanation, the hint ladder, and optimized code.

Key behaviours:
- No "Analyze" button — the pipeline auto-runs on code change.
- Debounce is achieved via st.fragment + code-hash caching in SessionState:
  the fragment re-runs on input change, but the heavy pipeline only runs once
  per unique code snippet.
- The orchestrator's autonomous chaining logic (analysis -> explanation ->
  hints -> optimization-only-if-high-severity) is encoded in
  orchestrator.py, not the UI.
- If no LLM key is configured, the app silently falls back to StubLLMClient.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from debug_advisor.config import Settings
from debug_advisor.llm.copilot_client import CopilotClient
from debug_advisor.llm.stub_client import StubLLMClient
from debug_advisor.models import PipelineResult
from debug_advisor.orchestrator import DebugAdvisor
from debug_advisor.session import SessionState

st.set_page_config(page_title="AI Bug & Debugging Advisor", page_icon="🐞", layout="wide")

DEFAULT_CODE = '''def process_items(items=[]):
    """Process items, accumulating across calls."""
    processed = items.copy()
    processed.append("processed")
    return processed


if __name__ == "__main__":
    print(process_items())
    print(process_items())
'''


# ---------------------------------------------------------------------------
# LLM client selection (silent fallback to stub when no key is configured)
# ---------------------------------------------------------------------------

def _get_llm_client():
    """Return a CopilotClient if an API key is configured, else StubLLMClient.

    Any failure during CopilotClient construction falls back silently to
    the stub so the user never sees an error.
    """
    settings = Settings.from_env()
    if settings.llm_api_key:
        try:
            return CopilotClient(settings.llm_api_key)
        except Exception:
            return StubLLMClient()
    return StubLLMClient()


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def _get_session() -> SessionState:
    if "session" not in st.session_state:
        st.session_state.session = SessionState()
    return st.session_state.session


def _get_advisor() -> DebugAdvisor:
    if "advisor" not in st.session_state:
        st.session_state.advisor = DebugAdvisor(_get_llm_client())
    return st.session_state.advisor


# ---------------------------------------------------------------------------
# Public analysis API (used by tests and the Streamlit fragment)
# ---------------------------------------------------------------------------

def analyze_code(code: str) -> PipelineResult:
    """Run the project analysis pipeline on a snippet.

    Uses the autonomous chaining logic (analysis -> explanation -> hints
    -> optimization-only-if-high-severity). Falls back to StubLLMClient
    when no API key is configured.
    """
    advisor = DebugAdvisor(_get_llm_client())
    return advisor.run_autonomous(code)


# ---------------------------------------------------------------------------
# Debounced autonomous analysis
# ---------------------------------------------------------------------------

@st.fragment
def _auto_analyze(code: str) -> None:
    """Run the autonomous pipeline on code change.

    Debounce strategy: the fragment re-runs on every input change, but the
    actual analysis is cached per code hash in SessionState. Unchanged code
    returns the cached result instantly, so the heavy pipeline only runs
    once per unique snippet — giving the user a "debounced" feel without
    needing real timers.
    """
    session = _get_session()
    advisor = _get_advisor()

    # No-repeat work: cache results per code hash.
    cached = session.get_cached_result(code)
    if cached is not None:
        st.session_state.result = cached
        st.session_state.status = "Idle (cached)"
        return

    # Show live status while running.
    st.session_state.status = "Analyzing..."

    result = advisor.run_autonomous(code)
    session.cache_result(code, result)
    st.session_state.result = result

    if result.findings:
        st.session_state.status = f"Found {len(result.findings)} issue(s)"
    else:
        st.session_state.status = "No issues found"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.title("AI Bug & Debugging Advisor")
st.caption("Paste Python code — the agent analyzes it automatically as you type.")

# Status bar (updated by the fragment)
status_placeholder = st.empty()

# Split view: code editor (left) | agent panel (right)
col_editor, col_agent = st.columns([2, 1])

with col_editor:
    code = st.text_area(
        "Python source",
        value=DEFAULT_CODE,
        height=500,
        key="code_input",
        help="Edit this code. The agent analyzes it automatically.",
    )

with col_agent:
    st.markdown("### 🤖 Agent")
    agent_panel = st.empty()

# Trigger autonomous analysis on code change (debounce handled by fragment).
_auto_analyze(code)

# Render status bar
status_placeholder.caption(f"Status: {st.session_state.get('status', 'Watching...')}")

# Render agent panel
with agent_panel.container():
    result: PipelineResult | None = st.session_state.get("result")
    if result is None:
        st.info("Waiting for analysis...")
    else:
        if not result.findings:
            st.success("✅ No issues found in the provided code.")
        else:
            st.warning(f"⚠️ {len(result.findings)} issue(s) detected")
            for finding in result.findings:
                with st.expander(
                    f"Line {finding.span.start_line} — {finding.message}",
                    expanded=True,
                ):
                    st.caption(f"Severity: {finding.severity}")
                    if finding.rule_id:
                        st.caption(f"Rule: {finding.rule_id}")

            if result.explanation:
                st.subheader("Explanation")
                st.write(result.explanation.body)

            if result.hints:
                st.subheader("Hint ladder")
                for hint in result.hints:
                    st.markdown(f"**Level {hint.level}:** {hint.text}")

            if result.optimized_code:
                st.subheader("Optimized code")
                st.code(result.optimized_code, language="python")