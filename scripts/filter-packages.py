#!/usr/bin/env python3
"""Keep only packages the ISO can install: name exists in enabled repos and every
dependency resolves to a repo package or a provide. Run inside the build container.

usage: filter-packages.py packages.in kept.out dropped.txt
  pacman -Sql must already list repo packages; pacman -Si gives Depends/Provides.
"""
import re, subprocess, sys

src, kept_out, dropped_out = sys.argv[1:4]
wanted = [l.strip() for l in open(src, encoding="utf-8") if l.strip()]
avail = set(subprocess.run(["pacman", "-Sql"], capture_output=True, text=True, check=True).stdout.split())

info = {}  # name -> (depends list, provides list)
names = [w for w in wanted if w in avail]
for i in range(0, len(names), 200):
    chunk = names[i:i + 200]
    out = subprocess.run(["pacman", "-Si", *chunk], capture_output=True, text=True).stdout
    for block in out.split("\n\n"):
        n = re.search(r"^Name\s*:\s*(\S+)", block, re.M)
        if not n:
            continue
        dep = re.search(r"^Depends On\s*:\s*(.*)$", block, re.M)
        prov = re.search(r"^Provides\s*:\s*(.*)$", block, re.M)
        deps = [] if not dep or dep.group(1).strip() == "None" else dep.group(1).split()
        provs = [] if not prov or prov.group(1).strip() == "None" else prov.group(1).split()
        info[n.group(1)] = (deps, [re.split(r"[<>=]", p)[0] for p in provs])

def base(d):
    return re.split(r"[<>=]", d)[0]

keep = {w for w in names if w in info}
dropped = {w: "not in repos" for w in wanted if w not in keep}

changed = True
while changed:
    changed = False
    provided = set(keep)
    for w in keep:
        provided.update(info[w][1])
    for w in list(keep):
        missing = [base(d) for d in info[w][0] if base(d) not in provided]
        if missing:
            keep.discard(w)
            dropped[w] = "unresolved: " + ", ".join(missing[:4])
            changed = True
            break

with open(kept_out, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(keep)) + "\n")
with open(dropped_out, "w", encoding="utf-8") as f:
    for w in sorted(dropped):
        f.write(f"{w}\t{dropped[w]}\n")
print(f"kept {len(keep)} of {len(wanted)}; dropped {len(dropped)}")
