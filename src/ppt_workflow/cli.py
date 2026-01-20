from __future__ import annotations

import argparse
from pathlib import Path

from ppt_workflow.deck_builder import build_outputs, load_deck


def build_command(args: argparse.Namespace) -> None:
    deck = load_deck(args.source)
    outputs = build_outputs(deck, args.output)
    output_lines = [
        f"Wrote {label}: {path}" for label, path in outputs.items()
    ]
    print("\n".join(output_lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build slide deck artifacts from YAML",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build outputs")
    build_parser.add_argument("source", type=Path, help="Path to deck YAML")
    build_parser.add_argument(
        "--output",
        type=Path,
        default=Path("output"),
        help="Directory for build outputs",
    )
    build_parser.set_defaults(func=build_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
