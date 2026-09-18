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
    Launcher->>Browser: termux-open-url / Start-Process URL
    Browser->>Gateway: Подключение Live Sync
    Gateway-->>Browser: Канал связи установлен
    Gateway->>CLI: Двусторонняя репликация стейта
    CLI-->>Browser: Стриминг (Diff, Term, Thinking, Tools)
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

## 🚀 Быстрый старт и ярлыки

### 🪟 Windows: Ярлык на Рабочем столе и Windows Terminal

В репозитории есть готовый скрипт, который создаёт нативный ярлык Windows с официальной иконкой `agy.exe`.

#### 1. Создание ярлыка в один клик:
Запустите скрипт из папки проекта:
```powershell
powershell -ExecutionPolicy Bypass -File ".\scripts\create-desktop-shortcut.ps1"
```

#### 2. Что происходит при клике на созданный ярлык `Remote Control AGY`:
1. В тихом скрытом режиме (`-WindowStyle Hidden`) запускается лаунчер `start-remote-control.ps1`.
2. На экране открывается **Windows Terminal (`wt.exe`)** с сессией `agy --remote-control` в рабочей папке (по умолчанию `D:\Coding`).
3. Лаунчер за ~1 секунду считывает сгенерированный Session UUID из журнала `~/.gemini/antigravity-cli/log/`.
4. Ссылка копируется в буфер обмена Windows и **автоматически открывается в вашем браузере по умолчанию** (`https://antigravity.google.com/r/<session-id>`).
5. Терминал остаётся активным перед глазами для синхронной работы (Live Sync).

#### 💡 Назначение горячей клавиши (HotKey):
1. Нажмите правой кнопкой мыши по созданному ярлыку **Remote Control AGY** на Рабочем столе → выберите **«Свойства»**.
2. Перейдите на вкладку **«Ярлык»** и кликните в поле **«Быстрый вызов» (Shortcut key)**.
3. Нажмите комбинацию (например, `Ctrl + Alt + A`) и нажмите **OK**.  
*Теперь удалённая сессия с автооткрытием в браузере запускается в любое время одной комбинацией клавиш!*

---

### 📱 Android (Termux): Виджет быстрого запуска на домашнем экране

Для Android предусмотрена бесшовная интеграция с **[Termux:Widget](https://github.com/termux/termux-widget)** — запуск сессии и открытие браузера в один тап по экрану смартфона.

#### 1. Необходимые компоненты:
Убедитесь, что установлены приложения из F-Droid (подписанные одним ключом):
- [Termux](https://f-droid.org/packages/com.termux/)
- [Termux:API](https://f-droid.org/packages/com.termux.api/)
- [Termux:Widget](https://f-droid.org/packages/com.termux.widget/)

В терминале Termux установите зависимости:
```bash
pkg update && pkg install termux-api jq grep -y
```

#### 2. Генерация скрипта виджета в один клик:
Выполните команду:
```bash
chmod +x scripts/start-remote-control.sh
./scripts/start-remote-control.sh --install-widget
```
*Скрипт автоматически создаст исполняемый лаунчер `~/.shortcuts/Antigravity-Remote.sh` с правильными правами доступа.*

#### 3. Добавление виджета на рабочий стол Android:
1. Выйдите на домашний экран смартфона.
2. Зажмите палец на пустом месте экрана → откройте меню **«Виджеты» (Widgets)**.
3. Прокрутите до раздела **Termux:Widget** и выберите элемент **«Termux shortcut»** (одиночная иконка) или **«Termux:Widget»** (панель списка).
4. В появившемся списке скриптов выберите **`Antigravity-Remote.sh`**.
5. Ярлык появится на домашнем экране!

#### 4. Как это работает в Android:
* Нажимаете на иконку на рабочем столе смартфона:
  1. В Termux мгновенно запускается сессия `agy --remote-control`.
  2. Скрипт перехватывает ссылку, копирует её в системный буфер Android (`termux-clipboard-set`).
  3. Отправляет виброотклик и push-уведомление в шторку уведомлений Android.
  4. **Автоматически открывает мобильный браузер (`termux-open-url`)** с готовым веб-интерфейсом Live Sync!


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
