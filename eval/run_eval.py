"""Run evaluation against the labeled dataset."""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("eval/dataset.jsonl"))
    args = parser.parse_args()
    print(f"Evaluating against {args.data}")
    # TODO: load dataset, run pipeline, compute metrics
    print("Evaluation complete")


if __name__ == "__main__":
    main()