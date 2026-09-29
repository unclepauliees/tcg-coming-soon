# The Concrete Group: Coming Soon, handoff

Static, single file. Deploy the contents of `dist/` to the web root of `theconcretegrp.com`. No build step.

The host must support HTTP Range requests (Firebase Hosting, Netlify, Vercel, S3/CloudFront and nginx all do). Without them, the video can't seek, and the portrait/landscape swap restarts at 0s instead of keeping its place.

## File map (`dist/`)

```
index.html                     page: inline CSS + JS, Google Fonts only external dep
assets/video/hero_16x9.mp4     landscape loop (approved, byte-identical to source)
assets/video/hero_9x16.mp4     portrait loop (approved, byte-identical to source)
assets/img/poster_16x9.jpg     frame 0, landscape; painted as page background + preloaded
assets/img/poster_9x16.jpg     frame 0, portrait; painted as page background + preloaded
assets/img/og-image.jpg        social card (OG + Twitter)
assets/img/TCG_Logo_Reverse.png  header mark (approved, unmodified)
assets/img/favicon-32.png      from TCG_Logo_Main.png, uniform scale onto transparent square
assets/img/favicon-180.png     apple-touch-icon, same method
```

## [RATIFY] placeholders

| Item | Current value | Where to swap |
|---|---|---|
| Status line | `The Pour Is Underway` (renders uppercase; **ratified 2026-09-28**) | `index.html`: the `<p class="status">` |
| Meta description (revised 2026-09-29) | "The Concrete Group. Senior-led PR, communications and brand advisory. We build brands that last." | `index.html` `<head>`, 3 places: `meta name="description"`, `og:description`, `twitter:description` (marked with a comment). Page title: "The Concrete Group | PR & Brand Advisory" |

## Other open items

- **Contact address.** The mailto is `YourAgency@theconcretegrp.com`, built as written. It reads like a placeholder, so confirm the real inbox. Swap it in the `<a class="cta">` href.
- **Domain.** `theconcretegrp.com` is used in the canonical URL, OG/Twitter image URLs, the mailto and the footer. The grp/group spelling still needs a decision before DNS.
- **Desktop video weight.** 7.4 MB, held deliberately (see the package README).

## Deviations from the brief (made to pass QA)

1. **≤420px wide:** `CONCRETE` is `15.5vw` instead of the 4rem floor. At 4rem, Archivo Black with −.04em tracking is ~372px wide and overflows a 390px screen.
2. **Landscape phones (height ≤520px):** the lockup, gaps and bar padding scale with viewport height so the whole stack fits in 390px without colliding with the footer.
3. **Scrim additions:** two layers on top of the brief's .85→.35 ramp and the radial behind the lockup.
   - A bottom band (concrete-black .96 → 0 over 9rem). Without it, the 11px footer in `--n-400` failed 4.5:1 over specular highlights near the bottom of the landscape clip.
   - A soft radial behind the CTA block in landscape. Without it, the brass hover/focus text failed 4.5:1 at 1920×1080 (3.63).
4. **Grain overlay omitted.** I A/B'd an feTurbulence layer at .03 as a 1:1 crop at 1920×1080 over the poster (`qa/grain_ab.png`). The footage already carries its own surface grain. The overlay only adds a faint second texture in the flat shadows and reads as double grain, which is the brief's condition for removing it.
5. **Terminal dot is a 5px square.** "Radius 0 everywhere" allows only the pill to be round.

## QA results (2026-09-28)

**Contrast.** Measured against the p99 (brightest) pixel under each element's box. Samples: the 3 brightest frames by mean luminance, plus the 3 brightest in the central band, for each clip. Scrim included. For the 9:16 clip that includes the brass-diagonal frames. The worst case per element across all viewports:

| Element | Target | Worst case |
|---|---|---|
| CONCRETE | 3:1 | 5.82 |
| the | 3:1 | 4.43 (9:16, f695) |
| GROUP | 3:1 | 3.51 (1440×900, f080) |
| Logo (non-text) | 3:1 | 13.52 |
| Tagline (We Build Brands That Last) | 4.5:1 | 9.44 |
| Status line | 4.5:1 | 6.49 (844×390, f243) |
| Button (rest, off-white) | 4.5:1 | 11.55 |
| Button (hover/focus, brass) | 4.5:1 | 5.32 (1920×1080, f411) |
| Pill (removed 2026-09-29) | — | — |
| Footer left / right | 4.5:1 | 4.72 / 4.75 |

**Layout.** Screenshots at 1440×900, 1920×1080, 390×844 and 844×390 are in `qa/`. There is no horizontal overflow at any size, and nothing collides with the footer. The bars pad with `env(safe-area-inset-*)` on all four sides.

**Behavior (Chrome and WebKit, headless).**
- Video plays muted with `loop`, and the fade runs on the first `playing` event.
- Rotating swaps the source and keeps currentTime (4.08s → 4.09s).
- `visibilitychange` pauses playback when hidden and resumes when visible (tested by dispatching the event with `document.hidden` set each way).
- With `prefers-reduced-motion` or Save-Data on, no video request is made and only the poster loads.
- A rejected `play()` (autoplay stubbed off, `play()` forced to reject) leaves the video paused at opacity 0 over the poster, with no page errors and no play button.
- Tab reaches the button first, and the 2px brass ring shows over the video.

**Loop seam.** `tools/seam.py` reports:
- 16:9: seam step 3.80 vs. typical 3.37 (p95 4.53).
- 9:16: seam step 1.79. This matches the steps across the final crossfade second (1.6–2.0); the largest step anywhere is 2.53, mid-clip.

Frames 716–719 → 0–2 are continuous (`qa/seam9x16.jpg`). No loop logic was added.

**Lighthouse mobile** (2 runs): Performance 90 / 95, Accessibility 100, Best Practices 100, SEO 100. CLS 0, TBT 0. The LCP element is the `CONCRETE` span of the lockup.

**Weight.** Local files plus 105 KB of measured Google Fonts transfer: mobile path 3.62 MB (≤4.5), desktop path 7.70 MB (≤8, about 4% headroom).

**Detector.** `impeccable detect`: no findings.

**Not verified.** Real iOS Safari on a device: muted inline autoplay, no black flash at the loop point, the rotation swap. WebKit headless is the closest proxy and it passed, but check once on an iPhone before launch. The seam was checked by frame metrics and stills, not by watching 3 full cycles.
