# -*- coding: utf-8 -*-
"""Generate index.html: language picker -> Part 1 schedule with per-language PDF downloads."""
import json, os
ROOT = '/home/claude/rgc-2026'
L = json.load(open(os.path.join(ROOT, 'tools', 'schedule.json'), encoding='utf-8'))
ORDER = ['ko', 'en', 'zh-CN', 'zh-TW', 'zh-HK', 'ja', 'th', 'ms', 'es']
FMT = {
    'ipet': 'downloads/ipet/IPET_KTour_2026_%s.pdf',
    'panel': 'downloads/panel/RGC2026_PanelTalk_%s.pdf',
    'afpet': 'downloads/afpet/AFpet_Korea2026_%s.pdf',
    'rachel': 'downloads/rachel/Rachel_US_Grooming_%s.pdf',
    'juan': 'downloads/juan/Juan_Miranda_%s.pdf',
}
SESSIONS = [
    {'time': '13:00–14:00', 'deck': 'ipet', 'sp': 'Mavis Chin', 'org': 'IPET'},
    {'time': '14:00–15:00', 'deck': 'panel'},
    {'time': '15:00–16:00', 'deck': 'afpet', 'sp': 'Jennifer Tzeng', 'org': 'AFPET'},
    {'time': '16:00–17:00', 'deck': 'rachel', 'sp': 'Rachel Colant'},
    {'time': '17:00–18:00', 'deck': 'juan', 'sp': 'Juan Miranda', 'org': 'Miranda PR'},
    {'time': '18:00–19:30', 'deck': None},
]
files, missing = {}, []
for k, fmt in FMT.items():
    files[k] = {}
    for l in ORDER:
        p = fmt % l
        if os.path.exists(os.path.join(ROOT, p)):
            files[k][l] = {'url': '/' + p, 'mb': round(os.path.getsize(os.path.join(ROOT, p)) / 1048576, 1)}
        else:
            missing.append(p)
data = json.dumps({'order': ORDER, 'L': L, 'sessions': SESSIONS, 'files': files}, ensure_ascii=False)
html = open(os.path.join(ROOT, 'tools', 'template2.html'), encoding='utf-8').read().replace('/*DATA*/', data)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html written; missing:', missing)
