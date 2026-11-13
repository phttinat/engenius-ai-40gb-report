# Design: Memphis showroom update

Weekly AI test update for a manager. Chosen by Adam on 2026-11-13 after he rejected the grey decision-pack rails ("font ไม่สวย สีไม่สวย อ่านยาก น่าเบื่อ จำเจ").

- **Grounds:** every slide owns one flat laminate colour: pink `#FF4F9A`, mint `#3FDDB4`, yellow `#FFD23F`, cobalt `#2E44E6`, white. Neighbouring slides never share a ground. No gradients.
- **Textures:** terrazzo speckle, black squiggle, dot grid and diagonal stripe, drawn in CSS at low opacity behind content. Squiggle stays at 0.16 so text over it reads.
- **Objects:** content sits on white panels with a 4px ink outline and 22px corners. Each panel rests on an offset colour block of another hue (the Memphis layered-shape move, not a drop shadow).
- **Shapes:** circles, triangles, half-moons and squiggle lines in the slide margins only, never behind running text.
- **Type:** Kanit 700/800 for headings and numerals, Anuphan 400–700 for body. Body 30–32px, headings 66px, cover title 104px.
- **Status:** a word in a pill sticker (สูง coral, กลาง yellow, ต่ำ mint), never colour alone. Before/after numbers in deep pink and deep teal.
- **Chart:** mint blocks with ink outline on a 0–100 scale, the latest round pink, a round still being tested shown hatched and dashed with "กำลังทดสอบ".
- **Language:** semi-formal Thai, short sentences, no kicker labels above headings.
- **Data flow:** `data/rounds.json` → `python src/build.py` → `index.html` (7 slides) and `full.html` (15 slides).
