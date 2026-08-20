# -*- coding: utf-8 -*-
"""Выбор лучшего окна 1.5 с: резкость кадра и плавность движения."""
import subprocess, numpy as np, sys
from PIL import Image
import io, os, glob, shutil

def frames(src, fps=10, h=270):
    d="_pk"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",src,
        "-vf",f"fps={fps},scale=-1:{h}",f"{d}/%04d.png"],check=True)
    out=[]
    for p in sorted(glob.glob(f"{d}/*.png")):
        out.append(np.asarray(Image.open(p).convert("L"),dtype=np.float32))
    return out, fps

def sharp(g):
    lap = (-4*g + np.roll(g,1,0)+np.roll(g,-1,0)+np.roll(g,1,1)+np.roll(g,-1,1))[2:-2,2:-2]
    return float(lap.var())

def analyse(src, win=1.5, fps=10):
    fr,fps = frames(src,fps)
    n=len(fr)
    sh=np.array([sharp(f) for f in fr])
    mo=np.array([0.0]+[float(np.abs(fr[i]-fr[i-1]).mean()) for i in range(1,n)])
    w=int(win*fps)
    print(f"\n{os.path.basename(src)}  {n/fps:.2f}s, кадров {n}")
    best=None
    for s in range(0, n-w+1):
        S=sh[s:s+w]; M=mo[s:s+w]
        # резкость выше — лучше; рывки (разброс движения) — хуже; полная статика — тоже не надо
        score = S.mean()/1000.0 - 2.2*M.std() + 0.5*min(M.mean(),3.0)
        if best is None or score>best[0]: best=(score,s)
        print(f"  {s/fps:5.2f}-{(s+w)/fps:5.2f}s  резк {S.mean():8.0f}  движ {M.mean():5.2f}  рывки {M.std():5.2f}  -> {score:7.2f}")
    print(f"  ЛУЧШЕЕ: {best[1]/fps:.2f}s")
    shutil.rmtree("_pk", ignore_errors=True)
    return best[1]/fps

U="/root/.claude/uploads/b6400e14-7267-55b4-8656-20982b523aea"
a=analyse(f"{U}/d81d347d-IMG_2114.mov")
b=analyse(f"{U}/73f86b86-1378091691894285115.mp4")
print(f"\nИТОГ: A ss={a:.2f}  B ss={b:.2f}")
