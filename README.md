# Codex PPT Workflow

A lightweight workflow for drafting slide decks from structured YAML. This repo includes a simple CLI that converts a YAML deck definition into Markdown and JSON outputs so you can review content before exporting to PowerPoint.

## What's inside

- `src/ppt_workflow/`: Core loader and builder.
- `projects/demo/`: Example project content to extend.
- `output/`: Generated artifacts (gitignored).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

ppt-workflow build projects/demo/deck.yaml --output output
```

## Deck format

`projects/demo/deck.yaml` shows the expected schema:

- `title`: Deck title.
- `subtitle`: Optional deck subtitle.
- `slides`: List of slides, each with a `title`, `goal`, and `bullets`.

You can extend the schema as needed.
