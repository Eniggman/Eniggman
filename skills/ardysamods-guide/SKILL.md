name: dota-surgical-vpk-optimizer
description: Комплексный инструментарий и экспертный ассистент по экосистеме ArdysaMods для Dota 2. Включает Модуль 1 (базовое руководство для игроков по лаунчеру ArdysaModsTools, выбору сетов в UI, настройке окружения MISCELLANEOUS и быстрому Re-patch) и Модуль 2 (ручное удаление и вырезание сетов героев из VPK при поломке селектора в лаунчере, вылетах игры, а также глубокая хирургическая оптимизация и пересборка архива через PowerShell и VPKEdit).
---

# ArdysaMods & Dota 2 Surgical VPK Toolkit

Этот навык оснащает ИИ-ассистента полной технической экспертизой по работе с модами Dota 2 в экосистеме **ArdysaMods**.

Навык охватывает два ключевых сценария взаимодействия:
1. **МОДУЛЬ 1 (Штатный сценарий для игроков):** Пошаговая консультация и помощь в работе с графическим лаунчером **ArdysaModsTools** (установка `pak01_dir.vpk`, выбор сетов в UI, настройка ландшафта, вышек и музыки во вкладке `MISCELLANEOUS`, применение `Patch update`, быстрый re-patch при микро-патчах Dota 2).
2. **МОДУЛЬ 2 (Аварийный & Продвинутый сценарий — ручное вырезание сетов):** Ручное удаление сетов героев непосредственно из архива `pak01_dir.vpk`. Применяется, когда в лаунчере **сломался селектор сетов**, конкретный скин **крашит клиент игры**, либо требуется **сжать архив с 15+ ГБ до <1 ГБ** через PowerShell-скрипты без повреждения `scripts/items/items_game.txt`.

---

## 🧭 Маршрутизация запросов пользователя

### 1. Если пользователь спрашивает:
- «Как установить моды / Арканы через лаунчер?»
- «Как настроить карту, вышки или музыку?»
- «Как поменять скин на герое в лаунчере?»
- «Что делать после обычного микро-обновления Доты?»
- «Почему в игре надписи ERROR?»
👉 **Используйте инструкции МОДУЛЯ 1** ([`docs/MODULE_1_USAGE_GUIDE.md`](./docs/MODULE_1_USAGE_GUIDE.md)).
- Рекомендуйте использовать **ArdysaModsTools**.
- Напоминайте при установке всегда выбирать опцию `Keep original`.
- В штатном режиме сеты переключаются прямо в интерфейсе без необходимости удалять файлы.
- Для окружения напоминайте цепочку: `MISCELLANEOUS` -> `Generate` -> `Add to Current Mods` -> `Patch update` -> `Verify mod file` -> `Patch Update`.

### 2. Если пользователь спрашивает:
- «В лаунчере сломался выбор сетов, что делать?»
- «Игра вылетает из-за сета / как удалить сет Пуджа/Морфа/героя?»
- «Как вручную вырезать героев из мод-пака VPK?»
- «Как удалить ненужные файлы через VPKEdit?»
- «Как уменьшить размер пака до 1 ГБ?»
- «Как запустить build_filtered_tree.ps1?»
- «Почему игра крашится при редактировании items_game.txt?»
👉 **Используйте инструкции МОДУЛЯ 2** ([`docs/MODULE_2_VPK_OPTIMIZER.md`](./docs/MODULE_2_VPK_OPTIMIZER.md)).
- Предложите Способ 0 (экспресс-сброс или правка `skins_preset.json` в папке лаунчера).
- Предложите Способ 1 (открыть `pak01_dir.vpk` в утилите **VPKEdit**, найти папки `models/items/<hero>`, `materials/models/items/<hero>`, `particles/econ/items/<hero>` и удалить их без распаковки всего пака).
- Предложите Способ 2 (пакетная фильтрация через `build_filtered_tree.ps1` и манифест `vpk_mod_config.json`).
- Предостерегайте от бездумного удаления блоков из `items_game.txt` (ошибки `EVENT_ID_WINTER_MAJOR_2016` и `effects_item_def 16844`).

---

## 📁 Структура и ключевые ресурсы репозитория

- 📘 **[`docs/MODULE_1_USAGE_GUIDE.md`](./docs/MODULE_1_USAGE_GUIDE.md)** — Гайд для игроков по лаунчеру ArdysaModsTools.
- ⚙️ **[`docs/MODULE_2_VPK_OPTIMIZER.md`](./docs/MODULE_2_VPK_OPTIMIZER.md)** — Руководство по ручному вырезанию сетов и оптимизации VPK.
- 🗂️ **[`docs/vpk_structure.md`](./docs/vpk_structure.md)** — Справочник структуры файлов и виртуальных путей Dota 2.
- 🎛️ **[`presets/`](./presets/)**:
  - `MiscPreset.json` — конфигурация карты, вышек, крипов и музыки.
  - `skins_preset.json` — эталонный профиль выбранных скинов персонажей.
  - `dota.json` — конфигурация лаунчера.
  - `vpk_mod_config.template.json` — шаблон манифеста для фильтрации VPK.
- 🛠️ **[`scripts/`](./scripts/)**:
  - `build_filtered_tree.ps1` — сборка чистого filtered-дерева из распакованного архива.
  - `optimize.ps1` — in-place зачистка каталогов.
  - `analyze_items_game_refs.py` — анализ целостности связей `items_game.txt`.
  - `sanitize_items_game.py` — экспериментальный санитайзер.

---

## ⚡ Быстрые команды для ИИ-ассистента

### Ручная вырезка в VPKEdit:
- Папки для удаления героя:
  - `models/items/<hero_name>/`
  - `materials/models/items/<hero_name>/`
  - `particles/econ/items/<hero_name>/`
  - `kisilev_ind/models/<hero_name>/` (если есть)

### Построение фильтрованного дерева (PowerShell):
```powershell
.\scripts\build_filtered_tree.ps1 `
  -SourceRoot "<build_dir>\source\pak01_dir_original" `
  -DestinationRoot "<build_dir>\filtered\pak01_dir" `
  -ConfigPath "<project_root>\vpk_mod_config.json"
```

### Упаковка и верификация через VPKEdit CLI:
```powershell
vpkeditcli --save "<build_dir>\filtered\pak01_dir" --output "<project_root>\pak01_dir_rebuilt.vpk"
vpkeditcli --verify-checksums all "<project_root>\pak01_dir_rebuilt.vpk"
```
