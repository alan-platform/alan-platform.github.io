#!/usr/bin/env python3
"""Model 108 to 109, in place and line by line, for models whose layout and comments the tutorials depend on.

The 109 upgrade transformation re-emits a whole model in canonical layout: it joins wrapped lines, drops blank
lines and moves a trailing comment, snippet markers included, behind the closing parenthesis it inserts. These
rules make the same syntax changes and leave every other character alone:
  sum <path> / count <path>          ->  sum ( <path> ) / count ( <path> )
  sibling in ( 'Graph' )             ->  siblings in 'Graph'[]
  sibling                            ->  siblings []
Quoted names and texts, and line comments, are never rewritten. A model that still does not compile afterwards
goes through the platform's transformation as before.
"""
import re
import sys

AGGREGATE = re.compile(r"\b(sum|count)\s+(?!\()(?P<path>.*?)(?P<space>\s*)$")
SIBLING_IN = re.compile(r"\bsibling\s+in\s*\(\s*('\x00*')\s*\)")
SIBLING = re.compile(r"\bsibling\b(?!s)(?!\s+in\b)(?P<space>\s*)$")
QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def rewrite(line):
    # The rules see the code only: quoted names and texts are masked (so 'sum total' is never a sum), and a line
    # comment, which starts at the first // outside quotes, is left as it is.
    masked = QUOTED.sub(lambda m: m.group(0)[0] + "\x00" * (len(m.group(0)) - 2) + m.group(0)[-1], line)
    cut = masked.find("//")
    cut = len(line) if cut < 0 else cut
    code, masked_code, rest = line[:cut], masked[:cut], line[cut:]

    def apply(pattern, replace):
        nonlocal code, masked_code
        m = pattern.search(masked_code)
        if m is None:
            return
        new = replace(m, code)
        code = code[: m.start()] + new + code[m.end():]
        masked_code = QUOTED.sub(lambda q: q.group(0)[0] + "\x00" * (len(q.group(0)) - 2) + q.group(0)[-1], code)

    apply(AGGREGATE, lambda m, c: f"{m.group(1)} ( {c[m.start('path'):m.end('path')]} ){c[m.start('space'):m.end('space')]}")
    apply(SIBLING_IN, lambda m, c: f"siblings in {c[m.start(1):m.end(1)]}[]")
    apply(SIBLING, lambda m, c: f"siblings []{c[m.start('space'):m.end('space')]}")
    return code + rest


for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        old = f.read()
    new = "".join(rewrite(l[:-1]) + "\n" if l.endswith("\n") else rewrite(l) for l in old.splitlines(keepends=True))
    if new != old:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"rewrote {path}", file=sys.stderr)
