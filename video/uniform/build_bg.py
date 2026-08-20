import subprocess, os, json
U="/root/.claude/uploads/b6400e14-7267-55b4-8656-20982b523aea"
NAVY="0x1E2A3D"; FPS=30; T=0.40
os.makedirs("bg", exist_ok=True)
CLIP1=f"{U}/5233a079-IMG_4125.mov"   # landscape 1920x1080
CLIP2=f"{U}/a006486e-IMG_4130.mov"   # portrait
CLIP3=f"{U}/78a03afc-IMG_4109.mov"   # portrait
PH_BAD=f"{U}/1d27a6cb-4A5A159A721B4882BC5F5FAA31ADCF9D.png"   # официантка
PH_LOGO=f"{U}/6f0ad446-1E193314BCDB40E79931458AC69F4713.png"  # фартук BISTRO

def run(a): subprocess.run(a, check=True)

def navy(dur, out):
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi",
         "-i",f"color=c={NAVY}:s=1080x1920:r={FPS}","-t",f"{dur:.3f}",
         "-c:v","libx264","-preset","veryfast","-crf","16","-pix_fmt","yuv420p",out])

def still(src, dur, out, zoom_from=1.0, zoom_to=1.10):
    n=int(round(dur*FPS))
    step=(zoom_to-zoom_from)/max(1,n-1)
    vf=(f"scale=2160:-1:flags=lanczos,"
        f"zoompan=z='{zoom_from}+{step:.7f}*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        f":s=1080x1920:fps={FPS},"
        f"eq=brightness=-0.045:contrast=1.05:saturation=0.42,"
        f"colorbalance=rs=-0.05:bs=0.11:rm=-0.04:bm=0.07:rh=-0.02:bh=0.04")
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",src,
         "-frames:v",str(n),"-vf",vf,"-r",str(FPS),
         "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out])

GRADE="eq=saturation=0.90:contrast=1.04:brightness=-0.02,colorbalance=bs=0.05:bm=0.03"

def clip_top(src, ss, dur, out, h=1180):
    """портретный клип сверху, тёмная панель снизу"""
    src_dur=dur/2.0
    vf=(f"setpts=2.0*PTS,fps={FPS},scale=1080:-2:flags=lanczos,crop=1080:{h}:0:'(ih-{h})/3',{GRADE}")
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(ss),"-t",f"{src_dur:.3f}","-i",src,
         "-f","lavfi","-i",f"color=c={NAVY}:s=1080x1920:r={FPS}",
         "-filter_complex",f"[0:v]{vf}[v];[1:v][v]overlay=0:0:shortest=1[o]",
         "-map","[o]","-t",f"{dur:.3f}","-r",str(FPS),
         "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out])

def clip_band(src, ss, dur, out, y=300):
    """горизонтальный клип полосой по центру"""
    src_dur=dur/2.0
    vf=(f"setpts=2.0*PTS,fps={FPS},scale=1080:-2:flags=lanczos,{GRADE}")
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",str(ss),"-t",f"{src_dur:.3f}","-i",src,
         "-f","lavfi","-i",f"color=c={NAVY}:s=1080x1920:r={FPS}",
         "-filter_complex",f"[0:v]{vf}[v];[1:v][v]overlay=0:{y}:shortest=1[o]",
         "-map","[o]","-t",f"{dur:.3f}","-r",str(FPS),
         "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p",out])

SEG=[("navy",  0.00, 4.61,  None),
     ("still", 4.61, 7.70,  PH_LOGO),
     ("still", 7.70, 11.93, PH_BAD),
     ("band",  11.93,14.96, (CLIP1,0.15)),
     ("top",   14.96,18.55, (CLIP2,0.20)),
     ("navy",  18.55,30.40, None),
     ("top",   30.40,33.46, (CLIP3,0.60)),
     ("navy",  33.46,36.93, None),
     ("band",  36.93,41.16, (CLIP1,2.00)),
     ("navy",  41.16,48.70, None)]

files=[]; D=[]
for i,(kind,a,b,src) in enumerate(SEG):
    d=b-a; last=(i==len(SEG)-1)
    L=d+T
    out=f"bg/s{i:02d}.mp4"
    if kind=="navy":  navy(L, out)
    elif kind=="still": still(src, L, out)
    elif kind=="top":  clip_top(src[0], src[1], L, out)
    elif kind=="band": clip_band(src[0], src[1], L, out)
    files.append(out); D.append(d)
    print(f"seg{i:02d} {kind:5s} {a:6.2f}-{b:6.2f}  len={L:.2f}", flush=True)

# xfade chain
inp=[]; 
for f in files: inp += ["-i", f]
fc=[]; cur="[0:v]"; acc=0.0
for i in range(1,len(files)):
    acc += D[i-1]
    lbl=f"[x{i}]"
    fc.append(f"{cur}[{i}:v]xfade=transition=fade:duration={T}:offset={acc-T:.3f}{lbl}")
    cur=lbl
fc_str=";".join(fc)
run(["ffmpeg","-hide_banner","-loglevel","error","-y"]+inp+
    ["-filter_complex",fc_str,"-map",cur,"-r",str(FPS),
     "-c:v","libx264","-preset","medium","-crf","17","-pix_fmt","yuv420p","bg.mp4"])
print("bg.mp4 built, target", sum(D))
