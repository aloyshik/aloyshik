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
  цветокоррекция, склейка через `xfade`.
* Логотип с прозрачностью лежит в `logo/`, вырезан из джипега по цветовой дистанции.
