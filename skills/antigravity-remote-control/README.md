# 🛰️ Antigravity Remote Control (v1.2.6+)

[![Antigravity CLI](https://img.shields.io/badge/Antigravity_CLI-v1.2.6+-orange?style=for-the-badge&logo=google&logoColor=white)](https://github.com/google)
[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Android](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://www.android.com/)
[![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white)](https://termux.dev/)
[![Transport: WebChannel](https://img.shields.io/badge/Transport-WebChannel%20%2F%20TLS-blue?style=for-the-badge&logo=google-cloud&logoColor=white)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

[![Topic: antigravity](https://img.shields.io/badge/antigravity-E37400?style=flat-square&logo=google&logoColor=white)](#)
[![Topic: antigravity-remote](https://img.shields.io/badge/antigravity--remote-1A73E8?style=flat-square&logo=google-chrome&logoColor=white)](#)
[![Topic: antigravity-ui](https://img.shields.io/badge/antigravity--ui-34A853?style=flat-square&logo=material-design&logoColor=white)](#)
[![Topic: agy](https://img.shields.io/badge/agy-9334E6?style=flat-square&logo=gnubash&logoColor=white)](#)
[![Topic: remote-control](https://img.shields.io/badge/remote--control-EA4335?style=flat-square&logo=google-play&logoColor=white)](#)
[![Topic: live-sync](https://img.shields.io/badge/live--sync-00ACC1?style=flat-square&logo=socketdotio&logoColor=white)](#)
[![Topic: termux-tools](https://img.shields.io/badge/termux--tools-000000?style=flat-square&logo=termux&logoColor=white)](#)

> 🚀 **Удалённый пульт управления Antigravity CLI прямо в вашем браузере!**  
> Мгновенный запуск сессий с ПК или Android (Termux) с автоматическим перехватом сессионных ссылок, открытием браузера, интеграцией с Termux:Widget и созданием ярлыка рабочего стола.

---

## 📖 О проекте

Начиная с версии **1.2.6**, в **Antigravity CLI** появилась возможность удалённого управления через веб-интерфейс `https://antigravity.google.com/r/<session-id>`.

Однако ручной процесс запуска требует:
1. Запускать `agy --remote-control`.
2. Ждать установки туннеля.
3. Вручную искать ссылку в выводе или логах.
4. Копировать длинный URL и открывать его в браузере.

Навык **antigravity-remote-control** полностью автоматизирует этот процесс для **Windows** и **Android Termux** — вы запускаете скрипт (или нажимаете ярлык/виджет на экране смартфона), и перед вами сразу открывается активный веб-интерфейс с живой синхронизацией!

---

## ⚡ Архитектура Live Sync

```mermaid
sequenceDiagram
    autonumber
    actor User as 👤 Разработчик
    participant Launcher as 🚀 Скрипт (PS1 / Bash)
    participant CLI as 💻 Antigravity CLI
    participant Gateway as ☁️ Google WebChannel
    participant Browser as 🌐 Web UI (antigravity.google.com)

    User->>Launcher: Запуск (ярлык / виджет / консоль)
    Launcher->>CLI: Старт 'agy --remote-control'
    CLI->>Gateway: Регистрация V2 туннеля (WebChannel)
    Gateway-->>CLI: Назначение UUID сессии
    CLI->>CLI: Запись [remote-control-:uuid-v2] в лог
    Launcher->>Launcher: Безопасное чтение лога (FileShare.ReadWrite)
    Launcher->>Browser: termux-open-url / Start-Process URL
    Browser<->>Gateway: Подключение Live Sync
    Gateway<->>CLI: Двусторонняя репликация стейта (Diff, Term, Thinking, Tools)
    User->>Browser: Управление агентом и подтверждение действий
```

---

## 🎯 Сравнение режимов

| Параметр | ⚡ Session-scoped (Скрипты навыка) | 🌐 Persistent Cloud Daemon |
| :--- | :--- | :--- |
| **Команда** | `agy --remote-control` | `agy remote-control start` |
| **Жизненный цикл** | Автоматически закрывается вместе с терминалом | Работает в фоне 24/7 до перезагрузки |
| **Безопасность** | Строго в рамках текущего окна CLI | Фоновый доступ к рабочим пространствам |
| **Веб-интерфейс** | Индивидуальная сессия `.../r/<uuid>` | Общий реестр машин в аккаунте |
| **Для чего лучше** | Парное программирование со смартфона / в пути | Стационарный сервер или облачная ВМ |

---

## 🚀 Быстрый старт

### 🪟 Windows

1. **Создание ярлыка на Рабочем столе в один клик:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File ".\scripts\create-desktop-shortcut.ps1"
   ```
   *Скрипт автоматически найдет `agy.exe`, назначит официальную иконку и положит `Remote Control AGY.lnk` на Рабочий стол.*

2. **Ручной запуск из терминала:**
   ```powershell
   powershell -ExecutionPolicy Bypass -File ".\scripts\start-remote-control.ps1"
   ```
   *Параметры:*
   - `-WorkDir "D:\Projects\MyApp"` — выбор папки проекта.
   - `-AgyArgs "--model gemini-2.5-pro"` — дополнительные флаги CLI.
   - `-NoBrowser` — не открывать браузер автоматически (только скопировать ссылку).

---

### 📱 Android (Termux)

1. **Установка необходимых пакетов:**
   ```bash
   pkg update && pkg install termux-api jq grep
   ```
   *(Убедитесь, что установлено дополнение [Termux:API](https://github.com/termux/termux-api)).*

2. **Запуск из командной строки:**
   ```bash
   chmod +x scripts/start-remote-control.sh
   ./scripts/start-remote-control.sh
   ```
   *Скрипт перехватит ссылку сессии, скопирует в буфер обмена, пришлет системное уведомление и откроет браузер.*

3. **Установка виджета Termux:Widget (Запуск в 1 тап):**
   ```bash
   ./scripts/start-remote-control.sh --install-widget
   ```
   *Добавьте виджет `Termux:Widget` на домашний экран Android и запускайте управление в одно касание!*

---

## 🛠️ Состав репозитория

```
skills/antigravity-remote-control/
├── SKILL.md                          # Полная архитектурная спецификация навыка
├── README.md                         # Документация для пользователей
└── scripts/
    ├── start-remote-control.ps1      # Портативный лаунчер для Windows (wt / powershell)
    ├── start-remote-control.sh       # Портативный лаунчер для Termux / Linux
    └── create-desktop-shortcut.ps1   # Создание ярлыка Windows с оригинальной иконкой
```

---

## 🔒 Безопасность и Приватность

- **100% Портативность:** Никаких абсолютных путей к папкам конкретных пользователей. Используются исключительно `$env:USERPROFILE`, `$env:LOCALAPPDATA`, `$HOME`, `$PREFIX`.
- **Безопасное чтение логов:** Использование .NET `[System.IO.FileShare]::ReadWrite` предотвращает конфликты блокировки файлов журнала работающим процессом Antigravity.
- **Официальный транспорт Google:** Соединение устанавливается напрямую между локальным CLI и защищенными шлюзами Google WebChannel по TLS без сторонних серверов-посредников.

---

## 📄 Лицензия

Распространяется под лицензией **MIT**. Разработано для открытого сообщества разработчиков и пользователей Termux & Antigravity.
