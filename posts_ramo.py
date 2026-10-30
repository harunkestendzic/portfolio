"""Ramo devlog posts. Same mini-markdown as posts.py."""

UPD_EN = """*This is the update post I published on itch.io after launch, expanded with what each change was in the project.*

[Screenshot: Ramo in a level after the update, with the new control buttons visible]

## Why an update

After Ramo went up on itch.io, the first players' feedback pointed at a few things: the controls, Ramo sticking to walls, and the balance of combat. On 10 October 2024, four days after the repository went public, I shipped one update for all of it.

## What changed

- **Clearer controls.** The input buttons were redrawn so it's obvious which key does what.
- **No more sticking to walls.** If you held a direction while jumping into a wall, Ramo stuck to it and didn't fall. The cause was friction. The player's Rigidbody2D had no physics material, so it used the default friction against the wall's side. The fix was a one-line change in the player prefab: a material called `Slip` with friction set to 0.
- **Combat balance.** Player bullets went from 1 to 1.5 damage. To keep the pistol from taking over, I removed four pistol pickups from the levels. The boss went from 15 to 20 health, so it now takes 14 shots instead of 15. The fight lasts about as long, but the player has fewer bullets to spare.
- **Needles fixed.** The syringe hazard's collider was a trigger, rotated at the wrong angle and much larger than the sprite, so players were hit by needles they never touched. It's now a solid collider on its own layer, sized and rotated to match the sprite.

```csharp
if(collision.tag == "Enemy" || collision.tag == "Boss" )
    collision.GetComponent<Health>().TakeDamage(1.5f);   // was 1
```

## What I learned

- The bugs that reached players were not code bugs. Three of the four fixes were data: a physics material, a collider shape and a few numbers in scenes.
- Balancing is a set of connected numbers. Raising damage meant removing pickups and raising boss health in the same update, or the fight would have become trivial.
- Players find what the developer stops seeing. I had played those levels so often that the wall-sticking no longer stood out to me.
"""

UPD_BS = """*Ovo je tekst o ažuriranju koji sam objavio na itch.io nakon izlaska, proširen onim što je svaka promjena bila u projektu.*

[Snimak ekrana: Ramo u nivou nakon ažuriranja, s vidljivim novim dugmadima za kontrole]

## Zašto ažuriranje

Nakon što je Ramo izašao na itch.io, povratne informacije prvih igrača ukazale su na nekoliko stvari: kontrole, Ramino lijepljenje za zidove i balans borbe. 10. oktobra 2024, četiri dana nakon što je repozitorij postao javan, objavio sam jedno ažuriranje za sve to.

## Šta se promijenilo

- **Jasnije kontrole.** Dugmad za unos su ponovo nacrtana, pa je očito koja tipka šta radi.
- **Nema više lijepljenja za zidove.** Ako bi držao smjer dok skačeš u zid, Ramo bi se zalijepio i ne bi padao. Uzrok je bilo trenje. Igračev Rigidbody2D nije imao fizički materijal, pa je koristio podrazumijevano trenje o bočnu stranu zida. Popravka je bila promjena jedne linije u prefabu igrača: materijal `Slip` s trenjem 0.
- **Balans borbe.** Igračevi meci su s 1 prešli na 1,5 štete. Da pištolj ne bi preuzeo igru, uklonio sam četiri pištolja iz nivoa. Boss je s 15 prešao na 20 zdravlja, pa sada treba 14 pogodaka umjesto 15. Borba traje otprilike isto, ali igrač ima manje metaka u rezervi.
- **Popravljene šprice.** Kolajder prepreke sa špricama bio je trigger, zarotiran pod pogrešnim uglom i mnogo veći od sprajta, pa su igrače pogađale šprice koje nikad nisu dodirnuli. Sada je čvrst kolajder na vlastitom sloju, veličine i rotacije usklađene sa sprajtom.

```csharp
if(collision.tag == "Enemy" || collision.tag == "Boss" )
    collision.GetComponent<Health>().TakeDamage(1.5f);   // was 1
```

## Šta sam naučio

- Greške koje su stigle do igrača nisu bile greške u kodu. Tri od četiri popravke bile su podaci: fizički materijal, oblik kolajdera i nekoliko brojeva u scenama.
- Balans je skup povezanih brojeva. Veća šteta značila je uklanjanje pištolja i više zdravlja za bossa u istom ažuriranju, inače bi borba postala trivijalna.
- Igrači nađu ono što developer prestane primjećivati. Te nivoe sam igrao toliko puta da mi lijepljenje za zidove više nije upadalo u oči.
"""

HAZ_EN = """[Screenshot: a level with a mine, barbed wire and a live electrical box close together]

## The idea

Most platformers use spikes and pits. Ramo is set in Sarajevo in spring 1992, so the hazards come from that setting instead: mines, barbed wire, live electrical boxes, discarded syringes, sniper fire from a high-rise and bombs falling from above. Each one had to be readable in pixel art, and fair for a player who sees it for the first time.

## One-hit hazards

Ramo has 5 health, and every hazard deals 5 damage. Touching any of them kills him, and he starts again from the last checkpoint. That decision shaped the levels more than any script did: hazards became puzzles about timing and positioning, and checkpoints had to sit right before each hard section.

## How a hazard sees the player

Most hazards use the same check. A box is cast in front of the object, its size set from the collider and a range value, and it hits only the player's layer. A gizmo draws the box in the editor, so I could tune each hazard's reach in the scene view.

```csharp
RaycastHit2D hit = Physics2D.BoxCast(
    boxCollider.bounds.center + transform.right * range * transform.localScale.x * colliderDistance,
    new Vector3(boxCollider.bounds.size.x * range, boxCollider.bounds.size.y, boxCollider.bounds.size.z),
    0, Vector2.left, 0, playerLayer);
```

[Screenshot: the red gizmo box of a hazard in the Unity scene view]

## Four kinds of timing

- **Always on:** mines and barbed wire. A mine explodes once when you step into its box, then disables itself.
- **On and off:** the electrical box switches between live and dead on a cooldown, with a looping buzz while it's live. You cross while it's dead.
- **On a timer:** the sniper fires every few seconds. It's paired with the Holiday Inn in the background, which flashes and plays the shot sound on its own cooldown. The player learns the rhythm from sound and light.
- **Random:** bombs drop from a point above the level at a random interval between a minimum and a maximum, so you can't memorise them. The bombs come from a small pool that is reused instead of creating new objects.

[Screenshot: the Holiday Inn flashing as the sniper fires]

## What went wrong

- **The same check, nine times.** The box-cast code above is copied into nine scripts: seven hazards and both enemy types. When I wanted to change it, I had to change it nine times.
- **Two timers that should be one.** The sniper and the Holiday Inn have separate cooldowns that only line up because I set them to the same value in the inspector.
- **The pools can steal.** When every bomb is in use, the pool returns the first one, so a bomb can disappear mid-air and reappear at the top. The projectile pool calls its search function twice per shot.

## What I'd change

- One `PlayerDetector` component with the box cast and gizmo, used by every hazard and enemy.
- One timer that drives both the warning and the shot.
- Pools that grow, or skip a shot, instead of recycling an active object.

## What I learned

- A hazard is mostly level design. The code is small, but placement, timing and checkpoints decide whether it feels fair.
- Copying code is fast for the second script and slow by the ninth.
"""

HAZ_BS = """[Snimak ekrana: nivo s minom, bodljikavom žicom i električnom kutijom blizu jedno drugog]

## Ideja

Većina platformera koristi šiljke i rupe. Ramo se dešava u Sarajevu u proljeće 1992, pa prepreke dolaze iz tog okruženja: mine, bodljikava žica, električne kutije pod naponom, bačene šprice, snajperska vatra s nebodera i bombe koje padaju odozgo. Svaka je morala biti čitljiva u pixel artu i fer prema igraču koji je vidi prvi put.

## Prepreke koje ubijaju odmah

Ramo ima 5 zdravlja, a svaka prepreka nanosi 5 štete. Dodir s bilo kojom ga ubija i on kreće ispočetka od posljednjeg checkpointa. Ta odluka je oblikovala nivoe više od ijedne skripte: prepreke su postale zagonetke o tajmingu i poziciji, a checkpointi su morali stajati odmah prije svakog teškog dijela.

## Kako prepreka vidi igrača

Većina prepreka koristi istu provjeru. Ispred objekta se baca kutija, čija veličina zavisi od kolajdera i vrijednosti dometa, i pogađa samo sloj igrača. Gizmo crta tu kutiju u editoru, pa sam domet svake prepreke mogao podesiti u prikazu scene.

```csharp
RaycastHit2D hit = Physics2D.BoxCast(
    boxCollider.bounds.center + transform.right * range * transform.localScale.x * colliderDistance,
    new Vector3(boxCollider.bounds.size.x * range, boxCollider.bounds.size.y, boxCollider.bounds.size.z),
    0, Vector2.left, 0, playerLayer);
```

[Snimak ekrana: crvena gizmo kutija prepreke u Unity prikazu scene]

## Četiri vrste tajminga

- **Uvijek aktivne:** mine i bodljikava žica. Mina eksplodira jednom kad uđeš u njenu kutiju, a zatim se isključi.
- **Pali-gasi:** električna kutija se na tajmer prebacuje između stanja pod naponom i bez napona, uz zujanje dok je pod naponom. Prelaziš kad je ugašena.
- **Na tajmer:** snajper puca svakih nekoliko sekundi. Uparen je s Holiday Innom u pozadini, koji bljesne i pusti zvuk pucnja na vlastiti tajmer. Igrač ritam uči iz zvuka i svjetla.
- **Nasumične:** bombe padaju s tačke iznad nivoa u nasumičnom intervalu između minimuma i maksimuma, pa ih ne možeš zapamtiti. Bombe dolaze iz malog poola koji se ponovo koristi umjesto pravljenja novih objekata.

[Snimak ekrana: Holiday Inn koji bljesne kad snajper puca]

## Šta je pošlo po zlu

- **Ista provjera, devet puta.** Kod s bacanjem kutije iznad kopiran je u devet skripti: sedam prepreka i obje vrste neprijatelja. Kad sam ga htio promijeniti, morao sam ga mijenjati devet puta.
- **Dva tajmera koja trebaju biti jedan.** Snajper i Holiday Inn imaju odvojene tajmere koji se poklapaju samo zato što sam im u inspektoru postavio istu vrijednost.
- **Poolovi mogu "ukrasti".** Kad su sve bombe u upotrebi, pool vrati prvu, pa bomba može nestati u zraku i pojaviti se gore. Pool projektila poziva funkciju za traženje dvaput po pucnju.

## Šta bih promijenio

- Jedna komponenta `PlayerDetector` s bacanjem kutije i gizmom, koju koriste sve prepreke i neprijatelji.
- Jedan tajmer koji pokreće i upozorenje i pucanj.
- Poolove koji rastu, ili preskoče pucanj, umjesto da recikliraju aktivan objekat.

## Šta sam naučio

- Prepreka je uglavnom dizajn nivoa. Kod je mali, ali postavljanje, tajming i checkpointi odlučuju da li djeluje fer.
- Kopiranje koda je brzo za drugu skriptu, a sporo za devetu.
"""

BOSS_EN = """[Screenshot: the boss mid-flight, with its curved route drawn as gizmos in the editor]

## The problem

Ramo's final fight needed an enemy that felt different from everything before it. Ground enemies patrol and chase on a flat line. I wanted the boss in the air, moving in smooth swooping arcs, so the player has to read its path and not just its position.

## Routes as curves

Each route is a cubic Bézier curve: four points placed in the scene, a start, an end and two handles that bend the curve between them. The boss has a list of routes and flies them in order, looping back to the first.

```csharp
while (tParam < 1)
{
    tParam += Time.deltaTime * speedModifier;
    objectPosition = Mathf.Pow(1 - tParam, 3) * p0
                   + 3 * Mathf.Pow(1 - tParam, 2) * tParam * p1
                   + 3 * (1 - tParam) * Mathf.Pow(tParam, 2) * p2
                   + Mathf.Pow(tParam, 3) * p3;
    transform.position = objectPosition;
    yield return new WaitForEndOfFrame();
}
```

The formula looked intimidating at first, but it's only a weighted average of the four points. As `t` goes from 0 to 1, the weight moves from the start point, through the handles, to the end point. Writing it out by hand, instead of using a spline package, kept every part of it visible and easy to tweak.

## Designing the route in the editor

A second script, `Route`, draws each curve in the scene view: a sphere every 5% of the way, and a line from each end point to its handle. I could drag the handles and see the flight path change before pressing play. Chaining routes so one ends where the next begins turns several short, simple curves into one long flight pattern.

[Screenshot: the scene view with the route spheres and handle lines]

## Shooting

While flying, the boss fires at a random interval between 1.1 and 2.1 seconds. The randomness keeps the player from settling into a rhythm. The script also has `StopShooting()` and `StartShooting()`, but nothing calls them yet.

## What went wrong

- **Speed depends on the curve.** `t` grows at a fixed rate, so the boss covers a long curve faster than a short one, and it speeds up where the handles stretch the curve. I tuned around it by placing the handles carefully, not by fixing it.
- **The formula is written twice.** `BezierFollow` and `Route` each have their own copy of the same equation.
- **`WaitForEndOfFrame` for movement.** It works, but moving in `Update` with `Time.deltaTime` is the usual approach and avoids surprises with physics.

## What I'd change

- Move the formula into one static function used by both scripts.
- Move at constant speed by sampling the curve's length first.

## What I learned

- A bit of math went a long way. Four points and one formula gave the boss its whole personality.
- Editor gizmos turned a math problem into a level design tool.
"""

BOSS_BS = """[Snimak ekrana: boss u letu, s krivuljom rute nacrtanom gizmoima u editoru]

## Problem

Za posljednju borbu u Rami trebao je neprijatelj koji djeluje drugačije od svega prije. Zemaljski neprijatelji patroliraju i jure po ravnoj liniji. Htio sam bossa u zraku, kako se kreće glatkim lukovima, pa igrač mora čitati njegovu putanju, a ne samo poziciju.

## Rute kao krivulje

Svaka ruta je kubna Bézierova krivulja: četiri tačke postavljene u sceni, početak, kraj i dvije ručke koje savijaju krivulju između njih. Boss ima listu ruta i leti ih redom, pa se vraća na prvu.

```csharp
while (tParam < 1)
{
    tParam += Time.deltaTime * speedModifier;
    objectPosition = Mathf.Pow(1 - tParam, 3) * p0
                   + 3 * Mathf.Pow(1 - tParam, 2) * tParam * p1
                   + 3 * (1 - tParam) * Mathf.Pow(tParam, 2) * p2
                   + Mathf.Pow(tParam, 3) * p3;
    transform.position = objectPosition;
    yield return new WaitForEndOfFrame();
}
```

Formula je na početku izgledala zastrašujuće, ali je samo ponderisani prosjek četiri tačke. Kako `t` ide od 0 do 1, težina se seli s početne tačke, preko ručki, do krajnje tačke. Pisanje ručno, umjesto korištenja paketa za krivulje, držalo je svaki njen dio vidljivim i lakim za podešavanje.

## Dizajniranje rute u editoru

Druga skripta, `Route`, crta svaku krivulju u prikazu scene: kuglicu na svakih 5% puta i liniju od svake krajnje tačke do njene ručke. Mogao sam vući ručke i vidjeti kako se putanja leta mijenja prije pokretanja igre. Spajanje ruta, tako da jedna završava gdje sljedeća počinje, pretvara nekoliko kratkih, jednostavnih krivulja u jedan dugi obrazac leta.

[Snimak ekrana: prikaz scene s kuglicama rute i linijama ručki]

## Pucanje

Dok leti, boss puca u nasumičnom intervalu između 1,1 i 2,1 sekunde. Nasumičnost sprečava igrača da uhvati ritam. Skripta ima i `StopShooting()` i `StartShooting()`, ali ih još ništa ne poziva.

## Šta je pošlo po zlu

- **Brzina zavisi od krivulje.** `t` raste fiksnom brzinom, pa boss dugu krivulju pređe brže od kratke i ubrzava gdje ručke razvuku krivulju. To sam zaobišao pažljivim postavljanjem ručki, a ne popravkom.
- **Formula je napisana dvaput.** `BezierFollow` i `Route` imaju svaki svoju kopiju iste jednačine.
- **`WaitForEndOfFrame` za kretanje.** Radi, ali kretanje u `Update` s `Time.deltaTime` je uobičajen pristup i izbjegava iznenađenja s fizikom.

## Šta bih promijenio

- Prebaciti formulu u jednu statičku funkciju koju koriste obje skripte.
- Kretati se konstantnom brzinom tako što se prvo izmjeri dužina krivulje.

## Šta sam naučio

- Malo matematike je mnogo značilo. Četiri tačke i jedna formula dale su bossu cijeli karakter.
- Gizmoi u editoru pretvorili su matematički problem u alat za dizajn nivoa.
"""

TELE_EN = """[Screenshot: the teletext episode menu with the on-screen TV remote]

## The idea

In Bosnia in the early 1990s, teletext was how many people checked the news, the weather and the TV schedule: blocky coloured text on a black screen, page numbers and a remote. I wanted Ramo's menus to feel like that, so picking an episode is like flipping teletext pages, and the UI belongs to the same year as the levels.

## Episodes that unlock

The episode menu is a row of buttons. Only episodes you've reached can be pressed, and progress is a single number saved on the player's machine:

```csharp
int unlockedLevel = PlayerPrefs.GetInt("UnlockedLevel", 1);
for (int i = 0; i < buttons.Length; i++)
    buttons[i].interactable = i < unlockedLevel;
```

Hovering over an episode shows its teletext page, and clicking it loads that level. The same small script handles the preview and the scene load, so adding an episode means adding one button and one page, with no new code.

[Screenshot: hovering over an episode and its teletext page appearing]

## Dialogue in the street

Characters talk to Ramo when he walks up to them. The dialogue box types each line letter by letter, plays one of three short voice sounds, waits, and moves to the next line. The player can skip ahead with R. Walking away closes the box and resets the conversation, so it starts from the beginning next time.

```csharp
foreach (char letter in dialogue[index])
{
    dialogueText.text += letter;
    yield return new WaitForSeconds(wordSpeed);
}
```

The setting does most of the storytelling: a burek is a health pickup, and the voices are short sounds, not full voice acting.

[Screenshot: a dialogue box mid-sentence next to a character]

## What went wrong

- **Progress is one number.** Saving a single unlocked level means there are no per-episode scores, and the save can't grow without a format change.
- **Two text systems.** Dialogue uses Unity's legacy `Text`, while other UI text uses TextMeshPro, so text is styled in two different ways.
- **Mixed languages in code.** Classes are named in both Bosnian and English (`Razgovor`, `HoverButton`, `NaScenu`). It was fine while I worked alone, but someone else would struggle to find their way around.

## What I'd change

- Save a small JSON file with progress per episode.
- Use TextMeshPro everywhere, and keep code names in English.

## What I learned

- Menus are part of the game's identity. The teletext screen says where and when the game is set before the first level starts.
- Small systems that take content as data (buttons and pages, an array of dialogue lines) made it easy to add content late in development.
"""

TELE_BS = """[Snimak ekrana: teletekst meni epizoda s TV daljinskim na ekranu]

## Ideja

U Bosni ranih 90-ih, teletekst je bio način na koji su mnogi provjeravali vijesti, vrijeme i TV program: kockasti obojeni tekst na crnom ekranu, brojevi stranica i daljinski. Htio sam da Ramini meniji djeluju tako, pa je biranje epizode kao listanje teletekst stranica, a UI pripada istoj godini kao i nivoi.

## Epizode koje se otključavaju

Meni epizoda je red dugmadi. Mogu se pritisnuti samo epizode do kojih si stigao, a napredak je jedan broj sačuvan na igračevom računaru:

```csharp
int unlockedLevel = PlayerPrefs.GetInt("UnlockedLevel", 1);
for (int i = 0; i < buttons.Length; i++)
    buttons[i].interactable = i < unlockedLevel;
```

Kad pređeš mišem preko epizode, pojavi se njena teletekst stranica, a klik učitava taj nivo. Ista mala skripta radi i pregled i učitavanje scene, pa dodavanje epizode znači dodavanje jednog dugmeta i jedne stranice, bez novog koda.

[Snimak ekrana: prelazak mišem preko epizode i pojavljivanje njene teletekst stranice]

## Dijalog na ulici

Likovi pričaju s Ramom kad im priđe. Okvir za dijalog ispisuje svaku rečenicu slovo po slovo, pusti jedan od tri kratka zvuka glasa, sačeka i pređe na sljedeću rečenicu. Igrač može preskočiti naprijed tipkom R. Kad se udalji, okvir se zatvara i razgovor se resetuje, pa sljedeći put počinje ispočetka.

```csharp
foreach (char letter in dialogue[index])
{
    dialogueText.text += letter;
    yield return new WaitForSeconds(wordSpeed);
}
```

Okruženje priča većinu priče: burek je predmet za zdravlje, a glasovi su kratki zvukovi, a ne puna glasovna gluma.

[Snimak ekrana: okvir za dijalog usred rečenice pored lika]

## Šta je pošlo po zlu

- **Napredak je jedan broj.** Čuvanje jednog otključanog nivoa znači da nema rezultata po epizodi, a snimak ne može rasti bez promjene formata.
- **Dva sistema za tekst.** Dijalog koristi Unityjev stari `Text`, a ostali UI tekst TextMeshPro, pa se tekst stilizuje na dva različita načina.
- **Miješani jezici u kodu.** Klase su nazvane i na bosanskom i na engleskom (`Razgovor`, `HoverButton`, `NaScenu`). Dok sam radio sam bilo je u redu, ali neko drugi bi se teško snašao.

## Šta bih promijenio

- Čuvati mali JSON fajl s napretkom po epizodi.
- Svuda koristiti TextMeshPro, a imena u kodu držati na engleskom.

## Šta sam naučio

- Meniji su dio identiteta igre. Teletekst ekran kaže gdje i kada se igra dešava prije nego što počne prvi nivo.
- Mali sistemi koji sadržaj primaju kao podatke (dugmad i stranice, niz rečenica dijaloga) olakšali su dodavanje sadržaja kasno u razvoju.
"""

RETRO_EN = """[Screenshot: the Ramo title screen]

## What Ramo was

Ramo was my first complete game. I built it alone, from the idea to the release on itch.io: a 2D platformer set in Sarajevo in spring 1992, with five episodes and a final level. It ended up at 64 scripts and about 3,400 lines of C#, more than 800 plays and downloads, first place at FIT Coding Challenge v.19, a segment on national TV, and my high school graduation project, a 25-page write-up of how it was made.

Looking at the code two years later, with a much bigger project behind me, here is what holds up and what doesn't.

## What holds up

- **Finishing.** Menus, audio settings, checkpoints, builds for Windows and the browser, two languages and a post-launch update. Most of the work of a release isn't gameplay, and Ramo is where I learned that.
- **Using the editor as a tool.** Gizmos for hazard ranges and boss routes let me tune the game in the scene view instead of guessing numbers.
- **The setting.** The hazards, the teletext menus and the dialogue all come from one idea, and that's what players remember.

## What doesn't

- **One script that knows everything.** `Health` is used by the player, the enemies and the boss. It decides what to switch off on death by checking tags and asking for components one by one: player movement, melee, pistol, enemy patrol, two kinds of enemy parents. Every new character type meant another `if` in the same file.
- **Copied code.** The same player detection is in nine scripts, and the Bézier formula is in two.
- **No history.** The public repository starts at the release, so it doesn't show how the game got there, and there is no earlier version to go back to.

```csharp
if (GetComponent<PlayerMovement>() != null) GetComponent<PlayerMovement>().enabled = false;
if (GetComponent<MeleeAttack>() != null)    GetComponent<MeleeAttack>().enabled = false;
if (GetComponent<PistolAttack>() != null)   GetComponent<PistolAttack>().enabled = false;
// ...and more checks for enemies and the boss
```

## What I do differently now

Most of what I changed in ArcaneTD comes straight from these lessons:

- **Events instead of reaching into other objects.** Something raises "died", and whoever cares reacts, instead of `Health` switching off every component itself.
- **Data in ScriptableObjects.** Ramo's numbers live in scenes and prefabs. That's why the balance update touched five scene files. In ArcaneTD, balance is in data assets.
- **Commits from day one**, with pull requests per feature, so the devlog can be written from the history.

## What I learned

- Shipping something small and complete taught me more than any unfinished bigger project would have.
- Code that works for one developer for one year is not the same as code that's easy to change. I only saw the difference once I had to change it.
"""

RETRO_BS = """[Snimak ekrana: naslovni ekran Rame]

## Šta je Ramo bio

Ramo je bila moja prva završena igra. Napravio sam je sam, od ideje do izlaska na itch.io: 2D platformer smješten u Sarajevo u proljeće 1992, s pet epizoda i završnim nivoom. Završio je sa 64 skripte i oko 3.400 linija C# koda, više od 800 igranja i preuzimanja, prvim mjestom na FIT Coding Challenge v.19, prilogom na državnoj televiziji i mojim maturskim radom, opisom razvoja na 25 stranica.

Gledajući kod dvije godine kasnije, s mnogo većim projektom iza sebe, evo šta i dalje valja, a šta ne.

## Šta valja

- **Završavanje.** Meniji, postavke zvuka, checkpointi, buildovi za Windows i preglednik, dva jezika i ažuriranje nakon izlaska. Većina posla oko izlaska igre nije gameplay, i to sam naučio na Rami.
- **Editor kao alat.** Gizmoi za domet prepreka i rute bossa omogućili su mi da igru podešavam u prikazu scene umjesto da pogađam brojeve.
- **Okruženje.** Prepreke, teletekst meniji i dijalozi dolaze iz jedne ideje, i to je ono što igrači pamte.

## Šta ne valja

- **Jedna skripta koja zna sve.** `Health` koriste igrač, neprijatelji i boss. Ona odlučuje šta se gasi pri smrti tako što provjerava tagove i jednu po jednu traži komponente: kretanje igrača, udarac, pištolj, patroliranje neprijatelja, dvije vrste roditeljskih objekata. Svaka nova vrsta lika značila je još jedan `if` u istom fajlu.
- **Kopirani kod.** Ista detekcija igrača je u devet skripti, a Bézierova formula u dvije.
- **Nema historije.** Javni repozitorij počinje izlaskom igre, pa ne pokazuje kako je igra nastala, i nema ranije verzije na koju se može vratiti.

```csharp
if (GetComponent<PlayerMovement>() != null) GetComponent<PlayerMovement>().enabled = false;
if (GetComponent<MeleeAttack>() != null)    GetComponent<MeleeAttack>().enabled = false;
if (GetComponent<PistolAttack>() != null)   GetComponent<PistolAttack>().enabled = false;
// ...and more checks for enemies and the boss
```

## Šta sada radim drugačije

Većina onoga što sam promijenio u ArcaneTD-u dolazi direktno iz ovih lekcija:

- **Događaji umjesto zadiranja u druge objekte.** Nešto objavi "umro", a ko god je zainteresovan reaguje, umjesto da `Health` sam gasi svaku komponentu.
- **Podaci u ScriptableObjectima.** Ramini brojevi žive u scenama i prefabima. Zato je ažuriranje balansa diralo pet fajlova scena. U ArcaneTD-u je balans u assetima s podacima.
- **Commitovi od prvog dana**, s pull requestom za svaku funkcionalnost, pa se devlog može pisati iz historije.

## Šta sam naučio

- Izbacivanje nečeg malog i završenog naučilo me više nego što bi me naučio ijedan nedovršeni veći projekt.
- Kod koji radi jednom developeru godinu dana nije isto što i kod koji je lako mijenjati. Razliku sam vidio tek kad sam ga morao mijenjati.
"""

RAMO_POSTS = {
    "ramo-update-after-launch": {
        "num": 1, "date": "2024-10-10", "project": "ramo",
        "title": {"en": "Update: improved controls, balanced gameplay and bug fixes",
                  "bs": "Ažuriranje: bolje kontrole, balans igre i popravke grešaka"},
        "summary": {"en": "The post-launch update, with what each fix was: a zero-friction material, a resized collider and a set of connected balance numbers.",
                    "bs": "Ažuriranje nakon izlaska, sa onim što je svaka popravka bila: materijal bez trenja, prepravljen kolajder i skup povezanih brojeva za balans."},
        "body": {"en": UPD_EN, "bs": UPD_BS},
    },
    "ramo-hazards-from-1992": {
        "num": 2, "date": "2026-10-17", "project": "ramo",
        "title": {"en": "Hazards from 1992: mines, snipers and live wires",
                  "bs": "Prepreke iz 1992: mine, snajperi i žice pod naponom"},
        "summary": {"en": "Why every hazard kills in one hit, how they detect the player, four kinds of timing, and the detection code I copied nine times.",
                    "bs": "Zašto svaka prepreka ubija iz prve, kako prepoznaju igrača, četiri vrste tajminga i kod za detekciju koji sam kopirao devet puta."},
        "body": {"en": HAZ_EN, "bs": HAZ_BS},
    },
    "ramo-boss-on-bezier-curves": {
        "num": 3, "date": "2026-10-17", "project": "ramo",
        "title": {"en": "A boss that flies on Bézier curves",
                  "bs": "Boss koji leti po Bézierovim krivuljama"},
        "summary": {"en": "Writing the curve formula by hand, designing flight paths with editor gizmos, and why the boss speeds up on long curves.",
                    "bs": "Ručno pisanje formule krivulje, dizajn putanja leta gizmoima u editoru i zašto boss ubrzava na dugim krivuljama."},
        "body": {"en": BOSS_EN, "bs": BOSS_BS},
    },
    "ramo-teletext-menus-and-dialogue": {
        "num": 4, "date": "2026-10-17", "project": "ramo",
        "title": {"en": "Teletext menus and street dialogue",
                  "bs": "Teletekst meniji i dijalozi na ulici"},
        "summary": {"en": "Making the UI feel like 1992: an episode menu styled as teletext, unlocks saved as one number, and dialogue typed out letter by letter.",
                    "bs": "Kako da UI djeluje kao 1992: meni epizoda u stilu teleteksta, otključavanje sačuvano kao jedan broj i dijalog koji se ispisuje slovo po slovo."},
        "body": {"en": TELE_EN, "bs": TELE_BS},
    },
    "ramo-two-years-later": {
        "num": 5, "date": "2026-10-17", "project": "ramo",
        "title": {"en": "Ramo, two years later: what I'd do differently",
                  "bs": "Ramo, dvije godine kasnije: šta bih uradio drugačije"},
        "summary": {"en": "Looking back at my first finished game: what holds up, the Health script that knew everything, and what I changed in ArcaneTD because of it.",
                    "bs": "Osvrt na moju prvu završenu igru: šta valja, skripta Health koja je znala sve i šta sam zbog toga promijenio u ArcaneTD-u."},
        "body": {"en": RETRO_EN, "bs": RETRO_BS},
    },
}
