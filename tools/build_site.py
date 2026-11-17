# -*- coding: utf-8 -*-
"""Generate index.html (language picker) for the RENADOG GLOBAL CONNECT 2026 presentation downloads."""
import json, os, sys
sys.path.insert(0, '/home/claude/tw')
ROOT = '/home/claude/rgc-2026'
LANGS = [  # code, native name, html lang
    ('ko', '한국어', 'ko'), ('zh-TW', '繁體中文（台灣）', 'zh-Hant-TW'), ('zh-HK', '繁體中文（廣東話）', 'zh-Hant-HK'),
    ('zh-CN', '简体中文', 'zh-Hans'), ('th', 'ภาษาไทย', 'th'), ('en', 'English', 'en'),
    ('ja', '日本語', 'ja'), ('ms', 'Bahasa Melayu', 'ms'), ('es', 'Español', 'es')]
UI = {
 'en': ('Choose your language', 'Download the presentations in your language (PDF)', 'Download PDF'),
 'ko': ('언어를 선택하세요', '내 언어로 된 발표자료(PDF)를 내려받으세요', 'PDF 다운로드'),
 'ja': ('言語を選択してください', 'ご自身の言語の発表資料（PDF）をダウンロード', 'PDFをダウンロード'),
 'zh-TW': ('請選擇語言', '下載您所選語言的簡報（PDF）', '下載 PDF'),
 'zh-HK': ('請揀語言', '下載你揀嘅語言版本簡報（PDF）', '下載 PDF'),
 'zh-CN': ('请选择语言', '下载您所选语言的演示文稿（PDF）', '下载 PDF'),
 'th': ('เลือกภาษาของคุณ', 'ดาวน์โหลดสไลด์นำเสนอ (PDF) ในภาษาของคุณ', 'ดาวน์โหลด PDF'),
 'ms': ('Pilih bahasa anda', 'Muat turun pembentangan (PDF) dalam bahasa anda', 'Muat turun PDF'),
 'es': ('Elige tu idioma', 'Descarga las presentaciones (PDF) en tu idioma', 'Descargar PDF'),
}
import cover
AF_TITLE = {l: cover.TXT[l][0].replace('|', ' ') for l in cover.TXT}
AF_TITLE['zh-TW'] = '保持初心，走得長久'
ipet_src = json.load(open('/home/claude/ktour/w/to_translate.json'))
t1 = {i['k']: i['t'] for i in ipet_src}
IP_TITLE = {'zh-CN': t1[1] + t1[2]}
for l, _, _ in LANGS:
    p = '/home/claude/ktour/w/tr/%s.json' % l
    if os.path.exists(p):
        t = json.load(open(p))
        fx = '/home/claude/ktour/w/tr/verify_fixes.json'
        if os.path.exists(fx): t.update(json.load(open(fx)).get(l, {}))
        IP_TITLE[l] = (t['1'] + ('' if l in ('zh-TW','zh-HK','zh-CN','ja') else ' ') + t['2']).replace('\n', ' ')
RC_TITLE = {'en': json.load(open('/home/claude/rachel/to_translate.json'))[0]['t']}
for l, _, _ in LANGS:
    pth = '/home/claude/rachel/tr/%s.json' % l
    if l != 'en' and os.path.exists(pth):
        t = json.load(open(pth))
        fx = '/home/claude/rachel/tr/verify_fixes.json'
        if os.path.exists(fx): t.update(json.load(open(fx)).get(l, {}))
        RC_TITLE[l] = t['1'].replace('\n', ' ')
decks = []
for key, label, sub, fmt, titles in (
        ('afpet', 'AFpet · Taiwan', 'Jennifer Tzeng', 'downloads/afpet/AFpet_Korea2026_%s.pdf', AF_TITLE),
        ('ipet', 'Shanghai Ipet · China', 'Shanghai Ipet Co., Ltd.', 'downloads/ipet/IPET_KTour_2026_%s.pdf', IP_TITLE),
        ('rachel', 'Groom Curriculum · USA', 'Rachel Colant', 'downloads/rachel/Rachel_US_Grooming_%s.pdf', RC_TITLE)):
    files = {}
    for l, _, _ in LANGS:
        f = fmt % l
        if os.path.exists(os.path.join(ROOT, f)):
            files[l] = {'url': f, 'mb': round(os.path.getsize(os.path.join(ROOT, f)) / 1048576, 1), 'title': titles.get(l, '')}
    decks.append({'key': key, 'label': label, 'sub': sub, 'files': files})
data = json.dumps({'langs': [{'code': c, 'name': n, 'html': h} for c, n, h in LANGS], 'ui': UI, 'decks': decks}, ensure_ascii=False)
html = open(os.path.join(ROOT, 'tools', 'template.html'), encoding='utf-8').read().replace('/*DATA*/', data)
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(html)
print('index.html written;', {d['key']: len(d['files']) for d in decks})
