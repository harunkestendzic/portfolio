# -*- coding: utf-8 -*-
"""Portfolio v2: redesigned static site. Run: python3 build2.py [--artifact]

Reuses the content (content.py, earlier.py, diagrams.py) and small helpers from build.py.
The site shell is quiet and monochrome; colour, type and texture belong to each project,
so every main project page is styled like the project itself."""
import math
import os
import shutil
import sys
from html import escape as E

import build as B
import content as C
from earlier import EARLIER, META, TYPES
from diagrams import DIAGRAMS

T, rel, page_path = B.T, B.rel, B.page_path
fmt_todo, md_inline = B.fmt_todo, B.md_inline
ROOT, DIST, LANGS = B.ROOT, B.DIST, B.LANGS
ARTIFACT = "--artifact" in sys.argv
t = C.t

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
         "&family=VT323&family=IM+Fell+English+SC&family=IM+Fell+English:ital@0;1"
         "&family=JetBrains+Mono:wght@300;400;500;700;800&family=Special+Elite&family=Monoton&family=Rubik:wght@400;500;700&display=swap")

THEME_OF = {"ramo": "ramo", "arcanetd": "arcane", "psychocat": "psycho", "vinyl-shop": "vinyl"}


def L(lang, en, bs):
    return en if lang == "en" else bs


# ======================================================================= CSS
LB_CSS = B.CSS[B.CSS.index("figure img[data-lb]{cursor"):]

CSS = r"""
:root{
  --paper:#F3F4F1; --surface:#FFFFFF; --ink:#1C2230; --muted:#5D6474; --line:#D8DBE1; --line-2:#C3C8D1;
  --accent:#1C2230; --accent-soft:#E6E9EF; --hydro:#1D8FA0; --vulcan:#C4542A; --solar:#B88A1C;
  --font-body:"Archivo",system-ui,sans-serif; --font-display:"Archivo",system-ui,sans-serif;
  --wrap:1180px; --pad:clamp(18px,4vw,40px); --r:14px;
  color-scheme:light;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#13161D; --surface:#1A1E27; --ink:#E8EAEF; --muted:#9AA1AF; --line:#2B313D; --line-2:#3A4150; --accent:#E8EAEF; --accent-soft:#232835; color-scheme:dark}}
:root[data-theme="dark"]{--paper:#13161D; --surface:#1A1E27; --ink:#E8EAEF; --muted:#9AA1AF; --line:#2B313D; --line-2:#3A4150; --accent:#E8EAEF; --accent-soft:#232835; color-scheme:dark}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation:none!important;transition:none!important}}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-body);font-size:17px;line-height:1.55;font-variation-settings:"wdth" 100}
.site,.th{background:var(--paper);color:var(--ink);min-height:100vh;overflow-x:clip}
img,video,svg{max-width:100%;display:block}
img{height:auto}
h1,h2,h3,h4,p,ul,ol,dl,dd,figure,blockquote{margin:0}
ul,ol{padding:0;list-style:none}
a{color:inherit;text-underline-offset:3px;text-decoration-thickness:1px}
a:focus-visible,button:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:2px solid var(--ink);outline-offset:3px;border-radius:4px}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 var(--pad)}
.skip{position:absolute;left:-9999px}.skip:focus{left:12px;top:12px;z-index:99;background:var(--surface);padding:8px 12px}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* ---------- header / footer (shared, themed through variables) ---------- */
.top{position:sticky;top:0;z-index:50;background:color-mix(in srgb,var(--paper) 88%,transparent);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:20px;height:60px}
.mark{display:flex;align-items:center;gap:10px;text-decoration:none;font-weight:700;font-size:15px;letter-spacing:.01em;margin-right:auto;font-family:"Archivo",sans-serif;font-variation-settings:"wdth" 112}
.mark svg{width:22px;height:22px;flex:none}
.nav{display:flex;align-items:center;gap:4px;font-family:"Archivo",sans-serif;font-size:15px}
.nav a{padding:6px 10px;border-radius:8px;text-decoration:none;color:var(--muted)}
.nav a:hover,.nav a[aria-current]{color:var(--ink)}
.nav a[aria-current]{background:var(--accent-soft)}
.nav .lang{border:1px solid var(--line-2);color:var(--ink);font-weight:600;margin-left:6px}
@media (max-width:560px){.nav a.hide-s{display:none}.mark span{display:none}}
footer.ft{border-top:1px solid var(--line);margin-top:96px;font-family:"Archivo",sans-serif;font-size:14px;color:var(--muted)}
footer.ft .wrap{display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between;padding-block:28px}

/* ---------- buttons ---------- */
.btns{display:flex;flex-wrap:wrap;gap:10px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;border:1px solid var(--ink);background:var(--ink);color:var(--paper);font:600 15px/1.2 "Archivo",sans-serif;text-decoration:none;cursor:pointer}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--line-2)}
.btn:hover{filter:brightness(1.12)}.btn.ghost:hover{border-color:var(--ink)}
.btn small{font-weight:500;opacity:.7}

/* ---------- home ---------- */
.h-hero{padding:44px 0 8px;position:relative;isolation:isolate}
.h-hero::before{content:"";position:absolute;inset:-60px 0 -40px;z-index:-1;pointer-events:none;
  background-image:radial-gradient(circle at 1px 1px,color-mix(in srgb,var(--ink) 22%,transparent) 1.1px,transparent 1.4px);background-size:22px 22px;
  -webkit-mask-image:radial-gradient(120% 90% at 30% 20%,#000 30%,transparent 75%);mask-image:radial-gradient(120% 90% at 30% 20%,#000 30%,transparent 75%)}
.h-hero .wrap{display:grid;grid-template-columns:minmax(0,1fr) 280px;gap:40px;align-items:end}
.h-name{font-family:"JetBrains Mono",ui-monospace,monospace;font-variation-settings:normal;font-weight:800;font-size:clamp(44px,8.6vw,124px);line-height:.95;letter-spacing:-.045em}
.h-name>span{display:block}
.h-name>span:last-child{font-weight:300;letter-spacing:-.05em;color:var(--muted)}
.h-lede{margin-top:28px;font-size:clamp(19px,2vw,23px);line-height:1.4;max-width:34ch}
.h-hero .btns{margin-top:28px}
.h-code{--k:#3D5BD9;--s:#1E7A4C;--kw:#B0326B;--c:#7A8292;border:1px solid var(--line);border-radius:12px;background:var(--surface);overflow:hidden;font:400 13.5px/1.75 "JetBrains Mono",ui-monospace,monospace;align-self:end;box-shadow:0 1px 0 var(--line)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .h-code{--k:#9DB1FF;--s:#86E0A8;--kw:#F28AB6;--c:#7E8696}}
:root[data-theme="dark"] .h-code{--k:#9DB1FF;--s:#86E0A8;--kw:#F28AB6;--c:#7E8696}
.h-code .tab{display:flex;align-items:center;gap:12px;padding:9px 14px;border-bottom:1px solid var(--line);color:var(--muted);font-size:12.5px;margin:0}
.tdots{display:flex;gap:6px}.tdots i{width:9px;height:9px;border-radius:50%;background:var(--line-2)}
.h-code pre{margin:0;padding:14px 16px 16px;white-space:pre-wrap;color:var(--ink);font:inherit;background:none;border-radius:0}
.h-code .ln{display:block;padding-left:2ch;text-indent:-2ch}
.h-code .ln:first-child,.h-code .ln:last-child{padding-left:0;text-indent:0}
.h-code .ln:not(:first-child):not(:last-child){margin-left:2ch}
.h-code .k{color:var(--k)}.h-code .s{color:var(--s)}.h-code .kw{color:var(--kw)}.h-code .p{color:var(--muted)}.h-code .v{color:var(--ink)}
.h-code .c{color:var(--c);font-size:12px;white-space:nowrap}.h-code .c .dot{display:inline-block;width:7px;height:7px;margin:0 5px 1px 4px;vertical-align:middle}
.h-lede .prompt{font-family:"JetBrains Mono",monospace;color:var(--muted);font-weight:500}
.caret{display:inline-block;width:.55em;height:1.05em;background:var(--ink);vertical-align:-.15em;margin-left:3px;opacity:.85}
.h-name span[data-scr]{white-space:nowrap}
.h-name .g{display:inline;color:#2FA36B}
.h-side{border-left:1px solid var(--line);padding-left:24px;display:grid;gap:18px;font-size:15px}
.h-side dt{color:var(--muted);font-size:13px}
.h-side dd{font-weight:500}
.h-side .now dd{display:flex;gap:8px;align-items:baseline}
.dot{width:8px;height:8px;border-radius:50%;background:#2FA36B;flex:none;transform:translateY(-1px);box-shadow:0 0 0 3px color-mix(in srgb,#2FA36B 25%,transparent)}
@media (max-width:860px){.h-hero .wrap{grid-template-columns:1fr}.h-side{border-left:0;padding-left:0;border-top:1px solid var(--line);padding-top:20px;grid-template-columns:1fr 1fr}}

.sh{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin:72px 0 22px;flex-wrap:wrap}
.sh h2{font-variation-settings:"wdth" 112;font-weight:750;font-size:clamp(24px,2.6vw,32px);letter-spacing:-.015em}
.sh p{color:var(--muted);font-size:15px;max-width:52ch}

/* the four worlds */
.worlds{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}
@media (max-width:820px){.worlds{grid-template-columns:1fr}}
.world{position:relative;display:block;aspect-ratio:16/10.5;border-radius:var(--r);overflow:hidden;text-decoration:none;isolation:isolate}
.world .w-meta{position:absolute;left:0;right:0;bottom:0;z-index:5;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:8px 12px;padding:16px 18px}
@media (max-width:560px){.world{aspect-ratio:4/3.5}.w-ramo .w-list{display:none}.w-ramo .w-logo{top:28%;width:30%}.w-ramo .w-street{bottom:62px;height:16%}
 .w-psycho .file{width:58%;top:9%;font-size:11px;padding:10px 10px 12px}.w-psycho .stamp{top:12%;right:4%;font-size:13px}.w-arcane .w-towers{top:8%}}
.world:focus-visible{outline-offset:4px}
.w-tag{font:500 13px/1.3 "Archivo",sans-serif;padding:5px 9px;border-radius:7px;white-space:nowrap}

/* Ramo world: a teletext page */
.w-ramo{background:#000;color:#fff;font-family:"VT323",monospace}
.w-ramo .tt-bar{display:flex;gap:14px;padding:12px 16px 0;font-size:20px;color:#fff}
.w-ramo .tt-bar b{color:#FFFF00;font-weight:400}
.w-ramo .tt-band{margin:8px 16px 0;background:#0000FF;color:#fff;padding:4px 10px;font-size:22px;display:flex;justify-content:space-between}
.w-ramo .w-logo{position:absolute;left:5%;top:27%;width:24%;image-rendering:pixelated}
.w-ramo .w-list{position:absolute;right:5%;top:30%;width:52%;font-size:clamp(18px,2.3vw,26px);line-height:1.15}
.w-ramo .w-list div{display:flex;gap:6px;color:#00FFFF}
.w-ramo .w-list div i{flex:1;border-bottom:3px dotted #00FFFF;transform:translateY(-6px)}
.w-ramo .w-list div b{color:#FFFF00;font-weight:400}
.w-ramo .w-street{position:absolute;left:0;right:0;bottom:58px;height:19%;display:flex;align-items:flex-end;justify-content:flex-end;gap:5%;padding-right:6%;border-bottom:4px solid #444}
.w-ramo .w-street img{height:100%;width:auto;image-rendering:pixelated}
.w-ramo .w-meta{color:#fff;font-size:22px}
.w-ramo .w-tag{background:#FF00FF;color:#000;font-family:"VT323",monospace;font-size:19px;border-radius:0}
.w-ramo h3{font-weight:400;font-size:30px;line-height:1}

/* ArcaneTD world */
.w-arcane{background:#0C1718;color:#E9E0C9}
.w-arcane svg.hexmap{position:absolute;inset:0;width:100%;height:100%;opacity:.95}
.w-arcane::after{content:"";position:absolute;inset:0;background:radial-gradient(120% 90% at 20% 110%,rgba(6,12,13,.92) 25%,transparent 70%);z-index:1}
.w-arcane .w-towers{position:absolute;right:5%;top:12%;display:flex;gap:10px;align-items:flex-end;z-index:2}
.w-arcane .w-towers img{width:clamp(44px,7vw,78px);filter:drop-shadow(0 6px 14px rgba(0,0,0,.55))}
.w-arcane .w-towers img:nth-child(2){width:clamp(56px,9vw,100px)}
.w-arcane h3{font:400 clamp(34px,4.6vw,54px)/1 "IM Fell English SC",serif;letter-spacing:.01em}
.w-arcane .w-tag{background:rgba(142,227,93,.14);color:#B6F08F;border:1px solid rgba(142,227,93,.45)}
.w-arcane .w-sub{font:italic 16px/1.3 "IM Fell English",serif;color:#CFC3A6;margin-top:4px}
.w-spark{position:absolute;z-index:1;mix-blend-mode:screen;opacity:.75;pointer-events:none}

/* Psychocat world: a case file on a blueprint */
.w-psycho{background:#173763;color:#F1E9D6}
.w-psycho .bp{position:absolute;inset:0;width:100%;height:100%}
.w-psycho .file{position:absolute;left:6%;top:12%;width:46%;background:#EFE5CE;color:#2A2622;padding:14px 16px 18px;font-family:"Special Elite",monospace;font-size:clamp(12px,1.3vw,15px);line-height:1.45;box-shadow:0 18px 30px rgba(4,12,26,.45);transform:rotate(-2.2deg);z-index:2}
.w-psycho .file b{font-weight:400;color:#7a6f62}
.w-psycho .file .photo{width:100%;aspect-ratio:16/9;object-fit:cover;filter:grayscale(.35) contrast(1.05);margin-bottom:10px;border:5px solid #fff}
.w-psycho .stamp{position:absolute;right:6%;top:16%;z-index:3;font:400 clamp(15px,2vw,22px)/1.05 "Special Elite",monospace;color:#E0443A;border:3px solid #E0443A;padding:8px 10px;transform:rotate(8deg);text-align:center;background:rgba(23,55,99,.35)}
.w-psycho h3{font:400 clamp(30px,4vw,46px)/1 "Special Elite",monospace;color:#F7EFDA}
.w-psycho .w-tag{background:#F7EFDA;color:#173763;font-family:"Special Elite",monospace}

/* Jugoton world: a 70s record sleeve */
.w-vinyl{background:#121110;color:#F3E6CF}
.w-vinyl .stripes{position:absolute;left:0;right:0;top:20%;height:30%;display:grid;grid-template-rows:repeat(5,1fr)}
.w-vinyl .stripes i:nth-child(1){background:#F6B33D}.w-vinyl .stripes i:nth-child(2){background:#F08A24}.w-vinyl .stripes i:nth-child(3){background:#E2561B}.w-vinyl .stripes i:nth-child(4){background:#B8361A}.w-vinyl .stripes i:nth-child(5){background:#6E2614}
.w-vinyl .disc{position:absolute;right:8%;top:8%;width:52%;aspect-ratio:1;z-index:2}
.w-vinyl .disc svg{width:100%;height:100%}
@media (prefers-reduced-motion:no-preference){.world:hover .disc svg,.world:focus-visible .disc svg{animation:spin 1.8s linear infinite}}
@keyframes spin{to{transform:rotate(360deg)}}
.w-vinyl h3{font:400 clamp(34px,5vw,62px)/1 "Monoton",cursive;color:#F3E6CF;letter-spacing:.02em}
.w-vinyl .w-tag{background:#F08A24;color:#121110}

/* experience + index lists */
.rows{border-top:1px solid var(--line)}
details.row{border-bottom:1px solid var(--line)}
details.row>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:150px minmax(0,1fr) auto;gap:18px;align-items:baseline;padding:18px 0}
details.row>summary::-webkit-details-marker{display:none}
details.row .when{color:var(--muted);font-size:14px;font-variant-numeric:tabular-nums}
details.row .what{font-weight:600;font-size:18px}
details.row .what span{font-weight:400;color:var(--muted)}
.plus{width:22px;height:22px;position:relative;flex:none;color:var(--muted)}
.plus::before,.plus::after{content:"";position:absolute;left:4px;right:4px;top:10px;height:2px;background:currentColor;border-radius:2px;transition:transform .2s}
.plus::after{transform:rotate(90deg)}
details[open]>summary .plus::after{transform:rotate(0)}
details.row .body{padding:0 0 22px 168px;display:grid;gap:10px;max-width:calc(168px + 70ch)}
details.row .body li{padding-left:18px;position:relative}
details.row .body li::before{content:"";position:absolute;left:2px;top:.72em;width:7px;height:2px;background:var(--muted)}
@media (max-width:640px){details.row>summary{grid-template-columns:1fr auto}details.row .when{grid-column:1/-1;order:-1;margin-bottom:-12px}details.row .body{padding-left:0}}
.quote{border-left:3px solid var(--ink);padding:4px 0 4px 16px;font-size:17px}
.quote cite{display:block;font-style:normal;color:var(--muted);font-size:14px;margin-top:6px}

.idx{border-top:1px solid var(--line)}
.idx-g{display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;padding:14px 0;border-bottom:1px solid var(--line)}
.idx-g>h3{font-size:14px;font-weight:500;color:var(--muted);padding-top:12px}
.idx a{display:grid;grid-template-columns:64px minmax(0,1fr) auto;gap:16px;align-items:center;padding:8px 0;text-decoration:none;border-radius:10px}
.idx a:hover .n{text-decoration:underline}
.idx .th-i{width:64px;height:44px;border-radius:7px;overflow:hidden;background:var(--accent-soft);border:1px solid var(--line)}
.idx .th-i img{width:100%;height:100%;object-fit:cover}
.idx .n{font-weight:600}
.idx .s{display:block;color:var(--muted);font-size:14.5px;line-height:1.4}
.idx .st{color:var(--muted);font-size:13px;white-space:nowrap}
@media (max-width:640px){.idx-g{grid-template-columns:1fr;gap:4px}.idx-g>h3{padding-top:4px}.idx .st{display:none}.idx a{grid-template-columns:56px minmax(0,1fr)}.idx .th-i{width:56px;height:40px}}

.cards-g{display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;padding:22px 0;border-top:1px solid var(--line)}
.cards-g>h3{font-size:15px;font-weight:600;padding-top:4px}
.cards-g>h3 span{display:block;font-weight:400;color:var(--muted);font-size:13.5px;margin-top:2px}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.card{display:flex;flex-direction:column;text-decoration:none;background:var(--surface);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.card:hover{border-color:var(--line-2)}.card:hover .cn{text-decoration:underline;text-underline-offset:3px}
.card .ct{position:relative;aspect-ratio:16/10;background:var(--accent-soft);overflow:hidden;border-bottom:1px solid var(--line)}
.card .ct img{width:100%;height:100%;object-fit:cover}
.card .ck{position:absolute;left:10px;top:10px;font-size:12.5px;font-weight:600;padding:4px 9px;border-radius:7px;background:var(--surface);color:var(--ink);box-shadow:0 1px 0 var(--line)}
.card .cb{padding:14px 16px 16px;display:flex;flex-direction:column;gap:6px;flex:1}
.card .cn{font-weight:650;font-size:17.5px;line-height:1.25}
.card .cs{color:var(--muted);font-size:14.5px;line-height:1.45}
.card .cst{margin-top:auto;padding-top:8px;display:flex;flex-wrap:wrap;gap:6px}
.card .cst span{font-size:12.5px;padding:3px 8px;border-radius:6px;background:var(--accent-soft);color:var(--ink)}
@media (max-width:980px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:760px){.cards-g{grid-template-columns:1fr;gap:12px}}
@media (max-width:520px){.cards{grid-template-columns:1fr}}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px}
@media (max-width:820px){.two{grid-template-columns:1fr;gap:0}}
.facts li{padding:12px 0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:150px minmax(0,1fr);gap:16px}
.facts.stack li{grid-template-columns:1fr;gap:2px}
.facts li b{font-weight:600}
.facts li span{color:var(--muted)}
.contact-big{font-variation-settings:"wdth" 118;font-weight:750;font-size:clamp(26px,5vw,58px);letter-spacing:-.02em;text-decoration:none;line-height:1.05;word-break:break-word}
.contact-big:hover{text-decoration:underline;text-decoration-thickness:3px}
.c-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px;align-items:center}

/* about page */
.a-head{padding:56px 0 8px}
.a-head h1{font-variation-settings:"wdth" 125;font-weight:800;font-size:clamp(40px,7vw,84px);letter-spacing:-.03em;line-height:.95}
.a-head p{margin-top:20px;font-size:20px;line-height:1.45;max-width:54ch}
.skills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;border-top:1px solid var(--line)}
.skills div{padding:14px 0;border-bottom:1px solid var(--line)}
.skills b{display:block;font-weight:600}
.skills span{color:var(--muted);font-size:15px}
@media (max-width:700px){.skills{grid-template-columns:1fr}}
.certs{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:18px}
.certs a{text-decoration:none;display:grid;gap:4px;align-content:start}
.certs .ci{aspect-ratio:4/3;border-radius:9px;overflow:hidden;border:1px solid var(--line);background:var(--surface);margin-bottom:6px}
.certs .ci img{width:100%;height:100%;object-fit:cover}
.certs b{font-weight:600;font-size:15px;line-height:1.3}
.certs span,.certs small{color:var(--muted);font-size:13.5px;line-height:1.35}
details.more{margin-top:18px}
details.more>summary{cursor:pointer;display:inline-flex;gap:10px;align-items:center;font-weight:600;list-style:none;padding:8px 0}
details.more>summary::-webkit-details-marker{display:none}
details.more>.inner{margin-top:14px}

/* small project pages (shell style) */
.e-head{padding:48px 0 24px}
.e-crumb{font-size:14px;color:var(--muted)}.e-crumb a{color:var(--muted)}
.e-head h1{margin-top:14px;font-variation-settings:"wdth" 118;font-weight:780;font-size:clamp(34px,5.6vw,64px);letter-spacing:-.025em;line-height:1}
.e-head .sum{margin-top:16px;font-size:20px;line-height:1.45;max-width:56ch}
.e-meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:18px}
.e-meta span{font-size:13.5px;padding:5px 10px;border-radius:7px;background:var(--accent-soft)}
.e-body{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:48px;align-items:start}
@media (max-width:900px){.e-body{grid-template-columns:1fr;gap:28px}}
.e-pts{display:grid;gap:12px}
.e-pts li{padding-left:20px;position:relative;max-width:68ch}
.e-pts li::before{content:"";position:absolute;left:2px;top:.7em;width:8px;height:2px;background:var(--ink)}
.e-aside{border:1px solid var(--line);border-radius:var(--r);padding:18px;display:grid;gap:14px;font-size:15px;background:var(--surface)}
.e-aside dt{color:var(--muted);font-size:13px}
.note{color:var(--muted);font-size:15px}
.gal{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:36px}
.gal figure.wide{grid-column:1/-1}
@media (max-width:640px){.gal{grid-template-columns:1fr}}
.gal img,.gal video{width:100%;border-radius:10px;border:1px solid var(--line);background:#000}
figcaption{font-size:14px;color:var(--muted);margin-top:8px;line-height:1.4}
.pnav{display:flex;justify-content:space-between;gap:18px;margin-top:64px;padding-top:20px;border-top:1px solid var(--line);font-size:15px}
.pnav a{text-decoration:none;display:grid;gap:2px}.pnav a span{color:var(--muted);font-size:13px}
.pnav a:last-child{text-align:right}
.todo{background:#fff3b0;color:#4a3b00;padding:0 3px;border-radius:3px}

/* ================= project pages: shared skeleton ================= */
.pj-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:8px}
.pj-strip div{padding:14px 16px 14px 0}
.pj-strip dt{font-size:13px;color:var(--muted)}
.pj-strip dd{font-weight:500;font-size:15.5px;line-height:1.35}
@media (max-width:760px){.pj-strip{grid-template-columns:1fr 1fr}}
.pj-sec{margin-top:56px}
.pj-h2{font-size:clamp(24px,2.6vw,32px);margin-bottom:18px}
.pj-media{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:18px 16px;align-items:start}
.pj-media figure{grid-column:span 2}
.pj-media figure.big{grid-column:span 4;grid-row:span 2}
.pj-media figure.full{grid-column:1/-1;grid-row:auto}.pj-media figure.half{grid-column:span 3}
@media (max-width:760px){.pj-media{grid-template-columns:1fr}.pj-media figure,.pj-media figure.big,.pj-media figure.half{grid-column:1/-1;grid-row:auto}}
.pj-media img,.pj-media video{width:100%;aspect-ratio:16/9;object-fit:cover;background:#000}
.pj-media img.contain,.pj-media img[style*=pixelated]{object-fit:contain}
.pj-acc{display:grid;gap:12px}
details.sx>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:16px;padding:16px 18px}
details.sx>summary::-webkit-details-marker{display:none}
details.sx .sx-k{flex:none}
details.sx .sx-t{flex:1;font-size:20px}
details.sx .sx-h{font-size:14px;opacity:.75;display:none}
@media (min-width:700px){details.sx .sx-h{display:block}}
details.sx .sx-b{padding:4px 18px 24px;display:grid;gap:16px}
.prose{display:grid;gap:14px;max-width:72ch}
.built{display:grid;gap:10px;max-width:76ch}
.built li{position:relative;padding-left:22px}
ol.built{counter-reset:s}
ol.built li{counter-increment:s}
ol.built li::before{content:counter(s);position:absolute;left:0;font-weight:700;font-size:.85em;top:.12em}
.figs{display:grid;gap:22px}
.figs h3{font-size:17px;margin-bottom:10px}
.dg-box{border-radius:10px;padding:16px;overflow-x:auto;background:var(--surface);border:1px solid var(--line)}
.dg{display:block;width:100%;min-width:640px;height:auto}.dg text{font-family:var(--font-body)}
.dn rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.dn.n-focus rect{fill:var(--accent-soft);stroke:var(--accent)}
.dn.n-hydro rect{stroke:var(--hydro);stroke-width:2}.dn.n-vulcan rect{stroke:var(--vulcan);stroke-width:2}.dn.n-solar rect{stroke:var(--solar);stroke-width:2.5}
.dt-title{fill:var(--ink);font-weight:600;font-size:17px}.dt-sub{fill:var(--muted);font-size:14px}
.dt-tag{fill:var(--accent);font-weight:700;font-size:12px;letter-spacing:.04em}.dt-label{fill:var(--muted);font-size:14px;font-style:italic}
.da{fill:none;stroke:var(--muted);stroke-width:1.6}.da.a-hydro{stroke:var(--hydro)}.da.a-vulcan{stroke:var(--vulcan)}
.dm{fill:var(--muted)}.dm-hydro{fill:var(--hydro)}.dm-vulcan{fill:var(--vulcan)}
.dbrace{fill:none;stroke:var(--line);stroke-width:1.5;stroke-dasharray:4 5}
pre{margin:0;overflow-x:auto;padding:16px;border-radius:10px;font:14px/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.code-h{font-size:13px;opacity:.75}
.vcard{display:flex;gap:14px;align-items:center;padding:16px;text-decoration:none;border-radius:10px}
.vplay{width:42px;height:42px;border-radius:50%;flex:none;position:relative}
.vplay::after{content:"";position:absolute;left:16px;top:12px;border-left:14px solid currentColor;border-top:9px solid transparent;border-bottom:9px solid transparent}
.vframe{position:relative;aspect-ratio:16/9}.vframe iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.dvl{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}
.pj-links{display:flex;flex-wrap:wrap;gap:10px}
.pj-next{display:flex;justify-content:space-between;gap:16px;margin-top:72px;padding:22px 0;border-top:1px solid var(--line)}
.pj-next a{text-decoration:none;display:grid;gap:2px}.pj-next a span{font-size:13px;opacity:.7}.pj-next a:last-child{text-align:right}
.pj-next b{font-size:20px}

/* ================= RAMO: teletext, Sarajevo 1992 ================= */
.th-ramo{--paper:#000;--surface:#000;--ink:#fff;--muted:#00FFFF;--line:#333;--line-2:#fff;--accent:#FFFF00;--accent-soft:#0000FF;
  --hydro:#00FFFF;--vulcan:#FF0000;--solar:#FFFF00;--font-body:"VT323",monospace;color-scheme:dark;font-family:"VT323",monospace;font-size:23px;line-height:1.25}
.th-ramo .top{background:#000;border-bottom:2px solid #0000FF}
.th-ramo .mark,.th-ramo .nav{font-family:"VT323",monospace;font-size:22px;font-variation-settings:normal}
.th-ramo .nav a{color:#fff;border-radius:0}.th-ramo .nav a[aria-current]{background:#0000FF}.th-ramo .nav .lang{border-color:#FFFF00;color:#FFFF00}
.th-ramo .btn{font-family:"VT323",monospace;font-size:22px;border-radius:0;background:#FFFF00;color:#000;border-color:#FFFF00;padding:4px 14px}
.th-ramo .btn.ghost{background:#000;color:#00FFFF;border-color:#00FFFF}
.r-hero{padding:22px 0 0}
.tt-bar{display:flex;flex-wrap:wrap;gap:6px 22px;font-size:24px;color:#fff}
.tt-bar b{font-weight:400;color:#FFFF00}.tt-bar .g{color:#00FF00}
.tt-band{display:flex;justify-content:space-between;gap:12px;background:#0000FF;color:#fff;font-size:28px;padding:4px 14px;margin-top:10px}
.tt-band span:last-child{color:#FFFF00}
.r-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:40px;padding:28px 0 8px;align-items:start}
@media (max-width:820px){.r-grid{grid-template-columns:1fr;gap:20px}}
.r-logo{width:min(320px,70%);image-rendering:pixelated}
.r-hook{color:#FFFF00;font-size:30px;line-height:1.1;margin-top:18px;max-width:24ch}
.r-sum{margin-top:12px;max-width:44ch}
.th-ramo .btns{margin-top:22px}
.tt-index{display:grid;gap:2px;font-size:28px}
.tt-index .ti-h{color:#000;background:#00FFFF;padding:0 10px;margin-bottom:8px;display:flex;justify-content:space-between}
.tt-index a{display:flex;gap:8px;text-decoration:none;color:#00FFFF;padding:0 10px}
.tt-index a i{flex:1;border-bottom:4px dotted currentColor;transform:translateY(-9px)}
.tt-index a b{color:#FFFF00;font-weight:400}
.tt-index a:hover,.tt-index a:focus-visible{background:#0000FF;color:#fff}
.tt-index .ti-f{margin-top:12px;color:#fff;padding:0 10px;font-size:22px}
.r-street{display:flex;align-items:flex-end;justify-content:space-between;gap:14px;height:140px;margin-top:24px;border-bottom:6px solid #555;width:100vw;margin-left:calc(50% - 50vw);padding:0 max(var(--pad),calc(50vw - var(--wrap)/2 + var(--pad)));overflow:hidden}
.r-street img{height:60%;width:auto;image-rendering:pixelated}
.r-street img.small{height:30%}
.tramx{position:absolute;bottom:0;display:block;overflow:hidden;aspect-ratio:1432/150;z-index:0}
.tramx img{width:400%;max-width:none;height:100%;image-rendering:pixelated}
.r-street .tramx{height:82%;left:0;translate:-105% 0}
.r-street img{position:relative;z-index:1}
.w-ramo .w-street{overflow:visible}
.w-ramo .w-street .tramx{height:72%;left:0;translate:-105% 0}
.w-ramo .w-street img{position:relative;z-index:1}
.th-ramo .pj-strip{border-color:#0000FF;border-width:2px}
.th-ramo .pj-strip dt{color:#00FFFF;font-size:20px}.th-ramo .pj-strip dd{font-size:24px;font-weight:400}
.th-ramo .pj-h2{font-weight:400;font-size:32px;background:#FF00FF;color:#000;display:inline-block;padding:0 12px}
.r-scores{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 40px;font-size:26px;margin-top:6px}
@media (max-width:700px){.r-scores{grid-template-columns:1fr}}
.r-scores div{display:flex;gap:8px;color:#fff}.r-scores i{flex:1;border-bottom:4px dotted #555;transform:translateY(-9px)}.r-scores b{color:#00FF00;font-weight:400}
.th-ramo .pj-media img{image-rendering:pixelated;border:2px solid #0000FF}
.th-ramo figcaption{color:#00FFFF;font-size:20px}
.th-ramo details.sx{border:2px solid #0000FF}
.th-ramo details.sx>summary{padding:6px 14px}
.th-ramo details.sx[open]>summary{background:#0000FF}
.th-ramo .sx-k{color:#FFFF00;font-size:24px}
.th-ramo .sx-t{font-size:28px!important}
.th-ramo .sx-h{color:#00FFFF;font-size:20px!important}
.th-ramo .note{color:#00FFFF;font-size:21px}.th-ramo .pj-next a span{font-size:20px}.th-ramo .code-h{font-size:20px}
.th-ramo .pj-media figure.full img{aspect-ratio:auto;width:auto;max-width:100%;max-height:600px;object-fit:contain;margin:0 auto}
.th-ramo .built li::before{content:">";position:absolute;left:0;color:#00FF00}
.th-ramo ol.built li::before{content:counter(s);color:#FFFF00}
.th-ramo .dg-box{background:#000;border:2px solid #333}
.th-ramo .dg text{font-family:"VT323",monospace}.th-ramo .dt-title{font-size:20px}.th-ramo .dt-sub{font-size:17px}
.th-ramo pre{background:#000;border:2px solid #0000FF;color:#00FF00;font:20px/1.25 "VT323",monospace}
.th-ramo .vcard{border:2px solid #FFFF00;color:#FFFF00}.th-ramo .vplay{background:#FF0000;color:#fff}
.th-ramo .vcard span:last-child{color:#fff}
.th-ramo a{text-decoration-thickness:2px}
.th-ramo footer.ft{font-family:"VT323",monospace;font-size:20px;color:#00FFFF;border-top:2px solid #0000FF}
.th-ramo .pj-next b{font-weight:400;color:#FFFF00;font-size:28px}

/* ================= ARCANETD: bio-punk plague apothecary ================= */
.th-arcane{--paper:#0C1718;--surface:#122224;--ink:#E9E0C9;--muted:#A9B5A6;--line:#26403F;--line-2:#3D5D59;--accent:#B6F08F;--accent-soft:#1B3330;
  --hydro:#5FD6E6;--vulcan:#F2814A;--solar:#F2D27A;color-scheme:dark;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='56' height='97' viewBox='0 0 56 97'%3E%3Cpath d='M28 0v16M0 32l28-16 28 16M0 32v32M56 32v32M0 64l28 16 28-16M28 80v17' fill='none' stroke='%23183031' stroke-width='1.2'/%3E%3C/svg%3E")}
.th-arcane .top{background:color-mix(in srgb,#0C1718 86%,transparent);border-bottom-color:#26403F}
.a-hero{position:relative;overflow:hidden;min-height:min(78vh,720px);display:flex;align-items:flex-end;border-bottom:1px solid #26403F}
.a-hero svg.hexmap{position:absolute;inset:0;width:100%;height:100%}
.a-hero::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(9,17,18,.95) 0%,rgba(9,17,18,.75) 45%,rgba(9,17,18,.1) 80%),linear-gradient(0deg,#0C1718 0%,transparent 35%)}
.a-hero .wrap{position:relative;z-index:2;width:100%;padding-bottom:48px;padding-top:72px}
.a-hero h1{font:400 clamp(64px,11vw,148px)/.9 "IM Fell English SC",serif;letter-spacing:.005em;color:#F2E8CF;text-shadow:0 4px 30px rgba(0,0,0,.6)}
.a-hook{font:italic clamp(20px,2.2vw,26px)/1.35 "IM Fell English",serif;color:#E2D6B8;max-width:36ch;margin-top:16px}
.a-tox{display:flex;gap:16px;align-items:center;margin-top:22px;font:600 13px/1 "Archivo",sans-serif;color:#B6F08F;letter-spacing:.02em}
.a-tox .bar{width:180px;height:8px;border-radius:4px;background:#1B3330;overflow:hidden;border:1px solid #2E5149}
.a-tox .bar i{display:block;height:100%;width:62%;background:linear-gradient(90deg,#5FD6E6,#B6F08F 60%,#F2D27A)}
.th-arcane .btns{margin-top:26px}
.th-arcane .btn{background:#B6F08F;color:#0C1718;border-color:#B6F08F}
.th-arcane .btn.ghost{background:transparent;color:#E9E0C9;border-color:#3D5D59}
.a-towers{position:absolute;right:6%;bottom:12%;z-index:2;display:flex;gap:18px;align-items:flex-end}
.a-towers img{width:clamp(70px,9vw,128px);filter:drop-shadow(0 12px 22px rgba(0,0,0,.6))}
.a-towers img:nth-child(2){width:clamp(90px,12vw,166px)}
@media (max-width:760px){.a-towers{display:none}}
.a-hero .w-spark{z-index:1}
.th-arcane .pj-h2,.th-arcane .sx-t{font-family:"IM Fell English SC",serif;font-weight:400;letter-spacing:.01em}
.th-arcane .pj-h2{font-size:clamp(28px,3vw,38px);color:#F2E8CF}
.th-arcane details.sx{background:linear-gradient(180deg,#132628,#0F1E20);border:1px solid #2E4B48;border-radius:4px;position:relative}
.th-arcane details.sx::before,.th-arcane details.sx::after{content:"";position:absolute;width:10px;height:10px;border:1px solid #8B7D5A;transform:rotate(45deg);top:-6px;background:#0C1718}
.th-arcane details.sx::before{left:14px}.th-arcane details.sx::after{right:14px}
.th-arcane .sx-k svg{width:22px;height:22px}
.th-arcane .sx-t{font-size:24px!important;color:#F2E8CF}
.th-arcane .built li::before{content:"";position:absolute;left:2px;top:.55em;width:8px;height:8px;background:#B6F08F;clip-path:polygon(50% 0,100% 25%,100% 75%,50% 100%,0 75%,0 25%)}
.th-arcane .lore p:first-child::first-letter{font:400 3.2em/0.8 "IM Fell English SC",serif;float:left;margin:6px 8px 0 0;color:#B6F08F}
.th-arcane .lore{font:18.5px/1.6 "IM Fell English",serif;color:#E2D6B8}
.th-arcane .pj-media img,.th-arcane .pj-media video{border-radius:4px;border:1px solid #2E4B48}
.th-arcane .nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.th-arcane .nums li{border:1px solid #2E4B48;border-radius:4px;padding:14px;background:#0F1E20}
.th-arcane .nums b{display:block;font:400 34px/1 "IM Fell English SC",serif;color:#B6F08F}
.th-arcane .nums span{color:#A9B5A6;font-size:14px}
.th-arcane .wip{border:1px dashed #8B7D5A;padding:14px 16px;border-radius:4px;color:#E2D6B8;font-size:15.5px}
.th-arcane .vcard{border:1px solid #2E4B48;background:#0F1E20}.th-arcane .vplay{background:#B6F08F;color:#0C1718}

/* ================= PSYCHOCAT: case file on a blueprint ================= */
.th-psycho{--paper:#173763;--surface:#EFE5CE;--ink:#F4ECD8;--muted:#B7C6DE;--line:#2E5486;--line-2:#5C80B2;--accent:#E0443A;--accent-soft:#E6DAC0;
  --hydro:#2B6CB0;--vulcan:#C0392B;--solar:#B7791F;color-scheme:dark;
  background-image:linear-gradient(rgba(170,200,240,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(170,200,240,.09) 1px,transparent 1px),linear-gradient(rgba(170,200,240,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(170,200,240,.05) 1px,transparent 1px);
  background-size:96px 96px,96px 96px,24px 24px,24px 24px}
.th-psycho .top{background:color-mix(in srgb,#173763 88%,transparent);border-bottom-color:#2E5486}
.th-psycho .nav a{color:#B7C6DE}.th-psycho .nav a[aria-current]{background:#21497F;color:#fff}
.p-hero{position:relative;padding:48px 0 24px;overflow:hidden}
.p-hero .bp{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.p-hero .wrap{position:relative;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:40px;align-items:center}
@media (max-width:860px){.p-hero .wrap{grid-template-columns:1fr}}
.dossier{background:#EFE5CE;color:#2A2622;font-family:"Special Elite",monospace;padding:26px 26px 30px;box-shadow:0 30px 60px rgba(3,12,28,.45);transform:rotate(-1.4deg);position:relative;font-size:16px;line-height:1.5}
.dossier::before{content:"";position:absolute;top:-14px;left:28px;width:120px;height:26px;background:#E3D5B5;border-radius:6px 6px 0 0}
.dossier .clip{position:absolute;top:-18px;right:40px;width:16px;height:56px;border:3px solid #9AA3AD;border-radius:9px}
.dossier .photo{border:8px solid #fff;box-shadow:0 4px 12px rgba(0,0,0,.18);transform:rotate(1.6deg);margin-bottom:18px}
.dossier .photo img{width:100%;aspect-ratio:16/9;object-fit:cover;filter:grayscale(.25) sepia(.12)}
.dossier dl{display:grid;grid-template-columns:auto 1fr;gap:4px 14px}
.dossier dt{color:#857867}
.dossier .stamp{position:absolute;right:-18px;top:-26px;font-size:20px;color:#D63A2F;border:3px solid #D63A2F;padding:6px 10px;transform:rotate(-9deg);background:rgba(239,229,206,.7);text-align:center;line-height:1.1}
.p-hero h1{font:400 clamp(52px,8vw,104px)/.95 "Special Elite",monospace;color:#F7EFDA}
.p-hook{font-size:clamp(20px,2.2vw,26px);line-height:1.35;margin-top:16px;max-width:30ch;color:#F4ECD8}
.p-sum{margin-top:14px;color:#C9D6EA;max-width:52ch}
.th-psycho .btns{margin-top:24px}
.th-psycho .btn{background:#F7EFDA;color:#173763;border-color:#F7EFDA;font-family:"Special Elite",monospace;font-weight:400;border-radius:4px}
.th-psycho .btn.ghost{background:transparent;color:#F7EFDA;border-color:#5C80B2}
.th-psycho .pj-h2{font:400 clamp(26px,3vw,36px)/1.1 "Special Elite",monospace;color:#F7EFDA}
.th-psycho .pj-strip{border-color:#2E5486}
.th-psycho details.sx{background:#EFE5CE;color:#2A2622;border-radius:3px 12px 3px 3px;box-shadow:0 10px 24px rgba(3,12,28,.35)}
.th-psycho details.sx .sx-k{font-family:"Special Elite",monospace;background:#173763;color:#F7EFDA;padding:3px 8px;font-size:14px;border-radius:3px}
.th-psycho details.sx .sx-t{font-family:"Special Elite",monospace}
.th-psycho details.sx .sx-h{color:#6E6253}
.th-psycho details.sx .plus{color:#6E6253}
.th-psycho details.sx .prose,.th-psycho details.sx .built{color:#2A2622}
.th-psycho details.sx a{color:#173763}
.th-psycho .built li::before{content:"";position:absolute;left:0;top:.35em;width:13px;height:13px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cg fill='%23C0392B'%3E%3Cellipse cx='12' cy='16' rx='6' ry='5'/%3E%3Ccircle cx='5' cy='9' r='2.4'/%3E%3Ccircle cx='9.5' cy='5' r='2.4'/%3E%3Ccircle cx='14.5' cy='5' r='2.4'/%3E%3Ccircle cx='19' cy='9' r='2.4'/%3E%3C/g%3E%3C/svg%3E") center/contain no-repeat}
.th-psycho pre{background:#2A2622;color:#EFE5CE}
.th-psycho .pj-media figure{background:#fff;padding:8px 8px 10px;box-shadow:0 12px 24px rgba(3,12,28,.35)}
.th-psycho .pj-media figure:nth-child(odd){transform:rotate(-.6deg)}.th-psycho .pj-media figure:nth-child(even){transform:rotate(.6deg)}
.th-psycho .pj-media figcaption{color:#3d352c;font-family:"Special Elite",monospace;font-size:13.5px}
.th-psycho .nums{display:flex;flex-wrap:wrap;gap:12px}
.th-psycho .nums li{border:2px dashed #5C80B2;padding:12px 16px;border-radius:6px}
.th-psycho .nums b{font:400 30px/1 "Special Elite",monospace;color:#F7EFDA;margin-right:8px}
.th-psycho .wip{font-family:"Special Elite",monospace;color:#F7EFDA;border-left:4px solid #E0443A;padding:6px 0 6px 14px;font-size:15px}
.th-psycho .vcard{background:#EFE5CE;color:#2A2622}.th-psycho .vplay{background:#E0443A;color:#fff}
.th-psycho .dg-box{background:#EFE5CE}
.th-psycho .dg-box .dn rect{fill:#fff;stroke:#5C80B2}.th-psycho .dg-box .dt-title{fill:#2A2622}.th-psycho .dg-box .dt-sub{fill:#6E6253}

/* ================= JUGOTON: 70s record sleeve ================= */
.th-vinyl{--paper:#121110;--surface:#1B1917;--ink:#F3E6CF;--muted:#B9A991;--line:#2E2A26;--line-2:#4A433C;--accent:#F08A24;--accent-soft:#2A221A;
  --hydro:#F6B33D;--vulcan:#E2561B;--solar:#F6B33D;--font-body:"Rubik",sans-serif;color-scheme:dark;font-family:"Rubik",sans-serif}
.th-vinyl .top{background:color-mix(in srgb,#121110 88%,transparent);border-bottom-color:#2E2A26}
.v-hero{position:relative;overflow:hidden;padding:56px 0 0}
.v-hero .wrap{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);gap:40px;align-items:center;padding-bottom:56px}
@media (max-width:860px){.v-hero .wrap{grid-template-columns:1fr}}
.v-band{display:grid;grid-template-rows:repeat(5,9px)}
.v-band i:nth-child(1){background:#F6B33D}.v-band i:nth-child(2){background:#F08A24}.v-band i:nth-child(3){background:#E2561B}.v-band i:nth-child(4){background:#B8361A}.v-band i:nth-child(5){background:#6E2614}
.v-hero h1{font:400 clamp(48px,7vw,92px)/1 "Monoton",cursive;color:#F3E6CF;letter-spacing:.02em}
.v-sub{font:500 15px/1.3 "Rubik",sans-serif;color:#F08A24;margin-top:10px}
.v-hook{font-size:clamp(19px,2vw,23px);line-height:1.4;margin-top:16px;max-width:34ch}
.th-vinyl .btns{margin-top:22px}
.th-vinyl .btn{background:#F08A24;color:#121110;border-color:#F08A24;border-radius:999px;font-family:"Rubik",sans-serif}
.th-vinyl .btn.ghost{background:transparent;color:#F3E6CF;border-color:#4A433C}
.v-sleeve{position:relative;aspect-ratio:1.42;max-width:580px;width:100%;justify-self:end}
.v-sleeve .jacket{position:absolute;left:0;top:0;bottom:0;aspect-ratio:1;background:#F1E4CB;box-shadow:0 30px 60px rgba(0,0,0,.55);z-index:2;overflow:hidden;color:#3A1D10}
.v-sleeve .jacket::before{content:"";position:absolute;left:-30%;right:-30%;top:52%;height:34%;transform:rotate(-24deg);
  background:linear-gradient(#F6B33D 0 20%,#F08A24 20% 40%,#E2561B 40% 60%,#B8361A 60% 80%,#6E2614 80%)}
.v-sleeve .jacket b{position:absolute;left:7%;top:8%;font:400 clamp(26px,3.6vw,42px)/1 "Monoton",cursive;color:#3A1D10}
.v-sleeve .jacket small{position:absolute;left:7%;top:25%;font:500 13px/1.35 "Rubik",sans-serif;color:#3A1D10}
.v-sleeve .jacket em{position:absolute;right:7%;top:9%;font:700 12px/1 "Rubik",sans-serif;font-style:normal;border:2px solid #3A1D10;border-radius:50%;width:44px;height:44px;display:grid;place-items:center}
.v-sleeve .disc{position:absolute;right:0;top:3%;height:94%;aspect-ratio:1;z-index:1}

.tracklist{margin-top:10px;display:grid;gap:0;border-top:1px solid #2E2A26}
.th-vinyl details.sx{border-bottom:1px solid #2E2A26}
.th-vinyl details.sx>summary{padding:16px 4px}
.th-vinyl .sx-k{font:700 15px/1 "Rubik",sans-serif;color:#121110;background:#F08A24;border-radius:50%;width:34px;height:34px;display:grid;place-items:center}
.th-vinyl .sx-t{font-weight:500}
.th-vinyl details.sx[open] .sx-k{background:#F3E6CF}
.th-vinyl .side{font:400 26px/1 "Monoton",cursive;color:#F08A24;margin:34px 0 8px}
.th-vinyl .pj-h2{font:700 clamp(24px,2.6vw,32px)/1.1 "Rubik",sans-serif}
.th-vinyl .built li::before{content:"";position:absolute;left:0;top:.45em;width:11px;height:11px;border-radius:50%;background:radial-gradient(circle,#F08A24 0 30%,#121110 32% 46%,#F08A24 48%)}
.th-vinyl .pj-media img,.th-vinyl .pj-media video{border-radius:8px}
.th-vinyl .nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:0;border-top:1px solid #2E2A26}
.th-vinyl .nums li{padding:16px 12px 16px 0;border-bottom:1px solid #2E2A26}
.th-vinyl .nums b{display:block;font:700 34px/1 "Rubik",sans-serif;color:#F08A24}
.th-vinyl .nums span{color:#B9A991;font-size:14px}
.th-vinyl pre{background:#0A0908;border:1px solid #2E2A26;color:#F3E6CF}
.th-vinyl .vcard{border:1px solid #2E2A26}.th-vinyl .vplay{background:#F08A24;color:#121110}
#cloud .pj-media figure{grid-column:span 3}#cloud .pj-media img{object-fit:contain;background:#0A0908}
@media (max-width:760px){#cloud .pj-media figure{grid-column:1/-1}}
.th-vinyl .er{background:#0A0908;border-radius:10px;padding:12px}
.th-vinyl .er img{margin:0 auto;max-height:560px;width:auto}
.lb img{max-width:calc(100vw - 140px)!important;max-height:calc(100vh - 150px)!important;width:auto;height:auto}
@media (max-width:640px){.lb img{max-width:calc(100vw - 20px)!important;max-height:calc(100vh - 170px)!important}}

/* ---------- icons ---------- */
.ic{width:17px;height:17px;flex:none}
.btn .ic{margin-left:-2px}
/* ---------- motion: one signature moment per page, all off with reduced motion ---------- */
.v-sleeve .arm{position:absolute;z-index:3;right:-4%;top:-6%;height:66%;transform-origin:72% 10%;transform:rotate(-26deg)}
.w-psycho .photo-w{position:relative;display:block}
.w-psycho .photo-w video{position:absolute;inset:0;width:100%;opacity:0;transition:opacity .3s;margin:0}
.w-psycho:hover .photo-w video,.w-psycho:focus-visible .photo-w video{opacity:1}
.r-street{position:relative}
@media (prefers-reduced-motion:no-preference){
 .dot{animation:pulse 2.4s ease-out infinite}
 .caret{animation:blink 1.05s steps(1) infinite}
 @keyframes pulse{0%{box-shadow:0 0 0 0 color-mix(in srgb,#2FA36B 55%,transparent)}100%{box-shadow:0 0 0 9px transparent}}
 .hexmap .hg{animation:hglow 4s ease-in-out infinite}
 @keyframes hglow{0%,100%{opacity:.12}50%{opacity:.42}}
 .hexmap .tc{animation:tpulse 2.6s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
 @keyframes tpulse{50%{transform:scale(1.6);opacity:.7}}
 .a-hero .w-spark{animation:drift 7s ease-in-out infinite}
 .a-hero .w-spark+.w-spark{animation-duration:9s;animation-delay:-3s}
 @keyframes drift{0%,100%{translate:0 0;opacity:.55}50%{translate:-26px 10px;opacity:.9}}
 .a-towers img{animation:float 5s ease-in-out infinite}.a-towers img:nth-child(2){animation-delay:-1.6s}.a-towers img:nth-child(3){animation-delay:-3.2s}
 @keyframes float{50%{translate:0 -10px}}
 .a-tox .bar i{animation:fill 1.6s .4s cubic-bezier(.2,.7,.2,1) both}
 @keyframes fill{from{width:0}}
 .world.w-arcane:hover .hexmap .hg{animation-duration:1.4s}
 .tramx img{animation:wheels .5s steps(4) infinite}
 @keyframes wheels{to{translate:-100% 0}}
 .r-street .tramx{animation:drive 22s linear infinite}
 @keyframes drive{0%{translate:calc(-100% - 10vw) 0}100%{translate:calc(100vw + 10%) 0}}
 .w-ramo .w-street .tramx img{animation-play-state:paused}
 .world.w-ramo:hover .w-street .tramx{translate:115% 0;transition:translate 3.2s linear}
 .world.w-ramo:hover .w-street .tramx img{animation-play-state:running}
 .cur{animation:blink 1s steps(1) infinite}
 @keyframes blink{50%{opacity:0}}
 .p-hero .rt1,.w-psycho .rt1{animation:march 1.6s linear infinite}
 .p-hero .rt2,.w-psycho .rt2{animation:march 2.4s linear infinite reverse}
 @keyframes march{to{stroke-dashoffset:-36}}
 .p-hero .cone{animation:sweep 6s ease-in-out infinite;transform-origin:860px 360px}
 @keyframes sweep{0%,100%{rotate:-14deg}50%{rotate:16deg}}
 .bp .paw{opacity:0;animation:step 4.8s linear infinite}
 @keyframes step{0%{opacity:0}6%{opacity:.85}40%{opacity:.85}55%,100%{opacity:0}}
 .dossier .stamp{animation:thunk .45s .9s cubic-bezier(.3,1.6,.5,1) both}
 @keyframes thunk{from{opacity:0;scale:1.7}to{opacity:1;scale:1}}
 .v-sleeve .arm{animation:drop 1.4s .5s cubic-bezier(.5,0,.2,1) both}
 @keyframes drop{from{transform:rotate(-26deg)}to{transform:rotate(0deg)}}
 .v-sleeve .disc svg{animation:spin 2.2s linear infinite;animation-delay:1.8s}
}
@media (prefers-reduced-motion:reduce){.bp .paw{opacity:.7}.v-sleeve .arm{transform:rotate(0)}}
""" + LB_CSS.replace(".lb img{max-width:100%;max-height:100%;", ".lb img{")



def _ic(d, fill=False):
    a = 'fill="currentColor" stroke="none"' if fill else 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" {a}>{d}</svg>'


IC = {
    "download": _ic('<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>'),
    "mail": _ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m4 7 8 6 8-6"/>'),
    "copy": _ic('<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2"/>'),
    "phone": _ic('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a1 1 0 0 1-1 1A16 16 0 0 1 4 5a1 1 0 0 1 1-1z"/>'),
    "ext": _ic('<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "play": _ic('<path d="M8 5.5v13l10.5-6.5z"/>', fill=True),
    "github": _ic('<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.45-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.53 2.35 1.09 2.92.83.09-.65.35-1.09.64-1.34-2.22-.25-4.55-1.11-4.55-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.68-4.57 4.93.36.31.68.92.68 1.85v2.74c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/>', fill=True),
    "linkedin": _ic('<path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4V21H3zM9.5 9.5h3.8v1.6h.05c.53-1 1.83-2.05 3.77-2.05 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.1c0-1.22-.02-2.78-1.7-2.78-1.7 0-1.96 1.33-1.96 2.7V21h-4z"/>', fill=True),
}

TONEARM = ('<svg class="arm" viewBox="0 0 120 260" aria-hidden="true"><circle cx="86" cy="26" r="20" fill="#2a2725" stroke="#4a433c" stroke-width="3"/>'
           '<circle cx="86" cy="26" r="7" fill="#B9A991"/><path d="M86 26 L86 170 L58 222" fill="none" stroke="#C9BBA3" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
           '<rect x="40" y="214" width="30" height="22" rx="4" transform="rotate(28 55 225)" fill="#E9DCC3"/></svg>')


# ===================================================================== frame
HEX = ('<svg class="ico" viewBox="0 0 64 64" aria-hidden="true">'
       '<path d="M32 3 58 18v28L32 61 6 46V18z" fill="#1C2230" stroke="#E6AA50" stroke-width="4" stroke-linejoin="round"/>'
       '<text x="32" y="41" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="24" fill="#E6AA50">{ }</text></svg>')


def header(lang, path, active):
    other = "bs" if lang == "en" else "en"
    other_path = path[3:] if lang == "bs" else "bs/" + path
    home = rel(path, page_path(lang, "home"))
    links = [
        (home + "#work", L(lang, "Work", "Radovi"), "work", ""),
        (rel(path, page_path(lang, "about")), L(lang, "About", "O meni"), "about", ""),
        (home + "#contact", L(lang, "Contact", "Kontakt"), "contact", "hide-s"),
    ]
    nav = "".join(f'<a class="{c}" href="{h}"{" aria-current=\"page\"" if k == active else ""}>{x}</a>' for h, x, k, c in links)
    nav += (f'<a class="lang" href="{rel(path, other_path)}" hreflang="{other}" lang="{other}" '
            f'title="{L(lang, "Bosanski", "English")}">{other.upper()}</a>')
    return (f'<a class="skip" href="#main">{L(lang, "Skip to content", "Preskoči na sadržaj")}</a>'
            f'<header class="top"><div class="wrap"><a class="mark" href="{home}">{HEX}<span>{E(C.PERSON["name"])}</span></a>'
            f'<nav class="nav" aria-label="{L(lang, "Main", "Glavna")}">{nav}</nav></div></header>')


def footer(lang, path):
    P = C.PERSON
    return (f'<footer class="ft"><div class="wrap"><span>{E(P["name"])}, 2026</span>'
            f'<span><a href="mailto:{P["email"]}">{P["email"]}</a> · <a href="{P["github"]}">GitHub</a> · <a href="{P["linkedin"]}">LinkedIn</a></span></div></footer>')


# Favicon: the hexagon from the preview card
FAVICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><path d="M32 3 58 18v28L32 61 6 46V18z" fill="#1C2230" stroke="#E6AA50" stroke-width="4" stroke-linejoin="round"/><text x="32" y="41" text-anchor="middle" font-family="monospace" font-weight="bold" font-size="24" fill="#E6AA50">{ }</text></svg>'
FAVICON_HREF = 'data:image/svg+xml,' + __import__('urllib.parse').parse.quote(FAVICON_SVG, safe="")


def document(lang, path, title, desc, body, fragment=False):
    other_path = path[3:] if lang == "bs" else "bs/" + path
    head = (f'<meta name="description" content="{E(desc)}">'
            f'<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:image" content="https://harunkestendzic.github.io/portfolio/assets/og-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image">'
            f'<meta name="theme-color" content="#1C2230"><meta name="referrer" content="strict-origin-when-cross-origin">'
            f'<link rel="icon" href="{FAVICON_HREF}">'
            f'<link rel="alternate" hreflang="{"bs" if lang == "en" else "en"}" href="{rel(path, other_path)}">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style>')
    if fragment:
        return (f'<title>{E(title)}</title><meta name="claude:viewport-fit-sides" content="cover">{head}'
                f'<div class="site">{body}</div>{JS}')
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><title>{E(title)}</title>{head}</head>'
            f'<body>{body}{JS}</body></html>')


JS = """<script>
(function(){
  function openTo(id){var el=document.getElementById(id); if(el&&el.tagName==='DETAILS'){el.open=true;}}
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href*="#"]'); if(!a)return;
    var h=a.getAttribute('href'); var id=h.split('#').pop(); if(id.indexOf('.')>=0)id=id.split('.').pop(); openTo(id);});
  if(location.hash){var id=location.hash.slice(1); if(id.indexOf('.')>=0)id=id.split('.').pop(); openTo(id);}
  document.querySelectorAll('.tt-clock').forEach(function(el){var p=el.textContent.split(':').map(Number),t=p[0]*3600+p[1]*60+p[2];
    setInterval(function(){t=(t+1)%86400;var h=Math.floor(t/3600),m=Math.floor(t/60)%60,x=t%60;el.textContent=[h,m,x].map(function(n){return(n<10?'0':'')+n}).join(':');},1000);});
  var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function heroFx(root){
    if(rm||root.dataset.fx)return; root.dataset.fx=1;
    var CH='{}[]()<>/;=+-*&|!_:#';
    function esc(c){return c==='<'?'&lt;':c==='>'?'&gt;':c==='&'?'&amp;':c;}
    root.querySelectorAll('[data-scr]').forEach(function(el,ix){
      var txt=el.textContent, n=txt.length, start=performance.now()+ix*180, dur=900;
      function frame(t){var k=Math.max(0,Math.min(1,(t-start)/dur)), done=Math.floor(k*n), out='';
        for(var i=0;i<n;i++){out+= i<done? esc(txt[i]) : '<span class="g">'+esc(CH[Math.floor(Math.random()*CH.length)])+'</span>';}
        el.innerHTML=out; if(k<1)requestAnimationFrame(frame); else el.textContent=txt;}
      requestAnimationFrame(frame);});
    root.querySelectorAll('[data-type]').forEach(function(el){
      var txt=el.textContent, i=0; el.textContent='';
      setTimeout(function step(){i+=1; el.textContent=txt.slice(0,i); if(i<txt.length)setTimeout(step, txt[i-1]==='.'?220:22);},1150);});
  }
  function runHero(){document.querySelectorAll('.h-hero').forEach(function(h){if(h.offsetParent!==null)heroFx(h);});}
  runHero(); window.addEventListener('hashchange',function(){setTimeout(runHero,30);});
  document.querySelectorAll('.world').forEach(function(w){var v=w.querySelector('video.hv'); if(!v||rm)return;
    function on(){var pr=v.play(); if(pr&&pr.catch)pr.catch(function(){});} function off(){v.pause();}
    w.addEventListener('mouseenter',on); w.addEventListener('focus',on); w.addEventListener('mouseleave',off); w.addEventListener('blur',off);});
  document.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    var v=b.getAttribute('data-copy'),done=b.getAttribute('data-done'),tg=b.querySelector('span')||b,orig=tg.textContent;
    try{navigator.clipboard.writeText(v).then(function(){tg.textContent=done;setTimeout(function(){tg.textContent=orig},1600)})}catch(err){}});});
})();
""" + B.LB_JS + "</script>"


# ================================================================ artwork
def hexmap(uid="hm"):
    """ArcaneTD map: pointy hex tiles with water and magma pools and towers."""
    W, H, r = 1200, 700, 40
    w = math.sqrt(3) * r
    hydro = {(13, 4), (14, 4), (13, 5), (12, 6), (14, 3)}
    vulcan = {(20, 8), (21, 8), (20, 9), (21, 7), (22, 8)}
    toxic = {(17, 2), (18, 2), (17, 3)}
    road = {(c, 11) for c in range(0, 30)} | {(10, rr) for rr in range(0, 11)} | {(c, 6) for c in range(10, 30)}
    towers = {(14, 5): "#7FE7F2", (12, 5): "#7FE7F2", (19, 8): "#FFA26E", (21, 9): "#FFA26E", (16, 3): "#B6F08F", (24, 5): "#F2D27A"}
    o = [f'<svg class="hexmap" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
         f'<defs><radialGradient id="{uid}g" cx="70%" cy="40%" r="75%"><stop offset="0" stop-color="#1b3a3c"/><stop offset="1" stop-color="#0a1415"/></radialGradient>'
         f'<filter id="{uid}b"><feGaussianBlur stdDeviation="7"/></filter></defs><rect width="{W}" height="{H}" fill="url(#{uid}g)"/>']
    glow = []
    for row in range(0, 13):
        for col in range(-1, 30):
            cx = col * w + (w / 2 if row % 2 else 0)
            cy = row * r * 1.5
            pts = " ".join(f"{cx + r * .93 * math.cos(math.radians(60 * k - 30)):.1f},{cy + r * .93 * math.sin(math.radians(60 * k - 30)):.1f}" for k in range(6))
            key = (col, row)
            if key in hydro:
                f, s = "#14707d", "#5fd6e6"; glow.append((cx, cy, "#5fd6e6"))
            elif key in vulcan:
                f, s = "#7a2410", "#f2814a"; glow.append((cx, cy, "#f2814a"))
            elif key in toxic:
                f, s = "#2f5a1d", "#b6f08f"; glow.append((cx, cy, "#b6f08f"))
            elif key in road:
                f, s = "#1f3134", "#2b4447"
            else:
                f, s = "#132325", "#1d3436"
            o.append(f'<polygon points="{pts}" fill="{f}" stroke="{s}" stroke-width="1.4"/>')
            if key in towers:
                c = towers[key]
                o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="14" fill="#0b1516" stroke="{c}" stroke-width="3"/><circle class="tc" cx="{cx:.0f}" cy="{cy:.0f}" r="5" fill="{c}"/>')
    o.insert(2, "".join(f'<circle class="hg" style="animation-delay:-{(i * 0.73) % 4:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="34" fill="{c}" opacity=".22" filter="url(#{uid}b)"/>' for i, (x, y, c) in enumerate(glow)))
    o.append("</svg>")
    return "".join(o)


def record_svg(uid="rec", label="#F08A24"):
    grooves = "".join(f'<circle cx="200" cy="200" r="{r}" fill="none" stroke="#2a2725" stroke-width="1.1"/>' for r in range(82, 196, 7))
    return (f'<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<defs><linearGradient id="{uid}s" x1="0" y1="0" x2="1" y2="1"><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset=".65" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            f'<circle cx="200" cy="200" r="198" fill="#0d0c0b" stroke="#3b3632" stroke-width="2"/>{grooves}<circle cx="200" cy="200" r="198" fill="url(#{uid}s)"/>'
            f'<circle cx="200" cy="200" r="70" fill="{label}"/><circle cx="200" cy="200" r="58" fill="none" stroke="#121110" stroke-width="2" opacity=".5"/>'
            f'<text x="200" y="186" text-anchor="middle" font-family="Monoton,cursive" font-size="17" fill="#121110">JUGOTON</text>'
            f'<text x="200" y="232" text-anchor="middle" font-family="Rubik,sans-serif" font-size="11" fill="#121110">SIDE A · 33⅓</text>'
            f'<circle cx="200" cy="200" r="7" fill="#F3E6CF"/></svg>')


def paw_trail():
    """Small paw prints along the cat's route, appearing one after another."""
    def bez(p0, p1, p2, p3, t):
        return tuple((1 - t) ** 3 * a + 3 * (1 - t) ** 2 * t * b + 3 * (1 - t) * t * t * c + t ** 3 * d for a, b, c, d in zip(p0, p1, p2, p3))
    segs = [((600, 520), (700, 470), (760, 380), (860, 360)), ((860, 360), (960, 340), (1020, 260), (1060, 170))]
    out = []
    k = 0
    for sg in segs:
        for t in (0.15, 0.4, 0.65, 0.9):
            x, y = bez(*sg, t)
            x2, y2 = bez(*sg, min(t + 0.02, 1))
            ang = math.degrees(math.atan2(y2 - y, x2 - x)) + 90
            side = 9 if k % 2 else -9
            out.append(f'<g class="paw" style="animation-delay:{k * 0.45:.2f}s" transform="translate({x:.0f} {y:.0f}) rotate({ang:.0f}) translate({side} 0) scale(.55) translate(-12 -12)">'
                       '<ellipse cx="12" cy="16" rx="6" ry="5"/><circle cx="5" cy="9" r="2.4"/><circle cx="9.5" cy="5" r="2.4"/><circle cx="14.5" cy="5" r="2.4"/><circle cx="19" cy="9" r="2.4"/></g>')
            k += 1
    return '<g fill="#F7EFDA">' + "".join(out) + "</g>"


def blueprint(uid="bp", big=False):
    """A floor plan of the house with the family's dashed routes and a vision cone."""
    return (f'<svg class="bp" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<g fill="none" stroke="#9CC0EE" stroke-opacity=".55" stroke-width="3">'
            f'<rect x="560" y="90" width="560" height="470"/><path d="M560 300h230M790 90v140M790 270v290M950 300h170M950 300v260M790 420h160"/>'
            f'<path d="M640 300v-40M700 560v-40M1040 90v40" stroke-width="2"/></g>'
            f'<g fill="none" stroke="#9CC0EE" stroke-opacity=".35" stroke-width="1.5"><rect x="600" y="130" width="120" height="60" rx="6"/><rect x="830" y="330" width="90" height="60"/><circle cx="1030" cy="200" r="34"/><rect x="980" y="430" width="110" height="80" rx="8"/></g>'
            f'<path class="rt1" d="M600 520 C700 470 760 380 860 360 S1020 260 1060 170" fill="none" stroke="#F7EFDA" stroke-opacity=".7" stroke-width="2.5" stroke-dasharray="9 9"/>'
            f'<path class="rt2" d="M1080 520 C1000 500 950 450 880 470 S700 420 650 240" fill="none" stroke="#E0443A" stroke-opacity=".75" stroke-width="2.5" stroke-dasharray="3 8" stroke-linecap="round"/>'
            f'<path class="cone" d="M860 360 L1010 300 A160 160 0 0 1 1000 430 Z" fill="#F7EFDA" fill-opacity=".1" stroke="#F7EFDA" stroke-opacity=".35"/>'
            f'{paw_trail()}'
            f'<g fill="#F7EFDA" fill-opacity=".85" transform="translate(1050 160) scale(1.1)"><ellipse cx="12" cy="16" rx="6" ry="5"/><circle cx="5" cy="9" r="2.4"/><circle cx="9.5" cy="5" r="2.4"/><circle cx="14.5" cy="5" r="2.4"/><circle cx="19" cy="9" r="2.4"/></g>'
            f'</svg>')


# ================================================================== pieces
def media_fig(m, lang, prefix, cls=""):
    c = f' class="{cls}"' if cls else ""
    if "video" in m:
        return (f'<figure{c}><video controls muted loop playsinline preload="metadata" poster="{prefix}{m["poster"]}" aria-label="{E(T(m["alt"], lang))}">'
                f'<source src="{prefix}{m["video"]}" type="video/mp4"></video><figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')
    px = ' style="image-rendering:pixelated"' if m.get("pixel") else ""
    return (f'<figure{c}><img src="{prefix}{m["src"]}" alt="{E(T(m["alt"], lang))}" loading="lazy"{px}>'
            f'<figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')


def media_grid(p, lang, prefix):
    """Editorial grid: one large item with two beside it, then rows of three.
    Leftovers are spread so no row ends with a gap."""
    ms = [m for m in p["media"] if "placeholder" not in m and not (p.get("cover_image") and m.get("src") == p.get("cover_image"))]
    n = len(ms)
    cls = ["" for _ in ms]
    if n:
        cls[0] = "big"
    rest = n - 3
    if n in (2, 4) or n == 1:
        cls[0] = "big full"
        rest = n - 1
        start = 1
    else:
        start = 3
    r = rest % 3 if rest > 0 else 0
    if r == 2:
        cls[-1] = cls[-2] = "half"
    elif r == 1 and rest >= 4:
        for k in range(1, 5):
            cls[-k] = "half"
    out = [media_fig(m, lang, prefix, c) for m, c in zip(ms, cls)]
    return f'<div class="pj-media">{"".join(out)}</div>'


def videos_block(p, lang):
    vs = list(p.get("videos", []))
    if not vs:
        return ""
    out = []
    for vid, vt in vs:
        url = f"https://www.youtube.com/watch?v={vid}"
        if ARTIFACT:
            out.append(f'<a class="vcard" href="{url}"><span class="vplay" aria-hidden="true"></span>'
                       f'<span><b>{E(T(vt, lang))}</b><br>{L(lang, "Watch on YouTube", "Pogledaj na YouTubeu")}</span></a>')
        else:
            out.append(f'<figure><div class="vframe"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(T(vt, lang))}" '
                       f'loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div><figcaption>{E(T(vt, lang))}</figcaption></figure>')
    return f'<div class="dvl" style="margin-bottom:18px">{"".join(out)}</div>'


def devlogs_block(p, lang):
    """Video devlogs from YouTube. Add entries to a project as
    "devlogs": [("YOUTUBE_ID", t("Title", "Naslov"), "2026-11-02"), ...]. Hidden while empty."""
    dl = p.get("devlogs", [])
    if not dl:
        return ""
    out = []
    for vid, vt, date in dl:
        url = f"https://www.youtube.com/watch?v={vid}"
        d = B.fmt_date(date, lang)
        if ARTIFACT:
            out.append(f'<a class="vcard" href="{url}"><span class="vplay" aria-hidden="true"></span><span><b>{E(T(vt, lang))}</b><br>{d}</span></a>')
        else:
            out.append(f'<figure><div class="vframe"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(T(vt, lang))}" loading="lazy" '
                       f'allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div><figcaption>{E(T(vt, lang))} · {d}</figcaption></figure>')
    return (f'<section class="pj-sec" id="devlogs"><h2 class="pj-h2">{L(lang, "Video devlogs", "Video devlogovi")}</h2>'
            f'<div class="dvl">{"".join(out)}</div></section>')


def sections(p, lang, prefix):
    """The expandable sections of a project page: (id, title, hint, html, open)."""
    U = C.UI
    out = []
    idea = f'<div class="prose"><p>{fmt_todo(T(p["idea"], lang))}</p><p>{fmt_todo(T(p["summary"], lang))}</p></div>'
    out.append(("idea", L(lang, "The idea", "Ideja"), L(lang, "What it is and why", "Šta je i zašto"), idea, False))
    if p.get("lore"):
        lp = "".join(f"<p>{fmt_todo(T(x, lang))}</p>" for x in p["lore"])
        out.append(("world", L(lang, "The world", "Svijet igre"), L(lang, "Setting and story", "Okruženje i priča"), f'<div class="prose lore">{lp}</div>', False))
    built = "".join(f"<li>{fmt_todo(T(b, lang))}</li>" for b in p["built"])
    built_html = (f'<ul class="built">{built}</ul><p class="note">{E(T(U["stack"], lang))}: {fmt_todo(p["stack"])}</p>')
    out.append(("built", L(lang, "What I built", "Šta sam napravio"), L(lang, f'{len(p["built"])} parts', f'{len(p["built"])} dijelova'), built_html, False))
    figs = []
    for key in p["diagrams"]:
        fn, (hen, hbs), (cen, cbs) = DIAGRAMS[key]
        figs.append(f'<figure><h3>{E(hen if lang == "en" else hbs)}</h3><div class="dg-box">{fn(lang)}</div><figcaption>{E(cen if lang == "en" else cbs)}</figcaption></figure>')
    if p.get("er_image"):
        er = p["er_image"]
        figs.append(f'<figure><h3>{E(T(er["title"], lang))}</h3><div class="er"><img src="{prefix}{er["src"]}" alt="{E(T(er["title"], lang))}"></div>'
                    f'<figcaption>{E(T(er["caption"], lang))}</figcaption></figure>')
    if figs:
        out.append(("how", L(lang, "How it works", "Kako radi"), L(lang, f"{len(figs)} diagrams", f"dijagrama: {len(figs)}"), f'<div class="figs">{"".join(figs)}</div>', False))
    if p.get("highlight"):
        code = ""
        if p.get("code"):
            code = (f'<div style="display:grid;gap:8px"><span class="code-h">{E(p["code"]["file"])}</span><pre><code>{E(p["code"]["body"])}</code></pre>'
                    f'<p class="note">{E(T(p["code"]["note"], lang))}</p></div>')
        out.append(("highlight", T(p["highlight_h"], lang), L(lang, "A closer look", "Detaljnije"),
                    f'<div class="prose"><p>{fmt_todo(T(p["highlight"], lang))}</p></div>{code}', False))
    if p.get("cloud"):
        cl = p["cloud"]
        fn, (hen, hbs), (cen, cbs) = DIAGRAMS["vinyl_cloud"]
        steps = "".join(f"<li>{fmt_todo(T(x, lang))}</li>" for x in cl["steps"])
        issues = "".join(f"<li>{fmt_todo(T(x, lang))}</li>" for x in cl["issues"])
        cf = "".join(media_fig(f, lang, prefix) for f in cl["figs"])
        html = (f'<div class="prose"><p>{fmt_todo(T(cl["intro"], lang))}</p></div>'
                f'<figure><div class="dg-box">{fn(lang)}</div><figcaption>{E(cen if lang == "en" else cbs)}</figcaption></figure>'
                f'<h3>{E(T(cl["steps_h"], lang))}</h3><ol class="built">{steps}</ol>'
                f'<h3>{E(T(cl["issues_h"], lang))}</h3><ul class="built">{issues}</ul>'
                f'<h3>{E(T(cl["prod_h"], lang))}</h3><div class="prose"><p>{fmt_todo(T(cl["prod"], lang))}</p></div>'
                f'<div class="pj-media">{cf}</div>')
        out.append(("cloud", T(cl["h"], lang), L(lang, "Ubuntu, Nginx, PHP-FPM, MySQL", "Ubuntu, Nginx, PHP-FPM, MySQL"), html, False))
    return out


def acc(secs, keyfn):
    out = []
    for i, (sid, title, hint, html, op) in enumerate(secs):
        out.append(f'<details class="sx" id="{sid}"{" open" if op else ""}><summary><span class="sx-k">{keyfn(i, sid)}</span>'
                   f'<span class="sx-t">{E(title)}</span><span class="sx-h">{E(hint)}</span><span class="plus" aria-hidden="true"></span></summary>'
                   f'<div class="sx-b">{html}</div></details>')
    return "".join(out)


def strip(p, lang):
    U = C.UI
    meta = [(U["status"], p["status"]), (U["role"], p["role"]), (U["timeline"], p["timeline"]), (U["platforms"], p["platforms"])]
    return '<dl class="pj-strip">' + "".join(f"<div><dt>{E(T(k, lang))}</dt><dd>{fmt_todo(T(v, lang))}</dd></div>" for k, v in meta) + "</dl>"


def link_icon(u, label=""):
    if any(w in label for w in ("Download", "Preuzmi")):
        return IC["download"]
    if "github.com" in u:
        return IC["github"]
    if "youtube" in u or "itch.io" in u and "download" not in u:
        return IC["play"]
    if "download" in u.lower():
        return IC["download"]
    return IC["ext"]


def links_html(p, lang, ghost_from=0):
    return "".join(f'<a class="btn{" ghost" if i >= ghost_from else ""}" href="{u}">{link_icon(u, T(n, "en"))}{E(T(n, lang))}</a>' for i, (n, u) in enumerate(p["links"]))


def next_nav(p, lang, path, idx):
    nxt = C.PROJECTS[(idx + 1) % len(C.PROJECTS)]
    return (f'<nav class="pj-next" aria-label="{L(lang, "Projects", "Projekti")}"><a href="{rel(path, page_path(lang, "home"))}#work"><span>{L(lang, "Back to", "Nazad na")}</span><b>{L(lang, "All work", "Sve radove")}</b></a>'
            f'<a href="{rel(path, page_path(lang, "project", nxt["slug"]))}"><span>{L(lang, "Next project", "Sljedeći projekat")}</span><b>{E(nxt["name"])}</b></a></nav>')


def nums_list(p, lang, cls="nums"):
    return f'<ul class="{cls}">' + "".join(f"<li><b>{E(n)}</b><span>{E(T(s, lang))}</span></li>" for n, s in p["numbers"]) + "</ul>"


# ============================================================ project pages
def page_ramo(p, lang, path, idx):
    pre = rel(path, "")
    a = pre + "assets/ramo/"
    secs = sections(p, lang, pre)
    pages = [110 + 15 * i for i in range(len(secs))]
    index = "".join(f'<a href="#{s[0]}"><span>{E(s[1])}</span><i></i><b>{pg}</b></a>' for s, pg in zip(secs, pages))
    index += f'<a href="#media"><span>{L(lang, "Screenshots and video", "Slike i video")}</span><i></i><b>200</b></a>'
    hero = (f'<section class="r-hero"><div class="wrap">'
            f'<div class="tt-bar"><span>P100</span><b>VHT</b><span>{L(lang, "Wed 15.04.92", "Sri 15.04.92")}</span><span class="g tt-clock">18:42:07</span></div>'
            f'<div class="tt-band"><span>TELETEKST</span><span>RAMO 100</span></div>'
            f'<div class="r-grid"><div><h1 class="sr">Ramo</h1><img class="r-logo" src="{a}logo.png" alt="Ramo" width="400" height="363">'
            f'<p class="r-hook">{fmt_todo(T(p["hook"], lang))}</p><p class="r-sum">{fmt_todo(T(p["summary"], lang))}</p>'
            f'<div class="btns">{links_html(p, lang, 1)}</div></div>'
            f'<nav class="tt-index" aria-label="{L(lang, "On this page", "Na ovoj stranici")}"><div class="ti-h"><span>{L(lang, "INDEX", "SADRŽAJ")}</span><span>101</span></div>{index}'
            f'<p class="ti-f">{L(lang, "Choose a page number", "Izaberite broj stranice")} <span class="cur" aria-hidden="true">&#9612;</span></p></nav></div>'
            f'<div class="r-street" aria-hidden="true"><span class="tramx"><img src="{a}tram-full.png" alt=""></span><img src="{a}enemy-1.png" alt="">'
            f'<img src="{a}ramo-pistol.png" alt=""><img class="small" src="{a}burek.png" alt="">'
            f'<img src="{a}enemy-2.png" alt=""><img src="{a}boss.png" alt=""></div></div></section>')
    scores = "".join(f"<div><span>{E(T(s, lang))}</span><i></i><b>{E(n)}</b></div>" for n, s in p["numbers"])
    body = (f'{strip(p, lang)}<section class="pj-sec"><h2 class="pj-h2">{L(lang, "RESULTS", "REZULTATI")}</h2><div class="r-scores">{scores}</div></section>'
            f'<section class="pj-sec" id="media"><h2 class="pj-h2">{L(lang, "SCREENSHOTS AND VIDEO", "SLIKE I VIDEO")} 200</h2>{videos_block(p, lang)}{media_grid(p, lang, pre)}</section>'
            f'<section class="pj-sec"><div class="pj-acc">{acc(secs, lambda i, s: pages[i])}</div></section>'
            f'{devlogs_block(p, lang)}{next_nav(p, lang, path, idx)}')
    return hero + f'<div class="wrap">{body}</div>'


def page_arcane(p, lang, path, idx):
    pre = rel(path, "")
    a = pre + "assets/arcanetd/art/"
    secs = sections(p, lang, pre)
    hexk = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2 20.7 7v10L12 22 3.3 17V7z" fill="none" stroke="#B6F08F" stroke-width="1.6"/><circle cx="12" cy="12" r="3" fill="#B6F08F"/></svg>'
    hero = (f'<section class="a-hero">{hexmap("ah")}'
            f'<img class="w-spark" src="{a}spark-purple.png" alt="" style="left:38%;top:8%;width:340px;transform:rotate(-12deg)">'
            f'<img class="w-spark" src="{a}spark-blue.png" alt="" style="right:-60px;top:30%;width:420px;transform:scaleX(-1)">'
            f'<div class="a-towers" aria-hidden="true"><img src="{a}tower-mage.png" alt=""><img src="{a}tower-archer.png" alt=""><img src="{a}tower-cannon.png" alt=""></div>'
            f'<div class="wrap"><h1>ArcaneTD</h1><p class="a-hook">{fmt_todo(T(p["hook"], lang))}</p>'
            f'<div class="a-tox"><span>SYS_TOX</span><span class="bar"><i></i></span><span>{E(T(p["status"], lang))}</span></div>'
            f'<div class="btns">{links_html(p, lang, 1)}</div></div></section>')
    wip = f'<p class="wip">{E(T(p["wip"], lang))}</p>' if p.get("wip") else ""
    body = (f'{strip(p, lang)}<section class="pj-sec">{wip}<div style="margin-top:18px">{nums_list(p, lang)}</div></section>'
            f'<section class="pj-sec" id="media"><h2 class="pj-h2">{L(lang, "From the game", "Iz igre")}</h2>{media_grid(p, lang, pre)}</section>'
            f'<section class="pj-sec"><h2 class="pj-h2">{L(lang, "The grimoire", "Knjiga zapisa")}</h2><div class="pj-acc">{acc(secs, lambda i, s: hexk)}</div></section>'
            f'{devlogs_block(p, lang)}{next_nav(p, lang, path, idx)}')
    return hero + f'<div class="wrap">{body}</div>'


def page_psycho(p, lang, path, idx):
    pre = rel(path, "")
    secs = sections(p, lang, pre)
    letters = "ABCDEFGH"
    rows = [(L(lang, "Subject", "Subjekt"), L(lang, "The family cat", "Porodična mačka")),
            (L(lang, "Motive", "Motiv"), L(lang, "Make the family believe the house is haunted", "Uvjeriti porodicu da je kuća ukleta")),
            (L(lang, "Location", "Lokacija"), L(lang, "One house, two floors, a garden", "Jedna kuća, dva sprata, bašta")),
            (L(lang, "Status", "Status"), T(p["status"], lang))]
    dl = "".join(f"<dt>{E(k)}:</dt><dd>{E(v)}</dd>" for k, v in rows)
    hero = (f'<section class="p-hero">{blueprint()}<div class="wrap">'
            f'<div><h1>Psychocat</h1><p class="p-hook">{fmt_todo(T(p["hook"], lang))}</p><p class="p-sum">{fmt_todo(T(p["summary"], lang))}</p>'
            f'<div class="btns">{links_html(p, lang, 1)}</div></div>'
            f'<div class="dossier"><span class="clip" aria-hidden="true"></span><div class="photo"><img src="{pre}{p["cover_image"]}" alt="{E(L(lang, "The Level 1 house from above, gray-box", "Kuća iz Nivoa 1 odozgo, gray-box"))}"></div>'
            f'<dl>{dl}</dl><div class="stamp" aria-hidden="true">{L(lang, "NOBODY<br>SUSPECTS<br>THE CAT", "NIKO NE<br>SUMNJA<br>NA MAČKU")}</div></div>'
            f'</div></section>')
    wip = f'<p class="wip">{E(T(p["wip"], lang))}</p>' if p.get("wip") else ""
    body = (f'{strip(p, lang)}<section class="pj-sec">{wip}<div style="margin-top:18px">{nums_list(p, lang)}</div></section>'
            f'<section class="pj-sec" id="media"><h2 class="pj-h2">{L(lang, "Surveillance footage", "Snimci s nadzora")}</h2>{media_grid(p, lang, pre)}</section>'
            f'<section class="pj-sec"><h2 class="pj-h2">{L(lang, "The case file", "Dosije")}</h2><div class="pj-acc">'
            f'{acc(secs, lambda i, s: L(lang, "Exhibit ", "Dokaz ") + letters[i])}</div></section>'
            f'{devlogs_block(p, lang)}{next_nav(p, lang, path, idx)}')
    return hero + f'<div class="wrap">{body}</div>'


def page_vinyl(p, lang, path, idx):
    pre = rel(path, "")
    secs = sections(p, lang, pre)
    side_a = [s for s in secs if s[0] in ("idea", "built", "how", "highlight")]
    side_b = [s for s in secs if s[0] not in ("idea", "built", "how", "highlight")]
    hero = (f'<section class="v-hero"><div class="wrap">'
            f'<div><h1>Jugoton</h1><p class="v-sub">{L(lang, "Online vinyl shop, built on PHP, MySQL and Oracle Cloud", "Online prodavnica vinila: PHP, MySQL i Oracle Cloud")}</p>'
            f'<p class="v-hook">{fmt_todo(T(p["hook"], lang))}</p><div class="btns"><a class="btn" href="#media">{L(lang, "Watch the demo", "Pogledaj demo")}</a>{links_html(p, lang, 0)}</div></div>'
            f'<div class="v-sleeve" aria-hidden="true"><div class="disc">{record_svg()}</div>{TONEARM}<div class="jacket"><b>Jugoton</b><em>LP</em>'
            f'<small>{L(lang, "Web Environments · Database Systems<br>Cloud Computing · SSST 2026", "Web okruženja · Baze podataka<br>Cloud Computing · SSST 2026")}</small></div></div>'
            f'</div><div class="v-band" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div></section>')
    body = (f'{strip(p, lang)}<section class="pj-sec">{nums_list(p, lang)}</section>'
            f'<section class="pj-sec" id="media"><h2 class="pj-h2">{L(lang, "The full demo, then every screen", "Cijeli demo, pa svaki ekran")}</h2>{media_grid(p, lang, pre)}</section>'
            f'<section class="pj-sec"><p class="side">{L(lang, "Side A", "Strana A")}</p><div class="tracklist">{acc(side_a, lambda i, s: "A" + str(i + 1))}</div>'
            + (f'<p class="side">{L(lang, "Side B", "Strana B")}</p><div class="tracklist">{acc(side_b, lambda i, s: "B" + str(i + 1))}</div>' if side_b else "")
            + f'</section>{devlogs_block(p, lang)}{next_nav(p, lang, path, idx)}')
    return hero + f'<div class="wrap">{body}</div>'


PAGES = {"ramo": page_ramo, "arcane": page_arcane, "psycho": page_psycho, "vinyl": page_vinyl}


def build_project(p, lang, idx):
    path = page_path(lang, "project", p["slug"])
    th = THEME_OF[p["slug"]]
    inner = PAGES[th](p, lang, path, idx)
    body = f'<div class="th th-{th}">' + header(lang, path, "work") + f'<main id="main">{inner}</main>' + footer(lang, path) + "</div>"
    return path, f'{p["name"]} | Harun Kestendžić', T(p["summary"], lang), body


# ============================================================== home page
def world_tile(p, lang, path):
    pre = rel(path, "")
    href = rel(path, page_path(lang, "project", p["slug"]))
    th = THEME_OF[p["slug"]]
    hook = E(T(p["hook"], lang))
    if th == "ramo":
        a = pre + "assets/ramo/"
        rows = [(L(lang, "Plays and downloads", "Igranja i preuzimanja"), "800+"), (L(lang, "FIT Coding Challenge", "FIT Coding Challenge"), L(lang, "1st", "1."), ),
                (L(lang, "Episodes", "Epizode"), "5+1")]
        lst = "".join(f"<div><span>{x}</span><i></i><b>{y}</b></div>" for x, y in rows)
        inner = (f'<div class="tt-bar" aria-hidden="true"><span>P100</span><b>VHT</b><span>15.04.92</span></div>'
                 f'<div class="tt-band" aria-hidden="true"><span>TELETEKST</span><span>RAMO</span></div>'
                 f'<img class="w-logo" src="{a}logo.png" alt="" width="400" height="363"><div class="w-list" aria-hidden="true">{lst}</div>'
                 f'<div class="w-street" aria-hidden="true"><span class="tramx"><img src="{a}tram-full.png" alt=""></span><img src="{a}burek.png" alt="" style="height:22%"><img src="{a}enemy-1.png" alt=""><img src="{a}ramo-pistol.png" alt=""><img src="{a}boss.png" alt=""></div>'
                 f'<div class="w-meta"><h3>Ramo</h3><span class="w-tag">{L(lang, "Released game", "Objavljena igra")}</span></div>')
    elif th == "arcane":
        a = pre + "assets/arcanetd/art/"
        inner = (f'{hexmap("w")}<img class="w-spark" src="{a}spark-purple.png" alt="" style="left:30%;top:6%;width:44%">'
                 f'<div class="w-towers" aria-hidden="true"><img src="{a}tower-mage.png" alt=""><img src="{a}tower-archer.png" alt=""><img src="{a}tower-cannon.png" alt=""></div>'
                 f'<div class="w-meta"><div><h3>ArcaneTD</h3><p class="w-sub">{L(lang, "Roguelike tower defence, 16,000 lines of C#", "Roguelike tower defence, 16.000 linija C#")}</p></div>'
                 f'<span class="w-tag">{L(lang, "In development", "U razvoju")}</span></div>')
    elif th == "psycho":
        inner = (f'{blueprint("wb")}<div class="file" aria-hidden="true"><span class="photo-w"><img class="photo" src="{pre}{p["cover_image"]}" alt=""><video class="photo hv" muted loop playsinline preload="none" poster="{pre}assets/psychocat/planning-view.jpg"><source src="{pre}assets/psychocat/planning-view.mp4" type="video/mp4"></video></span>'
                 f'<b>{L(lang, "Subject", "Subjekt")}:</b> {L(lang, "the family cat", "porodična mačka")}<br><b>{L(lang, "Motive", "Motiv")}:</b> {L(lang, "a haunted house", "ukleta kuća")}</div>'
                 f'<div class="stamp" aria-hidden="true">{L(lang, "NOBODY<br>SUSPECTS<br>THE CAT", "NIKO NE<br>SUMNJA<br>NA MAČKU")}</div>'
                 f'<div class="w-meta"><h3>Psychocat</h3><span class="w-tag">{L(lang, "Prototype", "Prototip")}</span></div>')
    else:
        inner = (f'<div class="stripes" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></div><div class="disc" aria-hidden="true">{record_svg("wr")}</div>'
                 f'<div class="w-meta"><h3>Jugoton</h3><span class="w-tag">{L(lang, "Web shop on Oracle Cloud", "Web shop na Oracle Cloudu")}</span></div>')
    return f'<a class="world w-{th}" href="{href}" aria-label="{E(p["name"])}: {hook}">{inner}</a>'


def thumb_of(e):
    if e.get("thumb") and os.path.exists(os.path.join(ROOT, e["thumb"])):
        return e["thumb"]
    return None


def e_item_path(lang, slug):
    return ("" if lang == "en" else "bs/") + f"earlier/{slug}.html"


def build_home(lang):
    path = page_path(lang, "home")
    P = C.PERSON
    pre = rel(path, "")
    side = [("now", L(lang, "Now", "Trenutno"), L(lang, "Backend AI Engineering intern at FlyRank", "Praksa iz Backend AI Engineeringa u FlyRanku")),
            ("", L(lang, "Studying", "Studij"), L(lang, "Computer Science at SSST, graduating 2028", "Računarske nauke na SSST-u, diploma 2028.")),
            ("", L(lang, "Looking for", "Tražim"), L(lang, "A junior or intern role in backend, software or games", "Junior poziciju ili praksu: backend, softver ili igre")),
            ("", L(lang, "Based in", "Lokacija"), L(lang, "Sarajevo, Bosnia and Herzegovina", "Sarajevo, Bosna i Hercegovina"))]
    side_html = '<dl class="h-side">' + "".join(f'<div class="{c}"><dt>{E(k)}</dt><dd>{"<span class=dot></span>" if c == "now" else ""}<span>{E(v)}</span></dd></div>' for c, k, v in side) + "</dl>"
    lede = L(lang, "I build games, and the systems behind them. Lately that means backends and AI.", "Pravim igre i sisteme iza njih. U posljednje vrijeme to znači backend i AI.")
    hero = (f'<section class="h-hero"><div class="wrap"><div><h1 class="h-name" aria-label="Harun Kestendžić"><span data-scr>Harun</span><span data-scr>Kestendžić</span></h1>'
            f'<p class="h-lede"><span class="prompt" aria-hidden="true">&gt;</span> <span class="typed" data-type>{lede}</span><span class="caret" aria-hidden="true"></span></p>'
            f'<div class="btns"><a class="btn" href="{pre}{P["cv"]}">{IC["download"]}{L(lang, "Download CV", "Preuzmi CV")} <small>PDF</small></a>'
            f'<a class="btn ghost" href="mailto:{P["email"]}">{IC["mail"]}{L(lang, "Email me", "Pošalji email")}</a></div></div>'
            f'{side_html}</div></section>')

    worlds = "".join(world_tile(p, lang, path) for p in C.PROJECTS)
    work = (f'<section id="work"><div class="wrap"><div class="sh" style="margin-top:44px"><h2>{L(lang, "Four projects", "Četiri projekta")}</h2>'
            f'<p>{L(lang, "Three games and a web shop. Each page looks like its project.", "Tri igre i web shop. Svaka stranica izgleda kao njen projekat.")}</p></div>'
            f'<div class="worlds">{worlds}</div></div></section>')

    # experience, expandable
    rows = []
    for x in C.EXPERIENCE:
        org = f' <span>{L(lang, "at", "u")} {E(x["org"])}</span>' if x["org"] else ""
        pts = "".join(f"<li>{E(T(pt, lang))}</li>" for pt in x["points"])
        q = ""
        if x["org"] == "Alchemy Studio":
            q = (f'<blockquote class="quote"><p>{E(T(C.UI["letter_quote"], lang))}</p><cite>{E(T(C.UI["letter_by"], lang))} · '
                 f'<a href="{pre}{P["letter"]}">{L(lang, "Read the letter", "Pročitaj pismo")} (PDF)</a></cite></blockquote>')
        lk = ""
        if x["org"] == "Orior Media":
            lk = ('<p class="btns"><a class="btn ghost" href="https://oriormedia.com/">' + IC["ext"] + 'Orior Media</a>'
                  '<a class="btn ghost" href="https://joyrideservices.com/">' + IC["ext"] + 'JR Services</a></p>')
        rows.append(f'<details class="row"><summary><span class="when">{E(T(x["dates"], lang))}</span><span class="what">{E(T(x["role"], lang))}{org}</span>'
                    f'<span class="plus" aria-hidden="true"></span></summary><div class="body"><ul style="display:grid;gap:8px">{pts}</ul>{q}{lk}</div></details>')
    exp = (f'<section id="experience"><div class="wrap"><div class="sh"><h2>{L(lang, "Experience", "Iskustvo")}</h2>'
           f'<p>{L(lang, "Open a row for the details.", "Otvori red za detalje.")}</p></div><div class="rows">{"".join(rows)}</div></div></section>')

    # more projects, grouped by type
    groups = {}
    for e in EARLIER:
        ty, _ = META[e["slug"]]
        groups.setdefault(ty, []).append(e)
    order = [k for k in TYPES if k in groups]
    cards = []
    for k in order:
        for e in groups[k]:
            th = thumb_of(e)
            img = f'<img src="{pre}{th}" alt="" loading="lazy">' if th else ""
            chips = "".join(f"<span>{E(x.strip())}</span>" for x in e["stack"].split(",") if x.strip())
            cards.append(f'<a class="card" href="{rel(path, e_item_path(lang, e["slug"]))}"><span class="ct">{img}<span class="ck">{E(T(TYPES[k], lang))}</span></span><span class="cb">'
                         f'<span class="cn">{E(e["name"])}</span><span class="cs">{E(T(e["summary"], lang))}</span><span class="cst">{chips}</span></span></a>')
    gh = [f'<div class="cards">{"".join(cards)}</div>']
    more = (f'<section id="more"><div class="wrap"><div class="sh"><h2>{L(lang, "Smaller projects", "Manji projekti")}</h2>'
            f'<p>{L(lang, "Coursework, learning projects and early work. Open one for screenshots and details.", "Fakultetski zadaci, projekti za učenje i rani radovi. Otvori jedan za slike i detalje.")}</p></div>'
            f'<div>{"".join(gh)}</div></div></section>')

    ed = C.EDUCATION[0]
    awards = [a for a in C.AWARDS if any(w in T(a["title"], "en") for w in ("1st place", "Scholarship", "TOEFL", "Participant"))]
    facts = "".join(f"<li><b>{E(T(a['title'], lang))}</b><span>{E(T(a['sub'], lang))}</span></li>" for a in awards)
    edu = (f'<section id="education"><div class="wrap"><div class="two"><div><div class="sh"><h2>{L(lang, "Education", "Obrazovanje")}</h2></div>'
           f'<ul class="facts"><li><b>SSST</b><span>{E(T(ed["what"], lang))}, {E(T(ed["dates"], lang))}. '
           f'{L(lang, "GPA 8.58 out of 10.", "Prosjek 8,58 od 10.")}</span></li>'
           f'<li><b>{L(lang, "Courses", "Predmeti")}</b><span>{L(lang, "Top grades in Programming and Calculus (10), then OOP, databases, web, and data structures and algorithms (9).", "Najviše ocjene iz programiranja i kalkulusa (10), zatim OOP, baze podataka, web te strukture podataka i algoritmi (9).")}</span></li></ul></div>'
           f'<div><div class="sh"><h2>{L(lang, "Recognition", "Priznanja")}</h2><p><a href="{rel(path, page_path(lang, "about"))}#certs">{L(lang, "All certificates", "Svi certifikati")}</a></p></div>'
           f'<ul class="facts stack">{facts}</ul></div></div></div></section>')

    contact = (f'<section id="contact"><div class="wrap"><div class="sh"><h2>{L(lang, "Contact", "Kontakt")}</h2>'
               f'<p>{L(lang, "Email is the fastest way to reach me.", "Email je najbrži način da me kontaktirate.")}</p></div>'
               f'<a class="contact-big" id="email-text" href="mailto:{P["email"]}">{P["email"]}</a>'
               f'<div class="c-row"><button class="btn ghost" type="button" data-copy="{P["email"]}" data-done="{L(lang, "Copied", "Kopirano")}">{IC["copy"]}<span>{L(lang, "Copy address", "Kopiraj adresu")}</span></button>'
               f'<a class="btn ghost" href="{P["linkedin"]}">{IC["linkedin"]}LinkedIn</a><a class="btn ghost" href="{P["github"]}">{IC["github"]}GitHub</a>'
               f'<a class="btn ghost" href="tel:+38761222430">{IC["phone"]}+387 61 222 430</a></div></div></section>')

    body = header(lang, path, "home") + f'<main id="main">{hero}{work}{exp}{more}{edu}{contact}</main>' + footer(lang, path)
    return path, "Harun Kestendžić", T(C.HOME["description"], lang), body


# ============================================================== about page
def build_about(lang):
    path = page_path(lang, "about")
    pre = rel(path, "")
    P = C.PERSON
    head = (f'<section class="a-head"><div class="wrap"><h1>{L(lang, "About me", "O meni")}</h1>'
            f'<p>{L(lang, "I am a Computer Science student at SSST in Sarajevo, minoring in Electrical Engineering. I work mostly in C#: a solo game released and played 800+ times, a 16,000-line roguelike in development, and ten months as a junior game developer in a studio. Now I am moving towards backend and AI engineering, through a web shop I deployed on Oracle Cloud and the Backend AI Engineering track at FlyRank.", "Student sam računarskih nauka na SSST-u u Sarajevu, s minorom iz elektrotehnike. Najviše radim u C#-u: samostalno napravljena igra objavljena i igrana 800+ puta, roguelike od 16.000 linija koda u razvoju i deset mjeseci kao junior game developer u studiju. Sada idem prema backendu i AI inženjeringu, kroz web shop koji sam postavio na Oracle Cloud i smjer Backend AI Engineering u FlyRanku.")}</p>'
            f'<div class="btns" style="margin-top:24px"><a class="btn" href="{pre}{P["cv"]}">{IC["download"]}{L(lang, "Download CV", "Preuzmi CV")} <small>PDF</small></a>'
            f'<a class="btn ghost" href="{pre}{P["letter"]}">{L(lang, "Recommendation letter", "Pismo preporuke")} <small>PDF</small></a></div></div></section>')
    sk = "".join(f'<div><b>{E(T(n, lang))}</b><span>{E(T(ev, lang))}</span></div>' for n, lv, ev in C.SKILLS)
    skills = (f'<section><div class="wrap"><div class="sh"><h2>{E(T(C.HOME["skills_h"], lang))}</h2><p>{E(T(C.HOME["skills_intro"], lang))}</p></div>'
              f'<div class="skills">{sk}</div></div></section>')
    rows = "".join(
        f'<details class="row"><summary><span class="when">{E(T(e["dates"], lang))}</span><span class="what">{E(T(e["school"], lang))} <span>{E(T(e["what"], lang))}</span></span>'
        f'<span class="plus" aria-hidden="true"></span></summary><div class="body"><p>{E(T(e["detail"], lang))}</p></div></details>' for e in C.EDUCATION)
    edu = f'<section><div class="wrap"><div class="sh"><h2>{L(lang, "Education", "Obrazovanje")}</h2></div><div class="rows">{rows}</div></div></section>'
    note = T(C.FORMER_NAME_NOTE, lang)
    with_img = [x for x in C.AWARDS if x.get("img")]
    no_img = [x for x in C.AWARDS if not x.get("img")]

    def cert(x):
        return (f'<a href="{pre}{x.get("link", x["img"])}" target="_blank" rel="noopener"><span class="ci"><img src="{pre}{x["img"]}" alt="{E(T(x["title"], lang))}" loading="lazy"></span>'
                f'<b>{E(T(x["title"], lang))}</b><span>{E(T(x["sub"], lang))}</span>' + (f'<small>{E(note)}</small>' if x.get("former") else "") + "</a>")
    first, rest = with_img[:4], with_img[4:]
    other = "".join(f"<li><b>{E(T(x['title'], lang))}</b><span>{E(T(x['sub'], lang))}</span></li>" for x in no_img)
    certs = (f'<section id="certs"><div class="wrap"><div class="sh"><h2>{E(T(C.HOME["awards_h"], lang))}</h2><p>{E(T(C.HOME["press_p"], lang))}</p></div>'
             f'<div class="certs">{"".join(cert(x) for x in first)}</div>'
             f'<details class="more"><summary><span class="plus" aria-hidden="true"></span>{L(lang, f"Show {len(rest)} more", f"Prikaži još {len(rest)}")}</summary>'
             f'<div class="inner certs">{"".join(cert(x) for x in rest)}</div></details>'
             f'<ul class="facts" style="margin-top:28px">{other}</ul></div></section>')
    body = header(lang, path, "about") + f'<main id="main">{head}{skills}{edu}{certs}</main>' + footer(lang, path)
    return path, L(lang, "About me", "O meni") + " | Harun Kestendžić", T(C.HOME["description"], lang), body


# ====================================================== smaller project page
def build_earlier_item(e, i, lang):
    path = e_item_path(lang, e["slug"])
    pre = rel(path, "")
    home = rel(path, page_path(lang, "home"))
    pts = "".join(f"<li>{md_inline(T(x, lang))}</li>" for x in e["points"])
    nxt = f'<p class="note" style="margin-top:16px"><b>{L(lang, "What I would change", "Šta bih promijenio")}:</b> {E(T(e["next"], lang))}</p>' if e.get("next") else ""
    note = f'<p class="note" style="margin-top:16px">{fmt_todo(T(e["note"], lang))}</p>' if e.get("note") else ""
    lk = ""
    for n, u in e["links"]:
        if not u.startswith("http"):
            u = rel(path, ("" if lang == "en" else "bs/") + u)
        lk += f'<a class="btn ghost" href="{u}">{E(T(n, lang))}</a>'
    ty, _ = META[e["slug"]]
    aside = (f'<dl class="e-aside"><div><dt>{L(lang, "Type", "Vrsta")}</dt><dd>{E(T(TYPES[ty], lang))}</dd></div>'
             f'<div><dt>{L(lang, "What it is", "Šta je")}</dt><dd>{E(T(e["kind"], lang))}</dd></div>'
             + (f'<div><dt>{L(lang, "Built with", "Napravljeno sa")}</dt><dd>{E(e["stack"])}</dd></div>' if e["stack"] else "")
             + (f'<div class="btns">{lk}</div>' if lk else "") + '</dl>')
    em = "".join(media_fig(m, lang, pre, "wide" if m.get("wide") else "") for m in e.get("media", []))
    gal = f'<div class="gal">{em}</div>' if em else ""
    nx = EARLIER[(i + 1) % len(EARLIER)]
    nav = (f'<nav class="pnav"><a href="{home}#more"><span>{L(lang, "Back to", "Nazad na")}</span>{L(lang, "Smaller projects", "Manje projekte")}</a>'
           f'<a href="{rel(path, e_item_path(lang, nx["slug"]))}"><span>{L(lang, "Next", "Sljedeći")}</span>{E(nx["name"])}</a></nav>')
    main = (f'<section class="e-head"><div class="wrap"><p class="e-crumb"><a href="{home}#more">{L(lang, "Smaller projects", "Manji projekti")}</a></p>'
            f'<h1>{E(e["name"])}</h1><p class="sum">{E(T(e["summary"], lang))}</p></div></section>'
            f'<div class="wrap"><div class="e-body"><div><ul class="e-pts">{pts}</ul>{nxt}{note}</div>{aside}</div>{gal}{nav}</div>')
    body = header(lang, path, "work") + f'<main id="main">{main}</main>' + footer(lang, path)
    return path, f'{e["name"]} | Harun Kestendžić', T(e["summary"], lang), body


# =================================================================== main
def write(path, html):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def page_id(path):
    p = path[:-5]
    lang = "bs" if p.startswith("bs/") else "en"
    p = p[3:] if lang == "bs" else p
    return lang + "-" + p.replace("projects/", "").replace("/", "-")


def single_page(pages):
    import posixpath
    import re
    ids = {path: page_id(path) for _, path, _, _, _ in pages}

    def fix(body, path):
        base = posixpath.dirname(path)

        def href(m):
            attr, url = m.group(1), m.group(2)
            if re.match(r"^(https?:|mailto:|tel:|data:)", url):
                return m.group(0)
            frag = ""
            if "#" in url:
                url, frag = url.split("#", 1)
            target = posixpath.normpath(posixpath.join(base, url)) if url else path
            if target in ids:
                return f'{attr}="#{ids[target]}' + ("." + frag if frag else "") + '"'
            extra = ' target="_blank" rel="noopener"' if attr == "href" and "target=" not in m.group(0) else ""
            return f'{attr}="{target}"{extra}'
        return re.sub(r'(href|src|poster)="([^"]*)"', href, body)

    blocks = [f'<div class="pg" data-page="{ids[path]}" data-title="{E(title)}" lang="{lang}" hidden>{fix(body, path)}</div>'
              for lang, path, title, desc, body in pages]
    router = """<script>
(function(){
  var pages=document.querySelectorAll('.pg');
  function show(){
    var h=(location.hash||'').slice(1), parts=h.split('.'), id=parts[0]||'en-index', sec=parts[1], found=false;
    pages.forEach(function(p){var on=p.getAttribute('data-page')===id; p.hidden=!on; if(on){found=true; document.title=p.getAttribute('data-title');}});
    if(!found){pages.forEach(function(p){p.hidden=p.getAttribute('data-page')!=='en-index'});}
    var cur=document.querySelector('.pg:not([hidden])'), el=sec&&cur?cur.querySelector('#'+sec):null;
    if(el){if(el.tagName==='DETAILS')el.open=true; el.scrollIntoView();}else{window.scrollTo(0,0);}
  }
  window.addEventListener('hashchange',show); show();
})();
</script>"""
    home = next(x for x in pages if x[1] == "index.html")
    return document("en", "index.html", home[2], home[3], "".join(blocks) + router, fragment=True)


def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    pages = []
    for lang in LANGS:
        pages.append((lang,) + build_home(lang))
        pages.append((lang,) + build_about(lang))
        for i, p in enumerate(C.PROJECTS):
            pages.append((lang,) + build_project(p, lang, i))
        for i, e in enumerate(EARLIER):
            pages.append((lang,) + build_earlier_item(e, i, lang))
    for lang, path, title, desc, body in pages:
        write(path, document(lang, path, title, desc, body))
    import re as _re
    used = set()
    for _, _, _, _, body in pages:
        used.update(_re.findall(r'assets/[^"\'#?) ]+', body))
    used.update(["assets/" + C.PERSON["cv"].split("assets/")[-1], C.PERSON["letter"], "assets/og-card.png"])
    removed = 0
    for dp, _, fs in os.walk(os.path.join(DIST, "assets")):
        for fn in fs:
            rp = os.path.relpath(os.path.join(dp, fn), DIST).replace(os.sep, "/")
            if rp not in used:
                os.remove(os.path.join(dp, fn)); removed += 1
    if ARTIFACT:
        write("_root_fragment.html", single_page(pages))
    print("built", len(pages), "pages; removed", removed, "unused files")


if __name__ == "__main__":
    main()
