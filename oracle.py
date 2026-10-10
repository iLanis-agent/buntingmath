#!/usr/bin/env python3
"""Independent oracle for Bunting math. Mirrors engine.js float ops exactly."""
import json, math

def r1(x): return math.floor(x * 10 + 0.5) / 10

def num(x):
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return repr(x)

def flag_count(length_cm, flag_w, gap_cm):
    if not (isinstance(length_cm, (int, float)) and math.isfinite(length_cm) and length_cm > 0):
        return {"error": "string length must be positive"}
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (flag_w, gap_cm)):
        return {"error": "flag width and gap must be positive"}
    flags = math.floor((length_cm + gap_cm) / (flag_w + gap_cm))
    if flags < 1:
        return {"error": "one flag is wider than the string"}
    leftover = r1(length_cm - (flags * flag_w + (flags - 1) * gap_cm))
    return {"lengthCm": r1(length_cm), "flagW": r1(flag_w), "gapCm": r1(gap_cm),
            "flags": flags, "leftover": leftover}

def render_flags(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['lengthCm'])} cm string holds {r['flags']} flags of {num(r['flagW'])} cm at {num(r['gapCm'])}"
            f" cm gaps, with {num(r['leftover'])} cm of slack to share between the ends (labeled 15 cm flags, 5 cm gaps).")

def fabric_plan(flag_w, flag_h, flags):
    if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in (flag_w, flag_h, flags)):
        return {"error": "flag dimensions and count must be positive"}
    across = math.floor(50 / flag_w)
    down = math.floor(55 / flag_h)
    if across < 1 or down < 1:
        return {"error": "flag is bigger than a labeled fat quarter"}
    per_fq = 2 * across * down
    fq = math.ceil(flags / per_fq)
    return {"flagW": r1(flag_w), "flagH": r1(flag_h), "flags": flags, "perFQ": per_fq, "fq": fq}

def render_fabric(r):
    if "error" in r: return r["error"]
    s = "" if r["fq"] == 1 else "s"
    return (f"A labeled 50 x 55 cm fat quarter nests {r['perFQ']} flags of {num(r['flagW'])} x {num(r['flagH'])}"
            f" cm (two per rectangle), so {r['flags']} flags need {r['fq']} fat quarter{s}.")

def tape_plan(length_cm):
    if not (isinstance(length_cm, (int, float)) and math.isfinite(length_cm) and length_cm > 0):
        return {"error": "string length must be positive"}
    tape_cm = r1(length_cm + 100)
    tape_m = r1(tape_cm / 100)
    return {"lengthCm": r1(length_cm), "tapeCm": tape_cm, "tapeM": tape_m}

def render_tape(r):
    if "error" in r: return r["error"]
    return (f"A {num(r['lengthCm'])} cm span wants {num(r['tapeCm'])} cm of tape ({num(r['tapeM'])}"
            " m) - the flags plus a labeled 50 cm tie at each end.")

cases = []
for l, w, g in [(300, 15, 5), (500, 12, 3), (200, 10, 5), (100, 20, 5), (14, 15, 5),
                (15, 15, 5), (1000, 18, 6), (250, 12.5, 4), (0, 15, 5), (300, 0, 5),
                (300, 15, 0), (-50, 15, 5), (400, 25, 10)]:
    res = flag_count(l, w, g)
    cases.append({"fn": "flagCount", "args": [l, w, g], "result": res, "render": render_flags(res)})
for w, h, n in [(15, 18, 15), (20, 22, 40), (10, 12, 30), (25, 28, 10), (15, 18, 18),
                (15, 18, 19), (51, 18, 5), (15, 56, 5), (0, 18, 15), (15, 0, 15), (15, 18, 0), (12.5, 13.5, 25)]:
    res = fabric_plan(w, h, n)
    cases.append({"fn": "fabricPlan", "args": [w, h, n], "result": res, "render": render_fabric(res)})
for l in [300, 250, 500, 100, 1000, 150.5, 0, -20, 42, 75]:
    res = tape_plan(l)
    cases.append({"fn": "tapePlan", "args": [l], "result": res, "render": render_tape(res)})

with open("expected.json", "w") as f:
    json.dump(cases, f, separators=(",", ":"))
    f.write("\n")
print(len(cases), "cases written")
