# Chinese Arts Journal Fallback

Use this fallback when:

- the target journal is Chinese
- the journal is not found in OpenAlex by ISSN or title
- the journal is not found in Crossref by ISSN
- the user still needs Chinese arts, design, media, or CSSCI-oriented coverage

## Recommended fallback order

1. `CNKI MCP` if available in your environment
2. publisher or journal website
3. Wanfang or CQVIP web search
4. manual metadata normalization into the same review-pack schema

## Why this fallback exists

On 2026-05-09, the screenshot journals showed a split:

- international journals such as `Design Studies`, `The Design Journal`, `Design Issues`, and `Leonardo` were found in OpenAlex and Crossref
- Chinese arts journals such as `文艺研究`, `新美术`, `美术研究`, `美术与设计`, `世界美术`, and `装饰` were not found in either system by ISSN

That makes a Chinese fallback necessary if your skill must support arts and design topics in Chinese.

## CNKI MCP role

Treat `CNKI MCP` as a retrieval fallback, not as the final authority for normalized metadata.

Use it for:

- title search in Chinese
- author and institution search in Chinese
- abstract and keyword harvesting
- issue and journal-page discovery

Then normalize final references into your common output format.

## Journal alias normalization

Before you batch-search Chinese arts journals, normalize the journal name to a CNKI-friendly query form.

Recommended starter map:

```json
{
  "文艺研究": "文艺研究",
  "新美术": "新美术",
  "美术研究": "美术研究",
  "美术与设计": "南京艺术学院学报",
  "世界美术": "世界美术",
  "装饰": "装饰杂志"
}
```

Recommended accepted source aliases:

```json
{
  "文艺研究": ["文艺研究"],
  "新美术": ["新美术"],
  "美术研究": ["美术研究"],
  "美术与设计": ["南京艺术学院学报(美术与设计版)", "南京艺术学院学报"],
  "世界美术": ["世界美术"],
  "装饰": ["装饰"]
}
```

## Year filtering rule

Do not rely on CNKI web sort order alone for `近5年` filtering.

Instead:

1. retrieve one or more pages
2. parse the article date locally
3. keep only records in the requested year window
4. keep only records whose `source` equals the target journal or approved alias

## Risks and guardrails

- Community CNKI MCP servers are typically not official CNKI products.
- Some implementations rely on browser automation and page parsing.
- Availability may change if CNKI updates the site structure or login flow.
- Do not assume stable machine-readable DOI coverage for all Chinese arts journals.

## Suggested output note

When fallback was used, include a note like:

```text
Chinese-journal records were retrieved through a CNKI-oriented fallback path because the target journals were not indexed in OpenAlex or Crossref.
```

## Optional CNKI MCP template

If you choose to test a community CNKI MCP, keep it clearly marked as optional and non-official in your config and notes.
