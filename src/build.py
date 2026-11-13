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


def chart(w=1640, h=640):
    """Agreement per round on a 0-100 scale: mint blocks with ink outlines, the latest round pink,
    a striped outline for a round still being tested."""
    pad_l, pad_b, top = 70, 86, 56
    n = len(rounds); slot = (w - pad_l) / n; bw = slot * 0.6
    y = lambda v: top + (h - top - pad_b) * (1 - v / 100)
    o = [f'<svg class="rchart" viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="ร้อยละของข้อที่ AI ตรวจถูก แยกตามรอบทดสอบ">'
         '<defs><pattern id="hatch" width="22" height="22" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
         '<rect width="22" height="22" fill="#F3F3F1"/><rect width="4" height="22" fill="#121212" opacity=".25"/></pattern></defs>']
    for g in (0, 25, 50, 75, 100):
        o.append(f'<line x1="{pad_l}" x2="{w}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="{"#121212" if g == 0 else "#DCDCDC"}" stroke-width="{2 if g == 0 else 1}"/>'
                 f'<text x="{pad_l - 14}" y="{y(g) + 8:.1f}" text-anchor="end" class="ax">{g}</text>')
    for i, r in enumerate(rounds):
        x = pad_l + i * slot + (slot - bw) / 2; cx = x + bw / 2
        if r.get("n"):
            v = pct(r); col = "#D0021B" if r is last else "#2B2B2B"
            o.append(f'<rect x="{x:.1f}" y="{y(v):.1f}" width="{bw:.1f}" height="{y(0) - y(v):.1f}" fill="{col}"/>'
                     f'<text x="{cx:.1f}" y="{y(v) - 14:.1f}" text-anchor="middle" class="val">{fmt1(v)}</text>')
            sub = f'{r["agree"]:,}/{r["n"]:,}'
        else:
            o.append(f'<rect x="{x:.1f}" y="{y(100):.1f}" width="{bw:.1f}" height="{y(0) - y(100):.1f}" fill="url(#hatch)" stroke="#7A7A7A" stroke-width="2" stroke-dasharray="10 8"/>'
                     f'<text x="{cx:.1f}" y="{y(55):.1f}" text-anchor="middle" class="wait">กำลัง</text><text x="{cx:.1f}" y="{y(55) + 32:.1f}" text-anchor="middle" class="wait">ทดสอบ</text>')
            sub = "&#160;"
        o.append(f'<text x="{cx:.1f}" y="{h - 44}" text-anchor="middle" class="rn">รอบ {r["round"]}</text>'
                 f'<text x="{cx:.1f}" y="{h - 12}" text-anchor="middle" class="sub2">{sub}</text>')
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
        res = f'{fmt1(pct(r))}%<span class="small">{r["agree"]}/{r["n"]}</span>' if r.get("n") else 'กำลังทดสอบ'
        out.append(f'<tr><td class="n">{r["round"]}</td><td>{r["scope"]}</td><td class="r"><b class="num" style="font-size:40px">{res}</b></td>'
                   f'<td>{r.get("finding") or "รอผล"}</td></tr>')
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
            out.append(f'<tr><td>รอบ {r["round"]}</td><td class="r" colspan="4">กำลังทดสอบ</td></tr>')
    return "".join(out)


# cumulative problem tally (data["problems"]) when present; else the latest round's recheck block
pb = data.get("problems")
rc = ({"items": pb["reported"], "fixed": pb["fixed"], "stillWrong": pb["thai"], "asr": pb["asr"],
       "policy": pb["policy"], "content": pb["content"], "new": pb.get("notRechecked", 0)}
      if pb else (last.get("recheck") or {}))
pending = [r for r in rounds if not r.get("n")]
fresh = last.get("fresh") or {}
TOKENS = {
    "{{CHART}}": chart(),
    "{{ROUND_ROWS}}": round_rows(),
    "{{DETAIL_A}}": detail_rows(1, 5),
    "{{DETAIL_B}}": detail_rows(6, 99),
    "{{NEXT_ROUND}}": str(pending[0]["round"] if pending else last["round"] + 1),
    "{{RC_CONFIRMED}}": str((pb or {}).get("confirmed", "-")), "{{RC_PENDING}}": str((pb or {}).get("pending", "-")),
    "{{FRESH_AGREE}}": str(fresh.get("agree", "-")), "{{FRESH_N}}": str(fresh.get("n", "-")),
    "{{FRESH_PCT}}": fmt1(100.0 * fresh["agree"] / fresh["n"]) if fresh.get("n") else "-",
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

EXTRA_CSS = "span.en{font-family:var(--display);font-style:italic;font-size:1.05em}"


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
