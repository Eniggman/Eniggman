param (
    [Parameter(Mandatory = $true)]
    [string]$SourceRoot,

    [Parameter(Mandatory = $true)]
    [string]$DestinationRoot,

    [string]$ConfigPath = (Join-Path (Resolve-Path ".") "vpk_mod_config.json")
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

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    throw "Config not found: $ConfigPath"
}

$config = Get-Content -Raw -LiteralPath $ConfigPath | ConvertFrom-Json
$keepAliases = [System.Collections.Generic.HashSet[string]]::new()
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

$preserveNames = [System.Collections.Generic.HashSet[string]]::new()
foreach ($name in @("logo", "particles", "invisible", "shared", "common", "generic")) {
    [void]$preserveNames.Add((Normalize-Token $name))
}

function Test-KeepName {
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

$strictParentDirs = @(
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

function Convert-ToRelativePath {
    param (
        [string]$Root,
        [string]$Path
    )

    return [System.IO.Path]::GetRelativePath($Root, $Path).Replace('\', '/')
}

function Test-IncludedPath {
    param ([string]$RelativePath)

    foreach ($parent in $strictParentDirs) {
        if ($RelativePath.StartsWith("$parent/")) {
            $remainder = $RelativePath.Substring($parent.Length + 1)
            $folder = $remainder.Split('/')[0]
            return (Test-KeepName $folder)
        }
    }

    foreach ($parent in $customParentDirs) {
        if ($RelativePath.StartsWith("$parent/")) {
            $remainder = $RelativePath.Substring($parent.Length + 1)
            $folder = $remainder.Split('/')[0]
            $normalized = Normalize-Token $folder
            return ((Test-KeepName $folder) -or $preserveNames.Contains($normalized))
        }
    }

    return $true
}

$source = (Resolve-Path -LiteralPath $SourceRoot).Path
if (Test-Path -LiteralPath $DestinationRoot) {
    throw "Destination already exists: $DestinationRoot"
}

New-Item -ItemType Directory -Path $DestinationRoot | Out-Null

$copied = 0
$skipped = 0
Get-ChildItem -LiteralPath $source -Recurse -File -Force | ForEach-Object {
    $relative = Convert-ToRelativePath -Root $source -Path $_.FullName
    if (-not (Test-IncludedPath $relative)) {
        $script:skipped++
        return
    }

    $destination = Join-Path $DestinationRoot $relative.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $destinationDir = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $destinationDir)) {
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    }

    Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
    $script:copied++
}

Write-Host "Filtered tree built: $DestinationRoot" -ForegroundColor Cyan
Write-Host "Copied files: $copied" -ForegroundColor Green
Write-Host "Skipped files: $skipped" -ForegroundColor Yellow
