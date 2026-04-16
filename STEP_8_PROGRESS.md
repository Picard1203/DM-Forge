# Step 8 Progress — Frontend Stabilization + PWA Scaffolding

## Git hygiene

The quiz YAML commits (`2825bdf`, `0c387a0`, `42f9ca3`, `61b7a00`) were made directly on
`dev` instead of a feature branch. They were never pushed to remote, so the remote was
already clean. Steps taken:

1. Created `feature/quiz-content-backfill` at the offending HEAD (`61b7a00`)
2. Reset local `dev` to `a7dc611` (the last clean merge commit)
3. Pushed both branches — `dev` and `feature/quiz-content-backfill`
4. PR for backfill: https://github.com/Picard1203/DM-Forge/pull/new/feature/quiz-content-backfill
   (open manually — `gh` CLI not installed in this environment)

All feature work below was done on `feature/frontend-stabilization-pwa`.

---

## Task 1 — Session persistence fix

**Root cause:** `ProtectedRoute` evaluates `token === null` synchronously on first render.
The Zustand store initialized `token: null`, so `ProtectedRoute` immediately redirected to
`/login` before `App`'s `useEffect(() => hydrate())` had a chance to run.

**Fix:** Initialize `token` directly from `localStorage.getItem(TOKEN_KEY)` in the store
definition (`authStore.ts:23`). This is synchronous — the token is available on the very
first render, so `ProtectedRoute` sees it before any effects fire. `hydrate()` remains in
place and is now idempotent.

**Files changed:** `frontend/src/store/authStore.ts`

---

## Task 2 — Reactivity audit + optimistic updates

### Completing a task → XP bar + level
**Problem:** `completeTask` was doing two sequential server round-trips after mutation:
`fetchOverview()` + `fetchMe()`. The user's XP bar didn't update until both completed.

**Fix:** The `POST /progress/complete` response already contains `new_xp` and `new_level`.
We now apply these directly to the store via `useAuthStore.setState(...)` immediately, then
`fetchOverview()` runs once to update module progress bars. `fetchMe()` is removed — it was
redundant given the data already in the response.

**Files changed:** `frontend/src/store/progressStore.ts`

### Submitting a quiz → XP award
**Problem:** Quiz submission (`QuizPage`) updated local result state but did not update the
user's XP or the progress overview, leaving the XP bar stale until the user navigated to
the dashboard.

**Fix:** After a first-time quiz submission, we apply `xp_earned` to the user store
immediately and fire `fetchOverview()` in the background.

**Files changed:** `frontend/src/pages/QuizPage.tsx`

### Submitting a review card → next card without delay
**Problem:** `handleQuality` awaited the `submitReview` API call before advancing to the
next card. The user saw a frozen UI during the network round-trip.

**Fix:** Advance the card index and reset flip state synchronously; fire the API call
fire-and-forget. If the submission fails, the card reappears in the next due session —
acceptable for SRS.

**Files changed:** `frontend/src/pages/ReviewPage.tsx`

### Session plan → no flash of empty state
**Problem:** The session page rendered with no plan on mount; the user had to interact with
the slider to see anything. Each slider interaction also caused a "loading" flash that hid
the previous plan.

**Fix:** Load the initial plan on mount with `useEffect`. Keep the previous plan visible
while a new one loads (removed `&& !isLoading` from the plan render condition).

**Files changed:** `frontend/src/pages/SessionPage.tsx`

---

## Task 3 — PWA scaffolding

| Item | Status |
|---|---|
| `vite-plugin-pwa` + Workbox | Installed and configured in `vite.config.ts` |
| `manifest.json` | Updated: added `orientation: "portrait"`, maskable icon |
| Icons 192×192, 512×512, maskable 512×512 | Placeholder PNGs at `public/icons/` |
| Service worker — auto-update prompt | Implemented in `App.tsx` via `useRegisterSW` |
| Offline fallback | `public/offline.html` — "You're offline" with retry button |
| Production build | `npx vite build` succeeds; `sw.js` + `workbox-*.js` generated |

**Theme colors used** (read from `tailwind.config.ts`, not invented):
- `theme_color: "#CC3333"` (primary)
- `background_color: "#0a0e1a"` (bg)

**Note on service worker in dev:** `devOptions.enabled: false` in the Vite PWA config —
the SW does not run during `vite dev`. Test installability and Lighthouse PWA audit against
`vite preview` or a deployed build.

---

## Explicitly out of scope

- Visual redesign, theme changes, color changes, or component styling changes — handled
  separately.
- Real PWA icon artwork — placeholder PNGs with "DF" initials at `public/icons/`. Replace
  with final assets before launch.

---

## Open questions

None requiring architectural decisions. All choices were unambiguous given the constraints.
