# Сборка

```
pip install imageio-ffmpeg playwright pillow numpy
python3 cut.py        # обрезка пауз -> voice_cut.wav, phrases_cut.json
python3 build_bg.py   # фоновая дорожка из клипов и фото -> bg.mp4
python3 render.py     # 1461 PNG с альфой (1080x1920) через Chromium, ~10 мин
ffmpeg -y -i bg.mp4 -framerate 30 -i frames/f%05d.png -i voice_cut.wav \
  -filter_complex "[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[v]" \
  -map "[v]" -map 2:a -c:v libx264 -preset slow -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart -shortest iconmade_uniform_v3.mp4
```

* `scene.html` — сцены и тайминги. Классы фона: `navy` (тёмный экран),
  `film` (фул-фрейм видео/фото, текст внизу), `band` (клип полосой, текст под ней),
  `split` (клип сверху, текст в нижней панели). Атрибуты `data-s` (старт сцены),
  `data-a` / `data-a2` (`старт, длительность, пресет`).
* `engine.js` — `window.seek(T)` выставляет состояние всей сцены на момент `T`,
  поэтому рендер покадровый и полностью детерминированный.
* Пресеты: `fade`, `up`, `down`, `left`, `pop`, `wipe`, `img`, `dim`, `rise`.
* `build_bg.py` — раскладка материала по таймлайну, замедление клипов вдвое,
  цветокоррекция, склейка через `xfade`. Длительность перехода задаётся
  отдельно для каждого стыка: по умолчанию 0.40 с, между двумя кадрами
  интерьера — 0.06 с, то есть встык.
* Логотип с прозрачностью лежит в `logo/`, вырезан из джипега по цветовой дистанции.

## Музыка

Трек написан программно (`music.py`) — эмбиент 72 BPM, ля минор,
последовательность Am9 · Fmaj7 · Cmaj7 · Em7 · Am9 · Fmaj7 · Cmaj9 по два такта.
Слои: пад из расстроенных голосов, арпеджио с шимером октавой выше, низкий
пульс на 55 Гц через такт, полоса воздуха 2.5–9 кГц. Реверберация — свёртка
с синтезированным импульсом 2.6 с. Автоматика громкости привязана к сценам:
пад входит к 4-й секунде, пульс — к 6-й, арпеджио — на «правильной униформе»
(13.6 с), плотность подрастает на блоке бренда, к финалу всё разрежается.

Сведение (`mix.sh` + `amix`): музыка приглушена на 5.5 дБ, срез ниже 60 Гц,
провал −3.5 дБ на 280 Гц под голос, +2 дБ на 3.2 кГц; сайдчейн-компрессия по
голосу даёт около 6 дБ дакинга. Итог: музыка на 20.6 дБ ниже речи под голосом
и на ~15 дБ в паузах. Мастер −14 LUFS, тру-пик −1.2 dBFS.

```
python3 music.py && ./mix.sh -5.5
ffmpeg -y -i voice_cut.wav -i music_ducked.wav -filter_complex \
  "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94,\
   loudnorm=I=-14:TP=-1.2:LRA=9[a]" -map "[a]" final_audio.wav
ffmpeg -y -i iconmade_uniform_v4.mp4 -i final_audio.wav \
  -filter_complex "[1:a]apad=whole_dur=48.70[a]" -map 0:v:0 -map "[a]" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart iconmade_uniform_v5.mp4
```

Свой трек подставляется вместо `music.wav` — остальная цепочка не меняется.
