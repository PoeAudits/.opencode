---
description: Research an external documentation question end-to-end using the exa-docs-researcher subagent and Exa MCP (Search + Fetch). Prioritize official, versioned sources. It is best to run this command in a new session.
---

# Documentation Research (using exa-docs-researcher)

You are tasked with conducting comprehensive documentation research to answer user questions by spawning tasks and synthesizing their findings using the exa-docs-researcher subagent_type (Exa Search + Exa Fetch).

The user will provide a ticket or ad-hoc query to read and begin researching.

## Steps to follow after receiving the documentation query:

1. **Read the ticket first**
   - Read the full ticket text (and any attached context like error logs, versions, platforms, product names) carefully before spawning any sub-tasks.
   - Identify key terms: product/library/framework, feature/endpoint/config, version(s), platform(s), error codes, regions, SKUs.
   - Capture any explicit constraints: target vendor domain(s), release line (e.g., v1.29), policy/compat requirements, dates.
   - Do not launch any sub-agents until you’ve read and understood the ticket.

2. **Detail the steps needed to perform the research**
   - Break the ticket into composable research areas (e.g., “Auth: OAuth scopes,” “API: rate limits,” “SDK: Node v3 migration,” “Release notes: breaking changes in 2024-10”).
   - Determine likely authoritative sources (official docs sites, API references, release notes, standards/RFCs, vendor blogs, GitHub repos/wiki, support KBs).
   - Plan multiple search angles for each area:
     - Broad semantic search per product/feature
     - Targeted exact phrases with quotes
     - site-restricted queries to official domains
     - Version/date-constrained queries (e.g., “v2.1”, “2024”, “GA”, “deprecated”)
   - Note which areas require fetching full content vs snippets, and which require version-aware analysis.

3. **Spawn tasks for comprehensive documentation research (follow this sequence)**

   **Phase 1 – Discover (Search)**
   - Identify all topics/components/areas you need to search.
   - Group related topics into coherent batches (e.g., “API auth,” “Webhooks,” “SDK Go v2”).
   - Spawn exa-docs-researcher agents in parallel (same-type) for each topic group to:
     - Run Exa Search with broad and targeted variants
     - Prefer official domains and canonical URLs
     - Propose top authoritative candidates with titles/URLs/snippets/dates
   - **WAIT** for all search agents to complete before proceeding.

   **Phase 2 – Fetch (Content Retrieval)**
   - Based on Phase 1, select the top 3–5 promising pages per topic group.
   - Spawn exa-docs-researcher agents in parallel (same-type) to:
     - Run Exa Fetch for full text or key sections
     - Capture publication/last-updated dates, version applicability, and anchors
   - **WAIT** for all fetch agents to complete before proceeding.

   **Phase 3 – Analyze (Docs Synthesis)**
   - Using search and fetch outputs, determine which pages need deep analysis.
   - Group analysis tasks by topic/component (e.g., “Webhook retries,” “JWT aud claim,” “K8s PDB v1.29”).
   - Spawn exa-docs-researcher agents in parallel (same-type) to:
     - Extract exact quotes with permalinks to headings/sections
     - Record last updated dates, versions, release channels
     - Note conflicts across sources and identify the most authoritative stance
     - Summarize behavior, caveats, and breaking changes
   - **WAIT** for all analyzer agents to complete before synthesizing.

   **Important sequencing notes**
   - Each phase builds on the previous one: **Discover → Fetch → Analyze**.
   - Run agents of the same type in parallel within each phase.
   - Do not mix agent types in parallel execution.
   - Each agent knows its job—describe what to find, not how to do it.

4. **Wait for all sub-agents to complete and synthesize findings**
   - Compile all sub-agent results per topic group.
   - Prioritize official, versioned, and latest stable documentation as the primary source of truth.
   - Include exact quotes with anchors/permalinks, last updated dates, and versions.
   - Call out conflicts and explain which source prevails and why.
   - Identify gaps that require further querying.
   - Provide clear, actionable answers that directly address the user’s question.

5. **Gather metadata for the research document**
   - Use the following metadata for the research document frontmatter:

     metadata for frontmatter

     !`agentic metadata`

   - Ensure you capture:
     - date/time with timezone of research
     - repository/branch/git_commit (if applicable in this workspace)
     - topic (user’s question)
     - last_updated
     - Optional docs-specific metadata if available: source_domains, product_versions, doc_release_lines.

6. **Generate research document**
   - Filename: `thoughts/research/date_topic.md`
   - Use the metadata gathered in step 5, mapping XML tags to frontmatter fields
   - Structure the document with YAML frontmatter followed by content:

     ```markdown
     ---
     date: [Current date and time with timezone in ISO format]
     git_commit: [from metadata]
     branch: [from metadata]
     repository: [from metadata]
     topic: "[User's Question/Topic]"
     tags: [research, documentation, exa, official-docs, relevant-product-names]
     last_updated: [from metadata]
     ---

     ## Ticket Synopsis
     [Synopsis of the ticket information, including product, feature, version(s), platform, constraints]

     ## Summary
     [High-level findings answering the user's question; highlight authoritative sources and versions]

     ## Detailed Findings

     ### [Topic/Source 1]
     **Source**: [Name with link]  
     **Relevance**: [Why this source is authoritative/useful]  
     **Key Information**:
     - "[Direct quote]" (link to anchor)
     - Last updated/version: [value]
     - [Concise explanation and implications]

     ### [Topic/Source 2]
     **Source**: [Name with link]  
     **Relevance**: [...]  
     **Key Information**:
     - "[Direct quote]" (anchor)
     - Last updated/version: [value]
     - [Notes, caveats, breaking changes]

     ## Additional Resources
     - [Relevant link] - Brief description
     - [Another link] - Brief description

     ## Gaps or Limitations
     [Note any missing information, unversioned pages, conflicting guidance, or areas needing vendor confirmation]

     ## Search Strategy
     - Broad queries used:
       - ["query 1", "query 2"...]
     - Targeted/site-restricted queries used:
       - site:[official-domain] ["exact phrase"]
     - Version/date constraints used:
       - ["vX.Y", "2025-10", "GA", "deprecated"]

     ## Source Record
     - Title, URL, domain, last updated, version, and quoted sections for each included source
     - Preference for canonical/stable permalinks
     ```

7. **Present findings**
   - Present a concise summary of findings to the user.
   - Include the most relevant quotes and permalinks, last updated dates, and versions.
   - Ask if they have follow-up questions or need clarification.

8. **Handle follow-up questions**
   - If the user has follow-up questions, append to the same research document.
   - Update frontmatter fields `last_updated` and `last_updated_by` accordingly.
   - Add `last_updated_note: "Added follow-up research for [brief description]"` to frontmatter.
   - Add a new section: `## Follow-up Research [timestamp]`.
   - Spawn new exa-docs-researcher sub-agents as needed for additional investigation.
   - Continue updating and syncing.

9. **Update ticket status to 'researched'**
   - Edit the ticket file's frontmatter to set `status: researched`.

Use the **todowrite** tool to create a structured task list for the 9 steps above, marking each as pending initially.

---

## Core Responsibilities (Docs)

When you receive a documentation query, you will:
- **Analyze the Query**
  - Identify key terms (product, feature, version, platform, error codes)
  - Determine authoritative sources (official docs, RFCs, vendor sites, support KBs)
  - Plan multiple search angles (broad, exact phrase, site-restricted, versioned)
- **Execute Strategic Exa Searches**
  - Start broad to map the landscape
  - Refine with exact phrases, version numbers, and site filters
  - Prefer official domains and canonical URLs
- **Fetch and Analyze Content**
  - Use Exa Fetch to retrieve full text or key sections
  - Extract exact quotes with anchors/permalinks
  - Note publication/update dates and version applicability
- **Synthesize Findings**
  - Organize by relevance and authority
  - Include quotes + concise explanations
  - Highlight version-specific behavior and breaking changes
  - Call out conflicts and gaps

---

## Exa Usage Guidelines

- Start with 2–3 broad Exa searches (semantic + keyword variants).
- Add targeted searches with:
  - site restrictions to official domains
  - exact phrases in quotes
  - version numbers, release lines, or dates
- Fetch the top 3–5 promising pages first.
- If insufficient, refine and repeat with:
  - alternative terminology/synonyms
  - narrowed/widened domain scope
  - feature-specific phrases or component names
- Deduplicate near-identical pages (e.g., older version mirrors).
- Prefer canonical URLs and stable permalinks.
- Record: title, URL, source domain, last updated, version, relevant quotes.

---

## Quality Guidelines

- **Accuracy:** Quote precisely; provide direct anchors/links.  
- **Relevance:** Focus on pages that directly answer the query.  
- **Currency:** Surface last-updated dates and doc versions; prefer stable/GA.  
- **Authority:** Prefer official docs, standards, vendor sources; cite clearly.  
- **Completeness:** Search from multiple angles; include caveats and edge cases.  
- **Transparency:** Flag conflicting guidance and explain your resolution.

---

## Examples of Search Variations

- `site:docs.github.com Actions reusable workflows reference`
- `OpenAI API "function calling" docs 2024`
- `Kubernetes "Pod Disruption Budget" documentation v1.29`
- `Stripe webhook signature verification docs`
- `RFC 7519 JSON Web Token "aud" claim`
- `AWS IAM "condition keys" docs 2025`
- `PostgreSQL "logical replication" 16 docs`
- `Apple developer "App Attest" documentation`

---

## Important notes

- Follow the three-phase sequence: **Discover (Search) → Fetch → Analyze**.
- Use parallel sub-agents OF THE SAME TYPE ONLY within each phase.
- Always run fresh documentation research—never rely solely on existing research documents.
- Prefer official, versioned documentation; record last updated dates and versions.
- Use canonical URLs and anchors for quotes.
- Research documents must be self-contained with all necessary context and links.
- Each sub-agent prompt should be specific and focused on read-only operations.
- Consider cross-vendor differences and version-specific behavior.
- Include temporal context (when the research was conducted).
- **Critical ordering:**
  - ALWAYS read the ticket first (step 1) before spawning sub-tasks.
  - ALWAYS wait for all sub-agents to complete before synthesizing (step 4).
  - ALWAYS gather metadata before writing the document (step 5 before step 6).
  - NEVER write the research document with placeholder values.
- **Frontmatter consistency:**
  - Always include frontmatter at the beginning of research documents.
  - Keep frontmatter fields consistent across all research documents.
  - Update frontmatter when adding follow-up research.
  - Use snake_case for multi-word field names (e.g., `last_updated`).
  - Tags should be relevant to the research topic and components studied.
