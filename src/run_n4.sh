#!/bin/sh
# Self-contained launcher for the n = 4 structure program.
#
# Everything here is designed so that the SSH connection is NEVER load-bearing:
# the job is detached, checkpoints per work unit, and resumes by skipping units
# whose output file already exists. Killing the terminal, losing the network or
# rebooting costs at most one unit.
#
#   ./run_n4.sh            build, gate, and launch detached
#   ./run_n4.sh status     how far along
#   ./run_n4.sh report     the results table
#   ./run_n4.sh stop       stop the workers (progress is kept)
#
# Re-running after an interruption resumes. It is safe to run twice.

set -e
cd "$(dirname "$0")"
WORKERS="${WORKERS:-6}"          # 6 is the sweet spot on 8 cores; override freely
LOG=n4_run.log

build() {
  if [ ! -x ./cube_regions_n ] || [ cube_regions.cpp -nt ./cube_regions_n ]; then
    echo "building cube_regions_n for $(uname -m) ..."
    c++ -O2 -std=c++17 -o cube_regions_n cube_regions.cpp
  fi
}

case "${1:-run}" in
  status)
    d=$(ls -d n4_run_* 2>/dev/null | head -1)
    [ -z "$d" ] && { echo "not started"; exit 0; }
    echo "run dir: $d"
    echo "phase 1 units done: $(ls "$d"/parts/p1_*.json 2>/dev/null | wc -l) / 60"
    echo "phase 2 cells done: $(ls "$d"/parts/p2_*.json 2>/dev/null | wc -l)"
    echo "workers alive:      $(pgrep -f n4_program.py | wc -l)"
    tail -3 "$LOG" 2>/dev/null
    ;;
  report)
    python3 n4_program.py report
    ;;
  stop)
    pkill -f n4_program.py || true
    pkill -f "caffeinate.*n4" || true
    echo "stopped; progress is checkpointed, re-run ./run_n4.sh to resume"
    ;;
  *)
    build
    # The gate is not optional: a rebuild on a different architecture and
    # compiler must reproduce known counts before any new result is believed.
    python3 n4_program.py gate

    echo "launching $WORKERS workers, detached, sleep inhibited ..."
    # caffeinate -dis: no idle sleep, no disk sleep, no system sleep. A laptop
    # will otherwise suspend a multi-hour job the moment it is left alone.
    nohup caffeinate -dis sh -c '
      for i in $(seq 0 '"$((WORKERS-1))"'); do
        python3 n4_program.py phase1 --shard $i --of '"$WORKERS"' &
      done
      wait
      for i in $(seq 0 '"$((WORKERS-1))"'); do
        python3 n4_program.py phase2 --shard $i --of '"$WORKERS"' &
      done
      wait
      echo "ALL PHASES COMPLETE"
      python3 n4_program.py report
    ' >> "$LOG" 2>&1 &
    echo "started. progress: ./run_n4.sh status   results: ./run_n4.sh report"
    echo "log: $LOG"
    ;;
esac
