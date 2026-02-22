---
name: gene-transfusion
description: Use when searching, reading, and applying existing genes (reusable implementation patterns), and recording post-use feedback.
version: 0.1.0
---

# Gene Transfusion

Search, read, and apply existing genes (reusable implementation patterns) from the local gene library.

This skill is about using genes. For creating/staging genes from source code, use the `gene-development` skill (and `/gene/create`).

Use two retrieval paths:
- Embedding search for semantic matching (`search_genes.py`)
- BM25 lexical search for fast keyword matching (`search_genes_bm25.py`)

## When to Use

Use this skill when:
- You want to find an existing gene by natural-language description or keywords
- You want to adapt a stored pattern to a new project/language
- You want to append post-use feedback when a gene was confusing or broke due to drift

## Scope

- Search genes via embedding similarity or BM25
- Read and apply gene artifacts (notes + snippets)
- Append post-use notes for significant impediments

Out of scope:

- Gene extraction and staging (see `gene-development`)
- Registry rebuild (see `gene-development`)

## Fast Workflow

1. Search for a gene that matches the problem.
2. Open the gene folder and read `notes.md` first (language-agnostic).
3. Read `snippets/<lang>/notes.md` (if present), then the snippet files.
4. Apply the pattern in your codebase, adapting to your language/runtime.
5. If something was confusing or broke due to drift, append a post-use note.

## Commands

Use the scripts in `scripts/`.

Search genes by description:

```bash
python ~/.agents/skills/gene-transfusion/scripts/search_genes.py \
  --query "idempotent upsert with conflict retry" \
  --json \
  --top-k 5
```

Search confirmed plus staging:

```bash
python ~/.agents/skills/gene-transfusion/scripts/search_genes.py \
  --query "batch deduplication with cosine similarity" \
  --include-staging \
  --json \
  --top-k 8
```

Search with BM25 (keywords, no embeddings):

```bash
python ~/.agents/skills/gene-transfusion/scripts/search_genes_bm25.py \
  --query "dedup cosine threshold batch" \
  --include-staging \
  --json \
  --top-k 8
```

Enable verbose model logs only when debugging:

```bash
python ~/.agents/skills/gene-transfusion/scripts/search_genes.py \
  --query "batch deduplication with cosine similarity" \
  --show-model-logs
```

Append a post-use issue note when the gene impeded implementation:

```bash
python ~/.agents/skills/gene-transfusion/scripts/append_gene_note.py \
  --gene-id dedupe.cosine-batch \
  --category confusing \
  --note "Threshold behavior was unclear for near-ties at 0.70"
```

## Gene Store

Canonical store paths:
- `~/.agents/genes/staging/`
- `~/.agents/genes/confirmed/`
- `~/.agents/genes/registry.jsonl`

Default search behavior:
- Search `confirmed` only
- Include `staging` with `--include-staging`

## How to Load a Gene

1. Run search and pick a top match by score.
2. Open the reported `location` directory.
3. Read `notes.md` first; it must be language-agnostic and start with the pattern.
4. Read `snippets/<lang>/notes.md` (if present) for language-specific notes and integration guidance.
5. Read `snippets/<lang>/` snippet files for source-backed exemplars.
6. Use invariants, edge cases, pitfalls, and post-use notes to adapt safely.

Use `staging/` while iterating on candidate genes. Use `confirmed/` for production reuse.

## Failure Handling Expectations

- If a confirmed gene fails due to dependency deprecation or runtime/API drift, immediately tell the user.
- Suggest specific edits in three areas: code snippet, explanation (pattern/notes), and metadata.
- After use, append any surprising behavior, confusion, or runtime issue to `notes.md` under a post-use section.

Use `append_gene_note.py` only for significant impediments:
- Confusing or contradictory guidance
- Unexpected, undocumented edge cases
- Runtime failures or dependency/API drift that blocks progress

## Additional Resources

- `~/.agents/skills/gene-development/references/gene-store-spec.md` - Store layout, ID rules, registry schema, notes split policy
