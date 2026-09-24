"""Project-local Streamlit application entry point."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import streamlit as st

from debug_advisor.llm.stub_client import StubLLMClient
from debug_advisor.orchestrator import DebugAdvisor

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


@st.cache_data
def analyze_code(code: str):
    """Run the project analysis pipeline on a snippet."""
    advisor = DebugAdvisor(StubLLMClient())
    return advisor.run(code)


st.title("AI Bug & Debugging Advisor")
st.caption("Paste Python code to check for bugs, read explanations, and view a hint ladder.")

with st.sidebar:
    st.markdown("### Project setup")
    st.info("Running in stub mode for offline analysis using the repository's existing pipeline.")

code = st.text_area(
    "Python source",
    value=DEFAULT_CODE,
    height=400,
    help="Paste Python code to analyze.",
)

if st.button("Analyze code", type="primary"):
    with st.spinner("Analyzing..."):
        result = analyze_code(code)

    if not result.findings:
        st.success("No issues found in the provided code.")
    else:
        st.subheader("Findings")
        for finding in result.findings:
            st.markdown(f"### {finding.message}")
            st.caption(f"Line {finding.span.start_line} • Severity: {finding.severity}")

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
