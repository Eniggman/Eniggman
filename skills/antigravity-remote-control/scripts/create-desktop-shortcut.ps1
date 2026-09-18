<#
.SYNOPSIS
    Создание ярлыка 'Remote Control AGY.lnk' на Рабочем столе Windows.

.DESCRIPTION
    Портативный PowerShell-скрипт. Создает на Рабочем столе пользователя
    ярлык для быстрого запуска Antigravity Remote Control в один клик.
    Автоматически находит установленный `agy.exe` для назначения оригинальной иконки.

.PARAMETER ShortcutName
    Имя ярлыка (по умолчанию "Remote Control AGY.lnk").

.PARAMETER WorkDir
    Рабочая директория по умолчанию для запуска сессии.

.EXAMPLE
    .\create-desktop-shortcut.ps1
#>

[CmdletBinding()]
param(
    [string]$ShortcutName = "Remote Control AGY.lnk",
    [string]$WorkDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Путь к рабочему столу текущего пользователя
$desktopDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
if (-not (Test-Path -LiteralPath $desktopDir)) {
    $desktopDir = Join-Path $env:USERPROFILE "Desktop"
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$targetScript = Join-Path $scriptDir "start-remote-control.ps1"

if (-not (Test-Path -LiteralPath $targetScript)) {
    Write-Error "Целевой скрипт не найден: $targetScript"
    exit 1
}

# Поиск пути к agy.exe для извлечения официальной иконки
$agyPath = $null
$agyCmd = Get-Command agy -ErrorAction SilentlyContinue
if ($agyCmd -and $agyCmd.Source -and (Test-Path -LiteralPath $agyCmd.Source)) {
    $agyPath = $agyCmd.Source
} else {
    $candidates = @(
        (Join-Path $env:LOCALAPPDATA "agy\bin\agy.exe"),
        (Join-Path $env:USERPROFILE ".gemini\antigravity-cli\bin\agy.exe")
    )
    foreach ($cand in $candidates) {
        if (Test-Path -LiteralPath $cand) {
            $agyPath = $cand
            break
        }
    }
}

# Определение рабочей директории
$workingDirectory = if (-not [string]::IsNullOrWhiteSpace($WorkDir)) {
    $WorkDir
} else {
    # По умолчанию корень репозитория или родительская папка
    (Split-Path -Parent (Split-Path -Parent $scriptDir))
}

$shortcutPath = Join-Path $desktopDir $ShortcutName

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  🛠️  Создание ярлыка Antigravity Remote Control         " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Ярлык           : $shortcutPath" -ForegroundColor Gray
Write-Host "  Целевой скрипт  : $targetScript" -ForegroundColor Gray
Write-Host "  Рабочая папка   : $workingDirectory" -ForegroundColor Gray

# Создание COM-объекта WScript.Shell
$wscript = New-Object -ComObject WScript.Shell
$shortcut = $wscript.CreateShortcut($shortcutPath)

# Параметры запуска powershell с обходом ExecutionPolicy
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Normal -File `"$targetScript`""
$shortcut.WorkingDirectory = $workingDirectory
$shortcut.Description = "Antigravity CLI Remote Control v1.2.6+ (Веб-пульт сессии)"

# Назначение иконки
if ($agyPath) {
    Write-Host "  Иконка agy.exe  : $agyPath" -ForegroundColor Gray
    $shortcut.IconLocation = "$agyPath,0"
} else {
    Write-Host "  [!] agy.exe не обнаружен для иконки, используется стандартная." -ForegroundColor Yellow
}

$shortcut.Save()

Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "  ✅ Ярлык успешно создан на Рабочем столе!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
