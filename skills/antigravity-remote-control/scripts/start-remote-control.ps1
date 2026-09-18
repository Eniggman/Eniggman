<#
.SYNOPSIS
    Запуск Antigravity CLI (v1.2.6+) с автоматическим перехватом сессии Remote Control и открытием веб-интерфейса.

.DESCRIPTION
    Портативный PowerShell-скрипт для Windows.
    Запускает `agy --remote-control` в отдельном окне терминала (Windows Terminal wt.exe или powershell.exe),
    безопасно отслеживает журнал сессии в ~/.gemini/antigravity-cli/log через FileShare.ReadWrite,
    извлекает уникальный session-id и автоматически открывает сессию в браузере по умолчанию.

.PARAMETER WorkDir
    Рабочая директория для запуска сессии Antigravity CLI. По умолчанию - текущая директория.

.PARAMETER AgyArgs
    Дополнительные аргументы командной строки для `agy` (например, `--model`, `--effort`, `--dangerously-skip-permissions`).

.PARAMETER NoBrowser
    Не открывать сессию в браузере автоматически (только вывести URL и скопировать в буфер обмена).

.PARAMETER TimeoutSeconds
    Таймаут ожидания инициализации туннеля Remote Control в секундах (по умолчанию 30).

.EXAMPLE
    .\start-remote-control.ps1
    Запуск сессии в текущей директории с автооткрытием браузера.

.EXAMPLE
    .\start-remote-control.ps1 -WorkDir "D:\Projects\MyApp" -AgyArgs "--model gemini-2.5-pro"
    Запуск в указанном проекте с выбором конкретной модели.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$WorkDir = (Get-Location).Path,

    [Parameter(Position = 1)]
    [string]$AgyArgs = "",

    [switch]$NoBrowser,

    [int]$TimeoutSeconds = 30
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

# Определение портативных путей пользователя
$geminiDir = Join-Path $env:USERPROFILE ".gemini\antigravity-cli"
$logDir    = Join-Path $geminiDir "log"
$cliLog    = Join-Path $geminiDir "cli.log"

# Проверка доступности исполняемого файла agy
$agyCmd = Get-Command agy -ErrorAction SilentlyContinue
if (-not $agyCmd) {
    # Поиск в стандартных портативных каталогах
    $possiblePaths = @(
        (Join-Path $env:LOCALAPPDATA "agy\bin\agy.exe"),
        (Join-Path $geminiDir "bin\agy.exe")
    )
    foreach ($p in $possiblePaths) {
        if (Test-Path -LiteralPath $p) {
            $agyCmd = $p
            break
        }
    }
}

if (-not $agyCmd) {
    Write-Error "Исполняемый файл 'agy' не найден в PATH и стандартных директориях. Убедитесь, что Antigravity CLI установлен."
    exit 1
}

# Формирование аргументов команды agy
$fullAgyCommand = if ([string]::IsNullOrWhiteSpace($AgyArgs)) {
    "agy --remote-control"
} else {
    "agy --remote-control $AgyArgs"
}

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  🛰️  Antigravity Remote Control Launcher v1.2.6+       " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Директория : $WorkDir" -ForegroundColor Gray
Write-Host "  Команда    : $fullAgyCommand" -ForegroundColor Gray
Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

# Фиксация времени старта для фильтрации логов
$launchTimeUtc = [System.DateTime]::UtcNow.AddSeconds(-2)

# Запуск сессии в новом окне терминала
$wtCmd = Get-Command wt.exe -ErrorAction SilentlyContinue
if ($wtCmd) {
    Write-Host "[*] Запуск сессии через Windows Terminal (wt.exe)..." -ForegroundColor DarkCyan
    $wtArgs = @("-d", "`"$WorkDir`"", "powershell.exe", "-NoExit", "-Command", $fullAgyCommand)
    Start-Process -FilePath "wt.exe" -ArgumentList $wtArgs
} else {
    Write-Host "[*] Запуск сессии через PowerShell..." -ForegroundColor DarkCyan
    $psArgs = @("-NoExit", "-Command", $fullAgyCommand)
    Start-Process -FilePath "powershell.exe" -WorkingDirectory $WorkDir -ArgumentList $psArgs
}

# Функция безопасного чтения лога без блокировки (FileShare.ReadWrite)
function Get-FileContentSafely {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    try {
        $fileStream = [System.IO.FileStream]::new(
            $Path,
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::Read,
            [System.IO.FileShare]::ReadWrite
        )
        $streamReader = [System.IO.StreamReader]::new($fileStream, [System.Text.Encoding]::UTF8)
        $text = $streamReader.ReadToEnd()
        $streamReader.Close()
        $fileStream.Close()
        return $text
    } catch {
        return $null
    }
}

Write-Host "[*] Ожидание инициализации Remote Control туннеля..." -ForegroundColor Yellow

$sw = [System.Diagnostics.Stopwatch]::StartNew()
$sessionId = $null
$sessionUrl = $null

while ($sw.Elapsed.TotalSeconds -lt $TimeoutSeconds) {
    Start-Sleep -Milliseconds 600

    # 1. Поиск новейшего лог-файла сессии в каталоге log/
    $targetLogs = @()
    if (Test-Path -LiteralPath $logDir) {
        $recentLog = Get-ChildItem -LiteralPath $logDir -Filter "cli-*.log" -File -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTimeUtc -Descending |
            Select-Object -First 1

        if ($recentLog -and $recentLog.LastWriteTimeUtc -ge $launchTimeUtc) {
            $targetLogs += $recentLog.FullName
        }
    }

    # 2. Также проверяем основной cli.log
    if (Test-Path -LiteralPath $cliLog) {
        $targetLogs += $cliLog
    }

    foreach ($logFile in $targetLogs) {
        $logContent = Get-FileContentSafely -Path $logFile
        if (-not $logContent) { continue }

        # Поиск паттерна session-id в протоколе Remote Control v2
        # Паттерн: [remote-control-7b909f69-f505-45c5-8ec8-b2d2bc12b3da-v2]
        if ($logContent -match '\[remote-control-([0-9a-fA-F-]+)-v2\]') {
            $sessionId = $Matches[1]
            $sessionUrl = "https://antigravity.google.com/r/$sessionId"
            break
        }
        # Альтернативный прямой URL
        if ($logContent -match 'https://antigravity\.google\.com/r/([0-9a-fA-F-]+)') {
            $sessionId = $Matches[1]
            $sessionUrl = "https://antigravity.google.com/r/$sessionId"
            break
        }
    }

    if ($sessionId) {
        break
    }
}

$sw.Stop()

if ($sessionId) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "  ✅  СЕССИЯ REMOTE CONTROL УСПЕШНО НАЙДЕНА!" -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "  Session ID : $sessionId" -ForegroundColor White
    Write-Host "  Web UI URL : $sessionUrl" -ForegroundColor Yellow
    Write-Host "----------------------------------------------------------" -ForegroundColor DarkGray

    # Копирование в системный буфер обмена
    try {
        Set-Clipboard -Value $sessionUrl -ErrorAction SilentlyContinue
        Write-Host "  📋 Ссылка скопирована в буфер обмена." -ForegroundColor Gray
    } catch {
        # Игнорируем ошибки headless буфера
    }

    # Открытие в браузере по умолчанию
    if (-not $NoBrowser) {
        Write-Host "  🌐 Открытие веб-интерфейса в браузере..." -ForegroundColor Cyan
        Start-Process -FilePath $sessionUrl
    }
    Write-Host "==========================================================`n" -ForegroundColor Green
} else {
    Write-Warning "Не удалось автоматически перехватить session-id за $TimeoutSeconds секунд."
    Write-Host "Подсказка:" -ForegroundColor Yellow
    Write-Host "  1. Проверьте запущенное окно Antigravity CLI." -ForegroundColor Gray
    Write-Host "  2. Убедитесь, что вы авторизованы ('agy login')." -ForegroundColor Gray
    Write-Host "  3. При необходимости введите команду '/remote-control' прямо в активном CLI." -ForegroundColor Gray
}
