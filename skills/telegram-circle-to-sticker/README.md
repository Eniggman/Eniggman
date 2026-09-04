# 🔵 Telegram Circle to Sticker

[![Telegram Sticker Specs](https://img.shields.io/badge/Telegram-Video%20Stickers-2CA5E0?logo=telegram&logoColor=white)](https://core.telegram.org/stickers/webm-vp9-encoding)
[![Codec](https://img.shields.io/badge/Codec-VP9%20yuva420p-orange)](https://www.webmproject.org/vp9/)
[![Format](https://img.shields.io/badge/Format-WebM-green)](https://www.webmproject.org/)
[![Resolution](https://img.shields.io/badge/Resolution-512%C3%97512-blue)](#-официальные-требования-telegram)
[![Size Limit](https://img.shields.io/badge/Size-%E2%89%A4%20256%20KB-red)](#-официальные-требования-telegram)
[![Termux Ready](https://img.shields.io/badge/Termux-Supported-black?logo=android)](https://termux.dev)

Набор инструментов и стандартизированный алгоритм для автоматической конвертации видеосообщений («кружочков») и стандартных видео Telegram в официальный формат **видеостикеров Telegram** (`.webm`, кодек VP9 с прозрачной альфа-маской по кругу, 512×512 px, до 3 секунд, до 256 КБ).

---

## 📋 Содержание

- [Обзор](#-обзор)
- [Официальные требования Telegram](#-официальные-требования-telegram)
- [Системные требования и зависимости](#-системные-требования-и-зависимости)
- [Быстрый старт (Установка)](#-быстрый-старт-установка)
- [Основной рабочий процесс (Рекомендуемый пайплайн)](#-основной-рабочий-процесс-рекомендуемый-пайплайн)
  - [Шаг 1: Анализ исходника](#шаг-1-анализ-исходника)
  - [Шаг 2: Извлечение кадров](#шаг-2-извлечение-кадров)
  - [Шаг 3: Наложение круглой альфа-маски](#шаг-3-наложение-круглой-альфа-маски)
  - [Шаг 4: Кодирование в VP9 WebM](#шаг-4-кодирование-в-vp9-webm)
  - [Шаг 5: Валидация и проверка альфа-канала](#шаг-5-валидация-и-проверка-альфа-канала)
- [Альтернатива: One-liner через FFmpeg](#-альтернатива-one-liner-через-ffmpeg)
- [Управление битрейтом и размером (≤ 256 КБ)](#-управление-битрейтом-и-размером--256-кб)
- [Неофициальный Spoofing длинных видео (`tgradish`)](#-неофициальный-spoofing-длинных-видео-tgradish)
- [Устранение неполадок (FAQ)](#-устранение-неполадок-faq)
- [Благодарности и атрибуция (Credits)](#-благодарности-и-атрибуция-credits)

---

## 🎯 Обзор

Круглые видеосообщения Telegram сохраняются в формате MP4/MPEG-4 AVC с квадратным соотношением сторон 1:1, но углы в них не прозрачны — они маскируются локально на стороне мобильного клиента. 

При попытке загрузить исходное видео в бота `@Stickers` файл будет отклонён:
1. Видеостикеры Telegram **обязаны** использовать контейнер **WebM** и кодек **VP9**.
2. Углы холста 512×512 **обязаны быть прозрачными** (альфа-канал `yuva420p`), иначе вокруг кружочка останется чёрная или цветная рамка.
3. Аудиодорожка **должна отсутствовать**.
4. Длительность — **не более 3.0 секунд**, размер — **не более 256 КБ**.

Данный скилл автоматизирует весь цикл подготовки: вырезку фрагмента, кадрирование, генерацию идеальной эллиптической альфа-маски, сжатие с сохранением прозрачности и проверку соответствия правилам Telegram.

---

## 📐 Официальные требования Telegram

Спецификация основана на [руководстве Telegram по кодированию WebM VP9](https://core.telegram.org/stickers/webm-vp9-encoding):

| Параметр | Требование Telegram | Решение в пайплайне |
| :--- | :--- | :--- |
| **Формат / Контейнер** | WebM (`.webm`) | `-f webm` |
| **Видеокодек** | VP9 (`libvpx-vp9`) | `-c:v libvpx-vp9` |
| **Разрешение** | 512×512 px (одна сторона строго 512 px, вторая ≤ 512 px) | `scale=512:512` |
| **Частота кадров** | До 30 FPS | `-framerate 30` / `fps=30` |
| **Длительность** | До 3.0 секунд | `-t 3` или выбор отрезка `-ss / -to` |
| **Размер файла** | **≤ 256 КБ** (строго ≤ 262 144 байт, целевой порог ≤ 256 000 байт) | `-b:v 200k -crf 48` |
| **Аудиодорожка** | **Запрещена** | `-an` (удаление аудио) |
| **Альфа-канал** | Поддерживается (8-bit alpha) | `-pix_fmt yuva420p -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1` |
| **Зацикливание** | Зацикленное воспроизведение | Бесшовное воспроизведение 3 секунд |

> [!IMPORTANT]
> **Критичный флаг: `-auto-alt-ref 0`**  
> По умолчанию энкодер `libvpx-vp9` включает механизм Alternate Reference Frames (`alt-ref`), который усредняет кадры во времени и **безвозвратно разрушает альфа-канал** в WebM. Отключение этой опции (`-auto-alt-ref 0`) строго обязательно для сохранения прозрачных углов!

---

## 🧰 Системные требования и зависимости

Скилл работает на любой Linux/Unix-системе, в macOS, Windows (WSL / Git Bash) и на Android через **Termux**.

- **FFmpeg** с включённым энкодером `libvpx-vp9`
- **Python 3**
- **Pillow (PIL)** — библиотека обработки изображений
- *(Опционально)* **tgradish** — для экспериментального spoofing метаданных

---

## 🚀 Быстрый старт (Установка)

### Установка в Termux (Android)

```bash
pkg update
pkg install ffmpeg python
pip install pillow
```

*(Опционально, для длинных видео)*:
```bash
pip install tgradish
```

### Установка в Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg python3 python3-pip python3-pil
```

---

## 🔄 Основной рабочий процесс (Рекомендуемый пайплайн)

Рекомендуемый двухэтапный пайплайн через `scripts/make_circle_frames.py` гарантирует 100% математически точный круг с идеально прозрачными углами без потерь антиалиасинга.

```
[ Исходное видео / кружок ]
            │
            ▼ (FFmpeg: обрезка до 3 сек, 30 fps, 512x512 PNG)
[ Временные кадры (RGB PNG) ]
            │
            ▼ (Python + Pillow: наложение эллипса 0,0..511,511)
[ RGBA кадры с альфа-каналом ]
            │
            ▼ (FFmpeg: libvpx-vp9, yuva420p, -auto-alt-ref 0)
[ Итоговый sticker.webm (≤256 КБ, 512x512) ]
            │
            ▼ (ffprobe + libvpx проверка пикселя 0,0)
[ Готов к загрузке в @Stickers ]
```

### Шаг 1: Анализ исходника

Проверьте разрешение и длительность видео:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,duration,r_frame_rate \
  -of default=noprint_wrappers=1:nokey=1 input.mp4
```

### Шаг 2: Извлечение кадров

Извлекаем до 3 секунд с частотой 30 кадров/сек, центрируя и масштабируя до 512×512:

```bash
mkdir -p input_frames rgba_frames

# Если нужен фрагмент с 1.5 по 4.5 секунду: -ss 1.5 -t 3
ffmpeg -y -i input.mp4 -t 3 \
  -vf "fps=30,scale=512:512:force_original_aspect_ratio=increase,crop=512:512" \
  input_frames/%04d.png
```

### Шаг 3: Наложение круглой альфа-маски

Используем встроенный скрипт `scripts/make_circle_frames.py`. Скрипт создаёт альфа-маску размером с кадр, вырезает круг от пикселя `(0, 0)` до `(w-1, h-1)` и сохраняет кадры в 32-битный RGBA:

```bash
python3 scripts/make_circle_frames.py input_frames rgba_frames
```

### Шаг 4: Кодирование в VP9 WebM

Сборка RGBA-кадров энкодером `libvpx-vp9`:

```bash
ffmpeg -y -framerate 30 -i 'rgba_frames/%04d.png' -an \
  -vf 'format=yuva420p' -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 200k -crf 48 -deadline good -cpu-used 2 -row-mt 1 \
  -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1 \
  sticker.webm
```

**Разбор аргументов кодирования:**
- `-an`: Полностью отключает звук.
- `-vf 'format=yuva420p' -pix_fmt yuva420p`: Задаёт цветовое пространство YUV420 с 8-битным каналом прозрачности.
- `-auto-alt-ref 0`: Запрещает альтернативные опорные кадры, сохраняя альфа-прозрачность.
- `-metadata:s:v:0 alpha_mode=1`: Прописывает флаг наличия альфа-канала в WebM-контейнере для плеера Telegram.
- `-b:v 200k -crf 48`: Ограничение битрейта и фактор качества для строгого соответствия лимиту в 256 КБ.
- `-row-mt 1`: Включает многопоточность по строкам (ускоряет сжатие на мобильных ARM/многоядерных CPU).

### Шаг 5: Валидация и проверка альфа-канала

1. **Проверка размера файла:**
```bash
# Размер не должен превышать 256000 байт (лимит Telegram 262144 байт):
ls -la sticker.webm
```

2. **Проверка длительности и отсутствия аудио:**
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 sticker.webm
ffprobe -v error -select_streams a -show_entries stream=codec_type -of default=noprint_wrappers=1:nokey=1 sticker.webm
# Вывод аудио должен быть пустым
```

3. **Проверка прозрачности углов:**
Обычный `ffprobe` может показывать `yuv420p` даже при наличии альфа-канала. Декодируйте первый кадр строго через `libvpx-vp9`:
```bash
ffmpeg -c:v libvpx-vp9 -i sticker.webm -frames:v 1 -pix_fmt rgba check.png
```
Пиксель в углу `(0, 0)` должен быть полностью прозрачным (Alpha = 0), а пиксель в центре `(256, 256)` — непрозрачным (Alpha = 255).

4. **Очистка временных файлов:**
```bash
rm -rf input_frames rgba_frames check.png
```

---

## ⚡ Альтернатива: One-liner через FFmpeg

Если на устройстве мало места или нежелательно сохранять сотни промежуточных PNG на диск, маску круга можно наложить на лету с помощью фильтра `geq`:

```bash
ffmpeg -y -i input.mp4 -t 3 -an \
  -vf "fps=30,scale=512:512:force_original_aspect_ratio=increase,crop=512:512,\
format=yuva420p,\
geq=lum='p(X,Y)':a='if(lte(pow(X-255.5,2)+pow(Y-255.5,2),pow(255.5,2)),255,0)'" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 200k -crf 48 \
  -deadline good -cpu-used 2 -row-mt 1 -auto-alt-ref 0 \
  -metadata:s:v:0 alpha_mode=1 sticker_direct.webm
```

> [!TIP]
> Метод со скриптом `make_circle_frames.py` работает быстрее на процессорах смартфонов в Termux, поскольку фильтр `geq` в софтверном FFmpeg производит вычисление формулы для каждого пикселя отдельно.

---

## 🎛️ Управление битрейтом и размером (≤ 256 КБ)

Telegram отклоняет любые стикеры размером больше **262 144 байт**. Рекомендуется держать размер в пределах **240–252 КБ** (запас 4–12 КБ на накладные расходы контейнера).

Максимально допустимый средний битрейт для 3 секунд:
$$\text{Bitrate}_{\max} \approx \frac{250 \times 1024 \times 8 \text{ бит}}{3 \text{ сек}} \approx 682 \text{ kbps}$$

Если видео очень динамичное (много шума, движения или мелких деталей) и превышает 256 КБ, примените двухпроходное кодирование (2-pass):

```bash
# Проход 1:
ffmpeg -y -framerate 30 -i 'rgba_frames/%04d.png' -an \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 180k -crf 50 \
  -auto-alt-ref 0 -pass 1 -f null /dev/null

# Проход 2:
ffmpeg -y -framerate 30 -i 'rgba_frames/%04d.png' -an \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 180k -crf 50 \
  -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1 -pass 2 \
  sticker.webm
```

---

## 🕵️ Неофициальный Spoofing длинных видео (`tgradish`)

В официальном боте `@Stickers` действует жёсткий серверный лимит длительности 3 секунды.  
Для личных экспериментов и обхода ограничения длительности используется метод спуфинга метаданных WebM из проекта [sliva0/tgradish](https://github.com/sliva0/tgradish). Утилита `tgradish` подменяет заголовок длительности (`Segment/Info/Duration`) в метаданных WebM-контейнера, заставляя клиент считать видео 3-секундным:

```bash
# Кодирование видео любой длины:
ffmpeg -y -i long_circle.mp4 -an \
  -vf "fps=30,scale=512:512:force_original_aspect_ratio=increase,crop=512:512,format=yuva420p" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 150k -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1 \
  temp_long.webm

# Подмена метаданных (метод tgradish):
python3 -m tgradish spoof temp_long.webm sticker_spoof.webm
```

> [!WARNING]
> Spoofing **НЕ** снимает серверные ограничения Telegram. Бот `@Stickers` может отклонить файл, либо видео будет зависать/не проигрываться на официальных мобильных клиентах Android и iOS. Используйте только если полностью осознаете ограничения.

---

## ❓ Устранение неполадок (FAQ)

### 1. Углы стикера чёрные/белые вместо прозрачных
- **Причина:** Не указан флаг `-auto-alt-ref 0` или неверно передан формат `yuva420p`.
- **Решение:** Убедитесь, что переданы параметры `-vf 'format=yuva420p' -pix_fmt yuva420p -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1`. Не проверяйте прозрачность через стандартный просмотрщик изображений Windows — декодируйте кадр через `ffmpeg -c:v libvpx-vp9 ...`.

### 2. Бот `@Stickers` пишет «File size must not exceed 256 KB»
- **Причина:** Размер файла превысил 262 144 байт.
- **Решение:** Увеличьте `-crf` (например, с 48 до 52) или уменьшите битрейт `-b:v 180k`.

### 3. Бот пишет «Video sticker duration must not exceed 3 seconds»
- **Причина:** Длительность составила 3.01–3.05 сек из-за несовпадения таймстемпов кадров.
- **Решение:** Задайте строго `-t 3` и зафиксируйте частоту кадров `-framerate 30` (ровно 90 кадров для 3 секунд).

### 4. В Termux процесс FFmpeg завершается с ошибкой `Killed` (OOM)
- **Причина:** Нехватка оперативной памяти при одновременной обработке большого количества кадров.
- **Решение:** Добавьте аргумент `-cpu-used 4` (меньше нагрузка на процессор и память), закройте фоновые приложения.

---

## 🙏 Благодарности и атрибуция (Credits)

- **[sliva0/tgradish](https://github.com/sliva0/tgradish)** — благодарность автору [sliva0](https://github.com/sliva0) за оригинальную идею и реализацию метода спуфинга метаданных WebM (`Duration` spoofing), позволяющего увеличивать длительность видеостикеров Telegram в неофициальных сценариях.
- **[FFmpeg Project](https://ffmpeg.org/)** — универсальный мультимедийный фреймворк и кодек `libvpx-vp9`.
- **[Telegram WebM VP9 Guide](https://core.telegram.org/stickers/webm-vp9-encoding)** — официальная спецификация формата видеостикеров Telegram.
