"""Recover columns from PDF word positions instead of flattened whitespace."""
import re
import unicodedata


def norm(value):
    return re.sub(r"[\s:：.()（）]+", "", unicodedata.normalize("NFKC", value)).lower()


def lines_from_words(words):
    lines = []
    for word in sorted(words, key=lambda w: (w["top"], w["x0"])):
        line = next((r for r in reversed(lines[-3:]) if abs(r[0]["top"]-word["top"]) <= 3), None)
        if line is None:
            lines.append([word])
        else:
            line.append(word)
    return [sorted(line, key=lambda w: w["x0"]) for line in lines]


def header_layout(line, aliases):
    matches = {}
    occupied = set()
    for start in range(len(line)):
        if start in occupied:
            continue
        candidates = []
        for size in range(1, min(8, len(line)-start)+1):
            value = norm("".join(w["text"] for w in line[start:start+size]))
            for key, names in aliases.items():
                if value in {norm(s) for s in names}:
                    candidates.append((size, key))
        if not candidates:
            continue
        size, key = max(candidates)
        if key in matches:
            return None
        matches[key] = (line[start]["x0"], line[start+size-1]["x1"])
        occupied.update(range(start, start+size))
    if set(matches) != set(aliases):
        return None
    ordered = sorted(matches, key=lambda k: matches[k][0])
    edges = [(matches[a][1]+matches[b][0])/2 for a, b in zip(ordered, ordered[1:])]
    return {"keys": ordered, "edges": edges,
            "span": [min(v[0] for v in matches.values()), max(v[1] for v in matches.values())]}


def aligned_tables(words, aliases, inherited=None):
    """Return explicit-header tables or one tentative continuation, never both."""
    lines = lines_from_words(words)
    headers = [(i, header_layout(line, aliases)) for i, line in enumerate(lines)]
    headers = [(i, layout) for i, layout in headers if layout]
    inherited_used = False
    if not headers and inherited:
        headers = [(-1, inherited)]
        inherited_used = True
    result = []
    for n, (start, layout) in enumerate(headers):
        end = headers[n+1][0] if n+1 < len(headers) else len(lines)
        rows = []
        for line in lines[start+1:end]:
            cells = [[] for _ in layout["keys"]]
            for word in line:
                center = (word["x0"]+word["x1"])/2
                col = sum(center >= edge for edge in layout["edges"])
                cells[col].append(word["text"])
            rows.append([" ".join(cell) for cell in cells])
        result.append({"rows": [layout["keys"], *rows], "layout": layout,
                       "inherited": inherited_used, "kind": "coordinates"})
    return result
