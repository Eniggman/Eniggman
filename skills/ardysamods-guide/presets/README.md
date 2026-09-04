# 🎛️ Каталог эталонных пресетов (Presets Directory)

В этой директории собраны готовые проверенные конфигурационные файлы для лаунчера **ArdysaModsTools** и скриптов оптимизации VPK.

---

## 📁 Содержимое каталога:

### 1. [`MiscPreset.json`](./MiscPreset.json)
- **Назначение:** Пресет кастомизации окружения и карты для вкладки `MISCELLANEOUS` в лаунчере ArdysaModsTools.
- **Включает:**
  - **Map:** *Sanctum of the Divine*
  - **Radiant Tower / Dire Tower:** *Grasp of the Elder Gods*
  - **Radiant Creep / Dire Creep:** *Nemestice* / *Dark Carnival*
  - **Music:** *Harmonies of New Bloom Music*
  - **River:** *Chrome Vial*
  - **Ancient / Roshan:** *New Bloom Ancient Dragon* / *Roshan Cosmic 2025*
  - **HUD:** *Default HUD*

### 2. [`skins_preset.json`](./skins_preset.json)
- **Назначение:** Профиль выбранных скинов и сетов для героев в ArdysaModsTools.
- **Включает:** Настроенные наборы для популярных персонажей (*Anti-Mage*, *Pudge*, *Rubick*, *Io*, *Sniper*, *Earthshaker*, *Luna*, *Faceless Void*, *Legion Commander*, *Marci*, *Terrorblade*, *Tusk*, *Spectre* и др.).
- **Использование:** Позволяет мгновенно загрузить проверенную комбинацию Аркан и Immortal-предметов без ручной настройки каждого персонажа.

### 3. [`dota.json`](./dota.json)
- **Назначение:** Альтернативный компактный профиль лаунчера ArdysaModsTools.
- **Включает:**
  - **Map:** *Sanctum of the Divine*
  - **Music:** *Deadmau5 Music*
  - **Radiant Tower / Dire Tower:** *The Eyes of Avilliva* / *The Gaze of Scree'Auk*
  - **Creeps / Siege:** *Nemestice* / *Crownfall*

### 4. [`vpk_mod_config.template.json`](./vpk_mod_config.template.json)
- **Назначение:** Эталонный манифест для скрипта фильтрации [`scripts/build_filtered_tree.ps1`](../scripts/build_filtered_tree.ps1) (Модуль 2).
- **Использование:** Скопируйте этот файл в корень рабочего каталога как `vpk_mod_config.json`, отредактируйте список `active_roster` и запустите сборку легкого VPK архива.

---

## 🚀 Как применить пресеты в лаунчере:
1. Закройте ArdysaModsTools.
2. Скопируйте нужный `.json` файл в рабочую папку лаунчера (или используйте функцию импорта пресета в интерфейсе).
3. Откройте ArdysaModsTools, проверьте настройки и выполните `Patch update` -> `Verify mod file` -> `Patch Update`.

---

## 🔗 Связанные руководства
- [Модуль 1: Базовый гайд для игроков](../docs/MODULE_1_USAGE_GUIDE.md)
- [Модуль 2: Ручное удаление сетов и оптимизация VPK](../docs/MODULE_2_VPK_OPTIMIZER.md)