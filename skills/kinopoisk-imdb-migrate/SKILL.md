---
name: kinopoisk-imdb-migrate
description: "Автоматизированная миграция оценок и списков «Буду смотреть» (Watchlist) с Кинопоиска в IMDb через браузерные JS-скрипты, Python-конвертеры и сопоставление IMDb/Letterboxd ID."
---

# Кинопоиск → IMDb Migration Toolkit

Этот навык предоставляет пошаговый алгоритм и набор инструментов для переноса киноархива пользователя (оценки от 1 до 10, даты просмотра, список «Буду смотреть») из сервиса Кинопоиск в профиль IMDb.

## 🧭 Ключевой пайплайн миграции

Миграция делится на 4 основных этапа:

```
[Кинопоиск (Консоль F12)]
       │ (extract_movies.js)
       ▼
[Локальный CSV/TXT] ──(convert_to_letterboxd.py)──► [Letterboxd Импорт]
                                                            │
[IMDb Watchlist] ◄──(imdb_watchlist_importer.js)── [IMDb IDs сопоставление]
       │
       ▼ (rebuild_watched.py)
[Markdown-архив watched.md]
```

---

## 🛠️ Справочник скриптов и ролей

### 1. Браузерные скрипты (JavaScript / DevTools Console F12)
* `Scripts/extract_movies.js` — парсит названия, оценки и даты прямо со страницы «Мои оценки» на Кинопоиске (`https://www.kinopoisk.ru/mykp/movies/`).
* `Scripts/imdb_watchlist_importer.js` — двухрежимный импортер (GraphQL + классический POST-fallback) для пакетного добавления фильмов в IMDb Watchlist с защитой от WAF и соблюдением интервалов.

### 2. Скрипты обработки данных (Python 3.10+)
* `Scripts/convert_to_letterboxd.py` — преобразует сырой экспорт Кинопоиска в совместимый CSV-формат Letterboxd.
* `Scripts/extract_from_letterboxd.py` — извлекает IMDb IDs из экспортного дампа Letterboxd.
* `Scripts/prepare_watchlist.py` — автоматический поиск IMDb ID через API для списка «Буду смотреть».
* `Scripts/check_ids.py` — выборочная валидация корректности сопоставления названий и ID.
* `Scripts/fix_order.py` — реверсирование хронологического порядка фильмов перед заливкой.
* `Scripts/make_chunks.py` — нарезка огромных JSON-списков на безопасные чанки для стабильного импорта.
* `Scripts/rebuild_watched.py` — компиляция итоговой базы в красивый Markdown-архив `watched.md`.

---

## 📋 Инструкция для AI-ассистента по ведению пользователя

1. **Диагностика сетевого доступа:**
   * Напомнить пользователю о необходимости стабильного подключения (порт 443 / Stealth VPN) во избежание WAF-блокировок Кинопоиска и IMDb.
2. **Парсинг оценок:**
   * Направить пользователя на `https://www.kinopoisk.ru/mykp/movies/`.
   * Попросить выставить отображение по 200 фильмов и прокрутить до конца.
   * Предоставить код `Scripts/extract_movies.js` для вставки в консоль F12.
3. **Сопоставление идентификаторов (ID Matching):**
   * Рекомендовать связку через Letterboxd (`convert_to_letterboxd.py`), так как это обеспечивает максимальный процент точных совпадений без ручного перебора.
4. **Заливка в IMDb:**
   * Использовать `Scripts/make_chunks.py` (порции по 50–100 фильмов).
   * Запускать `Scripts/imdb_watchlist_importer.js` во вкладке [IMDb Watchlist](https://www.imdb.com/watchlist/).
   * Напоминать: вкладку во время импорта не закрывать и не переключать (предотвращение троттлинга браузером фоновых тасок).
5. **Формирование локального архива:**
   * Сгенерировать финальный `watched.md` с помощью `Scripts/rebuild_watched.py`.
