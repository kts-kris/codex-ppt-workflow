from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml


@dataclass(frozen=True)
class Slide:
    title: str
    goal: str
    bullets: List[str]


@dataclass(frozen=True)
class Deck:
    title: str
    subtitle: str | None
    slides: List[Slide]


def _require(value: Any, field_name: str) -> Any:
    if value is None:
        raise ValueError(f"Missing required field: {field_name}")
    return value


def load_deck(path: str | Path) -> Deck:
    deck_path = Path(path)
    raw = yaml.safe_load(deck_path.read_text(encoding="utf-8")) or {}

    title = _require(raw.get("title"), "title")
    subtitle = raw.get("subtitle")
    slides_raw = _require(raw.get("slides"), "slides")
    slides: List[Slide] = []
    for index, slide in enumerate(slides_raw, start=1):
        if not isinstance(slide, dict):
            raise ValueError(f"Slide {index} must be a mapping")
        slide_title = _require(slide.get("title"), f"slides[{index}].title")
        goal = _require(slide.get("goal"), f"slides[{index}].goal")
        bullets = slide.get("bullets") or []
        if not isinstance(bullets, list):
            raise ValueError(f"slides[{index}].bullets must be a list")
        slides.append(Slide(title=slide_title, goal=goal, bullets=bullets))

    return Deck(title=title, subtitle=subtitle, slides=slides)


def _deck_to_dict(deck: Deck) -> Dict[str, Any]:
    return {
        "title": deck.title,
        "subtitle": deck.subtitle,
        "slides": [
            {"title": slide.title, "goal": slide.goal, "bullets": slide.bullets}
            for slide in deck.slides
        ],
    }


def _deck_to_markdown(deck: Deck) -> str:
    lines = [f"# {deck.title}"]
    if deck.subtitle:
        lines.append(f"_ {deck.subtitle} _")
    lines.append("")

    for idx, slide in enumerate(deck.slides, start=1):
        lines.append(f"## {idx}. {slide.title}")
        lines.append(f"**Goal:** {slide.goal}")
        if slide.bullets:
            lines.append("")
            for bullet in slide.bullets:
                lines.append(f"- {bullet}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def build_outputs(deck: Deck, output_dir: str | Path) -> Dict[str, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "deck.json"
    markdown_path = output_path / "deck.md"

    json_path.write_text(
        json.dumps(_deck_to_dict(deck), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown_path.write_text(_deck_to_markdown(deck), encoding="utf-8")

    return {"json": json_path, "markdown": markdown_path}
