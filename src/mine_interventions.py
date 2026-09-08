#!/usr/bin/env python3
"""Mine human turns out of session transcripts, cheaply enough to actually read.

The concern that prompted this (user, 2026-08-31): "transcripts might be more
tokens than our session limit allows."  They are — 84.4 MB across 5 files — but
almost none of that is the human.  Three filters bring it inside budget:

    all JSONL lines                 32 186         84.4 MB
    genuine human turns              1 554        476.6 KB    0.58%
    challenge-like turns               588        321.5 KB
    ... long pastes truncated to 400   588         79.2 KB    ~20k tokens   0.09%

"Genuine" excludes tool_result blocks (which carry role=user), system reminders,
task notifications, and slash-command envelopes.  "Challenge-like" keeps turns
containing a question mark or corrective vocabulary, dropping bare
acknowledgements.  Truncation is safe for this purpose because a long paste only
needs its opening to be classified.

Run it again after new sessions to refresh INTERVENTIONS.md.
"""
import json, glob, os, re, sys

SRC = os.path.expanduser('~/.claude/projects/-Users-dmi-cube-compounds')
TRIVIAL = re.compile(r'^(ok|okay|yes|no|y|n|sure|thanks|ty|go|go ahead|please|'
                     r'please do|continue|do it|proceed|next|good|great|nice|'
                     r'yep|yeah|k)\.?$', re.I)
CHALLENGE = re.compile(
    r'\?|\b(wrong|incorrect|mistake|isn\'t|aren\'t|shouldn\'t|didn\'t|doesn\'t|'
    r'i think|i thought|actually|but |however|seems|sounds like|are you sure|'
    r'why |sampl|step size|forgot|remember|recall|already|contradict|inconsist|'
    r'stale|reproduc|unevaluat|artifact|assume|assumption|check|verify|really)\b',
    re.I)


def human_turns(src=SRC):
    out = []
    for fn in sorted(glob.glob(os.path.join(src, '*.jsonl')), key=os.path.getmtime):
        with open(fn, errors='replace') as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get('type') != 'user':
                    continue
                c = (d.get('message') or {}).get('content')
                if isinstance(c, str):
                    txt = c
                elif isinstance(c, list):
                    if any(isinstance(b, dict) and b.get('type') == 'tool_result'
                           for b in c):
                        continue
                    txt = '\n'.join(b.get('text', '') for b in c
                                    if isinstance(b, dict) and b.get('type') == 'text')
                else:
                    continue
                txt = re.sub(r'<system-reminder>.*?</system-reminder>', '', txt,
                             flags=re.S).strip()
                if (not txt or txt.startswith(('<command-', 'Caveat:',
                                               '[SYSTEM NOTIFICATION'))
                        or '<task-notification>' in txt):
                    continue
                out.append((os.path.basename(fn)[:8],
                            (d.get('timestamp') or '')[:10], txt))
    return out


def main():
    turns = human_turns()
    cand = [t for t in turns if not TRIVIAL.match(t[2]) and CHALLENGE.search(t[2])]
    rows = []
    for f, d, b in cand:
        b = re.sub(r'\s+', ' ', b.strip())
        if len(b) > 400:
            b = b[:400] + ' …[+%d chars]' % (len(b) - 400)
        rows.append('%s %s | %s' % (f, d, b))
    txt = '\n'.join(rows)
    open('user_turns_challenges.txt', 'w').write(txt)
    print('%d human turns -> %d challenge-like -> %.1f KB (~%dk tokens)'
          % (len(turns), len(cand), len(txt) / 1024, len(txt) / 4000))


if __name__ == '__main__':
    main()
