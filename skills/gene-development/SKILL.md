---
name: gene-development
description: Use when creating or updating genes from local code into the staging gene store (extraction, synthesis, decision gate, materialization, registry rebuild). This is the gene authoring workflow.
version: 0.1.0
---

# Gene Development

Create and refine reusable implementation patterns ("genes") from local repositories, materialize them into the staging store, and rebuild the local gene registry.

This skill is about authoring genes. For searching/applying existing genes, use the `gene-transfusion` skill.

## Scope

- Run multiple `@gene-scout` (read-only) investigations
- Synthesize candidate outputs into a single analysis document for user review
- Decision gate: wait for explicit user selection before materializing anything
- Run post-selection BM25 similarity checks against confirmed + staging genes
- Materialize user-approved candidates into `~/.agents/genes/staging/`
- Rebuild the local registry (include staging)

Out of scope:

- Promotion from `staging/` to `confirmed/` (manual/optional outside this workflow)

## Store Paths

- `~/.agents/genes/staging/`
- `~/.agents/genes/confirmed/`
- `~/.agents/genes/registry.jsonl`

## Workflow

1. Identify the extraction goal and the source roots to inspect.
2. Choose 2-6 parallel `@gene-scout` runs with distinct search angles.
3. Collect strict Markdown locator reports (1-2 findings each, usually 1).
4. Write an analysis document and present it to the user for a decision.
5. Decision gate (required): ask which candidates (if any) to stage.
6. For user-approved candidates only, run BM25 similarity checks with `--include-staging`.
7. Resolve near-duplicate choices (stage variant anyway / improve existing as variant / skip).
8. For approved candidates, materialize them into staging.
9. Rebuild registry with staging included.

## Commands

Materialize one staged gene from a Markdown draft piped via stdin:

```bash
python ~/.agents/skills/gene-development/scripts/materialize_gene.py --input-md -
```

Run BM25 similarity checks against confirmed + staging:

```bash
python ~/.agents/skills/gene-transfusion/scripts/search_genes_bm25.py --query "<candidate query>" --include-staging --top-k 5 --json
```

Rebuild registry including staging:

```bash
python ~/.agents/skills/gene-development/scripts/rebuild_registry.py --include-staging
```

## Agent Integration

- Keep `@gene-scout` read-only; it returns strict Markdown locator reports only.
- Do not write gene folders until the user explicitly selects candidates.
- `pattern_spec`, `invariants`, `edge_cases`, and `pitfalls` should be phrased to remain language-agnostic.
- Language-specific implementation notes belong in `snippets/<lang>/notes.md` and snippet files.
- If user chooses "improve existing", stage a new variant ID; never overwrite an existing gene.

## Additional Resources

- `references/gene-store-spec.md` - Store layout, ID rules, registry schema, notes split policy
- `references/gene-scout-examples.md` - Strict Markdown locator examples and quality rules
- `references/gene-analysis-template.md` - Standard synthesis template for user review + decision gate
