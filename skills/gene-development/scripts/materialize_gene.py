#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

GENES_ROOT_DEFAULT = Path.home() / ".agents" / "genes"
UNIQUENESS_SRC_DEFAULT = (
    Path.home() / "Overlord" / "projects" / "libs" / "uniqueness" / "src"
)


def main() -> int:
    args = parse_args()
    candidate, confidence = load_candidate(args)
    proposed_id = str(candidate.get("proposed_id", "")).strip()
    gene_id = allocate_gene_id(args.genes_root, proposed_id)
    gene_path = args.genes_root / "staging" / gene_id

    gene_path.mkdir(parents=True, exist_ok=False)
    (gene_path / "snippets").mkdir(parents=True, exist_ok=True)

    timestamp = timestamp_iso()
    embedding = {}
    if args.with_embedding:
        embedding = build_embedding(candidate, args.model, args.uniqueness_src)

    gene_json = {
        "id": gene_id,
        "title": candidate.get("title", ""),
        "summary": candidate.get("summary", ""),
        "tags": candidate.get("tags", []),
        "languages": candidate.get("languages", []),
        "status": "staging",
        "created_at": timestamp,
        "updated_at": timestamp,
        "aliases": [],
        "provenance": sanitize_provenance(candidate.get("provenance", [])),
        "embedding": embedding,
    }

    (gene_path / "gene.json").write_text(
        json.dumps(gene_json, indent=2, ensure_ascii=True) + "\n", encoding="utf-8"
    )
    (gene_path / "notes.md").write_text(
        build_notes_markdown(candidate, confidence), encoding="utf-8"
    )
    write_snippets(gene_path, candidate)

    print(f"Materialized staged gene: {gene_path}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Materialize gene folder from JSON or Markdown draft"
    )
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--input",
        type=Path,
        help="Path to strict gene-scout JSON output",
    )
    input_group.add_argument(
        "--input-md",
        type=str,
        help=(
            "Markdown draft input path, or '-' to read from stdin. "
            "The draft must start with JSON frontmatter delimited by --- lines."
        ),
    )
    parser.add_argument(
        "--genes-root",
        type=Path,
        default=GENES_ROOT_DEFAULT,
        help="Root directory containing staging/ and confirmed/",
    )
    parser.add_argument(
        "--with-embedding",
        action="store_true",
        help="Compute and store embedding in gene.json",
    )
    parser.add_argument(
        "--model",
        default="all-MiniLM-L6-v2",
        help="Sentence-transformers model name",
    )
    parser.add_argument(
        "--uniqueness-src",
        type=Path,
        default=UNIQUENESS_SRC_DEFAULT,
        help="Path to uniqueness/src for local embedder import",
    )
    return parser.parse_args()


def allocate_gene_id(genes_root: Path, proposed_id: str) -> str:
    staging_root = genes_root / "staging"
    confirmed_root = genes_root / "confirmed"
    base_id = sanitize_gene_id(proposed_id)
    candidate_id = base_id
    index = 2
    while (staging_root / candidate_id).exists() or (
        confirmed_root / candidate_id
    ).exists():
        candidate_id = f"{base_id}--{index}"
        index += 1
    return candidate_id


def load_candidate(args: argparse.Namespace) -> tuple[dict, object]:
    if args.input is not None:
        return load_candidate_from_json(args.input)
    if args.input_md is not None:
        return load_candidate_from_markdown(args.input_md)
    raise ValueError("One of --input or --input-md is required")


def load_candidate_from_json(input_path: Path) -> tuple[dict, object]:
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    result = payload.get("result", {})
    if result.get("status") != "found":
        raise ValueError("Input status is not 'found'; nothing materialized")
    candidate = result.get("gene_candidate", {})
    if not isinstance(candidate, dict):
        raise ValueError("JSON input is missing result.gene_candidate object")
    return candidate, result.get("confidence", "")


def load_candidate_from_markdown(input_md: str) -> tuple[dict, object]:
    markdown_text = (
        sys.stdin.read()
        if input_md == "-"
        else Path(input_md).read_text(encoding="utf-8")
    )
    frontmatter = parse_markdown_frontmatter(markdown_text)
    candidate_raw = frontmatter.get("gene_candidate", frontmatter)
    if not isinstance(candidate_raw, dict):
        raise ValueError("Markdown frontmatter must define a gene candidate object")
    return candidate_raw, frontmatter.get("confidence", "")


def parse_markdown_frontmatter(markdown_text: str) -> dict:
    if not markdown_text.startswith("---\n"):
        raise ValueError(
            "Markdown draft must start with frontmatter delimited by --- lines"
        )

    lines = markdown_text.splitlines()
    end_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break
    if end_index is None:
        raise ValueError("Markdown draft frontmatter is missing closing --- delimiter")

    frontmatter_text = "\n".join(lines[1:end_index]).strip()
    if not frontmatter_text:
        raise ValueError("Markdown draft frontmatter is empty")
    try:
        frontmatter = json.loads(frontmatter_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Markdown frontmatter must be strict JSON for machine parsing"
        ) from exc

    if not isinstance(frontmatter, dict):
        raise ValueError("Markdown frontmatter JSON must decode to an object")
    return frontmatter


def sanitize_gene_id(value: str) -> str:
    value_clean = value.strip().lower()
    if not value_clean:
        return "gene.untitled"

    value_clean = re.sub(r"[^a-z0-9.-]+", "-", value_clean)
    value_clean = re.sub(r"-{2,}", "-", value_clean)
    value_clean = value_clean.strip("-.")

    if "." not in value_clean:
        value_clean = f"gene.{value_clean}"
    if not re.match(
        r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*(?:\.[a-z][a-z0-9]*(?:-[a-z0-9]+)*)*$",
        value_clean,
    ):
        return "gene.untitled"
    return value_clean


def build_embedding(candidate: dict, model: str, uniqueness_src: Path) -> dict:
    import sys

    if str(uniqueness_src) not in sys.path:
        sys.path.insert(0, str(uniqueness_src))

    from uniqueness import SentenceTransformerEmbedder  # type: ignore[import-not-found]

    embedding_text = build_embedding_text(candidate)
    embedder = SentenceTransformerEmbedder(model)
    vector_wrapped = embedder.embed([embedding_text])
    vector = vector_wrapped[0] if vector_wrapped else []
    return {
        "model": model,
        "dimension": len(vector),
        "metric": "cosine",
        "text": embedding_text,
        "vector": vector,
    }


def build_embedding_text(candidate: dict) -> str:
    parts = [
        str(candidate.get("proposed_id", "")),
        str(candidate.get("title", "")),
        str(candidate.get("summary", "")),
    ]
    tags = candidate.get("tags")
    if isinstance(tags, list):
        parts.extend(str(tag) for tag in tags)
    return " ".join(part for part in parts if part).strip()


def build_pattern_markdown(candidate: dict) -> list[str]:
    pattern_lines = ["## Pattern", ""]
    steps = candidate.get("pattern_spec", [])
    if isinstance(steps, list) and steps:
        for index, step in enumerate(steps, start=1):
            pattern_lines.append(f"{index}. {step}")
    else:
        pattern_lines.append("1. No pattern steps were provided.")
    return pattern_lines


def build_notes_markdown(candidate: dict, confidence: object) -> str:
    invariants = candidate.get("invariants", [])
    edge_cases = candidate.get("edge_cases", [])
    pitfalls = candidate.get("pitfalls", [])
    gaps = candidate.get("gaps", [])

    lines = [
        "# Notes",
        "",
        f"- Confidence: {confidence}",
        f"- Generated: {timestamp_iso()}",
        "- Scope: Language-agnostic. Put language-specific guidance in snippets/<lang>/notes.md",
        "",
    ]
    lines.extend(build_pattern_markdown(candidate))
    lines.append("")
    lines.append("## Invariants")
    lines.extend(format_list(invariants))
    lines.append("")
    lines.append("## Edge Cases")
    lines.extend(format_list(edge_cases))
    lines.append("")
    lines.append("## Pitfalls")
    lines.extend(format_list(pitfalls))
    lines.append("")
    lines.append("## Gaps")
    lines.extend(format_list(gaps))
    lines.append("")
    lines.append("## Post-Use Notes")
    lines.append("- Add runtime surprises, breakages, or confusing behavior here.")
    lines.append("- If package/API drift breaks snippets, record the fix guidance.")
    lines.append("")
    return "\n".join(lines)


def format_list(values: object) -> list[str]:
    if not isinstance(values, list) or not values:
        return ["- (none)"]
    return [f"- {value}" for value in values]


def write_snippets(gene_path: Path, candidate: dict) -> None:
    snippets_by_language = candidate.get("snippets_by_language", {})
    if not isinstance(snippets_by_language, dict):
        return

    for language, snippets in snippets_by_language.items():
        language_name = str(language).strip()
        language_key = language_name.lower() if language_name else "unknown"
        language_dir = gene_path / "snippets" / language_key
        language_dir.mkdir(parents=True, exist_ok=True)
        if not isinstance(snippets, list):
            continue

        ensure_language_notes(language_dir, language_name, snippets)

        for index, snippet in enumerate(snippets, start=1):
            if not isinstance(snippet, dict):
                continue
            symbol = str(snippet.get("symbol", f"snippet-{index}"))
            symbol_clean = re.sub(r"[^a-zA-Z0-9._-]+", "-", symbol).strip("-")
            file_name = f"{index:02d}-{symbol_clean or 'snippet'}.md"
            file_path = language_dir / file_name
            code_block = str(snippet.get("code", "")).strip()
            fence_lang = language_key if language_key != "unknown" else ""
            body = [
                f"# {symbol}",
                "",
                f"- Source Note: {snippet.get('source_note', '')}",
                f"- Why Relevant: {snippet.get('why_relevant', '')}",
                "",
                f"```{fence_lang}",
                code_block,
                "```",
                "",
            ]
            file_path.write_text("\n".join(body), encoding="utf-8")


def ensure_language_notes(
    language_dir: Path, language_name: str, snippets: list[object]
) -> None:
    notes_path = language_dir / "notes.md"
    if notes_path.exists():
        return

    title_lang = language_name.strip() or "Language"
    lines: list[str] = [
        f"# {title_lang} Notes",
        "",
        f"- Generated: {timestamp_iso()}",
        "",
        "## Purpose",
        "",
        "This file is for language-specific implementation guidance for this gene.",
        "Keep the top-level notes.md language-agnostic; put library/framework details here.",
        "",
        "## Snippet Index",
        "",
    ]

    snippet_lines: list[str] = []
    for index, snippet in enumerate(snippets, start=1):
        if not isinstance(snippet, dict):
            continue
        symbol = (
            str(snippet.get("symbol", f"snippet-{index}")).strip() or f"snippet-{index}"
        )
        symbol_clean = re.sub(r"[^a-zA-Z0-9._-]+", "-", symbol).strip("-")
        file_name = f"{index:02d}-{symbol_clean or 'snippet'}.md"
        why = str(snippet.get("why_relevant", "")).strip()
        if why:
            snippet_lines.append(f"- `{file_name}` ({symbol}) - {why}")
        else:
            snippet_lines.append(f"- `{file_name}` ({symbol})")
    lines.extend(snippet_lines or ["- (none)"])

    lines.extend(
        [
            "",
            "## Integration Checklist",
            "",
            "- Identify required dependencies and versions.",
            "- Map the gene's inputs/outputs to your application's types and error model.",
            "- Decide lifecycle ownership (init/start/stop) for any background tasks/resources.",
            "- Add tests for invariants and edge cases described in the top-level notes.md.",
            "",
            "## Dependency / Runtime Notes",
            "",
            "- Record framework assumptions (event loop, threads, runtime).",
            "- Record configuration defaults that materially affect behavior.",
            "",
            "## Post-Use Notes",
            "",
            "- Add language-specific surprises, breakages, or gotchas here.",
            "",
        ]
    )

    notes_path.write_text("\n".join(lines), encoding="utf-8")


def sanitize_provenance(provenance_raw: object) -> list[dict]:
    if not isinstance(provenance_raw, list):
        return []

    provenance_clean: list[dict] = []
    for item in provenance_raw:
        if not isinstance(item, dict):
            continue
        origin_note = str(item.get("origin_note", "")).strip()
        if not origin_note:
            origin_note = "Extracted from local source analysis"
        symbols = item.get("symbols", [])
        search_terms = item.get("search_terms", [])
        provenance_clean.append(
            {
                "origin_note": origin_note,
                "symbols": symbols if isinstance(symbols, list) else [],
                "search_terms": search_terms if isinstance(search_terms, list) else [],
                "captured_at": timestamp_iso(),
            }
        )
    return provenance_clean


def timestamp_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
