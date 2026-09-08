#!/bin/sh
# Self-sequencing: wait for the Phase A census, verify it produced real output,
# then run Phase B. No agent or session watches anything.
while pgrep -f "continua.py" > /dev/null; do sleep 30; done
n=$(grep -cE '^line +[0-9]' continua_phaseA.out)
echo "phase A finished: $n lines scanned"
if [ "$n" -lt 100 ]; then echo "phase A incomplete -- not starting phase B"; exit 1; fi
c=$(wc -l < continua_shard_0.jsonl)
echo "records: $c"
if python3 continua_endpoints.py > continua_phaseB.out 2>&1; then
  echo "phase B done"
else
  echo "PHASE B FAILED (exit $?) -- see continua_phaseB.out"; exit 1
fi
