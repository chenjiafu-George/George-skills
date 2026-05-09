# CNKI MCP Tuning Report on 2026-05-09

## What was changed

- Downloaded matching ChromeDriver for local `Google Chrome 147.0.7727.138`
- Added a local wrapper server:
  - `E:\daizuo\1111\academic-search-workflow\tools\cnki_mcp_local.py`
- Updated local Codex CNKI MCP entry to call the wrapper instead of the raw community server
- Forced the wrapper to use:
  - local Chrome binary
  - local ChromeDriver 147
  - local user-data-dir in workspace
  - non-headless browser mode by default

## Why the original community CNKI MCP failed

The original server assumed:

- `ChromeDriverManager().install()`
- default Chrome startup path
- headless Selenium session

On this machine, the working combination required:

- installed Chrome at `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- manually downloaded matching `chromedriver 147.0.7727.117`
- sandbox-external browser startup
- non-headless mode to reduce CNKI verification blocking

## Current Codex CNKI MCP target

Configured wrapper:

- `E:\daizuo\1111\academic-search-workflow\tools\cnki_mcp_local.py`

Driver path:

- `E:\daizuo\1111\.tmp\chromedriver-147\chromedriver-win64\chromedriver.exe`

## Per-journal live test

Test mode:

- CNKI browser search
- search field: `文献来源`
- one page per query
- real Selenium run with local Chrome and matching driver

### Directly stable with the journal short name

| Journal | Query used | Result |
|---|---|---|
| 文艺研究 | `文艺研究` | searchable |
| 新美术 | `新美术` | searchable |
| 美术研究 | `美术研究` | searchable |
| 世界美术 | `世界美术` | searchable |

### Searchable, but better with a normalized query

| Target journal | Query used | Practical note |
|---|---|---|
| 美术与设计 | `南京艺术学院学报` | CNKI results can hit source `南京艺术学院学报(美术与设计版)` |
| 装饰 | `装饰杂志` | CNKI results can hit source `装饰`, but mixed with similar source names |

## Practical conclusion

- The CNKI MCP chain is now usable on this machine.
- For `文艺研究 / 新美术 / 美术研究 / 世界美术`, direct short-name source search can run.
- For `美术与设计 / 装饰`, the search is usable but should prefer normalized query aliases during skill execution.
- If this is integrated into a production skill, add a journal-alias normalization layer before calling `search_cnki`.

## Recommended alias map

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

## Remaining limitation

The current wrapper makes retrieval work, but does not yet guarantee perfect `近5年` sorting or filtering from CNKI's web UI alone. For literature review production, you should still:

- fetch one or more pages
- filter by `date` locally
- confirm `source` equality or alias match locally
