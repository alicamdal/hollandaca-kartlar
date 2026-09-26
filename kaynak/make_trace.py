import os, math, random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, black
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Group
from svglib.svglib import svg2rlg
from HersheyFonts import HersheyFonts

HERE = os.path.dirname(os.path.abspath(__file__))
pdfmetrics.registerFont(TTFont("Hand", f"{HERE}/fonts/Kalam-Regular.ttf"))
pdfmetrics.registerFont(TTFont("HandB", f"{HERE}/fonts/Kalam-Bold.ttf"))
INK = black
GUIDE = HexColor("#8a8a8a")
GUIDE_L = HexColor("#bdbdbd")
random.seed(3)

HF = HersheyFonts()
HF.load_default_font("futural")
HF.normalize_rendering(100)
# metrics at h=100: baseline 36.36, x-height top 63.64, ascender 100, descender 0
BASE, XTOP, ASC = 25.0, 75.0, 100.0
ASC_K = (ASC - BASE) / 100

W, H = A4
M = 40

# ---------------------------------------------------------------- content
# (turkish, dutch, pic)  pic: OpenMoji code | ("color",) | ("num","7") | None
TOPICS = [
    ("Vücudum", "Mijn lichaam", [
        ("baş", "het hoofd", "1F642"), ("saç", "het haar", "1F471"),
        ("göz", "het oog", "1F441"), ("kulak", "het oor", "1F442"),
        ("burun", "de neus", "1F443"), ("ağız", "de mond", "1F444"),
        ("diş", "de tand", "1F9B7"), ("dil", "de tong", "1F60B"),
        ("el", "de hand", "270B"), ("parmak", "de vinger", "261D"),
        ("kol", "de arm", "1F4AA"), ("karın", "de buik", None),
        ("bacak", "het been", "1F9B5"), ("ayak", "de voet", "1F9B6"),
    ]),
    ("Renkler", "Kleuren", [
        ("kırmızı", "rood", ("color",)), ("mavi", "blauw", ("color",)),
        ("sarı", "geel", ("color",)), ("yeşil", "groen", ("color",)),
        ("turuncu", "oranje", ("color",)), ("mor", "paars", ("color",)),
        ("pembe", "roze", ("color",)), ("kahverengi", "bruin", ("color",)),
        ("siyah", "zwart", ("color",)), ("beyaz", "wit", ("color",)),
        ("gri", "grijs", ("color",)),
    ]),
    ("Günler", "De dagen", [
        ("pazartesi", "maandag", None), ("salı", "dinsdag", None),
        ("çarşamba", "woensdag", None), ("perşembe", "donderdag", None),
        ("cuma", "vrijdag", None), ("cumartesi", "zaterdag", None),
        ("pazar", "zondag", None),
    ]),
    ("Sayılar", "Getallen", [(tr, nl, ("num", str(i + 1))) for i, (tr, nl) in enumerate([
        ("bir", "een"), ("iki", "twee"), ("üç", "drie"), ("dört", "vier"), ("beş", "vijf"),
        ("altı", "zes"), ("yedi", "zeven"), ("sekiz", "acht"), ("dokuz", "negen"), ("on", "tien"),
        ("on bir", "elf"), ("on iki", "twaalf"), ("on üç", "dertien"), ("on dört", "veertien"),
        ("on beş", "vijftien"), ("on altı", "zestien"), ("on yedi", "zeventien"),
        ("on sekiz", "achttien"), ("on dokuz", "negentien"), ("yirmi", "twintig"),
    ])]),
    ("Hayvanlar", "Dieren", [
        ("kedi", "de kat", "1F431"), ("köpek", "de hond", "1F436"),
        ("kuş", "de vogel", "1F426"), ("balık", "de vis", "1F41F"),
        ("at", "het paard", "1F434"), ("inek", "de koe", "1F42E"),
        ("koyun", "het schaap", "1F411"), ("tavşan", "het konijn", "1F430"),
        ("ördek", "de eend", "1F986"), ("tavuk", "de kip", "1F414"),
        ("fare", "de muis", "1F42D"), ("kurbağa", "de kikker", "1F438"),
        ("kelebek", "de vlinder", "1F98B"), ("aslan", "de leeuw", "1F981"),
        ("fil", "de olifant", "1F418"), ("maymun", "de aap", "1F435"),
        ("ayı", "de beer", "1F43B"), ("zürafa", "de giraf", "1F992"),
    ]),
    ("Ailem", "Mijn familie", [
        ("anne", "mama", "1F469"), ("baba", "papa", "1F468"),
        ("erkek kardeş", "de broer", "1F466"), ("kız kardeş", "de zus", "1F467"),
        ("dede", "opa", "1F474"), ("nine", "oma", "1F475"),
        ("bebek", "de baby", "1F476"), ("çocuk", "het kind", "1F9D2"),
        ("oğlan", "de jongen", "1F466"), ("kız", "het meisje", "1F467"),
        ("arkadaş", "de vriend", "1F91D"),
        ("öğretmen (kadın)", "de juf", "1F469-200D-1F3EB"),
        ("öğretmen (erkek)", "de meester", "1F468-200D-1F3EB"),
    ]),
    ("Yiyecekler", "Eten en drinken", [
        ("elma", "de appel", "1F34E"), ("muz", "de banaan", "1F34C"),
        ("armut", "de peer", "1F350"), ("çilek", "de aardbei", "1F353"),
        ("üzüm", "de druif", "1F347"), ("portakal", "de sinaasappel", "1F34A"),
        ("karpuz", "de watermeloen", "1F349"), ("havuç", "de wortel", "1F955"),
        ("ekmek", "het brood", "1F35E"), ("peynir", "de kaas", "1F9C0"),
        ("yumurta", "het ei", "1F95A"), ("süt", "de melk", "1F95B"),
        ("su", "het water", "1F4A7"), ("dondurma", "het ijsje", "1F366"),
        ("kurabiye", "het koekje", "1F36A"), ("domates", "de tomaat", "1F345"),
    ]),
    ("Okulda", "Op school", [
        ("okul", "de school", "1F3EB"), ("sınıf", "de klas", "1F9D1-200D-1F3EB"),
        ("kitap", "het boek", "1F4D5"), ("kurşun kalem", "het potlood", "270F"),
        ("boya kalemi", "het kleurpotlood", "1F58D"), ("kağıt", "het papier", "1F4C4"),
        ("makas", "de schaar", "2702"), ("çanta", "de tas", "1F392"),
        ("sandalye", "de stoel", "1FA91"), ("top", "de bal", "26BD"),
        ("oyuncak", "het speelgoed", "1F9F8"), ("tuvalet", "de wc", "1F6BD"),
    ]),
    ("Konuşalım", "Korte zinnen", [
        ("Merhaba", "Hallo", "1F44B"), ("Günaydın", "Goedemorgen", "1F305"),
        ("Hoşça kal", "Doei", "1F44B"), ("Teşekkür ederim", "Dank je wel", "1F64F"),
        ("Lütfen / Buyrun", "Alsjeblieft", None), ("Evet", "Ja", None),
        ("Hayır", "Nee", None), ("Özür dilerim", "Sorry", None),
        ("Benim adım Ömer", "Ik heet Ömer", None), ("Acıktım", "Ik heb honger", "1F37D"),
        ("Susadım", "Ik heb dorst", "1F964"),
        ("Tuvalete gidebilir miyim?", "Mag ik naar de wc?", "1F6BD"),
        ("Ben de oynayabilir miyim?", "Mag ik meespelen?", "26BD"),
        ("Bana yardım eder misin?", "Kun je me helpen?", None),
        ("Anlamadım", "Ik begrijp het niet", "1F914"),
    ], "stack"),
]

# ---------------------------------------------------------------- helpers
def split_article(nl):
    for a in ("de ", "het "):
        if nl.startswith(a):
            return a.strip(), nl[len(a):]
    return "", nl

def chaikin(pts, it=2):
    for _ in range(it):
        if len(pts) < 3:
            return pts
        out = [pts[0]]
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            out.append((0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1))
            out.append((0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1))
        out.append(pts[-1])
        pts = out
    return pts

UMLAUT = {"Ö": "O", "ö": "o", "Ü": "U", "ü": "u", "ë": "e", "ï": "i", "é": "e"}

def script_strokes(text, marks=None):
    base = "".join(UMLAUT.get(ch, ch) for ch in text)
    strokes = [list(s) for s in HF.strokes_for_text(base)]
    if marks is not None:
        for i, ch in enumerate(text):
            if ch in UMLAUT:
                n0 = len(list(HF.strokes_for_text(base[:i])))
                n1 = len(list(HF.strokes_for_text(base[:i + 1])))
                glyph = strokes[n0:n1]
                xs = [x for st in glyph for x, _ in st]
                ys = [y for st in glyph for _, y in st]
                cx, top = (min(xs) + max(xs)) / 2, max(ys)
                if ch == "é":
                    marks.append(("acute", cx, top))
                else:
                    marks.append(("dots", cx, top))
    return strokes

def script_width(text, h):
    xs = [x for s in script_strokes(text) for x, _ in s]
    return (max(xs) - min(xs)) * h / 100 if xs else 0

def draw_dotted(c, text, x, baseline, h, spacing=None, r=None):
    """Draw text in single-stroke cursive as dots. h = full glyph height (desc..asc)."""
    k = h / 100.0
    spacing = spacing or 4.0
    r = r or 1.15
    c.setFillColor(INK)
    marks = []
    strokes = script_strokes(text, marks)
    minx = min(px for s in strokes for px, _ in s)
    for kind, mx, top in marks:
        X = x + (mx - minx) * k
        Y = baseline + (top - BASE) * k + 0.13 * h
        if kind == "dots":
            for dx in (-0.1 * h, 0.1 * h):
                c.circle(X + dx, Y, r * 1.7, stroke=0, fill=1)
    for s in strokes:
        pts = [(x + (px - minx) * k, baseline + (py - BASE) * k) for px, py in s]
        pts = chaikin(pts)
        # resample along the polyline
        acc = 0.0
        c.circle(pts[0][0], pts[0][1], r, stroke=0, fill=1)
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            seg = math.hypot(x1 - x0, y1 - y0)
            d = spacing - acc
            while d <= seg:
                t = d / seg
                c.circle(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, stroke=0, fill=1)
                d += spacing
            acc = seg - (d - spacing)
        c.circle(pts[-1][0], pts[-1][1], r, stroke=0, fill=1)

def guides(c, x1, x2, baseline, h):
    k = h / 100.0
    c.saveState()
    c.setLineCap(1)
    # baseline
    c.setStrokeColor(GUIDE)
    c.setLineWidth(0.9)
    c.line(x1, baseline, x2, baseline)
    # x-height (dashed)
    c.setStrokeColor(GUIDE_L)
    c.setLineWidth(0.7)
    c.setDash(3, 3)
    c.line(x1, baseline + (XTOP - BASE) * k, x2, baseline + (XTOP - BASE) * k)
    # ascender (thin)
    c.setDash()
    c.setLineWidth(0.5)
    c.line(x1, baseline + (ASC - BASE) * k, x2, baseline + (ASC - BASE) * k)
    c.restoreState()

def hand_line(c, x1, y, x2, width=1.6):
    c.setLineWidth(width)
    c.setStrokeColor(INK)
    c.setLineCap(1)
    p = c.beginPath()
    j = lambda a: random.uniform(-a, a)
    p.moveTo(x1, y + j(0.8))
    p.curveTo(x1 + (x2 - x1) * .35, y + j(1.2), x1 + (x2 - x1) * .7, y + j(1.2), x2, y + j(.8))
    c.drawPath(p, stroke=1, fill=0)

_svg_cache = {}
def thicken(node, f):
    if hasattr(node, "strokeWidth") and node.strokeWidth:
        node.strokeWidth *= f
    for ch in getattr(node, "contents", []) or []:
        thicken(ch, f)

def draw_pic(c, pic, cx, cy, size):
    if pic is None:
        return
    if pic[0] == "color":
        c.setStrokeColor(INK)
        c.setLineWidth(1.8)
        c.setFillColor(HexColor("#ffffff"))
        c.circle(cx, cy, size * 0.42, stroke=1, fill=0)
        return
    if pic[0] == "num":
        fs = size * 0.85
        c.saveState()
        t = c.beginText()
        t.setTextRenderMode(1)
        t.setFont("HandB", fs)
        c.setStrokeColor(INK)
        c.setLineWidth(1.5)
        w = pdfmetrics.stringWidth(pic[1], "HandB", fs)
        t.setTextOrigin(cx - w / 2, cy - fs * 0.33)
        t.textOut(pic[1])
        c.drawText(t)
        c.restoreState()
        return
    d = svg2rlg(f"{HERE}/ol/{pic}.svg")
    thicken(d, 1.45)
    s = size / d.width
    d.scale(s, s)
    renderPDF.draw(d, c, cx - size / 2, cy - size / 2)

# ---------------------------------------------------------------- layout
GH = 44          # cursive glyph height (x-height ~12pt)
TR_FS = 21
PIC = 66
PIC_COL = 74

BASE_URL = "https://alicamdal.github.io/hollandaca-kartlar/"
import qrcode, io, json
from reportlab.lib.utils import ImageReader

def draw_qr(c, num):
    q = qrcode.QRCode(border=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=10)
    q.add_data(f"{BASE_URL}?s={num}")
    q.make(fit=True)
    img = q.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    sz = 62
    x, y = W - M - sz, H - M - sz + 14
    c.drawImage(ImageReader(buf), x, y, sz, sz)
    c.setFillColor(INK)
    c.setFont("Hand", 10)
    c.drawCentredString(x + sz / 2, y - 10, "luister / dinle")

def header(c, tr, nl, num, cont):
    draw_qr(c, num)
    c.setFillColor(INK)
    c.setFont("HandB", 30)
    t = f"{tr}  ~  {nl}"
    c.drawString(M + 4, H - M - 26, t)
    hand_line(c, M + 4, H - M - 34, M + 10 + pdfmetrics.stringWidth(t, "HandB", 30), 2.2)
    c.setFont("Hand", 9)
    c.setFillColor(HexColor("#666666"))
    c.drawCentredString(W / 2, M - 18, str(num))
    c.drawRightString(W - M, M - 18, "Resimler: OpenMoji (CC BY-SA 4.0)")

def row_side(c, entry, top, xt, gh):
    """Turkish word ---- [article] dotted word ; practice line underneath."""
    tr, nl, pic = entry
    b1 = top - ASC_K * gh - 14   # tracing baseline
    b2 = b1 - gh - 20            # practice baseline
    draw_pic(c, pic, M + PIC_COL / 2 - 6, (b1 + b2) / 2 + 10, PIC)
    c.setFillColor(INK)
    c.setFont("Hand", TR_FS)
    tx = M + PIC_COL
    c.drawString(tx, b1, tr)
    dx = tx + pdfmetrics.stringWidth(tr, "Hand", TR_FS) + 8
    hand_line(c, dx, b1 + 8, max(dx + 22, xt - 12))
    art, word = split_article(nl)
    for b in (b1, b2):
        guides(c, xt, W - M, b, gh)
        ax = xt + 4
        if art:
            c.setFillColor(INK)
            c.setFont("Hand", TR_FS)
            c.drawString(ax, b, art)
            ax += pdfmetrics.stringWidth(art, "Hand", TR_FS) + 10
        if b == b1:
            draw_dotted(c, word, ax, b1, gh)

def row_stack(c, entry, top, gh):
    tr, nl, pic = entry
    b0 = top - 22            # turkish line
    b1 = b0 - ASC_K * gh - 14    # tracing
    b2 = b1 - gh - 20            # practice
    draw_pic(c, pic, M + PIC_COL / 2 - 6, (b1 + b2) / 2 + 10, PIC)
    xt = M + PIC_COL
    c.setFillColor(INK)
    c.setFont("Hand", TR_FS)
    c.drawString(xt, b0, tr)
    tw = pdfmetrics.stringWidth(tr, "Hand", TR_FS)
    hand_line(c, xt + tw + 8, b0 + 8, xt + tw + 38)
    for b in (b1, b2):
        guides(c, xt, W - M, b, gh)
    draw_dotted(c, nl, xt + 4, b1, gh)

def chunks(lst, per):
    n = math.ceil(len(lst) / per)
    size = math.ceil(len(lst) / n)
    return [lst[i:i + size] for i in range(0, len(lst), size)]

out = f"{HERE}/out/Flemenkce_Noktali_Boyama.pdf"
c = canvas.Canvas(out, pagesize=A4)
c.setTitle("Türkçe – Nederlands: noktalı yazma ve boyama")
page = 0
EXPORT = []
for topic in TOPICS:
    tr_t, nl_t, entries = topic[:3]
    mode = topic[3] if len(topic) > 3 else "side"
    per = 4 if mode == "stack" else 5
    step = (H - M - 58 - (M + 10)) / per
    def xt_for(group):
        return M + PIC_COL + max(pdfmetrics.stringWidth(e[0], "Hand", TR_FS) for e in group) + 44
    groups = chunks(entries, per)
    gh = GH
    for g in groups:
        for e in g:
            if mode == "side":
                art, word = split_article(e[1])
                aw = (pdfmetrics.stringWidth(art, "Hand", TR_FS) + 10) if art else 0
                avail = W - M - xt_for(g) - 8 - aw
            else:
                word, avail = e[1], W - M - (M + PIC_COL) - 10
            while script_width(word, gh) > avail and gh > 22:
                gh -= 1
    for ci, ch in enumerate(groups):
        page += 1
        header(c, tr_t, nl_t, page, ci > 0)
        EXPORT.append({"page": page, "tr": tr_t, "nl": nl_t, "stack": mode == "stack",
                       "items": [{"tr": e[0], "nl": e[1],
                                  "pic": (e[2] if isinstance(e[2], str) else (list(e[2]) if e[2] else None))}
                                 for e in ch]})
        top = H - M - 58
        xt = xt_for(ch)
        for i, e in enumerate(ch):
            if mode == "side":
                row_side(c, e, top - i * step, xt, gh)
            else:
                row_stack(c, e, top - i * step, gh)
        c.showPage()
c.save()
json.dump(EXPORT, open(f"{HERE}/out/pages.json", "w"), ensure_ascii=False, indent=1)
print("pages", page, out)
