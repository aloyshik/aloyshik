# -*- coding: utf-8 -*-
import json, os

W,H = 1080,1920

CSS = open("fonts/manrope.css").read() + """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden}
body{
  background:#12100E;
  font-family:'Manrope','DejaVu Sans',sans-serif;
  color:#F2EDE6;
  -webkit-font-smoothing:antialiased;
}
.stage{position:absolute;inset:0;padding:130px 92px;display:flex;flex-direction:column;justify-content:center}
.grain{position:absolute;inset:0;opacity:.55;pointer-events:none;
  background:radial-gradient(120% 80% at 50% 0%, rgba(198,164,110,.16), transparent 60%),
             radial-gradient(90% 60% at 50% 100%, rgba(198,164,110,.07), transparent 60%);}
.kicker{font-size:30px;font-weight:700;letter-spacing:.28em;text-transform:uppercase;color:#C6A46E}
.rule{width:96px;height:3px;background:#C6A46E;margin:34px 0 0}
h1{font-size:70px;line-height:1.1;font-weight:800;letter-spacing:-.02em}
h2{font-size:64px;line-height:1.18;font-weight:800;letter-spacing:-.015em}
.lead{font-size:46px;line-height:1.34;font-weight:300;color:#CFC6BA}
.accent{color:#C6A46E}
.dim{color:#7C7268}
.mt{margin-top:44px}.mt2{margin-top:72px}.mt3{margin-top:110px}
.spacer{flex:1}
.slot{border:3px dashed #4A423A;border-radius:28px;display:flex;align-items:center;
  justify-content:center;flex-direction:column;gap:18px;color:#6E655B;
  background:repeating-linear-gradient(135deg,#191612 0 26px,#15120F 26px 52px)}
.slot .lab{font-size:30px;font-weight:700;letter-spacing:.2em;text-transform:uppercase}
.slot .sub{font-size:28px;font-weight:300;max-width:70%;text-align:center;line-height:1.35}
.row{display:flex;align-items:flex-start;gap:34px}
.mark{font-size:52px;line-height:1;width:76px;height:76px;border-radius:50%;
  display:flex;align-items:center;justify-content:center;flex:0 0 auto;font-weight:700}
.bad{background:rgba(190,90,70,.16);color:#D97B62;border:2px solid rgba(217,123,98,.45)}
.good{background:rgba(198,164,110,.14);color:#C6A46E;border:2px solid rgba(198,164,110,.5)}
.rowtxt{font-size:50px;line-height:1.24;font-weight:500;padding-top:8px}
.rowsub{font-size:32px;font-weight:300;color:#8C8377;margin-top:12px;line-height:1.3}
.chips{display:flex;flex-wrap:wrap;gap:22px}
.chip{border:2px solid #3A342D;border-radius:999px;padding:20px 38px;font-size:38px;font-weight:500}
.chip.on{border-color:#C6A46E;background:rgba(198,164,110,.12);color:#F2EDE6}
.num{font-size:34px;font-weight:800;color:#C6A46E;letter-spacing:.2em}
.item{opacity:.22}
.item.on{opacity:1}
.logo{font-size:64px;font-weight:800;letter-spacing:.14em}
.logo .m{font-weight:300;color:#C6A46E}
.center{justify-content:center}
.big{font-size:100px;line-height:1.06;font-weight:800;letter-spacing:-.025em}
.cap{font-size:34px;font-weight:300;color:#8C8377;letter-spacing:.02em}
"""

def page(body, cls=""):
    return f"<style>{CSS}</style><div class='stage {cls}'><div class='grain'></div>{body}</div>"

def slot(h, lab, sub):
    return f"<div class='slot' style='height:{h}px'><div class='lab'>{lab}</div><div class='sub'>{sub}</div></div>"

def principles(on):
    items=[("01","сочетается с интерьером"),("02","поддерживает концепцию"),("03","становится частью образа")]
    rows="".join(
        f"<div class='row item {'on' if i<on else ''}' style='margin-top:{0 if i==0 else 52}px'>"
        f"<div class='num' style='padding-top:18px'>{n}</div>"
        f"<div class='rowtxt' style='font-size:48px'>{t}</div></div>"
        for i,(n,t) in enumerate(items))
    return rows

SLIDES = [
 # (id, start, end, html)
 ("s01",0.00,3.20, page("<div class='kicker'>униформа</div><div class='rule'></div>"
    "<h1 class='mt2'>Есть простой способ<br>испортить впечатление<br>от красивого места</h1>")),
 ("s02",3.20,5.10, page("<div class='kicker'>униформа</div><div class='rule'></div>"
    "<h1 class='mt2'>Есть простой способ<br>испортить впечатление<br>от красивого места</h1>"
    "<div class='lead mt2'>Просто выбрать <span class='accent' style='font-weight:800'>случайную униформу</span></div>")),
 ("s03",5.10,8.69, page("<div class='kicker'>знакомо?</div>"
    "<h2 class='mt'>Тот самый обычный фартук<br>с логотипом</h2>"
    + "<div class='mt2'>" + slot(760,"кадр 1","обычный / случайный фартук — «как у всех»") + "</div>")),
 ("s04",8.69,10.92, page("<div class='spacer'></div>"
    "<div class='row'><div class='mark good'>✓</div><div><div class='rowtxt'>Функцию — выполняет</div>"
    "<div class='rowsub'>защищает, обозначает персонал</div></div></div>"
    "<div class='row' style='margin-top:60px;opacity:.18'><div class='mark bad'>✕</div><div><div class='rowtxt'>Образу места — ничего не добавляет</div></div></div>"
    "<div class='spacer'></div>")),
 ("s05",10.92,13.32, page("<div class='spacer'></div>"
    "<div class='row' style='opacity:.3'><div class='mark good'>✓</div><div><div class='rowtxt'>Функцию — выполняет</div>"
    "<div class='rowsub'>защищает, обозначает персонал</div></div></div>"
    "<div class='row' style='margin-top:60px'><div class='mark bad'>✕</div><div><div class='rowtxt'>Образу места —<br>ничего не добавляет</div></div></div>"
    "<div class='spacer'></div>")),
 ("s06",13.32,16.72, page("<div class='kicker'>а когда наоборот</div><div class='rule'></div>"
    "<h2 class='mt2'>Когда униформа подобрана<br>правильно —<br><span class='accent'>это всегда чувствуется</span></h2>")),
 ("s07",16.72,20.54, page("<h2>Всё выглядит цельно</h2>"
    "<div class='lead mt'>здесь подумали о каждой детали</div>"
    + "<div class='mt2'>" + slot(820,"кадр 2","интерьер + персонал в подобранной форме — «цельная картинка»") + "</div>")),
 ("s08",20.54,25.92, page("<div class='spacer'></div>"
    "<div class='kicker' style='color:#D97B62'>и наоборот</div>"
    "<h2 class='mt'>Если форма выбивается<br>из общего стиля —</h2>"
    "<div class='lead mt'>даже в красивом пространстве<br>чего-то будет не хватать</div>"
    "<div class='spacer'></div>")),
 ("s09",25.92,28.65, page("<div class='kicker'>униформа должна</div><div class='rule'></div>"
    "<div class='mt2'>"+principles(1)+"</div>")),
 ("s10",28.65,30.69, page("<div class='kicker'>униформа должна</div><div class='rule'></div>"
    "<div class='mt2'>"+principles(3)+"</div>")),
 ("s11",30.69,33.44, page("<div class='spacer'></div><div class='logo'>WIKEN<span class='m'>MADE</span></div>"
    "<div class='rule'></div><h2 class='mt2'>Готовый каталог<br>униформы</h2><div class='spacer'></div>")),
 ("s12",33.44,37.06, page("<div class='logo' style='font-size:44px'>WIKEN<span class='m'>MADE</span></div>"
    "<h2 class='mt2'>Для кого</h2>"
    "<div class='chips mt2'><div class='chip on'>рестораны</div><div class='chip on'>отели</div>"
    "<div class='chip on'>бьюти</div><div class='chip on'>сервисные пространства</div></div>"
    + "<div class='mt2'>" + slot(600,"кадр 3","линейка моделей из каталога") + "</div>")),
 ("s13",37.06,38.78, page("<div class='kicker'>как это работает</div><div class='rule'></div>"
    "<div class='mt2'><div class='row'><div class='num' style='padding-top:14px'>01</div>"
    "<div class='rowtxt'>Подобрать подходящую модель</div></div>"
    "<div class='row item mt2'><div class='num' style='padding-top:14px'>02</div><div class='rowtxt'>Цвет · ткань · фактура</div></div>"
    "<div class='row item mt2'><div class='num' style='padding-top:14px'>03</div><div class='rowtxt'>Логотип · вышивка · печать</div></div></div>")),
 ("s14",38.78,40.97, page("<div class='kicker'>как это работает</div><div class='rule'></div>"
    "<div class='mt2'><div class='row item on' style='opacity:.35'><div class='num' style='padding-top:14px'>01</div>"
    "<div class='rowtxt'>Подобрать подходящую модель</div></div>"
    "<div class='row mt2'><div class='num' style='padding-top:14px'>02</div><div class='rowtxt'>Цвет · ткань · фактура</div></div>"
    "<div class='row item mt2'><div class='num' style='padding-top:14px'>03</div><div class='rowtxt'>Логотип · вышивка · печать</div></div></div>")),
 ("s15",40.97,43.27, page("<div class='kicker'>как это работает</div><div class='rule'></div>"
    "<div class='mt2'><div class='row' style='opacity:.35'><div class='num' style='padding-top:14px'>01</div>"
    "<div class='rowtxt'>Подобрать подходящую модель</div></div>"
    "<div class='row mt2' style='opacity:.35'><div class='num' style='padding-top:14px'>02</div><div class='rowtxt'>Цвет · ткань · фактура</div></div>"
    "<div class='row mt2'><div class='num' style='padding-top:14px'>03</div><div class='rowtxt'>Логотип · вышивка · печать</div></div></div>"
    + "<div class='mt2'>" + slot(480,"кадр 4","деталь: логотип / вышивка на форме, крупно") + "</div>")),
 ("s16",43.27,49.29, page("<div class='spacer'></div><div class='kicker'>не нашли нужную модель?</div>"
    "<h2 class='mt2'>Разработаем униформу<br><span class='accent'>с нуля</span></h2>"
    "<div class='lead mt'>индивидуально под ваш проект</div><div class='spacer'></div>")),
 ("s17",49.29,52.14, page("<div class='spacer'></div>"
    "<div class='lead'>Форму, может быть,<br>никто специально<br>и не рассматривает</div><div class='spacer'></div>")),
 ("s18",52.14,53.79, page("<div class='spacer'></div><div class='big'>Но замечают<br>её <span class='accent'>все</span></div>"
    "<div class='spacer'></div><div class='logo' style='font-size:52px'>WIKEN<span class='m'>MADE</span></div>"
    "<div class='cap mt'>униформа для сервисных пространств</div>")),
]

os.makedirs("slides", exist_ok=True)
meta=[]
for sid,a,b,html in SLIDES:
    open(f"slides/{sid}.html","w").write(html)
    meta.append({"id":sid,"start":a,"end":b,"dur":round(b-a,3)})
json.dump(meta, open("slides/meta.json","w"), ensure_ascii=False, indent=1)
print(f"{len(SLIDES)} slides, total {sum(m['dur'] for m in meta):.2f}s")
