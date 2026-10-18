"""Render the JJ Tour Québec intro film: photos with Ken Burns + Korean titles + stat cards, muxed with music.wav."""
import sys, os, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg

IMG = sys.argv[1]; OUT = sys.argv[2]; WAV = sys.argv[3]
PREVIEW = len(sys.argv) > 4 and sys.argv[4]  # comma list of seconds -> png stills
W, H, FPS = 1280, 720, 30
FONT = "/System/Library/Fonts/AppleSDGothicNeo.ttc"
F = lambda size, idx: ImageFont.truetype(FONT, size, index=idx)
REG, MED, SEMI, BOLD, LIGHT, XB, HEAVY = 0, 2, 4, 6, 8, 14, 16

ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * min(1, max(0, x)))

# ---------------- timeline ----------------
# photo shot: ("ph", t0, t1, key, zoom from, zoom to, pan (dx,dy) in fraction, chapter label, title, sub)
# card: ("card", t0, t1, kind, data)
S = []
def ph(t0, d, key, title="", sub="", ch="", z=(1.04, 1.16), pan=(0.0, 0.0)):
    S.append(dict(k="ph", t0=t0, t1=t0 + d, key=key, title=title, sub=sub, ch=ch, z=z, pan=pan))
def card(t0, d, kind, **kw):
    S.append(dict(k="card", t0=t0, t1=t0 + d, kind=kind, **kw))

card(0, 6.4, "heart")
card(6.0, 5.6, "flight")
ph(11.0, 4.6, "frontenac_winter", "퀘벡은 어떤 곳일까?", "추수감사절에 떠나는 우리 가족 여행 예고편", z=(1.18, 1.04))
C1 = "CHAPTER 1 · 성벽 도시  OLD QUEBEC"
ph(15.0, 3.2, "champlain", "북미에서 가장 오래된 거리", "1608년 샹플랭이 세운 마을, 프티 샹플랭", C1, pan=(0.0, 0.03))
ph(18.0, 3.2, "place_royale", "400년 된 광장과 교회", "루아얄 광장 · 승리의 노트르담 교회", C1, pan=(-0.03, 0.02))
ph(21.0, 3.2, "marche_noel", "11월 말, 도시가 크리스마스로", "독일식 크리스마스 마켓", C1, pan=(0.03, -0.02))
card(24.2, 4.2, "stat", big="1608", line1="샹플랭이 퀘벡을 세운 해", line2="멕시코 북쪽 유일한 성벽 도시", photo="dufferin")
C2 = "CHAPTER 2 · 강과 폭포  RIVER & FALLS"
ph(28.2, 3.2, "montmorency", "나이아가라보다 30m 높은 폭포", "몽모랑시 폭포, 83m", C2, z=(1.14, 1.02), pan=(0, 0.03))
ph(31.2, 3.2, "ste_anne", "350년 넘게 이어진 순례길", "생탄드보프레 대성당", C2, pan=(0, -0.04))
ph(34.2, 3.2, "citadelle", "지금도 군인이 지키는 별 모양 요새", "시타델", C2, pan=(0.04, 0))
card(37.4, 4.2, "stat", big="1759", line1="아브라함 평원에서", line2="15분 만에 역사가 바뀐 해", photo="plaines_hist")
C3 = "CHAPTER 3 · 섬의 도시  MONTREAL"
ph(41.6, 3.0, "via", "정오 기차로 260km", "VIA 레일 3시간 22분", C3, pan=(0.04, 0))
ph(44.6, 3.2, "notre_dame", "빛과 음악으로 채우는 성당", "노트르담 대성당 AURA", C3, pan=(0, -0.03))
ph(47.8, 3.0, "smoked_meat", "1928년부터 이어진 맛", "Schwartz's 훈제고기 샌드위치", C3, pan=(-0.03, 0))
ph(50.8, 3.0, "bagel", "꿀물에 삶아 장작불에 굽는", "몬트리올 베이글", C3, z=(1.02, 1.14))
ph(53.8, 3.2, "mont_royal", "도시 이름이 된 산", "몽루아얄 전망대", C3, pan=(0.03, 0))
CF = "OUR FAMILY"
ph(57.0, 3.2, "frontenac", "첫마디는 Bonjour!", "Jaei & Jia의 프랑스어 배지 5개", CF, pan=(-0.03, 0))
card(60.2, 8.8, "end", photo="frontenac_ice")
DUR = 69.0

# ---------------- assets ----------------
cache = {}
def photo(key):
    if key not in cache:
        im = Image.open(os.path.join(IMG, key + ".jpg")).convert("RGB")
        # cover-fit to 1.25x output so zooms stay sharp-ish
        s = max(W * 1.25 / im.width, H * 1.25 / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32)
        # warm, slightly faded cinematic grade
        a = a * np.array([1.04, 1.0, 0.94]) + np.array([4, 2, 0])
        a = 255 * (a / 255) ** 0.95
        cache[key] = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return cache[key]

def kenburns(key, p, z, pan):
    im = photo(key)
    zz = z[0] + (z[1] - z[0]) * ease(p)
    bw, bh = im.width / zz / 1.25 * 1.25, im.height / zz / 1.25 * 1.25
    # visible window in source px: output aspect at current zoom
    s = max(W / im.width, H / im.height)
    vw, vh = W / s / zz * 1.25 / 1.25, H / s / zz * 1.25 / 1.25
    vw = min(vw, im.width); vh = min(vh, im.height)
    cx = im.width / 2 + pan[0] * im.width * (p - 0.5)
    cy = im.height / 2 + pan[1] * im.height * (p - 0.5)
    cx = min(max(cx, vw / 2), im.width - vw / 2); cy = min(max(cy, vh / 2), im.height - vh / 2)
    return im.resize((W, H), Image.BILINEAR, box=(cx - vw/2, cy - vh/2, cx + vw/2, cy + vh/2))

yy, xx = np.mgrid[0:H, 0:W]
d = np.sqrt(((xx - W/2) / (W/2)) ** 2 + ((yy - H/2) / (H/2)) ** 2)
VIG = np.clip(1 - 0.45 * np.clip(d - 0.55, 0, 1) ** 1.4, 0, 1)[..., None].astype(np.float32)
grad = np.clip((yy / H - 0.42) / 0.58, 0, 1) ** 1.3
GRAD = (1 - 0.72 * grad)[..., None].astype(np.float32)

text_cache = {}
def text_layer(lines, anchor="ls", shadow=True):
    """lines: list of (text, font, color(rgba), dy). Returns RGBA full-frame layer."""
    key = (tuple((t, id(f), c, dy) for t, f, c, dy in lines), anchor)
    if key in text_cache: return text_cache[key]
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
    for t, f, c, (x, y) in lines:
        dr.text((x, y), t, font=f, fill=c, anchor=anchor)
    if shadow:
        a = lay.split()[3].filter(ImageFilter.GaussianBlur(10))
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(a.point(lambda v: int(v * 0.65)))
        lay = Image.alpha_composite(sh, lay)
    text_cache[key] = lay
    return lay

def over(base, lay, alpha=1.0, dy=0):
    if alpha <= 0: return base
    if dy: lay2 = Image.new("RGBA", (W, H), (0, 0, 0, 0)); lay2.paste(lay, (0, int(dy))); lay = lay2
    if alpha < 1:
        a = lay.split()[3].point(lambda v: int(v * alpha)); lay = lay.copy(); lay.putalpha(a)
    return Image.alpha_composite(base, lay)

def appear(t, t0, t1, fin=0.6, fout=0.5):
    a = ease((t - t0) / fin) * (1 - ease((t - (t1 - fout)) / fout))
    return a, (1 - ease((t - t0) / (fin * 1.3))) * 22

f_ch = F(19, SEMI); f_title = F(60, XB); f_sub = F(28, MED)

def render_ph(s, t):
    p = (t - s["t0"]) / (s["t1"] - s["t0"])
    im = kenburns(s["key"], p, s["z"], s["pan"])
    a = np.asarray(im).astype(np.float32) * VIG * GRAD
    base = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
    x = 84
    if s["ch"]:
        al, dy = appear(t, s["t0"] + 0.1, s["t1"], 0.5, 0.4)
        base = over(base, text_layer([(s["ch"], f_ch, (255, 226, 160, 255), (x, 70))]), al, 0)
    if s["title"]:
        al, dy = appear(t, s["t0"] + 0.35, s["t1"] + 0.2)
        base = over(base, text_layer([(s["title"], f_title, (255, 255, 255, 255), (x, H - 128))]), al, dy)
    if s["sub"]:
        al, dy = appear(t, s["t0"] + 0.75, s["t1"] + 0.2)
        base = over(base, text_layer([(s["sub"], f_sub, (230, 236, 238, 255), (x, H - 76))]), al, dy)
    return base

def dark(alpha=1.0, col=(6, 12, 18)):
    return Image.new("RGBA", (W, H), col + (255,))

def blurred_bg(key, t, s, darkness=0.42):
    p = (t - s["t0"]) / (s["t1"] - s["t0"])
    im = kenburns(key, p, (1.1, 1.18), (0.02, 0))
    k = ("blur", key)
    if k not in cache:
        cache[k] = 1
    im = im.filter(ImageFilter.GaussianBlur(6))
    a = np.asarray(im).astype(np.float32) * darkness
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")

f_heart = F(74, XB); f_heart2 = F(30, MED); f_small = F(22, MED)
f_big = F(168, HEAVY); f_l1 = F(34, MED); f_l2 = F(40, BOLD)
f_end = F(120, HEAVY); f_end2 = F(30, SEMI); f_end3 = F(24, REG)

# heartbeat pulse times (match music.py)
HB = []; tt = 0.4; hb = 0.86
while tt < 11: HB.append(tt); tt += hb; hb = max(0.62, hb - 0.012)

def render_card(s, t):
    kind = s["kind"]; t0, t1 = s["t0"], s["t1"]
    if kind == "heart":
        base = dark()
        pulse = max([math.exp(-max(0, t - h) * 6) * (t >= h) for h in HB] + [0])
        r = 150 + 40 * pulse
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
        g.ellipse((W/2 - r, H/2 - 40 - r, W/2 + r, H/2 - 40 + r), fill=(190, 60, 50, int(60 + 120 * pulse)))
        glow = glow.filter(ImageFilter.GaussianBlur(70))
        base = Image.alpha_composite(base, glow)
        al, dy = appear(t, 1.0, t1 + 1, 0.8)
        base = over(base, text_layer([("두근, 두근.", f_heart, (255, 255, 255, 255), (W/2, H/2 - 20))], "ms"), al, dy)
        al, dy = appear(t, 3.0, t1 + 1, 0.8)
        base = over(base, text_layer([("2026년 11월, 우리 가족 넷이 눈의 도시로 떠납니다", f_heart2, (230, 230, 230, 255), (W/2, H/2 + 50))], "ms"), al, dy)
        return base
    if kind == "flight":
        base = dark(col=(8, 18, 30))
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); dr = ImageDraw.Draw(lay)
        p = ease((t - t0 - 0.4) / 3.6)
        A = (200, 470); B = (1080, 470); top = 200
        pts = []
        for i in range(121):
            u = i / 120
            x = A[0] + (B[0] - A[0]) * u; y = A[1] - (A[1] - top) * 4 * u * (1 - u)
            pts.append((x, y))
        n = int(120 * p)
        for i in range(0, n, 2):
            dr.line([pts[i], pts[i + 1]], fill=(255, 210, 140, 230), width=4)
        # faint full path
        for i in range(0, 120, 4):
            dr.line([pts[i], pts[i + 1]], fill=(255, 255, 255, 40), width=2)
        for (x, y), lab, sub in [(A, "얼바인", "SNA"), (B, "퀘벡", "YQB")]:
            dr.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(255, 255, 255, 255))
            dr.text((x, y + 44), lab, font=F(34, BOLD), fill=(255, 255, 255, 255), anchor="ms")
            dr.text((x, y + 78), sub, font=f_small, fill=(160, 180, 195, 255), anchor="ms")
        px, py = pts[min(n, 120)]
        dr.ellipse((px - 12, py - 12, px + 12, py + 12), fill=(255, 210, 140, 255))
        dr.text((W/2, 330), "북아메리카 대륙을 가로질러", font=F(26, LIGHT), fill=(150, 175, 195, 255), anchor="ms")
        al, _ = appear(t, t0, t1, 0.5, 0.5)
        base = over(base, lay, al)
        al, dy = appear(t, t0 + 1.2, t1, 0.7, 0.5)
        base = over(base, text_layer([("밤새 날아 약 4,000km", F(52, XB), (255, 255, 255, 255), (W/2, 640))], "ms"), al, dy)
        return base
    if kind == "stat":
        base = blurred_bg(s["photo"], t, s)
        al, dy = appear(t, t0 + 0.2, t1, 0.7, 0.5)
        base = over(base, text_layer([(s["line1"], f_l1, (230, 235, 238, 255), (W/2, 230))], "ms"), al, dy)
        al, dy = appear(t, t0 + 0.5, t1, 0.7, 0.5)
        base = over(base, text_layer([(s["big"], f_big, (255, 214, 140, 255), (W/2, 430))], "ms"), al, dy * 1.5)
        al, dy = appear(t, t0 + 0.9, t1, 0.7, 0.5)
        base = over(base, text_layer([(s["line2"], f_l2, (255, 255, 255, 255), (W/2, 520))], "ms"), al, dy)
        return base
    if kind == "end":
        p = (t - t0) / (t1 - t0)
        im = kenburns(s["photo"], p, (1.16, 1.0), (0, 0))
        a = np.asarray(im).astype(np.float32) * VIG * (0.62 - 0.12 * ease(p))
        base = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert("RGBA")
        al, dy = appear(t, t0 + 0.6, t1 + 2, 0.9)
        base = over(base, text_layer([("JJ TOUR", f_end, (255, 255, 255, 255), (W/2, 380))], "ms"), al, dy)
        al, dy = appear(t, t0 + 1.4, t1 + 2, 0.9)
        base = over(base, text_layer([("QUEBEC · MONTREAL", f_end2, (255, 220, 160, 255), (W/2, 450))], "ms"), al, dy)
        al, dy = appear(t, t0 + 2.2, t1 + 2, 0.9)
        base = over(base, text_layer([("2026. 11. 25 – 11. 29   ·   Bon voyage!", f_end3, (225, 230, 232, 255), (W/2, 500))], "ms"), al, dy)
        fo = ease((t - (t1 - 2.0)) / 2.0)
        if fo > 0:
            base = Image.blend(base, dark(), fo)
        return base

def frame(t):
    act = [s for s in S if s["t0"] <= t < s["t1"] + 0.6]
    act.sort(key=lambda s: s["t0"])
    out = None
    for s in act:
        im = render_ph(s, t) if s["k"] == "ph" else render_card(s, t)
        if out is None: out = im
        else:
            a = ease((t - s["t0"]) / 0.6)
            out = Image.blend(out, im, a) if a < 1 else im
    if out is None: out = dark()
    # last shot of each overlap is the newcomer; ensure old one fades only after its end
    return out.convert("RGB")

# fix overlaps: each shot persists 0.6s past its end so the next one cross-fades over it
for i, s in enumerate(S):
    nxt = S[i + 1]["t0"] if i + 1 < len(S) else DUR
    s["t1"] = max(s["t1"], nxt)  # hold until next starts

if PREVIEW:
    for sec in PREVIEW.split(","):
        frame(float(sec)).save(f"{OUT}_{sec}.png")
    sys.exit()

ff = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-i", WAV, "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
       "-c:a", "aac", "-b:a", "160k", "-shortest", OUT]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
nf = int(DUR * FPS)
for i in range(nf):
    pr.stdin.write(frame(i / FPS).tobytes())
    if i % 300 == 0: print(f"{i}/{nf}", flush=True)
pr.stdin.close(); pr.wait()
frame(60.2 + 3.5).save(OUT.replace(".mp4", "_poster.jpg"), quality=88)
print("done", OUT)
