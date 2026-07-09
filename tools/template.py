#!/usr/bin/env python3
"""Decode/encode the JSON-embedded page template in index.html / docs.html.

Both pages keep all visible content in ONE JSON-encoded string on a single line
inside <script type="__bundler/template">, with `/` in closing tags escaped as
\\u002F. Editing that line directly is error-prone; this tool round-trips it:

    python3 tools/template.py decode docs.html     # writes docs.decoded.html
    # ... edit docs.decoded.html as plain HTML ...
    python3 tools/template.py encode docs.html     # re-embeds it, verifies round-trip

`encode` refuses to write unless the re-encoded line json-decodes back to
exactly the edited content, and re-applies the <\\u002F escape profile.
"""

import json
import re
import sys
from pathlib import Path

def find_payload(lines: list[str]) -> tuple[int, int, int, str]:
    """Locate the page-content payload: the largest JSON string literal in the
    file that decodes to HTML mentioning steckling. (The pages also embed other
    big JSON blobs — framework bundles — which must NOT be matched.)

    Returns (line_index, start, end, decoded_content).
    """
    best: tuple[int, int, int, str] | None = None
    for i, line in enumerate(lines):
        if len(line) < 10000:
            continue
        for m in re.finditer(r'"(?:[^"\\]|\\.)*"', line):
            raw = line[m.start() : m.end()]
            if len(raw) < 10000:
                continue
            try:
                content = json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                continue
            if not isinstance(content, str) or "steck" not in content.lower():
                continue
            if best is None or len(content) > len(best[3]):
                best = (i, m.start(), m.end(), content)
    if best is None:
        sys.exit("error: no steckling page-content payload found")
    return best


def decode(page: Path) -> None:
    lines = page.read_text().split("\n")
    idx, _, _, content = find_payload(lines)
    out = page.with_suffix(".decoded.html")
    out.write_text(content)
    print(f"decoded line {idx + 1} of {page} -> {out} ({len(content)} chars)")


def encode(page: Path) -> None:
    decoded = page.with_suffix(".decoded.html")
    if not decoded.exists():
        sys.exit(f"error: {decoded} not found — run decode first")
    content = decoded.read_text()

    lines = page.read_text().split("\n")
    idx, start, end, _ = find_payload(lines)
    line = lines[idx]

    encoded = json.dumps(content, ensure_ascii=False)
    # match the original escape profile: every `</` becomes `</`
    encoded = encoded.replace("</", "<\\u002F")

    if json.loads(encoded) != content:
        sys.exit("error: round-trip check failed — nothing written")

    lines[idx] = line[:start] + encoded + line[end:]
    page.write_text("\n".join(lines))
    if "</" in encoded:
        sys.exit("error: raw '</' survived in encoded payload — page written but check it")
    print(f"encoded {decoded} back into {page} (round-trip verified)")


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in ("decode", "encode"):
        sys.exit(__doc__)
    page = Path(sys.argv[2])
    if not page.exists():
        sys.exit(f"error: {page} not found")
    (decode if sys.argv[1] == "decode" else encode)(page)


if __name__ == "__main__":
    main()
