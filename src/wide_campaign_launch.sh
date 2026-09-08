#!/bin/sh
# Wait for the enumeration to finish writing mixed_q2_configs.pkl, then fan out
# the counting into 8 shards. Self-sequencing so nothing is parked waiting.
while pgrep -f "mixed_q2_full.py" > /dev/null; do sleep 20; done
sz=$(stat -f%z mixed_q2_configs.pkl)
echo "enumeration done, pickle $sz bytes"
if [ "$sz" -lt 1000 ]; then echo "pickle too small -- enumeration failed, not counting"; exit 1; fi
for i in 0 1 2 3 4 5 6 7; do
  nohup python3 wide_campaign.py count $i 8 > wide_campaign_shard_$i.out 2>&1 &
done
echo "8 shards launched"
