import asyncio, pathlib, os, time
from playwright.async_api import async_playwright
FPS=30; DUR=48.70; N=int(round(DUR*FPS))
os.makedirs("frames", exist_ok=True)
async def main():
    t0=time.time()
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox","--force-color-profile=srgb","--font-render-hinting=none",
                  "--disable-gpu","--hide-scrollbars"])
        pg=await b.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
        await pg.goto("file://"+str(pathlib.Path("scene.html").resolve()))
        await pg.wait_for_timeout(1200)
        for i in range(N):
            await pg.evaluate("t=>window.seek(t)", i/FPS)
            await pg.screenshot(path=f"frames/f{i:05d}.png", omit_background=True)
            if i%150==0: print(f"{i}/{N}  {time.time()-t0:.0f}s", flush=True)
        await b.close()
    print(f"done {N} frames in {time.time()-t0:.0f}s")
asyncio.run(main())
