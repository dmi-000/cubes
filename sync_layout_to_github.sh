#!/bin/sh
# Apply the 2026-09-08 layout reorganisation to the publish tree.
#   sh sync_layout_to_github.sh [PROJECT_DIR] [PUBLISH_DIR]
# defaults: ~/cube-compounds and ~/cube-compounds/github
#
# `git mv a b` is just `mv a b` + `git add a b`.  Git stores CONTENT and infers
# renames at diff time, so one `git add -A` after plain moves gives an identical
# commit to 1278 `git mv` calls, instantly.
#
# Moves ONLY what MOVE_LOG.json records, to the destination it records, so both
# trees end up identical.  Files the project kept at its root (127 opened by
# scripts by bare name) are not in the log and are left alone here too.
# STAGES but does not commit or push.
set -e
PROJ="${1:-$HOME/cube-compounds}"; PUB="${2:-$PROJ/github}"; LOG="$PROJ/MOVE_LOG.json"
[ -f "$LOG" ] || { echo "no MOVE_LOG.json at $LOG"; exit 1; }
cd "$PUB" || { echo "no publish dir at $PUB"; exit 1; }
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "$PUB is not a git repo"; exit 1; }
[ -z "$(git status --porcelain)" ] || { echo "publish tree dirty -- commit or stash first"; git status --short; exit 1; }
mkdir -p src runs data viewers transcripts
python3 - "$LOG" <<'PY'
import json, os, shutil, sys, collections
log=json.load(open(sys.argv[1])); done=collections.Counter(); missing=0
for name,dest in log["moved"]:
    if os.path.isfile(name):
        os.makedirs(dest,exist_ok=True); shutil.move(name,os.path.join(dest,name)); done[dest]+=1
    else: missing+=1
for f in os.listdir('.'):
    if f.endswith('.err') and os.path.isfile(f):
        shutil.move(f,os.path.join('runs',f)); done['runs (.err)']+=1
print("  moved:",dict(done)); print("  in log but not published here:",missing,"(expected: curated tree)")
PY
for d in src runs data viewers transcripts; do rmdir "$d" 2>/dev/null || true; done
git add -A
echo "renames detected: $(git diff --cached --name-status -M | grep -c '^R' || true)"
git status --short | head -12
echo; echo "then:  cd $PUB && git commit -m 'Reorganise into src/ runs/ data/ viewers/ transcripts/' && git push --verbose origin main"
