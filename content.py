# -*- coding: utf-8 -*-
"""All site content, in English (en) and Bosnian (bs).

To add a project: append a dict to PROJECTS (copy an existing one), add its
images under assets/<slug>/, and optionally a diagram function in diagrams.py.
To add a devlog post: append a dict to DEVLOG. Then run `python3 build.py`.
"""


def t(en, bs):
    return {"en": en, "bs": bs}


PLACEHOLDER = t("Placeholder", "Privremeno")

PERSON = {
    "name": "Harun Kestendžić",
    "email": "harunkestendzic@gmail.com",
    "phone": "061 222 430",
    "linkedin": "https://www.linkedin.com/in/harun-kestend%C5%BEi%C4%87-055188280/",
    "github": "https://github.com/harunkestendzic",
    "cv": "assets/Harun-Kestendzic-CV.pdf",
    "letter": "assets/Harun-Kestendzic-Recommendation-Alchemy-Studio.pdf",  # placeholder: export the CV doc here
}

UI = {
    "nav_work": t("Work", "Projekti"),
    "nav_experience": t("Experience", "Iskustvo"),
    "nav_devlog": t("Devlog", "Devlog"),
    "nav_contact": t("Contact", "Kontakt"),
    "skip": t("Skip to content", "Preskoči na sadržaj"),
    "lang_other": t("BS", "EN"),
    "lang_other_label": t("Bosanski", "English"),
    "download_cv": t("Download CV", "Preuzmi CV"),
    "letter": t("Recommendation letter", "Pismo preporuke"),
    "letter_long": t("Read the recommendation letter", "Pročitaj pismo preporuke"),
    "letter_quote": t("He stood out the most by far from all the previous applicants we had.",
                      "Isticao se daleko najviše od svih prethodnih kandidata koje smo imali."),
    "letter_by": t("Jasmin Skamo, Founder and CEO, Alchemy Studio", "Jasmin Skamo, osnivač i direktor, Alchemy Studio (pismo na engleskom)"),
    "email_me": t("Email me", "Pošalji email"),
    "copy": t("Copy", "Kopiraj"),
    "copied": t("Copied", "Kopirano"),
    "read_case": t("Read the case study", "Pročitaj studiju projekta"),
    "status": t("Status", "Status"),
    "role": t("Role", "Uloga"),
    "timeline": t("Timeline", "Period"),
    "platforms": t("Platforms", "Platforme"),
    "stack": t("Stack", "Tehnologije"),
    "links": t("Links", "Linkovi"),
    "back_home": t("All work", "Svi projekti"),
    "next_project": t("Next project", "Sljedeći projekt"),
    "devlog_for": t("Devlog entries", "Devlog zapisi"),
    "no_posts": t("No entries for this project yet.", "Još nema zapisa za ovaj projekt."),
    "all_posts": t("All devlog entries", "Svi devlog zapisi"),
    "footer_note": t("Built from plain HTML and CSS. Updated as the work moves.",
                     "Napravljeno u čistom HTML-u i CSS-u. Ažurira se kako rad napreduje."),
    "evidence": t("Where it shows", "Gdje se vidi"),
    "placeholder": PLACEHOLDER,
}

HOME = {
    "title": t("Harun Kestendžić", "Harun Kestendžić"),
    "description": t(
        "Backend and software developer in Sarajevo. Node.js, C#, PHP and cloud deployment, with a Computer Science degree in progress.",
        "Backend i softverski developer iz Sarajeva. Node.js, C#, PHP i deploy u cloudu, uz studij računarskih nauka u toku."),
    "hero_h1": t("Building backend systems, and learning to make them intelligent.",
                 "Pravim backend sisteme i učim kako ih napraviti pametnim."),
    "hero_p": t(
        "Computer Science student at SSST in Sarajevo, minoring in Electrical Engineering. "
        "I build backend systems and web applications: a shop deployed on Oracle Cloud, APIs in Node.js and PHP. "
        "Before that I spent a year as a junior developer in a studio, building UI and systems. I now work through the Backend AI Engineering track at FlyRank.",
        "Student računarskih nauka na SSST-u u Sarajevu, sa minorom iz elektrotehnike. "
        "Pravim backend sisteme i web aplikacije: shop postavljen na Oracle Cloud, API-je u Node.js-u i PHP-u. "
        "Prije toga sam godinu dana radio kao junior developer u studiju, na UI-ju i sistemima. Sada radim kroz smjer Backend AI Engineering u FlyRanku."),
    "brief_title": t("At a glance", "Ukratko"),
    "brief": [
        (t("Looking for", "Tražim"), t("Junior developer or internship role, in backend, AI or software",
                                       "Poziciju junior developera ili praksu, u backendu, AI-ju ili softveru")),
        (t("Location", "Lokacija"), t("Sarajevo, Bosnia and Herzegovina", "Sarajevo, Bosna i Hercegovina")),
        (t("Studying", "Studij"), t("BSc Computer Science, SSST, 3rd year (graduating 2028)",
                                    "BSc računarske nauke, SSST, 3. godina (diploma 2028.)")),
        (t("Languages", "Jezici"), t("English (TOEFL iBT 100/120), Bosnian", "Engleski (TOEFL iBT 100/120), bosanski")),
    ],
    "proof": [
        (t("800+", "800+"), t("plays and downloads of Ramo, a game I built alone",
                               "igranja i preuzimanja igre Ramo, koju sam napravio sam")),
        (t("1st", "1."), t("place, game programming, FIT Coding Challenge v.19 (2026)",
                           "mjesto, programiranje igara, FIT Coding Challenge v.19 (2026.)")),
        (t("16k", "16k"), t("lines of C# in ArcaneTD, written and understood end to end",
                            "linija C# koda u ArcaneTD-u, napisanih i razumljivih od početka do kraja")),
        (t("8.58", "8,58"), t("GPA out of 10 after four semesters at SSST (81.75/100, B+), plus an Atlantbh scholarship",
                                "prosjek od 10 nakon četiri semestra na SSST-u (81,75/100, B+), uz Atlantbh stipendiju")),
    ],
    "work_h": t("Selected work", "Izdvojeni projekti"),
    "work_intro": t("Projects, each with its own page: what it is, how it is built, and what I did.",
                    "Projekti, svaki sa svojom stranicom: šta je, kako je napravljen i šta sam radio."),
    "more_h": t("Smaller projects", "Manji projekti"),
    "exp_h": t("Experience", "Iskustvo"),
    "skills_h": t("Skills, with evidence", "Vještine, uz dokaze"),
    "skills_intro": t("Each skill points to where it was used, so nothing here is just a keyword.",
                      "Svaka vještina pokazuje gdje je korištena, tako da ništa ovdje nije samo ključna riječ."),
    "edu_h": t("Education", "Obrazovanje"),
    "awards_h": t("Awards and certificates", "Nagrade i certifikati"),
    "press_h": t("In the media", "U medijima"),
    "press_p": t("Ramo was covered by Dnevni avaz, TVSA, Face TV, Federalna TV and BHRT.",
                 "O Rami su izvještavali Dnevni avaz, TVSA, Face TV, Federalna TV i BHRT."),
    "now_h": t("Now", "Trenutno"),
    "now_p": t("The latest entries from the devlog.", "Najnoviji zapisi iz devloga."),
    "contact_h": t("Contact", "Kontakt"),
    "contact_p": t("Email is the fastest way to reach me. The CV has everything on one page.",
                   "Email je najbrži način da me kontaktirate. CV ima sve na jednom mjestu."),
}

# ---------------------------------------------------------------- projects
PROJECTS = [
    {
        "slug": "ramo",
        "name": "Ramo",
        "theme": "ramo",
        "status": t("Released", "Objavljeno"),
        "status_kind": "live",
        "hook": t("A 2D platformer set in Sarajevo in spring 1992, where the level select is a teletext screen.",
                  "2D platformer smješten u Sarajevo u proljeće 1992., u kojem je izbor nivoa teletekst ekran."),
        "summary": t(
            "Built alone, from idea to release. Ramo, an underdog from Alipašino Polje, fights his way across the city "
            "through five episodes and a final level, with melee and pistol combat, wartime hazards and a boss fight.",
            "Napravljeno samostalno, od ideje do objave. Ramo, uličar s Alipašinog Polja, probija se kroz grad "
            "kroz pet epizoda i finalni nivo, uz borbu prsa u prsa i pištoljem, ratne prepreke i borbu s bossom."),
        "tags": ["Unity", "C#", "2D", "Pixel art"],
        "facts": [t("800+ plays and downloads", "800+ igranja i preuzimanja"),
                  t("1st place, FIT Coding Challenge v.19", "1. mjesto, FIT Coding Challenge v.19"),
                  t("Covered on national TV", "Prikazano na državnoj televiziji")],
        "role": t("Solo developer", "Samostalni developer"),
        "timeline": t("2023 to 2024, released on itch.io", "2023. do 2024., objavljeno na itch.io"),
        "platforms": t("Windows and browser, in English and Bosnian", "Windows i preglednik, na engleskom i bosanskom"),
        "stack": "Unity, C#",
        "links": [
            (t("Play in browser (itch.io)", "Igraj u pregledniku (itch.io)"), "https://simpohax.itch.io/ramobrowseredition"),
            (t("Download for Windows", "Preuzmi za Windows"), "https://simpohax.itch.io/ramo"),
            (t("Source on GitHub", "Kod na GitHubu"), "https://github.com/harunkestendzic/ramo"),
            (t("Trailer and clips (YouTube)", "Trailer i snimci (YouTube)"), "https://www.youtube.com/@ramothegame6274"),
        ],
        "idea": t(
            "Ramo takes the classic side-scrolling platformer and puts it somewhere games rarely go: Sarajevo in 1992. "
            "The city is the level design. Enemies, hazards and even health pickups (a burek) come from local life of that time, "
            "and the menus are styled as the teletext pages and TV remote people used then.",
            "Ramo uzima klasični side-scrolling platformer i smješta ga tamo gdje igre rijetko idu: u Sarajevo 1992. "
            "Grad je dizajn nivoa. Neprijatelji, prepreke, pa čak i predmeti za zdravlje (burek) dolaze iz tadašnjeg lokalnog života, "
            "a meniji su napravljeni kao teletekst stranice i TV daljinski iz tog vremena."),
        "built": [
            t("Player controller with running, jumping, crouching, ladder climbing, melee attacks and a pistol pickup with projectiles.",
              "Kontroler igrača sa trčanjem, skakanjem, čučanjem, penjanjem uz ljestve, udarcima i pištoljem koji se pokupi."),
            t("Melee and ranged enemy types with patrol and chase behaviour, enemy respawning and floating health bars.",
              "Neprijatelji za blisku i daljinsku borbu, s patroliranjem i jurenjem, ponovnim pojavljivanjem i trakama zdravlja."),
            t("A boss that flies along curved routes and fires at the player.",
              "Boss koji leti po zakrivljenim putanjama i puca na igrača."),
            t("Hazards built for the setting: mines, barbed wire, live electrical boxes, syringes, sniper fire and falling bombs.",
              "Prepreke prilagođene okruženju: mine, bodljikava žica, električne kutije, šprice, snajperska vatra i bombe koje padaju."),
            t("Checkpoints, respawning, keys and doors, dialogue triggers with typed-out text and sound.",
              "Checkpointi, ponovno oživljavanje, ključevi i vrata, dijalozi koji se ispisuju slovo po slovo, sa zvukom."),
            t("Parallax backgrounds, music and sound settings, and a teletext-style episode menu driven by an on-screen TV remote.",
              "Parallax pozadine, postavke muzike i zvuka i meni epizoda u stilu teleteksta kojim se upravlja TV daljinskim na ekranu."),
        ],
        "numbers": [
            ("64", t("C# scripts", "C# skripti")),
            ("3,400+", t("lines of game code", "linija koda igre")),
            ("6", t("levels: five episodes and a final", "nivoa: pet epizoda i finale")),
            ("800+", t("plays and downloads", "igranja i preuzimanja")),
        ],
        "highlight_h": t("What I learned shipping it", "Šta sam naučio objavljujući je"),
        "highlight": t(
            "Ramo was my first complete game, which meant doing everything a release needs: level design, balancing, "
            "menus, audio, builds for two platforms and fixing what players reported after launch "
            "(the last update was a round of bug fixes and changes based on feedback). It also became my high school "
            "graduation project, a 25-page write-up of the development process from start to finish.",
            "Ramo je moja prva završena igra, što znači da sam morao uraditi sve što objava traži: dizajn nivoa, balans, "
            "menije, zvuk, verzije za dvije platforme i popravke onoga što su igrači prijavili nakon objave "
            "(posljednje ažuriranje bili su popravci grešaka i izmjene na osnovu povratnih informacija). Postala je i moj "
            "maturski rad, opis razvojnog procesa od početka do kraja na 25 stranica."),
        "code": None,
        "media": [
            {"src": "assets/ramo/teletext.png", "alt": t("The episode menu, styled as a 1990s teletext page", "Meni epizoda, napravljen kao teletekst stranica iz 90-ih"),
             "caption": t("The episode select, styled as a teletext page.", "Izbor epizode, u stilu teletekst stranice."), "pixel": False},
            {"src": "assets/ramo/shot-1.png", "alt": t("Ramo climbing a ladder between apartment blocks, with health hearts and ammo in the corner", "Ramo se penje uz ljestve između zgrada, sa srcima zdravlja i municijom u uglu"),
             "caption": t("Climbing between apartment blocks. Hearts show health, the top right shows ammo.", "Penjanje između zgrada. Srca pokazuju zdravlje, gore desno je municija."), "pixel": True},
            {"src": "assets/ramo/shot-2.png", "alt": t("A fight inside a Sarajevo tram", "Borba u sarajevskom tramvaju"),
             "caption": t("A level set inside a tram.", "Nivo smješten u tramvaj."), "pixel": True},
            {"src": "assets/ramo/shot-3.png", "alt": t("A street level with a police car and armed enemies", "Ulični nivo s policijskim autom i naoružanim neprijateljima"),
             "caption": t("Street combat: melee and pistol enemies.", "Borba na ulici: neprijatelji s udarcima i pištoljima."), "pixel": True},
        ],
        "diagrams": ["ramo_structure", "ramo_systems"],
        "cover_image": "assets/ramo/cover.jpg",
        "videos": [("kaMRZPMHqCY", t("Official trailer", "Službeni trailer")),
                   ("GLMcg1Q5ywI", t("Speedrun of the full game", "Speedrun cijele igre"))],
    },
    {
        "slug": "arcanetd",
        "name": "ArcaneTD",
        "theme": "arcane",
        "status": t("In development", "U razvoju"),
        "status_kind": "dev",
        "hook": t("A tower defence where every power spike comes with a price: pollution, a stressed crew, and a Middleman who sells you out.",
                  "Tower defence u kojem svako pojačanje ima cijenu: zagađenje, iscrpljenu ekipu i Posrednika koji vas prodaje."),
        "summary": t(
            "A roguelike tower defence on a hex grid with a bio-punk plague doctor theme. Towers turn elemental when built next to "
            "the right liquid, a black-market Middleman drafts cards between waves, and a crew of scientists has to be kept from burning out.",
            "Roguelike tower defence na heksagonalnoj mreži, s bio-punk temom doktora kuge. Tornjevi postaju elementarni kada se izgrade "
            "pored prave tečnosti, crnoberzanski Posrednik nudi karte između talasa, a tim naučnika treba čuvati od izgaranja."),
        "tags": ["Unity 3D (URP)", "C#", "Game design", "Hex grid"],
        "facts": [t("About 16,000 lines of C#", "Oko 16.000 linija C# koda"),
                  t("156 scripts, built solo", "156 skripti, samostalno"),
                  t("Own game design document", "Vlastiti dizajn dokument igre")],
        "role": t("Solo developer and designer", "Samostalni developer i dizajner"),
        "timeline": t("Ongoing", "U toku"),
        "platforms": t("PC and mobile (planned)", "PC i mobilni uređaji (planirano)"),
        "stack": "Unity 3D (URP), C#, ScriptableObjects, DOTween",
        "links": [(t("Showcase on GitHub (code is private)", "Prikaz na GitHubu (kod je privatan)"), "https://github.com/harunkestendzic/arcane-td-showcase")],
        "idea": t(
            "Most tower defence games reward building more. ArcaneTD makes every decision cost something. "
            "Turning a tower elemental needs a blueprint card and a retrofit, so timing matters. "
            "Refusing a risky card from the Middleman means he sells it to the enemy. "
            "Strong towers pollute the base, and an overworked crew performs worse.",
            "Većina tower defence igara nagrađuje gradnju što više tornjeva. U ArcaneTD-u svaka odluka ima cijenu. "
            "Da toranj postane elementaran, trebaju karta nacrta i adaptacija, pa je tajming bitan. "
            "Ako odbijete rizičnu kartu od Posrednika, on je prodaje neprijatelju. "
            "Jaki tornjevi zagađuju bazu, a preopterećena ekipa radi lošije."),
        "lore": [
            t("A rogue doctor has formed a rebel alliance to cure a disease that is spreading across the world. The cure can only be researched from rare elements found on one place on Earth: an archipelago of islands. You play the doctor, and the islands are where you work.",
              "Odmetnuti doktor je osnovao pobunjenički savez kako bi pronašao lijek za bolest koja se širi svijetom. Lijek se može istražiti samo iz rijetkih elemenata koji postoje na jednom mjestu na Zemlji: arhipelagu ostrva. Ti igraš doktora, a ostrva su mjesto gdje radiš."),
            t("The most important element is Nexium. It is powerful enough to help build a cure, and just as able to be turned into a weapon. How it ended up on the islands is still an open question in the story.",
              "Najvažniji element je Nexium. Dovoljno je moćan da pomogne u izradi lijeka, a jednako se može pretvoriti u oružje. Kako je dospio na ostrva, za sada je otvoreno pitanje priče."),
            t("The World Government wants the same islands for the opposite reason. It sends troops, and infected soldiers, to stop the research and silence the rebels, so it can use the elements for weapons of mass destruction and tools of control instead of a cure.",
              "Svjetska vlada želi ista ostrva iz suprotnog razloga. Šalje vojsku i zaražene vojnike da zaustave istraživanje i ušutkaju pobunjenike, kako bi elemente iskoristila za oružje masovnog uništenja i alate kontrole, a ne za lijek."),
            t("Between waves, a corrupt broker called the Middleman trades with both sides, purely for his own benefit. Which side he leans towards depends on how you play. Conquer every island and finish the cure to win.",
              "Između talasa, korumpirani posrednik zvani Middleman trguje s obje strane, isključivo za vlastitu korist. Na čiju stranu se priklanja zavisi od toga kako igraš. Osvoji sva ostrva i završi lijek da pobijediš."),
        ],
        "built": [
            t("Wrote the full game design document, then implemented the game from it.",
              "Napisao kompletan dizajn dokument igre, a zatim igru napravio po njemu."),
            t("Hex-grid maps based on the Catlike Coding hex map tutorial, extended with liquid sources (Vulcanex, Hydronium) and ores that towers react to.",
              "Mape na heksagonalnoj mreži zasnovane na Catlike Coding tutorijalu, proširene izvorima tečnosti (Vulcanex, Hydronium) i rudama na koje tornjevi reaguju."),
            t("Six attack behaviours (single target, splash, cone, pierce, mortar, all-around) on Cannon, Syringe and Mortar bases, each with seven elemental variants and three upgrade tiers.",
              "Šest načina napada (jedna meta, splash, konus, probijanje, minobacač, napad oko sebe) na bazama Cannon, Syringe i Mortar, svaka sa sedam elementarnih varijanti i tri nivoa nadogradnje."),
            t("Four support towers: the Spotter pulses to reveal camouflaged enemies, the Deceiver sends enemies down a different branch at path forks, the Extraction Beacon harvests ore from neighbouring tiles, and the Attacher clips onto another tower and gives it an element-specific buff.",
              "Četiri pomoćna tornja: Spotter otkriva kamuflirane neprijatelje, Deceiver šalje neprijatelje drugom granom na račvanjima puta, Extraction Beacon vadi rudu sa susjednih polja, a Attacher se veže na drugi toranj i daje mu pojačanje prema elementu."),
            t("Seven enemy classes with their own rules and twelve named designs, from Patrol Drones and Hazmat Grunts to Cloaked Enforcers, Roller Echoes and the Nexium Abomination. Camo enemies need a Spotter, disruptors slow or lock down towers, decoys split on death, thieves drain your elements, and every enemy has an elemental weakness.",
              "Sedam klasa neprijatelja sa vlastitim pravilima i dvanaest imenovanih dizajna, od Patrol Dronova i Hazmat Grunta do Cloaked Enforcera, Roller Echoa i Nexium Abominationa. Kamuflirane otkriva Spotter, ometači usporavaju ili gase tornjeve, mamci se dijele nakon smrti, lopovi crpe elemente, a svaki neprijatelj ima elementarnu slabost."),
            t("Two win types. Survive every wave for an Attrition win, or push the Research Lab to its top tier before the waves run out for a Turbo win. The win type decides what you get: an Attrition win banks your leftover liquids into the permanent Nexium Codex, while a Turbo win opens the bribe shop, where those liquids buy bonuses for the next level.",
              "Dva tipa pobjede. Preživi sve talase za Attrition pobjedu, ili podigni Research Lab na najviši nivo prije kraja talasa za Turbo pobjedu. Tip pobjede određuje nagradu: Attrition ulaže preostale tečnosti u trajni Nexium Codex, a Turbo otvara prodavnicu mita u kojoj te tečnosti kupuju bonuse za sljedeći nivo."),
            t("A campaign map of levels with prerequisites that unlock the next ones, a wave system built from mini-waves, and an auto-assign that finds the best crew-to-department match.",
              "Kampanja sa nivoima koji se otključavaju preduslovima, sistem talasa složen od mini-talasa i automatsko raspoređivanje ekipe koje traži najbolji odnos člana i odjela."),
            t("Elemental upgrades that check neighbouring hex tiles, and a toxicity system with five stages. Elemental towers add to it every time they fire. At Critical, towers start to misfire; at Meltdown, tiles get contaminated; at Rapture, tanks are drained, a tower slot is contaminated and the whole crew takes a stress hit. Maintenance crew slow it down and vent it faster.",
              "Elementarne nadogradnje koje provjeravaju susjedna polja i sistem toksičnosti s pet faza. Elementarni tornjevi ga povećavaju pri svakom ispaljivanju. Na Critical tornjevi počinju zakazivati, na Meltdown se polja zagađuju, a na Rapture se prazne rezervoari, zagađuje se jedno polje za toranj i cijela ekipa dobija stres. Ekipa za održavanje ga usporava i brže ispušta."),
            t("The Middleman shows three offers between waves: a single card, a pack, and either a risk card or a logistics card. Cards come in five types (Blueprint, Tactical, Logistics, Crew Management and Risk) and three tiers. Packs come as Blueprint Crates, Supply and Crew Manifests and Black Market Tactical Stashes, and you pick from what is inside.",
              "Posrednik između talasa nudi tri ponude: jednu kartu, jedan paket i rizičnu ili logističku kartu. Karte su pet tipova (Blueprint, Tactical, Logistics, Crew Management i Risk) u tri nivoa. Paketi su Blueprint Crate, Supply and Crew Manifest i Black Market Tactical Stash, a iz njih biraš ponuđeno."),
            t("His loyalty runs from 0 to 100, starts at 50 each run and sets how good and how expensive the offers are. It moves with almost everything you do: taking a card, rejecting a risk card, refreshing the offers, or leaving without buying. High loyalty also unlocks the best bribes.",
              "Njegova lojalnost ide od 0 do 100, svaku partiju počinje na 50 i određuje koliko su ponude dobre i skupe. Mijenja se skoro svakom odlukom: uzimanjem karte, odbijanjem rizične karte, osvježavanjem ponuda ili odlaskom bez kupovine. Visoka lojalnost otključava i najbolje mito."),
            t("A crew of scientists, each rated 1 to 5 stars in science, maintenance and defence, with three work slots and a rest slot. The Research slot runs the Research Lab, and with nobody in it, research and harvesting stop. Maintenance cuts toxicity build-up and speeds up venting. Defence runs the attack towers. How strong each slot is depends on who you put in it. Stress and burnout lower a member's performance, and an auto-assign finds the best placement.",
              "Ekipa naučnika, svaki ocijenjen od 1 do 5 zvjezdica u nauci, održavanju i odbrani, s tri radna mjesta i jednim mjestom za odmor. Research mjesto upravlja laboratorijom, a bez nikoga u njemu istraživanje i vađenje staju. Održavanje smanjuje rast toksičnosti i ubrzava ispuštanje. Odbrana pokreće napadačke tornjeve. Jačina svakog mjesta zavisi od toga ko je u njemu. Stres i izgaranje smanjuju učinak člana, a automatski raspored nalazi najbolji smještaj."),
            t("XP and a skill tree, the Nexium Codex for permanent unlocks, and save/load.",
              "XP i stablo vještina, Nexium Codex za trajna otključavanja i snimanje igre."),
        ],
        "numbers": [
            ("156", t("C# scripts", "C# skripti")),
            ("~16,000", t("lines of code", "linija koda")),
            ("4", t("support towers", "pomoćna tornja")),
            ("7", t("enemy classes", "klasa neprijatelja")),
            ("7", t("elements, all made from Nexium", "elemenata, svi od Nexiuma")),
            ("5", t("card types in the draft", "tipova karata u izboru")),
        ],
        "wip": t(
            "ArcaneTD is a work in progress. The systems described here are implemented, but the interface and art are still placeholders and will be replaced as the game gets its real UI. The screenshots show the current state.",
            "ArcaneTD je projekat u izradi. Sistemi opisani ovdje su implementirani, ali su interfejs i grafika još privremeni i bit će zamijenjeni kada igra dobije pravi UI. Slike prikazuju trenutno stanje."),
        "cover_image": "assets/arcanetd/hex-action.jpg",
        "media": [
            {"src": "assets/arcanetd/hex-action.jpg",
             "alt": t("Towers on the hex map firing at enemies, with grass, water and a lava river around them", "Tornjevi na heksagonalnoj mapi gađaju neprijatelje, s travom, vodom i rijekom lave oko njih"),
             "caption": t("Towers defending a path on the hex map. HUD hidden for this shot.", "Tornjevi brane put na heksagonalnoj mapi. HUD je sakriven za ovaj snimak.")},
            {"video": "assets/arcanetd/field-retrofit.mp4", "poster": "assets/arcanetd/field-retrofit-poster.jpg",
             "alt": t("A tower being changed through the Field Retrofit panel", "Toranj koji se mijenja kroz Field Retrofit panel"),
             "caption": t("A Field Retrofit, 8 seconds. The panel uses placeholder art.", "Field Retrofit, 8 sekundi. Panel koristi privremenu grafiku.")},
            {"src": "assets/arcanetd/hex-lava.jpg",
             "alt": t("A lava river (Vulcanex) crossing the hex map, with the game HUD around it", "Rijeka lave (Vulcanex) koja prelazi heksagonalnu mapu, s HUD-om igre oko nje"),
             "caption": t("A Vulcanex lava source on the map. Placeholder HUD.", "Izvor lave Vulcanex na mapi. Privremeni HUD.")},
            {"src": "assets/arcanetd/middleman.jpg",
             "alt": t("The Middleman's three offers between waves: a Tactical card, a Supply and Crew Manifest pack and a Logistics card", "Posrednikove tri ponude između talasa: Tactical karta, paket Supply and Crew Manifest i Logistics karta"),
             "caption": t("The Middleman draft between waves. Card names and text are test data.", "Posrednikov izbor između talasa. Nazivi i tekstovi karata su testni podaci.")},
            {"src": "assets/arcanetd/crew.jpg",
             "alt": t("The crew screen with three scientists rated in science, defence and maintenance, and the work slots", "Ekran ekipe s tri naučnika ocijenjena u nauci, odbrani i održavanju, i radnim mjestima"),
             "caption": t("Crew management: ratings, work slots and a detox slot. Work-in-progress UI.", "Upravljanje ekipom: ocjene, radna mjesta i mjesto za detoksikaciju. UI u izradi.")},
        ],
        "diagrams": ["arcane_loop", "arcane_elements", "arcane_loyalty", "arcane_crew"],
    },
    {
        "slug": "psychocat",
        "name": "Psychocat",
        "theme": "psycho",
        "status": t("Early development", "Rani razvoj"),
        "status_kind": "early",
        "hook": t("Hitman, but you are the family cat, and nobody suspects you.",
                  "Hitman, ali ti si porodična mačka i niko ne sumnja u tebe."),
        "summary": t(
            "A 3D third-person stealth sandbox set in one house. You play a secretly evil house cat who builds chain-reaction pranks so the family believes the house is haunted, while every objective pushes toward a bigger goal. A new Unity project started in October 2026.",
            "3D stealth sandbox iz trećeg lica smješten u jednoj kući. Igraš tajno zlu kućnu mačku koja pravi lančane podvale kako bi porodica povjerovala da je kuća uklet, a svaki zadatak vodi ka većem cilju. Novi Unity projekt započet u oktobru 2026."),
        "tags": ["Unity (URP)", "C#", "Game design", "Stealth sandbox"],
        "facts": [t("Started October 2026", "Započeto u oktobru 2026."),
                  t("Playable gray-box prototype", "Igriv prototip bez grafike"),
                  t("Full design document written", "Napisan cijeli dizajn dokument")],
        "role": t("Solo developer and designer", "Samostalni developer i dizajner"),
        "timeline": t("October 2026 onwards", "Od oktobra 2026."),
        "platforms": t("PC first, controller support later", "Prvo PC, podrška za kontroler kasnije"),
        "stack": "Unity (URP), C#",
        "links": [(t("Showcase on GitHub (code is private)", "Prikaz na GitHubu (kod je privatan)"), "https://github.com/harunkestendzic/psychocat-showcase")],
        "idea": t(
            "The player plans first, then watches the plan play out. Every action gets a reaction from the world, and the reaction is where the humour comes from, from slapstick to darker themes like a planted lipstick mark that ends a marriage. "
            "The cat can always read who is where and what is risky, and nobody suspects it, except in the places a cat does not belong. Failure costs position or time, never injury, and the family dog, Biscuit, is never harmed.",
            "Igrač prvo planira, a zatim gleda kako se plan odigrava. Svaka radnja dobija odgovor svijeta, a taj odgovor je izvor humora, od slapsticka do mračnijih tema, poput podmetnutog traga ruža koji okončava brak. "
            "Mačka uvijek može pročitati ko je gdje i šta je rizično, i niko ne sumnja u nju, osim na mjestima gdje mačka ne pripada. Neuspjeh košta poziciju ili vrijeme, nikad povrede, a porodični pas Biscuit nikad nije povrijeđen."),
        "built": [t("Built a first playable prototype in five days (5 to 9 October 2026): a cat that runs, crouches under furniture, climbs where a paw prompt shows it can, walks thin beams and hides, in a small house with a family on a clock.",
                    "Napravio prvi igrivi prototip za pet dana (5. do 9. oktobra 2026.): mačka koja trči, čučne ispod namještaja, penje se gdje joj to pokaže znak šape, hoda po uskim gredama i krije se, u maloj kući s porodicom na satu."),
                  t("Family members that follow schedules from 7:00 to 21:00 on a game clock, so a day plays out the same way every time. Pressing F freezes the day into a planning view with each person's route, see-through ghosts of where they will be, and a timeline you can scrub.",
                    "Članovi porodice koji slijede raspored od 7:00 do 21:00 na igračkom satu, pa se dan uvijek odigra isto. Tipka F zamrzava dan u pregled planiranja s rutom svake osobe, prozirnim sjenama gdje će biti i vremenskom linijom koju možeš premotavati."),
                  t("Two chains of cause and effect: push a vase while Biscuit lies beside it and Mom blames him, or drag a slipper into the dog bed so Dad finds it chewed. Who gets blamed depends on who is where, and the prototype had five endings.",
                    "Dva lanca uzroka i posljedica: gurni vazu dok Biscuit leži pored nje i mama krivi njega, ili odvuci papuču u pseći krevet da je tata nađe izgrižen. Ko je kriv zavisi od toga ko je gdje, a prototip je imao pet završetaka."),
                  t("Vision cones for every person, shown while planning. Being seen doing something guilty raises suspicion, and at the first stage Mom moves the vase out of reach.",
                    "Vidno polje za svaku osobu, prikazano tokom planiranja. Ako te neko vidi dok radiš nešto sumnjivo, raste sumnja, a na prvom stepenu mama pomjera vazu van dosega."),
                  t("Then redesigned it. The game design document is written, with four design pillars, the cast, and a Level 1 plan with eight paths on paper and five picked for the first slice.",
                    "Zatim sam ga redizajnirao. Dizajn dokument igre je napisan, s četiri stuba dizajna, likovima i planom Nivoa 1 s osam puteva na papiru, od kojih je pet odabrano za prvi dio."),
                  t("Rebuilt the base for the real game: a two-floor house with a front yard, side passage and back garden, built from a written map of rooms, doors and furniture, with a continuous clock and world state kept as data.",
                    "Obnovio sam osnovu za pravu igru: kuću na dva sprata s prednjim dvorištem, bočnim prolazom i zadnjom baštom, izgrađenu iz napisane mape soba, vrata i namještaja, s kontinuiranim satom i stanjem svijeta u podacima."),
                  t("New jump rules: up to 1.5 m from standing, 2.0 m across a gap, 2.0 m down, and a bit more beside the tree trunk. You aim a jump with the camera, and cat-only routes (a gap behind the shelves, a pipe, a tree branch to a window, a dumbwaiter) are climbed hop by hop.",
                    "Nova pravila skoka: do 1,5 m iz stojećeg stava, 2,0 m preko procjepa, 2,0 m naniže i malo više pored debla. Skok ciljaš kamerom, a putevi samo za mačku (procjep iza polica, cijev, grana drveta do prozora, lift za posluživanje) penju se skok po skok.")],
        "numbers": [("4", t("design pillars", "stuba dizajna")),
                    ("8", t("paths designed for Level 1", "puteva osmišljeno za Nivo 1")),
                    ("5", t("paths in the first slice", "puteva u prvom dijelu"))],
        "highlight_h": t("Plan", "Plan"),
        "highlight": t("Build the first playable slice of Level 1: the house, the family routine from 7:00 to 21:00 and five paths. Playtest it until it is fun, then decide how far to grow. An art style test comes before the content is finished.",
                       "Napraviti prvi igrivi dio Nivoa 1: kuću, porodični raspored od 7:00 do 21:00 i pet puteva. Testirati ga dok ne bude zabavan, pa odlučiti koliko dalje rasti. Test vizuelnog stila dolazi prije nego se sadržaj završi."),
        "code": None,
        "wip": t(
            "Psychocat is at an early stage, and the name is a working title. Everything on this page is gray-box: plain blocks, no art yet. It shows how the game plays, not how it will look.",
            "Psychocat je u ranoj fazi, a ime je radni naslov. Sve na ovoj stranici je bez grafike: obični blokovi, još bez umjetničkog dijela. Pokazuje kako se igra igra, ne kako će izgledati."),
        "cover_image": "assets/psychocat/house-overview.jpg",
        "media": [
            {"video": "assets/psychocat/tree-branch.mp4", "poster": "assets/psychocat/tree-branch.jpg",
             "alt": t("The cat walking a tree branch towards a window of the house", "Mačka koja hoda po grani drveta prema prozoru kuće"),
             "caption": t("A cat-only route: the tree branch to Leo's window.", "Put samo za mačku: grana drveta do Leovog prozora.")},
            {"video": "assets/psychocat/planning-view.mp4", "poster": "assets/psychocat/planning-view.jpg",
             "alt": t("The planning view with routes, ghosts of family members and a timeline", "Pregled planiranja s rutama, sjenama članova porodice i vremenskom linijom"),
             "caption": t("The planning view: the day is frozen and you scrub the timeline.", "Pregled planiranja: dan je zamrznut i premotavaš vremensku liniju.")},
            {"video": "assets/psychocat/vase-chain.mp4", "poster": "assets/psychocat/vase-chain.jpg",
             "alt": t("A vase falls, Biscuit barks, and Mom blames the dog", "Vaza pada, Biscuit laje, a mama krivi psa"),
             "caption": t("A chain: the vase falls, Biscuit barks and Mom blames the dog.", "Lanac: vaza pada, Biscuit laje i mama krivi psa.")},
            {"video": "assets/psychocat/slipper-chain.mp4", "poster": "assets/psychocat/slipper-chain.jpg",
             "alt": t("A slipper dragged into the dog bed and found chewed by Dad", "Papuča odvučena u pseći krevet koju tata nalazi izgrižen"),
             "caption": t("A second chain: the slipper goes into the dog bed and Dad finds it chewed.", "Drugi lanac: papuča ide u pseći krevet i tata je nalazi izgrižen.")},
            {"video": "assets/psychocat/vision.mp4", "poster": "assets/psychocat/vision.jpg",
             "alt": t("Mom's vision cone in the planning view, then the push while she watches", "Momino vidno polje u pregledu planiranja, pa guranje dok ona gleda"),
             "caption": t("Vision cones: being seen doing something guilty raises suspicion.", "Vidna polja: ako te vide dok radiš nešto sumnjivo, raste sumnja.")},
            {"video": "assets/psychocat/house-flyover.mp4", "poster": "assets/psychocat/house-flyover.jpg",
             "alt": t("A flight around the new two-floor house and garden", "Let oko nove kuće na dva sprata i bašte"),
             "caption": t("The rebuilt house, from the front yard to the back garden.", "Obnovljena kuća, od prednjeg dvorišta do zadnje bašte.")},
            {"src": "assets/psychocat/house-overview.jpg",
             "alt": t("The two-floor house from above, with the garage, the tree and the garden", "Kuća na dva sprata odozgo, s garažom, drvetom i baštom"),
             "caption": t("The Level 1 house from above, still gray-box.", "Kuća Nivoa 1 odozgo, još bez grafike.")},
        ],
        "diagrams": [],
    },
    {
        "slug": "vinyl-shop",
        "name": "Jugoton",
        "theme": "vinyl",
        "featured": False,
        "cover_photo": "assets/vinyl/home.jpg",
        "status": t("University project", "Univerzitetski projekt"),
        "status_kind": "uni",
        "hook": t("A working online vinyl shop with full CRUD, where the database itself guards stock, orders and addresses. Deployed live on Oracle Cloud.",
                  "Funkcionalna online prodavnica vinila s punim CRUD-om, u kojoj sama baza čuva zalihe, narudžbe i adrese. Postavljena uživo na Oracle Cloud."),
        "summary": t(
            "Built for two courses at once, Web Environments (CS270) and Database Systems (CS240), in a team of two, then deployed to Oracle Cloud for a third, Cloud Computing (CS260). "
            "Customers browse, search, filter by genre, preview tracks, review records and check out; admins add, edit and delete records and artists and read sales reports.",
            "Napravljeno za dva predmeta odjednom, Web okruženja (CS270) i Baze podataka (CS240), u timu od dvoje, a zatim postavljeno na Oracle Cloud za treći, Cloud Computing (CS260). "
            "Kupci pregledaju, pretražuju, filtriraju po žanru, preslušavaju pjesme, ocjenjuju ploče i kupuju; admini dodaju, mijenjaju i brišu ploče i izvođače i čitaju izvještaje o prodaji."),
        "tags": ["PHP", "MySQL", "JavaScript", "HTML/CSS", "Oracle Cloud", "Nginx"],
        "facts": [t("10 tables, 2 triggers, a view, a procedure and a function", "10 tabela, 2 okidača, pogled, procedura i funkcija"),
                  t("Deployed on an Oracle Cloud VM for CS260 Cloud Computing", "Postavljeno na Oracle Cloud VM za CS260 Cloud Computing")],
        "role": t("Full-stack developer, team of two (with Sajra Agić); cloud deployment done on my own",
                  "Full-stack developer, tim od dvoje (sa Sajrom Agić); postavljanje u cloud uradio sam samostalno"),
        "timeline": t("Spring 2026, SSST (CS270, CS240 and CS260), deployed June 2026", "Proljeće 2026., SSST (CS270, CS240 i CS260), postavljeno u junu 2026."),
        "platforms": t("Responsive web app", "Responzivna web aplikacija"),
        "stack": "PHP, HTML, CSS, JavaScript, MySQL/MariaDB, phpMyAdmin, iTunes Search API, Oracle Cloud Object Storage, GitHub; deployment: Oracle Cloud Infrastructure, Ubuntu 24, Nginx, PHP 8.4-FPM, Oracle Autonomous Database, OCI8",
        "links": [(t("Source on GitHub", "Kod na GitHubu"), "https://github.com/harunkestendzic/jugoton-vinyl-shop")],
        "cloud": {
            "h": t("Deploying it to Oracle Cloud (CS260 Cloud Computing)", "Postavljanje na Oracle Cloud (CS260 Cloud Computing)"),
            "intro": t("For the Cloud Computing course (CS260), I took the same app live on Oracle Cloud Infrastructure on my own in June 2026. "
                       "It runs on an Ubuntu 24 virtual machine as a classic three-tier setup: Nginx serves the static files, PHP 8.4-FPM runs the PHP, and MySQL stores the data. "
                       "A copy of the database also lives in an Oracle Autonomous Database. The cloud server was a course deployment and may be taken down, so the video on this page shows the full flow.",
                       "Za predmet Cloud Computing (CS260) samostalno sam postavio istu aplikaciju uživo na Oracle Cloud Infrastructure u junu 2026. "
                       "Radi na Ubuntu 24 virtualnoj mašini kao klasična troslojna postavka: Nginx servira statične fajlove, PHP 8.4-FPM izvršava PHP, a MySQL čuva podatke. "
                       "Kopija baze nalazi se i u Oracle Autonomous Database. Cloud server je bio dio kursa i može biti ugašen, pa video na ovoj stranici prikazuje cijeli tok."),
            "steps_h": t("What I did", "Šta sam uradio"),
            "steps": [
                t("I connected to the VM over SSH, updated the system, and cloned the repository from GitHub into the Nginx web root, owned by the www-data user.",
                  "Spojio sam se na VM preko SSH-a, ažurirao sistem i klonirao repozitorij s GitHuba u Nginx web root, u vlasništvu korisnika www-data."),
                t("I wrote an Nginx server block that passes PHP files to PHP-FPM through a Unix socket.",
                  "Napisao sam Nginx server block koji PHP fajlove prosljeđuje PHP-FPM-u preko Unix socketa."),
                t("I installed MySQL, created the vinyl_shop database and a dedicated user, and imported the project's SQL export.",
                  "Instalirao sam MySQL, napravio bazu vinyl_shop i posebnog korisnika i uvezao SQL export projekta."),
                t("I opened port 80 in the OCI security list and the VM firewall, and kept the MySQL port closed, so only the VM itself can reach the database.",
                  "Otvorio sam port 80 u OCI security listi i firewallu VM-a, a MySQL port ostavili zatvorenim, pa bazi može pristupiti samo sama VM."),
                t("I exported the data with mysqldump and rewrote the script by hand for Oracle (NUMBER instead of INT UNSIGNED, sequences instead of AUTO_INCREMENT, TO_DATE for dates), then loaded it into an Oracle Autonomous Database through SQL Developer Web.",
                  "Izvezao sam podatke s mysqldump i ručno prepravio skriptu za Oracle (NUMBER umjesto INT UNSIGNED, sekvence umjesto AUTO_INCREMENT, TO_DATE za datume), pa je učitao u Oracle Autonomous Database preko SQL Developer Weba."),
                t("I built the PHP OCI8 extension against the Oracle Instant Client, so PHP can connect to the Autonomous Database for syncing and reports.",
                  "Izgradio sam PHP ekstenziju OCI8 uz Oracle Instant Client, da se PHP može spojiti na Autonomous Database za sinhronizaciju i izvještaje."),
            ],
            "issues_h": t("What broke, and how I found it", "Šta se pokvarilo i kako sam to našao"),
            "issues": [
                t("Every page returned a 500 error. The Nginx error log showed PHP logging in to MySQL as a user that only existed only on our own machines, and index.php had a second hard-coded connection of its own. I fixed db.php, then found every other reference with grep.",
                  "Svaka stranica je vraćala grešku 500. Nginx error log je pokazao da se PHP prijavljuje u MySQL korisnikom koji je postojao samo na našim računarima, a index.php je imao i svoju drugu konekciju upisanu u kod. Popravio sam db.php, pa sve ostale reference pronašao s grep."),
                t("Some pages said tables like Artists didn't exist. MySQL on Windows ignores case in table names, MySQL on Linux doesn't. A sed replace that was too broad emptied several files. I restored them with git checkout and redid the fix with word-boundary patterns.",
                  "Neke stranice su javljale da tabele poput Artists ne postoje. MySQL na Windowsu ne razlikuje velika i mala slova u imenima tabela, a na Linuxu razlikuje. Preširoka zamjena sa sed ispraznila je nekoliko fajlova. Vratio sam ih s git checkout i ponovio popravku sa šablonima za granice riječi."),
                t("The OCI8 build couldn't find oci.h, and PHP-FPM couldn't load libclntsh.so. I pointed PECL at the Instant Client folder and made LD_LIBRARY_PATH available to the www-data user.",
                  "Build OCI8 nije mogao naći oci.h, a PHP-FPM nije mogao učitati libclntsh.so. PECL sam usmjerio na folder Instant Clienta i LD_LIBRARY_PATH učinio dostupnim korisniku www-data."),
            ],
            "prod_h": t("What a real production setup would change", "Šta bi prava produkcija promijenila"),
            "prod": t("One VM works for a course, not for real customers. Production would move the database to a managed service, put a load balancer in front of several app servers, serve everything over HTTPS, keep credentials in OCI Vault instead of in the code, and deploy through a CI/CD pipeline instead of by hand over SSH. "
                      "The biggest lesson was to read the logs: none of the real errors showed up in the browser.",
                      "Jedna VM je dovoljna za predmet, ali ne i za prave kupce. Produkcija bi bazu prebacila na upravljani servis, postavila load balancer ispred više aplikacijskih servera, sve servirala preko HTTPS-a, čuvala pristupne podatke u OCI Vaultu umjesto u kodu i postavljala nove verzije kroz CI/CD pipeline umjesto ručno preko SSH-a. "
                      "Najveća lekcija je bila čitati logove: nijedna prava greška se nije vidjela u pregledniku."),
            "figs": [
                {"src": "assets/vinyl/oracle-autonomous-db.png",
                 "alt": t("Oracle SQL Developer Web listing the Jugoton tables in the Autonomous Database", "Oracle SQL Developer Web s listom Jugoton tabela u Autonomous Database"),
                 "caption": t("All project tables imported into the Oracle Autonomous Database.", "Sve tabele projekta uvezene u Oracle Autonomous Database.")},
                {"src": "assets/vinyl/nginx-error-log.png",
                 "alt": t("Nginx error log showing PHP failing to log in to MySQL", "Nginx error log u kojem PHP ne uspijeva da se prijavi u MySQL"),
                 "caption": t("The first clue: the Nginx error log behind the 500 errors.", "Prvi trag: Nginx error log iza grešaka 500.")},
            ],
        },
        "idea": t(
            "Vinyl is popular again, so we built Jugoton, a record shop named after and styled like the old Yugoslav record label: dark, with orange accents. "
            "The project had to satisfy two courses, so it is a complete web app and a properly designed database at the same time. "
            "We started from written business rules, built the ER model and normalised it before writing application code.",
            "Vinili su ponovo popularni, pa smo napravili Jugoton, prodavnicu ploča nazvanu i stilizovanu po staroj jugoslavenskoj izdavačkoj kući: tamna, s narandžastim detaljima. "
            "Projekt je morao zadovoljiti dva predmeta, pa je istovremeno kompletna web aplikacija i pravilno dizajnirana baza. "
            "Krenuli smo od napisanih poslovnih pravila, napravili ER model i normalizovali ga prije pisanja koda aplikacije."),
        "built": [
            t("Responsive front end in plain HTML, CSS and JavaScript, no frameworks, with a record-shaped menu button.",
              "Responzivan front end u čistom HTML-u, CSS-u i JavaScriptu, bez frameworka, s dugmetom menija u obliku ploče."),
            t("Catalogue with new arrivals, search by title or artist, genre filtering with paging, and record pages with an iTunes track preview.",
              "Katalog s novim pločama, pretraga po naslovu ili izvođaču, filtriranje po žanru sa stranicama i stranice ploča s iTunes pregledom pjesama."),
            t("Registration and login with hashed passwords and sessions, a profile with account balance, and separate customer and admin areas.",
              "Registracija i prijava s heširanim lozinkama i sesijama, profil sa stanjem računa i odvojeni dijelovi za kupce i admine."),
            t("Side cart, checkout that lowers balance and stock in one transaction, and reviews (one per user and record, updated in a single query).",
              "Bočna korpa, plaćanje koje u jednoj transakciji umanjuje stanje i zalihu i recenzije (jedna po korisniku i ploči, ažurirane jednim upitom)."),
            t("Admin panel with full CRUD for records and artists, inventory, and reports: best sellers, most valuable customers, latest orders.",
              "Admin panel s punim CRUD-om za ploče i izvođače, zalihama i izvještajima: najprodavanije, najvredniji kupci, posljednje narudžbe."),
            t("New records are filled in automatically from the iTunes Search API (release date, preview ID, genre); cover images live in Oracle Cloud Object Storage.",
              "Nove ploče se automatski popunjavaju iz iTunes Search API-ja (datum izdanja, ID pregleda, žanr); omoti su u Oracle Cloud Object Storageu."),
            t("MySQL database: 10 tables, 30+ business rules, 4 indexes, a sales analytics view, an order procedure, a customer tier function and 2 triggers.",
              "MySQL baza: 10 tabela, 30+ poslovnih pravila, 4 indeksa, pogled za analitiku prodaje, procedura za narudžbe, funkcija za nivo kupca i 2 okidača."),
        ],
        "numbers": [
            ("10", t("tables", "tabela")),
            ("30+", t("business rules", "poslovnih pravila")),
            ("2", t("triggers, plus a view, procedure and function", "okidača, plus pogled, procedura i funkcija")),
            ("4", t("indexes for search and reports", "indeksa za pretragu i izvještaje")),
        ],
        "highlight_h": t("Technical highlight: letting the database enforce the rules", "Tehnički detalj: baza provodi pravila"),
        "highlight": t(
            "Some rules are too important to leave to application code. A trigger stops any order item that asks for more copies than are in stock, "
            "and a second trigger keeps exactly one default address per user. Placing an order runs through a stored procedure as a single transaction: "
            "it checks the record and the stock, creates the order, adds the item and lowers the stock, and rolls everything back if one step fails. "
            "The next step we planned is moving every query to prepared statements.",
            "Neka pravila su previše bitna da bi se prepustila kodu aplikacije. Okidač zaustavlja svaku stavku narudžbe koja traži više primjeraka nego što ima na zalihi, "
            "a drugi okidač čuva tačno jednu zadanu adresu po korisniku. Narudžba ide kroz pohranjenu proceduru kao jedna transakcija: "
            "provjerava ploču i zalihu, pravi narudžbu, dodaje stavku i umanjuje zalihu, a ako jedan korak ne uspije, sve vraća nazad. "
            "Sljedeći planirani korak je prebacivanje svih upita na prepared statements."),
        "code": {
            "file": "tr_verify_vinyl_stock.sql",
            "body": """CREATE TRIGGER tr_verify_vinyl_stock
BEFORE INSERT ON Order_Items FOR EACH ROW
BEGIN
  DECLARE current_stock INT;
  SELECT stock INTO current_stock FROM Vinyls WHERE vinyl_id = NEW.vinyl_id;
  IF current_stock < NEW.quantity THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Transaction aborted: Insufficient vinyl inventory available.';
  END IF;
END""",
            "note": t("From the project report. The trigger runs before every order item is saved.",
                      "Iz izvještaja projekta. Okidač se pokreće prije snimanja svake stavke narudžbe."),
        },
        "er_image": {"src": "assets/vinyl/er-diagram.png",
                     "title": t("Entity relationship diagram", "Dijagram entiteta i veza"),
                     "caption": t("The final schema: ten tables, including the Vinyl_Genres link table for the many-to-many relationship.",
                                  "Konačna šema: deset tabela, uključujući veznu tabelu Vinyl_Genres za vezu više-prema-više.")},
        "media": [
            {"video": "assets/vinyl/demo.mp4", "poster": "assets/vinyl/demo-poster.jpg",
             "alt": t("Screen recording: an admin adds a record, the iTunes Search API fills in the details, and the record appears in the shop with its cover and a preview player",
                      "Snimak ekrana: admin dodaje ploču, iTunes Search API popunjava podatke, a ploča se pojavljuje u prodavnici s omotom i pregledom pjesama"),
             "caption": t("Adding a record as an admin. Choosing the artist triggers an iTunes Search API lookup that fills in the release date and iTunes ID, and the cover art is fetched on save. Then the record page with its 30-second preview and reviews. Slow parts are sped up (the label shows the speed).",
                          "Dodavanje ploče kao admin. Odabir izvođača pokreće upit prema iTunes Search API-ju koji popunjava datum izlaska i iTunes ID, a omot se preuzima pri snimanju. Zatim stranica ploče s pregledom od 30 sekundi i recenzijama. Spori dijelovi su ubrzani (oznaka prikazuje brzinu).")},
            {"src": "assets/vinyl/latest.jpg", "alt": t("Jugoton home page with the latest records", "Početna stranica Jugotona s najnovijim pločama"), "caption": t("Home page: the latest records, and the record-shaped menu button.", "Početna: najnovije ploče i dugme menija u obliku ploče.")},
            {"src": "assets/vinyl/record.jpg", "alt": t("A record page with the iTunes player and track list", "Stranica ploče s iTunes plejerom i listom pjesama"), "caption": t("Record page with a 30-second preview through the iTunes embed.", "Stranica ploče s pregledom od 30 sekundi preko iTunes embeda.")},
            {"src": "assets/vinyl/genres.jpg", "alt": t("Genre filter page", "Stranica za filtriranje po žanru"), "caption": t("Genres page. A record can belong to several genres.", "Stranica žanrova. Ploča može pripadati više žanrova.")},
            {"src": "assets/vinyl/search.jpg", "alt": t("Search results for an artist", "Rezultati pretrage za izvođača"), "caption": t("Search by album title or artist name.", "Pretraga po nazivu albuma ili imenu izvođača.")},
            {"src": "assets/vinyl/cart.jpg", "alt": t("The side cart with a record and the total", "Bočna korpa s pločom i ukupnom cijenom"), "caption": t("The cart opens on the side, with quantity and total.", "Korpa se otvara sa strane, s količinom i ukupnom cijenom.")},
            {"src": "assets/vinyl/reviews.jpg", "alt": t("Review form and customer reviews", "Forma za recenziju i recenzije kupaca"), "caption": t("Reviews: rating required, comment optional, one per user and record.", "Recenzije: ocjena obavezna, komentar nije, jedna po korisniku i ploči.")},
            {"src": "assets/vinyl/admin.jpg", "alt": t("Admin dashboard with best sellers, top customers and latest orders", "Admin panel s najprodavanijim pločama, najboljim kupcima i posljednjim narudžbama"), "caption": t("Admin dashboard: best sellers, top customers, latest orders and inventory.", "Admin panel: najprodavanije ploče, najbolji kupci, posljednje narudžbe i zalihe.")},
            {"src": "assets/vinyl/report.jpg", "alt": t("Top-selling records report", "Izvještaj o najprodavanijim pločama"), "caption": t("Sales report, read from a database view.", "Izvještaj o prodaji, čitan iz pogleda (view) u bazi.")},
            {"src": "assets/vinyl/add-record.jpg", "alt": t("Form for adding a new record", "Forma za dodavanje nove ploče"), "caption": t("Adding a record. Details are filled in from the iTunes Search API.", "Dodavanje ploče. Podaci se popunjavaju iz iTunes Search API-ja.")},
        ],
        "diagrams": ["vinyl_checkout"],
    },
]

OTHER_PROJECTS = [
    (t("Shop reports, player score analysis, workshop registrations", "Izvještaji trgovine, analiza golova igrača, prijave na radionice"), "Java",
     t("Three Java console programs from university: files, streams and threads.", "Tri Java konzolna programa s fakulteta: fajlovi, streamovi i niti.")),
    (t("JavaScript web apps", "JavaScript web aplikacije"), "JavaScript",
     t("Forkify (recipes, 12 modules), Mapty (workout map with Leaflet) and Bankist.",
       "Forkify (recepti, 12 modula), Mapty (mapa treninga s Leafletom) i Bankist.")),
]

EXPERIENCE = [
    {"role": t("AI Internship, Backend AI Engineering track", "AI praksa, smjer Backend AI Engineering"), "org": "FlyRank",
     "dates": t("Oct 2026 to now", "okt. 2026. do danas"),
     "points": [
         t("A remote, self-paced internship programme that I do part-time alongside my studies.",
           "Online praksa vlastitim tempom, koju radim pored studija."),
         t("Learning to build RAG systems, AI agents and APIs with the Claude API and MCP, with expert feedback and a capstone project.",
           "Učim praviti RAG sisteme, AI agente i API-je uz Claude API i MCP, s povratnim informacijama mentora i završnim projektom."),
     ]},
    {"role": t("Web Developer", "Web developer"), "org": "Orior Media",
     "dates": t("2025", "2025."),
     "points": [
         t("Orior Media (oriormedia.com) is a digital agency in Chandler, Arizona. I worked in a team of two on projects for its client JR Services, a logistics outsourcing company with offices in Sarajevo, Phoenix and Dubai.",
           "Orior Media (oriormedia.com) je digitalna agencija iz Chandlera u Arizoni. Radio sam u timu od dvoje na projektima za njihovog klijenta JR Services, firmu za outsourcing u logistici s uredima u Sarajevu, Phoenixu i Dubaiju."),
         t("Built their WordPress website, including the careers and job location pages (joyrideservices.com).",
           "Napravio njihovu WordPress stranicu, uključujući stranice za karijeru i lokacije poslova (joyrideservices.com)."),
         t("Built parts of an applicant tracking system for truck-driver recruitment: the React and TypeScript frontend with Tailwind, and the Node.js and Express API on PostgreSQL. The system was planned to pull leads from Facebook Lead Ads into a Kanban pipeline; it was partly built.",
           "Napravio dijelove sistema za praćenje kandidata za zapošljavanje vozača kamiona: React i TypeScript frontend s Tailwindom te Node.js i Express API nad PostgreSQL bazom. Sistem je planiran da preuzima kandidate iz Facebook Lead Ads oglasa u Kanban tok; djelimično je napravljen."),
     ]},
    {"role": t("Junior Game Developer", "Junior Game Developer"), "org": "Alchemy Studio",
     "dates": t("Nov 2024 to Aug 2025", "nov. 2024. do avg. 2025."),
     "points": [
         t("Built the full interface of an in-game computer for a simulation game: a mock Linux-style operating system with windows and apps.",
           "Napravio kompletan interfejs računara unutar igre za simulacijsku igru: lažni operativni sistem u stilu Linuxa, s prozorima i aplikacijama."),
         t("Implemented a shop for computer parts, a PC crafting system, time management for in-game PCs and an item placement system.",
           "Implementirao prodavnicu dijelova, sistem sklapanja računara, upravljanje vremenom na računarima u igri i sistem postavljanja predmeta."),
         t("Worked in an AI-assisted workflow, about half of the code written with Claude, reviewed and integrated by me.",
           "Radio uz pomoć AI alata, oko polovine koda napisano s Claudeom, a ja sam ga pregledao i uklopio."),
         t("Received a written recommendation from the studio's founder and CEO.",
           "Dobio pismenu preporuku od osnivača i direktora studija."),
     ]},
    {"role": t("Graphic Designer", "Grafički dizajner"), "org": "Aktuelno Design",
     "dates": t("Oct 2023 to May 2025", "okt. 2023. do maj 2025."),
     "points": [t("Designed visuals for social media stories and posts, and added and updated products on client WordPress websites.",
                  "Dizajnirao vizuale za objave i storyje na društvenim mrežama te dodavao i ažurirao proizvode na WordPress stranicama klijenata.")]},
    {"role": t("Other work and volunteering", "Ostali poslovi i volontiranje"), "org": "",
     "dates": t("2022 to 2026", "2022. do 2026."),
     "points": [t("Driver at Vozzy (2026), bartender at L'Incontro (2023), volunteer at Sarajevo Film Festival and Omladinski Film Festival (2022).",
                  "Vozač u Vozzyju (2026.), barmen u L'Incontru (2023.), volonter na Sarajevo Film Festivalu i Omladinskom film festivalu (2022.).")]},
]

SKILLS = [
    (t("Unity and C#", "Unity i C#"), t("Main tools", "Glavni alati"),
     t("Ramo, ArcaneTD, Alchemy Studio", "Ramo, ArcaneTD, Alchemy Studio")),
    (t("Game design", "Dizajn igara"), "",
     t("ArcaneTD design document, Ramo", "ArcaneTD dizajn dokument, Ramo")),
    (t("Object-oriented programming, Java", "Objektno orijentisano programiranje, Java"), "",
     t("OOP course grade 9 (90/100, A-), Java console programs", "Ocjena 9 (90/100, A-) iz OOP-a, Java konzolni programi")),
    (t("Data structures and algorithms", "Strukture podataka i algoritmi"), "",
     t("Course grade 9 (87/100, A-), hex grid and pathing in ArcaneTD", "Ocjena 9 (87/100, A-), heksagonalna mreža i kretanje u ArcaneTD-u")),
    (t("SQL and databases", "SQL i baze podataka"), "",
     t("Database Systems grade 9 (88/100, A-), vinyl records database", "Ocjena 9 (88/100, A-) iz baza podataka, baza vinilnih ploča")),
    (t("Python and data", "Python i podaci"), "",
     t("Academy387 Python course, statistics", "Academy387 kurs Pythona, statistika")),
    (t("Web: JavaScript, HTML, CSS, WordPress", "Web: JavaScript, HTML, CSS, WordPress"), "",
     t("69-hour JavaScript course, Web Environments grade 9 (88/100, A-), Aktuelno Design", "Kurs JavaScripta od 69 sati, ocjena 9 (88/100, A-) iz web okruženja, Aktuelno Design")),
    (t("Node.js, React and TypeScript", "Node.js, React i TypeScript"), "",
     t("Applicant tracking system for JR Services (Orior Media)", "Sistem za praćenje kandidata za JR Services (Orior Media)")),
    (t("Tools and workflow", "Alati i način rada"), "",
     t("Git and GitHub, AI-assisted development with Claude, graphic design", "Git i GitHub, razvoj uz AI (Claude), grafički dizajn")),
]

EDUCATION = [
    {"school": t("Sarajevo School of Science and Technology (SSST)", "Sarajevo School of Science and Technology (SSST)"),
     "what": t("BSc Computer Science, minor in Electrical Engineering", "BSc računarske nauke, minor iz elektrotehnike"),
     "dates": t("2024 to 2028 (expected)", "2024. do 2028. (očekivano)"),
     "detail": t("GPA 8.58 out of 10 (81.75/100, B+). Highest grades, out of 10, with the grade out of 100 and the letter in brackets: "
                 "Programming and Problem Solving I 10 (95, A), Calculus 10 (94, A), Object-Oriented Programming 9 (90, A-), "
                 "Introduction to Computer Systems 9 (90, A-), Database Systems 9 (88, A-), Web Environments 9 (88, A-), "
                 "Data Structures and Algorithms 9 (87, A-).",
                 "Prosjek 8,58 od 10 (81,75/100, B+). Najviše ocjene, od 10, s ocjenom od 100 i slovnom ocjenom u zagradi: "
                 "Programiranje i rješavanje problema I 10 (95, A), Kalkulus 10 (94, A), Objektno orijentisano programiranje 9 (90, A-), "
                 "Uvod u računarske sisteme 9 (90, A-), Baze podataka 9 (88, A-), Web okruženja 9 (88, A-), "
                 "Strukture podataka i algoritmi 9 (87, A-).")},
    {"school": t("Četvrta gimnazija Ilidža", "Četvrta gimnazija Ilidža"),
     "what": t("High school, GPA 4.9 out of 5", "Gimnazija, prosjek 4,9 od 5"),
     "dates": t("2020 to 2024", "2020. do 2024."),
     "detail": t("Graduation project: The Development Process of a 2D Game from Beginning to End.",
                 "Maturski rad: Razvojni proces 2D igre od početka do kraja.")},
]

FORMER_NAME_NOTE = t("Issued under my former surname.", "Izdato na moje ranije prezime.")

# img: thumbnail; link: file opened on click (defaults to img); former: issued under former surname
AWARDS = [
    {"title": t("1st place, game programming", "1. mjesto, programiranje igara"), "sub": t("FIT Coding Challenge v.19, June 2026", "FIT Coding Challenge v.19, juni 2026."), "img": "assets/certs/fit-coding-challenge.jpg"},
    {"title": t("Certificate of Recognition, Professional Programming", "Priznanje, program Profesionalno programiranje"), "sub": t("Digital School, May 2024", "Digital School, maj 2024."), "img": "assets/certs/digital-school-recognition.jpg"},
    {"title": t("TOEFL iBT 100/120", "TOEFL iBT 100/120"), "sub": t("English language test, April 2024", "Test engleskog jezika, april 2024."), "img": "assets/certs/toefl-scores.jpg"},
    {"title": t("The Complete JavaScript Course (69 hours)", "The Complete JavaScript Course (69 sati)"), "sub": t("Udemy, May 2023", "Udemy, maj 2023."), "img": "assets/certs/udemy-javascript.jpg"},
    {"title": t("React Native programme, progress report", "React Native program, izvještaj o napretku"), "sub": t("Digital School, Oct 2022 to Mar 2023: 38 lessons, final project (PDF)", "Digital School, okt. 2022. do mar. 2023.: 38 lekcija, završni projekt (PDF)"), "img": "assets/certs/digital-school-react-native-report.jpg", "link": "assets/certs/digital-school-react-native-report.pdf", "former": True},
    {"title": t("Winter Academy", "Zimska akademija"), "sub": t("SSST, January 2024", "SSST, januar 2024."), "img": "assets/certs/ssst-winter-academy.jpg"},
    {"title": t("Podcast workshop, 4 weeks", "Radionica podcasta, 4 sedmice"), "sub": t("International Burch University, Apr to May 2022", "Internacionalni Burch univerzitet, apr. do maj 2022."), "img": "assets/certs/ibu-podcast-workshop.jpg", "former": True},
    {"title": t("Volunteer, 28th Sarajevo Film Festival", "Volonter, 28. Sarajevo Film Festival"), "sub": t("40 hours, August 2022", "40 sati, august 2022."), "img": "assets/certs/sff-volunteer.jpg", "former": True},
    {"title": t("Volunteer, 14th Omladinski Film Festival", "Volonter, 14. Omladinski film festival"), "sub": t("Sarajevo, 2022", "Sarajevo, 2022."), "img": "assets/certs/off-volunteer.jpg", "former": True},
    {"title": t("Photo school \"Moje kulturno blago\"", "Foto škola \"Moje kulturno blago\""), "sub": t("EU Info Centre in BiH, June 2021", "Info centar EU u BiH, juni 2021."), "img": "assets/certs/eu-photo-school.jpg", "former": True},
    {"title": t("Interactive Python Programming Course", "Interaktivni kurs programiranja u Pythonu"), "sub": t("Academy387, July 2020", "Academy387, juli 2020."), "img": "assets/certs/academy387-python.jpg", "former": True},
    {"title": t("Scholarship", "Stipendija"), "sub": t("Atlantbh, 2026", "Atlantbh, 2026.")},
    {"title": t("Participant", "Učesnik"), "sub": t("BEST Mostar Hackathon, 2025", "BEST Mostar Hackathon, 2025.")},
]

# ---------------------------------------------------------------- devlog
DEVLOG = []


# Long posts live in posts.py and get their own pages.
from posts import POSTS as LONG_POSTS
for _slug, _p in LONG_POSTS.items():
    DEVLOG.append({"slug": _slug, "date": _p["date"], "project": _p["project"], "title": _p["title"],
                   "body": _p["summary"], "long": True, "num": _p["num"], "text": _p["body"]})
