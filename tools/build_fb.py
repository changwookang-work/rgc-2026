# -*- coding: utf-8 -*-
"""Generate feedback/index.html (anonymous post-event survey)."""
import json, os, re
ROOT = '/home/claude/rgc-2026'
S = json.load(open(os.path.join(ROOT, 'tools', 'schedule.json'), encoding='utf-8'))
F = json.load(open(os.path.join(ROOT, 'tools', 'fb_i18n.json'), encoding='utf-8'))
ORDER = ['ko', 'en', 'zh-CN', 'zh-TW', 'zh-HK', 'ja', 'th', 'vi', 'ms', 'es']
SESSIONS = [
    {'time': '13:00–14:00', 'deck': 'ipet', 'sp': 'Mavis Chin', 'org': 'IPET'},
    {'time': '14:00–15:00', 'deck': 'panel'},
    {'time': '15:00–16:00', 'deck': 'afpet', 'sp': 'Jennifer Tzeng', 'org': 'AFPET'},
    {'time': '16:00–17:00', 'deck': 'rachel', 'sp': 'Rachel Colant'},
    {'time': '17:00–18:00', 'deck': 'juan', 'sp': 'Juan Miranda', 'org': 'Miranda PR'},
]
PROG = ['timing_breaks', 'interpretation', 'food']
for l in ORDER:
    assert l in F and l in S, l
    assert len(F[l]['program']) == len(PROG), l
data = json.dumps({'order': ORDER, 'S': {l: S[l] for l in ORDER}, 'F': {l: F[l] for l in ORDER},
                   'sessions': SESSIONS, 'progKeys': PROG}, ensure_ascii=False)
html = open(os.path.join(ROOT, 'tools', 'fb_template.html'), encoding='utf-8').read().replace('/*DATA*/', data)
vi = re.search(r"(@font-face\{font-family:'Be Vietnam Pro'.*?\n)(?=:lang\(vi\))", open(os.path.join(ROOT, 'tools', 'template2.html'), encoding='utf-8').read(), re.S)
html = html.replace('/*VIFONTS*/', vi.group(1) if vi else '')
os.makedirs(os.path.join(ROOT, 'feedback'), exist_ok=True)
open(os.path.join(ROOT, 'feedback', 'index.html'), 'w', encoding='utf-8').write(html)
print('feedback/index.html written')
