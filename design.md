# design.md — Pro Lash

> Distilled from `brand-guide.html` (Brand Book) and `project-knowledge.md`. In any build prompt, say: **"use my design.md."**

## Brand
Pro Lash — a vegan, prostaglandin-free lash-growth serum formulated by a six-year lash technician, built to be worn safely underneath extensions. Mood: **warm, premium, girly**. Voice: two sisters talking — direct, not formal.

## Color Palette

| Token | Hex | Role |
|---|---|---|
| `--canvas` | `#FBF5F1` | Page background — warm ivory |
| `--surface-1` | `#FFFFFF` | Default card/panel |
| `--surface-2` | `#F3E1DA` | Elevated card, matches box blush |
| `--surface-2-strong` | `#EFC9C1` | Stronger blush accent surface |
| `--text-primary` | `#2B211D` | Warm near-black — body/headline text |
| `--text-secondary` | `rgba(43,33,29,0.66)` | Secondary copy |
| `--text-tertiary` | `rgba(43,33,29,0.45)` | Labels, meta, captions |
| `--border-subtle` | `rgba(43,33,29,0.10)` | Default hairline borders |
| `--border-emphasis` | `rgba(43,33,29,0.20)` | Stronger borders (secondary buttons) |
| `--accent` | `#BD6F63` | **Status / CTA / emphasis ONLY** — rose |
| `--accent-ink` | `#9C564C` | Darker rose — accent text on light |
| `--gold` | `#C7A66B` | Atmospheric — matches bottle metal |
| `--blush` | `#EFC7C0` | Atmospheric secondary — box top color |
| `--cream-deep` | `#EEE2D6` | Fur/lifestyle-photo reference tone |

**Rule:** the rose accent (`--accent`) marks status, CTAs, and single-word emphasis only — never body text, never a full section background. Restraint reads premium; overuse reads cheap.

## Typography

- **Display / headline:** `Manrope` (400/500/600/700/800) — workhorse sans for all headlines and body copy.
- **Accent face:** `Fraunces` italic (400/500/600) — used for **exactly one emphasis word per heading** and for **big stat numerals only**. Never set full sentences in it.
- **Mono / label:** `JetBrains Mono` (500/600) — eyebrows, IDs, stat labels, uppercase, letter-spaced (~0.08–0.14em). Never above 13px, never for body copy.
- Load all three via Google Fonts. Never letter-space body text.

## Voice & Tone

**Archetype:** your sister who happens to be a lash tech — direct, warm, a little cheeky. Never clinical, never hypey.

**Core principles:**
1. Talk like two sisters — direct, not formal, skip beauty-industry padding.
2. Confident, not hypey — specificity beats "miracle." Name the mechanism, not just the outcome.
3. Honest about gaps — if there's no number yet, say so instead of faking one.

**Signature sentence structures:**
- "You shouldn't have to choose between [X] and [Y]." — e.g. *"You shouldn't have to choose between your extensions and your real lashes."*
- "[Category norm], without [the risk everyone quietly accepts]." — e.g. *"Growth, without the eye irritation you've read about."*

**USE:** vegan · prostaglandin-free · gentle · extension-safe · lash-technician-formulated · honest · real
**AVOID:** miracle · guaranteed overnight results · "clinically proven" without a real number attached · as seen on

## Components

- **Buttons:** primary = solid `--accent` fill, white text, pill radius (999px). Secondary = transparent, `--border-emphasis` outline, `--text-primary` label.
- **Status pill:** `--surface-2` background, `--accent-ink` text, small `--accent` dot before the label (e.g. "Prostaglandin-free").
- **Standard card:** `--surface-1` background, `--border-subtle` 1px border, 18px radius, generous padding (28px+).
- **Elevated/featured card:** gradient `#fff → --surface-2`, soft shadow (`0 20px 40px -28px rgba(43,33,29,0.35)`) — use for the two-pack offer, founder story, hero proof points.
- **Blockquote (Voice of Customer):** 3px `--accent` left border, `--surface-2` background, no italics — quote the customer verbatim, never paraphrase.

## Mood & Motion

- **Atmosphere:** soft champagne-gold metal, warm cream/fur textures, gold jewelry, natural hand-held product photography — warm and tactile, not clinical or sterile.
- **Motion:** gentle scroll fade-up on headlines/cards (15–25px lift, 400–600ms via IntersectionObserver). Never aggressive, never bouncy.
- **Depth:** every section needs presence — a soft radial gradient/glow (blush + gold tones), never a flat dead background.
- **Structure:** max content width ~1140px, consistent section padding, eyebrows (mono, uppercase) above section headings.

## Logo

- Full lockup: `assets/logo.png` — rose-gold "P" monogram resolving into a lash flick, paired with tracked wordmark "PRO LASH." Transparent background.
- Icon-only crop (nav, favicon, small/social use): `assets/logo-icon.png`.
- Don't recolor — the rose-gold metallic finish is the signature. Scale proportionally only.

## Proof Discipline (carries over from `claude-project-instructions.md`)

Never state a claim not sourced in `project-knowledge.md` or `deepresearch.md`. Currently off-limits: specific % / sample size behind "clinically proven," guarantee terms, postpartum/hormonal claims, payment structure. Confirmed and safe to use: prostaglandin-free, vegan, the ingredient list (peptides, hyaluronic acid, vegetable keratin, biotin, pumpkin seed oil), extension-safe, founder's six years as a lash technician.

---

**Usage note:** In any build prompt, say: *"use my design.md."*
