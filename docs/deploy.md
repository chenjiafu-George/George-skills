# Deploy Guide

## Goal

Move the current Codex skills and MCP setup to another machine with minimum manual work.

## Steps

1. Clone or copy the `George-Skill` folder.
2. Run `install.ps1` in PowerShell.
3. Open `mcp-config/codex/config.portable.template.toml`.
4. Update machine-specific paths:
   - Codex Python or `uvx`
   - Chrome binary path
   - ChromeDriver path
   - local workspace path for `academic-search-workflow`
5. Merge the final config into `C:\Users\<YourUser>\.codex\config.toml`.

## CNKI note

The CNKI MCP in this bundle is a repaired local wrapper.
It depends on:

- installed Google Chrome
- matching ChromeDriver
- a reachable CNKI web session

On a new machine, verify:

- Chrome path
- driver path
- Python path used by the wrapper

## Suggested verification

After deployment:

1. confirm Codex can see the copied skills
2. confirm `openalex`, `crossref`, and `cnki` MCP entries parse
3. test a simple CNKI journal lookup
4. test the `academic-search-workflow` skill end to end
