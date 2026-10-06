import json,sys,subprocess,re,os,numpy as np,soundfile as sf
import sherpa_onnx
from scipy.signal import butter,sosfilt
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); TTS=os.path.join(HERE,"models")+"/"
SR=44100; FPS=30; PAD=0.25; WORD0=.22; WSTEP=.09
spec=json.load(open(sys.argv[1])); out=sys.argv[2]; debug=len(sys.argv)>3 and sys.argv[3]=="debug"
os.makedirs("work",exist_ok=True)
rs=np.random.RandomState(7)


# ---------- prononciation : mots que la voix française lit mal -> écriture phonétique (voix uniquement, les sous-titres restent normaux)
LEX=[(r"burgers?","beurgueur"),(r"tacos","takoss"),(r"k[ée]babs?","kébab"),(r"bubble\s*tea","bobeul ti"),(r"food[\s-]*trucks?","foude treuk"),
 (r"fast[\s-]*foods?","faste foude"),(r"cheese","tchize"),(r"google","gougueul"),(r"wi-?fi","ouifi"),(r"brunch","breunch"),(r"milk-?shakes?","milkchèke"),
 (r"ketchup","kétchoupe"),(r"smash","smache"),(r"topping","toping"),(r"sandwicheries","sandouicheri"),(r"sandwicherie","sandouicheri"),(r"sandwichs?","sandouiche"),(r"sandwiches","sandouiche"),
 (r"nuggets","neugueutse"),(r"cookies?","kouki"),(r"e-?mails?","imèl"),(r"you-?tube","iou tube"),(r"tik-?tok","tik tok"),(r"followers?","folooweur"),
 (r"likes?","laïke"),(r"lives?","laïve"),(r"reels?","ril"),(r"stor(?:y|ies)","stori"),(r"marketing","markétingue"),(r"business","bizness"),(r"feedbacks?","fidebak"),
 (r"cashback","cache bak"),(r"drive","draïve"),(r"happy hour","appi aour"),(r"lunch","leunche"),(r"boost(?:er)?","bouste"),(r"check","chèque"),(r"hashtags?","ache tag"),(r"shorts","chorts")]
def say_fix(x):
    for p,r in LEX: x=re.sub(r"\b"+p+r"\b",r,x,flags=re.I)
    return x

# ---------- voice ----------
D=TTS+"vits-piper-fr_FR-tom-medium"
tts=sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=D+"/fr_FR-tom-medium.onnx",tokens=D+"/tokens.txt",data_dir=D+"/espeak-ng-data",noise_scale=0.667,noise_scale_w=0.8,length_scale=spec.get("length",0.9)),num_threads=2)))
voices=[]
for s in spec["scenes"]:
    g=tts.generate(say_fix(s["say"]),sid=0,speed=1.0); w=np.array(g.samples,dtype=np.float32)
    assert g.sample_rate==SR
    w=w/max(1e-6,np.abs(w).max())*0.9
    idx=np.where(np.abs(w)>0.04)[0]
    if len(idx): w=w[max(0,idx[0]-int(.02*SR)):idx[-1]+int(.06*SR)]
    voices.append(w)

# ---------- page: word counts ----------
pw=sync_playwright().start(); br=pw.chromium.launch(); pg=br.new_page(viewport={"width":1080,"height":1920})
pg.goto("file://"+os.path.abspath("template.html")); pg.wait_for_timeout(400)
wc=pg.evaluate("s=>buildScenes(s)",spec["scenes"])

# ---------- timeline ----------
scenes=[];caps=[];t=0.0;hits=[];vstarts=[]
N=len(spec["scenes"])
for i,(s,w) in enumerate(zip(spec["scenes"],voices)):
    d=len(w)/SR; tail=0.22 if i<N-1 else 1.3
    start=t; pd=0.04 if i==0 else PAD; vs=start+pd; end=vs+d+tail; sid="s%d"%(i+1); ty=s["type"]
    ev={}
    PADs=PAD if i else 0.04
    if ty=="phone_loyalty": ev["fill0"]=PAD+d*.5; ev["fill1"]=ev["fill0"]+.9; ev["unlock"]=ev["fill1"]+.05
    if ty=="phone_sms": ev["n1"]=PAD+d*.5; ev["n2"]=ev["n1"]+.8; ev["chip"]=ev["n2"]+.4
    if ty=="phone_review": ev["press"]=PAD+d*.55; ev["stars"]=ev["press"]+.35
    if ty=="phone_dash": ev["k0"]=PAD+.9; ev["b0"]=PAD+max(.9,d*.25); ev["chip"]=ev["b0"]+1.4
    if ty=="tips":
        nI=len(s["items"]); t0=PAD+max(.9,d*.2); gap=max(.6,d*.65/nI); ev["items"]=[t0+k*gap for k in range(nI)]
    if ty=="cta": ev["url"]=PAD+d*.78
    scenes.append({"id":sid,"type":ty,"p":s,"start":start,"end":end,"ev":ev,"vs":vs,"d":d})
    words=s["cap"].split(); chunks=[];cur=[]
    for wd in words:
        cur.append(wd)
        if len(cur)>=3 or re.search(r"[.?!,]$",wd): chunks.append(cur);cur=[]
    if cur: chunks.append(cur)
    tot=sum(len(" ".join(c)) for c in chunks); cs=vs
    for c in chunks:
        dd=d*len(" ".join(c))/tot
        h=" ".join(f"<b>{x}</b>" if x.strip(".,?!").lower() in s.get("hl",[]) else x for x in c)
        caps.append({"s":cs,"e":cs+dd,"h":h}); cs+=dd
    vstarts.append(vs); t=end
total=t
# shake hits
for sc in scenes:
    st=sc["start"]; ty=sc["type"]; sid=sc["id"]
    if ty=="hook":
        hits.append({"t":st+.02,"a":16}); hits.append({"t":st+.34,"a":8})
    if ty=="cta": hits.append({"t":st+.3,"a":20})
    if ty=="phone_loyalty": hits.append({"t":st+sc["ev"]["unlock"],"a":9})
    if ty=="phone_review": hits.append({"t":st+sc["ev"]["press"],"a":6})

# ---------- synth helpers ----------
n=int(total*SR)+SR
def T(d): return np.arange(int(d*SR))/SR
def hp(x,fc): return sosfilt(butter(2,fc,'high',fs=SR,output='sos'),x)
def lp(x,fc): return sosfilt(butter(2,fc,'low',fs=SR,output='sos'),x)
def bp(x,lo,hi): return sosfilt(butter(2,[lo,hi],'band',fs=SR,output='sos'),x)
def put(buf,t0,sig,g=1.0):
    a=int(t0*SR)
    if a<0: sig=sig[-a:]; a=0
    b=min(len(buf),a+len(sig))
    if b>a: buf[a:b]+=sig[:b-a]*g
def kick():
    t=T(.38); f=42+120*np.exp(-t*30); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)
    s[:200]+=rs.randn(200)*.3*np.linspace(1,0,200); return s
def clap():
    t=T(.22); x=hp(rs.randn(len(t)),1100)*np.exp(-t*22)
    for off in (.011,.022):
        k=int(off*SR); x[k:]+=0.7*x[:-k]*0
    y=np.zeros(len(t))
    for off,gg in ((0,1),(.010,.8),(.021,.7)):
        k=int(off*SR); y[k:]+=x[:len(t)-k]*gg
    return y*0.8
def hat(o=.04): t=T(o+.02); return hp(rs.randn(len(t)),7000)*np.exp(-t/(o/4))
def bassn(f,d=.26):
    t=T(d); s=np.sin(2*np.pi*f*t)+.45*np.sin(2*np.pi*2*f*t)+.25*(2*((f*t)%1)-1)
    return lp(s,900)*np.minimum(1,t/.004)*np.exp(-t*7)
def pluck(f,d=.22):
    t=T(d); s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.3*np.sin(2*np.pi*3*f*t)
    return s*np.exp(-t*16)
def pad(fs,d):
    t=T(d); s=sum(np.sin(2*np.pi*f*t)+.3*np.sin(2*np.pi*2*f*t) for f in fs)/len(fs)
    return s*np.minimum(1,t/.25)*np.minimum(1,(d-t)/.25)
def crash(d=1.4): t=T(d); return hp(rs.randn(len(t)),5000)*np.exp(-t*3.2)
def whoosh(d=.6):
    t=T(d); nz=rs.randn(len(t)); o=np.zeros(len(t))
    bands=[250,500,1000,2000,4000,8000]
    for k,fc in enumerate(bands):
        y=bp(nz,fc/1.5,min(fc*1.5,20000)); c=(k+.5)/len(bands)*d
        o+=y*np.exp(-((t-c)/(d*.2))**2)
    return o/np.abs(o).max()*np.sin(np.pi*np.clip(t/d,0,1))**.7
def riser(d=1.3):
    t=T(d); x=hp(rs.randn(len(t)),600)*(t/d)**2.2
    x+=np.sin(2*np.pi*np.cumsum(180+900*(t/d)**2)/SR)*.25*(t/d)**2
    return x/np.abs(x).max()
def impact(d=1.3):
    t=T(d); f=38+110*np.exp(-t*14); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3.2)
    s+=lp(rs.randn(len(t)),1800)*np.exp(-t*9)*.6
    return s/np.abs(s).max()
def popf(f=700,d=.12):
    t=T(d); ff=f*(1+.9*np.exp(-t*60)); return np.sin(2*np.pi*np.cumsum(ff)/SR)*np.exp(-t*30)
def tick(f=1200): t=T(.05); return np.sin(2*np.pi*f*t)*np.exp(-t*70)
def ding(f=1318.5,d=1.1):
    t=T(d); return (np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*2*f*t)+.25*np.sin(2*np.pi*3*f*t))*np.exp(-t*4.5)*np.minimum(1,t/.003)
def ping():
    a=ding(1046.5,.5); b=ding(1568,.7); o=np.zeros(int(.9*SR)); o[:len(a)]+=a*.8; k=int(.12*SR); o[k:k+len(b)]+=b; return o
def click(): t=T(.04); return (hp(rs.randn(len(t)),2500)*np.exp(-t*160)+np.sin(2*np.pi*1800*t)*np.exp(-t*200))
def sparkle(d=.7):
    o=np.zeros(int(d*SR))
    for i in range(10):
        f=rs.uniform(2500,6500); t0=rs.uniform(0,d-.25); s=np.sin(2*np.pi*f*T(.2))*np.exp(-T(.2)*22)
        k=int(t0*SR); o[k:k+len(s)]+=s*.5
    return o
def thud(): t=T(.25); return np.sin(2*np.pi*np.cumsum(55+80*np.exp(-t*40))/SR)*np.exp(-t*14)

# ---------- SFX ----------
def loadw(p):
    a,sr=sf.read(p); a=a.mean(1) if a.ndim>1 else a; return a/np.abs(a).max()
if os.path.exists(os.path.join(HERE,"sfx","swoosh.wav")): NOTIF=loadw(os.path.join(HERE,"sfx","notif.wav")); SWOOSH=loadw(os.path.join(HERE,"sfx","swoosh.wav"))
else: NOTIF=ping(); SWOOSH=whoosh(1.0)
def soft(f=520,d=.1):
    t=T(d); return lp(np.sin(2*np.pi*f*t)*np.exp(-t*38),1400)

sfx=np.zeros(n,dtype=np.float64)
def S(t0,sig,g=1.0): put(sfx,t0,sig,g)
for i,sc in enumerate(scenes):
    st=sc["start"]; sid=sc["id"]; ev=sc["ev"]; ty=sc["type"]
    if i<N-1:
        S(sc["end"]-.494,SWOOSH,.85); S(sc["end"]+.0,thud(),.3)
    if ty=="hook": S(st+.0,impact(.7),.6); S(st+.0,SWOOSH[int(.35*SR):int(.85*SR)],.5)
    if i>0 and ty!="cta": S(st+.38,SWOOSH[:int(.8*SR)]*np.linspace(1,0,int(.8*SR))**1.5,.22)
    for k in range(wc[sid]):
        tt=st+WORD0+WSTEP*k+.1
        if ty=="hook": pass
        elif ty!="cta": S(tt,soft(420+20*k,.1),.35)
    if ty=="phone_loyalty":
        for k in range(11): S(st+ev["fill0"]+k*.09,soft(380*1.05**k,.06),.28)
        S(st+ev["unlock"],soft(520,.16),.7); S(st+ev["unlock"],thud(),.45); S(st+ev["unlock"]+.03,sparkle(.5),.08)
    if ty=="phone_sms":
        S(st+ev["n1"]-.079,NOTIF,.8); S(st+ev["n2"]-.079,NOTIF[:int(1.3*SR)]*np.linspace(1,0,int(1.3*SR))**.8,.65)
        S(st+ev["chip"],soft(450,.12),.4)
    if ty=="phone_review":
        S(st+ev["press"],click(),.5); S(st+ev["press"]+.02,soft(320,.14),.5)
        S(st+ev["stars"],soft(400,.12),.3)
        for k in range(5): S(st+ev["stars"]+.1+.12*k,soft(420*1.09**k,.07),.3)
    if ty=="phone_dash":
        for k in range(8): S(st+ev["b0"]+.1*k,soft(360*1.07**k,.07),.28)
        for k in range(10): S(st+ev["k0"]+k*.12,soft(420*1.04**k,.05),.2)
        S(st+ev["chip"],soft(480,.14),.45)
    if ty=="tips":
        for k,tm in enumerate(ev["items"]): S(st+tm,soft(420*1.08**k,.12),.5); S(st+tm+.02,thud(),.25)
    if i<N-1 and spec["scenes"][i+1]["type"]=="cta": S(sc["end"]-1.25,lp(riser(1.25),3500),.3)
    if ty=="cta":
        S(st+.12,impact(1.3),.55); S(st+.25,sparkle(),.1); S(st+.18,lp(crash(1.5),6000),.12)
        for k in range(6): S(st+.35+.06*k,soft(380*1.07**k,.06),.22)
        for k in range(wc[sid]): S(st+.2+WORD0+WSTEP*k+.1,soft(430+20*k,.1),.35)
        S(st+ev["url"],soft(460,.14),.55); S(st+ev["url"]-.079,(lambda x:x*np.linspace(1,0,len(x)))(NOTIF[:int(1.6*SR)]),.45)

# ---------- music ----------
# 6 styles (spec["music"] = 0..5) : tempo, accords, basses, motifs de batterie
MUSICS=[
 dict(bpm=124,chords=[[220,261.6,329.6],[174.6,220,261.6],[261.6,329.6,392],[196,246.9,293.7]],roots=[55,43.65,65.4,49],kick=(0,4,8,12),clap=(4,12),hat=(0,2,4,6,8,10,12,14),bass=(2,3,6,10,11,14),arp=False),
 dict(bpm=96,chords=[[261.6,311.1,392],[207.7,261.6,311.1],[311.1,392,466.2],[233.1,293.7,349.2]],roots=[65.4,51.9,77.8,58.3],kick=(0,7,10),clap=(4,12),hat=(0,2,4,6,8,10,12,14),bass=(0,7,10,14),arp=False),
 dict(bpm=112,chords=[[293.7,349.2,440],[233.1,293.7,349.2],[174.6,220,261.6],[261.6,329.6,392]],roots=[73.4,58.3,43.65,65.4],kick=(0,6,8,11),clap=(4,12),hat=tuple(range(0,16,1)),bass=(0,3,6,8,11,14),arp=True),
 dict(bpm=128,chords=[[164.8,196,246.9],[261.6,329.6,392],[196,246.9,293.7],[146.8,185,220]],roots=[41.2,65.4,49,36.7],kick=(0,4,8,12),clap=(4,12),hat=(2,6,10,14),bass=(2,6,10,14),arp=False),
 dict(bpm=88,chords=[[349.2,440,523.3],[329.6,392,493.9],[293.7,349.2,440],[261.6,329.6,392]],roots=[43.65,41.2,36.7,32.7],kick=(0,10),clap=(8,),hat=(0,4,8,12),bass=(0,10),arp=True),
 dict(bpm=118,chords=[[220,277.2,329.6],[246.9,293.7,370],[196,246.9,293.7],[185,220,277.2]],roots=[55,61.7,49,46.2],kick=(0,3,8,11),clap=(4,12),hat=(0,2,4,6,8,10,12,14),bass=(0,3,6,8,11,14),arp=True),
]
M=MUSICS[int(spec.get("music",0))%len(MUSICS)]
BPM=M["bpm"]; beat=60/BPM; step=beat/4
mus=np.zeros(n,dtype=np.float64); drums=np.zeros(n,dtype=np.float64)
chords=M["chords"]; roots=M["roots"]
s2s=scenes[min(1,N-1)]["start"]; s3s=scenes[min(2,N-1)]["start"]; s5s=scenes[-1]["start"]
nsteps=int(total/step)+2
kk=kick(); cl=clap();
for i in range(nsteps):
    t0=i*step
    if t0>total: break
    bar=(i//16)%4; sp=i%16
    full=t0>=s5s; mid=t0>=s2s; arpon=t0>=s3s
    if sp in M["kick"]: put(drums,t0,kk,.55)
    if sp in M["clap"] and mid: put(drums,t0,cl,.28)
    if sp in M["hat"] and t0>.3: put(drums,t0,hat(.05 if sp%4 else .07),(.12 if sp%4==2 else .06) if len(M["hat"])<16 else (.07 if sp%4==0 else .03))
    if full and sp%2==1 and len(M["hat"])<16: put(drums,t0,hat(.03),.1)
    if mid and sp in M["bass"]: put(mus,t0,bassn(roots[bar]*(2 if sp in (3,11) else 1)),.38)
    if M["arp"] and mid and sp%2==0: put(mus,t0,pluck(chords[bar][(sp//2)%3]*2,.2),.07)
    if sp==0 and i%16==0:
        put(mus,t0,pad(chords[bar],step*16),.16 if not full else .22)
    if sp==0 and i%64==0 and (t0>=s2s-.2) and (abs(t0-s2s)<2 or abs(t0-s5s)<2): put(drums,t0,crash(1.2),.2)
put(drums,s2s,lp(crash(1.2),7000),.08); put(drums,s5s,lp(crash(1.6),7000),.1)
tt=np.arange(n)/SR
pump=1-.55*np.exp(-(tt%beat)*9)
music=lp(drums+mus*pump,8000)
fade=np.clip((total-tt)/1.0,0,1)*np.clip(tt/.08,0,1); music*=fade

# ---------- voice track + EQ ----------
vtrack=np.zeros(n,dtype=np.float64)
for vs,w in zip(vstarts,voices): put(vtrack,vs,w,1.0)
sf.write("work/voice_raw.wav",vtrack[:int(total*SR)].astype(np.float32),SR)
chain=("highpass=f=90,asetrate=%d,aresample=%d,atempo=%.5f,"%(int(SR*.955),SR,1/.955)+
 "equalizer=f=220:t=q:w=1.0:g=3.5,equalizer=f=1000:t=q:w=1.1:g=-5,equalizer=f=1700:t=q:w=1.4:g=-2.5,"
 "equalizer=f=3800:t=q:w=1.5:g=1.5,equalizer=f=6500:t=q:w=2:g=2,"
 "acompressor=threshold=0.1:ratio=3:attack=5:release=90:makeup=2.5,aecho=0.7:0.55:28:0.12")
subprocess.run(["ffmpeg","-y","-v","error","-i","work/voice_raw.wav","-af",chain,"work/voice_fx.wav"],check=True)
vfx,_=sf.read("work/voice_fx.wav");
if vfx.ndim>1: vfx=vfx.mean(1)
vtrack=np.zeros(n); vtrack[:len(vfx)]=vfx[:n]
# time shift correction: pitch change keeps length (atempo compensates)

# ---------- mix ----------
env=np.abs(vtrack); k_=int(.12*SR); env=np.convolve(env,np.ones(k_)/k_,mode="same"); duck=1-.62*np.clip(env*9,0,1)
mix=vtrack*1.3+music*.30*duck+sfx*.6
mix=mix/max(1.0,np.abs(mix).max()/.95)
mix=mix[:int(total*SR)]
sf.write("work/mix.wav",mix.astype(np.float32),SR)
json.dump({"total":total,"scenes":scenes,"caps":caps,"hits":hits},open("work/tl.json","w"),ensure_ascii=False)

# ---------- render ----------
nf=int(total*FPS)
ff=subprocess.Popen(["ffmpeg","-y","-v","error","-f","image2pipe","-framerate",str(FPS),"-c:v","mjpeg","-i","-","-i","work/mix.wav","-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","21","-pix_fmt","yuv420p","-r",str(FPS),"-af","loudnorm=I=-14:TP=-1.5:LRA=11","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",out],stdin=subprocess.PIPE)
pg.evaluate("tl=>setTL(tl)",json.load(open("work/tl.json")))
if debug: pg.evaluate("debug(true)")
for i in range(nf):
    pg.evaluate(f"seek({i/FPS})")
    ff.stdin.write(pg.screenshot(type="jpeg",quality=93))
br.close(); pw.stop()
ff.stdin.close(); ff.wait(); print("done",round(total,2),nf)
