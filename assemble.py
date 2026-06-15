#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يجمّع فصول الكورس إلى ملف Markdown شامل + تطبيق HTML تفاعلي (RTL):
قارئ آلي (TTS) · ملاحظات (localStorage) · شرح مصطلحات تلقائي + مسرد ·
حفظ مكان القراءة + شريط تقدّم · تحكّم بحجم الخط · صور بين الأقسام."""
import os, glob, html, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SECTIONS_DIR = os.path.join(BASE, "sections")
MD_OUT = os.path.join(BASE, "الدليل_الشامل_لبناء_نماذج_اللغة.md")
HTML_OUT = os.path.join(BASE, "index.html")

TITLE = "الدليل الكامل لبناء نماذج اللغة الكبيرة من الصفر إلى أحدث المستويات (SOTA)"
SUBTITLE = "كورس عربي شامل من البداية للنهاية: المعمارية، الترميز، البيانات، التدريب، المحاذاة، والنشر — مع أمثلة كود وبدائل ومبرّرات"

def collect():
    files = sorted(glob.glob(os.path.join(SECTIONS_DIR, "*.md")))
    parts = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            txt = fh.read().strip()
        if txt:
            parts.append((os.path.basename(f), txt))
    return parts

def first_heading(txt):
    for line in txt.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return None

def build_markdown(parts):
    today = datetime.date.today().isoformat()
    out = []
    out.append("# " + TITLE)
    out.append("")
    out.append("> " + SUBTITLE)
    out.append("")
    out.append(f"*نسخة مُجمّعة آليًا — {today}. وقفٌ لوجه الله تعالى، متاحٌ للجميع مجانًا. كل المحتوى تعليمي مُعاد صياغته من مصادر عامة.*")
    out.append("")
    out.append("---")
    out.append("")
    out.append("## جدول المحتويات")
    out.append("")
    for i, (_, txt) in enumerate(parts, 1):
        h = first_heading(txt) or f"القسم {i}"
        out.append(f"{i}. {h}")
    out.append("")
    out.append("---")
    out.append("")
    for _, txt in parts:
        out.append(txt.strip())
        out.append("")
        out.append("---")
        out.append("")
    return "\n".join(out)

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=Noto+Kufi+Arabic:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css">
<style>
:root{
  --bg:#0f1117; --panel:#171a23; --panel2:#1d2130; --border:#2a2f3e;
  --text:#e7e9ee; --muted:#9aa3b2; --accent:#6ea8fe; --accent2:#8b5cf6;
  --green:#34d399; --amber:#fbbf24; --code-bg:#11141c; --sidebar-w:340px; --fs:1;
  font-size:17px;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
  font-family:'Cairo','Noto Kufi Arabic',-apple-system,'Segoe UI',Tahoma,sans-serif;
  line-height:1.95;scroll-behavior:smooth}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
#layout{display:flex;min-height:100vh}
/* Sidebar */
#sidebar{width:var(--sidebar-w);min-width:var(--sidebar-w);background:var(--panel);
  border-inline-start:1px solid var(--border);height:100vh;position:sticky;top:0;
  overflow-y:auto;padding:0}
#brand{padding:18px 18px 12px;border-bottom:1px solid var(--border);position:sticky;top:0;
  background:linear-gradient(180deg,var(--panel),rgba(23,26,35,.96));z-index:5;backdrop-filter:blur(6px)}
#brand h1{font-size:18px;margin:0 0 6px;line-height:1.5;color:#fff}
#brand p{font-size:12.5px;color:var(--muted);margin:0 0 8px}
.prog-chip{display:inline-block;font-size:12px;color:var(--green);background:rgba(52,211,153,.1);
  border:1px solid rgba(52,211,153,.3);border-radius:999px;padding:3px 11px}
#search{width:calc(100% - 36px);margin:12px 18px 8px;padding:10px 12px;border-radius:10px;
  border:1px solid var(--border);background:var(--panel2);color:var(--text);font-family:inherit;font-size:14px}
#search:focus{outline:none;border-color:var(--accent)}
#controls{display:flex;flex-wrap:wrap;gap:6px;padding:0 18px 12px;border-bottom:1px solid var(--border)}
.ctl{background:var(--panel2);border:1px solid var(--border);color:var(--text);border-radius:9px;
  padding:6px 10px;font-size:12.5px;cursor:pointer;font-family:inherit}
.ctl:hover{border-color:var(--accent)}
.ctl.on{border-color:var(--green);color:var(--green)}
#toc{list-style:none;margin:0;padding:6px 8px 40px}
#toc li{margin:1px 0}
#toc a{display:block;padding:8px 12px;border-radius:9px;color:var(--muted);font-size:14px;
  border-inline-start:3px solid transparent;transition:.15s}
#toc a:hover{background:var(--panel2);color:var(--text);text-decoration:none}
#toc a.h1{font-weight:700;color:#cdd5e3;font-size:14.5px;margin-top:8px}
#toc a.h2{padding-inline-start:26px;font-size:13px}
#toc a.active{background:rgba(110,168,254,.12);color:#fff;border-inline-start-color:var(--accent)}
#toc a.h1.seen::after{content:" ✓";color:var(--green);font-size:12px}
/* Content */
#main{flex:1;min-width:0;padding:0}
#progressbar{position:fixed;top:0;inset-inline-start:0;height:3px;width:0;
  background:linear-gradient(90deg,var(--accent),var(--accent2));z-index:50;transition:width .1s}
.content{max-width:920px;margin:0 auto;padding:46px 40px 150px;font-size:calc(1rem * var(--fs))}
.hero{background:linear-gradient(135deg,rgba(110,168,254,.10),rgba(139,92,246,.10));
  border:1px solid var(--border);border-radius:18px;padding:30px 30px 24px;margin-bottom:20px}
.hero h1{font-size:1.78em;margin:0 0 12px;line-height:1.5;color:#fff}
.hero p{color:var(--muted);margin:0;font-size:.92em}
.badges{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.badge{background:var(--panel2);border:1px solid var(--border);border-radius:999px;
  padding:5px 13px;font-size:.74em;color:var(--muted)}
/* resume banner */
#resume{display:flex;gap:12px;align-items:center;background:rgba(110,168,254,.10);
  border:1px solid rgba(110,168,254,.4);border-radius:14px;padding:12px 16px;margin-bottom:18px;font-size:.86em}
#resume b{color:#fff}
#resume .sp{flex:1;color:#cdd5e3}
#resume button{background:var(--accent);color:#08121f;border:none;border-radius:9px;padding:7px 14px;cursor:pointer;font-family:inherit;font-size:.95em;font-weight:600}
#resume .x{background:transparent;color:var(--muted);font-weight:400;padding:7px 8px}
/* onboarding tip */
#tip{display:flex;gap:12px;align-items:flex-start;background:rgba(52,211,153,.08);
  border:1px solid rgba(52,211,153,.35);border-radius:14px;padding:14px 16px;margin-bottom:26px;font-size:.84em;color:#cdd5e3}
#tip b{color:#7ee0a8}
#tip button{margin-inline-start:auto;background:transparent;border:none;color:var(--muted);cursor:pointer;font-size:18px;flex-shrink:0}
.content h1{font-size:1.53em;margin:56px 0 6px;padding:0 0 14px;border-bottom:2px solid var(--border);
  color:#fff;line-height:1.6;scroll-margin-top:18px}
.content h2{font-size:1.24em;margin:38px 0 14px;color:#cdd5e3;scroll-margin-top:18px}
.content h3{font-size:1.04em;margin:26px 0 10px;color:var(--accent);scroll-margin-top:18px}
.content h4{font-size:.95em;margin:20px 0 8px;color:#b8c0d0}
.content p{margin:12px 0}
.content ul,.content ol{padding-inline-start:26px;margin:12px 0}
.content li{margin:7px 0}
.content blockquote{border-inline-start:4px solid var(--accent);background:var(--panel);
  margin:18px 0;padding:12px 18px;border-radius:0 10px 10px 0;color:#cdd5e3}
.content blockquote p{margin:6px 0}
.content code{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;
  padding:2px 7px;font-size:.83em;font-family:'SF Mono',Menlo,Consolas,monospace;direction:ltr;
  unicode-bidi:embed;color:#ffd9a0}
.content pre{background:var(--code-bg);border:1px solid var(--border);border-radius:14px;
  padding:0;margin:18px 0;overflow:hidden;direction:ltr;text-align:left}
.content pre code{display:block;background:transparent;border:none;border-radius:0;padding:18px 20px;
  overflow-x:auto;font-size:.80em;line-height:1.7;color:#e7e9ee;white-space:pre}
.content table{border-collapse:collapse;width:100%;margin:18px 0;font-size:.82em;display:block;overflow-x:auto}
.content th,.content td{border:1px solid var(--border);padding:9px 12px;text-align:right}
.content th{background:var(--panel2);color:#fff;font-weight:700}
.content tr:nth-child(even){background:rgba(255,255,255,.02)}
.content hr{border:none;border-top:1px solid var(--border);margin:48px 0}
.content strong{color:#fff}
.content img{max-width:100%;height:auto;display:block;margin:22px auto;border:1px solid var(--border);
  border-radius:14px;background:#0b0d13;padding:6px}
/* callout headings */
.content h3.cs-summary,.content h3.cs-exercise{display:inline-block;padding:7px 16px;border-radius:11px;margin-top:30px}
.content h3.cs-summary{background:rgba(52,211,153,.12);color:#7ee0a8;border:1px solid rgba(52,211,153,.4)}
.content h3.cs-exercise{background:rgba(251,191,36,.12);color:#fbbf24;border:1px solid rgba(251,191,36,.4)}
.content h3.cs-summary + ul,.content h3.cs-summary + ol{background:rgba(52,211,153,.05);
  border-inline-start:3px solid rgba(52,211,153,.45);padding:14px 30px;border-radius:0 10px 10px 0}
.content h3.cs-exercise + p,.content h3.cs-exercise + ul,.content h3.cs-exercise + ol{background:rgba(251,191,36,.05);
  border-inline-start:3px solid rgba(251,191,36,.45);padding:14px 30px;border-radius:0 10px 10px 0}
/* term explanation boxes */
.term-note{display:flex;gap:10px;background:rgba(139,92,246,.07);border:1px solid rgba(139,92,246,.35);
  border-radius:12px;padding:11px 14px;margin:12px 0;font-size:.85em}
.term-note .tn-ic{flex-shrink:0;font-size:1.1em}
.term-note .tn-head{font-size:.85em;color:#b79bff;font-weight:700;margin-bottom:5px}
.term-note .tn-item{color:#cdd5e3;margin:4px 0;line-height:1.8}
.term-note .tn-item b{color:#cbb6ff}
body.hide-terms .term-note{display:none}
/* per-section toolbar */
.sec-tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 22px}
.chip{background:var(--panel2);border:1px solid var(--border);border-radius:999px;padding:4px 12px;font-size:.74em;color:var(--muted)}
.stool{background:var(--panel2);border:1px solid var(--border);border-radius:999px;padding:5px 14px;
  font-size:.78em;color:var(--text);cursor:pointer;font-family:inherit;transition:.15s}
.stool:hover{border-color:var(--accent);color:#fff}
.stool.has-note{border-color:var(--amber);color:var(--amber)}
.stool.reading{border-color:var(--green);color:var(--green)}
.tts-reading{background:rgba(110,168,254,.16)!important;border-radius:6px;box-shadow:0 0 0 3px rgba(110,168,254,.18)}
/* audio bar */
#audiobar{position:fixed;bottom:18px;left:50%;transform:translateX(-50%);z-index:70;
  display:flex;gap:10px;align-items:center;background:var(--panel);border:1px solid var(--border);
  border-radius:14px;padding:8px 12px;box-shadow:0 10px 30px rgba(0,0,0,.5);max-width:94vw;flex-wrap:wrap}
#audiobar button{background:var(--panel2);border:1px solid var(--border);color:var(--text);
  width:38px;height:38px;border-radius:10px;cursor:pointer;font-size:15px}
#audiobar button:hover{border-color:var(--accent)}
#ab-title{font-size:12.5px;color:var(--muted);max-width:240px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#audiobar label{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:5px}
#audiobar select,#audiobar input[type=range]{background:var(--panel2);border:1px solid var(--border);
  color:var(--text);border-radius:8px;font-family:inherit;font-size:12px;max-width:150px}
/* side panels (notes + glossary) */
.fab{position:fixed;bottom:24px;z-index:60;width:54px;height:54px;border-radius:50%;
  color:#fff;border:none;font-size:22px;cursor:pointer;box-shadow:0 6px 22px rgba(0,0,0,.45)}
#notes-fab{inset-inline-end:24px;background:linear-gradient(135deg,var(--accent),var(--accent2))}
#notes-fab .dot{position:absolute;top:8px;inset-inline-end:8px;width:11px;height:11px;border-radius:50%;background:var(--amber);display:none}
#panel-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:75}
.sidepanel{position:fixed;top:0;inset-inline-end:0;height:100vh;width:min(440px,93vw);z-index:80;
  background:var(--panel);border-inline-start:1px solid var(--border);box-shadow:-12px 0 40px rgba(0,0,0,.5);
  display:flex;flex-direction:column}
.sidepanel header{display:flex;align-items:center;justify-content:space-between;padding:18px;border-bottom:1px solid var(--border)}
.sidepanel header strong{font-size:16px;color:#fff}
.sidepanel header button{background:transparent;border:none;color:var(--muted);font-size:20px;cursor:pointer}
.notes-current{padding:16px 18px;border-bottom:1px solid var(--border)}
.notes-current label{font-size:12px;color:var(--muted)}
#note-section-title{font-size:14px;color:var(--accent);margin:4px 0 10px;font-weight:600;line-height:1.5}
#note-text{width:100%;min-height:150px;resize:vertical;background:var(--panel2);border:1px solid var(--border);
  border-radius:11px;color:var(--text);font-family:inherit;font-size:14.5px;line-height:1.8;padding:12px}
#note-text:focus{outline:none;border-color:var(--accent)}
.note-status{font-size:12px;color:var(--green);height:16px;margin-top:6px}
.notes-actions{display:flex;gap:8px;flex-wrap:wrap;padding:14px 18px;border-bottom:1px solid var(--border)}
.notes-actions button{flex:1;min-width:90px;background:var(--panel2);border:1px solid var(--border);color:var(--text);
  border-radius:10px;padding:9px;font-size:13px;cursor:pointer;font-family:inherit}
.notes-actions button:hover{border-color:var(--accent)}
#notes-clear:hover{border-color:#ff7a7a;color:#ff9a9a}
.notes-list-wrap{flex:1;overflow-y:auto;padding:14px 18px}
.notes-list-wrap>strong{font-size:13px;color:var(--muted)}
#notes-list{list-style:none;margin:10px 0 0;padding:0}
#notes-list li{background:var(--panel2);border:1px solid var(--border);border-radius:11px;padding:11px 13px;margin-bottom:9px}
#notes-list .nl-title{font-size:12.5px;color:var(--accent);cursor:pointer;font-weight:600;line-height:1.5}
#notes-list .nl-snippet{font-size:13px;color:var(--muted);margin:6px 0 0;max-height:46px;overflow:hidden}
#notes-list .nl-del{float:left;background:transparent;border:none;color:var(--muted);cursor:pointer;font-size:14px}
#notes-list .nl-del:hover{color:#ff9a9a}
.notes-empty{color:var(--muted);font-size:13px;margin-top:10px}
/* glossary panel */
#gloss-search{margin:14px 18px;width:calc(100% - 36px);padding:10px 12px;border-radius:10px;border:1px solid var(--border);
  background:var(--panel2);color:var(--text);font-family:inherit;font-size:14px}
#gloss-search:focus{outline:none;border-color:var(--accent)}
#gloss-list{list-style:none;margin:0;padding:0 18px 30px;overflow-y:auto;flex:1}
#gloss-list li{padding:11px 0;border-bottom:1px solid var(--border);font-size:14px;line-height:1.85}
#gloss-list b{color:#cbb6ff;display:block;margin-bottom:2px}
#gloss-list span{color:var(--muted);font-size:13.5px}
#topbtn{position:fixed;bottom:24px;inset-inline-start:24px;background:var(--accent);color:#08121f;
  border:none;width:46px;height:46px;border-radius:50%;font-size:20px;cursor:pointer;display:none;
  box-shadow:0 6px 20px rgba(0,0,0,.4);z-index:40}
#menubtn{display:none}
@media (max-width:980px){
  #sidebar{position:fixed;inset-inline-end:0;transform:translateX(100%);transition:.25s;z-index:90;box-shadow:-8px 0 30px rgba(0,0,0,.5)}
  #sidebar.open{transform:translateX(0)}
  #menubtn{display:flex;position:fixed;top:14px;inset-inline-end:14px;z-index:61;background:var(--accent);
    color:#08121f;border:none;border-radius:10px;width:46px;height:46px;font-size:22px;cursor:pointer;align-items:center;justify-content:center}
  .content{padding:64px 18px 160px}
}
@media print{
  #sidebar,#audiobar,.sidepanel,#panel-backdrop,#notes-fab,#topbtn,#menubtn,#progressbar,.sec-tools,#tip,#resume{display:none!important}
  .content{max-width:100%}
}
</style>
</head>
<body>
<div id="progressbar"></div>
<button id="menubtn" aria-label="القائمة">☰</button>
<div id="layout">
  <aside id="sidebar">
    <div id="brand">
      <h1>الدليل الكامل لنماذج اللغة</h1>
      <p>من الصفر إلى أحدث المستويات — كورس تفاعلي · وقفٌ لله</p>
      <span class="prog-chip" id="prog-chip">التقدّم: 0/24 فصلاً</span>
    </div>
    <input id="search" type="text" placeholder="🔍 ابحث في الفهرس..." autocomplete="off">
    <div id="controls">
      <button id="btn-gloss" class="ctl">📖 المسرد</button>
      <button id="btn-terms" class="ctl on" title="إظهار/إخفاء شرح المصطلحات التلقائي">🔤 شرح المصطلحات</button>
      <button id="fs-dec" class="ctl" title="تصغير الخط">أ−</button>
      <button id="fs-inc" class="ctl" title="تكبير الخط">أ+</button>
    </div>
    <ul id="toc"></ul>
  </aside>
  <main id="main">
    <div class="content">
      <div class="hero">
        <h1>__TITLE__</h1>
        <p>__SUBTITLE__</p>
        <div class="badges">
          <span class="badge">24 فصلاً</span>
          <span class="badge">🔊 قارئ آلي</span>
          <span class="badge">📝 ملاحظات تُحفظ</span>
          <span class="badge">📖 شرح المصطلحات</span>
          <span class="badge">📍 يحفظ مكانك</span>
          <span class="badge">وقفٌ لوجه الله</span>
        </div>
      </div>
      <div id="tip">
        <span>✨</span>
        <div><b>ميزات تفاعلية:</b> اضغط <b>🔊 استمع</b> ليُقرأ القسم صوتيًا، ودوّن <b>📝 ملاحظاتك</b> (تُحفظ تلقائيًا)، وستُشرح <b>المصطلحات الجديدة</b> أسفل الفقرات، ويُحفظ <b>مكان قراءتك</b> تلقائيًا لتُكمل لاحقًا.</div>
        <button id="tip-close" title="إخفاء">✕</button>
      </div>
      <div id="content"></div>
    </div>
  </main>
</div>

<div id="audiobar" hidden>
  <button id="ab-pp" title="إيقاف مؤقت/متابعة">⏸</button>
  <button id="ab-stop" title="إيقاف">⏹</button>
  <span id="ab-title">—</span>
  <label>السرعة <input id="ab-rate" type="range" min="0.7" max="1.5" step="0.1" value="1"></label>
  <select id="ab-voice" title="الصوت"></select>
  <button id="ab-close" title="إغلاق">✕</button>
</div>

<div id="panel-backdrop" hidden></div>

<aside id="notes" class="sidepanel" hidden>
  <header><strong>📝 ملاحظاتي وأسئلتي</strong><button id="notes-close" title="إغلاق">✕</button></header>
  <div class="notes-current">
    <label>القسم الحالي:</label>
    <div id="note-section-title">—</div>
    <textarea id="note-text" placeholder="اكتب ملاحظاتك أو أسئلتك حول هذا القسم هنا... (تُحفظ تلقائيًا)"></textarea>
    <div class="note-status" id="note-status"></div>
  </div>
  <div class="notes-actions">
    <button id="notes-export">⬇ تصدير (JSON)</button>
    <button id="notes-import">⬆ استيراد</button>
    <input id="notes-file" type="file" accept="application/json" hidden>
    <button id="notes-clear">🗑 مسح الكل</button>
  </div>
  <div class="notes-list-wrap">
    <strong>كل ملاحظاتي</strong>
    <ul id="notes-list"></ul>
  </div>
</aside>

<aside id="glossary" class="sidepanel" hidden>
  <header><strong>📖 مسرد المصطلحات</strong><button id="gloss-close" title="إغلاق">✕</button></header>
  <input id="gloss-search" type="text" placeholder="🔍 ابحث عن مصطلح..." autocomplete="off">
  <ul id="gloss-list"></ul>
</aside>

<button id="notes-fab" class="fab" title="ملاحظاتي">📝<span class="dot" id="fab-dot"></span></button>
<button id="topbtn" title="أعلى">↑</button>

<script type="text/markdown" id="md">__MARKDOWN__</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>
__GLOSSARY__
(function(){
  'use strict';
  var raw = document.getElementById('md').textContent;
  if(window.marked){ marked.setOptions({gfm:true, breaks:false}); }
  var contentEl = document.getElementById('content');
  contentEl.innerHTML = window.marked ? marked.parse(raw) : '<pre>'+raw.replace(/</g,'&lt;')+'</pre>';
  if(window.hljs){ document.querySelectorAll('pre code').forEach(function(b){ try{hljs.highlightElement(b);}catch(e){} }); }

  var heads = Array.prototype.slice.call(contentEl.querySelectorAll('h1, h2'));
  var h1s = Array.prototype.slice.call(contentEl.querySelectorAll('h1'));

  /* ---------- TOC ---------- */
  var toc = document.getElementById('toc');
  var idx=0;
  heads.forEach(function(h){
    idx++; var id='sec-'+idx; h.id=id;
    var a=document.createElement('a');
    a.href='#'+id; a.textContent=h.textContent;
    a.className = h.tagName.toLowerCase()==='h1' ? 'h1' : 'h2';
    a.addEventListener('click',function(e){
      e.preventDefault();
      document.getElementById(id).scrollIntoView({behavior:'smooth',block:'start'});
      if(window.innerWidth<=980){ document.getElementById('sidebar').classList.remove('open'); }
      history.replaceState(null,'','#'+id);
    });
    var li=document.createElement('li'); li.appendChild(a); toc.appendChild(li);
  });
  function tocLink(id){ return toc.querySelector('a[href="#'+id+'"]'); }

  function chapterEls(h1){ var els=[]; var n=h1.nextElementSibling; while(n && n.tagName!=='H1'){ els.push(n); n=n.nextElementSibling;} return els; }
  function wordCount(els){ var w=0; els.forEach(function(el){ if(el.tagName==='PRE') return; w += (el.textContent.trim().match(/\S+/g)||[]).length; }); return w; }

  /* ---------- callout headings ---------- */
  contentEl.querySelectorAll('h3').forEach(function(h){
    var t=h.textContent;
    if(t.indexOf('الخلاصة')>-1 || t.indexOf('النقاط الأساسية')>-1) h.classList.add('cs-summary');
    else if(t.indexOf('تمرين')>-1) h.classList.add('cs-exercise');
  });

  /* ---------- per-chapter toolbar (reading time + listen + note) ---------- */
  h1s.forEach(function(h1){
    var mins=Math.max(1, Math.round(wordCount(chapterEls(h1))/180));
    var bar=document.createElement('div'); bar.className='sec-tools';
    var chip=document.createElement('span'); chip.className='chip'; chip.textContent='⏱ ~'+mins+' دقيقة قراءة';
    var listen=document.createElement('button'); listen.className='stool listen'; listen.textContent='🔊 استمع للقسم';
    listen.addEventListener('click',function(){ TTS.start(h1); });
    h1.__listenBtn=listen;
    var note=document.createElement('button'); note.className='stool note'; note.textContent='📝 ملاحظة'; note.setAttribute('data-id',h1.id);
    note.addEventListener('click',function(){ openNotes(h1.id, h1.textContent); });
    bar.appendChild(chip); bar.appendChild(listen); bar.appendChild(note);
    h1.parentNode.insertBefore(bar, h1.nextSibling);
  });

  /* ---------- auto term explanations (first occurrence) ---------- */
  GLOSSARY.forEach(function(g){
    var latin=(g.k||[]).filter(function(s){return /[A-Za-z]/.test(s);});
    if(latin.length){
      var pat=latin.map(function(s){return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}).sort(function(a,b){return b.length-a.length;}).join('|');
      g._re=new RegExp('(?:^|[^A-Za-z0-9_])(?:'+pat+')(?![A-Za-z0-9_])');
    }
  });
  function injectTerms(){
    var seen={};
    var blocks=Array.prototype.slice.call(contentEl.querySelectorAll('p, li, blockquote'));
    blocks.forEach(function(el){
      var txt=el.textContent; if(!txt) return;
      var hits=[];
      for(var i=0;i<GLOSSARY.length;i++){
        var g=GLOSSARY[i];
        if(seen[g.n]||!g._re) continue;
        if(g._re.test(txt)){ hits.push(g); seen[g.n]=true; }
      }
      if(hits.length){
        var box=document.createElement('div'); box.className='term-note';
        var h='<span class="tn-ic">📖</span><div class="tn-body"><div class="tn-head">مصطلحات جديدة في هذه الفقرة</div>';
        hits.forEach(function(g){ h+='<div class="tn-item"><b>'+g.n+'</b> — '+g.d+'</div>'; });
        h+='</div>';
        box.innerHTML=h;
        if(el.tagName==='LI') el.appendChild(box);
        else el.parentNode.insertBefore(box, el.nextSibling);
      }
    });
  }
  if(localStorage.getItem('arllm_terms_off')==='1'){ document.body.classList.add('hide-terms'); document.getElementById('btn-terms').classList.remove('on'); }
  setTimeout(injectTerms, 30);
  document.getElementById('btn-terms').addEventListener('click',function(){
    document.body.classList.toggle('hide-terms');
    var off=document.body.classList.contains('hide-terms');
    this.classList.toggle('on',!off);
    try{localStorage.setItem('arllm_terms_off', off?'1':'0');}catch(e){}
  });

  /* ---------- glossary panel ---------- */
  var glist=document.getElementById('gloss-list');
  GLOSSARY.slice().sort(function(a,b){return a.n.localeCompare(b.n);}).forEach(function(g){
    var li=document.createElement('li');
    li.innerHTML='<b>'+g.n+'</b><span>'+g.d+'</span>';
    glist.appendChild(li);
  });
  document.getElementById('gloss-search').addEventListener('input',function(){
    var q=this.value.trim().toLowerCase();
    Array.prototype.forEach.call(glist.children,function(li){
      li.style.display = (!q || li.textContent.toLowerCase().indexOf(q)>-1) ? '' : 'none';
    });
  });

  /* ---------- panels open/close ---------- */
  var backdrop=document.getElementById('panel-backdrop');
  function closePanels(){ document.getElementById('notes').hidden=true; document.getElementById('glossary').hidden=true; backdrop.hidden=true; }
  backdrop.addEventListener('click',closePanels);
  document.getElementById('btn-gloss').addEventListener('click',function(){ closePanels(); document.getElementById('glossary').hidden=false; backdrop.hidden=false; document.getElementById('gloss-search').focus(); });
  document.getElementById('gloss-close').addEventListener('click',closePanels);

  /* ---------- TTS ---------- */
  var synth=window.speechSynthesis;
  var TTS={ items:[],i:0,playing:false,title:'',voice:null,rate:1,curEl:null,voices:[],
    pickVoices:function(){ this.voices=synth?synth.getVoices():[]; var ar=this.voices.filter(function(v){return (v.lang||'').toLowerCase().indexOf('ar')===0;});
      var sel=document.getElementById('ab-voice'); sel.innerHTML=''; var list=ar.length?ar:this.voices;
      if(!ar.length){ var o=document.createElement('option'); o.value=''; o.textContent='(صوت افتراضي)'; sel.appendChild(o); }
      list.forEach(function(v){ var o=document.createElement('option'); o.value=v.name; o.textContent=v.name+' ('+v.lang+')'; sel.appendChild(o); });
      this.voice=ar.length?ar[0]:null; if(this.voice)sel.value=this.voice.name; },
    chunk:function(el,text){ var t=text.replace(/\s+/g,' ').trim(); if(!t)return; var ss=t.split(/(?<=[\.\!\?؟،:])\s/); var buf=''; var self=this;
      ss.forEach(function(s){ if((buf+' '+s).length>180){ if(buf)self.items.push({el:el,text:buf}); buf=s;} else buf=buf?buf+' '+s:s; }); if(buf)self.items.push({el:el,text:buf}); },
    build:function(h1){ this.items=[]; var self=this; chapterEls(h1).forEach(function(el){
      if(['PRE','TABLE','HR','IMG','DIV'].indexOf(el.tagName)>-1) return;
      if(el.tagName==='UL'||el.tagName==='OL'){ Array.prototype.slice.call(el.children).forEach(function(li){ self.chunk(li,li.textContent); }); }
      else self.chunk(el,el.textContent); }); },
    start:function(h1){ if(!synth){ alert('متصفحك لا يدعم القارئ الآلي. جرّب Chrome أو Safari حديثًا.'); return; }
      this.stop(); this.build(h1); this.title=h1.textContent; document.getElementById('ab-title').textContent='🔊 '+this.title;
      this.i=0; this.playing=true; document.getElementById('audiobar').hidden=false; document.getElementById('ab-pp').textContent='⏸';
      clearReadingBtns(); if(h1.__listenBtn)h1.__listenBtn.classList.add('reading'); this.speak(); },
    speak:function(){ if(this.i>=this.items.length){ this.finish(); return; } var it=this.items[this.i]; this.highlight(it.el);
      var u=new SpeechSynthesisUtterance(it.text); u.lang=this.voice?this.voice.lang:'ar-SA'; if(this.voice)u.voice=this.voice; u.rate=this.rate;
      var self=this; u.onend=function(){ if(self.playing){ self.i++; self.speak(); } }; u.onerror=function(){ if(self.playing){ self.i++; self.speak(); } }; synth.speak(u); },
    highlight:function(el){ if(this.curEl)this.curEl.classList.remove('tts-reading'); this.curEl=el; if(el){ el.classList.add('tts-reading');
      var r=el.getBoundingClientRect(); if(r.top<80||r.bottom>window.innerHeight-120) el.scrollIntoView({behavior:'smooth',block:'center'}); } },
    pauseResume:function(){ if(!synth)return; if(this.playing){ synth.pause(); this.playing=false; document.getElementById('ab-pp').textContent='▶'; }
      else { synth.resume(); this.playing=true; document.getElementById('ab-pp').textContent='⏸'; } },
    finish:function(){ this.playing=false; if(this.curEl)this.curEl.classList.remove('tts-reading'); clearReadingBtns(); document.getElementById('ab-pp').textContent='▶'; },
    stop:function(){ this.playing=false; if(synth){try{synth.cancel();}catch(e){}} if(this.curEl)this.curEl.classList.remove('tts-reading'); clearReadingBtns(); } };
  function clearReadingBtns(){ document.querySelectorAll('.stool.reading').forEach(function(b){b.classList.remove('reading');}); }
  if(synth){ TTS.pickVoices(); if(typeof synth.onvoiceschanged!=='undefined'){ synth.onvoiceschanged=function(){TTS.pickVoices();}; } }
  document.getElementById('ab-pp').addEventListener('click',function(){TTS.pauseResume();});
  document.getElementById('ab-stop').addEventListener('click',function(){TTS.stop();document.getElementById('audiobar').hidden=true;});
  document.getElementById('ab-close').addEventListener('click',function(){TTS.stop();document.getElementById('audiobar').hidden=true;});
  document.getElementById('ab-rate').addEventListener('input',function(){TTS.rate=parseFloat(this.value);});
  document.getElementById('ab-voice').addEventListener('change',function(){ var v=TTS.voices.filter(function(x){return x.name===this.value;}.bind(this))[0]; if(v)TTS.voice=v; });

  /* ---------- Notes ---------- */
  var NK='arllm_notes_v1';
  function loadNotes(){ try{return JSON.parse(localStorage.getItem(NK))||{};}catch(e){return {};} }
  function saveNotes(o){ try{localStorage.setItem(NK,JSON.stringify(o));}catch(e){} }
  var notes=loadNotes(); var activeId=null, activeTitle='';
  var ta=document.getElementById('note-text'), nstatus=document.getElementById('note-status'),
      nlist=document.getElementById('notes-list'), nsectitle=document.getElementById('note-section-title');
  function openNotes(id,title){ closePanels(); activeId=id||currentChapterId(); var h=document.getElementById(activeId);
    activeTitle=title||(h?h.textContent:'ملاحظة عامة'); nsectitle.textContent=activeTitle;
    ta.value=(notes[activeId]&&notes[activeId].text)||''; nstatus.textContent='';
    document.getElementById('notes').hidden=false; backdrop.hidden=false; renderNotesList(); ta.focus(); }
  var saveTimer=null;
  ta.addEventListener('input',function(){ if(!activeId)return; var val=ta.value; if(saveTimer)clearTimeout(saveTimer);
    saveTimer=setTimeout(function(){ if(val.trim())notes[activeId]={title:activeTitle,text:val,ts:Date.now()}; else delete notes[activeId];
      saveNotes(notes); nstatus.textContent='✓ حُفظ تلقائيًا'; setTimeout(function(){nstatus.textContent='';},1500); renderNotesList(); refreshNoteIndicators(); },350); });
  function renderNotesList(){ var keys=Object.keys(notes).sort(function(a,b){return (notes[b].ts||0)-(notes[a].ts||0);});
    if(!keys.length){ nlist.innerHTML='<div class="notes-empty">لا ملاحظات بعد. اكتب أول ملاحظة في الأعلى ✍️</div>'; return; }
    nlist.innerHTML=''; keys.forEach(function(k){ var n=notes[k]; var li=document.createElement('li');
      var del=document.createElement('button'); del.className='nl-del'; del.textContent='🗑';
      del.addEventListener('click',function(){ delete notes[k]; saveNotes(notes); renderNotesList(); refreshNoteIndicators(); if(k===activeId)ta.value=''; });
      var t=document.createElement('div'); t.className='nl-title'; t.textContent=n.title||k;
      t.addEventListener('click',function(){ var el=document.getElementById(k); if(el)el.scrollIntoView({behavior:'smooth',block:'start'}); openNotes(k,n.title); });
      var s=document.createElement('div'); s.className='nl-snippet'; s.textContent=n.text||'';
      li.appendChild(del); li.appendChild(t); li.appendChild(s); nlist.appendChild(li); }); }
  function refreshNoteIndicators(){ document.querySelectorAll('.stool.note').forEach(function(b){ var id=b.getAttribute('data-id');
      if(notes[id])b.classList.add('has-note'); else b.classList.remove('has-note'); });
    document.getElementById('fab-dot').style.display=Object.keys(notes).length?'block':'none'; }
  document.getElementById('notes-close').addEventListener('click',closePanels);
  document.getElementById('notes-fab').addEventListener('click',function(){ openNotes(null,null); });
  document.getElementById('notes-export').addEventListener('click',function(){ var blob=new Blob([JSON.stringify(notes,null,2)],{type:'application/json'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='ملاحظاتي_الكورس.json'; a.click(); });
  document.getElementById('notes-import').addEventListener('click',function(){ document.getElementById('notes-file').click(); });
  document.getElementById('notes-file').addEventListener('change',function(e){ var f=e.target.files[0]; if(!f)return; var rd=new FileReader();
    rd.onload=function(){ try{ var o=JSON.parse(rd.result); Object.keys(o).forEach(function(k){notes[k]=o[k];}); saveNotes(notes); renderNotesList(); refreshNoteIndicators(); nstatus.textContent='✓ تم الاستيراد'; }catch(err){ alert('ملف غير صالح'); } };
    rd.readAsText(f); });
  document.getElementById('notes-clear').addEventListener('click',function(){ if(confirm('مسح كل الملاحظات نهائيًا؟')){ notes={}; saveNotes(notes); ta.value=''; renderNotesList(); refreshNoteIndicators(); } });
  refreshNoteIndicators();

  /* ---------- reading position + progress ---------- */
  var PK='arllm_progress_v1';
  function loadProg(){ try{var p=JSON.parse(localStorage.getItem(PK))||{}; if(!p.seen)p.seen={}; return p;}catch(e){return {seen:{}};} }
  function saveProg(){ try{localStorage.setItem(PK,JSON.stringify(prog));}catch(e){} }
  var prog=loadProg();
  var chapterH1s=h1s.filter(function(h){return /^القسم/.test(h.textContent.trim());});
  var totalCh=chapterH1s.length||24;
  var progChip=document.getElementById('prog-chip');
  function updateProgressUI(){ var n=Object.keys(prog.seen).length; progChip.textContent='التقدّم: '+n+'/'+totalCh+' فصلاً';
    chapterH1s.forEach(function(h){ var a=tocLink(h.id); if(a)a.classList.toggle('seen',!!prog.seen[h.id]); }); }
  function currentChapterId(){ var cur=chapterH1s.length?chapterH1s[0].id:(h1s[0]&&h1s[0].id); chapterH1s.forEach(function(h){ if(h.getBoundingClientRect().top<160)cur=h.id; }); return cur; }
  function currentChapterEl(){ var id=currentChapterId(); return document.getElementById(id); }
  updateProgressUI();

  /* resume banner */
  if(prog.y && prog.y>400 && prog.title){
    var rb=document.createElement('div'); rb.id='resume';
    rb.innerHTML='<span>📍</span><span class="sp">تابع القراءة من: <b></b></span><button id="rb-go">متابعة</button><button class="x" id="rb-x">✕</button>';
    rb.querySelector('b').textContent=prog.title;
    var contentWrap=document.querySelector('.content');
    contentWrap.insertBefore(rb, document.getElementById('tip'));
    document.getElementById('rb-go').addEventListener('click',function(){ window.scrollTo({top:prog.y,behavior:'smooth'}); rb.remove(); });
    document.getElementById('rb-x').addEventListener('click',function(){ rb.remove(); });
  }

  /* ---------- font size ---------- */
  var fs=parseFloat(localStorage.getItem('arllm_fs')||'1'); if(isNaN(fs))fs=1;
  function applyFs(){ document.documentElement.style.setProperty('--fs', fs); try{localStorage.setItem('arllm_fs',String(fs));}catch(e){} }
  applyFs();
  document.getElementById('fs-inc').addEventListener('click',function(){ fs=Math.min(1.6, Math.round((fs+0.1)*10)/10); applyFs(); });
  document.getElementById('fs-dec').addEventListener('click',function(){ fs=Math.max(0.8, Math.round((fs-0.1)*10)/10); applyFs(); });

  /* ---------- search ---------- */
  var search=document.getElementById('search');
  search.addEventListener('input',function(){ var q=this.value.trim().toLowerCase();
    toc.querySelectorAll('li').forEach(function(li){ li.style.display=(!q||li.textContent.toLowerCase().indexOf(q)>-1)?'':'none'; }); });

  /* ---------- scroll: active link, progress bar, save position ---------- */
  var links=Array.prototype.slice.call(toc.querySelectorAll('a'));
  var bar=document.getElementById('progressbar');
  var topbtn=document.getElementById('topbtn');
  var saveScrollTimer=null;
  function onScroll(){
    var st=window.scrollY||document.documentElement.scrollTop;
    var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;
    bar.style.width=(h>0?(st/h*100):0)+'%';
    topbtn.style.display=st>500?'block':'none';
    var cur=null; heads.forEach(function(hd){ if(hd.getBoundingClientRect().top<140)cur=hd.id; });
    links.forEach(function(a){ a.classList.toggle('active', a.getAttribute('href')==='#'+cur); });
    if(saveScrollTimer)clearTimeout(saveScrollTimer);
    saveScrollTimer=setTimeout(function(){ prog.y=st; var ch=currentChapterEl();
      if(ch){ prog.id=ch.id; prog.title=ch.textContent; if(!prog.seen[ch.id]){ prog.seen[ch.id]=true; updateProgressUI(); } }
      saveProg(); },700);
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();

  topbtn.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var menubtn=document.getElementById('menubtn');
  menubtn && menubtn.addEventListener('click',function(){document.getElementById('sidebar').classList.toggle('open');});

  /* ---------- keyboard navigation ---------- */
  function gotoChapter(delta){ var list=chapterH1s; if(!list.length)return; var ci=0;
    list.forEach(function(h,k){ if(h.getBoundingClientRect().top<160)ci=k; });
    var ni=Math.min(list.length-1, Math.max(0, ci+delta)); list[ni].scrollIntoView({behavior:'smooth',block:'start'}); }
  document.addEventListener('keydown',function(e){ var tag=(e.target&&e.target.tagName)||''; if(tag==='INPUT'||tag==='TEXTAREA')return;
    if(e.key==='ArrowLeft'){ gotoChapter(1); } else if(e.key==='ArrowRight'){ gotoChapter(-1); } });

  /* ---------- onboarding tip ---------- */
  var tip=document.getElementById('tip');
  if(localStorage.getItem('arllm_tip_hidden')==='1') tip.style.display='none';
  document.getElementById('tip-close').addEventListener('click',function(){ tip.style.display='none'; try{localStorage.setItem('arllm_tip_hidden','1');}catch(e){} });

  window.addEventListener('beforeunload',function(){ if(synth){try{synth.cancel();}catch(e){}} prog.y=window.scrollY||0; saveProg(); });
})();
</script>
</body>
</html>
"""

GLOSSARY_JS = r"""var GLOSSARY = [
 {n:'GPT', k:['GPT','GPT-2','GPT-3','GPT-4'], d:'عائلة نماذج OpenAI التوليدية (decoder-only) التي رسّخت أسلوب «توقّع الرمز التالي».'},
 {n:'BERT', k:['BERT'], d:'نموذج Google (2018) من نوع encoder ثنائي الاتجاه، للفهم لا التوليد؛ مرجع تاريخي.'},
 {n:'T5', k:['T5'], d:'نموذج Google (2019) «Text-to-Text Transfer Transformer»؛ منه جاءت مجموعة بيانات C4 وقواعد تنظيف النص.'},
 {n:'Llama', k:['Llama','LLaMA','Llama-3','Llama 3','Llama-3.1'], d:'عائلة نماذج Meta المفتوحة؛ مرجع شائع لمعمارية decoder-only مع GQA وRoPE.'},
 {n:'Mistral', k:['Mistral','Mistral-7B'], d:'نموذج Mistral AI (7B) المفتوح المعروف بكفاءته؛ يُستخدم كثيرًا كمولّد لإعادة صياغة البيانات.'},
 {n:'Mixtral', k:['Mixtral','Mixtral-8x7B'], d:'نموذج Mistral من نوع خليط خبراء (MoE) 8×7B؛ استُخدم لتوليد مجموعة Cosmopedia.'},
 {n:'DeepSeek', k:['DeepSeek','DeepSeek-V2','DeepSeek-V3','DeepSeek V3','DeepSeekMoE','DeepSeek-R1','DeepSeekMath'], d:'عائلة نماذج DeepSeek الصينية المفتوحة؛ مصدر ابتكارات MLA وموازنة MoE بلا خسارة وMTP وFP8 وGRPO.'},
 {n:'Qwen', k:['Qwen','Qwen3','Qwen3.5','Qwen2','Qwen3-Next'], d:'عائلة نماذج Alibaba المفتوحة؛ مرجع لمنهج البيانات على مستوى المثيل والمنهج ثلاثي المراحل.'},
 {n:'OLMo', k:['OLMo','OLMo 2','OLMo 3','OLMo-2','OLMo-3'], d:'نماذج معهد Allen AI المفتوحة بالكامل (الكود والبيانات والوصفة)؛ أهم مرجع تعليمي شفّاف.'},
 {n:'Gemma', k:['Gemma'], d:'نماذج Google المفتوحة الخفيفة.'},
 {n:'Phi', k:['Phi','phi-1.5','Phi-4'], d:'عائلة Microsoft الصغيرة المدرّبة على بيانات اصطناعية «بأسلوب الكتب المدرسية».'},
 {n:'Nemotron', k:['Nemotron','Nemotron-CC','Nemotron-Nano'], d:'نماذج وبيانات NVIDIA؛ مرجع لإعادة صياغة البيانات الاصطناعية والمعمارية الهجينة.'},
 {n:'Moonlight', k:['Moonlight'], d:'نموذج Moonshot (MoE 3B/16B) دُرّب بمحسّن Muon على 5.7T رمز لإثبات فعاليته على نطاق واسع.'},
 {n:'Kimi', k:['Kimi','Kimi K2'], d:'نماذج Moonshot AI؛ استخدمت محسّن Muon في الإنتاج.'},
 {n:'Chinchilla', k:['Chinchilla'], d:'ورقة DeepMind (2022) التي أسّست قانون التوازن الأمثل بين حجم النموذج وعدد الرموز (~20 رمزًا لكل معامل).'},
 {n:'BloombergGPT', k:['BloombergGPT'], d:'نموذج مالي دُرّب من الصفر على بيانات مالية؛ مثال على أن التخصّص الكامل غالبًا أسوأ قيمةً من التدريب المستمر.'},
 {n:'Galactica', k:['Galactica'], d:'نموذج Meta العلمي؛ مثال آخر على مخاطر التدريب على مجال ضيّق.'},
 {n:'PaLM', k:['PaLM'], d:'نموذج Google الكبير؛ مرجع تاريخي لقوانين القياس.'},
 {n:'Falcon', k:['Falcon'], d:'نموذج TII الإماراتي المفتوح؛ مرتبط بمجموعة بيانات RefinedWeb.'},
 {n:'MAP-Neo', k:['MAP-Neo'], d:'نموذج مفتوح استُخدم كخط أساس قارنته DCLM.'},
 {n:'Common Crawl', k:['Common Crawl','CommonCrawl'], d:'أرشيف ويب عام ضخم (بيتابايت) يُحدَّث شهريًا؛ الأساس الخام لمعظم مجموعات التدريب.'},
 {n:'FineWeb', k:['FineWeb'], d:'مجموعة ويب مفتوحة (~15T رمز) من HuggingFace بخط أنابيب تصفية مُختبَر تجريبيًا.'},
 {n:'FineWeb-Edu', k:['FineWeb-Edu'], d:'مجموعة فرعية من FineWeb (~1.3T) مُرشّحة بمصنّف «قيمة تعليمية»؛ قوية لاختبارات المعرفة.'},
 {n:'DCLM', k:['DCLM','DataComp-LM','DCLM-Baseline','DCLM-POOL'], d:'معيار/ساحة DataComp-LM لمقارنة استراتيجيات تنسيق البيانات؛ ومنه مصنّف fastText الشهير.'},
 {n:'Dolma', k:['Dolma'], d:'مجموعة AI2 المفتوحة (~3T) بأدواتها؛ تُدرَّب عليها نماذج OLMo.'},
 {n:'The Pile', k:['The Pile'], d:'مجموعة EleutherAI المبكرة المتنوّعة (ويب + كتب + كود + علمي).'},
 {n:'RedPajama', k:['RedPajama'], d:'مجموعة مفتوحة تعيد إنتاج وصفة بيانات Llama.'},
 {n:'SlimPajama', k:['SlimPajama'], d:'نسخة مُزالة التكرار ومُنظّفة من RedPajama.'},
 {n:'C4', k:['C4'], d:'«Colossal Clean Crawled Corpus» من مشروع T5؛ منها جاءت «قواعد C4» الشهيرة للتنظيف.'},
 {n:'The Stack', k:['The Stack','Stack v1','Stack v2','Stack-Edu'], d:'مجموعة كود BigCode من GitHub/Software Heritage؛ أساس StarCoder.'},
 {n:'StarCoder', k:['StarCoder','StarCoderData','StarCoder2','StarCoder2Data'], d:'نماذج/بيانات كود BigCode المفتوحة.'},
 {n:'OpenWebMath', k:['OpenWebMath'], d:'مجموعة صفحات ويب رياضية (~15B رمز).'},
 {n:'Proof-Pile-2', k:['Proof-Pile-2','Proof-Pile','AlgebraicStack'], d:'مجموعة رياضية (~55B) تشمل أوراقًا وكودًا رياضيًا.'},
 {n:'Cosmopedia', k:['Cosmopedia'], d:'مجموعة اصطناعية مفتوحة (~25B) بأسلوب الكتب المدرسية وُلّدت بـ Mixtral.'},
 {n:'Ultra-FineWeb', k:['Ultra-FineWeb'], d:'نسخة مُحسّنة من FineWeb باستراتيجية «تحقق فعّال» (verification-based).'},
 {n:'RefinedWeb', k:['RefinedWeb'], d:'مجموعة ويب مُصفّاة جيدًا (Falcon) أثبتت أن الويب وحده قد يضاهي المصادر المنسقة.'},
 {n:'MixtureVitae', k:['MixtureVitae'], d:'مجموعة «المسموح أولًا» (permissive-first) برخص منفتحة.'},
 {n:'peS2o', k:['peS2o'], d:'مجموعة أوراق علمية بصيغة منسّقة ضمن Dolma.'},
 {n:'FineWeb-2', k:['FineWeb-2'], d:'امتداد FineWeb لما يقارب ألف لغة (تشمل العربية).'},
 {n:'OpenHermes', k:['OpenHermes','OpenHermes-2.5','OH-2.5'], d:'مجموعة تعليمات عالية الجودة استُخدمت كأمثلة إيجابية لتدريب مصنّف DCLM.'},
 {n:'WARC', k:['WARC'], d:'صيغة الاستجابات الخام في Common Crawl؛ يُفضّل إعادة استخراج النص منها على WET الجاهز.'},
 {n:'WET', k:['WET'], d:'صيغة النص الجاهز المستخرج في Common Crawl؛ جودته أقل من إعادة الاستخراج من WARC.'},
 {n:'Transformer', k:['Transformer'], d:'المعمارية الأساس لكل النماذج الحديثة (انتباه + تغذية أمامية + وصلات متبقية + تطبيع).'},
 {n:'RoPE', k:['RoPE'], d:'التشفير الموضعي الدوّار؛ يدمج الموضع بتدوير المتجهات ويعمّم لأطوال أطول.'},
 {n:'RMSNorm', k:['RMSNorm'], d:'تطبيع يعتمد على جذر متوسط المربعات فقط؛ أرخص وأكثر استقرارًا من LayerNorm.'},
 {n:'LayerNorm', k:['LayerNorm'], d:'التطبيع الكلاسيكي (متوسط + تباين)؛ استبدله الأحدث غالبًا بـ RMSNorm.'},
 {n:'SwiGLU', k:['SwiGLU','SiLU'], d:'دالة تغذية أمامية ببوّابة (Gated Linear Unit) بتنشيط SiLU؛ جودة أعلى لكل معامل.'},
 {n:'MHA', k:['MHA','Multi-Head Attention'], d:'الانتباه متعدد الرؤوس الكلاسيكي؛ مكلف ذاكرةً (KV لكل رأس).'},
 {n:'MQA', k:['MQA','Multi-Query'], d:'انتباه برأس K/V واحد مشترك؛ يوفّر ذاكرة لكن قد يضرّ الجودة.'},
 {n:'GQA', k:['GQA','Grouped-Query'], d:'مجموعات رؤوس تتشارك K/V؛ التوازن الآمن (يستخدمه Llama).'},
 {n:'MLA', k:['MLA','Latent Attention'], d:'انتباه DeepSeek يضغط K/V لفضاء كامن منخفض الرتبة؛ أقل ذاكرةً وجودة أعلى.'},
 {n:'KV cache', k:['KV cache','KV-cache'], d:'ذاكرة تخزّن مفاتيح/قيم الرموز السابقة لتسريع التوليد؛ عنق الزجاجة في الاستدلال.'},
 {n:'FlashAttention', k:['FlashAttention'], d:'خوارزمية انتباه لا تجسّد مصفوفة n×n كاملة (tiling في الذاكرة السريعة).'},
 {n:'MoE', k:['MoE','Mixture-of-Experts'], d:'خليط الخبراء؛ يُفعّل جزءًا صغيرًا من الشبكة لكل رمز عبر بوّاب/راوتر.'},
 {n:'Mamba', k:['Mamba','Mamba-2'], d:'نموذج فضاء حالة (State-Space) خطّي بديل/مكمّل للانتباه في السياق الطويل.'},
 {n:'MTP', k:['MTP','Multi-Token Prediction'], d:'التنبؤ بعدة رموز للأمام؛ إشارة تدريب أكثف + تمكين فك التشفير التخميني.'},
 {n:'YaRN', k:['YaRN'], d:'تقنية لتمديد نافذة السياق عبر إعادة تحجيم RoPE.'},
 {n:'QK-norm', k:['QK-norm','QK-Normalization'], d:'تطبيع Q وK قبل الانتباه لمنع تضخّم اللوجيتس وتثبيت التدريب.'},
 {n:'BPE', k:['BPE','Byte-Pair'], d:'الترميز بدمج أكثر أزواج الرموز شيوعًا تكراريًا.'},
 {n:'BBPE', k:['BBPE','byte-level BPE'], d:'BPE على مستوى البايت؛ يتعامل مع أي مدخل بلا مشكلة «خارج المفردات».'},
 {n:'SentencePiece', k:['SentencePiece'], d:'أداة ترميز شائعة تدعم BPE وUnigram.'},
 {n:'WordPiece', k:['WordPiece'], d:'خوارزمية ترميز (BERT) بديلة لـ BPE.'},
 {n:'Unigram', k:['Unigram'], d:'نموذج ترميز احتمالي (بديل لـ BPE).'},
 {n:'Deduplication', k:['deduplication','dedup'], d:'إزالة المستندات المكرّرة/المتشابهة لتقليل الهدر والحفظ وتشويه التوزيع.'},
 {n:'MinHash', k:['MinHash'], d:'تقدير سريع لتشابه Jaccard عبر توقيعات مضغوطة لكشف شبه المكرّرات.'},
 {n:'LSH', k:['LSH'], d:'تجزئة حساسة للموضع تجمع المتشابهات في «دلاء» للمقارنة الفعّالة.'},
 {n:'SemDeDup', k:['SemDeDup'], d:'إزالة تكرار دلالية (تشابه التضمينات لا الألفاظ).'},
 {n:'Bloom filter', k:['Bloom filter','BFF'], d:'بنية احتمالية لكشف التكرار بكفاءة على نطاق ضخم.'},
 {n:'fastText', k:['fastText'], d:'مصنّف خفيف سريع (يعمل على المعالج) يُستخدم لتحديد اللغة وتصفية الجودة.'},
 {n:'Gopher', k:['Gopher'], d:'نموذج/قواعد DeepMind؛ منها «قواعد Gopher» التجريبية للتصفية.'},
 {n:'DoReMi', k:['DoReMi'], d:'طريقة لتعلّم أوزان خلط المجالات عبر نموذج وكيل صغير (Group DRO).'},
 {n:'RegMix', k:['RegMix'], d:'اختيار خلطة البيانات بالانحدار من نماذج صغيرة كثيرة.'},
 {n:'WRAP', k:['WRAP'], d:'«Web Rephrase Augmented Pre-training»؛ إعادة صياغة الويب اصطناعيًا للتدريب.'},
 {n:'ProX', k:['ProX'], d:'تنقيح البيانات بمعاملته كبرمجة (إبقاء/حذف/تطبيع spans).'},
 {n:'RefineX', k:['RefineX'], d:'تقطير تنقيحات الخبير لبرامج تعديل دنيا يطبّقها نموذج صغير سريع.'},
 {n:'BeyondWeb', k:['BeyondWeb'], d:'دراسة منهجية لقياس البيانات الاصطناعية خلصت إلى «لا رصاصة فضية».'},
 {n:'Model collapse', k:['model collapse'], d:'تدهور التنوّع عند التدريب المتكرر على مخرجات النموذج نفسه.'},
 {n:'Decontamination', k:['decontamination'], d:'إزالة تسرّب بيانات الاختبار من بيانات التدريب لضمان صدق النتائج.'},
 {n:'n-gram', k:['n-gram'], d:'تتابع من n وحدات؛ يُستخدم في كشف التكرار والتلوّث.'},
 {n:'AdamW', k:['AdamW','Adam'], d:'المحسّن القياسي (زخم + RMS + اضمحلال وزن).'},
 {n:'Muon', k:['Muon'], d:'محسّن 2025 يعامل الأوزان كمصفوفات (تعامد Newton-Schulz)؛ نحو ~2× كفاءة على AdamW.'},
 {n:'μP', k:['μP','muP','maximal-update'], d:'تحجيم يسمح بضبط فرط-المعاملات على نماذج صغيرة ونقلها للكبيرة.'},
 {n:'FP8', k:['FP8'], d:'دقة 8-بت لتدريب أرخص دون مساس يُذكر بالجودة (DeepSeek-V3).'},
 {n:'WSD', k:['WSD','Warmup-Stable-Decay'], d:'جدول معدّل تعلّم: إحماء ثم استقرار طويل ثم انحلال سريع (مناسب للتلدين).'},
 {n:'Annealing', k:['annealing'], d:'مرحلة الانحلال السريع لمعدّل التعلّم؛ أعلى عائد لحقن أفضل البيانات وأكثرها مجالية.'},
 {n:'Mid-training', k:['mid-training'], d:'مرحلة وسيطة عالية الجودة ترفع وزن المجال والاستدلال قبل التلدين.'},
 {n:'Scaling laws', k:['scaling laws'], d:'علاقات تنبؤية بين الحساب والحجم والبيانات والأداء.'},
 {n:'SFT', k:['SFT','Supervised Fine-Tuning'], d:'الضبط الدقيق بالإشراف على أزواج تعليمات-استجابة عالية الجودة.'},
 {n:'RLHF', k:['RLHF'], d:'التعلّم المعزّز من تغذية بشرية (نموذج مكافأة ثم PPO).'},
 {n:'PPO', k:['PPO'], d:'خوارزمية تعلّم معزّز شائعة تُستخدم في RLHF.'},
 {n:'DPO', k:['DPO','Direct Preference'], d:'تحسين مباشر للتفضيل دون نموذج مكافأة؛ أبسط وأكثر استقرارًا من PPO.'},
 {n:'GRPO', k:['GRPO'], d:'تحسين سياسة نسبي للمجموعة (DeepSeek) دون شبكة قيمة؛ أساس تدريب الاستدلال.'},
 {n:'RLVR', k:['RLVR'], d:'تعلّم معزّز بمكافآت قابلة للتحقّق (رياضيات/كود) لتدريب الاستدلال الطويل.'},
 {n:'Chain-of-Thought', k:['Chain-of-Thought','CoT','Long-CoT'], d:'سلسلة خطوات تفكير صريحة يولّدها النموذج قبل الجواب النهائي.'},
 {n:'Constitutional AI', k:['Constitutional AI','RLAIF'], d:'محاذاة بتغذية من الذكاء الاصطناعي وفق مبادئ مكتوبة بدل التغذية البشرية.'},
 {n:'FSDP', k:['FSDP','Fully Sharded'], d:'تقسيم المعاملات والتدرّجات وحالات المحسّن عبر البطاقات لتوفير الذاكرة.'},
 {n:'ZeRO', k:['ZeRO'], d:'تقنية DeepSpeed لتقسيم حالة التدريب (مراحل 1/2/3).'},
 {n:'Megatron', k:['Megatron','Megatron-LM'], d:'مكتبة NVIDIA لتوازي الموتّر وخط الأنابيب.'},
 {n:'DeepSpeed', k:['DeepSpeed'], d:'مكتبة Microsoft لتدريب موزّع وكفؤ الذاكرة.'},
 {n:'vLLM', k:['vLLM'], d:'محرّك خدمة استدلال عالي الإنتاجية (PagedAttention + تجميع مستمر).'},
 {n:'PagedAttention', k:['PagedAttention'], d:'إدارة الـ KV cache بصفحات كذاكرة افتراضية لمنع التشظّي ورفع الإنتاجية.'},
 {n:'Speculative decoding', k:['speculative decoding','Speculative'], d:'نموذج مسوّدة صغير يقترح رموزًا يتحقّق منها الكبير دفعةً لتسريع التوليد.'},
 {n:'Quantization', k:['quantization','GPTQ','AWQ'], d:'خفض دقة الأوزان (INT8/INT4/FP8) لتقليل الحجم وزيادة السرعة مقابل جودة أقل قليلًا.'},
 {n:'Distillation', k:['distillation'], d:'تدريب نموذج صغير على محاكاة نموذج كبير لنقل قدرته.'},
 {n:'MFU', k:['MFU'], d:'معدّل استخدام الـ FLOPs الفعلي مقابل النظري — مقياس كفاءة التدريب.'},
 {n:'Perplexity', k:['perplexity'], d:'الحيرة — مقياس لمدى صعوبة توقّع النموذج للنص (أقل = أفضل).'},
 {n:'Embedding', k:['embedding'], d:'التضمين — تمثيل عددي كثيف للرموز/النصوص.'},
 {n:'Pretraining', k:['pretraining'], d:'التدريب المسبق من الصفر على بيانات ضخمة لبناء القدرة العامة.'},
 {n:'Fine-tuning', k:['fine-tuning'], d:'الضبط الدقيق — تكييف نموذج مدرَّب على مهمة أو مجال أضيق.'},
 {n:'Continual pretraining', k:['continual pretraining','continual pre-training'], d:'متابعة التدريب المسبق على بيانات مجال جديد مع الحفاظ على القدرة العامة.'},
 {n:'Ablation', k:['ablation'], d:'المقارنة التجريبية — تغيير عنصر واحد وقياس أثره لاختيار الأفضل.'},
 {n:'datatrove', k:['datatrove'], d:'مكتبة HuggingFace لبناء خطوط بيانات ضخمة (استخراج/تصفية/إزالة تكرار) — وراء FineWeb.'},
 {n:'NeMo Curator', k:['NeMo Curator'], d:'خط أنابيب NVIDIA لتنسيق البيانات (تجميع مصنّفات + إعادة صياغة) — وراء Nemotron-CC.'},
 {n:'lighteval', k:['lighteval'], d:'حزمة تقييم سريعة تُستخدم في تجارب المقارنة الصغيرة.'}
];
"""

def build_html(md_text):
    safe = md_text.replace("</script>", "<\\/script>")
    out = HTML_TEMPLATE
    out = out.replace("__GLOSSARY__", GLOSSARY_JS)
    out = out.replace("__TITLE__", html.escape(TITLE))
    out = out.replace("__SUBTITLE__", html.escape(SUBTITLE))
    out = out.replace("__MARKDOWN__", safe)
    return out

def main():
    parts = collect()
    if not parts:
        print("لا توجد فصول بعد في", SECTIONS_DIR)
        return
    md = build_markdown(parts)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write(md)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(build_html(md))
    words = len(md.split())
    print(f"عدد الفصول: {len(parts)}")
    print(f"عدد الكلمات التقريبي: {words}")
    print(f"عدد المصطلحات في المسرد: {GLOSSARY_JS.count(chr(123)+'n:')}")
    print(f"Markdown -> {MD_OUT}")
    print(f"HTML app -> {HTML_OUT}")

if __name__ == "__main__":
    main()
