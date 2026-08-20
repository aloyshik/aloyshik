# Как пересобрать ролик

```
pip install imageio-ffmpeg playwright
python3 slides.py    # HTML-слайды из сценария (тайминги внутри slides.py)
python3 shoot.py     # рендер PNG 1080x1920 через Chromium
python3 build.py     # сборка клипов + склейка со звуком исходника
```

`asr.py` + `bounds.json` — расшифровка звука (sherpa-onnx, модель
`sherpa-onnx-whisper-small`), тайминги слайдов взяты из детекта пауз:

```
ffmpeg -i audio16k.wav -af "silencedetect=noise=-34dB:d=0.16" -f null /dev/null
```

Чтобы подставить реальные кадры — заменить вызовы `slot(...)` в `slides.py`
на `<img src="frames/....jpg">` в тех же блоках.
