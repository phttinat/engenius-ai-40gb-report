"""Build index.html (short deck) and full.html (long deck) from src/ and data/rounds.json.

    python src/build.py      (run from anywhere)

To add a round: append it to data/rounds.json (n, agree, ratings, scope, finding, fix) and rebuild.
Every chart and table that lists rounds is generated from that file; slide text that quotes a single
round's numbers uses the {{...}} tokens below, so nothing in the slides needs hand editing.
"""
import json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data/rounds.json").read_text(encoding="utf-8"))
rounds = data["rounds"]
done = [r for r in rounds if r.get("n")]
last = done[-1]
pct = lambda r: 100.0 * r["agree"] / r["n"]
fmt1 = lambda x: f"{x:.1f}".replace(".0", "") if abs(x - round(x)) < 0.05 else f"{x:.1f}"
MK = ' class="mark"'
mean3 = lambda r: sum(r["ratings"].values()) / 3


def chart(w=1330, h=780):
    """Agreement per round, 0-100 scale. Latest round in saffron, rounds without data dashed."""
    pad_l, pad_b, top = 64, 74, 46
    n = len(rounds); slot = (w - pad_l) / n; bw = slot * 0.56
    y = lambda v: top + (h - top - pad_b) * (1 - v / 100)
    o = [f'<svg class="rchart" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="ร้อยละที่ผู้ทดสอบเห็นด้วยกับผลของ AI รายรอบ">']
    for g in (0, 25, 50, 75, 100):
        o.append(f'<line x1="{pad_l}" x2="{w}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="{"#111A2E" if g == 0 else "#D9D8D0"}" stroke-width="{3 if g == 0 else 1}"/>'
                 f'<text x="{pad_l - 12}" y="{y(g) + 8:.1f}" text-anchor="end" class="ax">{g}</text>')
    for i, r in enumerate(rounds):
        x = pad_l + i * slot + (slot - bw) / 2; cx = x + bw / 2
        if r.get("n"):
            v = pct(r); col = "#F2A900" if r is last else "#0B6E6E"
            o.append(f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{y(0) - y(v):.1f}" fill="{col}"/>'
                     f'<text x="{cx:.1f}" y="{y(v) - 12:.1f}" text-anchor="middle" class="val">{fmt1(v)}</text>')
            sub = f'{r["agree"]:,}/{r["n"]:,}'
        else:
            o.append(f'<rect x="{x:.1f}" y="{y(100):.1f}" width="{bw:.1f}" height="{y(0) - y(100):.1f}" fill="none" stroke="#626B7C" stroke-width="2" stroke-dasharray="8 7"/>'
                     f'<text x="{cx:.1f}" y="{y(50):.1f}" text-anchor="middle" class="wait">รอผล</text>')
            sub = "&#160;"
        o.append(f'<text x="{cx:.1f}" y="{h - 40}" text-anchor="middle" class="rn">รอบ {r["round"]}</text>'
                 f'<text x="{cx:.1f}" y="{h - 8}" text-anchor="middle" class="sub">{sub}</text>')
    o.append("</svg>")
    return "".join(o)


def round_rows():
    out = []
    for r in rounds:
        if r.get("n"):
            out.append(f'<tr{MK if r is last else ""}><td>รอบ {r["round"]}</td><td>{r["date"]}</td>'
                       f'<td class="r">{r["n"]:,}</td><td class="r">{r["agree"]:,}</td><td class="r">{fmt1(pct(r))}</td></tr>')
        else:
            out.append(f'<tr><td>รอบ {r["round"]}</td><td>{r["date"]}</td><td class="r">รอผล</td><td class="r">รอผล</td><td class="r">รอผล</td></tr>')
    return "".join(out)


def detail_rows(lo, hi):
    out = []
    for r in rounds:
        if not lo <= r["round"] <= hi:
            continue
        res = f'{fmt1(pct(r))}<small>{r["agree"]}/{r["n"]}</small>' if r.get("n") else "รอผล"
        out.append(f'<tr><td class="n">{r["round"]}</td><td>{r["scope"]}</td><td class="r big">{res}</td>'
                   f'<td>{r.get("finding") or "รอผลวิเคราะห์"}</td><td>{r.get("fix") or "รอผลวิเคราะห์"}</td></tr>')
    return "".join(out)


def ratings_rows():
    out = []
    for r in rounds:
        if r["round"] < 6:
            continue
        if r.get("ratings"):
            t = r["ratings"]
            out.append(f'<tr{MK if r is last else ""}><td>รอบ {r["round"]}</td><td class="r">{t["heard"]:.2f}</td>'
                       f'<td class="r">{t["thai"]:.2f}</td><td class="r">{t["tip"]:.2f}</td><td class="r"><b>{mean3(r):.2f}</b></td></tr>')
        else:
            out.append(f'<tr><td>รอบ {r["round"]}</td><td class="r" colspan="4">รอผล</td></tr>')
    return "".join(out)


rc = last.get("recheck") or {}
TOKENS = {
    "{{CHART}}": chart(),
    "{{ROUND_ROWS}}": round_rows(),
    "{{DETAIL_A}}": detail_rows(1, 5),
    "{{DETAIL_B}}": detail_rows(6, 99),
    "{{RATINGS_ROWS}}": ratings_rows(),
    "{{TOTAL_N}}": f'{sum(r["n"] for r in done):,}',
    "{{N_ROUNDS}}": str(len(done)),
    "{{FIRST_PCT}}": f"{pct(done[0]):.0f}",
    "{{BEST_PCT}}": f"{max(pct(r) for r in done):.0f}",
    "{{LAST_ROUND}}": str(last["round"]),
    "{{LAST_PCT}}": fmt1(pct(last)),
    "{{LAST_AGREE}}": f'{last["agree"]:,}', "{{LAST_N}}": f'{last["n"]:,}',
    "{{LAST_MEAN}}": f"{mean3(last):.2f}" if last.get("ratings") else "-",
    "{{RC_ITEMS}}": str(rc.get("items", "-")), "{{RC_FIXED}}": str(rc.get("fixed", "-")),
    "{{RC_WRONG}}": str(rc.get("stillWrong", "-")), "{{RC_ASR}}": str(rc.get("asr", "-")),
    "{{RC_POLICY}}": str(rc.get("policy", "-")), "{{RC_CONTENT}}": str(rc.get("content", "-")), "{{RC_NEW}}": str(rc.get("new", "-")),
}

EXTRA_CSS = """
/* round chart and report additions (2026-11-13) */
.rchart .ax{font:500 22px 'Bai Jamjuree',sans-serif;fill:#626B7C}.rchart .val{font:700 34px 'Bai Jamjuree',sans-serif;fill:#111A2E}
.rchart .rn{font:600 25px 'Bai Jamjuree',sans-serif;fill:#111A2E}.rchart .sub{font:500 21px 'Sarabun',sans-serif;fill:#626B7C}.rchart .wait{font:600 26px 'Sarabun',sans-serif;fill:#626B7C}
.ba td{font-size:25px;padding:14px 12px}.ba td.r{font:700 34px 'Bai Jamjuree',sans-serif}.ba td.was{color:var(--red)}.ba td.now{color:var(--teal)}
.detail td{font-size:22px;padding:13px 10px;vertical-align:top;line-height:1.38}.detail th{font-size:20px}.detail td.n{font:700 40px/1 'Bai Jamjuree',sans-serif;color:var(--teal)}
.detail td.big{font:700 32px/1.1 'Bai Jamjuree',sans-serif;color:var(--navy)}.detail td.big small{display:block;font:500 19px 'Sarabun',sans-serif;color:var(--ink3);margin-top:4px}
.ex td{font-size:23px;padding:12px 10px;line-height:1.36;vertical-align:top}.ex td.en{font-family:'Bai Jamjuree',sans-serif;font-weight:500}.ex td.was{color:#94151E}.ex td.now{color:#075353}
.split{display:grid;grid-template-columns:1fr 1fr;gap:44px;flex:1;min-height:0}.split>div{display:flex;flex-direction:column;gap:14px;min-height:0}
.lead{font-size:27px;line-height:1.45;color:var(--ink2)}
.navlink{font:600 15px 'Sarabun',sans-serif}
/* page fill: tables and text grow into the slide like the approved decision pack */
.ba td{font-size:30px;padding:30px 14px}.ba td.r{font-size:46px}.ba th{font-size:23px}
.detail td{font-size:25px;padding:24px 12px}.detail th{font-size:22px}.detail td.n{font-size:50px}.detail td.big{font-size:38px}.detail td.big small{font-size:21px}
.ex td{font-size:28px;padding:24px 12px}.ex th{font-size:23px}
.measures td{font-size:26px;padding:24px 12px;line-height:1.4}.measures th{font-size:23px}
.lead{font-size:30px;line-height:1.5}
.split td{font-size:28px;padding:20px 12px}.split th{font-size:23px}.split h3{font-size:31px;margin-top:8px}.split .note{font-size:24px}
.risk td{padding:30px 14px}
.body.row>div:first-child table td{font-size:30px;padding:26px 12px}.body.row>div:first-child table th{font-size:23px}
.def dt{font-size:31px;padding:24px 0}.def dd{font-size:29px;padding:24px 0;line-height:1.5}
.detail td{padding:34px 12px}.ex td{padding:30px 12px}.split td{padding:26px 12px}
.body.row .block.sun{align-self:start}
.cap-chart .hb{min-height:70px}.cap-chart .hb label{font-size:28px}.cap-chart .hb b{font-size:32px}
"""


def build(src, out, title, other_href, other_label):
    shell = (ROOT / "src/shell.html").read_text(encoding="utf-8")
    slides = (ROOT / src).read_text(encoding="utf-8")
    for k, v in TOKENS.items():
        slides = slides.replace(k, v)
    n = [1]
    slides = re.sub(r"\{\{PG\}\}", lambda m: (n.__setitem__(0, n[0] + 1), str(n[0]))[1], slides)
    left = re.findall(r"\{\{[A-Z_]+\}\}", slides)
    assert not left, f"unfilled tokens in {src}: {sorted(set(left))}"
    nav = (f'<a href="{other_href}">{other_label}</a>'
           f'<a class="main" href="https://github.com/phttinat/engenius-ai-40gb-report/blob/main/data/rounds.json" target="_blank" rel="noopener">ข้อมูลรายรอบ</a>')
    html = (shell.replace("{{TITLE}}", title).replace("{{EXTRA_CSS}}", EXTRA_CSS)
            .replace("{{NAVLINKS}}", nav).replace("<!--SLIDES-->", slides))
    (ROOT / out).write_text(html, encoding="utf-8", newline="\n")
    print(out, n[0], "slides")


build("src/short.html", "index.html", "Engenius AI · ผลการทดสอบบนเครื่อง 40GB (ฉบับย่อ)", "full.html", "ฉบับเต็ม")
build("src/long.html", "full.html", "Engenius AI · ผลการทดสอบบนเครื่อง 40GB (ฉบับเต็ม)", "index.html", "ฉบับย่อ")
