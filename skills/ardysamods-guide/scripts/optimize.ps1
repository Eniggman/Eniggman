param (
    [string]$RootPath = ".",
    [string]$ConfigPath = (Join-Path (Resolve-Path ".") "vpk_mod_config.json"),
    [string[]]$KeepKeywords = @()
)

function Normalize-Token {
    param ([string]$Value)
    if ($null -eq $Value) {
        return ""
    }

    return ($Value.ToLowerInvariant() -replace '[^a-z0-9]', '')
}

function Add-KeepAlias {
    param (
        [System.Collections.Generic.HashSet[string]]$Set,
        [string]$Alias
    )

    $normalized = Normalize-Token $Alias
    if ([string]::IsNullOrWhiteSpace($normalized)) {
        return
    }

    [void]$Set.Add($normalized)
    [void]$Set.Add("hero$normalized")
}

$aliasMap = @{
    "wisp" = @("wisp", "io", "wips", "portal", "cube", "companion", "companion_cube")
    "io" = @("wisp", "io", "wips", "portal", "cube", "companion", "companion_cube")
    "sniper" = @("sniper", "kardel")
    "razor" = @("razor")
    "muerta" = @("muerta")
    "phantom_lancer" = @("phantom_lancer", "phantomlancer")
    "luna" = @("luna")
    "lion" = @("lion")
    "bounty_hunter" = @("bounty_hunter", "bountyhunter", "gondar")
}

$keepAliases = [System.Collections.Generic.HashSet[string]]::new()

if ($KeepKeywords.Count -gt 0) {
    foreach ($keyword in $KeepKeywords) {
        Add-KeepAlias $keepAliases $keyword
    }
} else {
    if (-not (Test-Path -LiteralPath $ConfigPath)) {
        throw "Config not found: $ConfigPath"
    }

    $config = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json
    foreach ($hero in $config.active_roster) {
        Add-KeepAlias $keepAliases $hero
        $key = [string]$hero
        if ($aliasMap.ContainsKey($key)) {
            foreach ($alias in $aliasMap[$key]) {
                Add-KeepAlias $keepAliases $alias
            }
        }
    }

    if ($config.PSObject.Properties.Name -contains "compat_keep_roster") {
        foreach ($hero in $config.compat_keep_roster) {
            Add-KeepAlias $keepAliases $hero
            $key = [string]$hero
            if ($aliasMap.ContainsKey($key)) {
                foreach ($alias in $aliasMap[$key]) {
                    Add-KeepAlias $keepAliases $alias
                }
            }
        }
    }

    foreach ($asset in $config.special_assets) {
        Add-KeepAlias $keepAliases $asset
    }
}

$preserveNames = [System.Collections.Generic.HashSet[string]]::new()
foreach ($name in @("logo", "particles", "invisible", "shared", "common", "generic")) {
    [void]$preserveNames.Add((Normalize-Token $name))
}

function Test-KeepDirectory {
    param ([string]$Name)

    $normalized = Normalize-Token $Name
    if ($keepAliases.Contains($normalized)) {
        return $true
    }

    foreach ($alias in $keepAliases) {
        if ($normalized.StartsWith($alias)) {
            return $true
        }
    }

    return $false
}

function Invoke-PurgeParent {
    param (
        [string]$RelativePath,
        [switch]$PreserveUnknown
    )

    $fullPath = Join-Path $RootPath $RelativePath
    if (-not (Test-Path -LiteralPath $fullPath)) {
        return
    }

    Get-ChildItem -LiteralPath $fullPath -Directory | ForEach-Object {
        $normalized = Normalize-Token $_.Name
        $shouldKeep = Test-KeepDirectory $_.Name
        $shouldPreserve = $PreserveUnknown -and $preserveNames.Contains($normalized)

        if ($shouldKeep -or $shouldPreserve) {
            Write-Host "[+] KEEP: $($_.FullName)" -ForegroundColor Green
            return
        }

        Get-ChildItem -LiteralPath $_.FullName -Recurse -Force | ForEach-Object {
            $_.Attributes = [System.IO.FileAttributes]::Normal
        }
        $_.Attributes = [System.IO.FileAttributes]::Directory
        Remove-Item -LiteralPath $_.FullName -Recurse -Force
        Write-Host "[-] Deleted: $($_.FullName)" -ForegroundColor Gray
    }
}

$strictHeroParentDirs = @(
    "models/heroes",
    "materials/models/heroes",
    "models/items",
    "materials/models/items",
    "particles/units/heroes",
    "sounds/weapons/hero",
    "sounds/vo",
    "8213/heroes",
    "8213/materials",
    "8213/particles",
    "8213/sounds",
    "jxj/models/heroes",
    "kisilev_ind/models"
)

$customParentDirs = @(
    "kisilev_ind/materials",
    "kisilev_ind/particles"
)

Write-Host "Starting config-driven surgical cleanup in: $RootPath" -ForegroundColor Cyan
Write-Host "Keeping aliases: $([string]::Join(', ', ($keepAliases | Sort-Object)))" -ForegroundColor Cyan

foreach ($dir in $strictHeroParentDirs) {
    Invoke-PurgeParent -RelativePath $dir
}

foreach ($dir in $customParentDirs) {
    Invoke-PurgeParent -RelativePath $dir -PreserveUnknown
}

Write-Host "Cleanup complete. VPK tree is limited to configured heroes plus preserved shared assets." -ForegroundColor Yellow
