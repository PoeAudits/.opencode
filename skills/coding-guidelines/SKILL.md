---
name: coding-guidelines
description: >
  This skill should be used when writing code in any supported language, reviewing
  code for style compliance, or establishing coding standards for a project. Trigger
  phrases include "writing code", "coding standards", "code style", "coding guidelines".
---

# Coding Guidelines

## 1. Purpose and Scope

This skill encodes cross-language coding principles and routes agents to language-specific reference files for detailed standards. It covers:

- **General coding principles** — Structure, control flow, data structures, error handling, naming, and type discipline that apply across all languages
- **Language routing** — Directing agents to the appropriate language-specific reference file based on the target language
- **Supported languages** — Python, TypeScript, Go, and Solidity, each with a dedicated reference file containing idiomatic rules, patterns, and anti-patterns

**Scope boundary:** This skill provides the shared foundation and routing logic. Language-specific syntax, tooling, framework conventions, and idiomatic patterns live in reference files under `references/`. This skill does NOT cover architecture decisions, deployment strategies, or infrastructure concerns beyond what directly affects code style.

Agents load this skill when writing, reviewing, or modifying code. The general principles apply universally. The agent then consults the relevant language-specific reference file for the target language.

After reading this skill, you MUST read the language-specific reference file for the target language. If one does not exist then consult the general principles in this skill.

## 2. Core Principles

1. **Readability Over Cleverness.** Code is read far more often than it is written. Prefer explicit, simple constructs over clever abstractions. Every abstraction introduces the risk of a leaky abstraction. Minimize abstraction depth and favor code that communicates intent on first read.

2. **Errors Are Not Optional.** All errors MUST be handled. An analysis of production failures in distributed data-intensive systems found that the majority of catastrophic failures could have been prevented by simple testing of error handling code. Never swallow errors, never ignore return values that indicate failure.

3. **Bounded Execution.** All loops and queues MUST have a fixed upper bound to prevent infinite loops or tail latency spikes. This follows the fail-fast principle so that violations are detected sooner rather than later. Where a loop cannot terminate (e.g., an event loop), this MUST be explicitly asserted.

4. **Names Carry Meaning.** Variable and function names encode domain knowledge. Add units or qualifiers last, sorted by descending significance, so the most important word comes first. Choose related names with matching character counts to produce visual symmetry in source code. A noun is often a better descriptor than an adjective or present participle.

5. **Smallest Sufficient Type.** Use the smallest type that can represent the value. Every variable, parameter, and return value MUST have an explicit type. Implicit typing hides intent and permits accidental widening.

## 3. Anatomy/Structure Guidance

### General Coding Rules

These rules apply to all supported languages. Language-specific references build on — but do not contradict — these foundations.

#### Structure

Order matters for readability even when it does not affect semantics. On first read, a file is read top-down. Place important constructs near the top. The main function or entry point goes first.

#### Control Flow

Use only simple, explicit control flow for clarity. Do not use recursion unless the problem is inherently recursive and bounded. Prefer a minimum of excellent abstractions that make the best sense of the domain.

#### Naming

Add units or qualifiers to variable names, placing the units or qualifiers last, sorted by descending significance. For example, `latency_ms_max` rather than `max_latency_ms`. This groups related variables (`latency_ms_min`, `latency_ms_max`) and aligns them visually.

When choosing related names, prefer names with the same character count so that related variables line up in source. For example, `source` and `target` are better than `src` and `dest` because `source_offset` and `target_offset` align in calculations.

When a function calls a helper function or callback, prefix the helper name with the calling function name to show call history. For example, `read_sector()` and `read_sector_callback()`.

#### Error Handling

Handle every error. Either propagate the error up the call stack with context, or handle it completely at the current level. Never log an error AND return it — choose one.

#### Types

Use the smallest type that can represent the value. Every variable, parameter, and return value MUST have an explicit type annotation where the language supports it.

### Language Routing

When writing code, determine the target language and load the corresponding reference file:

| Language | Reference File |
|----------|---------------|
| Python | `skills/coding-guidelines/references/python.md` |
| TypeScript / JavaScript | `skills/coding-guidelines/references/typescript.md` |
| Go | `skills/coding-guidelines/references/golang.md` |
| Solidity | `skills/coding-guidelines/references/solidity.md` |

Read the relevant reference file before writing code in that language. The general principles from this skill apply in addition to the language-specific rules. If a language-specific rule conflicts with a general principle, the language-specific rule takes precedence for that language.

## 4. Creation Process

This section describes how to add a new language to the coding guidelines.

1. **Identify the language.** Determine the target language and confirm it is not already covered by an existing reference file.

2. **Create the reference file.** Create `skills/coding-guidelines/references/<language>.md` as a plain Markdown file. Start with an H1 title heading and a one-to-two sentence purpose statement. No YAML frontmatter.

3. **Populate language-specific rules.** Cover at minimum: naming conventions, error handling patterns, type system usage, control flow idioms, code style (formatting, imports, comments), tooling (linter, formatter, test runner), and common anti-patterns.

4. **Avoid duplicating general guidelines.** The general principles in this SKILL.md apply to all languages. The reference file MUST NOT repeat general rules — only language-specific interpretations or overrides.

5. **Update the routing table.** Add the new language and reference file path to the language routing table in Section 3.

6. **Update the references usage section.** Add an entry for the new reference file in Section 8.

7. **Validate.** Confirm the reference file follows the reference file conventions: H1 title, purpose statement, no frontmatter, imperative third-person tone, no second person language.

## 5. Structural Rules

### General Rules

- The general coding principles in Section 3 apply to all code regardless of language.
- Language-specific reference files MUST NOT contradict the general principles unless an explicit override is documented with rationale.
- All code MUST have explicit error handling. Swallowed errors are prohibited.
- All loops and queues MUST have a fixed upper bound or an explicit assertion that unbounded execution is intentional.
- All variables, parameters, and return values MUST have explicit type annotations where the language supports it.

### Reference File Format

- Reference files are plain Markdown with no YAML frontmatter.
- Each reference file MUST start with an H1 title heading and a one-to-two sentence purpose statement.
- Reference files MUST use imperative, third-person tone throughout.
- Second person language ("you", "your") MUST NOT appear in reference files.
- Reference file names MUST use lowercase-hyphenated format with `.md` extension.
- Reference files MUST NOT duplicate the general coding principles from this skill's Section 3.

### Routing Rules

- The language routing table in Section 3 MUST list every supported language with its reference file path.
- Every reference file under `references/` MUST have a corresponding entry in the routing table.
- Agents MUST read the relevant language reference file before writing code in that language.

### Prohibited Actions

- MUST NOT write code without loading the appropriate language reference file first.
- MUST NOT ignore or swallow errors in any language.
- MUST NOT use implicit types where explicit type annotations are available.
- MUST NOT create unbounded loops or queues without explicit justification.
- MUST NOT add YAML frontmatter to reference files.

## 6. Validation Checklist

- [ ] SKILL.md exists at `skills/coding-guidelines/SKILL.md`
- [ ] YAML frontmatter contains exactly two fields: `name` and `description`
- [ ] `name` field is `coding-guidelines`, matching the parent directory
- [ ] `description` starts with "This skill should be used when" and includes quoted trigger phrases
- [ ] All eight body sections present in correct order with numbered headings
- [ ] General coding principles cover structure, control flow, naming, error handling, and types
- [ ] Language routing table lists all supported languages with correct reference file paths
- [ ] Every reference file under `references/` has a corresponding routing table entry
- [ ] No second person language in SKILL.md or any reference file
- [ ] Imperative voice used throughout
- [ ] Reference files are plain Markdown with no YAML frontmatter
- [ ] Each reference file starts with an H1 title and a purpose statement
- [ ] Reference files do not duplicate general coding principles from SKILL.md Section 3
- [ ] Common mistakes table has at least six entries with Mistake, Problem, and Fix columns

## 7. Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Writing code without loading the language reference file | Language-specific rules are missed, producing non-idiomatic code that violates project conventions. | Always read the relevant reference file from Section 3's routing table before writing code. |
| Swallowing errors or ignoring error return values | Unhandled errors cause silent failures that surface as production incidents. The majority of catastrophic distributed system failures trace to unhandled errors. | Handle every error: either propagate with context or handle completely at the current level. |
| Duplicating general guidelines in language reference files | Duplicated rules drift out of sync and create contradictions. Changes to a general rule require updating every reference file. | Language reference files encode only language-specific rules. General principles live in SKILL.md Section 3. |
| Adding YAML frontmatter to reference files | Reference files are plain Markdown. Frontmatter causes them to be parsed as standalone skills or agents, breaking the routing architecture. | Remove all YAML frontmatter from reference files. Start with an H1 title heading. |
| Using implicit types where explicit annotations are available | Implicit typing hides intent, permits accidental widening, and makes code harder to review. It violates the smallest-sufficient-type principle. | Add explicit type annotations to all variables, parameters, and return values. |
| Creating unbounded loops without assertions | Unbounded loops cause infinite execution or tail latency spikes. The fail-fast principle requires that all loops have termination guarantees. | Add a fixed upper bound to every loop and queue. Assert unbounded execution when intentional. |
| Using second person language in skill or reference files | Convention violation. Skills and reference files are consumed by agents and MUST use imperative voice or third-person construction. | Replace all instances of "you/your" with imperative constructions or third-person references. |
| Naming variables with qualifiers first (e.g., `max_latency_ms`) | Breaks the naming convention of descending significance ordering. Related variables do not group or align visually. | Place the most significant word first, qualifiers last: `latency_ms_max`. |

## 8. References Usage

- **`skills/coding-guidelines/references/python.md`** — Consult before writing any Python code. Provides Python-specific rules covering architecture patterns (Protocol over ABC, data-centric design), type system usage (modern union syntax, comprehensive annotations), code style (f-strings, comprehensions, match statements), context managers, generators, data validation (dataclasses vs Pydantic), async patterns, testing with pytest, tooling (ruff, uv), and dependency management.

- **`skills/coding-guidelines/references/typescript.md`** — Consult before writing any TypeScript or JavaScript code. Provides TypeScript-specific rules covering architecture patterns, type system usage, advanced type patterns, null handling, code style, modules and imports, error handling, async patterns, testing, tooling, React/Next.js conventions, and runtime validation with Zod.

- **`skills/coding-guidelines/references/golang.md`** — Consult before writing any Go code. Provides Go-specific rules covering formatting, naming conventions, interface design, control flow idioms, composition patterns, key idioms (defer, multiple returns, zero values), error handling patterns (wrapping, sentinel errors, custom types, panic decisions), methods, and anti-patterns to avoid.

- **`skills/coding-guidelines/references/solidity.md`** — Consult before writing any Solidity code. Provides Solidity-specific rules covering architecture and design patterns, security patterns (CEI, reentrancy, access control), dependency priority (Solmate, Solady, OpenZeppelin), naming conventions, custom errors, NatSpec documentation, events, function ordering, storage patterns, math and precision, gas optimization, contract structure templates, and deployment conventions.
