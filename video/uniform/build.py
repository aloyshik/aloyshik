import json, subprocess, os
meta=json.load(open("slides/meta.json"))
FPS=30
os.makedirs("clips", exist_ok=True)
lines=[]
for i,m in enumerate(meta):
    dur=m["dur"]; n=max(2,int(round(dur*FPS)))
    zdir = 1 if i%2==0 else -1
    if zdir>0:
        z="min(1.001+0.00030*on,1.06)"
    else:
        z="max(1.06-0.00030*on,1.001)"
    vf=(f"scale=1296:2304:flags=lanczos,"
        f"zoompan=z='{z}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},"
        f"fade=t=in:st=0:d=0.30")
    if i==len(meta)-1:
        vf+=f",fade=t=out:st={max(0,dur-0.6):.2f}:d=0.6"
    out=f"clips/{m['id']}.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-loop","1","-i",f"slides/{m['id']}.png",
        "-frames:v",str(n),"-vf",vf,"-r",str(FPS),"-c:v","libx264","-preset","medium","-crf","17",
        "-pix_fmt","yuv420p",out],check=True)
    lines.append(f"file '{out}'")
open("concat.txt","w").write("\n".join(lines))
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i","concat.txt",
    "-i","/root/.claude/uploads/b6400e14-7267-55b4-8656-20982b523aea/b561a6e1-copy_6D3FDD148AFE4D099E25D50EB8F8E186.mov",
    "-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",
    "-movflags","+faststart","wikenmade_uniform_draft.mp4"],check=True)
print("built")
