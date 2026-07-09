# SITE-SYNC — procedure for syncing this site with the steckling repo docs

You are updating the site so it matches the current state of the steckling CLI's
documentation. The pages are **plain static HTML** — edit them directly.

## Layout

- `index.html` — marketing page (plain HTML, inline styles)
- `docs.html` — docs page: Concepts / Install / Quickstart / Commands / steckling.yml /
  MCP sections, plus a client-side **search index** (a JS array of
  `{ page, tag, t, s, k }` objects near the bottom) that must stay in step with the
  command table and config reference.
- `assets/runtime.js` — page behaviour (search, terminal animation). Rarely needs edits.
- `assets/vendor/` (React) and `assets/fonts/` — leave alone.

GitHub Pages serves `main` directly: **pushing publishes**. Agents must NOT push.

## Source of truth

The steckling repo at `/Users/tim/data/code/timd/steckling`:

- `docs/commands.md` — canonical command list, flags, and wording
- `README.md` — quickstart + commands-table wording
- `CHANGELOG.md` — what changed recently ("Unreleased" section)

You will be told which commits/files changed. Read the relevant diffs first:
`git -C /Users/tim/data/code/timd/steckling diff <old>..<new> -- docs README.md CHANGELOG.md`

## What to update (match the repo docs' wording, keep the page's voice)

1. **Command tables** (both pages): one row per command — add new, update changed,
   remove deleted. Copy the row markup and inline styles of neighbouring rows exactly.
2. **docs.html search index**: keep entries in step with the table (`k` = space-separated
   search keywords).
3. **Prose**: quickstart sections, feature descriptions — only where the repo change
   affected the meaning; don't rewrite for style.
4. **Never invent features.** If the diff is ambiguous, prefer `docs/commands.md` verbatim.

## Finishing

1. Sanity-check your edits: the file must still be valid HTML; if you touched the search
   index, make sure the JS array still parses (balanced quotes/braces).
2. `git add index.html docs.html && git commit` with a short
   `docs: sync with steckling <short description>` message.
3. **Do NOT push.** The owner reviews and pushes.
