#!/usr/bin/env python3
"""Extract and validate generated Alan tutorial snippets."""
import argparse
import concurrent.futures
import difflib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
INCLUDE = re.compile(r"^\{% include_relative snippets/([A-Za-z0-9][A-Za-z0-9_-]*)\.alan %\}$")
FOLDER = re.compile(r"<tutorial folder: .*?/(step_[0-9]+[a-z]?)/>")
DIAG_LINE = re.compile(r"^.+:(\d+):(\d+)(?: to \d+:\d+)?: (?:error|warning):")
DIAG_LOC = re.compile(r"^(.+?):(\d+):(\d+)(?: to \d+:\d+)?: (?:error|warning):")
MIGRATION_LANG = "system-types/datastore/migration/language"
MODEL_LANG = "platform/if-types/model/language"


class ExtractError(Exception):
    def __init__(self, diagnostics):
        self.diagnostics = diagnostics


def diag(path, line, message, column=1, level="error"):
    return f"{Path(path).resolve()}:{line}:{column}: {level}: {message}"


def strip_comment(line):
    quote = None
    escape = False
    for i in range(len(line) - 1):
        c = line[i]
        if quote:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                quote = None
        elif c in "'\"":
            quote = c
        elif c == "/" and line[i + 1] == "/":
            return line[:i].rstrip()
    return line


def trim_dedent(lines):
    lines = list(lines)
    while lines and not lines[0].strip(): lines.pop(0)
    while lines and not lines[-1].strip(): lines.pop()
    if not lines:
        return []
    indents = [len(x) - len(x.lstrip("\t")) for x in lines if x.strip()]
    amount = min(indents) if indents else 0
    return [("" if not x.strip() else x[amount:]) for x in lines]


def marker_parts(line):
    lead = len(line) - len(line.lstrip())
    rest = line[lead:]
    if rest.startswith("//@"):
        return rest[3:].strip().split(), lead + 1
    pos = line.find("//@")
    if pos >= 0:
        return None, pos + 1
    return None, None


def extract_file(path):
    path = Path(path).resolve()
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    if lines and lines[-1] == "": lines.pop()
    diagnostics, open_regions, done, regions = [], {}, {}, {}
    all_name = None
    expect = None
    all_lines = []
    for number, line in enumerate(lines, 1):
        parts, col = marker_parts(line)
        if parts is None and col is not None:
            diagnostics.append(diag(path, number, "marker must be on its own line", col))
            continue
        if parts is None:
            all_lines.append(line)
            for state in open_regions.values():
                mode = state["mode"]
                if mode == "show": state["lines"].append(strip_comment(line) if state["strip"] else line)
                elif mode == "hide" and line.strip() and not state["hidden"]:
                    state["lines"].append(line[:len(line)-len(line.lstrip("\t"))] + "...")
                    state["hidden"] = True
            continue
        if not parts:
            diagnostics.append(diag(path, number, "unknown marker command")); continue
        command = parts[0]
        if command == "begin":
            if len(parts) not in (2, 3) or (len(parts) == 3 and parts[2] != "strip-comments"):
                diagnostics.append(diag(path, number, "unknown marker command")); continue
            name = parts[1]
            if not NAME.match(name): diagnostics.append(diag(path, number, "bad name")); continue
            if name in open_regions: diagnostics.append(diag(path, number, f"begin of already open region '{name}'")); continue
            open_regions[name] = {"lines": [], "mode": "show", "hidden": False, "strip": len(parts) == 3, "begin": number}
        elif command == "end":
            match = re.fullmatch(r'end\s+([^\s]+)(?:\s+cut="(.*)")?', line.lstrip()[3:].strip())
            if not match:
                diagnostics.append(diag(path, number, "unknown marker command")); continue
            name, cut = match.group(1), match.group(2)
            if not NAME.match(name): diagnostics.append(diag(path, number, "bad name")); continue
            if name not in open_regions: diagnostics.append(diag(path, number, f"end of non-open region '{name}'")); continue
            state = open_regions.pop(name); chunk = trim_dedent(state["lines"])
            if not chunk: diagnostics.append(diag(path, number, "empty region")); continue
            if cut is not None:
                at = chunk[-1].find(cut)
                if at < 0: diagnostics.append(diag(path, number, "cut text missing")); continue
                chunk[-1] = chunk[-1][:at].rstrip() + " ..."
            done.setdefault(name, []).append(chunk)
            regions.setdefault(name, []).append((state["begin"] + 1, number - 1))
        elif command in ("hide", "skip", "show"):
            names = parts[1:] or list(open_regions)
            for name in names:
                if not NAME.match(name): diagnostics.append(diag(path, number, "bad name")); continue
                if name not in open_regions: diagnostics.append(diag(path, number, f"{command} of non-open region '{name}'")); continue
                state = open_regions[name]; state["mode"] = command; state["hidden"] = False
        elif command == "all":
            if len(parts) != 2: diagnostics.append(diag(path, number, "unknown marker command")); continue
            if all_name is not None: diagnostics.append(diag(path, number, "second all")); continue
            if not NAME.match(parts[1]): diagnostics.append(diag(path, number, "bad name")); continue
            all_name = parts[1]
        elif command == "expect":
            raw = line.lstrip()[3:].strip().split(None, 2)
            if expect is not None: diagnostics.append(diag(path, number, "second expect")); continue
            if len(raw) < 3 or raw[1] not in ("error", "warning"):
                diagnostics.append(diag(path, number, "expect kind not error/warning")); continue
            expect = (raw[1], raw[2], number)
        else:
            diagnostics.append(diag(path, number, "unknown marker command"))
    for name, state in open_regions.items(): diagnostics.append(diag(path, state["begin"], "unterminated region"))
    if all_name is not None:
        chunk = trim_dedent(all_lines)
        if not chunk: diagnostics.append(diag(path, 1, "empty region"))
        else: done.setdefault(all_name, []).append(chunk); regions.setdefault(all_name, []).append((1, len(lines)))
    for name, chunks in done.items():
        text = "\n...\n".join("\n".join(chunk) for chunk in chunks)
        if "{{" in text or "{%" in text: diagnostics.append(diag(path, 1, "Liquid syntax in snippet"))
    if diagnostics: raise ExtractError(diagnostics)
    return done, expect, regions


def extract_all(models_dir):
    output, owners, diagnostics = {}, {}, []
    for d, kind in project_dirs(models_dir):
        for path in marker_files(d, kind):
            try: chunks, _, _ = extract_file(path)
            except ExtractError as e: diagnostics.extend(e.diagnostics); continue
            for name, pieces in chunks.items():
                if name in owners:
                    diagnostics += [diag(path, 1, f"snippet '{name}' also produced by {owners[name]}"), diag(owners[name], 1, f"snippet '{name}' also produced by {path}")]
                else:
                    owners[name] = path; output[name] = "\n...\n".join("\n".join(x) for x in pieces)
    if diagnostics: raise ExtractError(diagnostics)
    return output


def version_dir(version, tutorial="model"): return ROOT / "pages/tutorials" / tutorial / version


def project_dirs(models_dir):
    """Every models/<dir> is either a model project (application.alan) or a migration project (migration.alan)."""
    out = []
    for d in sorted(p for p in Path(models_dir).glob("*") if p.is_dir()):
        if (d / "migration.alan").exists(): out.append((d, "migration"))
        elif (d / "application.alan").exists(): out.append((d, "model"))
    return out


def marker_files(d, kind):
    """Files of a project that may carry //@ markers."""
    if kind == "model": return [d / "application.alan"]
    files = [d / "migration.alan"]
    for sub in ("source", "target"):
        f = d / "models" / sub / "application.alan"
        if f.exists(): files.append(f)
    return files


def language_for(platform, kind): return Path(platform) / (MODEL_LANG if kind == "model" else MIGRATION_LANG)


def inline_check(vdir):
    models = []
    for d, kind in project_dirs(vdir / "models"):
        for p in marker_files(d, kind):
            models.append(re.sub(r"\s+", " ", p.read_text(encoding="utf-8").replace("\r\n", "\n")).strip())
    for md in sorted(vdir.glob("*.md")):
        lines = md.read_text(encoding="utf-8").splitlines(); i = 0
        while i < len(lines):
            if lines[i] == "```js":
                start = i; i += 1; body = []
                while i < len(lines) and not lines[i].startswith("```"): body.append((i + 1, lines[i])); i += 1
                if not (len(body) == 1 and INCLUDE.fullmatch(body[0][1].strip())):
                    for n, text in body:
                        norm = re.sub(r"\s+", " ", text).strip()
                        if not norm or norm == "..." or re.fullmatch(r"[(){}\[\]|=>,;.\s]+", text): continue
                        if not any(norm in model for model in models): print(f"{md.resolve()}:{n}: {text}")
            i += 1


def audit_docs(vdir, generated):
    errors = warnings = 0; refs = set()
    for md in sorted(vdir.glob("*.md")):
        lines = md.read_text(encoding="utf-8").replace("\r\n", "\n").splitlines()
        for n, line in enumerate(lines, 1):
            if "files_application-tutorial" in line: print(diag(md, n, "legacy snippet path")); errors += 1
            match = FOLDER.search(line)
            if match and not (vdir / "models" / match.group(1)).is_dir(): print(diag(md, n, f"no models/{match.group(1)} for tutorial folder marker")); errors += 1
            if line.rstrip() == "```js":
                inc = lines[n].strip() if n < len(lines) else ""
                close = lines[n + 1].rstrip() if n + 1 < len(lines) else ""
                m = INCLUDE.fullmatch(inc)
                if not m or close != "```": print(diag(md, n, "```js fence must contain exactly one include_relative of snippets/<name>.alan")); errors += 1
                else:
                    name = m.group(1); refs.add(name)
                    if name not in generated: print(diag(md, n + 1, f"unknown snippet '{name}'")); errors += 1
            elif line.startswith("```") and line.rstrip() != "```": print(diag(md, n, "non-verified fence", level="warning")); warnings += 1
    for name in generated:
        if name not in refs: print(diag(vdir / "snippets" / f"{name}.alan", 1, "snippet not referenced by any page")); errors += 1
    return errors, warnings


def compiler_check(d, kind, platform, expect, regions_by_file):
    """Compile one project dir (model or migration). Returns (diagnostics, toolchain_notices)."""
    main_file = d / ("application.alan" if kind == "model" else "migration.alan")
    cmd = [str(Path(platform)/"platform/project-compiler/tools/compiler-project"), str(language_for(platform, kind)), "--format", "vscode", "-C", str(d), "/dev/null"]
    try: r = subprocess.run(cmd, text=True, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired: return [diag(main_file, 1, "compiler timeout")], []
    out = (r.stdout + r.stderr).strip("\n"); lines = out.splitlines() if out else []
    located = [x for x in lines if DIAG_LINE.match(x)]
    # warnings without a source location come from the toolchain itself (e.g. an annotation package that
    # could not be loaded); they are reported once per run by the caller, not attributed to the model
    notices = [x.strip() for x in lines if "warning:" in x and not DIAG_LINE.match(x)]
    located_warnings = [x for x in located if " warning: " in x]
    if expect is None:
        if r.returncode == 0 and not located_warnings: return [], notices
        result = list(located) + ([diag(main_file, 1, "model compiles with warnings; add '//@ expect warning <text>' or fix")] if r.returncode == 0 else [])
        if r.returncode != 0 and not any(": error:" in x for x in result):
            result.append(diag(main_file, 1, f"compiler failed (exit {r.returncode})"))
        return result, notices
    kind_, text, eline, efile = expect
    if kind_ == "error": ok = r.returncode != 0 and text in out
    else: ok = r.returncode == 0 and any(text in x for x in located_warnings)
    if not ok:
        msg = f"expected compile {kind_} containing '{text}'" + (f" (compiler exit {r.returncode})" if kind_ == "error" else "")
        return list(located) + [diag(efile, eline, msg)], notices
    if kind_ == "error":
        for line in located:
            m = DIAG_LOC.match(line)
            if m:
                at = int(m.group(2)); where = Path(m.group(1)).resolve()
                ranges = [rng for f, rs in regions_by_file.items() if Path(f).resolve() == where for rng in rs.values()]
                if ranges and not any(a <= at <= b for rs in ranges for a, b in rs):
                    return [diag(where, at, "expected error is not shown by any snippet", level="warning")], notices
                break
    return [], notices


# the online-ide docs directory that holds the step models of a tutorial, per website tutorial name
REFERENCE_DOCS = {"model": "restaurant1", "mission": "mission-control"}


def compare_reference(path, platform, reference, version, tutorial="model"):
    ref = Path(reference)/"docs/tutorials"/REFERENCE_DOCS[tutorial]/version/path.parent.name/"to_model/application.alan"
    if not ref.exists(): return [diag(path, 1, f"missing online-ide reference {ref.resolve()}")]
    def without_comments(text):
        # markers and every // comment are stripped on BOTH sides; the pretty-printer keeps comments otherwise
        kept = []
        for x in text.replace("\r\n", "\n").splitlines():
            if marker_parts(x)[0] is not None or x.lstrip().startswith("//"):
                continue
            kept.append(strip_comment(x))
        return "\n".join(kept) + "\n"
    cleaned = without_comments(path.read_text(encoding="utf-8"))
    cleaned_ref = without_comments(ref.read_text(encoding="utf-8"))
    pp = Path(platform)/"platform/project-compiler/tools/pretty-printer"; lang = Path(platform)/"platform/if-types/model/language"
    with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
        (Path(a)/"application.alan").write_text(cleaned); (Path(b)/"application.alan").write_text(cleaned_ref)
        def run(d, label):
            r = subprocess.run([str(pp), str(lang), "-C", d, "--file", "/dev/stdout", "--", "application.alan"], text=True, capture_output=True)
            if r.returncode != 0 or not r.stdout.strip():
                raise RuntimeError(f"pretty-printer failed on {label} (exit {r.returncode}): {(r.stderr or r.stdout).strip()[:300]}")
            return r.stdout.splitlines()
        try: left, right = run(a, str(path)), run(b, str(ref))
        except RuntimeError as e: return [diag(path, 1, str(e))]
    if left == right: return []
    first = next((i+1 for i,(x,y) in enumerate(zip(left,right)) if x != y), min(len(left),len(right))+1)
    diff = list(difflib.unified_diff(left, right, fromfile=str(path), tofile=str(ref), n=1))[:6]
    return [diag(path, first, f"differs from online-ide {ref.resolve()}")] + ["  " + x for x in diff]


def verify(version, platform=None, jobs=None, reference=None, no_compile=False, tutorial="model"):
    vdir = version_dir(version, tutorial); errors = warnings = 0
    info = []
    for d, kind in project_dirs(vdir / "models"):
        expect = None; regions_by_file = {}
        for path in marker_files(d, kind):
            try:
                chunks, expected, regions = extract_file(path); regions_by_file[path] = regions
                if expected and expect is None: expect = (*expected, path)
            except ExtractError as e: print("\n".join(e.diagnostics)); errors += len(e.diagnostics)
        info.append((d, kind, expect, regions_by_file))
    if platform and not no_compile:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs or os.cpu_count() or 1) as ex:
            futures = [ex.submit(compiler_check, d, k, platform, e, r) for d, k, e, r in info]
            seen_notices = set()
            for fut in futures:
                msgs, notices = fut.result(); print("\n".join(msgs)) if msgs else None
                errors += sum(": error:" in x for x in msgs); warnings += sum(": warning:" in x for x in msgs)
                for note in notices:
                    if note not in seen_notices:
                        seen_notices.add(note); warnings += 1
                        print(diag(Path(platform)/MODEL_LANG, 1, f"toolchain: {note}", level="warning"))
    try: generated = extract_all(vdir/"models")
    except ExtractError as e: print("\n".join(e.diagnostics)); generated = {}; errors += len(e.diagnostics)
    snips = vdir/"snippets"
    for name, text in generated.items():
        target = snips/f"{name}.alan"
        if not target.exists() or target.read_text(encoding="utf-8").replace("\r\n", "\n") != text: print(diag(target, 1, f"snippet out of date; run snippets.py extract {version} --write")); errors += 1
    for target in snips.glob("*.alan") if snips.exists() else []:
        if target.stem not in generated: print(diag(target, 1, "stale generated snippet; run extract --write")); errors += 1
    e,w = audit_docs(vdir, generated); errors += e; warnings += w
    if platform and reference and tutorial in REFERENCE_DOCS:
        for d, kind, expect, _ in info:
            # a model that is meant not to compile has no online-ide counterpart: it is never a tutorial step
            if kind == "model" and re.match(r"^step_[0-9]+[a-z]?$", d.name) and not expect:
                msgs = compare_reference(d/"application.alan", platform, reference, version, tutorial); print("\n".join(msgs)) if msgs else None; errors += len([x for x in msgs if ": error:" in x])
    print(f"verify: {errors} error(s), {warnings} warning(s)", file=sys.stderr)
    return errors, warnings


def census(version, tutorial="model"):
    result = {}; diagnostics = []; vdir = version_dir(version, tutorial)
    for d, kind in project_dirs(vdir/"models"):
        for path in marker_files(d, kind):
            markers = []; lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").splitlines()
            try: extract_file(path)
            except ExtractError as e: diagnostics += e.diagnostics
            for n,line in enumerate(lines,1):
                parts,col = marker_parts(line)
                if parts:
                    name = parts[1] if parts[0] in ("begin", "end", "all") and len(parts) > 1 else None
                    markers.append([parts[0], name, n])
            result[str(path.relative_to(vdir))] = {"markers": markers, "marker_count": len(markers), "comment_count": sum("//" in x and marker_parts(x)[0] is None for x in lines)}
    if diagnostics: print("\n".join(diagnostics), file=sys.stderr); return 1
    print(json.dumps(result, indent=2, sort_keys=True)); return 0


def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="command", required=True)
    x=sub.add_parser("extract"); x.add_argument("version"); x.add_argument("--write",action="store_true"); x.add_argument("--check-inline",action="store_true")
    v=sub.add_parser("verify"); v.add_argument("version"); v.add_argument("--platform",required=True); v.add_argument("--jobs",type=int); v.add_argument("--reference"); v.add_argument("--no-compile",action="store_true")
    c=sub.add_parser("census"); c.add_argument("version")
    for sp in (x, v, c): sp.add_argument("--tutorial", default="model", help="tutorial dir under pages/tutorials (default: model)")
    a=p.parse_args()
    if a.command == "census": return census(a.version, a.tutorial)
    if a.command == "verify": return 1 if verify(a.version,a.platform,a.jobs,a.reference,a.no_compile,a.tutorial)[0] else 0
    vd=version_dir(a.version, a.tutorial)
    try: generated=extract_all(vd/"models")
    except ExtractError as e: print("\n".join(e.diagnostics)); return 1
    snips=vd/"snippets"; changed=sum(not (snips/f"{n}.alan").exists() or (snips/f"{n}.alan").read_text().replace("\r\n","\n") != t for n,t in generated.items()); stale=sum(1 for q in snips.glob("*.alan") if q.stem not in generated) if snips.exists() else 0
    if a.write:
        snips.mkdir(exist_ok=True)
        for n,t in generated.items():
            q=snips/f"{n}.alan"
            if not q.exists() or q.read_text().replace("\r\n","\n") != t: q.write_text(t,encoding="utf-8")
        for q in snips.glob("*.alan"):
            if q.stem not in generated: q.unlink()
        print(f"wrote {len(generated)} snippets ({changed} changed, {stale} stale)", file=sys.stderr)
    else: print(f"would write {len(generated)} snippets ({changed} changed, {stale} stale)", file=sys.stderr)
    if a.check_inline: inline_check(vd)
    return 0


if __name__ == "__main__": sys.exit(main())
