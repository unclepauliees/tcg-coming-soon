# Claude Code Prompt: The Concrete Group, Coming Soon Page (v2)

**Status:** Footage generation, retime, loop and encode are complete (formerly Phases 1–2). This prompt starts at the build. All media in this package is final and approved; do not regenerate, regrade or re-encode it.

> Unzip this package at the repo root so `/brand-assets`, `/assets` and `/tools` sit beside the build. `[RATIFY]` items are copy placeholders awaiting sign-off. Build with them as written.

---

```
ROLE
You are a senior creative technologist. You ship production-grade, single-file landing pages. You execute the brief exactly: no redesigns, no invented copy, no commentary on approved assets.

MISSION
Build a single-page "coming soon" landing page for THE CONCRETE GROUP (TCG), a senior-led PR and brand advisory agency. A full-bleed, 30-second looping cinematic video of steel mixer fins turning through wet concrete plays behind a restrained typographic lockup. Positioning: permanence over trend-chasing, "We Are Solid." Concept: concrete in a turning drum is still changeable; once it stops, it sets permanently. The page is the last moment before the pour. Restraint is the flex.

APPROVED INPUTS (final; use exactly as supplied)
/brand-assets/TCG_Logo_Main.png      ring mark, logo ink #484848, transparent, 900x967
/brand-assets/TCG_Logo_Reverse.png   ring mark, off-white reverse, transparent, 900x967  -> use this one on the dark field
/assets/video/hero_16x9.mp4          1920x1080, 30.000s, H.264 High, 24fps, no audio, faststart, 7.4 MB
/assets/video/hero_9x16.mp4          720x1280,  30.000s, H.264 High, 24fps, no audio, faststart, 3.4 MB
/assets/img/poster_16x9.jpg          frame 0 of hero_16x9 (identical to the first painted video frame)
/assets/img/poster_9x16.jpg          frame 0 of hero_9x16
/assets/img/og-image.jpg             1200x630 social card
Video facts (measured): both files are seamless loops. One 1s crossfade seam, constant rotation speed (±5%), no cuts. Set loop on the <video> element. Do NOT add any JS loop logic, crossfade, or playbackRate change. Do not recolor, crop, filter or redraw the logos.
Brand OS tokens: https://github.com/unclepauliees/tcg-brand-os (tokens/tokens.json is the source of truth). Values reproduced below; use verbatim.

HARD CREATIVE CONSTRAINT
Nothing on the page may read as a construction company: no hard-hat iconography, no "building" or "contractor" language, no hi-vis color. Shoot-for-luxury restraint.

=== BUILD ===
Deliverable: /dist/index.html (single file, inline CSS + JS) + /dist/assets/ (copy the approved media in, unchanged). No frameworks, no build step, no paid deps.

EXACT TOKENS (use as :root)
--concrete-black:#1C1C1A --true-black:#0F0F0D --brass:#C49A3C --sage:#7D8B6D --off-white:#ECEAE3 --logo-ink:#484848
--n-300:#BAB6AB --n-400:#908D83 --n-600:#4A4D45 --n-700:#333330
--text-primary:var(--off-white) --text-secondary:var(--n-300) --text-muted-body:var(--n-400) --text-accent:var(--brass)
--font-display:"Archivo Black","Arial Black",sans-serif
--font-display-light:"Archivo","Arial",sans-serif (300)
--font-eyebrow:"Space Mono","Courier New",monospace
--font-body:"Inter",system-ui,sans-serif
Load via Google Fonts: Archivo Black; Archivo 300/400; Space Mono 400/700; Inter 400/500. font-display:swap. Preconnect to fonts.gstatic.com.
Hero lockup: prefix "the" = Archivo 300 clamp(1.5rem,3vw,2.5rem); heavy "CONCRETE" = Archivo Black clamp(4rem,14vw,13rem) ls -.04em lh .92; light "GROUP" = Archivo 300 clamp(2.5rem,8vw,7rem), color text-secondary.
Eyebrow: Space Mono 11px / ls .2em / uppercase.
--ease-reveal:cubic-bezier(0,0,.2,1)   --ease-cursor:cubic-bezier(.22,1,.36,1)
Shape: radius 0 everywhere; the ONLY round form is the 999px eyebrow pill.
Page background (behind video, visible before first paint): var(--true-black).

LAYER STACK (back to front)
1. <video> full-bleed (position:fixed; inset:0), object-fit:cover, autoplay muted loop playsinline, preload="auto", disablepictureinpicture, aria-hidden="true", poster set.
   Source selection in JS: matchMedia("(orientation: portrait)") -> hero_9x16.mp4 + poster_9x16.jpg, else hero_16x9.mp4 + poster_16x9.jpg. Re-evaluate on change: swap src, keep currentTime, call play().
2. Scrim: linear-gradient concrete-black 0.85 at bottom -> 0.35 at top, plus a soft radial darkening behind the lockup. Tune until QA contrast passes.
3. Grain: inline SVG feTurbulence overlay, opacity ≤ 0.03. The footage already carries grain; if the overlay reads as double grain at 100% zoom, remove it.
4. Content.

CONTENT (copy is locked; [RATIFY] items are placeholders to build as written)
- Top-left: TCG_Logo_Reverse.png, height 56px desktop / 44px mobile, alt="The Concrete Group". Respect the Brand OS minimum size if it specifies a larger floor.
- Top-right: eyebrow pill "COMING SOON" (1px border var(--n-400), Space Mono).
- Center-left (desktop) / center (mobile): hero lockup "the / CONCRETE / GROUP" as one <h1> with the three lines in spans.
- Below lockup: brass rule line (1px x 64px) + terminal dot, then "We Are Solid." in Archivo 300, clamp(1.25rem,2vw,1.75rem), text-primary.
- Status line, Space Mono eyebrow, text-secondary: [RATIFY: "NOW SETTING."]
- Primary button: "GET IN TOUCH" -> mailto:YourAgency@theconcretegrp.com. Space Mono uppercase ls .12em, radius 0, min-height 44px, 1px off-white border, transparent fill. Hover/focus: brass border + brass text, .25s var(--ease-cursor). Visible :focus-visible ring (2px offset, brass).
- Footer bar, Space Mono 11px, text-muted-body: "© 2026 THE CONCRETE GROUP" left, "THECONCRETEGRP.COM" right.
- Brass appears only on the rule/dot and the button hover/focus. Nowhere else.
- No email-capture form (no backend). No countdown timer. No social icons.

MOTION
- On load, staged reveal: logo -> pill -> lockup lines -> rule -> tagline -> status -> button. Each .reveal = opacity 0 -> 1, translateY 24px -> 0, .4s var(--ease-reveal), 120ms stagger. Starts once fonts are ready (document.fonts.ready, 1.2s max wait). Never waits on the video.
- Video: starts at opacity 0 over the poster (poster rendered as the page's background image), fades to 1 over .8s var(--ease-reveal) on the first 'playing' event. Posters are frame 0, so the handoff is invisible.
- One ambient loop only: the video. No parallax, no cursor effects, no bounce.
- prefers-reduced-motion: never call play(), remove autoplay, show poster only, disable transforms, show content immediately.
- Pause on visibilitychange (hidden), resume on visible.
- navigator.connection?.saveData === true: poster only, no video request.
- If autoplay is rejected (play() promise rejects), stay on poster silently. No play button.

META
<title>The Concrete Group | Coming Soon</title>; meta description [RATIFY: "The Concrete Group. Senior-led PR, communications and brand advisory. Coming soon."]; canonical https://theconcretegrp.com/; OG + Twitter (summary_large_image) with og-image.jpg; theme-color #1C1C1A; <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"> with safe-area padding on the top/bottom bars. Favicons: PNG 32 and 180 generated from TCG_Logo_Main.png by uniform scale onto a transparent square canvas. No recolor, no crop into the mark.
<link rel="preload" as="image"> for the poster matching the current orientation (use media attributes).

=== QA (report results; fix before handoff) ===
- Contrast: sample the 3 brightest frames of each video under every text region (PIL). Verify each element over scrim + frame meets WCAG 2.1 AA: 4.5:1 for eyebrow/body/button/footer, 3:1 for the display lockup. Report the worst-case ratio per element; strengthen the scrim if any fail. Note: the 9:16 clip carries bright brass highlights on a diagonal from upper-left. Check the lockup against those frames specifically.
- Screenshots (headless Chromium): 1440x900, 1920x1080, 390x844, 844x390 landscape phone. "CONCRETE" never overflows the viewport; nothing collides with the footer; logo and pill clear the safe areas.
- iOS Safari: muted inline autoplay works; poster paints before play; no black flash at the loop point; orientation change swaps source without a visible jump.
- Loop: watch 3 full cycles per file and confirm the seam at 29–30s is invisible. Do not "fix" the loop in code; if you see a problem, stop and report it.
- Lighthouse mobile: Performance ≥ 85, Accessibility 100. LCP element = poster or lockup, not the video.
- Weight: mobile path ≤ 4.5 MB total; desktop path ≤ 8 MB total (approved: hero_16x9 is 7.4 MB; do not re-encode to hit a smaller number).
- Keyboard: Tab reaches the button; focus ring visible over the video.

WORKING METHOD
1. Read this prompt, list the files you found in /brand-assets and /assets with their dimensions, and output a one-screen build plan. Then build (no approval gate needed; copy and media are locked).
2. Build /dist.
3. Run QA and fix.
4. Hand off /dist plus a short README: file map, where each [RATIFY] placeholder lives, and how to swap it.
Flag every [RATIFY] item still open at handoff.

CONSTRAINTS
Do not invent taglines, client names, or claims. Do not redraw, recolor or filter the logo. Do not re-encode, trim, grade or retime the video. Restraint over decoration: if it doesn't read durable, senior, and authoritative, cut it.
```
