# SITE-SYNC — procedure for syncing this site with the steckling repo docs

You are updating the two site pages so they match the current state of the
steckling CLI's documentation. Follow this procedure exactly.

## Source of truth

The steckling repo at `/Users/tim/data/code/timd/steckling`:

- `docs/commands.md` — canonical command list, flags, and wording
- `README.md` — quickstart + commands table wording
- `CHANGELOG.md` — what changed recently ("Unreleased" section)

You will be told which commits/files changed. Read the relevant diffs first:
`git -C /Users/tim/data/code/timd/steckling diff <old>..<new> -- docs README.md CHANGELOG.md`

## The pages (IMPORTANT — do not edit them directly)

`index.html` (marketing page) and `docs.html` (docs page) embed all visible
content as ONE JSON-encoded string on a single long line. NEVER edit that line
by hand. Always use the round-trip tool:

```sh
python3 tools/template.py decode docs.html    # writes docs.decoded.html (plain HTML)
# edit docs.decoded.html with normal Edit operations
python3 tools/template.py encode docs.html    # re-embeds it, verifies losslessness
rm docs.decoded.html
```

Same for `index.html`. The encode step fails loudly if anything would be
corrupted — if it fails, do not try to fix the encoded line manually; re-check
your decoded edit instead.

## What to update (match the repo docs' wording, keep the page's voice)

1. **Command tables** (both pages): one row per command. Add rows for new
   commands, update descriptions/flags for changed ones, remove deleted ones.
   Copy the row markup style of neighbouring rows exactly.
2. **docs.html search index**: a JS array of `{ page, tag, t, s, k }` objects.
   Keep it in step with the command table (add/update/remove entries; `k` is
   space-separated search keywords).
3. **Prose mentions**: quickstart sections, feature descriptions. Only touch
   prose whose meaning the repo change affected — don't rewrite for style.
4. **Never invent features.** If the diff is ambiguous, prefer the wording in
   `docs/commands.md` verbatim.

## Finishing

1. Re-run the encode step for every page you touched; confirm it prints
   "round-trip verified".
2. Delete the `*.decoded.html` files.
3. `git add index.html docs.html && git commit` in this repo with a short
   `docs: sync with steckling <short description>` message.
4. **Do NOT push.** The owner reviews and pushes.
