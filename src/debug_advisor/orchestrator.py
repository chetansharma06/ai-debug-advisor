"""Top-level pipeline that coordinates analysis, explanation, and hints."""

from debug_advisor.agents.analysis.agent import CodeAnalysisAgent
from debug_advisor.agents.explanation import ErrorExplanationAgent
from debug_advisor.agents.hints import HintGenerationAgent
from debug_advisor.agents.optimization import CodeOptimizationAgent
from debug_advisor.llm.base import LLMClient
from debug_advisor.models import PipelineResult


class DebugAdvisor:
    """Runs the full debugging pipeline for one code snippet."""

    def __init__(self, llm: LLMClient) -> None:
        self.analysis = CodeAnalysisAgent()
        self.explanation = ErrorExplanationAgent(llm)
        self.hints = HintGenerationAgent(llm)
        self.optimization = CodeOptimizationAgent(llm)

    def run(self, code: str) -> PipelineResult:
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