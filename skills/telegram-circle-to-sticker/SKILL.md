---
name: telegram-circle-to-sticker
description: "Преобразование круглых видео Telegram (видеосообщений / кружочков) в видеостикеры Telegram (WebM VP9, 512x512, <=3 сек, <=256 КБ, прозрачная маска)."
---

# Telegram Circle to Sticker

## Официальные требования

Создавать `.webm` с VP9, без аудио, размером 512×512 (или с одной стороной 512 px), до 30 FPS, длительностью не более 3 секунд и размером не более 256 КБ. Официальный источник: `https://core.telegram.org/stickers/webm-vp9-encoding`.

## Рабочий процесс

1. Проверить исходник через `ffprobe`.
2. Сохранить квадратный canvas 512×512 и 30 FPS.
3. Создать RGBA PNG-последовательность и наложить эллиптическую маску от `(0,0)` до `(511,511)`, чтобы углы стали прозрачными. Не заливать углы белым или цветом, если нужен прозрачный фон.
4. Кодировать PNG-последовательность в VP9 WebM с `-pix_fmt yuva420p`, `-auto-alt-ref 0` и `-metadata:s:v:0 alpha_mode=1`. Удалить аудио через `-an`.
5. Для официального стикера ограничить длительность 3 секундами. Подбирать `-b:v` и `-crf`, чтобы итоговый размер был не выше 256000 байт; оставлять запас 3–6 КБ.
6. Если пользователь явно просит полный ролик, предупредить о неофициальности и можно применить метод подмены метаданных длительности из проекта [tgradish](https://github.com/sliva0/tgradish) (`python3 -m tgradish spoof`). Это spoofing метаданных контейнера WebM, а не снятие лимита: Telegram может отклонить файл или проиграть его некорректно.
7. Проверить VP9, размер, FPS, длительность и отсутствие аудио. Обычный `ffprobe` может показывать `yuv420p`, даже когда альфа присутствует. Проверять альфа-канал через libvpx:

```bash
ffmpeg -c:v libvpx-vp9 -i sticker.webm -frames:v 1 -pix_fmt rgba check.png
```

У пикселя `(0,0)` должен быть alpha 0, а у центра — alpha 255. Стандартное декодирование без `-c:v libvpx-vp9` может ошибочно показать непрозрачные углы.

## Кодирование

```bash
ffmpeg -y -framerate 30 -i 'rgba/%04d.png' -an \
  -vf 'format=yuva420p' -c:v libvpx-vp9 -pix_fmt yuva420p \
  -b:v 200k -crf 48 -deadline good -row-mt 1 -auto-alt-ref 0 \
  -metadata:s:v:0 alpha_mode=1 output.webm
```

### Неофициальное увеличение длительности (tgradish spoofing)

Для обхода лимита длительности в неофициальных сценариях используется метод спуфинга метаданных контейнера WebM из репозитория [sliva0/tgradish](https://github.com/sliva0/tgradish) (автор: sliva0; благодарность за метод подмены метаданных длительности):

```bash
python3 -m tgradish spoof input.webm output_spoof.webm
```

Не обещать работоспособность spoof-файла на всех клиентах Telegram (бот `@Stickers` или мобильные клиенты могут отклонить файл).

## Ресурс

Использовать `scripts/make_circle_frames.py` для создания RGBA-кадров:

```bash
python3 scripts/make_circle_frames.py input_frames rgba_frames
```
