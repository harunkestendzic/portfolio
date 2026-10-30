# -*- coding: utf-8 -*-
"""System diagrams as inline SVG. Colours come from CSS custom properties,
so every diagram follows the light and dark theme automatically."""
from html import escape


def _lines(x, y, lines, cls, lh=18, anchor="start"):
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i * lh}" class="{cls}" text-anchor="{anchor}">{escape(ln)}</text>')
    return "".join(out)


def node(x, y, w, h, title, sub=(), kind="", tag=None):
    """A box with a bold title and optional smaller lines."""
    k = f" n-{kind}" if kind else ""
    s = f'<g class="dn{k}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10"/>'
    ty = y + 26
    if tag:
        s += f'<text x="{x + 16}" y="{y + 22}" class="dt-tag">{escape(tag)}</text>'
        ty = y + 44
    s += f'<text x="{x + 16}" y="{ty}" class="dt-title">{escape(title)}</text>'
    s += _lines(x + 16, ty + 21, list(sub), "dt-sub")
    return s + "</g>"


def arrow(points, label=None, lx=None, ly=None, kind=""):
    d = "M" + " L".join(f"{px},{py}" for px, py in points)
    k = f" a-{kind}" if kind else ""
    s = f'<path d="{d}" class="da{k}" marker-end="url(#ah{("-" + kind) if kind else ""})"/>'
    if label:
        s += f'<text x="{lx}" y="{ly}" class="dt-label">{escape(label)}</text>'
    return s


DEFS = """<defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dm"/></marker>
<marker id="ah-hydro" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dm-hydro"/></marker>
<marker id="ah-vulcan" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="dm-vulcan"/></marker>
</defs>"""


def svg(w, h, body, label):
    return (f'<svg class="dg" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{DEFS}{body}</svg>')


def L(lang, en, bs):
    return en if lang == "en" else bs


# ------------------------------------------------------------------ ArcaneTD
def arcane_loop(lang):
    b = ""
    b += node(30, 40, 160, 80, L(lang, "Deploy", "Iskrcavanje"), [L(lang, "to the next island", "na sljedeće ostrvo")])
    b += node(230, 30, 210, 100, L(lang, "Setup and extraction", "Priprema i ekstrakcija"),
              [L(lang, "Harvest liquids with beacons", "Vađenje tečnosti pomoću stanica"),
               L(lang, "Place the first towers", "Postavljanje prvih tornjeva")], tag="A")
    # combat box
    b += node(480, 20, 450, 220, L(lang, "Combat waves", "Talasi borbe"), [], kind="focus", tag="B")
    steps = [L(lang, "1  Real-time wave defence", "1  Odbrana od talasa u realnom vremenu"),
             L(lang, "2  Retrofit towers into elemental forms", "2  Adaptacija tornjeva u elementarne forme"),
             L(lang, "3  Manage crew stress and toxicity", "3  Upravljanje stresom ekipe i toksičnošću"),
             L(lang, "4  Middleman card draft between waves", "4  Posrednikov izbor karata između talasa")]
    b += _lines(500, 98, steps, "dt-sub", lh=27)
    b += arrow([(905, 200), (905, 225), (720, 225)], None)
    b += f'<text x="760" y="216" class="dt-label">{escape(L(lang, "next wave", "sljedeći talas"))}</text>'
    b += node(670, 300, 260, 90, L(lang, "Level clear", "Nivo završen"),
              [L(lang, "Attrition or Turbo win", "Attrition ili Turbo pobjeda")], tag="C")
    b += node(370, 300, 260, 90, L(lang, "Turbo win: bribe shop", "Turbo: prodavnica mita"),
              [L(lang, "Spend liquids on next-level bonuses", "Tečnosti za bonuse u sljedećem nivou")], tag="D")
    b += node(30, 300, 300, 90, L(lang, "Attrition win: Nexium Codex", "Attrition: Nexium Codex"),
              [L(lang, "Bank liquids for permanent unlocks", "Tečnosti za trajna otključavanja")], tag="E")
    b += arrow([(190, 80), (226, 80)])
    b += arrow([(440, 80), (476, 80)])
    b += arrow([(800, 240), (800, 296)])
    b += arrow([(670, 345), (634, 345)], L(lang, "Turbo", "Turbo"), 636, 292)
    b += arrow([(800, 390), (800, 420), (180, 420), (180, 394)], L(lang, "Attrition", "Attrition"), 420, 414)
    b += arrow([(110, 300), (110, 124)], L(lang, "next island", "sljedeće ostrvo"), 120, 220)
    return svg(960, 440, b, L(lang, "ArcaneTD level loop", "Petlja nivoa u ArcaneTD-u"))


def arcane_elements(lang):
    b = ""
    b += node(20, 150, 200, 90, L(lang, "Basic tower", "Osnovni toranj"), [L(lang, "Upgradable anywhere", "Nadogradiv bilo gdje")])
    b += node(270, 50, 190, 80, "Hydronium", [L(lang, "needs a water tile", "traži polje vode")], kind="hydro")
    b += node(270, 260, 190, 80, "Vulcanex", [L(lang, "needs a magma tile", "traži polje magme")], kind="vulcan")
    for i, (nm, sb) in enumerate([("Sizzlium", L(lang, "corrosive acid", "korozivna kiselina")),
                                  ("Blumion", L(lang, "green lightning", "zelena munja")),
                                  ("Last Breath", L(lang, "choking mist", "zagušljiva magla"))]):
        y = 4 + i * 74
        b += node(540, y, 200, 64, nm, [sb], kind="hydro")
        b += arrow([(460, 90), (500, 90), (500, y + 32), (536, y + 32)], kind="hydro")
    b += node(540, 268, 200, 64, "Plasmonex", [], kind="vulcan")
    b += node(780, 260, 160, 80, "Solarix", [L(lang, "prestige form", "prestižna forma")], kind="solar")
    b += arrow([(220, 180), (245, 180), (245, 90), (266, 90)], kind="hydro")
    b += arrow([(220, 210), (245, 210), (245, 300), (266, 300)], kind="vulcan")
    b += arrow([(460, 300), (536, 300)], kind="vulcan")
    b += arrow([(740, 300), (776, 300)], kind="vulcan")
    b += f'<text x="20" y="390" class="dt-label">{escape(L(lang, "Every elemental upgrade needs a blueprint card and a retrofit.", "Svaka elementarna nadogradnja traži kartu nacrta i adaptaciju."))}</text>'
    return svg(960, 400, b, L(lang, "ArcaneTD tower upgrade tree", "Stablo nadogradnje tornjeva u ArcaneTD-u"))


def arcane_loyalty(lang):
    x0, w, y = 40, 880, 70
    bands = [(0, 19, L(lang, "Distrust", "Nepovjerenje"), L(lang, "Worse offers, more risk cards", "Lošije ponude, više rizičnih karata")),
             (20, 39, L(lang, "Volatile", "Nestabilno"), L(lang, "Higher prices, rarer blueprints", "Više cijene, rjeđi nacrti")),
             (40, 59, L(lang, "Neutral", "Neutralno"), L(lang, "Baseline offers", "Osnovne ponude")),
             (60, 79, L(lang, "Friendly", "Prijateljski"), L(lang, "Better cards, cheaper rerolls", "Bolje karte, jeftinije osvježavanje")),
             (80, 100, L(lang, "Loyal", "Lojalno"), L(lang, "Best pools, insider cards", "Najbolje karte, insajderske karte"))]
    b = ""
    for i, (a, z, nm, eff) in enumerate(bands):
        bx = x0 + a / 100 * w
        bw = (z - a + (1 if z == 100 else 1)) / 100 * w if z != 100 else (100 - a) / 100 * w
        b += f'<rect x="{bx:.1f}" y="{y}" width="{bw - 2:.1f}" height="40" rx="6" class="lb lb-{i}"/>'
        b += f'<text x="{bx + 10:.1f}" y="{y + 26}" class="dt-title lb-t">{escape(nm)}</text>'
        b += f'<text x="{bx + 4:.1f}" y="{y + 66}" class="dt-sub">{escape(eff.split(", ")[0])}</text>'
        if ", " in eff:
            b += f'<text x="{bx + 4:.1f}" y="{y + 84}" class="dt-sub">{escape(eff.split(", ")[1])}</text>'
    for v in (0, 20, 40, 60, 80, 100):
        tx = x0 + v / 100 * w
        b += f'<line x1="{tx:.1f}" y1="{y - 8}" x2="{tx:.1f}" y2="{y}" class="dtick"/>'
        b += f'<text x="{tx:.1f}" y="{y - 14}" class="dt-label" text-anchor="middle">{v}</text>'
    sx = x0 + 0.5 * w
    b += f'<path d="M{sx},{y + 100} L{sx},{y + 112}" class="da"/>'
    b += f'<text x="{sx}" y="{y + 132}" class="dt-label" text-anchor="middle">{escape(L(lang, "every run starts at 50", "svaka partija počinje na 50"))}</text>'
    b += f'<text x="{x0}" y="{y + 170}" class="dt-label">{escape(L(lang, "Loyalty moves when you take cards, reject risk cards, refresh offers or leave without buying.", "Lojalnost se mijenja kada uzmeš kartu, odbiješ rizičnu, osvježiš ponude ili odeš bez kupovine."))}</text>'
    return svg(960, 260, b, L(lang, "Middleman loyalty scale", "Skala lojalnosti Posrednika"))


def arcane_crew(lang):
    b = ""
    b += node(370, 10, 220, 60, L(lang, "Crew selection", "Raspored ekipe"), [])
    cols = [(L(lang, "Research Lab", "Laboratorija"), [L(lang, "Runs the lab", "Upravlja laboratorijom")]),
            (L(lang, "Maintenance", "Održavanje"), [L(lang, "Slows toxicity build-up", "Usporava rast toksičnosti"), L(lang, "Speeds up venting", "Ubrzava ispuštanje")]),
            (L(lang, "Defense", "Odbrana"), [L(lang, "Runs the attack towers", "Pokreće napadačke tornjeve")])]
    for i, (nm, sub) in enumerate(cols):
        x = 40 + i * 310
        b += node(x, 120, 260, 100, nm, sub)
        b += arrow([(480, 70), (480, 92), (x + 130, 92), (x + 130, 116)])
        b += arrow([(x + 130, 220), (x + 130, 246), (480, 246), (480, 266)])
    b += node(360, 270, 240, 56, L(lang, "Stress builds up", "Stres raste"), [], kind="focus")
    b += node(80, 370, 300, 70, L(lang, "Rest slot", "Mjesto za odmor"), [L(lang, "Stress goes down safely", "Stres se sigurno smanjuje")])
    b += node(580, 370, 320, 70, L(lang, "Burnout", "Izgaranje"), [L(lang, "Performance drops further", "Učinak dodatno pada")], kind="vulcan")
    b += arrow([(420, 326), (420, 346), (230, 346), (230, 366)])
    b += arrow([(540, 326), (540, 346), (740, 346), (740, 366)], kind="vulcan")
    return svg(960, 450, b, L(lang, "ArcaneTD crew and stress system", "Sistem ekipe i stresa u ArcaneTD-u"))


# ------------------------------------------------------------------ Ramo
def ramo_structure(lang):
    b = ""
    b += node(20, 40, 200, 100, L(lang, "Main menu", "Glavni meni"),
              [L(lang, "Teletext page", "Teletekst stranica"), L(lang, "on-screen TV remote", "TV daljinski na ekranu")], kind="focus")
    x = 270
    for i in range(1, 6):
        b += node(x, 60, 88, 60, f"{L(lang, 'Ep.', 'Ep.')} {i}", [])
        if i < 5:
            b += arrow([(x + 88, 90), (x + 102, 90)])
        x += 106
    b += node(x + 10, 50, 110, 80, L(lang, "Final", "Finale"), [L(lang, "boss", "boss")], kind="vulcan")
    b += arrow([(x - 18, 90), (x + 6, 90)])
    b += arrow([(220, 90), (266, 90)])
    b += f'<path d="M270,150 L920,150" class="dbrace"/>'
    b += node(270, 180, 650, 110, L(lang, "Inside every level", "Unutar svakog nivoa"),
              [L(lang, "Checkpoints and respawn, keys that open doors, NPC dialogue,", "Checkpointi i ponovno oživljavanje, ključevi za vrata, dijalozi s likovima,"),
               L(lang, "melee and ranged enemies, and hazards from the setting.", "neprijatelji za blisku i daljinsku borbu i prepreke iz okruženja.")])
    return svg(960, 300, b, L(lang, "Ramo game structure", "Struktura igre Ramo"))


def ramo_systems(lang):
    b = ""
    b += node(370, 165, 220, 80, "Ramo", [L(lang, "player controller", "kontroler igrača")], kind="focus")
    boxes = [
        (20, 10, L(lang, "Movement", "Kretanje"), [L(lang, "Run, jump, crouch", "Trčanje, skok, čučanj"), L(lang, "Ladder climbing", "Penjanje uz ljestve")]),
        (660, 10, L(lang, "Combat", "Borba"), [L(lang, "Melee attacks, pistol pickup", "Udarci, pištolj koji se pokupi"), L(lang, "Health, burek pickups", "Zdravlje, burek kao bonus")]),
        (20, 290, L(lang, "World", "Svijet"), [L(lang, "Melee and ranged enemies", "Neprijatelji blizu i daleko"), L(lang, "Boss on curved flight paths", "Boss po zakrivljenim putanjama"), L(lang, "Mines, wire, electricity, snipers", "Mine, žica, struja, snajperi")]),
        (660, 290, L(lang, "Flow and presentation", "Tok i prezentacija"), [L(lang, "Checkpoints, keys, doors", "Checkpointi, ključevi, vrata"), L(lang, "Dialogue, parallax, audio", "Dijalozi, parallax, zvuk"), L(lang, "Teletext menu, settings", "Teletekst meni, postavke")]),
    ]
    for x, y, nm, sub in boxes:
        h = 100 if len(sub) == 2 else 120
        b += node(x, y, 280, h, nm, sub)
    b += arrow([(300, 60), (366, 180)])
    b += arrow([(660, 60), (594, 180)])
    b += arrow([(366, 230), (300, 320)])
    b += arrow([(594, 230), (660, 320)])
    return svg(960, 420, b, L(lang, "Ramo gameplay systems", "Sistemi igre Ramo"))


# ------------------------------------------------------------------ Jugoton
def vinyl_checkout(lang):
    b = ""
    b += node(20, 40, 170, 80, L(lang, "Cart", "Korpa"), [L(lang, "records and quantities", "ploče i količine")])
    b += node(230, 40, 190, 80, L(lang, "Checkout form", "Forma za plaćanje"), [L(lang, "shipping address", "adresa dostave")])
    b += node(460, 20, 300, 200, L(lang, "One transaction", "Jedna transakcija"), [], kind="focus", tag="sp_place_order")
    steps = [L(lang, "1  Check the record exists", "1  Provjera da ploča postoji"),
             L(lang, "2  Check there is enough stock", "2  Provjera zalihe"),
             L(lang, "3  Create the order", "3  Kreiranje narudžbe"),
             L(lang, "4  Add items, lower stock", "4  Dodavanje stavki, umanjenje zalihe")]
    b += _lines(478, 96, steps, "dt-sub", lh=27)
    b += node(800, 20, 140, 80, L(lang, "Commit", "Potvrda"), [L(lang, "order placed", "narudžba primljena")])
    b += node(800, 140, 140, 80, L(lang, "Rollback", "Poništenje"), [L(lang, "nothing changes", "ništa se ne mijenja")], kind="vulcan")
    b += arrow([(190, 80), (226, 80)])
    b += arrow([(420, 80), (456, 80)])
    b += arrow([(760, 60), (796, 60)])
    b += arrow([(760, 180), (796, 180)], kind="vulcan")
    b += node(460, 260, 300, 70, L(lang, "Trigger on Order_Items", "Okidač na Order_Items"), [L(lang, "blocks any quantity above stock", "blokira količinu veću od zalihe")], kind="vulcan")
    b += arrow([(610, 256), (610, 224)], kind="vulcan")
    return svg(960, 340, b, L(lang, "Jugoton checkout flow", "Tok plaćanja u Jugotonu"))


def vinyl_cloud(lang):
    b = ""
    b += node(200, 20, 540, 290, L(lang, "Ubuntu 24 virtual machine", "Ubuntu 24 virtualna mašina"), [], kind="focus", tag="Oracle Cloud (OCI)")
    b += node(20, 130, 140, 80, L(lang, "Browser", "Preglednik"), [L(lang, "visitor", "posjetilac")])
    b += node(220, 110, 150, 100, "Nginx", [L(lang, "serves CSS,", "servira CSS,"), L(lang, "images, HTML", "slike, HTML")])
    b += node(400, 110, 150, 100, "PHP 8.4-FPM", [L(lang, "runs the PHP", "izvršava PHP"), L(lang, "scripts", "skripte")])
    b += node(580, 110, 140, 100, "MySQL", ["vinyl_shop", L(lang, "localhost only", "samo localhost")])
    b += node(220, 236, 500, 56, L(lang, "Port 80 open, port 3306 closed to the internet", "Port 80 otvoren, port 3306 zatvoren prema internetu"), [], kind="vulcan")
    b += node(780, 110, 160, 100, "Autonomous DB", [L(lang, "Oracle copy of", "Oracle kopija"), L(lang, "the data", "podataka")])
    b += arrow([(160, 170), (216, 170)], ":80", 168, 160)
    b += arrow([(370, 160), (396, 160)])
    b += arrow([(550, 160), (576, 160)])
    b += arrow([(475, 210), (475, 222), (860, 222), (860, 214)], "OCI8", 870, 236)
    b += _lines(385, 102, [L(lang, "socket", "socket")], "dt-label", anchor="middle")
    return svg(960, 330, b, L(lang, "Jugoton deployed on Oracle Cloud", "Jugoton postavljen na Oracle Cloud"))


DIAGRAMS = {
    "vinyl_cloud": (vinyl_cloud, ("Jugoton in the cloud", "Jugoton u cloudu"),
                    ("Three tiers on one Oracle Cloud VM, with an Oracle Autonomous Database holding a copy of the data.",
                     "Tri sloja na jednoj Oracle Cloud virtualnoj mašini, uz Oracle Autonomous Database koji čuva kopiju podataka.")),
    "vinyl_checkout": (vinyl_checkout, ("Checkout, step by step", "Plaćanje, korak po korak"),
                       ("Placing an order is all or nothing. The database stops overselling even if the application misses it.",
                        "Narudžba je sve ili ništa. Baza sprječava prodaju preko zalihe čak i ako aplikacija to propusti.")),
    "arcane_loop": (arcane_loop, ("The level loop", "Petlja jednog nivoa"),
                    ("One island from start to finish. Combat is the inner loop; the outer loop carries resources between islands.",
                     "Jedno ostrvo od početka do kraja. Borba je unutrašnja petlja; vanjska prenosi resurse između ostrva.")),
    "arcane_elements": (arcane_elements, ("Tower upgrade tree", "Stablo nadogradnje tornjeva"),
                        ("Which elemental forms a tower can take, and what each branch needs on the map.",
                         "Koje elementarne forme toranj može dobiti i šta svaka grana traži na mapi.")),
    "arcane_loyalty": (arcane_loyalty, ("Middleman loyalty", "Lojalnost Posrednika"),
                       ("Loyalty runs from 0 to 100 and changes what the Middleman offers. Drawn to scale.",
                        "Lojalnost ide od 0 do 100 i mijenja šta Posrednik nudi. Nacrtano u razmjeri.")),
    "arcane_crew": (arcane_crew, ("Crew and stress", "Ekipa i stres"),
                    ("Three work slots and one rest slot. Stress and burnout lower how well a member performs.",
                     "Tri radna mjesta i jedno za odmor. Stres i izgaranje smanjuju učinak člana.")),
    "ramo_structure": (ramo_structure, ("Game structure", "Struktura igre"),
                       ("Five episodes and a final level, picked from a teletext menu.",
                        "Pet epizoda i finalni nivo, birani iz teletekst menija.")),
    "ramo_systems": (ramo_systems, ("Gameplay systems", "Sistemi igre"),
                     ("How the player connects to the rest of the game.",
                      "Kako je igrač povezan s ostatkom igre.")),
}
