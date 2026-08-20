import json, asyncio, pathlib
from playwright.async_api import async_playwright
meta=json.load(open("slides/meta.json"))
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                                  args=["--no-sandbox","--font-render-hinting=none"])
        pg=await b.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
        for m in meta:
            await pg.goto("file://"+str(pathlib.Path(f"slides/{m['id']}.html").resolve()))
            try: await pg.wait_for_function("document.fonts.ready.then(()=>true)", timeout=15000)
            except Exception: pass
            await pg.wait_for_timeout(500)
            await pg.screenshot(path=f"slides/{m['id']}.png")
            print("shot", m["id"], flush=True)
        await b.close()
asyncio.run(main())
