# Gene Scout Markdown Locator Examples and Quality Rules

Return strict Markdown only. Do not wrap the full response in fences, and do not add narration outside the template.

## Example A: Single High-Signal Finding

```md
# Gene Scout Locator Report

## Request
- Query: generic reuse scan
- Source Roots: /local/repo
- Search Terms: retry, backoff, transient, timeout

## Findings

### Finding 1: Bounded retry loop with failure classification
- Proposed ID: http.retry.bounded-backoff
- Why High Impact: This pattern centralizes transient-failure handling and reduces duplicated retry code across network-facing features.
- Why Reusable: The retry policy and classification are decoupled from transport details, so it can be adapted to API clients, jobs, and queue workers.
- Why Quality: The implementation enforces bounded attempts, explicit delay caps, and clear non-retryable exits.
- Evidence:
  - src/net/retry.py:41 - Defines retryable error classification and terminal error path.
  - src/net/retry.py:67 - Applies capped exponential delay before each subsequent attempt.
  - tests/net/test_retry.py:24 - Verifies non-retryable errors short-circuit without extra attempts.
- Pitfalls / Edge Cases / Risks:
  - Misclassifying permanent errors as retryable can hide real failures.
  - Missing idempotency safeguards may duplicate side effects on retries.
```

## Example B: Two Findings (When Both Are Strong)

```md
# Gene Scout Locator Report

## Request
- Query: Find reusable ingestion reliability patterns
- Source Roots: /repo-a
- Search Terms: queue, backpressure, checkpoint, flush

## Findings

### Finding 1: Batch flush with timeout + size trigger
- Proposed ID: pipeline.batch.dual-trigger-flush
- Why High Impact: Prevents throughput stalls and unbounded latency by flushing on either queue size or elapsed time.
- Why Reusable: Trigger logic is storage-agnostic and can be reused for logs, analytics, and event delivery.
- Why Quality: The implementation includes explicit lifecycle handling and tests around trigger ordering.
- Evidence:
  - ingest/buffer.py:52 - Implements combined size and timeout flush conditions.
  - ingest/buffer.py:119 - Ensures final flush executes during shutdown.
  - tests/ingest/test_buffer.py:88 - Asserts timeout flush occurs when size threshold is not reached.
- Pitfalls / Edge Cases / Risks:
  - Clock drift can cause unstable timeout behavior if timers are not monotonic.
  - Flush callback failures can drop buffered data unless retried or persisted.

### Finding 2: Monotonic checkpoint commit after side-effect success
- Proposed ID: pipeline.checkpoint.post-commit
- Why High Impact: Avoids duplicate processing and prevents data loss around restarts.
- Why Reusable: Works in stream, queue, and polling systems where checkpoint ordering matters.
- Why Quality: Commit only happens after downstream side effects succeed and monotonic checks are enforced.
- Evidence:
  - ingest/consumer.py:101 - Advances checkpoint only after processing returns success.
  - ingest/consumer.py:133 - Rejects stale checkpoint updates that regress offset.
- Pitfalls / Edge Cases / Risks:
  - Non-atomic side effects plus checkpoint writes can still produce split-brain outcomes.
```

## Example C: No Strong Findings

```md
# Gene Scout Locator Report

## Request
- Query: Find CRDT merge pattern in local repos
- Source Roots: /repo-a
- Search Terms: crdt, merge, lamport

## Findings
- None
```

## Quality Rules

- Only report 1-2 findings, usually 1.
- Every finding must justify impact, reusability, and quality.
- Every evidence bullet must include file path plus single line anchor.
- Do not include code excerpts in the scout output.
- If evidence is weak, return `## Findings` with `- None`.
