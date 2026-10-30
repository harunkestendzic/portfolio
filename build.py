# -*- coding: utf-8 -*-
"""Static site generator. Run: python3 build.py  ->  writes dist/

Pages: index.html, devlog.html, projects/<slug>.html, and the same under bs/.
`python3 build.py --artifact` also writes dist/_root_fragment.html (the home page
without <html>/<head>, used for the Claude artifact preview)."""
import math
import os
import shutil
import sys
from html import escape as E

import content as C
from earlier import EARLIER, META, TYPES, LENSES
from diagrams import DIAGRAMS

ROOT = os.path.dirname(os.path.abspath(__file__))
ARTIFACT = "--artifact" in sys.argv
DIST = os.path.join(ROOT, "dist")
LANGS = ("en", "bs")

FONTS = ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800"
         "&family=Instrument+Sans:ital,wght@0,400..700;1,400&family=JetBrains+Mono:wght@400;500&display=swap")

CSS = r"""
/* Layout: one 1160px column; home sections use a left label rail + content; projects lead with a visual. */
:root{
  --bg:#F2F4F3; --surface:#FFFFFF; --sunk:#E8ECEB; --ink:#152120; --muted:#566563; --line:#D3DCDA;
  --accent:#0B7268; --accent-ink:#FFFFFF; --accent-soft:#DDEFEC;
  --hydro:#0E8AA0; --vulcan:#C2481B; --solar:#A97C0C;
  --ramo:#1B1BCF; --ramo-ink:#FFFFFF; --arcane:#0F1C22;
  --font-display:"Bricolage Grotesque", "Avenir Next", "Segoe UI", system-ui, sans-serif;
  --font-body:"Instrument Sans", "Segoe UI", system-ui, -apple-system, sans-serif;
  --font-code:"JetBrains Mono", ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  --step--1:.875rem; --step-0:1.0625rem; --step-1:1.25rem; --step-2:1.6rem; --step-3:2.2rem;
  --step-4:clamp(2.6rem, 5.4vw, 4.6rem);
  --r-sm:8px; --r-lg:16px;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0F1918; --surface:#152221; --sunk:#1A2A29; --ink:#E5EEEC; --muted:#93A6A3; --line:#2A3D3B;
  --accent:#55C9BA; --accent-ink:#062320; --accent-soft:#183531;
  --hydro:#4CC5D8; --vulcan:#F0844F; --solar:#E5BE4C; color-scheme:dark; } }
:root[data-theme="dark"]{
  --bg:#0F1918; --surface:#152221; --sunk:#1A2A29; --ink:#E5EEEC; --muted:#93A6A3; --line:#2A3D3B;
  --accent:#55C9BA; --accent-ink:#062320; --accent-soft:#183531;
  --hydro:#4CC5D8; --vulcan:#F0844F; --solar:#E5BE4C; color-scheme:dark; }

*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--font-body);font-size:var(--step-0);line-height:1.6;
  text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
.site{min-height:100%}
.wrap{max-width:1160px;margin:0 auto;padding-left:max(20px, env(safe-area-inset-left, 0px));padding-right:max(20px, env(safe-area-inset-right, 0px))}
a{color:inherit;text-decoration-color:color-mix(in srgb, var(--accent) 60%, transparent);text-underline-offset:3px;text-decoration-thickness:1.5px}
a:hover{color:var(--accent)}
:focus-visible{outline:2.5px solid var(--accent);outline-offset:3px;border-radius:4px}
h1,h2,h3,h4{font-family:var(--font-display);font-weight:700;line-height:1.08;letter-spacing:-.02em;margin:0;text-wrap:balance}
p{margin:0}
.skip{position:absolute;left:-999px;top:8px;background:var(--surface);padding:8px 12px;border-radius:var(--r-sm);z-index:20}
.skip:focus{left:16px}

/* header */
.top{border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:24px;padding-block:18px;flex-wrap:wrap}
.mark{font-family:var(--font-display);font-weight:700;font-size:1.15rem;letter-spacing:-.01em;text-decoration:none;margin-right:auto;display:flex;align-items:center;gap:10px}
.mark-hex{width:22px;height:22px;flex:none}
.mark-hex path{fill:var(--accent)}
.nav{display:flex;gap:6px 22px;flex-wrap:wrap;align-items:center;font-size:.98rem}
.nav a{text-decoration:none;color:var(--muted)}
.nav a:hover,.nav a[aria-current="page"]{color:var(--ink)}
.lang{font-weight:600;border:1px solid var(--line);border-radius:999px;padding:3px 12px;color:var(--ink)!important}
.lang:hover{border-color:var(--accent)}

/* buttons */
.btns{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:600;font-size:1rem;text-decoration:none;padding:11px 18px;border-radius:999px;border:1.5px solid var(--ink);color:var(--ink);background:transparent;cursor:pointer;font-family:inherit}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.primary:hover{filter:brightness(1.08);color:var(--accent-ink)}
.btn small{font-weight:500;opacity:.75}

/* hero */
.hero .wrap{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:56px;padding-block:72px 56px;align-items:end}
.hero h1{font-size:var(--step-4);font-weight:750;letter-spacing:-.035em;max-width:13ch}
.hero .lede{margin-top:24px;font-size:var(--step-1);line-height:1.55;color:var(--muted);max-width:60ch}
.hero .btns{margin-top:32px}
.brief{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:24px 26px}
.brief h2{font-size:1rem;font-family:var(--font-body);font-weight:600;color:var(--muted);letter-spacing:0;margin-bottom:6px}
.brief dl{margin:0;display:grid;gap:0}
.brief div{padding:12px 0;border-top:1px solid var(--line)}
.brief div:first-child{border-top:0}
.brief dt{font-size:var(--step--1);color:var(--muted)}
.brief dd{margin:2px 0 0;font-weight:500;line-height:1.4}

/* proof */
.proof{border-block:1px solid var(--line);background:var(--surface)}
.proof ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr))}
.proof li{padding:26px 24px 26px 0;display:grid;gap:6px;align-content:start}
.proof li + li{padding-left:24px;border-left:1px solid var(--line)}
.proof b{font-family:var(--font-display);font-size:var(--step-3);font-weight:700;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.proof span{color:var(--muted);font-size:.95rem;line-height:1.45}

/* sections */
.sec{padding-block:88px 0}
.sec > .wrap{display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px 48px}
.sec-h h2{font-size:var(--step-2)}
.sec-h p{color:var(--muted);margin-top:12px;font-size:.98rem;max-width:30ch}
.stack{display:grid;gap:56px;min-width:0}
.sec.wide > .wrap{grid-template-columns:1fr;gap:32px}
.sec.wide .sec-h{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 32px}
.sec.wide .sec-h p{max-width:60ch;margin:0}
.feat + .feat{padding-top:56px;border-top:1px solid var(--line)}
.blk.wide{grid-template-columns:1fr}
.feat-link{display:block;text-decoration:none;color:inherit}

/* project feature */
.feat{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:36px;align-items:center}
.feat-v{display:block;border-radius:var(--r-lg);overflow:hidden;aspect-ratio:16/11;max-width:100%;position:relative}
.feat-t{display:grid;gap:14px;min-width:0}
.feat h3{font-size:var(--step-3)}
.feat h3 a{text-decoration:none}
.hook{font-family:var(--font-display);font-size:var(--step-1);font-weight:500;line-height:1.35;letter-spacing:-.01em}
.feat .sum{color:var(--muted)}
.facts{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px}
.facts li{font-size:.9rem;font-weight:500;background:var(--accent-soft);border-radius:999px;padding:4px 12px}
.tags{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.88rem;color:var(--muted)}
.status{display:inline-flex;align-items:center;gap:8px;font-size:.88rem;font-weight:600}
.status::before{content:"";width:9px;height:9px;border-radius:50%;background:var(--muted)}
.status.live::before{background:#2FA36B}
.status.dev::before{background:var(--solar)}
.status.early::before{background:var(--hydro)}
.status.uni::before{background:var(--accent)}
.compact{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.6fr);gap:28px;align-items:center;border-top:1px solid var(--line);padding-top:24px}
.compact .feat-v{aspect-ratio:16/10}
.compact h3{font-size:var(--step-2)}
.compact h3 a{text-decoration:none}
@media (max-width:600px){.compact{grid-template-columns:1fr}}
.more{color:var(--accent);font-weight:600;text-decoration:none}
.more:hover{text-decoration:underline}

/* cover visuals */
.cv-ramo{background:var(--ramo);color:var(--ramo-ink);display:flex;align-items:flex-end;justify-content:center;gap:4%;padding:7% 6% 0 22%}
.cv-ramo::after{content:"";position:absolute;inset:auto 0 0;height:13%;background:repeating-linear-gradient(90deg,#3a3a3a 0 26px,#4a4a4a 26px 52px)}
.cv-ramo img{image-rendering:pixelated;position:relative;z-index:1;margin-bottom:7.5%;height:auto}
.cv-ramo .logo{position:absolute;left:4%;top:7%;width:19%;z-index:2}
.cv-ramo .tt{position:absolute;right:5%;top:7%;font:600 .8rem/1.3 var(--font-code);text-align:right;opacity:.92;z-index:2}
.cv-arcane{background:var(--arcane)}
.cv-art{background:#000}
.cv-art .art{width:100%;height:100%;object-fit:cover;display:block}
.cv-art .spr{position:absolute;bottom:9%;image-rendering:pixelated;height:auto;z-index:1}
.cv-art .ground{position:absolute;left:0;right:0;bottom:0;height:9%;background:repeating-linear-gradient(90deg,#2b2b2b 0 26px,#383838 26px 52px)}
.spr-a{width:7%;right:4%;bottom:5%}.spr-b{width:5%;left:4%;bottom:6%}
.strip{display:flex;align-items:flex-end;justify-content:flex-end;gap:22px;padding-top:14px;opacity:.9}
.strip img{image-rendering:pixelated;width:auto}
.strip{border-bottom:3px solid var(--line);padding-bottom:0;margin-top:8px}
.vframe{position:relative;aspect-ratio:16/9;border-radius:var(--r-lg);overflow:hidden;background:#000;max-width:100%}
.vframe iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.vcard{display:flex;align-items:center;gap:16px;padding:20px;border:1px solid var(--line);border-radius:var(--r-lg);background:var(--surface);text-decoration:none;aspect-ratio:16/9;max-width:100%}
.vcard:hover{border-color:var(--accent)}
.vplay{width:56px;height:56px;border-radius:50%;background:var(--accent);flex:none;position:relative}
.vplay::after{content:"";position:absolute;left:22px;top:17px;border-left:16px solid var(--accent-ink);border-top:11px solid transparent;border-bottom:11px solid transparent}
.cv-arcane svg{width:100%;height:100%;display:block}
.cv-ph{background:var(--sunk);border:1.5px dashed var(--line);display:grid;place-items:center;text-align:center;padding:24px;color:var(--muted)}
.cv-ph b{display:block;font-family:var(--font-display);font-size:var(--step-3);color:var(--ink);margin-bottom:6px}

/* other projects */
.wk-controls{display:grid;gap:14px;margin-bottom:12px}.wk-controls[hidden]{display:none}
.wk-row{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}.wk-row>b{min-width:110px;font-size:.92rem}
.wk-h{font-size:var(--step-1);margin:36px 0 16px}.wk-out>.egrid{margin-bottom:8px}
.etags{font-size:.82rem;color:var(--muted)}.cwrap{display:block;border-radius:var(--r-lg);overflow:hidden;aspect-ratio:16/10}.cwrap>*{width:100%;height:100%;object-fit:cover}
.egrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:28px 22px}
.ecard{display:grid;gap:6px;align-content:start;text-decoration:none;color:inherit}
.ecard h3,.ecard h4{font-size:1.1rem;font-family:var(--font-body);font-weight:650;letter-spacing:0}
.ecard p{color:var(--muted);font-size:.95rem;line-height:1.5}.ecard:hover h3,.ecard:hover h4{color:var(--accent)}
.ecard .lang-tag{font-size:.82rem;color:var(--accent);font-weight:600}
.ethumb{aspect-ratio:16/10;border:1.5px dashed var(--line);border-radius:var(--r-lg);background:var(--sunk);display:grid;place-content:center;gap:4px;text-align:center;padding:12px;color:var(--muted);font-size:.9rem;max-width:100%}
.ethumb b{font-size:.78rem;font-weight:700;color:var(--vulcan)}
.p-head .ethumb{max-width:520px}
.ethumb.has-img{border:1px solid var(--line);padding:0;display:block;overflow:hidden;background:#101415}
.ethumb.has-img img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.others{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:0;border-top:1px solid var(--line)}
.others a{text-decoration:none}.others h4 a{color:inherit}.others div{padding:18px 18px 18px 0;border-bottom:1px solid var(--line);display:grid;gap:4px;align-content:start}
.others h4{font-size:1.05rem;font-family:var(--font-body);font-weight:600;letter-spacing:0}
.others .lang-tag{font-size:.82rem;color:var(--accent);font-weight:600}
.others p{color:var(--muted);font-size:.95rem;line-height:1.5}

/* timeline / lists */
.rows{display:grid;gap:0;border-top:1px solid var(--line)}
.row{display:grid;grid-template-columns:200px minmax(0,1fr);gap:8px 32px;padding:24px 0;border-bottom:1px solid var(--line)}
.row .when{color:var(--muted);font-size:.95rem;font-variant-numeric:tabular-nums}
.row h3{font-size:var(--step-1);font-weight:650;letter-spacing:-.01em}
.row h3 span{color:var(--muted);font-weight:500}
.row ul{margin:10px 0 0;padding-left:1.1em;display:grid;gap:6px;color:var(--muted)}
.row p{color:var(--muted);margin-top:8px;max-width:70ch}

.skills{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;border-top:1px solid var(--line)}
.skill{padding:16px 0;border-bottom:1px solid var(--line);display:grid;gap:3px;align-content:start}
.skill b{font-weight:600}
.skill span{color:var(--muted);font-size:.95rem}
.skill em{font-style:normal;font-size:.8rem;font-weight:600;color:var(--accent);margin-left:8px}

.awards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 40px;border-top:1px solid var(--line)}
.awards li{padding:14px 0;border-bottom:1px solid var(--line);display:grid;align-content:start}
.awards span{color:var(--muted);font-size:.95rem}
.quote{margin:18px 0 0;padding:16px 20px;border-left:3px solid var(--accent);background:var(--surface);border-radius:0 var(--r-sm) var(--r-sm) 0;display:grid;gap:6px;max-width:68ch}
.quote p{font-family:var(--font-display);font-size:var(--step-1);font-weight:500;line-height:1.35;color:var(--ink)}
.quote .qby{color:var(--muted);font-size:.9rem}
.certs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:24px}
.cert{display:grid;gap:4px;text-decoration:none;color:inherit;align-content:start}
.cert-img{display:block;aspect-ratio:4/3;border-radius:var(--r-sm);overflow:hidden;border:1px solid var(--line);background:var(--surface);margin-bottom:8px}
.cert-img img{width:100%;height:100%;object-fit:contain;padding:8px;display:block;transition:transform .3s}
.cert:hover .cert-img img{transform:scale(1.03)}
.cert b{font-weight:600;line-height:1.35}
.cert .csub{color:var(--muted);font-size:.92rem}
.cert .former{color:var(--muted);font-size:.8rem;font-style:italic}
@media (prefers-reduced-motion: reduce){.cert-img img{transition:none}}
.press{margin-top:28px;color:var(--muted);max-width:60ch}

.posts{display:grid;gap:0;border-top:1px solid var(--line)}
.prose{max-width:68ch}.shot{margin:1.4em 0;aspect-ratio:16/9;display:grid;place-items:center;text-align:center;padding:20px;border:1.5px dashed var(--line);border-radius:var(--r-lg);background:var(--sunk);font-size:.95rem}.prose h2{margin:2.2em 0 .6em;font-size:var(--step-2)}.prose p,.prose ul{margin:0 0 1em}.prose ul{padding-left:1.2em}.prose li{margin:.35em 0}.prose pre{margin:1.2em 0}.prose code{font-family:var(--font-code);font-size:.92em}
.post{display:grid;grid-template-columns:130px minmax(0,1fr);gap:6px 28px;padding:22px 0;border-bottom:1px solid var(--line)}
.post time{color:var(--muted);font-size:.95rem;font-variant-numeric:tabular-nums}
.post h3{font-size:var(--step-1);font-weight:650;letter-spacing:-.01em}
.post p{color:var(--muted);margin-top:6px;max-width:68ch}
.dl-controls{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;margin:0 0 8px}
.dl-controls[hidden]{display:none}.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:inherit;font-size:.92rem;font-weight:550;padding:7px 14px;border-radius:999px;border:1px solid var(--line);background:transparent;color:var(--ink);cursor:pointer}
.chip span{color:var(--muted);font-weight:450;margin-left:4px}.chip:hover{border-color:var(--accent)}
.chip[aria-pressed="true"]{background:var(--ink);color:var(--bg);border-color:var(--ink)}.chip[aria-pressed="true"] span{color:inherit;opacity:.7}
.chip:focus-visible,.dl-sort select:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.dl-sort{font-size:.92rem;color:var(--muted);display:flex;gap:8px;align-items:center}
.dl-sort select{font:inherit;color:var(--ink);background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 10px}
.dl-count{font-size:.85rem;color:var(--muted);margin:4px 0 0}.post[hidden]{display:none}
.ptag{display:inline-block;font-size:.8rem;font-weight:600;color:var(--accent);margin-left:10px;letter-spacing:0;font-family:var(--font-body);vertical-align:middle}

.contact-card{display:grid;gap:18px}
.contact-line{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px}
.contact-line .big{font-family:var(--font-display);font-size:clamp(1.4rem,3.6vw,2.4rem);font-weight:700;letter-spacing:-.02em;word-break:break-all}
.copy{font:600 .9rem var(--font-body);border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer}
.copy:hover{border-color:var(--accent)}
.contact-meta{color:var(--muted);display:flex;flex-wrap:wrap;gap:6px 24px}

footer{margin-top:120px;border-top:1px solid var(--line)}
footer .wrap{display:flex;flex-wrap:wrap;gap:8px 24px;padding-block:28px;color:var(--muted);font-size:.9rem}
footer .wrap span:first-child{margin-right:auto}

/* project page */
.p-head .wrap{padding-block:48px 40px;display:grid;gap:22px}
.crumb{font-size:.95rem;color:var(--muted)}
.crumb a{text-decoration:none}
.p-head h1{font-size:clamp(3rem,9vw,6.5rem);letter-spacing:-.045em;font-weight:780}
.p-head .hook{font-size:clamp(1.25rem,2.4vw,1.7rem);max-width:34ch}
.meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0;border-top:1px solid var(--line);margin:0}
.meta div{padding:14px 18px 14px 0}
.meta div + div{padding-left:18px;border-left:1px solid var(--line)}
.meta dt{font-size:var(--step--1);color:var(--muted)}
.meta dd{margin:2px 0 0;font-weight:500;line-height:1.4}
.p-cover{aspect-ratio:21/9}
.p-body{display:grid;gap:96px;padding-top:72px}
.blk{display:grid;grid-template-columns:220px minmax(0,1fr);gap:20px 48px}
.blk > h2{font-size:var(--step-2)}
.prose{display:grid;gap:16px;max-width:68ch;font-size:1.1rem}
.prose p{line-height:1.7}
.nums{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));border-top:1px solid var(--line)}
.nums li{padding:18px 18px 18px 0;display:grid;gap:4px}
.nums b{font-family:var(--font-display);font-size:var(--step-3);font-weight:700;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.nums span{color:var(--muted);font-size:.95rem}
.built{margin:0;padding:0;list-style:none;display:grid;gap:0;border-top:1px solid var(--line);max-width:76ch}
.built li{padding:14px 0 14px 28px;border-bottom:1px solid var(--line);position:relative}
.built li::before{content:"";position:absolute;left:4px;top:23px;width:10px;height:10px;border-radius:2px;background:var(--accent);transform:rotate(45deg)}
.figs{display:grid;gap:56px;min-width:0}
figure{margin:0;display:grid;gap:12px;min-width:0}
figure h3{font-size:var(--step-1);font-weight:650;letter-spacing:-.01em}
figcaption{color:var(--muted);font-size:.98rem;max-width:68ch}
.dg-box{background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:20px;overflow-x:auto}
.dg{display:block;width:100%;min-width:640px;height:auto}
.dg text{font-family:var(--font-body)}
.dn rect{fill:var(--surface);stroke:var(--line);stroke-width:1.5}
.dn.n-focus rect{fill:var(--accent-soft);stroke:var(--accent)}
.dn.n-hydro rect{stroke:var(--hydro);stroke-width:2}
.dn.n-vulcan rect{stroke:var(--vulcan);stroke-width:2}
.dn.n-solar rect{stroke:var(--solar);stroke-width:2.5}
.dt-title{fill:var(--ink);font-weight:600;font-size:17px}
.dt-sub{fill:var(--muted);font-size:14px}
.dt-tag{fill:var(--accent);font-weight:700;font-size:12px;letter-spacing:.04em}
.dt-label{fill:var(--muted);font-size:14px;font-style:italic}
.da{fill:none;stroke:var(--muted);stroke-width:1.6}
.da.a-hydro{stroke:var(--hydro)} .da.a-vulcan{stroke:var(--vulcan)}
.dm{fill:var(--muted)} .dm-hydro{fill:var(--hydro)} .dm-vulcan{fill:var(--vulcan)}
.dbrace{fill:none;stroke:var(--line);stroke-width:1.5;stroke-dasharray:4 5}
.dtick{stroke:var(--muted);stroke-width:1}
.lb{stroke:none}
.lb-0{fill:color-mix(in srgb, var(--vulcan) 70%, var(--surface))}
.lb-1{fill:color-mix(in srgb, var(--vulcan) 35%, var(--surface))}
.lb-2{fill:var(--sunk)}
.lb-3{fill:color-mix(in srgb, var(--accent) 35%, var(--surface))}
.lb-4{fill:color-mix(in srgb, var(--accent) 70%, var(--surface))}
.lb-t{font-size:14px}
pre{margin:0;background:var(--sunk);border:1px solid var(--line);border-radius:var(--r-lg);padding:20px 22px;overflow-x:auto;font:400 .88rem/1.65 var(--font-code);color:var(--ink);tab-size:4}
.code-h{font:500 .85rem var(--font-code);color:var(--muted)}
.gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}
.gallery figure img{width:100%;border-radius:var(--r-lg);border:1px solid var(--line);display:block}
.ph{aspect-ratio:16/10;border:1.5px dashed var(--line);border-radius:var(--r-lg);background:var(--sunk);display:grid;place-content:center;gap:4px;text-align:center;padding:20px;color:var(--muted);max-width:100%}
.ph b{font-size:.8rem;font-weight:700;color:var(--vulcan);letter-spacing:.02em}
.wip{border:1px solid var(--line);border-left:4px solid var(--solar);border-radius:var(--r-lg);background:var(--sunk);padding:16px 20px;max-width:68ch}.wip b{display:block;font-size:.8rem;letter-spacing:.04em;text-transform:uppercase;margin-bottom:4px}.wip p{margin:0;color:var(--muted)}
.pnext{display:flex;justify-content:space-between;flex-wrap:wrap;gap:16px;border-top:1px solid var(--line);padding-top:28px}
.pnext a{font-family:var(--font-display);font-size:var(--step-2);font-weight:700;text-decoration:none;letter-spacing:-.02em}
.pnext span{display:block;font-family:var(--font-body);font-size:.9rem;color:var(--muted);font-weight:500;letter-spacing:0}
.todo{color:var(--vulcan)}

@media (max-width: 920px){
  .hero .wrap{grid-template-columns:1fr;gap:36px;padding-block:48px 40px}
  .proof ul{grid-template-columns:repeat(2,minmax(0,1fr))}
  .proof li:nth-child(3){padding-left:0;border-left:0}
  .proof li:nth-child(n+3){border-top:1px solid var(--line)}
  .sec > .wrap,.blk{grid-template-columns:1fr}
  .sec-h p{max-width:60ch}
  .feat{grid-template-columns:1fr;gap:20px}
  .meta{grid-template-columns:repeat(2,minmax(0,1fr))}
  .meta div:nth-child(3){padding-left:0;border-left:0}
  .sec{padding-block:64px 0}
}
@media (max-width: 600px){
  .proof ul,.skills,.awards,.gallery{grid-template-columns:1fr}
  .proof li,.proof li + li{padding-left:0;border-left:0}
  .proof li + li{border-top:1px solid var(--line)}
  .row,.post{grid-template-columns:1fr}
  .meta{grid-template-columns:1fr}
  .meta div + div{padding-left:0;border-left:0;border-top:1px solid var(--line)}
  .cv-ramo .tt{display:none}
  .p-cover{aspect-ratio:4/3}
}
@media (prefers-reduced-motion: no-preference){
  .hero h1,.hero .lede,.hero .btns,.brief{animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
  .hero .lede{animation-delay:.06s}.hero .btns{animation-delay:.12s}.brief{animation-delay:.18s}
  @keyframes rise{from{transform:translateY(10px)}to{transform:none}}
}
"""
CSS = CSS.replace("#566563", "#566563")

CSS += """
figure img[data-lb]{cursor:zoom-in;transition:transform .2s,box-shadow .2s}
figure img[data-lb]:hover{box-shadow:0 8px 28px rgba(0,0,0,.22)}
figure img[data-lb]:focus-visible{outline:3px solid var(--accent,#0a7d6d);outline-offset:3px}
.lb{position:fixed;inset:0;z-index:2000;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;padding:56px 64px 22px;background:rgba(8,12,12,.9)}
.lb[hidden]{display:none}
.lb-stage{flex:1;min-height:0;width:100%;display:grid;place-items:center}
.lb img{max-width:100%;max-height:100%;object-fit:contain;border-radius:8px;background:#fff}
.lb-cap{color:#e9efee;font-size:.95rem;line-height:1.45;text-align:center;max-width:min(80ch,100%);min-height:1.4em}
.lb-count{color:#9fb0ae;font-size:.8rem}
.lb button{position:absolute;display:grid;place-items:center;width:44px;height:44px;border:0;border-radius:50%;background:rgba(255,255,255,.14);color:#fff;font:inherit;font-size:1.5rem;line-height:1;cursor:pointer}
.lb button:hover{background:rgba(255,255,255,.28)}
.lb button:focus-visible{outline:3px solid #fff;outline-offset:2px}
.lb-close{top:12px;right:14px}
.lb-prev{left:12px;top:50%;transform:translateY(-50%)}
.lb-next{right:12px;top:50%;transform:translateY(-50%)}
@media (max-width:640px){.lb{padding:56px 10px 18px}.lb-prev,.lb-next{top:auto;bottom:14px;transform:none}.lb-prev{left:14px}.lb-next{right:14px}}
@media (prefers-reduced-motion: no-preference){.lb{animation:lbin .18s ease-out}@keyframes lbin{from{opacity:0}to{opacity:1}}}
"""

LB_JS = """
(function(){
  var T={en:{open:'Enlarge image: ',close:'Close',prev:'Previous image',next:'Next image',of:' of '},
         bs:{open:'Uvećaj sliku: ',close:'Zatvori',prev:'Prethodna slika',next:'Sljedeća slika',of:' od '}};
  var lb,img,cap,cnt,bc,bp,bn,items=[],idx=0,last=null,lang='en';
  function L(el){var n=el.closest('[lang]');return n&&n.getAttribute('lang')==='bs'?'bs':'en'}
  function ok(i){return i.tagName==='IMG'&&i.closest('figure')}
  function prep(){document.querySelectorAll('figure img').forEach(function(i){
    if(i.getAttribute('data-lb'))return; i.setAttribute('data-lb','1'); i.tabIndex=0; i.setAttribute('role','button');
    i.setAttribute('aria-label',T[L(i)].open+(i.alt||''));});}
  function build(){
    lb=document.createElement('div'); lb.className='lb'; lb.hidden=true; lb.setAttribute('role','dialog'); lb.setAttribute('aria-modal','true');
    lb.innerHTML='<button type="button" class="lb-close">&times;</button><button type="button" class="lb-prev">&#8249;</button><button type="button" class="lb-next">&#8250;</button>'+
      '<div class="lb-stage"><img alt=""></div><div class="lb-cap"></div><div class="lb-count"></div>';
    document.body.appendChild(lb);
    img=lb.querySelector('img'); cap=lb.querySelector('.lb-cap'); cnt=lb.querySelector('.lb-count');
    bc=lb.querySelector('.lb-close'); bp=lb.querySelector('.lb-prev'); bn=lb.querySelector('.lb-next');
    bc.addEventListener('click',close); bp.addEventListener('click',function(){step(-1)}); bn.addEventListener('click',function(){step(1)});
    lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-stage')||e.target===cap)close()});
  }
  function show(){
    var i=items[idx], fc=i.closest('figure').querySelector('figcaption'), s=T[lang];
    img.src=i.currentSrc||i.src; img.alt=i.alt||''; img.style.imageRendering=getComputedStyle(i).imageRendering;
    cap.textContent=fc?fc.textContent:(i.alt||''); lb.setAttribute('aria-label',i.alt||'');
    bc.setAttribute('aria-label',s.close); bp.setAttribute('aria-label',s.prev); bn.setAttribute('aria-label',s.next);
    var many=items.length>1; bp.hidden=bn.hidden=!many; cnt.textContent=many?(idx+1)+s.of+items.length:'';
  }
  function open(i){
    if(!lb)build(); lang=L(i); last=i;
    var scope=i.closest('main')||document; items=[].filter.call(scope.querySelectorAll('figure img'),ok); idx=items.indexOf(i); if(idx<0){items=[i];idx=0}
    show(); lb.hidden=false; document.documentElement.style.overflow='hidden'; bc.focus();
  }
  function close(){if(!lb||lb.hidden)return; lb.hidden=true; document.documentElement.style.overflow=''; if(last)last.focus();}
  function step(d){idx=(idx+d+items.length)%items.length; show();}
  document.addEventListener('click',function(e){var t=e.target; if(t.getAttribute&&t.getAttribute('data-lb')&&ok(t)){e.preventDefault();open(t)}});
  document.addEventListener('keydown',function(e){
    var t=e.target;
    if(lb&&!lb.hidden){
      if(e.key==='Escape'){e.preventDefault();close()}
      else if(e.key==='ArrowLeft'&&items.length>1){e.preventDefault();step(-1)}
      else if(e.key==='ArrowRight'&&items.length>1){e.preventDefault();step(1)}
      else if(e.key==='Tab'){var f=[].filter.call(lb.querySelectorAll('button'),function(b){return !b.hidden});
        if(!f.length)return; var a=f.indexOf(document.activeElement);
        if(e.shiftKey&&a<=0){e.preventDefault();f[f.length-1].focus()} else if(!e.shiftKey&&a===f.length-1){e.preventDefault();f[0].focus()}}
      return;}
    if((e.key==='Enter'||e.key===' ')&&t.getAttribute&&t.getAttribute('data-lb')&&ok(t)){e.preventDefault();open(t)}
  });
  prep();
})();
"""

JS = """<script>
document.querySelectorAll('[data-copy]').forEach(function(b){
  b.addEventListener('click',function(){
    var v=b.getAttribute('data-copy'),done=b.getAttribute('data-done'),orig=b.textContent;
    function ok(){b.textContent=done;setTimeout(function(){b.textContent=orig},1600)}
    function fallback(){var el=document.getElementById(b.getAttribute('data-target'));
      if(el){var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r)}}
    try{navigator.clipboard.writeText(v).then(ok,fallback)}catch(e){fallback()}
  });
});
</script>"""
JS = JS.replace("</script>", LB_JS + "</script>")


def T(x, lang):
    if isinstance(x, dict):
        return x[lang]
    return x


# ----------------------------------------------------------------- paths
def page_path(lang, kind, slug=None):
    base = "" if lang == "en" else "bs/"
    if kind == "home":
        return base + "index.html"
    if kind == "devlog":
        return base + "devlog.html"
    if kind == "contact":
        return base + "contact.html"
    if kind == "about":
        return base + "about.html"
    if kind == "work":
        return base + "work.html"
    if kind == "earlier":
        return base + "earlier.html"
    if kind == "post":
        return base + f"devlog/{slug}.html"
    return base + f"projects/{slug}.html"


def rel(from_path, to_path):
    depth = from_path.count("/")
    return "../" * depth + to_path


# ----------------------------------------------------------------- visuals
def hex_cover(uid="h"):
    """Illustration of an ArcaneTD map: pointy hex tiles, liquid tiles and towers."""
    W, H, r = 800, 550, 38
    w = math.sqrt(3) * r
    hydro = {(4, 3), (5, 3), (4, 4), (3, 5)}
    vulcan = {(10, 6), (11, 6), (10, 7), (11, 5)}
    path = {(c, 8) for c in range(0, 14)} | {(1, r_) for r_ in range(0, 9)}
    towers = {(5, 4): "hydro", (6, 3): "hydro", (9, 6): "vulcan", (10, 5): "vulcan", (7, 7): "base"}
    out = [f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">']
    out.append('<defs><radialGradient id="glow" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#1b3a40"/><stop offset="1" stop-color="#0d171c"/></radialGradient></defs>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#glow)"/>')
    for row in range(0, 11):
        for col in range(-1, 14):
            cx = col * w + (w / 2 if row % 2 else 0) + 10
            cy = row * r * 1.5 + 10
            pts = " ".join(f"{cx + r * 0.94 * math.cos(math.radians(60 * k - 30)):.1f},{cy + r * 0.94 * math.sin(math.radians(60 * k - 30)):.1f}" for k in range(6))
            key = (col, row)
            if key in hydro:
                fill, stroke = "#14707d", "#5fd6e6"
            elif key in vulcan:
                fill, stroke = "#7a2410", "#f2814a"
            elif key in path:
                fill, stroke = "#22323a", "#2d434c"
            else:
                fill, stroke = "#16252c", "#223841"
            out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            if key in towers:
                k = towers[key]
                c = {"hydro": "#7fe7f2", "vulcan": "#ffa26e", "base": "#f2d27a"}[k]
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="13" fill="#0d171c" stroke="{c}" stroke-width="3"/>')
                out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{c}"/>')
    out.append("</svg>")
    return "".join(out)


def cover(p, prefix, lang, big=False):
    cls = "feat-v" + (" p-cover" if big else "")
    art = p.get("cover_image")
    if art and os.path.exists(os.path.join(ROOT, art)):
        a = prefix + "assets/ramo/"
        alt = T(C.t(f"{p['name']} cover art", f"{p['name']}, naslovna slika"), lang)
        return (f'<div class="{cls} cv-art"><img class="art" src="{prefix}{art}" alt="{E(alt)}">'
                f'</div>')
    if p["theme"] == "ramo":
        a = prefix + "assets/ramo/"
        alt = T(C.t("Ramo, two enemies and the boss, as pixel art sprites from the game",
                    "Ramo, dva neprijatelja i boss, kao pixel art likovi iz igre"), lang)
        return (f'<div class="{cls} cv-ramo" role="img" aria-label="{E(alt)}">'
                f'<img class="logo" src="{a}logo.png" alt="" width="400" height="363">'
                f'<span class="tt">VHT TELETEKST<br>Ramo ep1 ... 131<br>Ramo ep5 ... 698</span>'
                f'<img src="{a}enemy-1.png" alt="" width="184" height="420" style="width:15%">'
                f'<img src="{a}ramo-pistol.png" alt="" width="315" height="480" style="width:26%">'
                f'<img src="{a}boss.png" alt="" width="275" height="360" style="width:21%">'
                f'<img src="{a}enemy-2.png" alt="" width="184" height="420" style="width:15%">'
                f'</div>')
    if p.get("cover_photo"):
        alt = T(C.t(f"{p['name']} home page", f"{p['name']}, početna stranica"), lang)
        return (f'<div class="{cls}" style="background:#0b0b0b"><img src="{prefix}{p["cover_photo"]}" alt="{E(alt)}" '
                f'style="width:100%;height:100%;object-fit:cover;object-position:center;display:block"></div>')
    if p["theme"] == "vinyl":
        grooves = "".join(f'<circle cx="300" cy="200" r="{r}" fill="none" stroke="#2c2c2c" stroke-width="1.2"/>' for r in range(70, 168, 9))
        svg = (f'<svg viewBox="0 0 600 400" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%;display:block" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
               f'<rect width="600" height="400" fill="#E9E4DA"/>'
               f'<rect x="60" y="40" width="320" height="320" fill="#0B7268"/>'
               f'<circle cx="300" cy="200" r="170" fill="#141414"/>{grooves}'
               f'<circle cx="300" cy="200" r="54" fill="#E0A43A"/><circle cx="300" cy="200" r="6" fill="#E9E4DA"/>'
               f'</svg>')
        alt = T(C.t("Illustration of a vinyl record sliding out of its sleeve", "Ilustracija ploče koja izlazi iz omota"), lang)
        return f'<div class="{cls}" role="img" aria-label="{E(alt)}" style="background:#E9E4DA">{svg}</div>'
    if p["theme"] == "arcane":
        alt = T(C.t("Illustration of an ArcaneTD hex map with water and magma tiles and towers next to them",
                    "Ilustracija ArcaneTD mape s poljima vode i magme i tornjevima pored njih"), lang)
        return f'<div class="{cls} cv-arcane" role="img" aria-label="{E(alt)}">{hex_cover()}</div>'
    return (f'<div class="{cls} cv-ph"><div><b>{E(p["name"])}</b>'
            f'{E(T(C.t("Key art coming soon", "Vizual uskoro"), lang))}</div></div>')


def sprite_strip(p, prefix):
    """Small in-game sprites placed along the page as background detail (Ramo only)."""
    if p["theme"] != "ramo":
        return ""
    a = prefix + "assets/ramo/"
    return (f'<div class="wrap strip" aria-hidden="true">'
            f'<img src="{a}tram.png" alt="" style="height:64px">'
            f'<img src="{a}enemy-2.png" alt="" style="height:58px">'
            f'<img src="{a}hazard-box.png" alt="" style="height:30px">'
            f'<img src="{a}ramo-idle.png" alt="" style="height:58px">'
            f'<img src="{a}burek.png" alt="" style="height:26px"></div>')


# ----------------------------------------------------------------- frame
HEX_MARK = '<svg class="mark-hex" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1.5 21.1 6.75v10.5L12 22.5 2.9 17.25V6.75z"/></svg>'


def header(lang, path, active):
    other = "bs" if lang == "en" else "en"
    # counterpart path
    other_path = path[3:] if lang == "bs" else "bs/" + path
    home = rel(path, page_path(lang, "home"))
    links = [
        (home, T(C.t("Home", "Početna"), lang), "home"),
        (rel(path, page_path(lang, "work")), T(C.UI["nav_work"], lang), "work"),
        (rel(path, page_path(lang, "devlog")), T(C.UI["nav_devlog"], lang), "devlog"),
        (rel(path, page_path(lang, "about")), T(C.t("About me", "O meni"), lang), "about"),
        (rel(path, page_path(lang, "contact")), T(C.UI["nav_contact"], lang), "contact"),
    ]
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k == active else ""}>{E(x)}</a>' for h, x, k in links)
    nav += (f'<a class="lang" href="{rel(path, other_path)}" hreflang="{other}" lang="{other}" '
            f'title="{E(T(C.UI["lang_other_label"], lang))}">{T(C.UI["lang_other"], lang)}</a>')
    return (f'<a class="skip" href="#main">{E(T(C.UI["skip"], lang))}</a>'
            f'<header class="top"><div class="wrap"><a class="mark" href="{home}">{HEX_MARK}{E(C.PERSON["name"])}</a>'
            f'<nav class="nav" aria-label="Main">{nav}</nav></div></header>')


def footer(lang):
    return (f'<footer><div class="wrap"><span>{E(C.PERSON["name"])}, 2026 · <a href="mailto:{C.PERSON["email"]}">{E(C.PERSON["email"])}</a></span>'
            f'<span>{E(T(C.UI["footer_note"], lang))}</span></div></footer>')


def document(lang, path, title, desc, body, fragment=False):
    other_path = path[3:] if lang == "bs" else "bs/" + path
    head = (f'<title>{E(title)}</title>'
            f'<meta name="description" content="{E(desc)}">'
            f'<link rel="alternate" hreflang="{lang}" href="{os.path.basename(path)}">'
            f'<link rel="alternate" hreflang="{"bs" if lang == "en" else "en"}" href="{rel(path, other_path)}">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com">'
            f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link rel="stylesheet" href="{FONTS}">'
            f'<style>{CSS}</style>')
    if fragment:
        return (f'<title>{E(title)}</title><meta name="claude:viewport-fit-sides" content="cover">' + head[len(f"<title>{E(title)}</title>"):]
                + f'<div class="site" lang="{lang}">{body}</div>{JS}')
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">{head}</head>'
            f'<body><div class="site">{body}</div>{JS}</body></html>')


# ----------------------------------------------------------------- home
def project_feature(p, lang, path):
    href = rel(path, page_path(lang, "project", p["slug"]))
    prefix = rel(path, "")
    facts = "".join(f"<li>{E(T(f, lang))}</li>" for f in p["facts"])
    tags = "".join(f"<span>{E(T(x, lang))}</span>" for x in p["tags"])
    return (f'<article class="feat"><a class="feat-link" href="{href}" tabindex="-1" aria-hidden="true">{cover(p, prefix, lang)}</a>'
            f'<div class="feat-t"><span class="status {p["status_kind"]}">{E(T(p["status"], lang))}</span>'
            f'<h3><a href="{href}">{E(p["name"])}</a></h3>'
            f'<p class="hook">{fmt_todo(T(p["hook"], lang))}</p><p class="sum">{fmt_todo(T(p["summary"], lang))}</p>'
            f'<ul class="facts">{facts}</ul><div class="tags">{tags}</div>'
            f'<a class="more" href="{href}">{E(T(C.UI["read_case"], lang))}</a></div></article>')


def project_compact(p, lang, path):
    href = rel(path, page_path(lang, "project", p["slug"]))
    prefix = rel(path, "")
    tags = "".join(f"<span>{E(T(x, lang))}</span>" for x in p["tags"])
    return (f'<article class="compact"><a class="feat-link" href="{href}" tabindex="-1" aria-hidden="true">{cover(p, prefix, lang)}</a>'
            f'<div class="feat-t"><span class="status {p["status_kind"]}">{E(T(p["status"], lang))}</span>'
            f'<h3><a href="{href}">{E(p["name"])}</a></h3><p class="sum">{fmt_todo(T(p["hook"], lang))}</p>'
            f'<div class="tags">{tags}</div><a class="more" href="{href}">{E(T(C.UI["read_case"], lang))}</a></div></article>')


def sec(id_, h, intro, inner, wide=False):
    ip = f"<p>{E(intro)}</p>" if intro else ""
    return (f'<section class="sec{" wide" if wide else ""}" id="{id_}" aria-labelledby="{id_}-h"><div class="wrap">'
            f'<div class="sec-h"><h2 id="{id_}-h">{E(h)}</h2>{ip}</div><div class="stack">{inner}</div></div></section>')


def post_rows(posts, lang, path, show_project=True):
    out = []
    for d in posts:
        tag = ""
        if show_project and d["project"]:
            pr = next(p for p in C.PROJECTS if p["slug"] == d["project"])
            tag = f'<a class="ptag" href="{rel(path, page_path(lang, "project", pr["slug"]))}">{E(pr["name"])}</a>'
        dev = rel(path, page_path(lang, "devlog"))
        if d.get("long"):
            href = rel(path, page_path(lang, "post", d["slug"]))
            num = f'#{d["num"]} ' if d.get("num") else ""
            pidx = next((i for i, p in enumerate(C.PROJECTS) if p["slug"] == d["project"]), 99)
            out.append(f'<article class="post" id="{d["slug"]}" data-project="{d["project"] or ""}" data-date="{d["date"]}" data-num="{d.get("num") or 0}" data-porder="{pidx}"><time datetime="{d["date"]}">{fmt_date(d["date"], lang)}</time>'
                       f'<div><h3><a href="{href}" style="text-decoration:none">{E(num)}{E(T(d["title"], lang))}</a>{tag}</h3>'
                       f'<p>{fmt_todo(T(d["body"], lang))}</p><a class="more" href="{href}">{E(T(C.t("Read the post", "Pročitaj tekst"), lang))}</a></div></article>')
            continue
        out.append(f'<article class="post" id="{d["slug"]}"><time datetime="{d["date"]}">{fmt_date(d["date"], lang)}</time>'
                   f'<div><h3><a href="{dev}#{d["slug"]}" style="text-decoration:none">{E(T(d["title"], lang))}</a>{tag}</h3>'
                   f'<p>{fmt_todo(T(d["body"], lang))}</p></div></article>')
    return '<div class="posts">' + "".join(out) + "</div>"


MONTHS = {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          "bs": ["jan.", "feb.", "mar.", "apr.", "maj", "jun.", "jul.", "avg.", "sep.", "okt.", "nov.", "dec."]}


def fmt_date(iso, lang):
    y, m, d = iso.split("-")
    if lang == "en":
        return f"{int(d)} {MONTHS['en'][int(m) - 1]} {y}"
    return f"{int(d)}. {MONTHS['bs'][int(m) - 1]} {y}."


def fmt_todo(s):
    """Escape text and highlight [bracketed] notes that still need content."""
    out, buf, i = [], "", 0
    import re
    parts = re.split(r"(\[[^\]]+\])", s)
    for part in parts:
        if part.startswith("[") and part.endswith("]"):
            out.append(f'<span class="todo">{E(part)}</span>')
        else:
            out.append(E(part))
    return "".join(out)


def build_home(lang):
    path = page_path(lang, "home")
    H, U, P = C.HOME, C.UI, C.PERSON
    cv = rel(path, P["cv"])
    brief = "".join(f"<div><dt>{E(T(k, lang))}</dt><dd>{E(T(v, lang))}</dd></div>" for k, v in H["brief"])
    hero = (f'<section class="hero"><div class="wrap"><div><h1>{E(T(H["hero_h1"], lang))}</h1>'
            f'<p class="lede">{E(T(H["hero_p"], lang))}</p>'
            f'<div class="btns"><a class="btn primary" href="#work">{E(T(C.HOME["work_h"], lang))}</a>'
            f'<a class="btn" href="{cv}">{E(T(U["download_cv"], lang))} <small>PDF</small></a>'
            f'<a class="btn" href="{rel(path, P["letter"])}">{E(T(U["letter"], lang))} <small>PDF</small></a></div></div>'
            f'<aside class="brief" aria-labelledby="brief-h"><h2 id="brief-h">{E(T(H["brief_title"], lang))}</h2><dl>{brief}</dl></aside>'
            f'</div></section>')
    proof = "".join(f"<li><b>{E(T(n, lang))}</b><span>{E(T(s, lang))}</span></li>" for n, s in H["proof"])
    proof = f'<section class="proof" aria-label="Highlights"><div class="wrap"><ul>{proof}</ul></div></section>'

    feats = "".join(project_feature(p, lang, path) for p in C.PROJECTS if p.get("featured", True))
    minor = [p for p in C.PROJECTS if not p.get("featured", True)]
    if minor:
        mh = T(C.t("Also worth a look", "Vrijedi pogledati"), lang)
        feats += f'<div><h3 style="font-size:var(--step-1);margin-bottom:16px">{E(mh)}</h3>' + "".join(project_compact(p, lang, path) for p in minor) + "</div>"
    ep = rel(path, page_path(lang, "earlier"))
    ep = rel(path, page_path(lang, "earlier"))
    others = "".join(f'<a class="ecard" href="{rel(path, e_item_path(lang, e["slug"]))}">{e_thumb(e, lang, rel(path, ""))}<span class="lang-tag">{E(T(e["kind"], lang))}</span>'
                     f'<h4>{E(e["name"])}</h4><p>{E(T(e["summary"], lang))}</p></a>' for e in EARLIER)
    others = f'<div class="egrid">{others}</div>'
    work = sec("work", T(H["work_h"], lang), T(H["work_intro"], lang),
               feats + f'<div><h3 style="font-size:var(--step-1);margin-bottom:16px">{E(T(H["more_h"], lang))}</h3>{others}</div>', wide=True)

    posts = sorted(C.DEVLOG, key=lambda d: (d["date"], d.get("num") or 0), reverse=True)[:3]
    now = sec("now", T(H["now_h"], lang), T(H["now_p"], lang),
              post_rows(posts, lang, path) + f'<a class="more" href="{rel(path, page_path(lang, "devlog"))}">{E(T(U["all_posts"], lang))}</a>')

    body = header(lang, path, "home") + f'<main id="main">{hero}{proof}{work}{now}</main>' + footer(lang)
    return path, T(H["title"], lang), T(H["description"], lang), body


# ----------------------------------------------------------------- project
def build_project(p, lang, idx):
    path = page_path(lang, "project", p["slug"])
    prefix = rel(path, "")
    U = C.UI
    meta = [(U["status"], p["status"]), (U["role"], p["role"]), (U["timeline"], p["timeline"]), (U["platforms"], p["platforms"])]
    meta_html = "".join(f"<div><dt>{E(T(k, lang))}</dt><dd>{fmt_todo(T(v, lang))}</dd></div>" for k, v in meta)
    links = "".join(f'<a class="btn{" primary" if i == 0 else ""}" href="{u}">{E(T(n, lang))}</a>' for i, (n, u) in enumerate(p["links"]))
    head = (f'<section class="p-head"><div class="wrap"><p class="crumb"><a href="{rel(path, page_path(lang, "home"))}#work">{E(T(U["back_home"], lang))}</a></p>'
            f'<h1>{E(p["name"])}</h1><p class="hook">{fmt_todo(T(p["hook"], lang))}</p>'
            f'<dl class="meta">{meta_html}</dl>'
            + (f'<div class="btns">{links}</div>' if links else "")
            + f'</div><div class="wrap">{cover(p, prefix, lang, big=True)}</div></section>')

    blocks = []
    lbl = lambda en, bs: en if lang == "en" else bs
    if p.get("wip"):
        blocks.append(f'<div class="wip" role="note"><b>{lbl("Work in progress", "U izradi")}</b><p>{E(T(p["wip"], lang))}</p></div>')
    blocks.append(f'<section class="blk"><h2>{lbl("The idea", "Ideja")}</h2><div class="prose"><p>{fmt_todo(T(p["idea"], lang))}</p>'
                  f'<p>{fmt_todo(T(p["summary"], lang))}</p></div></section>')
    if p.get("lore"):
        lp = "".join(f"<p>{fmt_todo(T(x, lang))}</p>" for x in p["lore"])
        blocks.append(f'<section class="blk"><h2>{lbl("The world", "Svijet igre")}</h2><div class="prose">{lp}</div></section>')
    if p["numbers"]:
        nums = "".join(f"<li><b>{E(n)}</b><span>{E(T(s, lang))}</span></li>" for n, s in p["numbers"])
        blocks.append(f'<section class="blk"><h2>{lbl("In numbers", "U brojkama")}</h2><ul class="nums">{nums}</ul></section>')
    er_fig = ""
    if p.get("er_image"):
        er = p["er_image"]
        er_fig = (f'<figure><h3>{E(T(er["title"], lang))}</h3>'
                  f'<div class="dg-box" style="background:#111;text-align:center"><img src="{prefix}{er["src"]}" alt="{E(T(er["title"], lang))}" style="max-width:min(100%,760px);display:inline-block"></div>'
                  f'<figcaption>{E(T(er["caption"], lang))}</figcaption></figure>')
        if not p["diagrams"]:
            blocks.append(f'<section class="blk wide"><h2>{lbl("How it works", "Kako radi")}</h2><div class="figs">{er_fig}</div></section>')
    if p["diagrams"]:
        figs = []
        for key in p["diagrams"]:
            fn, (hen, hbs), (cen, cbs) = DIAGRAMS[key]
            figs.append(f'<figure><h3>{E(hen if lang == "en" else hbs)}</h3><div class="dg-box">{fn(lang)}</div>'
                        f'<figcaption>{E(cen if lang == "en" else cbs)}</figcaption></figure>')
        blocks.append(f'<section class="blk wide"><h2>{lbl("How it works", "Kako radi")}</h2><div class="figs">{"".join(figs)}{er_fig}</div></section>')
    built = "".join(f"<li>{fmt_todo(T(b, lang))}</li>" for b in p["built"])
    blocks.append(f'<section class="blk"><h2>{lbl("What I built", "Šta sam napravio")}</h2><div><ul class="built">{built}</ul>'
                  f'<p style="margin-top:16px;color:var(--muted)">{E(T(U["stack"], lang))}: {fmt_todo(p["stack"])}</p></div></section>')
    code = ""
    if not p.get("highlight"):
        pass
    elif p["code"]:
        code = (f'<div style="display:grid;gap:10px;margin-top:8px"><span class="code-h">{E(p["code"]["file"])}</span>'
                f'<pre><code>{E(p["code"]["body"])}</code></pre><p style="color:var(--muted);font-size:.95rem">{E(T(p["code"]["note"], lang))}</p></div>')
    if p.get("highlight"):
        blocks.append(f'<section class="blk"><h2>{E(T(p["highlight_h"], lang))}</h2><div class="prose"><p>{fmt_todo(T(p["highlight"], lang))}</p>{code}</div></section>')

    if p.get("cloud"):
        cl = p["cloud"]
        fn, (hen, hbs), (cen, cbs) = DIAGRAMS["vinyl_cloud"]
        dg = (f'<figure><div class="dg-box">{fn(lang)}</div><figcaption>{E(cen if lang == "en" else cbs)}</figcaption></figure>')
        steps = "".join(f"<li>{fmt_todo(T(x, lang))}</li>" for x in cl["steps"])
        issues = "".join(f"<li>{fmt_todo(T(x, lang))}</li>" for x in cl["issues"])
        figs = "".join(f'<figure><img src="{prefix}{f["src"]}" alt="{E(T(f["alt"], lang))}" loading="lazy"><figcaption>{E(T(f["caption"], lang))}</figcaption></figure>' for f in cl["figs"])
        blocks.append(f'<section class="blk wide" id="cloud"><h2>{E(T(cl["h"], lang))}</h2><div class="stack" style="gap:28px">'
                      f'<div class="prose"><p>{fmt_todo(T(cl["intro"], lang))}</p></div>{dg}'
                      f'<div class="prose"><h3>{E(T(cl["steps_h"], lang))}</h3><ol class="built">{steps}</ol>'
                      f'<h3>{E(T(cl["issues_h"], lang))}</h3><ul class="built">{issues}</ul>'
                      f'<h3>{E(T(cl["prod_h"], lang))}</h3><p>{fmt_todo(T(cl["prod"], lang))}</p></div>'
                      f'<div class="gallery">{figs}</div></div></section>')

    media = []
    for m in p["media"]:
        if "video" in m:
            media.append(f'<figure><video controls muted loop playsinline preload="metadata" poster="{prefix}{m["poster"]}" aria-label="{E(T(m["alt"], lang))}" style="width:100%;border-radius:var(--r-lg);background:#000"><source src="{prefix}{m["video"]}" type="video/mp4"></video><figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')
        elif "placeholder" in m:
            media.append(f'<div class="ph"><b>{E(T(U["placeholder"], lang))}</b><span>{E(T(m["placeholder"], lang))}</span></div>')
        else:
            media.append(f'<figure><img src="{prefix}{m["src"]}" alt="{E(T(m["alt"], lang))}" loading="lazy"{" style=\"image-rendering:pixelated\"" if m.get("pixel") else ""}><figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')
    vids = ""
    for vid, vt in p.get("videos", []):
        url = f"https://www.youtube.com/watch?v={vid}"
        if ARTIFACT:
            vids += (f'<a class="vcard" href="{url}"><span class="vplay" aria-hidden="true"></span>'
                     f'<span><b>{E(T(vt, lang))}</b><br>{lbl("Watch on YouTube", "Pogledaj na YouTubeu")}</span></a>')
        else:
            vids += (f'<figure><div class="vframe"><iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{E(T(vt, lang))}" '
                     f'loading="lazy" allow="encrypted-media; picture-in-picture" allowfullscreen></iframe></div>'
                     f'<figcaption>{E(T(vt, lang))}</figcaption></figure>')
    vids = f'<div class="gallery" style="margin-bottom:20px">{vids}</div>' if vids else ""
    blocks.append(f'<section class="blk"><h2>{lbl("Screenshots and video", "Slike i video")}</h2><div>{vids}<div class="gallery">{"".join(media)}</div></div></section>')

    posts = sorted([d for d in C.DEVLOG if d["project"] == p["slug"]], key=lambda d: (d.get("num") or 0, d["date"]))
    plist = post_rows(posts, lang, path, show_project=False) if posts else f'<p style="color:var(--muted)">{E(T(U["no_posts"], lang))}</p>'
    blocks.append(f'<section class="blk"><h2>{E(T(U["devlog_for"], lang))}</h2><div class="stack" style="gap:20px">{plist}'
                  f'<a class="more" href="{rel(path, page_path(lang, "devlog"))}#{p["slug"]}">{E(T(C.t("All posts about " + p["name"], "Svi tekstovi o projektu " + p["name"]), lang))}</a></div></section>')

    nxt = C.PROJECTS[(idx + 1) % len(C.PROJECTS)]
    blocks.append(f'<nav class="pnext" aria-label="Projects"><a href="{rel(path, page_path(lang, "home"))}#work"><span>{E(T(U["back_home"], lang))}</span>{lbl("Home", "Početna")}</a>'
                  f'<a href="{rel(path, page_path(lang, "project", nxt["slug"]))}" style="text-align:right"><span>{E(T(U["next_project"], lang))}</span>{E(nxt["name"])}</a></nav>')

    body = (header(lang, path, "work") + f'<main id="main">{head}<div class="wrap p-body">{"".join(blocks)}</div></main>' + footer(lang))
    title = f'{p["name"]}, {T(C.UI["read_case"], lang).lower()}' if False else f'{p["name"]} | Harun Kestendžić'
    return path, title, T(p["summary"], lang), body


def md_inline(s):
    import re
    s = E(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*]+)\*(?![*\w])", r"<em>\1</em>", s)
    return s


def md_render(md):
    out, lines, i = [], md.strip("\n").split("\n"), 0
    para, items = [], []

    def flush():
        nonlocal para, items
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para = []
        if items:
            out.append("<ul>" + "".join(f"<li>{md_inline(x)}</li>" for x in items) + "</ul>")
            items = []
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            flush()
            i += 1
            code = []
            while not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(f"<pre><code>{E(chr(10).join(code))}</code></pre>")
        elif ln.startswith("[") and ln.rstrip().endswith("]"):
            flush()
            out.append(f'<figure class="shot"><span>{fmt_todo(ln.strip())}</span></figure>')
        elif ln.startswith("## "):
            flush()
            out.append(f"<h2>{md_inline(ln[3:])}</h2>")
        elif ln.startswith("- "):
            if para:
                flush()
            items.append(ln[2:])
        elif not ln.strip():
            flush()
        else:
            if items:
                flush()
            para.append(ln.strip())
        i += 1
    flush()
    return "".join(out)


def build_post(d, lang):
    path = page_path(lang, "post", d["slug"])
    pr = next(p for p in C.PROJECTS if p["slug"] == d["project"])
    dev = rel(path, page_path(lang, "devlog"))
    prj = rel(path, page_path(lang, "project", pr["slug"]))
    num = f'Devlog #{d["num"]} · ' if d.get("num") else ""
    series = sorted([x for x in C.DEVLOG if x.get("long") and x["project"] == d["project"]], key=lambda x: x["num"])
    i = series.index(d)
    nav = f'<a href="{dev}"><span>{E(T(C.t("All posts", "Svi tekstovi"), lang))}</span>Devlog</a>'
    if i + 1 < len(series):
        nx = series[i + 1]
        nav += (f'<a href="{rel(path, page_path(lang, "post", nx["slug"]))}" style="text-align:right">'
                f'<span>{E(T(C.t("Next", "Sljedeći"), lang))} · #{nx["num"]}</span>{E(T(nx["title"], lang))}</a>')
    head = (f'<section class="p-head"><div class="wrap"><p class="kicker">{E(num)}{fmt_date(d["date"], lang)} · '
            f'<a href="{prj}">{E(pr["name"])}</a></p><h1 style="font-size:clamp(1.9rem,4.2vw,3rem);max-width:22ch">{E(T(d["title"], lang))}</h1>'
            f'<p class="hook">{E(T(d["body"], lang))}</p></div></section>')
    body = (header(lang, path, "devlog") + f'<main id="main">{head}<div class="wrap p-body"><div class="prose">{md_render(T(d["text"], lang))}</div>'
            f'<nav class="pnext" aria-label="Devlog">{nav}</nav></div></main>'
            + footer(lang))
    return path, f'{T(d["title"], lang)} | Harun Kestendžić', T(d["body"], lang), body


def build_devlog(lang):
    path = page_path(lang, "devlog")
    pidx = {p["slug"]: i for i, p in enumerate(C.PROJECTS)}
    posts = sorted(C.DEVLOG, key=lambda d: (d["date"], -pidx.get(d["project"], 99), d.get("num") or 0), reverse=True)
    intro = T(C.t("How I built things, what broke, and what I'd change. Each post is about one system.",
                  "Kako sam pravio stvari, šta se pokvarilo i šta bih promijenio. Svaki tekst je o jednom sistemu."), lang)
    L = lambda en, bs: E(T(C.t(en, bs), lang))
    chips = f'<button type="button" class="chip" data-filter="" aria-pressed="true">{L("All", "Sve")} <span>{len(posts)}</span></button>'
    for pr in C.PROJECTS:
        n = sum(1 for d in posts if d["project"] == pr["slug"])
        if n:
            chips += f'<button type="button" class="chip" data-filter="{pr["slug"]}" aria-pressed="false">{E(pr["name"])} <span>{n}</span></button>'
    controls = (f'<div class="dl-controls" hidden><div class="chips" role="group" aria-label="{L("Filter by project", "Filtriraj po projektu")}">{chips}</div>'
                f'<label class="dl-sort">{L("Sort", "Poredaj")} <select>'
                f'<option value="new">{L("Newest first", "Najnovije prvo")}</option>'
                f'<option value="old">{L("Oldest first", "Najstarije prvo")}</option>'
                f'<option value="series">{L("By project, in series order", "Po projektu, redom serije")}</option>'
                f'</select></label></div><p class="dl-count" aria-live="polite"></p>')
    script = """<script>
(function(){
  var root=document.currentScript.parentNode, list=root.querySelector('.posts'), ctl=root.querySelector('.dl-controls');
  if(!list||!ctl)return; ctl.hidden=false;
  var rows=[].slice.call(list.querySelectorAll('.post')), chips=[].slice.call(ctl.querySelectorAll('.chip')),
      sel=ctl.querySelector('select'), count=root.querySelector('.dl-count'), slugs=chips.map(function(c){return c.dataset.filter});
  var st={f:'',s:'new'};
  try{var sv=JSON.parse(localStorage.getItem('devlogView')||'{}'); if(slugs.indexOf(sv.f)>=0)st.f=sv.f; if(sv.s)st.s=sv.s;}catch(e){}
  function fromHash(){var h=(location.hash||'').slice(1).split('.').pop(); if(h&&slugs.indexOf(h)>=0){st.f=h; if(!st.locked)st.s='series';}}
  function cmp(a,b){var A=a.dataset,B=b.dataset;
    if(st.s==='series'){return (A.porder-B.porder)||(A.num-B.num)||(A.date<B.date?-1:1);}
    var d=A.date<B.date?-1:A.date>B.date?1:0; if(st.s==='new')d=-d;
    return d||((A.porder-B.porder))||(st.s==='new'?B.num-A.num:A.num-B.num);}
  function render(){
    rows.sort(cmp).forEach(function(r){list.appendChild(r); r.hidden=!!st.f&&r.dataset.project!==st.f;});
    chips.forEach(function(c){c.setAttribute('aria-pressed',String(c.dataset.filter===st.f));});
    sel.value=st.s; var n=rows.filter(function(r){return !r.hidden}).length;
    count.textContent=n+' """ + T(C.t("posts", "tekstova"), lang) + """';
    try{localStorage.setItem('devlogView',JSON.stringify(st));}catch(e){}
  }
  chips.forEach(function(c){c.addEventListener('click',function(){st.f=c.dataset.filter; render();});});
  sel.addEventListener('change',function(){st.s=sel.value; render();});
  window.addEventListener('hashchange',function(){fromHash(); render();});
  fromHash(); render();
})();
</script>"""
    body = (header(lang, path, "devlog") +
            f'<main id="main"><section class="p-head"><div class="wrap"><h1>Devlog</h1><p class="hook">{E(intro)}</p></div></section>'
            f'<div class="wrap">{controls}{post_rows(posts, lang, path)}{script}</div></main>' + footer(lang))
    return path, "Devlog | Harun Kestendžić", intro, body


def e_thumb(e, lang, prefix=""):
    if e.get("thumb") and os.path.exists(os.path.join(ROOT, e["thumb"])):
        alt = T(e.get("thumb_alt", C.t(e["name"], e["name"])), lang)
        return f'<span class="ethumb has-img"><img src="{prefix}{e["thumb"]}" alt="{E(alt)}" loading="lazy"></span>'
    lab = T(C.t("Image: " + e["name"], "Slika: " + e["name"]), lang)
    return f'<span class="ethumb" role="img" aria-label="{E(lab)}"><b>{E(T(C.UI["placeholder"], lang))}</b><span>{E(e["name"])}</span></span>'


def e_item_path(lang, slug):
    return ("" if lang == "en" else "bs/") + f"earlier/{slug}.html"


def build_earlier(lang):
    path = page_path(lang, "earlier")
    intro = T(C.t("Smaller and older projects: coursework, learning projects and early experiments. Each has its own short page.",
                  "Manji i stariji projekti: zadaci s fakulteta, projekti za učenje i rani eksperimenti. Svaki ima svoju kratku stranicu."), lang)
    head = (f'<section class="p-head"><div class="wrap"><p class="crumb"><a href="{rel(path, page_path(lang, "home"))}#work">{E(T(C.UI["back_home"], lang))}</a></p>'
            f'<h1 style="font-size:clamp(2.4rem,7vw,5rem)">{E(T(C.t("Earlier work", "Raniji rad"), lang))}</h1><p class="hook">{E(intro)}</p></div></section>')
    cards = "".join(f'<a class="ecard" href="{rel(path, e_item_path(lang, e["slug"]))}">{e_thumb(e, lang, rel(path, ""))}'
                    f'<span class="lang-tag">{E(T(e["kind"], lang))}</span><h3>{E(e["name"])}</h3><p>{E(T(e["summary"], lang))}</p></a>' for e in EARLIER)
    body = header(lang, path, "work") + f'<main id="main">{head}<div class="wrap p-body"><div class="egrid">{cards}</div></div></main>' + footer(lang)
    return path, T(C.t("Earlier work", "Raniji rad"), lang) + " | Harun Kestendžić", intro, body


def build_earlier_item(e, i, lang):
    path = e_item_path(lang, e["slug"])
    lbl = lambda en, bs: en if lang == "en" else bs
    idx = rel(path, page_path(lang, "earlier"))
    pts = "".join(f"<li>{md_inline(T(x, lang))}</li>" for x in e["points"])
    pts = f'<ul class="built">{pts}</ul>' if pts else f'<p style="color:var(--muted)">{fmt_todo(T(C.t("[More details to add.]", "[Dodati više detalja.]"), lang))}</p>'
    nxt = f'<p style="margin-top:14px"><b style="color:var(--ink)">{lbl("What I would change", "Šta bih promijenio")}:</b> {E(T(e["next"], lang))}</p>' if e.get("next") else ""
    note = f'<p style="margin-top:14px;color:var(--muted)">{fmt_todo(T(e["note"], lang))}</p>' if e.get("note") else ""
    stack = f'<p style="margin-top:14px;color:var(--muted)">{E(T(C.UI["stack"], lang))}: {E(e["stack"])}</p>' if e["stack"] else ""
    lk = ""
    for n, u in e["links"]:
        if not u.startswith("http"):
            u = rel(path, ("" if lang == "en" else "bs/") + u)
        lk += f'<a class="btn" href="{u}">{E(T(n, lang))}</a> '
    lk = f'<div class="btns" style="margin-top:18px">{lk}</div>' if lk else ""
    head = (f'<section class="p-head"><div class="wrap"><p class="crumb"><a href="{idx}">{E(T(C.t("Back to earlier work", "Nazad na raniji rad"), lang))}</a></p>'
            f'<h1 style="font-size:clamp(2.2rem,6vw,4.5rem)">{E(e["name"])}</h1><p class="hook">{E(T(e["summary"], lang))}</p>'
            f'<p class="lang-tag" style="color:var(--accent);font-weight:600">{E(T(e["kind"], lang))}</p></div>'
            f'<div class="wrap">{e_thumb(e, lang, rel(path, ""))}</div></section>')
    pre = rel(path, "")
    em = []
    for m in e.get("media", []):
        if "video" in m:
            em.append(f'<figure><video controls muted loop playsinline preload="metadata" poster="{pre}{m["poster"]}" aria-label="{E(T(m["alt"], lang))}" style="width:100%;border-radius:var(--r-lg);background:#000"><source src="{pre}{m["video"]}" type="video/mp4"></video><figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')
        else:
            em.append(f'<figure{" style=\"grid-column:1/-1\"" if m.get("wide") else ""}><img src="{pre}{m["src"]}" alt="{E(T(m["alt"], lang))}" loading="lazy"><figcaption>{E(T(m["caption"], lang))}</figcaption></figure>')
    gal = (f'<section class="blk"><h2>{lbl("Screenshots and video", "Slike i video")}</h2><div><div class="gallery">{"".join(em)}</div></div></section>') if em else ""
    nx = EARLIER[(i + 1) % len(EARLIER)]
    nav = (f'<nav class="pnext" aria-label="Earlier work"><a href="{idx}"><span>{E(T(C.t("All earlier work", "Sav raniji rad"), lang))}</span>{lbl("Back", "Nazad")}</a>'
           f'<a href="{rel(path, e_item_path(lang, nx["slug"]))}" style="text-align:right"><span>{E(T(C.UI["next_project"], lang))}</span>{E(nx["name"])}</a></nav>')
    body = (header(lang, path, "work") + f'<main id="main">{head}<div class="wrap p-body"><section class="blk"><h2>{lbl("What I built", "Šta sam napravio")}</h2>'
            f'<div>{pts}{nxt}{stack}{note}{lk}</div></section>{gal}{nav}</div></main>' + footer(lang))
    return path, f'{e["name"]} | Harun Kestendžić', T(e["summary"], lang), body


def build_work(lang):
    path = page_path(lang, "work")
    prefix = rel(path, "")
    lbl = lambda en, bs: en if lang == "en" else bs
    items = []
    for i, p in enumerate(C.PROJECTS):
        ty, ls = META[p["slug"]]
        items.append(dict(name=p["name"], href=rel(path, page_path(lang, "project", p["slug"])), type=ty, lenses=ls, order=i,
                          kind=T(p["status"], lang), summary=T(p["hook"], lang), thumb=f'<span class="cwrap">{cover(p, prefix, lang)}</span>'))
    for j, e in enumerate(EARLIER):
        ty, ls = META[e["slug"]]
        items.append(dict(name=e["name"], href=rel(path, e_item_path(lang, e["slug"])), type=ty, lenses=ls, order=100 + j,
                          kind=T(e["kind"], lang), summary=T(e["summary"], lang), thumb=e_thumb(e, lang, prefix)))
    cards = "".join(
        f'<a class="ecard" href="{x["href"]}" data-type="{x["type"]}" data-lens="{" ".join(x["lenses"])}" data-main="{x["lenses"][0]}" data-order="{x["order"]}" data-name="{E(x["name"])}">'
        f'{x["thumb"]}<span class="lang-tag">{E(x["kind"])}</span><h3>{E(x["name"])}</h3><p>{fmt_todo(x["summary"])}</p>'
        f'<span class="etags">{E(T(TYPES[x["type"]], lang))}</span></a>' for x in items)

    def chips(group, d):
        out = f'<button type="button" class="chip" data-g="{group}" data-v="" aria-pressed="true">{lbl("All", "Sve")}</button>'
        for k, v in d.items():
            n = sum(1 for x in items if (x["type"] == k if group == "type" else k in x["lenses"]))
            if n:
                out += f'<button type="button" class="chip" data-g="{group}" data-v="{k}" aria-pressed="false">{E(T(v, lang))} <span>{n}</span></button>'
        return out
    labels = {"type": {k: T(v, lang) for k, v in TYPES.items()}, "lens": {k: T(v, lang) for k, v in LENSES.items()}}
    import json
    controls = (f'<div class="wk-controls" hidden>'
                f'<div class="wk-row"><b>{lbl("Type", "Vrsta")}</b><div class="chips" role="group" aria-label="{lbl("Filter by type", "Filtriraj po vrsti")}">{chips("type", TYPES)}</div></div>'
                f'<div class="wk-row"><b>{lbl("What it shows", "Šta pokazuje")}</b><div class="chips" role="group" aria-label="{lbl("Filter by skill", "Filtriraj po vještini")}">{chips("lens", LENSES)}</div></div>'
                f'<div class="wk-row"><label class="dl-sort">{lbl("Group by", "Grupiši po")} <select data-k="group">'
                f'<option value="">{lbl("No grouping", "Bez grupisanja")}</option><option value="type">{lbl("Type", "Vrsta")}</option>'
                f'<option value="main">{lbl("What it shows", "Šta pokazuje")}</option></select></label>'
                f'<label class="dl-sort">{lbl("Sort", "Poredaj")} <select data-k="sort"><option value="order">{lbl("Best first", "Najbolje prvo")}</option>'
                f'<option value="name">{lbl("A to Z", "A do Z")}</option></select></label></div></div>'
                f'<p class="dl-count" aria-live="polite"></p>')
    script = """<script>
(function(){
  var root=document.currentScript.parentNode, ctl=root.querySelector('.wk-controls'), list=root.querySelector('.egrid');
  if(!ctl||!list)return; ctl.hidden=false;
  var L=""" + json.dumps(labels, ensure_ascii=False) + """, word='""" + lbl("projects", "projekata") + """', none='""" + lbl("Nothing matches these filters.", "Nijedan projekat ne odgovara filterima.") + """';
  var slot=list.parentNode, cards=[].slice.call(list.children), st={type:'',lens:'',group:'',sort:'order'};
  function render(){
    var shown=cards.filter(function(c){return (!st.type||c.dataset.type===st.type)&&(!st.lens||(' '+c.dataset.lens+' ').indexOf(' '+st.lens+' ')>=0);});
    shown.sort(function(a,b){return st.sort==='name'?a.dataset.name.localeCompare(b.dataset.name):a.dataset.order-b.dataset.order;});
    var host=document.createElement('div'); host.className='wk-out';
    function grid(arr){var g=document.createElement('div'); g.className='egrid'; arr.forEach(function(c){g.appendChild(c);}); return g;}
    if(!shown.length){var p=document.createElement('p'); p.textContent=none; host.appendChild(p);}
    else if(!st.group){host.appendChild(grid(shown));}
    else{
      var keys=[]; shown.forEach(function(c){var k=st.group==='type'?c.dataset.type:c.dataset.main; if(keys.indexOf(k)<0)keys.push(k);});
      keys.forEach(function(k){var h=document.createElement('h2'); h.className='wk-h'; h.textContent=(st.group==='type'?L.type:L.lens)[k]||k; host.appendChild(h);
        host.appendChild(grid(shown.filter(function(c){return (st.group==='type'?c.dataset.type:c.dataset.main)===k;})));});
    }
    slot.innerHTML=''; slot.appendChild(host);
    ctl.querySelectorAll('.chip').forEach(function(b){b.setAttribute('aria-pressed',String(st[b.dataset.g]===b.dataset.v));});
    root.querySelector('.dl-count').textContent=shown.length+' '+word;
  }
  ctl.querySelectorAll('.chip').forEach(function(b){b.addEventListener('click',function(){st[b.dataset.g]=b.dataset.v; render();});});
  ctl.querySelectorAll('select').forEach(function(s){s.addEventListener('change',function(){st[s.dataset.k]=s.value; render();});});
  render();
})();
</script>"""
    intro = T(C.t("Everything in one place. Filter by type, or by what you want to see: game development, front end, backend, cloud, team work, data.",
                  "Sve na jednom mjestu. Filtriraj po vrsti ili po tome šta želiš vidjeti: razvoj igara, front end, backend, cloud, timski rad, podaci."), lang)
    head = (f'<section class="p-head"><div class="wrap"><p class="crumb"><a href="{rel(path, page_path(lang, "home"))}#work">{E(T(C.UI["back_home"], lang))}</a></p>'
            f'<h1 style="font-size:clamp(2.4rem,7vw,5rem)">{lbl("All work", "Sav rad")}</h1><p class="hook">{E(intro)}</p></div></section>')
    body = (header(lang, path, "work") + f'<main id="main">{head}<div class="wrap p-body"><div>{controls}<div class="wk-slot"><div class="egrid">{cards}</div></div>{script}</div></div></main>' + footer(lang))
    return path, lbl("All work", "Sav rad") + " | Harun Kestendžić", intro, body


def build_about(lang):
    path = page_path(lang, "about")
    H, U, P = C.HOME, C.UI, C.PERSON
    cv = rel(path, P["cv"])
    exp_rows = []
    for x in C.EXPERIENCE:
        org = f' <span>at {E(x["org"])}</span>' if (x["org"] and lang == "en") else (f' <span>u {E(x["org"])}</span>' if x["org"] else "")
        pts = "".join(f"<li>{E(T(pt, lang))}</li>" for pt in x["points"])
        q = ""
        if x["org"] == "Alchemy Studio":
            q = (f'<blockquote class="quote"><p>{E(T(C.UI["letter_quote"], lang))}</p>'
                 f'<span class="qby">{E(T(C.UI["letter_by"], lang))}</span>'
                 f'<a class="more" href="{rel(path, C.PERSON["letter"])}">{E(T(C.UI["letter_long"], lang))} (PDF)</a></blockquote>')
        exp_rows.append(f'<div class="row"><div class="when">{E(T(x["dates"], lang))}</div>'
                        f'<div><h3>{E(T(x["role"], lang))}{org}</h3><ul>{pts}</ul>{q}</div></div>')
    exp = sec("experience", T(H["exp_h"], lang), None, '<div class="rows">' + "".join(exp_rows) + "</div>")

    sk = "".join(f'<div class="skill"><b>{E(T(n, lang))}{f"<em>{E(T(lv, lang))}</em>" if lv else ""}</b><span>{E(T(ev, lang))}</span></div>'
                 for n, lv, ev in C.SKILLS)
    skills = sec("skills", T(H["skills_h"], lang), T(H["skills_intro"], lang), f'<div class="skills">{sk}</div>')

    ed = "".join(f'<div class="row"><div class="when">{E(T(e["dates"], lang))}</div><div><h3>{E(T(e["school"], lang))}</h3>'
                 f'<p style="color:var(--ink);margin-top:4px">{E(T(e["what"], lang))}</p><p>{E(T(e["detail"], lang))}</p></div></div>'
                 for e in C.EDUCATION)
    edu = sec("education", T(H["edu_h"], lang), None, f'<div class="rows">{ed}</div>')

    with_img = [x for x in C.AWARDS if x.get("img")]
    no_img = [x for x in C.AWARDS if not x.get("img")]
    note = T(C.FORMER_NAME_NOTE, lang)
    cards = "".join(f'<a class="cert" href="{rel(path, x.get("link", x["img"]))}" target="_blank" rel="noopener">'
                    f'<span class="cert-img"><img src="{rel(path, x["img"])}" alt="{E(T(x["title"], lang))}" loading="lazy"></span>'
                    f'<b>{E(T(x["title"], lang))}</b><span class="csub">{E(T(x["sub"], lang))}</span>'
                    + (f'<small class="former">{E(note)}</small>' if x.get("former") else "") + '</a>' for x in with_img)
    aw = "".join(f"<li><b>{E(T(x['title'], lang))}</b><span>{E(T(x['sub'], lang))}</span></li>" for x in no_img)
    awards = sec("awards", T(H["awards_h"], lang), None,
                 f'<div><div class="certs">{cards}</div><ul class="awards" style="margin-top:28px">{aw}</ul><p class="press"><b style="color:var(--ink)">{E(T(H["press_h"], lang))}.</b> {E(T(H["press_p"], lang))}</p></div>')

    brief = "".join(f"<div><dt>{E(T(k, lang))}</dt><dd>{E(T(v, lang))}</dd></div>" for k, v in H["brief"])
    head = (f'<section class="hero"><div class="wrap"><div><h1>{E(T(C.t("About me", "O meni"), lang))}</h1>'
            f'<p class="lede">{E(T(H["hero_p"], lang))}</p>'
            f'<div class="btns"><a class="btn primary" href="{rel(path, page_path(lang, "contact"))}">{E(T(U["nav_contact"], lang))}</a>'
            f'<a class="btn" href="{cv}">{E(T(U["download_cv"], lang))} <small>PDF</small></a>'
            f'<a class="btn" href="{rel(path, P["letter"])}">{E(T(U["letter"], lang))} <small>PDF</small></a></div></div>'
            f'<aside class="brief" aria-labelledby="brief-h"><h2 id="brief-h">{E(T(H["brief_title"], lang))}</h2><dl>{brief}</dl></aside>'
            f'</div></section>')
    body = header(lang, path, "about") + f'<main id="main">{head}{exp}{skills}{edu}{awards}</main>' + footer(lang)
    return path, T(C.t("About me", "O meni"), lang) + " | Harun Kestendžić", T(H["description"], lang), body


def build_contact(lang):
    path = page_path(lang, "contact")
    H, U, P = C.HOME, C.UI, C.PERSON
    cv = rel(path, P["cv"])
    contact = sec("contact", T(H["contact_h"], lang), T(H["contact_p"], lang),
                  f'<div class="contact-card"><div class="contact-line"><a class="big" id="email-text" href="mailto:{P["email"]}">{E(P["email"])}</a>'
                  f'<button class="copy" type="button" data-copy="{P["email"]}" data-target="email-text" data-done="{E(T(U["copied"], lang))}">{E(T(U["copy"], lang))}</button></div>'
                  f'<div class="contact-meta"><span>{E(P["phone"])}</span><a href="{P["linkedin"]}">LinkedIn</a><a href="{P["github"]}">GitHub</a>'
                  f'<a href="{cv}">{E(T(U["download_cv"], lang))} (PDF)</a><a href="{rel(path, P["letter"])}">{E(T(U["letter"], lang))} (PDF)</a></div></div>')

    head = (f'<section class="p-head"><div class="wrap"><h1 style="font-size:clamp(2.4rem,7vw,5rem)">{E(T(U["nav_contact"], lang))}</h1></div></section>')
    body = header(lang, path, "contact") + f'<main id="main">{head}{contact}</main>' + footer(lang)
    return path, T(U["nav_contact"], lang) + " | Harun Kestendžić", T(H["contact_p"], lang), body


# ----------------------------------------------------------------- main
def write(path, html):
    full = os.path.join(DIST, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def main():
    artifact = "--artifact" in sys.argv
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    pages = []
    for lang in LANGS:
        pages.append((lang,) + build_home(lang))
        pages.append((lang,) + build_devlog(lang))
        pages.append((lang,) + build_about(lang))
        pages.append((lang,) + build_contact(lang))
        pages.append((lang,) + build_work(lang))
        pages.append((lang,) + build_earlier(lang))
        for i, e in enumerate(EARLIER):
            pages.append((lang,) + build_earlier_item(e, i, lang))
        for i, p in enumerate(C.PROJECTS):
            pages.append((lang,) + build_project(p, lang, i))
        for d in C.DEVLOG:
            if d.get("long"):
                pages.append((lang,) + build_post(d, lang))
    for lang, path, title, desc, body in pages:
        write(path, document(lang, path, title, desc, body))
    if artifact:
        write("_root_fragment.html", single_page(pages))
    print("built", len(pages), "pages")


def page_id(path):
    p = path[:-5]  # drop .html
    lang = "bs" if p.startswith("bs/") else "en"
    p = p[3:] if lang == "bs" else p
    return lang + "-" + p.replace("projects/", "").replace("/", "-")


def single_page(pages):
    """Preview build: every page in one HTML document with hash routing (#en-ramo, #en-index.work),
    because the artifact viewer blocks navigation between separately published HTML files."""
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
                tok = ids[target] + ("." + frag if frag else "")
                return f'{attr}="#{tok}"'
            extra = ' target="_blank" rel="noopener"' if attr == "href" and "target=" not in m.group(0) else ""
            return f'{attr}="{target}"{extra}'
        return re.sub(r'(href|src)="([^"]*)"', href, body)

    blocks = []
    for lang, path, title, desc, body in pages:
        blocks.append(f'<div class="pg" data-page="{ids[path]}" data-title="{E(title)}" lang="{lang}" hidden>{fix(body, path)}</div>')
    router = """<script>
(function(){
  var pages=document.querySelectorAll('.pg');
  function show(){
    var h=(location.hash||'').slice(1), parts=h.split('.'), id=parts[0]||'en-index', sec=parts[1];
    var found=false;
    pages.forEach(function(p){var on=p.getAttribute('data-page')===id; p.hidden=!on; if(on){found=true; document.title=p.getAttribute('data-title');}});
    if(!found){pages.forEach(function(p){p.hidden=p.getAttribute('data-page')!=='en-index'});}
    var cur=document.querySelector('.pg:not([hidden])');
    var el=sec&&cur?cur.querySelector('#'+sec):null;
    if(el){el.scrollIntoView();}else{window.scrollTo(0,0);}
  }
  window.addEventListener('hashchange',show); show();
})();
</script>"""
    home = next(x for x in pages if x[1] == "index.html")
    return document("en", "index.html", home[2], home[3], "".join(blocks) + router, fragment=True)


if __name__ == "__main__":
    main()


