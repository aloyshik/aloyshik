"""Композит кадра + разметка безопасной зоны Instagram Reels."""
import subprocess, sys
from PIL import Image, ImageDraw
TOP, BOT = 260, 1460
outs=[]
for t in sys.argv[1:]:
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss",t,"-i","bg.mp4",
        "-i",f"ov_{float(t):.2f}.png","-filter_complex","[0][1]overlay","-frames:v","1",f"sf_{t}.png"],check=True)
    im=Image.open(f"sf_{t}.png").convert("RGB"); d=ImageDraw.Draw(im,"RGBA")
    d.rectangle([0,0,1080,TOP], fill=(220,60,60,90))
    d.rectangle([0,BOT,1080,1920], fill=(220,60,60,90))
    d.line([0,TOP,1080,TOP], fill=(255,90,90), width=4)
    d.line([0,BOT,1080,BOT], fill=(255,90,90), width=4)
    im=im.resize((250,444)); im.save(f"sf_{t}.jpg"); outs.append(f"sf_{t}.jpg")
args=[]
for o in outs: args+=["-i",o]
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y"]+args+
    ["-filter_complex",f"hstack={len(outs)}","safe.jpg"],check=True)
print("safe.jpg")
