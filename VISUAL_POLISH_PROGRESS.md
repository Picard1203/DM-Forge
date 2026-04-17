# Visual Polish Progress — Step 8.5

Branch: `feature/visual-polish` → `dev`

---

## Task 1 — Fix icon rendering bug ✅

**What changed:** Achievement icons and module icons were rendering as literal slug text (`flag`, `swords`, `flame`, etc.) instead of visual glyphs.

**Fix:**
- Created `frontend/src/components/ui/DynamicIcon.tsx` — a `Record<string, LucideIcon>` mapping covering all 25 slugs used across modules and achievements. Logic: null/empty → `Award` fallback; known slug → Lucide component; non-ASCII-kebab string (emoji) → render as `<span>` so the `⚡`/`🚀` in ext_01/ext_02 are preserved; unknown ASCII-kebab → `Award` fallback.
- Applied to `AchievementBadge.tsx`, `ModuleCard.tsx`, and `ModulePage.tsx`.

**Trade-off:** The task brief stated the bug was in `AchievementsPage.tsx`, but the actual render site is `AchievementBadge.tsx`. Same for `ModulePage.tsx` — the icon renders in both `ModulePage.tsx` (page header) and `ModuleCard.tsx` (card). Both are fixed.

**Dependency added:** `lucide-react ^1.8.0` (was not previously installed).

---

## Task 2 — Card design elevation ✅

**What changed:**
- `frontend/tailwind.config.ts` extended with:
  - New `amber: '#E8B14F'` color token
  - `display: ['Cinzel', ...]` font family
  - `backgroundImage` tokens: `card-surface` and `card-surface-hover` (subtle navy gradients)
  - `boxShadow` tokens: `card`, `card-hover`, `card-complete`
  - `keyframes` + `animation` for `shimmer`
- `frontend/src/styles/globals.css` — added `@layer components` with `.card-surface`, `.card-interactive`, and `.card-complete` utilities
- Applied `.card-surface` / `.card-interactive` to: `ModuleCard`, `AchievementBadge`, `TaskCard`, `FlashCard`, `XPBar`, `StreakWidget`, `QuizResult`, `QuestionCard`, session task rows, login/register auth cards, dashboard inline progress cards, App PWA update banner

**Every card now has:**
- Subtle top-to-bottom gradient instead of flat `#12182b`
- 1px `rgba(255,255,255,0.10)` border (replaces the flat `border-border`)
- Drop shadow with inset highlight simulating a light source from above
- Interactive cards: 2px lift on hover, border shifts to `amber/30`, shadow deepens

---

## Task 3 — Typography hierarchy ✅

**What changed:**
- Cinzel and Inter loaded via Google Fonts `<link>` in `frontend/index.html` (Inter was previously referenced in config but never loaded)
- All page H1s converted to `font-display text-3xl md:text-4xl font-bold tracking-wide` (Cinzel): Dashboard, Achievements, Curriculum, Module, Session, Review, Settings, Login/Register/Quiz pages
- Dashboard H2 ("Module Progress") converted to `font-display text-xl md:text-2xl font-semibold`
- Navbar logo: `font-display text-xl tracking-widest`
- Card titles: remain `font-sans font-semibold` — Cinzel at small sizes is illegible
- Achievement descriptions: reduced to `text-white/70` to create hierarchy under semibold titles
- Module description in `ModulePage.tsx` header: `text-muted`

---

## Task 4 — Progress indicator color + completion visual + XP shimmer ✅

**What changed:**
- `frontend/src/utils/progressColor.ts` — helper returning Tailwind class based on percent: 0–24% → `bg-amber/60`, 25–74% → `bg-amber`, 75–99% → `bg-gold`, 100% → `bg-emerald-500`
- Applied in `ModuleCard.tsx` (was `bg-primary` / red — now correct) and `DashboardPage.tsx` (was `bg-gold` regardless of level — now ramps)
- 100%-complete modules: receive `.card-complete` (gold shadow + gold border tint) + `<CheckCircle>` badge in top-right corner; icon glows amber (`drop-shadow`)
- `XPBar.tsx`: triggered shimmer using `useRef` to track previous XP value. When `xp > prevXp`, a gradient overlay with `animate-shimmer` is rendered on the fill for 1.6 s then removed. No ambient shimmer.

**Trade-off:** The DashboardPage inline module cards are not linked (clicking doesn't navigate) — this is pre-existing and out of scope.

---

## Task 5 — Fix empty states ✅

**Review page:**
- Added a progress bar at top of page showing `(currentIndex / cards.length) * 100%` with numeric "N / total" label beneath
- Added 2 decorative card-shaped divs behind `FlashCard` that are absolutely positioned and offset to create a deck illusion. The offset divs' count matches `min(remaining, 2)` so the deck shrinks as the user reviews.
- Fixed pre-existing bug: `FlashCard` was keyed without `card.id`, so its internal `flipped` state persisted across cards. Fixed with `key={currentCard.id}`.

**Session page:**
- Added `flex flex-col min-h-[calc(100vh-4rem)] justify-center` to `<main>` — content sits vertically centered when the task list is short.

---

## Task 6 — Grammar + pluralization ✅

**What changed:**
- `StreakWidget.tsx`: removed hardcoded `" days"` suffix. Now uses `t('dashboard.streak', { count })` (→ `streak_one` / `streak_other`) and `t('dashboard.streak_best', { count })` (→ `streak_best_one` / `streak_best_other`). Added Flame icon.
- `en.json`: added `streak_one`, `streak_other`, `streak_best_one`, `streak_best_other` keys; replaced `tasks_done` with `tasks_done_one` / `tasks_done_other`
- `DashboardPage.tsx`: `t('progress.tasks_done', { count: completed })` now resolves correctly ("1/1 task", "2/3 tasks")
- `Navbar.tsx`: `{user.xp}` → `{user.xp.toLocaleString()}` for formatting consistency with XPBar

No `XPs` pluralization issues found in source.

---

## Task 7 — Amber accent ✅

**What changed:**
- `amber: '#E8B14F'` added to Tailwind config
- `.card-interactive:hover` uses `border-amber/30` — applied to all interactive cards
- `AchievementBadge.tsx` "+XP" pill: `bg-amber/10 border-amber/40 text-amber px-2 py-0.5 rounded-full text-xs font-medium`
- `Navbar.tsx`: nav links use `NavLink` with active state `border-b-2 border-amber`, inactive `border-transparent`. Replaces the previous active-route visual (none — links had identical appearance whether active or not)
- Completed modules: icon `className` includes `drop-shadow-[0_0_8px_rgba(232,177,79,0.55)]` for amber glow on 100%-complete module icon
- `QualityButtons.tsx`: hover state uses `border-amber/50` instead of `border-primary/50`

Three-accent ceiling held: red (`primary`), gold (`#C9A84C`), amber (`#E8B14F`).

---

## Pre-existing issues noted (not fixed — out of scope)

- `StatsCard.tsx` and `NextUpCard.tsx` exist in `frontend/src/components/dashboard/` but are never imported anywhere. The dashboard `md:grid-cols-3` row is now collapsed to `grid-cols-1 md:grid-cols-2` to avoid two visibly empty columns (the grid only had `StreakWidget`).
- `Sidebar.tsx`, `Footer.tsx`, `SessionPlanner.tsx`, `SessionRunner.tsx` are stubs; left untouched.
- `FlashCard.tsx` owned its own `flipped` state that was not reset between cards — fixed with `key={currentCard.id}` in `ReviewPage.tsx` (this was a visible UX bug affecting the polish goal of the review page, so fixed).
- `index.html` `meta[name=theme-color]` is `#0a0e1a`; `manifest.json` has `#CC3333`. Inconsistency noted but left as-is (affects PWA splash color on Android, not app visuals).

---

## Open questions / VISUAL_POLISH_QUESTIONS.md items

None blocking the PR. Possible follow-ups:

1. **Login/Register auth card border-radius** — currently `rounded-xl` from `.card-surface`. The auth flow used `rounded-xl` before so it's consistent, but the inner `<h2>` could use `font-display` for the form heading too (currently just `font-semibold sans`).
2. **QualityButtons color ramp** — the 6 quality buttons (Blackout → Perfect) all look identical. A red→green ramp (0 = red-tinted, 5 = green-tinted) would reinforce the quality scale visually. Deferred as a follow-up since it's additive and the task brief didn't specify it.
3. **Self-hosting fonts** — currently loaded via Google Fonts CDN. For full offline PWA support, fonts should be self-hosted in `public/fonts/`. Deferred.
4. **Dashboard "Today's XP" stat** — the `md:grid-cols-3` row was collapsed to 2 columns. The second column is empty until `StatsCard` is wired up. A "today" chip or a small stat (total modules completed, total XP) would fill the gap.

---

## Screenshots

*Screenshots to be taken after reviewing the running app (`npm run dev`). Run at 1440px viewport width on dashboard, achievements, session, and review pages after logging in as the trial user.*

Pages to capture:
- `/` (Dashboard) — welcome title in Cinzel, XP bar, streak widget, module progress grid with color ramps
- `/achievements` — achievement grid with Lucide icons, amber XP pills, earned/unearned distinction
- `/session` — vertically centered plan layout, task cards with gradient backgrounds
- `/review` — deck effect behind flashcard, progress bar at top
