$ErrorActionPreference = "Stop"

$bundleRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$codexHome = Join-Path $env:USERPROFILE ".codex"
$targetSkillsRoot = Join-Path $codexHome "skills"
$systemRoot = Join-Path $bundleRoot "skills\\system"
$customRoot = Join-Path $bundleRoot "skills\\custom"
$manifestPath = Join-Path $bundleRoot "docs\\skills-manifest.json"

if (-not (Test-Path $manifestPath)) {
    throw "Missing manifest: $manifestPath"
}

$manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

New-Item -ItemType Directory -Path $targetSkillsRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $targetSkillsRoot ".system") -Force | Out-Null

foreach ($name in $manifest.system) {
    $source = Join-Path $systemRoot $name
    $dest = Join-Path (Join-Path $targetSkillsRoot ".system") $name
    if (Test-Path $source) {
        Copy-Item $source $dest -Recurse -Force
        Write-Host "Installed system skill: $name"
    }
}

foreach ($name in $manifest.custom) {
    $source = Join-Path $customRoot $name
    $dest = Join-Path $targetSkillsRoot $name
    if (Test-Path $source) {
        Copy-Item $source $dest -Recurse -Force
        Write-Host "Installed custom skill: $name"
    }
}

Write-Host ""
Write-Host "Skill files copied."
Write-Host "Next:"
Write-Host "1. Review mcp-config\\codex\\config.portable.template.toml"
Write-Host "2. Merge machine-specific MCP settings into $codexHome\\config.toml"
