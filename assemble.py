#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""يجمّع فصول الكورس إلى ملف Markdown شامل + تطبيق HTML تفاعلي (RTL)."""
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
  --green:#34d399; --code-bg:#11141c; --sidebar-w:340px;
}
*{box-sizing:border-box}
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
.content{max-width:920px;margin:0 auto;padding:46px 40px 120px}
.hero{background:linear-gradient(135deg,rgba(110,168,254,.10),rgba(139,92,246,.10));
  border:1px solid var(--border);border-radius:18px;padding:30px 30px 24px;margin-bottom:36px}
.hero h1{font-size:30px;margin:0 0 12px;line-height:1.5;color:#fff}
.hero p{color:var(--muted);margin:0;font-size:15.5px}
.badges{margin-top:18px;display:flex;flex-wrap:wrap;gap:8px}
.badge{background:var(--panel2);border:1px solid var(--border);border-radius:999px;
  padding:5px 13px;font-size:12.5px;color:var(--muted)}
.content h1{font-size:26px;margin:54px 0 18px;padding-bottom:12px;border-bottom:2px solid var(--border);
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
#topbtn{position:fixed;bottom:26px;inset-inline-start:26px;background:var(--accent);color:#08121f;
  border:none;width:46px;height:46px;border-radius:50%;font-size:20px;cursor:pointer;display:none;
  box-shadow:0 6px 20px rgba(0,0,0,.4);z-index:40}
#menubtn{display:none}
@media (max-width:980px){
  #sidebar{position:fixed;inset-inline-end:0;transform:translateX(100%);transition:.25s;z-index:60;box-shadow:-8px 0 30px rgba(0,0,0,.5)}
  #sidebar.open{transform:translateX(0)}
  #menubtn{display:flex;position:fixed;top:14px;inset-inline-end:14px;z-index:61;background:var(--accent);
    color:#08121f;border:none;border-radius:10px;width:46px;height:46px;font-size:22px;cursor:pointer;align-items:center;justify-content:center}
  .content{padding:64px 18px 100px}
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
          <span class="badge">end-to-end SOTA</span>
        </div>
      </div>
      <div id="content"></div>
    </div>
  </main>
</div>
<button id="topbtn" title="أعلى">↑</button>

<script type="text/markdown" id="md">__MARKDOWN__</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.0/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>
(function(){
  var raw = document.getElementById('md').textContent;
  if(window.marked){
    marked.setOptions({gfm:true, breaks:false});
  }
  var contentEl = document.getElementById('content');
  contentEl.innerHTML = window.marked ? marked.parse(raw) : '<pre>'+raw.replace(/</g,'&lt;')+'</pre>';

  // syntax highlight
  if(window.hljs){ document.querySelectorAll('pre code').forEach(function(b){ try{hljs.highlightElement(b);}catch(e){} }); }

  // build TOC from h1/h2
  var toc = document.getElementById('toc');
  var heads = contentEl.querySelectorAll('h1, h2');
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

  // search filter
  var search=document.getElementById('search');
  search.addEventListener('input',function(){
    var q=this.value.trim().toLowerCase();
    toc.querySelectorAll('li').forEach(function(li){
      var t=li.textContent.toLowerCase();
      li.style.display = (!q || t.indexOf(q)>-1) ? '' : 'none';
    });
  });

  // active link on scroll + progress bar
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
    links.forEach(function(a){
      a.classList.toggle('active', a.getAttribute('href')==='#'+cur);
    });
  }
  window.addEventListener('scroll',onScroll,{passive:true});
  onScroll();

  document.getElementById('topbtn').addEventListener('click',function(){window.scrollTo({top:0,behavior:'smooth'});});
  var menubtn=document.getElementById('menubtn');
  menubtn && menubtn.addEventListener('click',function(){document.getElementById('sidebar').classList.toggle('open');});
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
