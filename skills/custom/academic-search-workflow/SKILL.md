---
name: academic-search-workflow
description: Use when users ask to search scholarly literature across OpenAlex, Crossref, and related academic indexes; build recent-paper shortlists; verify DOI and journal metadata; test journal coverage; or draft a literature-review workflow for topics such as UAV governance, drone imagery, AI media language, design, art, and interdisciplinary research.
---

# Academic Search Workflow

Use this skill when the task is about:

- finding papers by topic, year range, venue, or journal
- expanding Chinese research topics into English search expressions
- validating DOI, title, authors, journal, year, and ISSN
- checking whether a journal is covered by OpenAlex or Crossref
- building a review shortlist, comparison table, or outline

This skill is designed around two MCP layers:

- `OpenAlex MCP` for discovery, topic mapping, source lookup, and trend analysis
- `Crossref MCP` for DOI-first metadata normalization and citation cleanup

Add `Academic Search MCP` only when you want a hosted broad-search convenience layer.
For Chinese arts or design journals that are missing from both systems, add the fallback in [references/chinese-fallback.md](references/chinese-fallback.md).
For CNKI-based Chinese retrieval, also apply the journal normalization and year filter rules in [references/cnki-normalization.md](references/cnki-normalization.md).

## Default flow

1. Normalize the research question.
2. Expand it into English search expressions and synonyms.
3. Use OpenAlex first to discover works, sources, authors, and topic clusters.
4. Use Crossref to verify DOI and clean the metadata for shortlisted items.
5. If the user names a target journal, test its coverage before promising retrieval.
6. If a Chinese journal is not covered, switch to the fallback path in [references/chinese-fallback.md](references/chinese-fallback.md).
7. If CNKI fallback is used, normalize the journal name with the alias map before searching.
8. Filter Chinese results locally by `source` equality or alias match and by year window before writing them into a review.
7. Return:
   - a shortlist
   - why each paper matters
   - metadata confidence notes
   - next-step options

## Tool routing

### Use OpenAlex MCP for

- topic discovery
- recent-paper search
- author/source lookup
- trend analysis
- ISSN-based source lookup

Open [references/io-schema.md](references/io-schema.md) for the recommended input and output shapes.

### Use Crossref MCP for

- DOI lookup
- title-to-DOI cleanup
- journal lookup
- funder lookup when useful

Open [references/io-schema.md](references/io-schema.md) for the normalization step and result schema.

### Use Academic Search MCP only when

- you need a fast, hosted first pass
- you are okay with an aggregator rather than a single authoritative source
- you still plan to verify the final shortlist with Crossref

### Use CNKI fallback for

- Chinese arts, design, or media journals that are absent from OpenAlex and Crossref
- journal-level source search after alias normalization
- article-level supplementation when official TOC pages or public mirrors are needed

When using CNKI fallback:

- prefer normalized journal aliases over raw title strings
- do not trust the web UI sort order alone
- filter final records locally to the requested year range
- keep only records whose `source` exactly matches the normalized journal name or approved alias

## Coverage rule

Before telling the user that a journal can be searched through the MCP stack, verify coverage by:

- OpenAlex source lookup via title or ISSN
- Crossref journal lookup via ISSN
- CNKI fallback only after both checks fail for a Chinese journal

See [references/coverage-test-2026-05-09.md](references/coverage-test-2026-05-09.md) for a worked example using the journals from the user's screenshot.

## Output format

Unless the user asks for another format, return:

```text
Literature search result
- topic
- date range
- sources used

Shortlist
- title | year | venue | DOI or URL | why it matters

Coverage / confidence notes
- which fields were verified in OpenAlex
- which fields were verified in Crossref
- missing fields or indexing gaps

Suggested next step
- expand search / build table / draft review / export citations
```

## Notes

- Do not invent DOI, ISSN, journal indexing, or impact metrics.
- Prefer ISSN and DOI identifiers over title-string matching.
- Treat OpenAlex and Crossref as complementary, not interchangeable.
- For Chinese arts journals, expect partial or absent coverage in these two systems and say so clearly.
- If CNKI fallback is enabled, label it as community or non-official unless you have confirmed an official deployment.
- For `新美术 / 美术与设计 / 装饰` and similar journals, build a journal-alias normalization layer before batch retrieval.
