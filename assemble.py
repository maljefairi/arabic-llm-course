#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يجمّع فصول الكورس إلى ملف Markdown شامل + تطبيق HTML تفاعلي (RTL)
مع قارئ آلي (Web Speech API)، نظام ملاحظات (localStorage)، صور، وتحسينات تخطيط."""
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
    out.append(f"*نسخة مُجمّعة آليًا — {today}. كل المحتوى تعليمي مُعاد صياغته من مصادر عامة؛ الأسماء والأرقام للتوضيح والتحقق.*")
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
  --green:#34d399; --amber:#fbbf24; --code-bg:#11141c; --sidebar-w:340px;
}
*{box-sizing:border-box}
[hidden]{display:none!important}
html,body{margin:0;padding:0;background:var(--bg);color:var(--text);
  font-family:'Cairo','Noto Kufi Arabic',-apple-system,'Segoe UI',Tahoma,sans-serif;
  font-size:17px;line-height:1.95;scroll-behavior:smooth}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
#layout{display:flex;min-height:100vh}
/* Sidebar */
#sidebar{width:var(--sidebar-w);min-width:var(--sidebar-w);background:var(--panel);
  border-inline-start:1px solid var(--border);height:100vh;position:sticky;top:0;
  overflow-y:auto;padding:0}
#brand{padding:20px 18px 14px;border-bottom:1px solid var(--border);position:sticky;top:0;
  background:linear-gradient(180deg,var(--panel),rgba(23,26,35,.96));z-index:5;backdrop-filter:blur(6px)}
#brand h1{font-size:18px;margin:0 0 6px;line-height:1.5;color:#fff}
#brand p{font-size:12.5px;color:var(--muted);margin:0}
#search{width:calc(100% - 36px);margin:12px 18px;padding:10px 12px;border-radius:10px;
  border:1px solid var(--border);background:var(--panel2);color:var(--text);font-family:inherit;font-size:14px}
#search:focus{outline:none;border-color:var(--accent)}
#toc{list-style:none;margin:0;padding:6px 8px 40px}
#toc li{margin:1px 0}
#toc a{display:block;padding:8px 12px;border-radius:9px;color:var(--muted);font-size:14px;
  border-inline-start:3px solid transparent;transition:.15s}
#toc a:hover{background:var(--panel2);color:var(--text);text-decoration:none}
#toc a.h1{font-weight:700;color:#cdd5e3;font-size:14.5px;margin-top:8px}
#toc a.h2{padding-inline-start:26px;font-size:13px}
#toc a.active{background:rgba(110,168,254,.12);color:#fff;border-inline-start-color:var(--accent)}
/* Content */
#main{flex:1;min-width:0;padding:0}
#progressbar{position:fixed;top:0;inset-inline-start:0;height:3px;width:0;
  background:linear-gradient(90deg,var(--accent),var(--accent2));z-index:50;transition:width .1s}
.content{max-width:920px;margin:0 auto;padding:46px 40px 140px}
.hero{background:linear-gradient(135deg,rgba(110,168,254,.10),rgba(139,92,246,.10));
  border:1px solid var(--border);border-radius:18px;padding:30px 30px 24px;margin-bottom:24px}
.hero h1{font-size:30px;margin:0 0 12px;line-height:1.5;color:#fff}
.hero p{color:var(--muted);margin:0;font-size:15.5px}
.badges{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.badge{background:var(--panel2);border:1px solid var(--border);border-radius:999px;
  padding:5px 13px;font-size:12.5px;color:var(--muted)}
/* onboarding tip */
#tip{display:flex;gap:12px;align-items:flex-start;background:rgba(52,211,153,.08);
  border:1px solid rgba(52,211,153,.35);border-radius:14px;padding:14px 16px;margin-bottom:30px;font-size:14px;color:#cdd5e3}
#tip b{color:#7ee0a8}
#tip button{margin-inline-start:auto;background:transparent;border:none;color:var(--muted);cursor:pointer;font-size:18px;flex-shrink:0}
.content h1{font-size:26px;margin:56px 0 6px;padding:0 0 14px;border-bottom:2px solid var(--border);
  color:#fff;line-height:1.6;scroll-margin-top:20px}
.content h2{font-size:21px;margin:38px 0 14px;color:#cdd5e3;scroll-margin-top:20px}
.content h3{font-size:17.5px;margin:26px 0 10px;color:var(--accent);scroll-margin-top:20px}
.content h4{font-size:16px;margin:20px 0 8px;color:#b8c0d0}
.content p{margin:12px 0}
.content ul,.content ol{padding-inline-start:26px;margin:12px 0}
.content li{margin:7px 0}
.content blockquote{border-inline-start:4px solid var(--accent);background:var(--panel);
  margin:18px 0;padding:12px 18px;border-radius:0 10px 10px 0;color:#cdd5e3}
.content blockquote p{margin:6px 0}
.content code{background:var(--code-bg);border:1px solid var(--border);border-radius:6px;
  padding:2px 7px;font-size:14px;font-family:'SF Mono',Menlo,Consolas,monospace;direction:ltr;
  unicode-bidi:embed;color:#ffd9a0}
.content pre{background:var(--code-bg);border:1px solid var(--border);border-radius:14px;
  padding:0;margin:18px 0;overflow:hidden;direction:ltr;text-align:left}
.content pre code{display:block;background:transparent;border:none;border-radius:0;padding:18px 20px;
  overflow-x:auto;font-size:13.6px;line-height:1.7;color:#e7e9ee;white-space:pre}
.content table{border-collapse:collapse;width:100%;margin:18px 0;font-size:14px;display:block;overflow-x:auto}
.content th,.content td{border:1px solid var(--border);padding:9px 12px;text-align:right}
.content th{background:var(--panel2);color:#fff;font-weight:700}
.content tr:nth-child(even){background:rgba(255,255,255,.02)}
.content hr{border:none;border-top:1px solid var(--border);margin:48px 0}
.content strong{color:#fff}
/* images between sections */
.content img{max-width:100%;height:auto;display:block;margin:22px auto;border:1px solid var(--border);
  border-radius:14px;background:#0b0d13;padding:6px}
.content p>img{margin:22px auto}
/* callout headings (الخلاصة / تمرين) */
.content h3.cs-summary,.content h3.cs-exercise{display:inline-block;padding:7px 16px;border-radius:11px;margin-top:30px}
.content h3.cs-summary{background:rgba(52,211,153,.12);color:#7ee0a8;border:1px solid rgba(52,211,153,.4)}
.content h3.cs-exercise{background:rgba(251,191,36,.12);color:#fbbf24;border:1px solid rgba(251,191,36,.4)}
.content h3.cs-summary + ul,.content h3.cs-summary + ol{background:rgba(52,211,153,.05);
  border-inline-start:3px solid rgba(52,211,153,.45);padding:14px 30px;border-radius:0 10px 10px 0}
.content h3.cs-exercise + p,.content h3.cs-exercise + ul,.content h3.cs-exercise + ol{background:rgba(251,191,36,.05);
  border-inline-start:3px solid rgba(251,191,36,.45);padding:14px 30px;border-radius:0 10px 10px 0}
/* per-section toolbar */
.sec-tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 22px}
.chip{background:var(--panel2);border:1px solid var(--border);border-radius:999px;padding:4px 12px;font-size:12.5px;color:var(--muted)}
.stool{background:var(--panel2);border:1px solid var(--border);border-radius:999px;padding:5px 14px;
  font-size:13px;color:var(--text);cursor:pointer;font-family:inherit;transition:.15s}
.stool:hover{border-color:var(--accent);color:#fff}
.stool.has-note{border-color:var(--amber);color:var(--amber)}
.stool.reading{border-color:var(--green);color:var(--green)}
/* TTS highlight */
.tts-reading{background:rgba(110,168,254,.16)!important;border-radius:6px;
  box-shadow:0 0 0 3px rgba(110,168,254,.18)}
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
/* notes */
#notes-fab{position:fixed;bottom:24px;inset-inline-end:24px;z-index:60;width:54px;height:54px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent),var(--accent2));color:#fff;border:none;font-size:22px;cursor:pointer;
  box-shadow:0 6px 22px rgba(0,0,0,.45)}
#notes-fab .dot{position:absolute;top:8px;inset-inline-end:8px;width:11px;height:11px;border-radius:50%;background:var(--amber);display:none}
#notes-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:75}
#notes{position:fixed;top:0;inset-inline-end:0;height:100vh;width:min(440px,93vw);z-index:80;
  background:var(--panel);border-inline-start:1px solid var(--border);box-shadow:-12px 0 40px rgba(0,0,0,.5);
  display:flex;flex-direction:column;transform:translateX(0)}
#notes header{display:flex;align-items:center;justify-content:space-between;padding:18px;border-bottom:1px solid var(--border)}
#notes header strong{font-size:16px;color:#fff}
#notes header button{background:transparent;border:none;color:var(--muted);font-size:20px;cursor:pointer}
.notes-current{padding:16px 18px;border-bottom:1px solid var(--border)}
.notes-current label{font-size:12px;color:var(--muted)}
#note-section-title{font-size:14px;color:var(--accent);margin:4px 0 10px;font-weight:600;line-height:1.5}
#note-text{width:100%;min-height:150px;resize:vertical;background:var(--panel2);border:1px solid var(--border);
  border-radius:11px;color:var(--text);font-family:inherit;font-size:14.5px;line-height:1.8;padding:12px;}
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
#topbtn{position:fixed;bottom:24px;inset-inline-start:24px;background:var(--accent);color:#08121f;
  border:none;width:46px;height:46px;border-radius:50%;font-size:20px;cursor:pointer;display:none;
  box-shadow:0 6px 20px rgba(0,0,0,.4);z-index:40}
#menubtn{display:none}
@media (max-width:980px){
  #sidebar{position:fixed;inset-inline-end:0;transform:translateX(100%);transition:.25s;z-index:90;box-shadow:-8px 0 30px rgba(0,0,0,.5)}
  #sidebar.open{transform:translateX(0)}
  #menubtn{display:flex;position:fixed;top:14px;inset-inline-end:14px;z-index:61;background:var(--accent);
    color:#08121f;border:none;border-radius:10px;width:46px;height:46px;font-size:22px;cursor:pointer;align-items:center;justify-content:center}
  .content{padding:64px 18px 150px}
}
@media print{
  #sidebar,#audiobar,#notes,#notes-fab,#topbtn,#menubtn,#progressbar,.sec-tools,#tip{display:none!important}
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
      <p>من الصفر إلى أحدث المستويات — كورس تفاعلي</p>
    </div>
    <input id="search" type="text" placeholder="🔍 ابحث في الفهرس..." autocomplete="off">
    <ul id="toc"></ul>
  </aside>
  <main id="main">
    <div class="content">
      <div class="hero">
        <h1>__TITLE__</h1>
        <p>__SUBTITLE__</p>
        <div class="badges">
          <span class="badge">24 فصلاً</span>
          <span class="badge">أمثلة كود PyTorch</span>
          <span class="badge">بدائل ومبرّرات</span>
          <span class="badge">من الصفر للمبتدئين</span>
          <span class="badge">🔊 قارئ آلي</span>
          <span class="badge">📝 ملاحظات تُحفظ</span>
        </div>
      </div>
      <div id="tip">
        <span>✨</span>
        <div><b>ميزات جديدة:</b> اضغط <b>🔊 استمع للقسم</b> ليقرأ المحتوى بصوت مسموع، ودوّن <b>📝 ملاحظاتك وأسئلتك</b> (تُحفظ تلقائيًا في متصفحك)، واستعن بالصور التوضيحية في كل فصل.</div>
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

<div id="notes-backdrop" hidden></div>
<aside id="notes" hidden>
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
<button id="notes-fab" title="ملاحظاتي">📝<span class="dot" id="fab-dot"></span></button>

<button id="topbtn" title="أعلى">↑</button>

<script type="text/markdown" id="md">__MARKDOWN__</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>
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

  /* ---------- helpers ---------- */
  function chapterEls(h1){ var els=[]; var n=h1.nextElementSibling; while(n && n.tagName!=='H1'){ els.push(n); n=n.nextElementSibling;} return els; }
  function wordCount(els){ var w=0; els.forEach(function(el){ if(el.tagName==='PRE') return; w += (el.textContent.trim().match(/\S+/g)||[]).length; }); return w; }

  /* ---------- callout headings ---------- */
  contentEl.querySelectorAll('h3').forEach(function(h){
    var t=h.textContent;
    if(t.indexOf('الخلاصة')>-1 || t.indexOf('النقاط الأساسية')>-1) h.classList.add('cs-summary');
    else if(t.indexOf('تمرين')>-1) h.classList.add('cs-exercise');
  });

  /* ---------- TTS engine ---------- */
  var synth = window.speechSynthesis;
  var TTS = {
    items:[], i:0, playing:false, title:'', voice:null, rate:1, curEl:null,
    voices:[],
    pickVoices:function(){
      this.voices = synth ? synth.getVoices() : [];
      var ar = this.voices.filter(function(v){return (v.lang||'').toLowerCase().indexOf('ar')===0;});
      var sel=document.getElementById('ab-voice'); sel.innerHTML='';
      var list = ar.length?ar:this.voices;
      if(!ar.length){ var o=document.createElement('option'); o.value=''; o.textContent='(لا صوت عربي — صوت افتراضي)'; sel.appendChild(o); }
      list.forEach(function(v,k){ var o=document.createElement('option'); o.value=v.name; o.textContent=v.name+' ('+v.lang+')'; sel.appendChild(o); });
      this.voice = ar.length?ar[0]:null;
      if(this.voice) sel.value=this.voice.name;
    },
    chunk:function(el,text){
      var parts = text.replace(/\s+/g,' ').trim();
      if(!parts) return;
      var sentences = parts.split(/(?<=[\.\!\?؟،:])\s/);
      var buf='';
      var self=this;
      sentences.forEach(function(s){
        if((buf+' '+s).length>180){ if(buf){ self.items.push({el:el,text:buf}); } buf=s; }
        else { buf = buf?buf+' '+s:s; }
      });
      if(buf) self.items.push({el:el,text:buf});
    },
    build:function(h1){
      this.items=[];
      var self=this;
      chapterEls(h1).forEach(function(el){
        if(['PRE','TABLE','HR','IMG','DIV'].indexOf(el.tagName)>-1) return;
        if(el.tagName==='UL'||el.tagName==='OL'){
          Array.prototype.slice.call(el.children).forEach(function(li){ self.chunk(li, li.textContent); });
        } else { self.chunk(el, el.textContent); }
      });
    },
    start:function(h1){
      if(!synth){ alert('متصفحك لا يدعم القارئ الآلي (Web Speech API). جرّب Chrome أو Safari حديثًا.'); return; }
      this.stop();
      this.build(h1);
      this.title = h1.textContent;
      document.getElementById('ab-title').textContent = '🔊 ' + this.title;
      this.i=0; this.playing=true;
      document.getElementById('audiobar').hidden=false;
      document.getElementById('ab-pp').textContent='⏸';
      markReadingBtn(h1);
      this.speak();
    },
    speak:function(){
      if(this.i>=this.items.length){ this.finish(); return; }
      var it=this.items[this.i];
      this.highlight(it.el);
      var u=new SpeechSynthesisUtterance(it.text);
      u.lang = this.voice ? this.voice.lang : 'ar-SA';
      if(this.voice) u.voice=this.voice;
      u.rate=this.rate;
      var self=this;
      u.onend=function(){ if(self.playing){ self.i++; self.speak(); } };
      u.onerror=function(){ if(self.playing){ self.i++; self.speak(); } };
      synth.speak(u);
    },
    highlight:function(el){
      if(this.curEl) this.curEl.classList.remove('tts-reading');
      this.curEl=el; if(el){ el.classList.add('tts-reading');
        var r=el.getBoundingClientRect(); if(r.top<80||r.bottom>window.innerHeight-120){ el.scrollIntoView({behavior:'smooth',block:'center'});} }
    },
    pauseResume:function(){
      if(!synth) return;
      if(this.playing){ synth.pause(); this.playing=false; document.getElementById('ab-pp').textContent='▶'; }
      else { synth.resume(); this.playing=true; document.getElementById('ab-pp').textContent='⏸'; }
    },
    finish:function(){ this.playing=false; if(this.curEl)this.curEl.classList.remove('tts-reading'); clearReadingBtns(); document.getElementById('ab-pp').textContent='▶'; },
    stop:function(){ this.playing=false; if(synth){try{synth.cancel();}catch(e){}} if(this.curEl)this.curEl.classList.remove('tts-reading'); clearReadingBtns(); }
  };
  function markReadingBtn(h1){ clearReadingBtns(); var b=h1.__listenBtn; if(b) b.classList.add('reading'); }
  function clearReadingBtns(){ document.querySelectorAll('.stool.reading').forEach(function(b){b.classList.remove('reading');}); }

  if(synth){ TTS.pickVoices(); if(typeof synth.onvoiceschanged!=='undefined'){ synth.onvoiceschanged=function(){TTS.pickVoices();}; } }
  document.getElementById('ab-pp').addEventListener('click',function(){TTS.pauseResume();});
  document.getElementById('ab-stop').addEventListener('click',function(){TTS.stop();document.getElementById('audiobar').hidden=true;});
  document.getElementById('ab-close').addEventListener('click',function(){TTS.stop();document.getElementById('audiobar').hidden=true;});
  document.getElementById('ab-rate').addEventListener('input',function(){TTS.rate=parseFloat(this.value);});
  document.getElementById('ab-voice').addEventListener('change',function(){
    var v=TTS.voices.filter(function(x){return x.name===this.value;}.bind(this))[0]; if(v)TTS.voice=v;
  });

  /* ---------- Notes (localStorage) ---------- */
  var NK='arllm_notes_v1';
  function loadNotes(){ try{return JSON.parse(localStorage.getItem(NK))||{};}catch(e){return {};} }
  function saveNotes(o){ try{localStorage.setItem(NK, JSON.stringify(o));}catch(e){} }
  var notes = loadNotes();
  var activeId=null, activeTitle='';
  var panel=document.getElementById('notes'), backdrop=document.getElementById('notes-backdrop'),
      ta=document.getElementById('note-text'), nstatus=document.getElementById('note-status'),
      nlist=document.getElementById('notes-list'), nsectitle=document.getElementById('note-section-title');

  function openNotes(id,title){
    activeId=id||currentChapterId();
    var h=document.getElementById(activeId);
    activeTitle=title|| (h?h.textContent:'ملاحظة عامة');
    nsectitle.textContent=activeTitle;
    ta.value = (notes[activeId] && notes[activeId].text) || '';
    nstatus.textContent='';
    panel.hidden=false; backdrop.hidden=false;
    renderNotesList();
    ta.focus();
  }
  function closeNotes(){ panel.hidden=true; backdrop.hidden=true; }
  var saveTimer=null;
  ta.addEventListener('input',function(){
    if(!activeId) return;
    var val=ta.value;
    if(saveTimer)clearTimeout(saveTimer);
    saveTimer=setTimeout(function(){
      if(val.trim()){ notes[activeId]={title:activeTitle,text:val,ts:Date.now()}; }
      else { delete notes[activeId]; }
      saveNotes(notes); nstatus.textContent='✓ حُفظ تلقائيًا';
      setTimeout(function(){nstatus.textContent='';},1500);
      renderNotesList(); refreshNoteIndicators();
    },350);
  });
  function renderNotesList(){
    var keys=Object.keys(notes).sort(function(a,b){return (notes[b].ts||0)-(notes[a].ts||0);});
    if(!keys.length){ nlist.innerHTML='<div class="notes-empty">لا ملاحظات بعد. اكتب أول ملاحظة في الأعلى ✍️</div>'; return; }
    nlist.innerHTML='';
    keys.forEach(function(k){
      var n=notes[k];
      var li=document.createElement('li');
      var del=document.createElement('button'); del.className='nl-del'; del.textContent='🗑';
      del.addEventListener('click',function(){ delete notes[k]; saveNotes(notes); renderNotesList(); refreshNoteIndicators(); if(k===activeId)ta.value=''; });
      var t=document.createElement('div'); t.className='nl-title'; t.textContent=n.title||k;
      t.addEventListener('click',function(){ var el=document.getElementById(k); if(el)el.scrollIntoView({behavior:'smooth',block:'start'}); openNotes(k,n.title); });
      var s=document.createElement('div'); s.className='nl-snippet'; s.textContent=n.text||'';
      li.appendChild(del); li.appendChild(t); li.appendChild(s); nlist.appendChild(li);
    });
  }
  function refreshNoteIndicators(){
    document.querySelectorAll('.stool.note').forEach(function(b){
      var id=b.getAttribute('data-id');
      if(notes[id]) b.classList.add('has-note'); else b.classList.remove('has-note');
    });
    document.getElementById('fab-dot').style.display = Object.keys(notes).length?'block':'none';
  }
  document.getElementById('notes-close').addEventListener('click',closeNotes);
  backdrop.addEventListener('click',closeNotes);
  document.getElementById('notes-fab').addEventListener('click',function(){ openNotes(null,null); });
  document.getElementById('notes-export').addEventListener('click',function(){
    var blob=new Blob([JSON.stringify(notes,null,2)],{type:'application/json'});
    var a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='ملاحظاتي_الكورس.json'; a.click();
  });
  document.getElementById('notes-import').addEventListener('click',function(){ document.getElementById('notes-file').click(); });
  document.getElementById('notes-file').addEventListener('change',function(e){
    var f=e.target.files[0]; if(!f)return; var rd=new FileReader();
    rd.onload=function(){ try{ var o=JSON.parse(rd.result); Object.keys(o).forEach(function(k){notes[k]=o[k];}); saveNotes(notes); renderNotesList(); refreshNoteIndicators(); nstatus.textContent='✓ تم الاستيراد'; }catch(err){ alert('ملف غير صالح'); } };
    rd.readAsText(f);
  });
  document.getElementById('notes-clear').addEventListener('click',function(){
    if(confirm('مسح كل الملاحظات نهائيًا؟')){ notes={}; saveNotes(notes); ta.value=''; renderNotesList(); refreshNoteIndicators(); }
  });

  /* ---------- per-chapter toolbar (reading time + listen + note) ---------- */
  h1s.forEach(function(h1){
    var els=chapterEls(h1);
    var mins=Math.max(1, Math.round(wordCount(els)/180));
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
  refreshNoteIndicators();

  /* ---------- current chapter tracking ---------- */
  function currentChapterId(){
    var cur=h1s.length?h1s[0].id:null;
    h1s.forEach(function(h){ if(h.getBoundingClientRect().top<160) cur=h.id; });
    return cur;
  }

  /* ---------- search ---------- */
  var search=document.getElementById('search');
  search.addEventListener('input',function(){
    var q=this.value.trim().toLowerCase();
    toc.querySelectorAll('li').forEach(function(li){
      var t=li.textContent.toLowerCase();
      li.style.display = (!q || t.indexOf(q)>-1) ? '' : 'none';
    });
  });

  /* ---------- scroll: active link + progress ---------- */
  var links=Array.prototype.slice.call(toc.querySelectorAll('a'));
  var bar=document.getElementById('progressbar');
  var topbtn=document.getElementById('topbtn');
  function onScroll(){
    var st=window.scrollY||document.documentElement.scrollTop;
    var h=document.documentElement.scrollHeight-document.documentElement.clientHeight;
    bar.style.width=(h>0?(st/h*100):0)+'%';
    topbtn.style.display = st>500 ? 'block':'none';
    var cur=null;
    heads.forEach(function(hd){ if(hd.getBoundingClientRect().top<140) cur=hd.id; });
    links.forEach(function(a){ a.classList.toggle('active', a.getAttribute('href')==='#'+cur); });
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();

  topbtn.addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var menubtn=document.getElementById('menubtn');
  menubtn && menubtn.addEventListener('click',function(){document.getElementById('sidebar').classList.toggle('open');});

  /* ---------- onboarding tip dismiss ---------- */
  var tip=document.getElementById('tip');
  if(localStorage.getItem('arllm_tip_hidden')==='1'){ tip.style.display='none'; }
  document.getElementById('tip-close').addEventListener('click',function(){ tip.style.display='none'; try{localStorage.setItem('arllm_tip_hidden','1');}catch(e){} });

  /* stop speech when leaving page */
  window.addEventListener('beforeunload',function(){ if(synth){try{synth.cancel();}catch(e){}} });
})();
</script>
</body>
</html>
"""

def build_html(md_text):
    safe = md_text.replace("</script>", "<\\/script>")
    out = HTML_TEMPLATE
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
    print(f"Markdown -> {MD_OUT}")
    print(f"HTML app -> {HTML_OUT}")

if __name__ == "__main__":
    main()
