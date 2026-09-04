# 🔵 Telegram Circle to Sticker

[![Telegram Sticker Specs](https://img.shields.io/badge/Telegram-Video%20Stickers-2CA5E0?logo=telegram&logoColor=white)](https://core.telegram.org/stickers/webm-vp9-encoding)
[![Codec](https://img.shields.io/badge/Codec-VP9%20yuva420p-orange)](https://www.webmproject.org/vp9/)
[![Format](https://img.shields.io/badge/Format-WebM-green)](https://www.webmproject.org/)
[![Resolution](https://img.shields.io/badge/Resolution-512%C3%97512-blue)](#-требования-telegram)
[![Size Limit](https://img.shields.io/badge/Size-%E2%89%A4%20256%20KB-red)](#-требования-telegram)

Инструмент и пайплайн для конвертации видеосообщений («кружочков») и квадратных видео Telegram в формат **видеостикеров** (`.webm`, VP9 с альфа-каналом, 512×512, до 3 секунд, до 256 КБ).

---

## 🎯 Зачем нужна маска?

Исходные кружочки Telegram сохраняются как квадратные MP4-видео, а круглую форму им придает сам клиент Telegram при отображении.

Если отправить такое видео в `@Stickers` без альфа-канала (или просто перекодировать в WebM без маски), **бот примет файл, но вокруг кружка останутся уродливые белые (или чёрные) углы и полосы** вместо аккуратного круглого стикера. Пайплайн накладывает правильную круглую альфа-маску, делая углы полностью прозрачными.

---

## 📐 Требования Telegram

- **Контейнер и кодек:** WebM (`.webm`), кодек VP9 (`libvpx-vp9`).
- **Разрешение:** 512×512 px (одна сторона строго 512 px, вторая ≤ 512 px).
- **Частота кадров:** до 30 FPS.
- **Длительность:** строго до 3.0 секунд.
- **Размер файла:** ≤ 256 КБ (строго ≤ 262 144 байт).
- **Аудио:** без аудиодорожки.
- **Прозрачность:** альфа-канал `yuva420p` с выключенным alt-ref (`-auto-alt-ref 0`).

---

## 🧰 Зависимости

Убедитесь, что установлены **FFmpeg** (с поддержкой `libvpx-vp9`), **Python 3** и библиотека **Pillow**:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y ffmpeg python3 python3-pip python3-pil

# Либо через pip
pip install pillow
```

---

## 🚀 Быстрый пайплайн (Рекомендуемый способ)

Двухэтапный метод через скрипт `scripts/make_circle_frames.py` даёт идеальное сглаживание краёв круга без артефактов.

### Шаг 1. Нарезка кадров (FFmpeg)
Обрезаем до 3 секунд, масштабируем до 512×512 и извлекаем PNG-кадры (30 fps):
```bash
mkdir -p input_frames rgba_frames
ffmpeg -y -i input.mp4 -t 3 \
  -vf "fps=30,scale=512:512:force_original_aspect_ratio=increase,crop=512:512" \
  input_frames/%04d.png
```

### Шаг 2. Наложение круглой маски (Python)
Генерируем прозрачный альфа-канал по кругу для каждого кадра:
```bash
python3 scripts/make_circle_frames.py input_frames rgba_frames
```

### Шаг 3. Кодирование в VP9 WebM (FFmpeg)
Собираем кадры в готовый стикер с флагом прозрачности:
```bash
ffmpeg -y -framerate 30 -i 'rgba_frames/%04d.png' -an \
  -vf 'format=yuva420p' -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 200k -crf 48 -deadline good -cpu-used 2 -row-mt 1 \
  -auto-alt-ref 0 -metadata:s:v:0 alpha_mode=1 \
  sticker.webm
```

*После кодирования временные папки можно удалить:* `rm -rf input_frames rgba_frames`

> [!IMPORTANT]
> Параметр `-auto-alt-ref 0` критичен: без него кодек VP9 размывает и разрушает прозрачность углов.

---

## ⚡ Альтернатива: One-liner через FFmpeg

Если нужно быстро сделать стикер без промежуточных файлов PNG, можно наложить маску формулой `geq`:

```bash
ffmpeg -y -i input.mp4 -t 3 -an \
  -vf "fps=30,scale=512:512:force_original_aspect_ratio=increase,crop=512:512,\
format=yuva420p,\
geq=lum='p(X,Y)':a='if(lte(pow(X-255.5,2)+pow(Y-255.5,2),pow(255.5,2)),255,0)'" \
  -c:v libvpx-vp9 -pix_fmt yuva420p -b:v 200k -crf 48 \
  -deadline good -cpu-used 2 -row-mt 1 -auto-alt-ref 0 \
  -metadata:s:v:0 alpha_mode=1 sticker.webm
```

---

## ⏱️ Увеличение длительности (Spoofing) и Credits

Официальный бот `@Stickers` строго ограничивает видео 3 секундами. Для обхода этого лимита существует техника подмены поля `Duration` в метаданных WebM-контейнера:

```bash
pip install tgradish
python3 -m tgradish spoof input_long.webm sticker_spoof.webm
```

*Примечание: неофициальный метод, используйте осторожно.*

**Благодарности:**
- Проекту **[sliva0/tgradish](https://github.com/sliva0/tgradish)** (автор [sliva0](https://github.com/sliva0)) за метод подмены длительности WebM.
- **[FFmpeg Project](https://ffmpeg.org/)** за мультимедийный инструментарий.
