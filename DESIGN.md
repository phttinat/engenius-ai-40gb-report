# Design: clean editorial magazine

Weekly AI test update for a manager, set like a business-magazine issue. Chosen by Adam on 2026-11-13 after he rejected the grey decision-pack rails and then the Memphis candy palette ("ไม่ชอบสี").

- **Paper:** white pages (`#FFFFFF`), ink `#121212`, secondary text `#4A4A4A`/`#7A7A7A`, hairlines `#DCDCDC`, soft fill `#F3F3F1`. Two slides per deck turn inverse (ink ground, white type) for rhythm.
- **One accent:** Engenius red `#D0021B` only: the latest figure, the headline rule, step numbers, "after" numbers, high-risk status. Nothing else is coloured.
- **Type:** Trirong (serif) for headlines and every large figure, italic Trirong for English example sentences; Noto Sans Thai for body, tables and labels. Headlines 62px, cover 118px, body 28–30px, comparison figures 220px.
- **Folio:** every page carries a running head ("Engenius AI · ผลทดสอบเครื่อง 40GB") with a hairline and the page number top right; each headline ends in a 120×6px red rule.
- **No boxes:** content sits on the page; columns are split by hairlines and a 2px ink top rule, never cards, shadows or outlines.
- **Status:** a word with a small dot (red สูง, amber กลาง, grey ต่ำ). Before numbers are struck through in red, after numbers are red.
- **Chart:** graphite bars on a 0–100 scale with hairline gridlines, the latest round red, a round still being tested hatched and dashed.
- **Language:** semi-formal Thai, short sentences, no kicker labels.
- **Data flow:** `data/rounds.json` → `python src/build.py` → `index.html` (8 slides) and `full.html` (16 slides).
