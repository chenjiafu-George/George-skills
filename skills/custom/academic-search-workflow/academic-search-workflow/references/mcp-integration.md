# MCP Integration

This file gives working templates for wiring `OpenAlex MCP` and `Crossref MCP` into Codex.

## Recommended architecture

Use:

- `OpenAlex MCP` as the main discovery server
- `Crossref MCP` as the metadata verification server

Optional:

- `Academic Search MCP` as a hosted broad-search layer for quick first-pass retrieval
- `CNKI MCP` as a Chinese-journal fallback when OpenAlex and Crossref do not cover the target source

## Trust model

OpenAI's MCP guidance recommends preferring trusted or official servers when possible. OpenAlex and Crossref are authoritative data sources, but the MCP wrappers listed below are third-party wrappers unless you self-host them.

Practical recommendation:

1. Use a local or self-hosted `OpenAlex MCP`.
2. Use a local or self-hosted `Crossref MCP`.
3. Treat hosted third-party MCP endpoints as convenience options, not your long-term default.

## Codex config template

OpenAI's Codex docs show that MCP servers can be configured in `~/.codex/config.toml` with `[mcp_servers.<name>]` entries, or added with `codex mcp add`.

### Option A: OpenAlex via local stdio

```toml
[mcp_servers.openalex]
command = "npx"
args = ["-y", "@cyanheads/openalex-mcp-server"]
env = { OPENALEX_API_KEY = "your-email@example.com" }
```

Notes:

- `OPENALEX_API_KEY` here is the email string used for OpenAlex's polite pool.
- This is the best default if you want a reproducible local setup.

### Option B: OpenAlex via remote HTTP

```toml
[mcp_servers.openalex]
url = "https://openalex.caseyjhand.com/mcp"
```

Notes:

- This is convenient, but it is a third-party hosted endpoint.
- Use only if you trust the operator and accept remote availability risk.

### Option C: Crossref via local Python server

```toml
[mcp_servers.crossref]
command = "python"
args = ["E:\\mcp\\Crossref-MCP-Server\\crossref_server.py"]
```

Notes:

- Replace the path with your actual local clone path.
- This template assumes the repository layout used by the public `JackKuo666/Crossref-MCP-Server` project.

### Combined example

```toml
[mcp_servers.openalex]
command = "npx"
args = ["-y", "@cyanheads/openalex-mcp-server"]
env = { OPENALEX_API_KEY = "your-email@example.com" }

[mcp_servers.crossref]
command = "python"
args = ["E:\\mcp\\Crossref-MCP-Server\\crossref_server.py"]
```

### Optional CNKI fallback example

```toml
[mcp_servers.cnki]
command = "uvx"
args = ["--from", "git+https://github.com/h-lu/cnki-mcp", "cnki-mcp"]
```

Notes:

- This is a community MCP example, not an official CNKI release.
- Some implementations depend on browser automation or site parsing.
- Enable it only if you accept maintenance and compatibility risk.

## Codex CLI commands

If you prefer CLI setup over manual edits:

```powershell
codex mcp add openalex --command npx -- -y @cyanheads/openalex-mcp-server
codex mcp add crossref --command python -- E:\mcp\Crossref-MCP-Server\crossref_server.py
codex mcp list
```

Adjust the exact command form if your installed Codex CLI version expects slightly different argument placement.

## Cursor template

```json
{
  "mcpServers": {
    "openalex": {
      "command": "npx",
      "args": ["-y", "@cyanheads/openalex-mcp-server"],
      "env": {
        "OPENALEX_API_KEY": "your-email@example.com"
      }
    },
    "crossref": {
      "command": "python",
      "args": ["E:\\mcp\\Crossref-MCP-Server\\crossref_server.py"]
    },
    "cnki": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/h-lu/cnki-mcp", "cnki-mcp"]
    }
  }
}
```

## Claude Desktop / Claude Code template

```json
{
  "mcpServers": {
    "openalex": {
      "command": "npx",
      "args": ["-y", "@cyanheads/openalex-mcp-server"],
      "env": {
        "OPENALEX_API_KEY": "your-email@example.com"
      }
    },
    "crossref": {
      "command": "python",
      "args": ["E:\\mcp\\Crossref-MCP-Server\\crossref_server.py"]
    },
    "cnki": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/h-lu/cnki-mcp", "cnki-mcp"]
    }
  }
}
```

## Suggested Codex AGENTS.md hint

Add a short hint to your project instructions if you want the agent to prefer this stack:

```text
For scholarly literature search, prefer the OpenAlex MCP for discovery and the Crossref MCP for DOI and journal metadata verification before using web search.
```

## What each MCP should own

`openalex`

- source lookup by ISSN
- topic discovery
- recent-paper search
- author and institution mapping
- trend analysis

`crossref`

- DOI validation
- publisher/journal cleanup
- citation export basis
- journal lookup by ISSN

`cnki`

- Chinese title search
- Chinese journal-page discovery
- fallback retrieval for arts and design journals absent from OpenAlex and Crossref

## Integration advice

- Do not route every query through all MCPs.
- Discover first with OpenAlex.
- Normalize only the shortlist with Crossref.
- Keep a fallback web-search path for journals outside both indexes.
