"""Long devlog posts. Mini-markdown: '## ' heading, '- ' bullets, ``` code fences, **bold**, *italic*, `code`.
Each post: EN and BS text. Code blocks are identical in both languages."""

HEX_CODE_SORT = """frontier.Sort((x, y) => x.Distance.CompareTo(y.Distance));"""

HEX_EN = """## The problem

A tower defence needs a map. I wanted more than a square grid: hexagonal cells, elevation, rivers, roads, water and room for my own game rules on top. I had never built terrain generation or pathfinding before, so I started with the Catlike Coding hex map tutorial and treated it as the foundation, not the finished product. This post is about what I took from it, what I added, and what I got wrong.

## Timeline

- **6 Feb:** first commit, "Rendered hex". One hexagon on screen.
- **10 Feb:** the grid, then blended cell colours.
- **12 and 17 Feb:** elevation with terraces, then irregular edges so the map stops looking like graph paper.
- **25 Feb:** larger maps, split into 5×5 chunks so only the changed part of the mesh is rebuilt.
- **3 to 5 Mar:** rivers (three commits), roads and water.
- **6 to 8 Mar:** terrain features, walls, save and load.
- **10 and 12 Mar:** map management, terrain textures.
- **13 Mar:** pathfinding. The Hex Grid pull request merged the same day: 19 commits over five weeks.

The Hex folder ended up at about 4,200 lines of C#. Most of the first five weeks was learning how Unity meshes, chunks and neighbour lookups fit together. The part that is mine started on 13 March.

## Pathfinding, version one (13 March, 03:23)

My first path search was a breadth-first flood fill. Every cell stored a `Distance`, and a list was the frontier. The cost rules were already the ones the game still uses: roads cost 1, flat ground 5, slopes 10, plus the cell's urban, farm and plant levels, and walls block you unless both cells agree.

The problem was one line:

```csharp
frontier.Sort((x, y) => x.Distance.CompareTo(y.Distance));
```

It sat inside the neighbour loop, so the list was re-sorted up to six times for every cell removed. It was correct but wasteful, and it ran inside a coroutine with a `1/60f` delay so I could watch the search spread across the map.

## Pathfinding, version two (13 March, 06:26, three hours later)

I replaced the list with a priority queue and added a heuristic, which makes it A*. The queue is a bucket list: one linked list of cells per priority value, and a `minimum` pointer so `Dequeue` never scans from zero.

```csharp
public void Enqueue (HexCell cell) {
    count += 1;
    int priority = cell.SearchPriority;
    if (priority < minimum) minimum = priority;
    while (priority >= list.Count) list.Add(null);
    cell.NextWithSamePriority = list[priority];
    list[priority] = cell;
}
```

Each cell now remembers where it was reached from (`PathFrom`), and the path is read backwards from the target once it is dequeued. The hex distance to the goal is the heuristic. This stage follows the tutorial closely. What I learned from it was why the sort was slow and how a priority queue fixes it.

## Making it a game system (17 to 19 March)

The tutorial finds one path from A to B. A tower defence needs several routes, or every enemy walks the same line and the map is solved by one tower cluster. Three commits changed that:

- **Waypoints (17 Mar).** The search now returns a list of cell transforms that `EnemyMovementSystem` follows, announced through a static event: `HexGrid.OnPathsFound`.
- **Path diversity (19 Mar).** Instead of one path, `FindKDiversePaths` runs A* up to `PathCount` times. After each run, every cell on the found path gets a penalty added to its cost, so the next run avoids it.
- **Multiple starts and ends (19 Mar, 30 minutes later).** The single start and end cell became two `HashSet<HexCell>`. For each start, the code checks which ends are reachable, splits the route budget between them (`PathCount / reachableEnds.Count`, at least 1), and shares one penalty table across all of them so routes from different spawns also avoid each other.

```csharp
foreach (HexCell cell in path) {
    if (cell == from || cell == to) continue;
    penalties[cell] = penalties.TryGetValue(cell, out int existing)
        ? existing + PathDiversityPenalty
        : PathDiversityPenalty;
}
```

With `PathDiversityPenalty = 100`, a cell used twice costs 200 extra, which is far more than any normal move. The routes spread out without me drawing them by hand.

The search is also limited to cells marked as enemy path (`IsEnemyPath`). Early on I used `IsRoad`; the flag later also decided where towers cannot be placed.

## Making the map part of the rules (March to April)

- **Swarms and elevation (26 Mar):** enemy movement now reads cell elevation.
- **Vulcan (16 to 28 Apr):** the map had water and rivers. I wanted a second liquid with the same behaviour: lava with its own level and its own rivers. I copied the water logic into `VulcanLevel`, `ValidateVulcanRivers` and the river setters, then fixed the places where water assumptions leaked in. One example was a river validator that still used water rules for lava, which got its own `IsValidVulcanRiverDestination`.

```csharp
if (vulcanLevel > 0 && vulcanLevel == waterLevel) {
    waterLevel = 0;
    ValidateRivers();
}
```

A cell can't hold both liquids at once, so setting one clears the other. `IsPlacable` also checks the lava, so towers can't be built in it. The save format gained a byte for the vulcan level, and one more for the ore type.

## What went wrong

- **Copy-paste for the second liquid.** Vulcan is water with a different name, and I duplicated the code instead of abstracting it. It works, but every river fix now has to be made twice.
- **Each A* call allocates.** `RunAStar` creates two dictionaries and a new queue every time. With 10 routes and several spawns, that is dozens of allocations when a level loads. It only happens once per map, so I left it.
- **A leftover helper.** `FindNearestReachableEnd` was written for multi-end maps and then replaced by `FindAllReachableEnds`. Nothing calls it now, and it should be deleted.
- **The path visualiser is gone.** The coroutine that animated the flood fill was useful for learning and got deleted when paths became events.

## What I'd change

- Model liquids as data: one `Liquid` type with a level and rivers, used for water and lava, instead of parallel fields.
- Cache the search buffers and clear them between runs.
- Write a few tests for the cost function and the diversity penalty, because those are the rules the whole game's difficulty rests on.

## What I learned

- Building from a tutorial is a good way to learn a system, but the real learning started when I had to bend it to my game's needs.
- A small change to a data structure (one sorted list to one bucket queue) changed the whole feel of the tool.
- Games push you toward more than one correct answer. One shortest path was easy; routes that stay good but different needed a different idea.
"""

HEX_BS = """## Problem

Tower defence igri treba mapa. Željeo sam više od kvadratne mreže: šestougaone ćelije, visine, rijeke, ceste, vodu i prostor za vlastita pravila igre iznad svega toga. Nikada ranije nisam pravio generisanje terena ni pronalaženje puta, pa sam krenuo od Catlike Coding tutorijala za hex mape i tretirao ga kao temelj, a ne kao gotov proizvod. Ovaj tekst govori o tome šta sam preuzeo, šta sam dodao i šta sam pogriješio.

## Vremenska linija

- **6. feb:** prvi commit, "Rendered hex". Jedan šestougao na ekranu.
- **10. feb:** mreža, zatim stapanje boja ćelija.
- **12. i 17. feb:** visine s terasama, zatim nepravilne ivice da mapa ne izgleda kao milimetarski papir.
- **25. feb:** veće mape, podijeljene na dijelove 5×5 da se ponovo gradi samo promijenjeni dio mesha.
- **3. do 5. mar:** rijeke (tri commita), ceste i voda.
- **6. do 8. mar:** elementi terena, zidovi, snimanje i učitavanje.
- **10. i 12. mar:** upravljanje mapama, teksture terena.
- **13. mar:** pronalaženje puta. Pull request "Hex Grid" spojen je istog dana: 19 commitova kroz pet sedmica.

Hex folder je na kraju imao oko 4.200 linija C# koda. Većina prvih pet sedmica otišla je na učenje kako se u Unityju slažu meshevi, dijelovi mape i traženje susjeda. Dio koji je moj počinje 13. marta.

## Pronalaženje puta, prva verzija (13. mart, 03:23)

Prva pretraga puta bila je pretraga u širinu. Svaka ćelija je pamtila `Distance`, a lista je bila front pretrage. Pravila troška su već bila ona koja igra i danas koristi: cesta košta 1, ravno tlo 5, padina 10, plus nivoi urbanizacije, farmi i biljaka u ćeliji, a zidovi blokiraju prolaz osim ako se obje ćelije slažu.

Problem je bio jedna linija:

```csharp
frontier.Sort((x, y) => x.Distance.CompareTo(y.Distance));
```

Bila je unutar petlje po susjedima, pa se lista sortirala do šest puta za svaku izvučenu ćeliju. Radilo je ispravno, ali rasipno, i izvršavalo se u korutini s odgodom od `1/60f` da bih mogao gledati kako se pretraga širi mapom.

## Pronalaženje puta, druga verzija (13. mart, 06:26, tri sata kasnije)

Zamijenio sam listu prioritetnim redom i dodao heuristiku, što ga čini A* algoritmom. Red je lista "kanti": jedna povezana lista ćelija po vrijednosti prioriteta i pokazivač `minimum` da `Dequeue` nikad ne skenira od nule.

```csharp
public void Enqueue (HexCell cell) {
    count += 1;
    int priority = cell.SearchPriority;
    if (priority < minimum) minimum = priority;
    while (priority >= list.Count) list.Add(null);
    cell.NextWithSamePriority = list[priority];
    list[priority] = cell;
}
```

Svaka ćelija sada pamti odakle je dostignuta (`PathFrom`), a put se čita unazad od cilja kad je on izvučen iz reda. Heuristika je hex udaljenost do cilja. Ova faza prati tutorijal vrlo blisko. Iz nje sam naučio zašto je sortiranje bilo sporo i kako prioritetni red to rješava.

## Od algoritma do sistema igre (17. do 19. mart)

Tutorijal pronalazi jedan put od A do B. Tower defenceu treba više ruta, inače svi neprijatelji idu istom linijom i mapu riješi jedna grupa tornjeva. To su promijenila tri commita:

- **Waypointi (17. mar).** Pretraga sada vraća listu transformacija ćelija koje prati `EnemyMovementSystem`, a objavljuje ih statički događaj `HexGrid.OnPathsFound`.
- **Raznolikost puteva (19. mar).** Umjesto jednog puta, `FindKDiversePaths` pokreće A* do `PathCount` puta. Nakon svakog pokretanja, svaka ćelija na pronađenom putu dobije kaznu u trošku, pa je sljedeći pokušaj zaobilazi.
- **Više početaka i krajeva (19. mar, 30 minuta kasnije).** Jedna početna i jedna krajnja ćelija postale su dva `HashSet<HexCell>`. Za svaki početak kod provjerava koji su krajevi dostižni, dijeli budžet ruta među njima (`PathCount / reachableEnds.Count`, najmanje 1) i dijeli jednu tabelu kazni među svima, pa se i rute iz različitih spawnova zaobilaze.

```csharp
foreach (HexCell cell in path) {
    if (cell == from || cell == to) continue;
    penalties[cell] = penalties.TryGetValue(cell, out int existing)
        ? existing + PathDiversityPenalty
        : PathDiversityPenalty;
}
```

Uz `PathDiversityPenalty = 100`, ćelija korištena dvaput košta 200 dodatno, što je mnogo više od bilo kojeg običnog poteza. Rute se razilaze bez da ih ja ručno crtam.

Pretraga je ograničena i na ćelije označene kao put neprijatelja (`IsEnemyPath`). Na početku sam koristio `IsRoad`; ta oznaka kasnije određuje i gdje se tornjevi ne mogu postaviti.

## Mapa postaje dio pravila (mart do april)

- **Rojevi i visina (26. mar):** kretanje neprijatelja sada čita visinu ćelije.
- **Vulcan (16. do 28. apr):** mapa je imala vodu i rijeke. Htio sam drugu tečnost s istim ponašanjem: lavu s vlastitim nivoom i vlastitim rijekama. Kopirao sam logiku vode u `VulcanLevel`, `ValidateVulcanRivers` i postavljače rijeka, pa popravljao mjesta gdje su pretpostavke o vodi curile unutra. Primjer je validator rijeka koji je za lavu još koristio pravila vode; dobio je vlastiti `IsValidVulcanRiverDestination`.

```csharp
if (vulcanLevel > 0 && vulcanLevel == waterLevel) {
    waterLevel = 0;
    ValidateRivers();
}
```

Ćelija ne može imati obje tečnosti odjednom, pa postavljanje jedne briše drugu. `IsPlacable` provjerava i lavu, pa se tornjevi ne mogu graditi u njoj. Format snimanja dobio je jedan bajt za nivo lave i još jedan za vrstu rude.

## Šta je pošlo po zlu

- **Copy-paste za drugu tečnost.** Vulcan je voda s drugim imenom, a ja sam duplicirao kod umjesto da ga apstrahujem. Radi, ali svaku popravku rijeka sada treba napraviti dvaput.
- **Svaki A* poziv alocira.** `RunAStar` svaki put pravi dva rječnika i novi red. Uz 10 ruta i nekoliko spawnova, to su desetine alokacija pri učitavanju nivoa. Dešava se jednom po mapi, pa sam ostavio.
- **Zaostala pomoćna funkcija.** `FindNearestReachableEnd` je napisana za mape s više krajeva pa zamijenjena funkcijom `FindAllReachableEnds`. Sada je nitko ne poziva i treba je obrisati.
- **Vizualizacije pretrage više nema.** Korutina koja je animirala širenje pretrage bila je korisna za učenje i obrisana je kad su putevi postali događaji.

## Šta bih promijenio

- Tečnosti modelirati kao podatke: jedan tip `Liquid` s nivoom i rijekama, za vodu i lavu, umjesto paralelnih polja.
- Keširati bufere pretrage i čistiti ih između pokretanja.
- Napisati nekoliko testova za funkciju troška i kaznu raznolikosti, jer na tim pravilima počiva težina cijele igre.

## Šta sam naučio

- Gradnja prema tutorijalu dobar je način da naučiš sistem, ali pravo učenje počelo je kad sam ga morao saviti prema potrebama svoje igre.
- Mala promjena strukture podataka (jedna sortirana lista u jedan red s kantama) promijenila je cijeli osjećaj alata.
- Igre te guraju prema više od jednog tačnog odgovora. Jedan najkraći put bio je lak; rute koje ostaju dobre, ali različite, tražile su drugu ideju.
"""

MM_EN = """## The problem

Between waves in ArcaneTD, a shady broker called the Middleman offers you cards. Some are safe, some are risky, and how generous he is depends on how much he trusts you. That sounds simple, but it touches almost everything: the player's resources, the towers you can upgrade, the crew, and later the bribe shop. The question was how to build a system that many parts of the game depend on without tangling them all together.

## Version one: one script, one evening (10 July)

The first `MiddleMan.cs` landed on 10 July as a single 217-line script. It picked three random cards, let you take one for free, and charged for more. The loyalty logic was only a sketch: five `if` branches for the five loyalty levels, with the actual effects commented out.

```csharp
private List<CardSO> GetFilteredCardPoolBasedOnLoyalty()
{
    List<CardSO> pool = new List<CardSO>(allAvailableCards);
    if (Loyalty < 20)      { /* pool.RemoveAll(...) */ }
    else if (Loyalty < 40) { /* ... */ }
    // ...three more empty branches
    return pool;
}
```

Two hours later the second commit made cards data instead of code. Every card is a ScriptableObject that holds a list of effects, and every effect is its own small ScriptableObject:

```csharp
public abstract class CardEffect : ScriptableObject
{
    public abstract void ApplyEffect();
}

public class ResourceGainEffect : CardEffect
{
    public ElementType Element;
    public int Amount;
    public override void ApplyEffect() { /* gain energy or an element */ }
}
```

That meant a card like "Get 50 Blumion" was an asset I could make in the editor with no new code. It is the decision that made the card pool easy to grow later.

## What was wrong with it

Looking back at that first version, a few things were already going to hurt:

- **The UI called the Middleman directly.** The card screen did `MiddleMan.Instance.OpenMiddleManDeals()`. Any change to one side would break the other.
- **Loyalty did nothing yet.** The filtering branches were empty.
- **Prices stacked by accident.** The extra-card price used a chain of separate `if` statements, so at low loyalty two multipliers both applied (1.5 and then 1.2, so 1.8 in total) when I meant one.
- **A wrong call.** Buying a second card called `InvokeEnergyGain` where it needed `InvokeEnergySpend`. The compiler can't catch that kind of mistake.

## The rewrite (13 August)

On 13 August I rewrote the Middleman. The commit touched `MiddleMan.cs` by +230 and −109 lines, and added five new files: `MiddleManCommands`, `MiddleManBalanceConfig`, `OfferSlot`, `OfferItem` and `CardOfferGenerator`, plus `CardPackSO` for the packs. Three decisions defined it.

**1. The UI only sends requests.** Buttons call a tiny static class. The Middleman listens, does the work, and broadcasts the results as events:

```csharp
public static class MiddleManCommands
{
    public static event Action OnOpenDealsRequested;
    public static event Action<int, int> OnSelectCardRequested;
    public static event Action OnRefreshRequested;
    public static event Action<CardSO> OnRejectRiskCardRequested;

    public static void RequestOpenDeals() => OnOpenDealsRequested?.Invoke();
    public static void RequestRefresh()   => OnRefreshRequested?.Invoke();
    // ...
}
```

After this, the card screen has no reference to the Middleman's internals at all. I could change how offers are generated without opening a single UI script.

**2. Each wave offers three fixed slots.** One generator builds them: a single card, a pack, and a third slot that is either a risk card or a logistics card. Every slot rolls a tier (low, mid or high) from weighted odds.

```csharp
OfferSlot slot1 = GenerateSingleCardSlot(pool, Slot1AllowedTypes, config.Slot1TierWeights);
OfferSlot slot2 = GeneratePackSlot(allPacks, config);
OfferSlot slot3 = GenerateSlot3(pool, config);
return new List<OfferSlot> { slot1, slot2, slot3 };
```

**3. Loyalty is a table, not a pile of ifs.** The five brackets (Distrust, Volatile, Neutral, Friendly, Loyal) each have their own odds and price multipliers in one balance file. To change how the Middleman feels at 30 loyalty, I change numbers in one place.

```csharp
public const int BaseRefreshCost = 15;
public const int RefreshCostIncrementPerUse = 10;
public const int RefreshLoyaltyPenalty = -3;
public const int LeaveShopWithoutBuyingLoyaltyPenalty = -5;
```

Loyalty starts at 50 and moves with almost everything the player does: taking a card, rejecting a risk card, refreshing the offers, and leaving without buying. Because it affects both what he offers and what it costs, the player is always trading a good deal now against his trust later.

## What it connected to

Once the Middleman was clean, other systems could plug into it easily:

- **1 September:** a `GameDatabaseSO` and a `PlayerProfile` to hold unlocked cards, crew and bribes between runs.
- **5 September:** the bribe shop. High loyalty unlocks the strongest bribes, so the system I built in July now shapes what the player can buy in September.

## What I'd still change

- The old generator code is still sitting in the file as commented-out blocks. It should be deleted.
- The balance numbers are `const` values in a static class. I would move them into a ScriptableObject so I can tune them from the inspector while the game runs.
- Static events are easy, but they make the system harder to unit test. I haven't written tests for the offer generator yet, and I should, since it is full of probabilities.

## What I learned

Writing the first version in one evening was the right call, because I needed something I could play. But I only found the right architecture after living with it for a month. If I did it again, I'd still start quick, then plan the rewrite for the moment a second system needs to talk to it.
"""

MM_BS = """## Problem

Između valova u ArcaneTD-u, sumnjivi posrednik zvan Middleman nudi ti karte. Neke su sigurne, neke rizične, a koliko je velikodušan zavisi od toga koliko ti vjeruje. Zvuči jednostavno, ali dotiče gotovo sve: igračeve resurse, tornjeve koje možeš nadograditi, posadu i kasnije prodavnicu mita. Pitanje je bilo kako napraviti sistem o kojem zavisi mnogo dijelova igre, a da se svi ne zapetljaju.

## Prva verzija: jedna skripta, jedno veče (10. juli)

Prvi `MiddleMan.cs` pojavio se 10. jula kao jedna skripta od 217 linija. Birao je tri nasumične karte, dozvoljavao da jednu uzmeš besplatno, a za više naplaćivao. Logika odanosti bila je samo skica: pet `if` grana za pet nivoa odanosti, a stvarni efekti zakomentarisani.

```csharp
private List<CardSO> GetFilteredCardPoolBasedOnLoyalty()
{
    List<CardSO> pool = new List<CardSO>(allAvailableCards);
    if (Loyalty < 20)      { /* pool.RemoveAll(...) */ }
    else if (Loyalty < 40) { /* ... */ }
    // ...three more empty branches
    return pool;
}
```

Dva sata kasnije drugi commit je karte pretvorio u podatke umjesto koda. Svaka karta je ScriptableObject s listom efekata, a svaki efekat je svoj mali ScriptableObject:

```csharp
public abstract class CardEffect : ScriptableObject
{
    public abstract void ApplyEffect();
}

public class ResourceGainEffect : CardEffect
{
    public ElementType Element;
    public int Amount;
    public override void ApplyEffect() { /* gain energy or an element */ }
}
```

To je značilo da je karta poput "Dobij 50 Blumiona" asset koji mogu napraviti u editoru bez novog koda. Ta odluka je kasnije olakšala rast skupa karata.

## Šta nije valjalo

Kad se osvrnem na tu prvu verziju, nekoliko stvari je već bilo osuđeno da zaboli:

- **UI je direktno zvao Middlemana.** Ekran s kartama je radio `MiddleMan.Instance.OpenMiddleManDeals()`. Svaka promjena s jedne strane lomila bi drugu.
- **Odanost još nije ništa radila.** Grane za filtriranje bile su prazne.
- **Cijene su se slučajno množile.** Cijena dodatne karte koristila je niz odvojenih `if` naredbi, pa su pri niskoj odanosti obje množilice važile (1,5 pa 1,2, ukupno 1,8) iako sam htio jednu.
- **Pogrešan poziv.** Kupovina druge karte pozivala je `InvokeEnergyGain` gdje je trebalo `InvokeEnergySpend`. Kompajler takvu grešku ne može uhvatiti.

## Prepravka (13. august)

13. augusta sam prepravio Middlemana. Commit je u `MiddleMan.cs` dodao +230 i obrisao −109 linija, uz pet novih fajlova: `MiddleManCommands`, `MiddleManBalanceConfig`, `OfferSlot`, `OfferItem` i `CardOfferGenerator`, plus `CardPackSO` za pakete. Tri odluke su je definisale.

**1. UI samo šalje zahtjeve.** Dugmad zovu malu statičku klasu. Middleman sluša, odrađuje posao i rezultate objavljuje kao događaje:

```csharp
public static class MiddleManCommands
{
    public static event Action OnOpenDealsRequested;
    public static event Action<int, int> OnSelectCardRequested;
    public static event Action OnRefreshRequested;
    public static event Action<CardSO> OnRejectRiskCardRequested;

    public static void RequestOpenDeals() => OnOpenDealsRequested?.Invoke();
    public static void RequestRefresh()   => OnRefreshRequested?.Invoke();
    // ...
}
```

Nakon toga ekran s kartama uopće nema referencu na unutrašnjost Middlemana. Mogao sam promijeniti način generisanja ponuda bez otvaranja ijedne UI skripte.

**2. Svaki val nudi tri fiksna slota.** Gradi ih jedan generator: jedna karta, jedan paket i treći slot koji je ili rizična ili logistička karta. Svaki slot baca nivo (nizak, srednji ili visok) prema ponderisanim šansama.

```csharp
OfferSlot slot1 = GenerateSingleCardSlot(pool, Slot1AllowedTypes, config.Slot1TierWeights);
OfferSlot slot2 = GeneratePackSlot(allPacks, config);
OfferSlot slot3 = GenerateSlot3(pool, config);
return new List<OfferSlot> { slot1, slot2, slot3 };
```

**3. Odanost je tabela, a ne gomila if-ova.** Pet razreda (Nepovjerenje, Nestabilan, Neutralan, Prijateljski, Odan) imaju svoje šanse i množioce cijena u jednom fajlu za balans. Da promijenim kako se Middleman ponaša pri odanosti 30, mijenjam brojeve na jednom mjestu.

```csharp
public const int BaseRefreshCost = 15;
public const int RefreshCostIncrementPerUse = 10;
public const int RefreshLoyaltyPenalty = -3;
public const int LeaveShopWithoutBuyingLoyaltyPenalty = -5;
```

Odanost počinje na 50 i mijenja se gotovo svime što igrač radi: uzimanjem karte, odbijanjem rizične karte, osvježavanjem ponude i odlaskom bez kupovine. Pošto utiče i na to šta nudi i na cijenu, igrač uvijek mijenja dobar posao sada za njegovo povjerenje kasnije.

## Sa čime se povezao

Kad je Middleman bio čist, drugi sistemi su se lako mogli priključiti:

- **1. septembar:** `GameDatabaseSO` i `PlayerProfile` koji čuvaju otključane karte, posadu i mita između partija.
- **5. septembar:** prodavnica mita. Visoka odanost otključava najjača mita, pa sistem koji sam napravio u julu sada oblikuje šta igrač može kupiti u septembru.

## Šta bih još promijenio

- Stari kod generatora još stoji u fajlu kao zakomentarisani blokovi. Treba ga obrisati.
- Brojevi balansa su `const` vrijednosti u statičkoj klasi. Prebacio bih ih u ScriptableObject da ih mogu podešavati iz inspektora dok igra radi.
- Statički događaji su laki, ali sistem čine težim za unit testiranje. Još nisam napisao testove za generator ponuda, a trebalo bi, jer je pun vjerovatnoća.

## Šta sam naučio

Pisanje prve verzije u jednom veče bila je dobra odluka, jer mi je trebalo nešto na čemu mogu igrati. Ali pravu arhitekturu sam našao tek nakon mjesec dana života s njom. Da radim ponovo, opet bih počeo brzo, pa planirao prepravku za trenutak kad drugi sistem treba da priča s njim.
"""

POSTS = {
    "hexmap-from-tutorial-to-enemy-paths": {
        "num": 1, "date": "2026-03-13", "project": "arcanetd",
        "title": {"en": "Building the hex map: from a tutorial to a map enemies can walk",
                  "bs": "Gradnja hex mape: od tutorijala do mape kojom neprijatelji hodaju"},
        "summary": {"en": "Six weeks from one hexagon to terrain, rivers, A* pathfinding, and diverse enemy routes, and what I'd do differently.",
                    "bs": "Šest sedmica od jednog šestougla do terena, rijeka, A* pretrage i raznolikih ruta neprijatelja, te šta bih sada uradio drugačije."},
        "body": {"en": HEX_EN, "bs": HEX_BS},
    },
    "middleman-from-script-to-system": {
        "num": 2, "date": "2026-08-13", "project": "arcanetd",
        "title": {"en": "How I built the Middleman: from one 217-line script to a system the UI can't break",
                  "bs": "Kako sam napravio Middlemana: od jedne skripte od 217 linija do sistema koji UI ne može slomiti"},
        "summary": {"en": "A broker system that many parts of the game depend on, rewritten after a month of living with the first version.",
                    "bs": "Sistem posrednika o kojem zavisi mnogo dijelova igre, prepravljen nakon mjesec dana života s prvom verzijom."},
        "body": {"en": MM_EN, "bs": MM_BS},
    },
}


# ---------------------------------------------------------------- screenshot placeholders for #1 and #5
HEX_EN = HEX_EN.replace("## The problem\n", "[Screenshot: a finished map, wide shot, with terrain, elevation, a river and roads]\n\n## The problem\n", 1)
HEX_BS = HEX_BS.replace("## Problem\n", "[Snimak ekrana: gotova mapa, širi kadar, s terenom, visinama, rijekom i cestama]\n\n## Problem\n", 1)
HEX_EN = HEX_EN.replace("The routes spread out without me drawing them by hand.\n", "The routes spread out without me drawing them by hand.\n\n[Screenshot: one A* route (blue start, red end, white path) next to the same map with ten diverse routes lit up]\n\n[Screenshot: a map with two or more start and end cells and the routes between them]\n", 1)
HEX_BS = HEX_BS.replace("Rute se razilaze bez da ih ja ručno crtam.\n", "Rute se razilaze bez da ih ja ručno crtam.\n\n[Snimak ekrana: jedna A* ruta (plavi početak, crveni kraj, bijeli put) pored iste mape s deset raznolikih ruta]\n\n[Snimak ekrana: mapa s dva ili više početaka i krajeva i rutama između njih]\n", 1)
HEX_EN = HEX_EN.replace("one more for the ore type.\n", "one more for the ore type.\n\n[Screenshot: a lava river and a water river on the same map]\n", 1)
HEX_BS = HEX_BS.replace("još jedan za vrstu rude.\n", "još jedan za vrstu rude.\n\n[Snimak ekrana: rijeka lave i rijeka vode na istoj mapi]\n", 1)
MM_EN = MM_EN.replace("## The problem\n", "[Screenshot: the offer screen with all three slots: a single card, a pack, and a risk or logistics card]\n\n## The problem\n", 1)
MM_BS = MM_BS.replace("## Problem\n", "[Snimak ekrana: ekran s ponudom i sva tri slota: jedna karta, paket i rizična ili logistička karta]\n\n## Problem\n", 1)
MM_EN = MM_EN.replace("I change numbers in one place.\n", "I change numbers in one place.\n\n[Screenshot: the same offer screen at low and at high loyalty, with different prices and tiers]\n", 1)
MM_BS = MM_BS.replace("mijenjam brojeve na jednom mjestu.\n", "mijenjam brojeve na jednom mjestu.\n\n[Snimak ekrana: isti ekran s ponudom pri niskoj i visokoj odanosti, s različitim cijenama i nivoima]\n", 1)
POSTS["hexmap-from-tutorial-to-enemy-paths"]["body"] = {"en": HEX_EN, "bs": HEX_BS}
POSTS["middleman-from-script-to-system"]["body"] = {"en": MM_EN, "bs": MM_BS}
POSTS["middleman-from-script-to-system"]["num"] = 5

from posts_more import MORE_POSTS
POSTS.update(MORE_POSTS)

from posts_ramo import RAMO_POSTS
POSTS.update(RAMO_POSTS)
