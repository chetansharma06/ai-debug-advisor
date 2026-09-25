"""Top-level pipeline that coordinates analysis, explanation, and hints."""

from debug_advisor.agents.analysis.agent import CodeAnalysisAgent
from debug_advisor.agents.explanation import ErrorExplanationAgent
from debug_advisor.agents.hints import HintGenerationAgent
from debug_advisor.agents.optimization import CodeOptimizationAgent
from debug_advisor.llm.base import LLMClient
from debug_advisor.models import Finding, PipelineResult


class DebugAdvisor:
    """Runs the full debugging pipeline for one code snippet.

    The original ``run()`` method executes all four stages unconditionally
    (analysis -> explanation -> hints -> optimization) and is kept
    unchanged so the CLI, tests, and any existing callers continue to work.

    The autonomous variant ``run_autonomous()`` implements the decision
    logic for the live Streamlit agent panel:

    1. Always run CodeAnalysisAgent first.
    2. If findings exist, auto-chain into ErrorExplanationAgent and
       HintGenerationAgent (no manual trigger required).
    3. Only auto-call CodeOptimizationAgent when a finding's severity is
       high ("high" or "error"). Low/medium findings still get hints and
       explanations but do not trigger an optimized-code rewrite.
    """

    def __init__(self, llm: LLMClient) -> None:
        self.analysis = CodeAnalysisAgent()
        self.explanation = ErrorExplanationAgent(llm)
        self.hints = HintGenerationAgent(llm)
        self.optimization = CodeOptimizationAgent(llm)

    def run(self, code: str) -> PipelineResult:
        """Run all four stages unconditionally (original behaviour, unchanged)."""
        findings = self.analysis.analyze(code)
        explanation = self.explanation.explain(code, findings)
        hints = self.hints.generate(code, findings)
        optimized_code = self.optimization.optimize(code)
        return PipelineResult(
            findings=findings,
            explanation=explanation,
            hints=hints,
            optimized_code=optimized_code,
        )

    def run_autonomous(self, code: str) -> PipelineResult:
        """Run the pipeline with autonomous chaining rules.

        Encodes the decision logic here (not in the UI) so the agent panel
        can call a single method and get the correct behaviour without
        needing to orchestrate agents itself.
        """
        # Stage 1: Always run analysis first.
        findings: list[Finding] = self.analysis.analyze(code)

        explanation = None
        hints = []
        optimized_code = None

        if findings:
            # Stage 2: Auto-chain explanation + hints when findings exist.
            explanation = self.explanation.explain(code, findings)
            hints = self.hints.generate(code, findings)

            # Stage 3: Only auto-call optimization when severity is high.
            if self._has_high_severity(findings):
                optimized_code = self.optimization.optimize(code)

        return PipelineResult(
            findings=findings,
            explanation=explanation,
            hints=hints,
            optimized_code=optimized_code,
        )

    @staticmethod
    def _has_high_severity(findings: list[Finding]) -> bool:
        """Return True if any finding has severity 'high' or 'error'."""
        return any(f.severity in ("high", "error") for f in findings)