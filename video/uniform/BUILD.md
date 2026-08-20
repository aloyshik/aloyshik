# Сборка

```
pip install imageio-ffmpeg playwright
python3 cut.py       # обрезка пауз + пересчёт таймингов -> voice_cut.wav, phrases_cut.json
python3 render.py    # 1461 кадр 1080x1920 через Chromium (~2 мин)
ffmpeg -y -framerate 30 -i frames/f%05d.jpg -i voice_cut.wav \
  -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart -shortest iconmade_uniform_v2.mp4
```

* `scene.html` — все сцены и тайминги (атрибуты `data-s`, `data-a`, `data-a2`).
* `engine.js` — детерминированный движок анимации: `window.seek(T)` выставляет
  состояние всей сцены на момент `T`, поэтому рендер покадровый и стабильный.
* Пресеты анимаций: `fade`, `up`, `down`, `left`, `pop`, `wipe`, `img`, `dim`, `rise`.
* Подставить кадры — заменить блоки `<div class="slot">` на `<img src="frames/...">`
  с тем же `data-a="t,0.9,img"`.
