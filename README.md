# TCG Coming Soon: Handoff Package

The Concrete Group · single-page coming-soon build · September 28, 2026

## How to use

1. Unzip at the root of an empty repo.
2. Open Claude Code in that folder.
3. Paste the fenced block from `CLAUDE_CODE_PROMPT.md`.
4. Output lands in `/dist`.

## Contents

```
CLAUDE_CODE_PROMPT.md        build prompt (starts at build; media is final)
brand-assets/
  TCG_Logo_Main.png          approved ring mark, ink #484848, 900x967, transparent
  TCG_Logo_Reverse.png       approved ring mark, off-white reverse, 900x967, transparent
assets/video/
  hero_16x9.mp4              desktop loop, 1920x1080, 30.000s, H.264 High, 7.4 MB
  hero_9x16.mp4              mobile loop, 720x1280, 30.000s, H.264 High, 3.4 MB
assets/img/
  poster_16x9.jpg            frame 0 of desktop loop
  poster_9x16.jpg            frame 0 of mobile loop
  og-image.jpg               1200x630 social card
tools/                       Python/OpenCV scripts used for motion QA and retime (for future re-cuts only)
  flow.py                    optical-flow speed profile per 2s window
  retime_chunk.py            constant-speed retime with motion-compensated interpolation
  seam.py                    loop-seam check (seam step vs typical frame step)
review/
  contact_sheet_final.png    final frames, both ratios, plus a shadow-detail crop
```

The 1080p high-quality masters (`tcg_hero_16x9_MASTER.mp4`, `tcg_hero_9x16_MASTER.mp4`, ~30 MB each) were delivered separately. Keep them for decks, social cutdowns or future re-encodes.

## Footage provenance

| | Desktop | Mobile |
|---|---|---|
| Source | Higgsfield Seedance 2.5, 30s, 1080p, omni-reference to approved draft | Higgsfield Seedance 2.5, 30s, 1080p, omni-reference to approved draft |
| Job ID | 2e090932-50f1-45df-8c00-18085d4a5616 | a3308aec-e733-4849-a208-75b28c5dbae0 |
| Approved draft | 09a7b5a5-ebbd-454c-9237-4a7c5e3b1c6e | 17d74efc-4e73-4b79-b5d1-83b95eb28463 |
| Post | Trimmed to 0–22.75s (hard cut at 22.9s removed), retimed to constant speed with motion-compensated interpolation | Retimed to constant speed |
| Loop | 1 × 1.0s crossfade seam, 30.000s | 1 × 1.0s crossfade seam, 30.000s |
| Measured speed variance | ±5% (raw render swung ~4x) | ±4% (raw render swung ~3x) |

Seedance ramps speed over long durations and returned HEVC. Any future footage needs the same measure → retime → loop → H.264 pass before it goes on the web.

## Open items (need a human decision)

- **[RATIFY] Status line.** Default "NOW SETTING." Alternates: "CURRENTLY CURING." / "THE POUR IS UNDERWAY."
- **[RATIFY] Meta description.** Placeholder in the prompt.
- **Domain.** The build uses theconcretegrp.com (canonical) throughout. The theconcretegrp.com vs theconcretegroup.com inconsistency is still unresolved; confirm before DNS and launch.
- **Desktop weight.** hero_16x9.mp4 is 7.4 MB against an original ≤6 MB target. It was held on purpose: at 6 MB the shadows block up. The poster paints first, so perceived load is unaffected.
