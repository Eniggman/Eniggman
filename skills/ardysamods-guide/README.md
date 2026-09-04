# 🎮 ArdysaMods — Комплексное руководство и инструментарий для модов Dota 2

[![Dota 2](https://img.shields.io/badge/Game-Dota%202-red.svg?style=for-the-badge&logo=dota2)](https://www.dota2.com/)
[![ArdysaModsTools](https://img.shields.io/badge/Launcher-ArdysaModsTools-blue.svg?style=for-the-badge&logo=github)](https://github.com/Anneardysa/ArdysaModsTools)
[![PowerShell](https://img.shields.io/badge/Shell-PowerShell%207%20%2F%205.1-blue.svg?style=for-the-badge&logo=powershell)](https://github.com/PowerShell/PowerShell)
[![VPKEdit](https://img.shields.io/badge/CLI-VPKEdit%20CLI-orange.svg?style=for-the-badge)](https://github.com/craftablescience/VPKEdit)
[![Status](https://img.shields.io/badge/Status-Active%20%26%20Tested-brightgreen.svg?style=for-the-badge)]()

Исчерпывающее техническое руководство, готовые проверенные пресеты и инструменты для комфортной и стабильной игры с модами **ArdysaMods** в Dota 2.

Репозиторий архитектурно разделён на **два взаимодополняющих модуля**:
1. **📘 МОДУЛЬ 1 (Ниже): Руководство по работе с лаунчером ArdysaModsTools (Штатный режим)**  
   Пошаговый гайд по правильной установке мод-пака `pak01_dir.vpk`, выбору Аркан, Личностей и предметов через графический интерфейс, настройке окружения во вкладке `MISCELLANEOUS` (ландшафты, вышки, крипы, музыка) и быстрому 30-секундному Re-patch при микро-обновлениях Dota 2.
2. **⚙️ МОДУЛЬ 2: Ручное удаление сетов и хирургия мод-пака (Аварийный & Продвинутый режим)**  
   Практическое руководство по ручному вырезанию и удалению сетов героев непосредственно из архива `pak01_dir.vpk`. Модуль незаменим, когда:
   * В лаунчере после очередного обновления Dota 2 **сломался селектор сетов** (зависает, не переключает скины, не видит героев или сбрасывает выбор);
   * Определённый кастомный сет **крашит клиент Dota 2** (Crash to Desktop) или вызывает визуальные баги, и его необходимо экстренно удалить из файлов мода;
   * Требуется **кардинально облегчить архив мод-пака** с 15+ ГБ до <1 ГБ, оставив только активный пул героев без нарушения ссылочной целостности `items_game.txt` и Valve Econ Schema.  
   👉 [**Перейти к полному гайду Модуля 2 ➔**](./docs/MODULE_2_VPK_OPTIMIZER.md)

---

# 📘 МОДУЛЬ 1: Руководство по установке и настройке (ArdysaModsTools)

> **🎯 Для кого этот гайд:** Для игроков Dota 2, которые хотят быстро и без головной боли включить любые Арканы, Личности, сеты, кастомные ландшафты, вышки, крипов и музыку через удобный графический интерфейс.
>
> 💡 **В штатном режиме** выбор, комбинирование и отключение сетов происходят прямо в окне программы.  
> ⚠️ **Если селектор сломался:** переходите к [Модулю 2: Ручное удаление сетов](./docs/MODULE_2_VPK_OPTIMIZER.md).

---

## 📋 Оглавление Модуля 1
1. [Подготовка и необходимые файлы](#1-подготовка-и-необходимые-файлы)
2. [Шаг 1: Правильная установка мод-пака (Install mod pack)](#2-шаг-1-правильная-установка-мод-пака-install-mod-pack)
3. [Шаг 2: Выбор и переключение сетов в интерфейсе](#3-шаг-2-выбор-и-переключение-сетов-в-интерфейсе)
4. [Шаг 3: Настройка карт, вышек, крипов и музыки (MISCELLANEOUS)](#4-шаг-3-настройка-карт-вышек-крипов-и-музыки-miscellaneous)
5. [Шаг 4: Проверка целостности и применение патча (Patch update)](#5-шаг-4-проверка-целостности-и-применение-патча-patch-update)
6. [Шаг 5: Что делать при обновлениях Dota 2 (Быстрый Re-patch)](#6-шаг-5-что-делать-при-обновлениях-dota-2-быстрый-re-patch)
7. [Решение частых проблем (FAQ & Troubleshooting)](#7-решение-частых-проблем-faq--troubleshooting)

---

## 1. Подготовка и необходимые файлы

Мод-пак **ArdysaMods** открывает доступ ко всем косметическим элементам Dota 2:
* 👑 **Все Арканы и Личности (Personas)**, включая эксклюзивные предметы прошлых Battle Pass.
* ✨ **Immortal-предметы** с кастомными анимациями и иконками способностей.
* 🗺️ **Ландшафты (Map Terrains):** *Sanctum of the Divine*, *Immortal Gardens*, *Reef's Edge*, *Overgrown Empire* и др.
* 🏰 **Кастомные башни (Towers):** *The Eyes of Avilliva*, *The Gaze of Scree'Auk*, *Grasp of the Elder Gods*.
* 👾 **Крипы и осадные машины:** *Nemestice*, *Dark Carnival*, *Crownfall*.
* 🎵 **Музыкальные паки:** *Deadmau5*, *Harmonies of New Bloom*, *The FatRat*, *AWOLNATION*.
* 🌊 **Скины реки, погодные эффекты, HUD, курсоры, скины Рошана, курьеров и вардов**.

### Что потребуется:
1. **ArdysaModsTools** — официальный графический лаунчер ([Скачать на GitHub](https://github.com/Anneardysa/ArdysaModsTools)).
2. **Файл мод-пака `pak01_dir.vpk`** — оригинальный или оптимизированный архив:
   * [Официальный Discord Ardysa Mods](https://discord.gg/GXuhAwte) (канал `#update-mods`).
   * [Сайт обновлений ArdysaMods](https://ardysamods.my.id/updates.html).
3. **Установленная Dota 2** в Steam.

> [!TIP]
> Перед выполнением любых действий с лаунчером убедитесь, что игра **Dota 2 полностью закрыта**.

---

## 2. Шаг 1: Правильная установка мод-пака (Install mod pack)

Для корректной инициализации мода в лаунчере:

1. Запустите **`ArdysaModsTools.exe`** (рекомендуется запускать от имени администратора).
2. На главном экране лаунчера нажмите большую кнопку **`Install mod pack`**.
3. В появившемся меню выберите вариант **`Manual install`**.
4. В окне проводника укажите ваш файл **`pak01_dir.vpk`**.
5. **⚡ КРИТИЧЕСКИ ВАЖНО:** При вопросе о сохранении файла выберите:
   > **`Keep original`** (*Оставить оригинал*)
   
   Это сохранит эталонную копию вашего архива и защитит его от повреждений при сбоях.
6. Нажмите **`Continue`** и дождитесь завершения импорта.

```text
+-------------------------------------------------------------+
|                      ArdysaModsTools                        |
|  [ Install mod pack ] -> [ Manual install ]                 |
|       |                                                     |
|       v                                                     |
|  Выбрать: pak01_dir.vpk -> Опция: [ Keep original ]         |
|       |                                                     |
|       v                                                     |
|  Нажать: [ Continue ] -> Завершение импорта                 |
+-------------------------------------------------------------+
```

---

## 3. Шаг 2: Выбор и переключение сетов в интерфейсе

### Как настроить персонажей:
1. Перейдите во вкладку героев в меню лаунчера.
2. Найдите интересующего героя (например, *Anti-Mage*, *Pudge*, *Rubick*, *Io*, *Sniper*, *Earthshaker*, *Luna*).
3. Для каждого персонажа вы можете:
   * **Выбрать полный готовый сет:** Аркану, Личность или коллекционный бандл.
   * **Скомбинировать отдельные слоты:** надеть Immortal-оружие, кастомные плечи, голову или насмешку.
   * **Сбросить на дефолт (Default):** если вы хотите вернуть базовый облик героя без мода, выберите стандартный скин. Лаунчер автоматически исключит кастомные модели.
4. Настройки сохраняются в ваш пользовательский профиль.

> [!TIP]
> В папке [`presets/skins_preset.json`](./presets/skins_preset.json) доступен готовый эталонный пресет с красивыми сетами на популярных героев.

---

## 4. Шаг 3: Настройка карт, вышек, крипов и музыки (MISCELLANEOUS)

Вкладка **MISCELLANEOUS** управляет глобальным окружением игры:

1. В верхнем меню лаунчера перейдите во вкладку **`MISCELLANEOUS`**.
2. Выберите желаемые настройки:
   * **Map (Ландшафт):** *Sanctum of the Divine*, *Immortal Gardens*, *Reef's Edge*, *Overgrown Empire* и др.
   * **Radiant Tower / Dire Tower (Башни):** *The Eyes of Avilliva*, *The Gaze of Scree'Auk*, *Grasp of the Elder Gods*.
   * **Radiant Creep / Dire Creep (Крипы):** *Nemestice*, *Dark Carnival*, *Crownfall*.
   * **Music (Музыка):** *Deadmau5 Music*, *Harmonies of New Bloom*, *The FatRat*, *AWOLNATION*.
   * **River (Эффекты реки):** *Chrome Vial*, *Oil Vial*, *Electric Vial*.
   * **HUD, Weather, Versus, Ancient, Roshan, Courier, Ward**.
3. **Применение окружения:**
   * В правом нижнем углу нажмите кнопку **`Generate`**.
   * В появившемся диалоговом окне обязательно выберите **`Add to Current Mods`** (*Добавить к текущим модам*).
   * Это наложит окружение поверх ваших скинов без конфликтов.

```text
[ Вкладка MISCELLANEOUS ]
  ├── 1. Выбрать Map, Towers, Creeps, Music, River, HUD
  ├── 2. Нажать кнопку "Generate"
  └── 3. Выбрать опцию "Add to Current Mods"
```

> [!TIP]
> Проверенные конфигурации окружения доступны в папке пресетов:
> * [`presets/MiscPreset.json`](./presets/MiscPreset.json) — ландшафт *Sanctum of the Divine*, вышки *Elder Gods*, крипы *Nemestice*, музыка *New Bloom*.
> * [`presets/dota.json`](./presets/dota.json) — ландшафт *Sanctum of the Divine*, музыка *Deadmau5*, вышки *Eyes of Avilliva*.

---

## 5. Шаг 4: Проверка целостности и применение патча (Patch update)

Финальный шаг, который активирует все выбранные скины и окружение в клиенте игры:

1. Перейдите в раздел **`Patch update`** в меню лаунчера.
2. Нажмите кнопку **`Verify mod file`** (*Проверить файлы мода*).
3. Дождитесь успешной проверки (зелёная индикация / статус *Ready*).
4. Нажмите кнопку **`Patch Update`** (*Применить патч*).
5. После завершения процесса (статус *Success*) закройте лаунчер и запустите Dota 2 в Steam.
6. **Готово! Все моды активированы.**

---

## 6. Шаг 5: Что делать при обновлениях Dota 2 (Быстрый Re-patch)

Когда Valve выпускает обновление Dota 2 в Steam, игровые файлы обновляются, и моды временно деактивируются.

### ⏱️ Быстрый Re-patch за 30 секунд:
```text
1. Дождитесь загрузки обновления Dota 2 в Steam.
                           |
                           v
2. Запустите ArdysaModsTools.
                           |
                           v
3. Перейдите в раздел "Patch update".
                           |
                           v
4. Нажмите "Verify mod file", затем "Patch Update".
                           |
                           v
5. Запустите Dota 2 — всё снова работает!
```

### 🚨 При крупных (глобальных) патчах игры:
Если после крупного патча Dota 2 игра не запускается:
1. Зайдите в [Discord Ardysa Mods](https://discord.gg/GXuhAwte) (канал `#update-mods`).
2. Скачайте свежий `pak01_dir.vpk`, адаптированный авторами под новую версию игры.
3. Установите его через `Install mod pack` ➔ `Manual install` ➔ `Keep original`.
4. Примените `MISCELLANEOUS` ➔ `Generate` ➔ `Add to Current Mods` и нажмите `Patch Update`.

---

## 7. Решение частых проблем (FAQ & Troubleshooting)

### ❓ Сломался селектор в лаунчере, список героев зависает или игра вылетает:
* **Причина:** Обновление схемы Valve Econ Schema, повреждение кэша пресета `skins_preset.json` или битый скин в мод-паке.
* **Решение:** Воспользуйтесь инструкциями **[Модуля 2: Ручное удаление сетов и хирургия мод-пака](./docs/MODULE_2_VPK_OPTIMIZER.md)**:
  * Быстрый сброс настроек через [`presets/skins_preset.json`](./presets/skins_preset.json).
  * Ручное вырезание проблемного героя или конкретного сета через утилиту **VPKEdit**.

### ❓ В игре вместо предметов красные надписи "ERROR":
* **Причина:** Не был выполнен `Patch Update` после изменения скинов, либо Дота обновилась в Steam.
* **Решение:** Закройте Доту, откройте лаунчер, перейдите в `Patch update` ➔ `Verify mod file` ➔ `Patch Update`.

### ❓ Пропала карта или музыка после смены сетов:
* **Причина:** При генерации во вкладке `MISCELLANEOUS` случайно была выбрана замена модов.
* **Решение:** Зайдите в `MISCELLANEOUS`, нажмите `Generate` ➔ **`Add to Current Mods`**, затем выполните `Patch Update`.

### ❓ Ошибка доступа при установке:
* **Причина:** Dota 2 или Steam запущены в фоне, либо не хватает прав Windows.
* **Решение:** Закройте Dota 2 и Steam через Диспетчер задач, запустите лаунчер от имени администратора.

---

# ⚙️ МОДУЛЬ 2: Ручное удаление сетов и хирургия мод-пака (Аварийный & Продвинутый)

> 📖 **Полная документация:** [**Руководство по ручному вырезанию сетов и оптимизации VPK ➔**](./docs/MODULE_2_VPK_OPTIMIZER.md)

### Когда необходим Модуль 2:
1. **Сломался выбор сетов в лаунчере:** Лаунчер зависает, не переключает скины или не дает снять скин с героя.
2. **Конкретный сет крашит Dota 2:** Вылет на рабочий стол (CTD) при пике персонажа или входе в матч из-за битых полигонов или эффектов.
3. **Оптимизация VPK до <1 ГБ:** Сжатие пака с 15+ ГБ до <1 ГБ для мгновенной загрузки игры на слабых ПК и SSD.

### 🛠️ Краткий обзор методов Модуля 2:

* **⚡ Способ 0: Экспресс-реанимация конфига (`skins_preset.json`)**  
  Без распаковки VPK. Закрыть лаунчер, открыть `skins_preset.json`, очистить блок проблемного героя или подставить готовый пресет [`presets/skins_preset.json`](./presets/skins_preset.json).
* **🖱️ Способ 1: Ручное вырезание через VPKEdit (GUI)**  
  Открыть `pak01_dir.vpk` в [VPKEdit](https://github.com/craftablescience/VPKEdit/releases). Найти папки героя:
  * `models/items/<hero_name>/` (кастомные сеты, Арканы, Личности)
  * `materials/models/items/<hero_name>/` (текстуры)
  * `particles/econ/items/<hero_name>/` (эффекты)
  * Авторские папки: `kisilev_ind/models/<hero_name>/`, `8213/heroes/<hero_name>/`  
  Удалить папки проблемного героя или отдельный крашащий сет и сохранить архив (`Ctrl + S`).
* **🚀 Способ 2: Пакетная сборка чистого дерева через PowerShell**  
  Распаковать VPK через `vpkeditcli`, указать нужных героев в `vpk_mod_config.json`, запустить [`scripts/build_filtered_tree.ps1`](./scripts/build_filtered_tree.ps1) и упаковать чистый архив.

### 📚 Материалы Модуля 2:
* 📖 [**Полное техническое руководство Модуля 2**](./docs/MODULE_2_VPK_OPTIMIZER.md)
* 🗂️ [**Справочник внутренней структуры архивов VPK Dota 2**](./docs/vpk_structure.md)
* 📜 **Скрипты автоматизации:**
  * [`scripts/build_filtered_tree.ps1`](./scripts/build_filtered_tree.ps1) — фильтрация и сборка чистого дерева ассетов.
  * [`scripts/optimize.ps1`](./scripts/optimize.ps1) — in-place зачистка каталогов.
  * [`scripts/analyze_items_game_refs.py`](./scripts/analyze_items_game_refs.py) — анализатор связей `items_game.txt`.

---

## 🎛️ Каталог пресетов (Presets)

В папке [`presets/`](./presets/) содержатся проверенные конфигурационные файлы:
* [`presets/MiscPreset.json`](./presets/MiscPreset.json) — пресет окружения (карта *Sanctum of the Divine*, вышки, крипы, музыка).
* [`presets/skins_preset.json`](./presets/skins_preset.json) — эталонный профиль выбранных сетов и Аркан на героев.
* [`presets/dota.json`](./presets/dota.json) — компактная конфигурация лаунчера.
* [`presets/vpk_mod_config.template.json`](./presets/vpk_mod_config.template.json) — шаблон манифеста для легковесной сборки VPK.
* [Подробное руководство по пресетам ➔](./presets/README.md)

---

## 🌐 Официальные ресурсы
* [ArdysaModsTools GitHub](https://github.com/Anneardysa/ArdysaModsTools) — официальный лаунчер модов.
* [Discord Ardysa Mods](https://discord.gg/GXuhAwte) — официальное сообщество (канал `#update-mods`).
* [ArdysaMods Updates](https://ardysamods.my.id/updates.html) — сайт обновлений и витрина сетов.
* [VPKEdit Releases](https://github.com/craftablescience/VPKEdit/releases) — GUI и CLI для редактирования VPK архивов.
