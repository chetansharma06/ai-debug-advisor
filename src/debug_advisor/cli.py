"""Typer CLI with Rich formatting."""

import typer
from rich.console import Console
from rich.syntax import Syntax

from debug_advisor.config import Settings
from debug_advisor.llm.copilot_client import CopilotClient
from debug_advisor.llm.stub_client import StubLLMClient
from debug_advisor.orchestrator import DebugAdvisor

app = typer.Typer(add_completion=False)
console = Console()


@app.command()
def analyze(
    file: typer.FileText = typer.Argument(..., help="Python file to analyze"),
    use_stub: bool = typer.Option(True, help="Use deterministic stub LLM"),
) -> None:
    """Analyze a Python file and show findings + hints."""
    code = file.read()
    console.print(f"Analyzing {file.name}...\n")

    # Select LLM backend
    if use_stub:
        llm = StubLLMClient()
    else:
        settings = Settings.from_env()
        llm = CopilotClient(settings.llm_api_key)

    advisor = DebugAdvisor(llm)
    result = advisor.run(code)

    if not result.findings:
        console.print("[green]No issues found![/green]")
        return

    for finding in result.findings:
        console.print(f"[bold red]Finding:[/bold red] {finding.message}")
        console.print(f"  Line {finding.span.start_line}, severity: {finding.severity}")

    if result.explanation:
        console.print(f"\n[bold blue]Explanation:[/bold blue] {result.explanation.body}")

    if result.hints:
        console.print("\n[bold yellow]Hints:[/bold yellow]")
        for hint in result.hints:
            console.print(f"  Level {hint.level}: {hint.text}")

    if result.optimized_code:
        console.print("\n[bold green]Optimized code:[/bold green]")
        console.print(Syntax(result.optimized_code, "python", theme="monokai"))


if __name__ == "__main__":
    app()