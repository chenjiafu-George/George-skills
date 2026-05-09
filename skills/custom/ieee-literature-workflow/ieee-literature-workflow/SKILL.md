---
name: ieee-literature-workflow
description: >-
  Trigger this skill whenever the user asks in Chinese or English to search IEEE
  literature, browse IEEE Xplore papers, collect IEEE references, identify relevant
  journal or conference articles, extract article metadata, compare IEEE papers, or
  build an IEEE-centered literature review workflow, including requests such as IEEE文献检索、
  IEEE Xplore 检索、IEEE论文搜索、找 IEEE 参考文献、筛 IEEE 论文、检索会议期刊论文、
  下载后精读 IEEE 文献, or build a literature-search-to-reading pipeline. Use the
  Codex-native workflow: web search for discovery and links, MinerU for local reading,
  and nature-citation when the user also needs structured citation support.
---

# IEEE Literature Workflow

This is a Codex-native adaptation of the original `cookjohn/ieee-skills` idea.
Do not assume Claude Code, Chrome DevTools MCP, or slash-command workflows exist.

## Purpose

Use this skill to create a practical IEEE literature loop:

1. discover candidate papers from IEEE Xplore
2. collect metadata and links
3. help the user shortlist relevant papers
4. move local PDFs/DOCX/PPTX into MinerU for deep reading
5. connect the result to citation, writing, response, or PPT workflows

## What this skill replaces from the original repo

The original repository provides Claude Code skills for:

- IEEE keyword search
- advanced IEEE search
- paper detail extraction
- journal/conference browsing
- PDF download
- citation export
- standards search

In Codex, do not try to replay those Chrome MCP steps literally.
Instead, map them to the tools already available in this environment.

## Codex-native mapping

### Discovery and metadata

For IEEE paper discovery, use web search first.

Preferred patterns:

- `site:ieeexplore.ieee.org <topic>`
- `site:ieeexplore.ieee.org/document <topic>`
- `site:ieeexplore.ieee.org "<exact title>"`
- `site:ieeexplore.ieee.org <author> <topic> IEEE`

When the user asks for current or precise results, browse and cite the source links.
Extract, when available:

- title
- authors
- venue
- year
- DOI
- abstract snippet
- IEEE article number
- direct IEEE Xplore URL

### Journal or conference browsing

When the user wants venue-level scanning:

- search the IEEE Xplore publication page
- summarize scope, recent article direction, and likely relevance
- do not invent impact metrics if not directly verified

### Local reading and evidence extraction

Once the user has PDFs or documents locally, route to `mineru-document-explorer`.

Typical MinerU sequence:

1. `search` or `query` across indexed literature folders
2. `doc_toc` on selected PDFs
3. `doc_read` for methods, results, discussion
4. `doc_grep` or `doc_query` for specific concepts, metrics, datasets, or formulas

Use MinerU whenever the task becomes:

- compare methods across downloaded papers
- find where a metric or dataset is defined
- locate equations, tables, or ablation sections
- build a project wiki from a paper set

### Citation support

When the user needs formal citation help, especially beyond IEEE-only retrieval,
route to `nature-citation`.

Use `nature-citation` for:

- support references for a claim
- structured export logic
- broader top-journal citation support

Use this IEEE workflow first when the user's source constraint is IEEE.

### Browser automation

Use `playwright` only when a real browser step is necessary, such as:

- the user explicitly wants portal interaction
- authenticated browsing or PDF download is needed
- a page requires scripted navigation that normal web access cannot provide

Do not default to browser automation when plain browsing is enough.

## Default workflow

When the user says “search IEEE papers on X”, do this:

1. clarify topic, time range, and venue preference only if missing and important
2. browse IEEE Xplore result pages or article pages
3. return a shortlist with title, venue, year, and why each item matters
4. ask whether to continue with:
   - broader search
   - local PDF reading
   - comparison table
   - citation extraction
   - review-outline drafting

When the user already has downloaded PDFs, do this:

1. use or set up MinerU collection indexing
2. search locally first
3. deep-read selected documents
4. produce structured notes for methods, datasets, metrics, limitations

## Recommended outputs

Unless the user asks for another format, return:

```text
IEEE literature shortlist
- [paper 1]
- [paper 2]

Why these matter
- [...]

Suggested next step
- local deep reading / citation support / comparison table / review outline
```

## Boundaries

- Do not promise direct IEEE PDF download unless access is actually available.
- Do not fabricate DOI, article number, abstract, or citation fields.
- Do not assume the original Claude Chrome MCP workflow exists in Codex.
- For standards work, treat IEEE standards search as a separate standards task, not a normal paper search.

## Practical trigger guidance

Prefer this skill when the user asks things like:

- “帮我检索 IEEE 上关于 xxx 的文献”
- “在 IEEE Xplore 上找近五年的论文”
- “筛几篇 IEEE 论文做综述”
- “先搜 IEEE 文献，再帮我精读 PDF”
- “做一个 IEEE 文献检索到写综述的闭环”

If the task shifts from discovery into local evidence extraction, bring in
`mineru-document-explorer`.
If the task shifts into formal paper writing or citation packaging, bring in
`nature-citation`, `nature-polishing`, `nature-response`, or `nature-paper2ppt`
as appropriate.
