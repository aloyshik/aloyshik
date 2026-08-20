import sherpa_onnx, wave, numpy as np, subprocess, json, sys

M="sherpa-onnx-whisper-small"
rec = sherpa_onnx.OfflineRecognizer.from_whisper(
    encoder=f"{M}/small-encoder.int8.onnx",
    decoder=f"{M}/small-decoder.int8.onnx",
    tokens=f"{M}/small-tokens.txt",
    language="ru", task="transcribe", num_threads=4,
)
bounds = json.load(open("bounds.json"))
out=[]
for (a,b) in bounds:
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-ss",str(a),"-to",str(b),
                    "-i","audio16k.wav","-ac","1","-ar","16000","chunk.wav","-y"],check=True)
    w=wave.open("chunk.wav"); n=w.getnframes()
    s=np.frombuffer(w.readframes(n),dtype=np.int16).astype(np.float32)/32768.0
    st=rec.create_stream(); st.accept_waveform(16000, s); rec.decode_stream(st)
    txt=st.result.text.strip()
    line=f"[{a:6.2f} - {b:6.2f}] {txt}"
    print(line, flush=True); out.append({"start":a,"end":b,"text":txt})
json.dump(out, open("transcript.json","w"), ensure_ascii=False, indent=1)
