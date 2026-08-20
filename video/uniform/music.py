# -*- coding: utf-8 -*-
"""Фоновый эмбиент под ролик iconmade: 48.70 с, 48 кГц, стерео."""
import numpy as np, wave

SR=48000; DUR=48.70; BPM=72.0
N=int(SR*DUR); t=np.arange(N)/SR
BEAT=60.0/BPM; BAR=4*BEAT          # 3.333 с
rng=np.random.default_rng(7)

def env(a, d, s, r, dur):
    """ADSR как огибающая длиной dur секунд"""
    n=int(dur*SR); e=np.zeros(n)
    ai,di,ri=int(a*SR),int(d*SR),int(r*SR)
    ai=min(ai,n); e[:ai]=np.linspace(0,1,ai)
    di=min(di,max(0,n-ai)); e[ai:ai+di]=np.linspace(1,s,di)
    body=max(0,n-ai-di-ri); e[ai+di:ai+di+body]=s
    if ri>0: e[n-ri:]=np.linspace(e[n-ri-1] if n-ri>0 else s,0,ri)
    return e

def voice(f, n, detune=6.0):
    """мягкий органный тембр из трёх расстроенных голосов"""
    out=np.zeros(n); tt=np.arange(n)/SR
    for c in (-detune,0.0,detune):
        ff=f*2**(c/1200.0)
        ph=rng.uniform(0,2*np.pi)
        out+= (np.sin(2*np.pi*ff*tt+ph)
               +0.30*np.sin(2*np.pi*2*ff*tt+ph*1.7)
               +0.13*np.sin(2*np.pi*3*ff*tt+ph*2.3)
               +0.06*np.sin(2*np.pi*4*ff*tt+ph*0.9)
               +0.030*np.sin(2*np.pi*6*ff*tt+ph*1.3)
               +0.016*np.sin(2*np.pi*8*ff*tt+ph*2.1))
    return out/3.0

def lp(x, cutoff):
    """однополюсный ФНЧ, cutoff — массив или число"""
    a=np.exp(-2*np.pi*np.asarray(cutoff)/SR)
    a=np.broadcast_to(a, x.shape).copy()
    y=np.empty_like(x); acc=0.0
    for i in range(len(x)):
        acc=(1-a[i])*x[i]+a[i]*acc; y[i]=acc
    return y

def lp_fast(x, cutoff_hz):
    """ФНЧ через частотную область — быстрее для статичного среза"""
    n=len(x); X=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR)
    return np.fft.irfft(X/(1+1j*f/cutoff_hz), n)

# ── гармония: 2 такта на аккорд ────────────────────────────────────────────
A2,E2,F2 = 110.00, 82.41, 87.31
C3,E3,F3,G3 = 130.81,164.81,174.61,196.00
A3,B3,C4,D4,E4,G4 = 220.00,246.94,261.63,293.66,329.63,392.00
CHORDS=[[A2,E3,A3,C4,B3],[F2,C3,A3,E4],[C3,G3,C4,E4,B3],[E2,B3,E3,G3,D4],
        [A2,E3,A3,C4,B3],[F2,C3,F3,A3,E4],[C3,G3,C4,E4,D4]]
CH_LEN=2*BAR
pad=np.zeros(N)
for i,ch in enumerate(CHORDS):
    start=i*CH_LEN
    if start>=DUR: break
    seg=min(CH_LEN+2.4, DUR-start)          # хвост наезжает на следующий аккорд
    n=int(seg*SR); s0=int(start*SR)
    e=env(1.30,0.9,0.72,1.6,seg)
    block=sum(voice(f,n)*(0.85 if f<140 else 1.0) for f in ch)/len(ch)
    pad[s0:s0+n]+=block*e
pad=lp_fast(pad, 2600.0)
# медленное дыхание среза
pad*= (0.80+0.20*np.sin(2*np.pi*t/17.0))

# ── арпеджио (входит на «правильной униформе») ─────────────────────────────
arp=np.zeros(N); step=BEAT/2
k=0; tt=0.0
while tt<DUR:
    ch=CHORDS[min(int(tt//CH_LEN), len(CHORDS)-1)]
    f=ch[(k*2+1)%len(ch)]*2.0
    if f>700: f/=2
    d=1.05; n=int(d*SR); s0=int(tt*SR); n=min(n, N-s0)
    if n>0:
        tl=np.arange(n)/SR
        note=(np.sin(2*np.pi*f*tl)+0.35*np.sin(2*np.pi*2*f*tl)+0.12*np.sin(2*np.pi*3.01*f*tl))
        note*=np.exp(-tl*4.2)*np.minimum(1.0, tl*260)
        arp[s0:s0+n]+=note*(0.55 if k%2 else 0.85)
        sh=int(2.2*SR); sh=min(sh, N-s0)
        if sh>0 and k%2==0:
            tl2=np.arange(sh)/SR
            arp[s0:s0+sh]+=0.22*np.sin(2*np.pi*f*2*tl2)*np.exp(-tl2*1.7)*np.minimum(1.0,tl2*90)
    tt+=step; k+=1
arp=lp_fast(arp, 7000.0)

# ── низкий пульс ───────────────────────────────────────────────────────────
sub=np.zeros(N); tt=0.0
while tt<DUR:
    n=int(0.55*SR); s0=int(tt*SR); n=min(n,N-s0)
    if n>0:
        tl=np.arange(n)/SR
        f=55.0*(1+0.6*np.exp(-tl*26))
        sub[s0:s0+n]+=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tl*5.0)
    tt+=2*BEAT

# ── воздух ─────────────────────────────────────────────────────────────────
_nz=rng.normal(0,1,N)
air=lp_fast(_nz, 9000.0)-lp_fast(_nz, 2500.0)
air*= (0.5+0.5*np.sin(2*np.pi*t/11.0))

def ramp(x0,x1): return np.clip((t-x0)/max(1e-6,x1-x0),0,1)
g_pad = ramp(0.0,4.2)*(1-0.55*ramp(46.9,48.7))
g_arp = ramp(11.9,13.6)*(1-ramp(45.6,47.4))
g_sub = ramp(4.6,6.4)*(1-ramp(45.0,47.0))
g_air = ramp(0.0,6.0)*(1-0.7*ramp(47.0,48.7))
# на блоке бренда добавляем плотности
lift  = 1.0+0.22*(ramp(27.6,28.6)-ramp(33.4,34.4))

mono = (0.62*pad*g_pad*lift + 0.20*arp*g_arp + 0.24*sub*g_sub + 0.055*air*g_air)

# ── стерео + реверберация ──────────────────────────────────────────────────
def reverb(x, tail=2.6, pre=0.028, dark=2600.0):
    n=int(tail*SR)
    ir=rng.normal(0,1,n)*np.exp(-np.arange(n)/SR*3.1)
    ir=lp_fast(ir, dark); ir[:int(pre*SR)]*=0.06
    ir/=np.abs(ir).max()
    L=1<<int(np.ceil(np.log2(len(x)+n)))
    y=np.fft.irfft(np.fft.rfft(x,L)*np.fft.rfft(ir,L), L)[:len(x)]
    return y/ (np.abs(y).max()+1e-9)

wet=reverb(mono)
d=int(0.012*SR)
L=mono+0.34*wet
R=np.concatenate([np.zeros(d), mono[:-d]])*0.98+0.34*np.roll(wet,-d)
st=np.stack([L,R],axis=1)
st=np.tanh(st*1.25)/1.25                       # мягкое насыщение
st/=np.abs(st).max()/0.92
st*=np.minimum(1.0, np.clip(t/1.2,0,1))[:,None]        # фейд-ин
st*=np.minimum(1.0, np.clip((DUR-t)/1.6,0,1))[:,None]  # фейд-аут

pcm=(np.clip(st,-1,1)*32767).astype(np.int16)
with wave.open("music.wav","w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"music.wav  {len(pcm)/SR:.2f}s  peak={np.abs(st).max():.3f}")
