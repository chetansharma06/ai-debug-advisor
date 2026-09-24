"""Entry point for `python -m debug_advisor`."""

from debug_advisor.cli import app


def main() -> None:
    """Run the CLI application."""
    app()


if __name__ == "__main__":
    main()