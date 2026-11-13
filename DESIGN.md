# Design: chapter colour fields

Annual-report structure for a decision pack. Each slide has a full-height colour rail (440px) holding the logo and the slide's conclusion as its heading; the data sits on a warm grey page.

- **Rails by meaning:** navy for decisions, teal for usage and measures, saffron for peak, ink for machine resources, vermilion for risk.
- **Palette:** navy `#0A1F66`, teal `#0B6E6E`, saffron `#F2A900`, vermilion `#C8202B`, ink `#111A2E`, page `#F5F4EF`, with tints `#CFE7E3`, `#FCEBBB`, `#F8D9D4` for table states.
- **Type:** Bai Jamjuree for headings and numerals, Sarabun for body and tables. Tabular numerals in tables.
- **Structure:** hairline tables and stat rows instead of cards. No shadows, no gradients. Status always carries a word as well as a colour.
- **Interaction:** slides change from buttons and arrow keys only, so dragging selects text for copying.

## This deck (2026-11-13)
Inherited unchanged from `engenius-ai-capacity-deck`; added for round-based test reporting:
- **Round chart:** inline SVG on a 0–100 scale, teal bars, the latest round in saffron, a dashed outline labelled "รอผล" for a round without data. Value above the bar, `agree/n` under the round label.
- **Before/after table (`.ba`):** old value in vermilion, new value in teal, numerals in Bai Jamjuree.
- **Example table (`.ex`):** English sentence in Bai Jamjuree, old Thai in dark red, current Thai in dark teal.
- **Page fill:** body text 26–30px and table rows 24–34px padding so each slide fills 1920×1080 the way the approved pack does.
- **Data flow:** every round figure comes from `data/rounds.json`; `python src/build.py` regenerates both `index.html` (short, 8 slides) and `full.html` (long, 16 slides).
