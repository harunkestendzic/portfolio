"""Devlog posts #2, #3, #4, #6 and #7 for ArcaneTD. Same mini-markdown as posts.py.
A line starting with [Screenshot: ...] / [Snimak ekrana: ...] renders as an image placeholder."""

WAVES_EN = """[Screenshot: a swarm walking up a terraced slope along one of the routes]

## The problem

Once the hex map could find routes, enemies still had to walk them. That meant three things: a way to describe waves without writing code for each one, movement that follows a path made of cells, and enemies that stay on the ground on a map with terraces and noisy, uneven edges. This post covers the two weeks after the hex grid merged, from 15 to 28 March.

## Moving the old game onto hexes (15 to 19 March)

Some systems existed before the hex map, like tower placement and basic enemy movement. The "Legacy Systems Adaptations" pull request (+996, −219 lines) moved them onto hex cells: tower placement on 15 March, paths and waypoints on 17 March, and on 19 March a commit called "Bugs fixed and systems adapted". That commit also deleted `Ucenje/Grid.cs` ("učenje" means learning), a procedural mesh exercise from when I was first learning how Unity builds meshes.

Movement lives in one place. `EnemyMovementSystem` listens for `HexGrid.OnPathsFound`, keeps every route, and moves all enemies in a single `Update` loop. Each new enemy takes the next route in turn, so a wave spreads across the map instead of piling onto one path:

```csharp
public Transform[] GetNextPath()
{
    if (allPaths.Count == 0) return null;
    Transform[] path = allPaths[nextPathIndex % allPaths.Count].ToArray();
    nextPathIndex++;
    return path;
}
```

## Waves as data (24 and 25 March)

I wanted to build levels in the editor, not in code. "Custom Waves implemented" split a level into a tree of ScriptableObjects: a level holds waves, a wave holds mini-waves, and a mini-wave holds groups of enemies with their own delays.

```csharp
[System.Serializable]
public class EnemyGroup
{
    public EnemySO enemyData;
    public int count = 1;
    public bool isSwarm;
}

public class MiniWaveDataSO : ScriptableObject
{
    public EnemyGroup[] EnemyGroups;
    public float DelayBetweenGroups;
    public float PostMiniWaveDelay = 3f;
}
```

Each wave can also set its own planning time before it starts. The day after, I cleaned up the first version. It created every enemy in `Awake` and printed three debug lines per enemy. It now preloads a pool once: every enemy the level will need is created up front, switched off, and taken from the pool when its group spawns.

[Screenshot: a wave asset in the Unity inspector, showing mini-waves and enemy groups]

## Swarms (26 March, morning)

A normal group spawns one enemy at a time. A swarm group spawns all at once on a single shared route, and each member gets a random offset inside a small circle. At every waypoint the offset picks a new target, and the enemy drifts towards it, so a swarm moves like a crowd and not like a line of clones.

```csharp
Transform[] sharedPath = group.isSwarm && EnemyMovementSystem.Instance
    ? EnemyMovementSystem.Instance.GetNextPath()
    : null;
for (int i = 0; i < group.count; i++)
{
    Enemy enemy = EnemyManager.Instance.FindPooledEnemy(group.enemyData);
    enemy.ResetEnemy(sharedPath);
    if (group.isSwarm) enemy.ApplySwarmOffset();
    enemy.gameObject.SetActive(true);
    if (!group.isSwarm) yield return new WaitForSeconds(miniWave.DelayBetweenGroups);
}
```

## Walking on uneven ground (26 March, 11:13 and 11:29)

Until then, enemies moved in a straight line between waypoint positions, so on slopes they cut through hills or floated above them. Part one split movement into horizontal and vertical. The enemy moves on the flat plane, tracks how far along the current segment it is, and blends its height between the start and end of that segment.

It still looked wrong. The waypoint positions sit at the cell centre, but the hex mesh is pushed up and down by noise, so enemies hovered or sank between cells. I had covered it with a 1-unit height offset. Part two, sixteen minutes later, fixed the cause: it blends between the cells' elevation levels and turns that into a height with the same noise sample the mesh uses. The offset went from 1 to 0.1.

```csharp
private static float ElevationToWorldY(float baseElevation, Vector3 worldPos)
{
    float y = baseElevation * HexMetrics.ELEVATION_STEP;
    y += (HexMetrics.SampleNoise(worldPos).y * 2f - 1f) * HexMetrics.ELEVATION_PERTURB_STRENGTH;
    return y;
}
```

[Screenshot: an enemy walking over terraces, before and after the fix]

## What went wrong

- **A magic number hid the real bug.** The 1-unit height offset made part one look fine from far away. The cause was that I computed height differently from the mesh.
- **Scanning for enemies every frame.** The movement system finds new enemies by looping over the children of two parent objects every frame and checking a list with `Contains`. It works for the enemy counts I have now, but it gets slower as waves grow.
- **Testing code that stayed.** Routes are recalculated at the start of every combat phase, and the line still has the comment `//JUST FOR TESTING` next to it.

## What I'd change

- Have the pool raise an event when it activates an enemy, so the movement system registers it once instead of searching.
- Calculate routes once when a level loads, and only again when the map changes.

## What I learned

- Data-driven waves paid off quickly. Every level since then was built in the inspector.
- When something looks slightly off, find out why before adding an offset. Here the fix was to use the same height function as the mesh.
- Later the route list became the base for the Deceiver tower, which reads the forks where routes split. That's the next post.
"""

WAVES_BS = """[Snimak ekrana: roj koji se penje terasastom padinom duž jedne od ruta]

## Problem

Kad je hex mapa mogla pronaći rute, neprijatelji su ih i dalje trebali prehodati. To je značilo tri stvari: način da opišem valove bez pisanja koda za svaki, kretanje koje prati put sastavljen od ćelija i neprijatelje koji ostaju na tlu na mapi s terasama i nepravilnim ivicama punim šuma. Ovaj tekst pokriva dvije sedmice nakon spajanja hex mreže, od 15. do 28. marta.

## Prebacivanje stare igre na heksagone (15. do 19. mart)

Neki sistemi su postojali prije hex mape, poput postavljanja tornjeva i osnovnog kretanja neprijatelja. Pull request "Legacy Systems Adaptations" (+996, −219 linija) prebacio ih je na hex ćelije: postavljanje tornjeva 15. marta, puteve i waypointe 17. marta, a 19. marta commit "Bugs fixed and systems adapted". Taj commit je obrisao i `Ucenje/Grid.cs`, vježbu s proceduralnim meshom iz vremena kad sam tek učio kako Unity pravi mesheve.

Kretanje živi na jednom mjestu. `EnemyMovementSystem` sluša `HexGrid.OnPathsFound`, čuva sve rute i pomjera sve neprijatelje u jednoj `Update` petlji. Svaki novi neprijatelj uzima sljedeću rutu po redu, pa se val širi mapom umjesto da se nagomila na jednom putu:

```csharp
public Transform[] GetNextPath()
{
    if (allPaths.Count == 0) return null;
    Transform[] path = allPaths[nextPathIndex % allPaths.Count].ToArray();
    nextPathIndex++;
    return path;
}
```

## Valovi kao podaci (24. i 25. mart)

Htio sam praviti nivoe u editoru, a ne u kodu. "Custom Waves implemented" je podijelio nivo u stablo ScriptableObjecta: nivo sadrži valove, val sadrži mini-valove, a mini-val grupe neprijatelja s vlastitim pauzama.

```csharp
[System.Serializable]
public class EnemyGroup
{
    public EnemySO enemyData;
    public int count = 1;
    public bool isSwarm;
}

public class MiniWaveDataSO : ScriptableObject
{
    public EnemyGroup[] EnemyGroups;
    public float DelayBetweenGroups;
    public float PostMiniWaveDelay = 3f;
}
```

Svaki val može postaviti i vlastito vrijeme za planiranje prije početka. Sutradan sam očistio prvu verziju. Pravila je sve neprijatelje u `Awake` i ispisivala tri debug linije po neprijatelju. Sada jednom unaprijed puni pool: svaki neprijatelj koji nivou treba napravi se na početku, isključi i uzme iz poola kad se njegova grupa pojavi.

[Snimak ekrana: asset vala u Unity inspektoru, s mini-valovima i grupama neprijatelja]

## Rojevi (26. mart, ujutro)

Obična grupa pušta jednog po jednog neprijatelja. Roj se pojavljuje odjednom na jednoj zajedničkoj ruti, a svaki član dobije nasumični pomak unutar malog kruga. Na svakom waypointu pomak bira novi cilj i neprijatelj lagano klizi prema njemu, pa se roj kreće kao gomila, a ne kao kolona klonova.

```csharp
Transform[] sharedPath = group.isSwarm && EnemyMovementSystem.Instance
    ? EnemyMovementSystem.Instance.GetNextPath()
    : null;
for (int i = 0; i < group.count; i++)
{
    Enemy enemy = EnemyManager.Instance.FindPooledEnemy(group.enemyData);
    enemy.ResetEnemy(sharedPath);
    if (group.isSwarm) enemy.ApplySwarmOffset();
    enemy.gameObject.SetActive(true);
    if (!group.isSwarm) yield return new WaitForSeconds(miniWave.DelayBetweenGroups);
}
```

## Hodanje po neravnom terenu (26. mart, 11:13 i 11:29)

Do tada su se neprijatelji kretali pravom linijom između pozicija waypointa, pa su na padinama prolazili kroz brda ili lebdjeli iznad njih. Prvi dio je razdvojio kretanje na horizontalno i vertikalno. Neprijatelj se kreće po ravni, prati koliko je prešao trenutnog segmenta i miješa visinu između početka i kraja tog segmenta.

I dalje je izgledalo pogrešno. Pozicije waypointa su u centru ćelije, ali hex mesh je pomjeren gore-dolje šumom, pa su neprijatelji lebdjeli ili tonuli između ćelija. To sam prekrio pomakom visine od 1 jedinice. Drugi dio, šesnaest minuta kasnije, popravio je uzrok: miješa nivoe visine ćelija i pretvara ih u visinu istim uzorkom šuma koji koristi mesh. Pomak je spao s 1 na 0,1.

```csharp
private static float ElevationToWorldY(float baseElevation, Vector3 worldPos)
{
    float y = baseElevation * HexMetrics.ELEVATION_STEP;
    y += (HexMetrics.SampleNoise(worldPos).y * 2f - 1f) * HexMetrics.ELEVATION_PERTURB_STRENGTH;
    return y;
}
```

[Snimak ekrana: neprijatelj koji hoda preko terasa, prije i poslije popravke]

## Šta je pošlo po zlu

- **Magični broj je sakrio pravu grešku.** Pomak od 1 jedinice činio je da prvi dio izdaleka izgleda dobro. Uzrok je bio što sam visinu računao drugačije od mesha.
- **Traženje neprijatelja svaki frame.** Sistem kretanja pronalazi nove neprijatelje tako što svaki frame prolazi kroz djecu dva roditeljska objekta i provjerava listu s `Contains`. Za trenutni broj neprijatelja radi, ali usporava kako valovi rastu.
- **Kod za testiranje koji je ostao.** Rute se ponovo računaju na početku svake borbe, a pored te linije i dalje stoji komentar `//JUST FOR TESTING`.

## Šta bih promijenio

- Da pool objavi događaj kad aktivira neprijatelja, pa ga sistem kretanja registruje jednom umjesto da ga traži.
- Rute računati jednom pri učitavanju nivoa, i ponovo samo kad se mapa promijeni.

## Šta sam naučio

- Valovi kao podaci brzo su se isplatili. Svaki nivo od tada napravljen je u inspektoru.
- Kad nešto izgleda malo pogrešno, prvo saznaj zašto, pa tek onda dodaj pomak. Ovdje je rješenje bilo koristiti istu funkciju visine kao mesh.
- Lista ruta kasnije je postala osnova za Deceiver toranj, koji čita račvanja gdje se rute razdvajaju. O tome je sljedeći tekst.
"""

SUPPORT_EN = """[Screenshot: all four support towers placed on one map]

## The problem

Attack towers all do the same thing in different ways: find a target, shoot, apply an element. Support towers don't. The Spotter reveals hidden enemies, the Deceiver sends enemies down the wrong route, the Extraction Beacon collects resources, and the Attacher strengthens another tower. I needed them to share placement, build time, selling and upgrades without forcing four different behaviours into one class.

## One base, thin layers

Every tower extends an abstract `TowerComponent`. It owns what all towers share: the build and retrofit timers, the Building and Ready states, selling, selection events and being locked down by enemies. Support towers add one thin abstract layer, `SupportTowerComponent`, and each tower's numbers live in its own ScriptableObject (`SpotterTowerSO`, `DeceiverTowerSO` and so on).

The important part is one virtual property. A tower only works when this is true, and each subclass can add its own conditions:

```csharp
// TowerComponent
public virtual bool IsOperational => CurrentState == TowerState.Ready && !IsEnemyDisrupted;

// ExtractionBeaconComponent
public override bool IsOperational => base.IsOperational && !ResearchStatus.IsLockedDown;
```

The Beacon's override is how the crew connects to the map: if nobody works in the Research Lab, beacons stop harvesting. One line, and no tower has to know about the crew.

## Attacher (9 June)

The Attacher is placed next to another tower and attaches to it. It can't attach to another Attacher, and it can attach to an attack tower only after that tower has been given an element. Instead of changing the host's code, it adds a component to the host. `AttacherBuff` reads the host's element and applies a different buff for each of the seven elements.

```csharp
private bool ValidateTarget(TowerComponent target)
{
    if (!target) return false;
    if (target is AttacherTowerComponent) return false;
    if (!IsNeighbor(target)) return false;
    if (target is AttackTowerComponent attackTarget)
        return attackTarget.AttackTowerUpgradeState.ChosenBranch != UpgradeBranch.Base;
    return true;
}
```

[Screenshot: an Attacher attached to an elemental attack tower, with the buff visible]

## Deceiver (6 to 9 July)

This was the hardest one. In deceive mode the camera goes top-down, the cells where routes fork next to the tower light up, and the player picks a fork and then the branch they want enemies to take. When an enemy reaches that fork, it rolls against the Deceiver's chance. If it succeeds, the enemy keeps the part of its route it has already walked and switches to the rest of another route that continues down the chosen branch:

```csharp
List<Transform[]> suffixOptions = PathIntersectionUtility.FindPathSuffixesAfterTransition(currentCell, chosenBranch, allPaths);
if (suffixOptions.Count == 0) return null;

Transform[] suffix = suffixOptions[Random.Range(0, suffixOptions.Count)];
Transform[] prefix = currentAssignedPath.Take(currentWaypointIndex + 1).ToArray();
return prefix.Concat(suffix).ToArray();
```

This only works because the hex map already produces several diverse routes. The Deceiver doesn't run its own pathfinding. It reuses the routes and splices them together.

The first version, committed with the message "Deceiver added (still has bugs)", found forks by grouping each cell's next cells by the cell before it, and only counted a fork if two routes arrived from the same direction and then split. It also skipped the first cell of every route. Forks where routes arrived from different sides, or split right at a spawn, never lit up. The fix three days later was to make it simpler: a fork is any cell where routes continue to two or more different cells. `PathIntersectionUtility` went from 57 to 39 lines. The same commit handled two Deceivers placed on the same fork: the newer one now clears the older one.

[Screenshot: deceive mode, top-down, with forks highlighted in cyan and branch choices in magenta]

## Spotter and Extraction Beacon

The **Spotter** pulses on a timer, finds enemies in its radius with a physics overlap, and reveals stealthed enemies for a few seconds. It came with the camouflaged enemies in August, so it gets its own post with the enemy types.

The **Extraction Beacon** can only be placed next to a cell with ore. When it's placed, it picks the element of the neighbouring ore and adds that element on a timer while it's operational.

[Screenshot: an Extraction Beacon next to an ore cell]

## What went wrong

- **Upgrade tiers are switch statements.** Each support tower has fields like `T1Radius`, `T2Radius` and `T3Radius`, read through a `switch`. While writing this post I found that the Deceiver's tier 2 reads the tier 1 value, because there is no tier 2 field. It's a one-line bug that a data table would have prevented.
- **Hard-coded values next to empty data assets.** The Beacon's harvest interval is a constant in the component, while `ExtractionBeaconSO` is empty. The Attacher's upgrade cost is `return 80f;` with a comment saying to make it data-driven later.
- **An event subscription I need to recheck.** The Attacher subscribes its buff method to the "Attacher upgraded" event and never unsubscribes. That event passes the upgraded Attacher itself, not the tower it's attached to.

## What I'd change

- Replace the per-tier fields with one list of tier data per tower, so adding a tier is a data change.
- Give every event subscription a matching unsubscribe in `OnDestroy`.

## What I learned

- A virtual `IsOperational` was the most useful line in the tower code. Crew, research and enemy disruption all switch towers off through it, without the towers knowing why.
- Reusing what another system already computes, like the Deceiver splicing existing routes, was simpler and more reliable than writing new logic.
"""

SUPPORT_BS = """[Snimak ekrana: sva četiri tornja podrške postavljena na jednoj mapi]

## Problem

Napadački tornjevi svi rade isto na različite načine: nađu metu, pucaju, primijene element. Tornjevi podrške ne. Spotter otkriva skrivene neprijatelje, Deceiver šalje neprijatelje pogrešnom rutom, Extraction Beacon skuplja resurse, a Attacher pojačava drugi toranj. Trebali su dijeliti postavljanje, vrijeme gradnje, prodaju i nadogradnje, bez guranja četiri različita ponašanja u jednu klasu.

## Jedna osnova, tanki slojevi

Svaki toranj nasljeđuje apstraktni `TowerComponent`. On posjeduje ono što svi tornjevi dijele: tajmere za gradnju i retrofit, stanja Building i Ready, prodaju, događaje odabira i blokadu od strane neprijatelja. Tornjevi podrške dodaju jedan tanki apstraktni sloj, `SupportTowerComponent`, a brojevi svakog tornja žive u vlastitom ScriptableObjectu (`SpotterTowerSO`, `DeceiverTowerSO` i tako dalje).

Najvažniji dio je jedno virtualno svojstvo. Toranj radi samo kad je ono tačno, a svaka podklasa može dodati svoje uslove:

```csharp
// TowerComponent
public virtual bool IsOperational => CurrentState == TowerState.Ready && !IsEnemyDisrupted;

// ExtractionBeaconComponent
public override bool IsOperational => base.IsOperational && !ResearchStatus.IsLockedDown;
```

Beaconov override je način na koji se posada povezuje s mapom: ako niko ne radi u istraživačkoj laboratoriji, beaconi prestaju sakupljati. Jedna linija, a nijedan toranj ne mora znati za posadu.

## Attacher (9. juni)

Attacher se postavlja pored drugog tornja i kači se na njega. Ne može se zakačiti na drugi Attacher, a na napadački toranj tek kad taj toranj dobije element. Umjesto da mijenja kod domaćina, dodaje mu komponentu. `AttacherBuff` čita element domaćina i primjenjuje drugačije pojačanje za svaki od sedam elemenata.

```csharp
private bool ValidateTarget(TowerComponent target)
{
    if (!target) return false;
    if (target is AttacherTowerComponent) return false;
    if (!IsNeighbor(target)) return false;
    if (target is AttackTowerComponent attackTarget)
        return attackTarget.AttackTowerUpgradeState.ChosenBranch != UpgradeBranch.Base;
    return true;
}
```

[Snimak ekrana: Attacher zakačen na elementarni napadački toranj, s vidljivim pojačanjem]

## Deceiver (6. do 9. juli)

Ovo je bio najteži. U deceive načinu kamera prelazi u pogled odozgo, ćelije pored tornja gdje se rute račvaju zasvijetle, a igrač bira račvanje i onda granu kojom želi da neprijatelji idu. Kad neprijatelj stigne do tog račvanja, baca kocku protiv Deceiverove šanse. Ako uspije, neprijatelj zadržava dio rute koji je već prešao i prelazi na ostatak druge rute koja nastavlja odabranom granom:

```csharp
List<Transform[]> suffixOptions = PathIntersectionUtility.FindPathSuffixesAfterTransition(currentCell, chosenBranch, allPaths);
if (suffixOptions.Count == 0) return null;

Transform[] suffix = suffixOptions[Random.Range(0, suffixOptions.Count)];
Transform[] prefix = currentAssignedPath.Take(currentWaypointIndex + 1).ToArray();
return prefix.Concat(suffix).ToArray();
```

Ovo radi samo zato što hex mapa već pravi nekoliko raznolikih ruta. Deceiver ne pokreće vlastitu pretragu puta. Ponovo koristi postojeće rute i spaja ih.

Prva verzija, s porukom commita "Deceiver added (still has bugs)", tražila je račvanja tako što je sljedeće ćelije grupisala po ćeliji prije njih, i brojala račvanje samo ako su dvije rute stigle iz istog smjera pa se razdvojile. Preskakala je i prvu ćeliju svake rute. Račvanja gdje su rute stizale s različitih strana, ili su se dijelile odmah na spawnu, nikad nisu zasvijetlila. Popravka tri dana kasnije bila je pojednostavljenje: račvanje je svaka ćelija iz koje rute nastavljaju u dvije ili više različitih ćelija. `PathIntersectionUtility` je spao s 57 na 39 linija. Isti commit riješio je i dva Deceivera na istom račvanju: noviji sada briše stariji.

[Snimak ekrana: deceive način, pogled odozgo, s račvanjima označenim cijan bojom i izborom grana magenta bojom]

## Spotter i Extraction Beacon

**Spotter** pulsira na tajmer, pronalazi neprijatelje u svom radijusu fizičkim preklapanjem i na nekoliko sekundi otkriva skrivene neprijatelje. Došao je zajedno s kamufliranim neprijateljima u augustu, pa ima svoje mjesto u tekstu o vrstama neprijatelja.

**Extraction Beacon** se može postaviti samo pored ćelije s rudom. Kad se postavi, uzima element susjedne rude i dodaje taj element na tajmer dok radi.

[Snimak ekrana: Extraction Beacon pored ćelije s rudom]

## Šta je pošlo po zlu

- **Nivoi nadogradnje su switch naredbe.** Svaki toranj podrške ima polja poput `T1Radius`, `T2Radius` i `T3Radius`, koja se čitaju kroz `switch`. Dok sam pisao ovaj tekst, našao sam da Deceiverov nivo 2 čita vrijednost nivoa 1, jer polje za nivo 2 ne postoji. To je greška od jedne linije koju bi tabela podataka spriječila.
- **Vrijednosti u kodu pored praznih assetova.** Beaconov interval sakupljanja je konstanta u komponenti, dok je `ExtractionBeaconSO` prazan. Attacherova cijena nadogradnje je `return 80f;` s komentarom da je kasnije treba prebaciti u podatke.
- **Pretplata na događaj koju moram ponovo provjeriti.** Attacher pretplaćuje svoju metodu za pojačanje na događaj "Attacher nadograđen" i nikad se ne odjavljuje. Taj događaj šalje sam nadograđeni Attacher, a ne toranj na koji je zakačen.

## Šta bih promijenio

- Zamijeniti polja po nivoima jednom listom podataka o nivoima za svaki toranj, pa da dodavanje nivoa bude promjena podataka.
- Svakoj pretplati na događaj dati odgovarajuću odjavu u `OnDestroy`.

## Šta sam naučio

- Virtualni `IsOperational` je bio najkorisnija linija u kodu tornjeva. Posada, istraživanje i ometanje od neprijatelja svi gase tornjeve kroz njega, a tornjevi ne znaju zašto.
- Ponovno korištenje onoga što drugi sistem već izračuna, kao što Deceiver spaja postojeće rute, bilo je jednostavnije i pouzdanije od pisanja nove logike.
"""

CREW_EN = """[Screenshot: the crew management screen with members assigned to Research, Maintenance, Defense and Detox]

## The problem

I wanted the player's power to cost something besides currency. Harvesting more liquid should make the base more dangerous, and the people running it should get tired. That became two systems, crew and toxicity. They only work because they push on each other and on the towers. This post covers 10 to 22 July.

## Timeline

- **10 Jul:** a six-line `CrewMember` class and a crew data asset, in the same commit as the first Extraction Beacon.
- **15 Jul:** crew logic and the management UI (department slots, member cards), then toxicity, committed as "crew and toxicity added with bugs".
- **18 Jul:** `DefenseStatus`, which connects the Defense slot to the attack towers, then the Research Lab.

## The crew

There are four slots: Research, Maintenance and Defense are work, and Detox is rest. Each crew member has 1 to 5 stars in each work department, so who you put where matters. Stress is ticked every frame, and the slot decides the direction:

```csharp
public void TickStressRealtime(float deltaTime, float situationalModifier)
{
    if (CurrentAssignment == DepartmentType.Detox)
        AdjustStress(-Data.StressRecoveryPerSecond * situationalModifier * deltaTime);
    else if (CurrentAssignment == DepartmentType.Unassigned)
        AdjustStress(-Data.StressRecoveryPerSecond * PASSIVE_RECOVERY_PERCENTAGE * situationalModifier * deltaTime);
    else
        AdjustStress(Data.StressBuildUpPerSecond * Data.StressTolerance * situationalModifier * deltaTime);
}
```

Working builds stress, scaled by each member's tolerance. Detox recovers it, and when a member reaches zero they leave Detox on their own. Sitting unassigned recovers too, but slowly.

## Empty slots switch things off

The crew doesn't add bonuses on top of a working base. An empty slot turns its part of the base off. Two small static classes publish the state every frame:

```csharp
public static void UpdateResearchModifiers(CrewMember researcher)
{
    if (researcher == null || researcher.CurrentAssignment != DepartmentType.Research)
    {
        IsLockedDown = true;
        EfficiencyMultiplier = 0f;
        return;
    }
    IsLockedDown = false;
    EfficiencyMultiplier = 1f;
}
```

With nobody in Research, the lab stops and so do the beacons, which check `ResearchStatus.IsLockedDown`. With nobody in Defense, attack towers don't fire. With a stressed defender, fire rate and turn speed drop gradually, and close to burnout mortars start to miss. Maintenance stars cut how much toxicity comes in and speed up how fast it clears.

## Toxicity

Liquids are stored in tanks. When a tank is full, the extra is vented into the air, and venting raises toxicity. Toxicity clears slowly on its own, and moves through five stages:

```csharp
public enum ToxicityStage { Stable, Leaking, Critical, Meltdown, Rapture }
```

From Critical, the game rolls for tower misfires on a timer. In Meltdown, cells next to your towers can become contaminated, and you can't build on them. At the top, Rapture drains part of every tank, contaminates a tower's cell, adds a large stress spike to the whole crew, and resets toxicity to the Critical level, so the player gets one chance to recover.

[Screenshot: the toxicity bar in Leaking, Critical and Meltdown, and contaminated cells next to towers]

## How the loop closes

Harvest a lot and the tanks fill up. Full tanks vent, and venting raises toxicity. To keep toxicity down you need a good engineer in Maintenance, but every working slot builds stress, and stress weakens Defense. Rapture then hits stress again. None of these systems knows about the others' internals. They meet through a few numbers: stars, stress and the toxicity value.

[Screenshot: a diagram of the loop: harvesting, tanks, toxicity, crew stress, defense]

## What went wrong

- **Code that does nothing yet.** `CrewMember` declares a burnout event that is never raised, and `ApplyDepartmentModifiers` calculates a research multiplier and then throws it away. Both are leftovers from an earlier plan.
- **An event with no listener.** The misfire roll fires `OnMisfireTriggered`, but no tower listens to it yet, so Critical has no visible effect on towers.
- **Stress only reaches Defense.** Research and Maintenance read stars only, so a stressed researcher works as well as a rested one.
- **Thresholds in two styles.** Toxicity thresholds are inspector fields, but the stress bands in `DefenseStatus` are written in code.

## What I'd change

- Finish the misfire hook in the attack tower, and give Research and Maintenance a stress curve like Defense has.
- Move the stress bands into the crew data, so one asset tunes them like the toxicity thresholds.
- Delete the unused burnout event and multiplier.

## What I learned

- Making an empty slot switch a system off, not just make it weaker, turned the crew from a stat bonus into a decision.
- Systems that talk through a few shared numbers are much easier to balance than systems that call each other.
"""

CREW_BS = """[Snimak ekrana: ekran za upravljanje posadom s članovima raspoređenim u Research, Maintenance, Defense i Detox]

## Problem

Htio sam da igračeva moć košta nešto osim valute. Više sakupljene tečnosti treba bazu učiniti opasnijom, a ljudi koji je vode trebaju se umarati. To su postala dva sistema, posada i toksičnost. Rade samo zato što pritišću jedan drugog i tornjeve. Ovaj tekst pokriva period od 10. do 22. jula.

## Vremenska linija

- **10. jul:** klasa `CrewMember` od šest linija i asset s podacima o posadi, u istom commitu kao prvi Extraction Beacon.
- **15. jul:** logika posade i UI za upravljanje (slotovi odjela, kartice članova), a zatim toksičnost, s porukom "crew and toxicity added with bugs".
- **18. jul:** `DefenseStatus`, koji povezuje slot Defense s napadačkim tornjevima, a zatim istraživačka laboratorija.

## Posada

Postoje četiri slota: Research, Maintenance i Defense su rad, a Detox je odmor. Svaki član posade ima od 1 do 5 zvjezdica u svakom radnom odjelu, pa je bitno ko gdje radi. Stres se računa svaki frame, a slot određuje smjer:

```csharp
public void TickStressRealtime(float deltaTime, float situationalModifier)
{
    if (CurrentAssignment == DepartmentType.Detox)
        AdjustStress(-Data.StressRecoveryPerSecond * situationalModifier * deltaTime);
    else if (CurrentAssignment == DepartmentType.Unassigned)
        AdjustStress(-Data.StressRecoveryPerSecond * PASSIVE_RECOVERY_PERCENTAGE * situationalModifier * deltaTime);
    else
        AdjustStress(Data.StressBuildUpPerSecond * Data.StressTolerance * situationalModifier * deltaTime);
}
```

Rad gradi stres, prema toleranciji svakog člana. Detox ga smanjuje, a kad član dođe do nule, sam napušta Detox. Član bez zaduženja se također oporavlja, ali sporo.

## Prazni slotovi gase stvari

Posada ne dodaje bonuse na bazu koja već radi. Prazan slot gasi svoj dio baze. Dvije male statičke klase objavljuju stanje svaki frame:

```csharp
public static void UpdateResearchModifiers(CrewMember researcher)
{
    if (researcher == null || researcher.CurrentAssignment != DepartmentType.Research)
    {
        IsLockedDown = true;
        EfficiencyMultiplier = 0f;
        return;
    }
    IsLockedDown = false;
    EfficiencyMultiplier = 1f;
}
```

Bez nikoga u Researchu, laboratorija staje, a s njom i beaconi, koji provjeravaju `ResearchStatus.IsLockedDown`. Bez nikoga u Defenseu, napadački tornjevi ne pucaju. Kad je branilac pod stresom, brzina paljbe i okretanja postepeno padaju, a blizu pregorijevanja minobacači počinju promašivati. Zvjezdice u Maintenanceu smanjuju koliko toksičnosti ulazi i ubrzavaju njeno čišćenje.

## Toksičnost

Tečnosti se čuvaju u rezervoarima. Kad je rezervoar pun, višak se ispušta u zrak, a ispuštanje podiže toksičnost. Toksičnost se sama polako čisti i prolazi kroz pet faza:

```csharp
public enum ToxicityStage { Stable, Leaking, Critical, Meltdown, Rapture }
```

Od faze Critical igra na tajmer baca kocku za zastoje tornjeva. U fazi Meltdown ćelije pored tvojih tornjeva mogu postati kontaminirane i na njima se ne može graditi. Na vrhu, Rapture prazni dio svakog rezervoara, kontaminira ćeliju jednog tornja, cijeloj posadi dodaje veliki skok stresa i vraća toksičnost na nivo faze Critical, pa igrač dobije jednu priliku da se oporavi.

[Snimak ekrana: traka toksičnosti u fazama Leaking, Critical i Meltdown i kontaminirane ćelije pored tornjeva]

## Kako se krug zatvara

Sakupljaš mnogo i rezervoari se pune. Puni rezervoari ispuštaju višak, a to podiže toksičnost. Da je držiš niskom, treba ti dobar inženjer u Maintenanceu, ali svaki radni slot gradi stres, a stres slabi Defense. Rapture onda opet udara na stres. Nijedan od ovih sistema ne zna kako su drugi napravljeni iznutra. Susreću se kroz nekoliko brojeva: zvjezdice, stres i vrijednost toksičnosti.

[Snimak ekrana: dijagram kruga: sakupljanje, rezervoari, toksičnost, stres posade, odbrana]

## Šta je pošlo po zlu

- **Kod koji još ništa ne radi.** `CrewMember` deklariše događaj za pregorijevanje koji se nikad ne pokreće, a `ApplyDepartmentModifiers` izračuna množilac za istraživanje i onda ga baci. Oboje su ostaci ranijeg plana.
- **Događaj bez slušaoca.** Bacanje kocke za zastoj pokreće `OnMisfireTriggered`, ali nijedan toranj ga još ne sluša, pa faza Critical nema vidljiv efekat na tornjeve.
- **Stres stiže samo do Defensea.** Research i Maintenance čitaju samo zvjezdice, pa istraživač pod stresom radi jednako dobro kao odmoran.
- **Pragovi u dva stila.** Pragovi toksičnosti su polja u inspektoru, ali razredi stresa u `DefenseStatus` napisani su u kodu.

## Šta bih promijenio

- Završiti vezu za zastoje u napadačkom tornju i dati Researchu i Maintenanceu krivulju stresa kakvu ima Defense.
- Prebaciti razrede stresa u podatke o posadi, da ih jedan asset podešava kao pragove toksičnosti.
- Obrisati nekorišteni događaj za pregorijevanje i množilac.

## Šta sam naučio

- To što prazan slot gasi sistem, a ne samo ga slabi, pretvorilo je posadu iz bonusa na statistiku u odluku.
- Sisteme koji komuniciraju kroz nekoliko zajedničkih brojeva mnogo je lakše balansirati nego sisteme koji direktno zovu jedan drugog.
"""

ENEMY_EN = """[Screenshot: one of each enemy class lined up on a route]

## The problem

Until August, enemies only differed in health and speed. A tower defence gets interesting when each enemy asks for a different answer: something you can't see, something that weakens your towers, something that multiplies when it dies. The "enemy-types" pull request (20 to 24 August) added seven classes. The open question was how to build them without seven enemy scripts that slowly drift apart.

## The seven classes

The enemy type is an enum, and the comments next to it are the designs from my board:

```csharp
public enum EnemyType {
    Light,      // Drones, Scavengers, basic cannon fodder
    Medium,     // Hazmat Infantry, Contractors
    Tank,       // Vulcanex Enforcer, Heavy Riot Troopers
    Camo,       // Ghost Scavenger, Shadow Sampler, Cloaked Enforcer
    Disruptor,  // Chemical Leech, Auto-Sampler Turret
    Decoy,      // Roller Echo, Nexium Echoes
    Elite       // Nexium Abomination, Government Agent
}
```

## One script, switches in data

There is still only one `Enemy` component. Each behaviour is switched on in that enemy's `EnemySO` asset, grouped by header: elemental affinities, stealth and theft, a slow aura, a lockdown aura, and splitting on death. A Ghost Scavenger is just an asset with stealth and theft turned on. I can combine behaviours without writing code.

Elements are part of the identity too. An enemy can have an identity element (what it drops), a weakness that takes extra damage, and a healing element that heals it instead of hurting it. Each one can be fixed or picked at random when the enemy spawns, so the same design can need a different answer in different runs.

```csharp
if (data.CanHeal && HealingElement != ElementType.None && sourceElement == HealingElement)
{
    Heal(damageAmount);
    return;
}
float mitigatedDamage = isTrueDamage ? damageAmount : damageAmount / data.ResistanceMultiplier;
bool isWeakness = sourceElement != ElementType.None && sourceElement == data.WeaknessElement;
```

## Counterplay, class by class

- **Camo:** stealthed enemies swap to a cloak material and can't be targeted. The Spotter tower was added in the same commit as camo (24 August). It pulses and reveals them for a few seconds, then they hide again.
- **Disruptor:** pulses every few seconds over the cells around it. One aura slows the fire rate of nearby attack towers, and the other locks towers down completely for a short time. The answer is range: kill it before it reaches your towers.
- **Decoy:** splits into smaller enemies when it dies. The children start where the parent died and continue on the rest of its route, so splash damage is the answer.
- **Thieves:** some enemies steal liquid from your tanks if they reach the end.

[Screenshot: a camouflaged enemy before and after a Spotter reveals it]

The aura pulses find cells in rings on the hex grid, which reuses the neighbour lookups from the map:

```csharp
for (int ring = 0; ring < range; ring++)
{
    var next = new List<HexCell>();
    foreach (HexCell cell in frontier)
        foreach (HexDirection direction in Enum.GetValues(typeof(HexDirection)))
        {
            HexCell neighbor = cell.GetNeighbor(direction);
            if (neighbor == null || !visited.Add(neighbor)) continue;
            next.Add(neighbor);
            yield return neighbor;
        }
    frontier = next;
}
```

[Screenshot: a Disruptor pulse slowing the towers around it]

## Splitting and the pool

Splitting broke the pool. All enemies are created up front, but the children of a Decoy aren't in any wave. The pool now also preloads `count × SplitCount` children for every group whose enemy splits, and the spawner takes children from that second pool.

[Screenshot: a Decoy splitting into its children]

## What went wrong

- **An ID that isn't saved.** Enemy and crew assets set their ID in `OnValidate`, which only runs in the editor, and the field is private without `[SerializeField]`, so Unity doesn't store it. It works while I play in the editor, but in a build the ID would be empty. Crew loading depends on that ID, so this needs fixing before a release build.
- **A possible division by zero.** Resistance divides the damage, and the inspector slider allows 0.
- **One script getting long.** `Enemy.cs` is over 700 lines because every behaviour lives in it, guarded by flags.

## What I'd change

- Serialize the IDs and set them once with an editor tool.
- Clamp resistance above zero, or turn it into a multiplier.
- Split behaviours into small components (stealth, aura, splitter) that the asset adds, so an enemy only carries the code it uses.

## What I learned

- Designing each enemy around the answer it demands gave every tower a reason to exist.
- Flags in data are a fast way to start. The same approach that made this quick is now the reason the script is so long.
"""

ENEMY_BS = """[Snimak ekrana: po jedan neprijatelj iz svake klase poredan na ruti]

## Problem

Do augusta su se neprijatelji razlikovali samo po zdravlju i brzini. Tower defence postaje zanimljiv kad svaki neprijatelj traži drugačiji odgovor: nešto što ne vidiš, nešto što slabi tvoje tornjeve, nešto što se umnoži kad umre. Pull request "enemy-types" (20. do 24. augusta) dodao je sedam klasa. Otvoreno pitanje je bilo kako ih napraviti bez sedam skripti za neprijatelje koje se polako udaljavaju jedna od druge.

## Sedam klasa

Vrsta neprijatelja je enum, a komentari pored su dizajni s moje table:

```csharp
public enum EnemyType {
    Light,      // Drones, Scavengers, basic cannon fodder
    Medium,     // Hazmat Infantry, Contractors
    Tank,       // Vulcanex Enforcer, Heavy Riot Troopers
    Camo,       // Ghost Scavenger, Shadow Sampler, Cloaked Enforcer
    Disruptor,  // Chemical Leech, Auto-Sampler Turret
    Decoy,      // Roller Echo, Nexium Echoes
    Elite       // Nexium Abomination, Government Agent
}
```

## Jedna skripta, prekidači u podacima

I dalje postoji samo jedna komponenta `Enemy`. Svako ponašanje se uključuje u `EnemySO` assetu tog neprijatelja, grupisano po naslovima: elementarne sklonosti, nevidljivost i krađa, aura usporavanja, aura blokade i dijeljenje pri smrti. Ghost Scavenger je samo asset s uključenom nevidljivošću i krađom. Ponašanja mogu kombinovati bez pisanja koda.

I elementi su dio identiteta. Neprijatelj može imati element identiteta (ono što ispusti), slabost koja prima dodatnu štetu i element koji ga liječi umjesto da ga povrijedi. Svaki može biti fiksan ili nasumično izabran pri pojavljivanju, pa isti dizajn u različitim partijama može tražiti drugačiji odgovor.

```csharp
if (data.CanHeal && HealingElement != ElementType.None && sourceElement == HealingElement)
{
    Heal(damageAmount);
    return;
}
float mitigatedDamage = isTrueDamage ? damageAmount : damageAmount / data.ResistanceMultiplier;
bool isWeakness = sourceElement != ElementType.None && sourceElement == data.WeaknessElement;
```

## Kontra-igra, klasa po klasa

- **Camo:** skriveni neprijatelji mijenjaju materijal u maskirni i ne mogu se gađati. Spotter toranj dodan je u istom commitu kao camo (24. augusta). Pulsira i otkriva ih na nekoliko sekundi, a onda se ponovo sakriju.
- **Disruptor:** svakih nekoliko sekundi pulsira po ćelijama oko sebe. Jedna aura usporava paljbu obližnjih napadačkih tornjeva, a druga ih nakratko potpuno blokira. Odgovor je domet: ubij ga prije nego stigne do tvojih tornjeva.
- **Decoy:** kad umre, dijeli se na manje neprijatelje. Djeca kreću s mjesta gdje je roditelj umro i nastavljaju ostatkom njegove rute, pa je odgovor šteta po području.
- **Lopovi:** neki neprijatelji kradu tečnost iz tvojih rezervoara ako stignu do kraja.

[Snimak ekrana: kamuflirani neprijatelj prije i nakon što ga Spotter otkrije]

Pulsevi aura pronalaze ćelije u prstenovima na hex mreži, ponovo koristeći traženje susjeda iz mape:

```csharp
for (int ring = 0; ring < range; ring++)
{
    var next = new List<HexCell>();
    foreach (HexCell cell in frontier)
        foreach (HexDirection direction in Enum.GetValues(typeof(HexDirection)))
        {
            HexCell neighbor = cell.GetNeighbor(direction);
            if (neighbor == null || !visited.Add(neighbor)) continue;
            next.Add(neighbor);
            yield return neighbor;
        }
    frontier = next;
}
```

[Snimak ekrana: puls Disruptora koji usporava tornjeve oko sebe]

## Dijeljenje i pool

Dijeljenje je pokvarilo pool. Svi neprijatelji se prave unaprijed, ali djeca Decoya nisu ni u jednom valu. Pool sada za svaku grupu čiji se neprijatelj dijeli unaprijed pravi i `count × SplitCount` djece, a spawner ih uzima iz tog drugog poola.

[Snimak ekrana: Decoy koji se dijeli na djecu]

## Šta je pošlo po zlu

- **ID koji se ne snima.** Asseti neprijatelja i posade postavljaju svoj ID u `OnValidate`, koji radi samo u editoru, a polje je privatno bez `[SerializeField]`, pa ga Unity ne čuva. Radi dok igram u editoru, ali u buildu bi ID bio prazan. Učitavanje posade zavisi od tog ID-a, pa ovo treba popraviti prije release builda.
- **Moguće dijeljenje nulom.** Otpornost dijeli štetu, a klizač u inspektoru dozvoljava 0.
- **Jedna skripta postaje duga.** `Enemy.cs` ima preko 700 linija jer svako ponašanje živi u njoj, iza prekidača.

## Šta bih promijenio

- Serijalizovati ID-eve i postaviti ih jednom alatom u editoru.
- Ograničiti otpornost iznad nule ili je pretvoriti u množilac.
- Razdvojiti ponašanja u male komponente (nevidljivost, aura, dijeljenje) koje asset dodaje, pa da neprijatelj nosi samo kod koji koristi.

## Šta sam naučio

- Dizajniranje svakog neprijatelja oko odgovora koji traži dalo je svakom tornju razlog da postoji.
- Prekidači u podacima su brz način da se počne. Isti pristup koji je ovo ubrzao sada je razlog zašto je skripta tako duga.
"""

MIRO_EN = """[Screenshot: an overview of the whole design board]

## Why a board

ArcaneTD is a set of systems that lean on each other: towers, elements, enemies, the Middleman, the crew and toxicity. Working alone, the risk isn't that I can't write a system. It's that I write one and only later see what it breaks. So before most systems existed in code, they existed on a Miro board.

## What's on it

The board is one large diagram, about 115 shapes connected by 60 arrows. It has three kinds of content:

- **Tower sheets.** One card per tower with starting numbers. The cannon, for example: direct hit 50, splash 20, 0.30 shots per second, range 10.
- **The enemy roster by stage of the game.** "Early Game Enemies (Waves 1-3)", "Mid Game Enemies (Waves 4-7)" and so on. Each enemy has a role, a look and what happens when it dies.
- **Systems and cards.** The Middleman, loyalty, crew and toxicity, connected by arrows to what they affect. Risk cards are written as a benefit line and a risk line, so every card idea has to answer what it costs.

[Screenshot: one tower sheet on the board]

## From board to code

Most systems moved from the board into ScriptableObjects. Starting numbers go into the asset and get tuned in play, not on the board. The enemy roster became the `EnemyType` enum. The comments in the code still list the designs from the board (Drones and Scavengers under Light, Chemical Leech under Disruptor). The wave bands became the structure of the level assets: levels, waves, mini-waves and groups.

The board also shows what I haven't built. The Spotter's card says it "reveals invisible enemies, marks high-value targets". The code does the first half. Marking targets is still only on the board.

[Screenshot: an enemy card on the board next to its EnemySO asset in the inspector]

## What the board is not

The board isn't the source of truth. The code is. Some ideas on the board are proposals that may never ship, and some details changed once I could play them. When this site or a devlog describes the game, it describes what is in the code, not what is on the board.

## What I'd change

- Tag every shape as built, in progress or proposed. Right now only I know which is which.
- Add a date when a design changes, so the board has a history like the git log.
- Keep the starting numbers on the board in step with the assets, or remove them once the asset exists.

## What I learned

- Drawing the arrows between systems before writing code showed most of the dependencies early. Those arrows became the events in the code.
- Writing a cost next to every benefit, even in a sketch, kept the game focused on trade-offs.
"""

MIRO_BS = """[Snimak ekrana: pregled cijele dizajn table]

## Zašto tabla

ArcaneTD je skup sistema koji se oslanjaju jedan na drugi: tornjevi, elementi, neprijatelji, Middleman, posada i toksičnost. Kad radim sam, rizik nije da ne mogu napisati sistem. Rizik je da ga napišem i tek kasnije vidim šta je pokvario. Zato je većina sistema, prije nego što je postojala u kodu, postojala na Miro tabli.

## Šta je na njoj

Tabla je jedan veliki dijagram, oko 115 oblika povezanih sa 60 strelica. Ima tri vrste sadržaja:

- **Kartice tornjeva.** Po jedna kartica za svaki toranj s početnim brojevima. Na primjer top: direktni pogodak 50, šteta po području 20, 0,30 pucnja u sekundi, domet 10.
- **Spisak neprijatelja po fazi igre.** "Early Game Enemies (Waves 1-3)", "Mid Game Enemies (Waves 4-7)" i tako dalje. Svaki neprijatelj ima ulogu, izgled i šta se dešava kad umre.
- **Sistemi i karte.** Middleman, odanost, posada i toksičnost, povezani strelicama s onim na šta utiču. Rizične karte su napisane kao red koristi i red rizika, pa svaka ideja za kartu mora odgovoriti koliko košta.

[Snimak ekrana: jedna kartica tornja na tabli]

## Od table do koda

Većina sistema je s table prešla u ScriptableObjecte. Početni brojevi idu u asset i podešavaju se igranjem, a ne na tabli. Spisak neprijatelja postao je enum `EnemyType`. Komentari u kodu i dalje navode dizajne s table (Drones i Scavengers pod Light, Chemical Leech pod Disruptor). Razredi valova postali su struktura assetova za nivoe: nivoi, valovi, mini-valovi i grupe.

Tabla pokazuje i šta još nisam napravio. Na Spotterovoj kartici piše da "otkriva nevidljive neprijatelje i označava vrijedne mete". Kod radi prvu polovinu. Označavanje meta je zasad samo na tabli.

[Snimak ekrana: kartica neprijatelja na tabli pored njegovog EnemySO asseta u inspektoru]

## Šta tabla nije

Tabla nije izvor istine. Kod jeste. Neke ideje na tabli su prijedlozi koji možda nikad neće ući u igru, a neki detalji su se promijenili kad sam ih mogao igrati. Kad ova stranica ili devlog opisuju igru, opisuju ono što je u kodu, a ne ono što je na tabli.

## Šta bih promijenio

- Označiti svaki oblik kao napravljen, u izradi ili prijedlog. Trenutno samo ja znam šta je šta.
- Dodati datum kad se dizajn promijeni, da tabla ima historiju kao git log.
- Početne brojeve na tabli držati usklađenim s assetima ili ih ukloniti kad asset postoji.

## Šta sam naučio

- Crtanje strelica između sistema prije pisanja koda rano je pokazalo većinu zavisnosti. Te strelice su postale događaji u kodu.
- Pisanje cijene pored svake koristi, čak i u skici, držalo je igru usmjerenom na kompromise.
"""

MORE_POSTS = {
    "waves-and-enemy-movement": {
        "num": 2, "date": "2026-03-28", "project": "arcanetd",
        "title": {"en": "Waves as data, and walking on a map that isn't flat",
                  "bs": "Valovi kao podaci i hodanje po mapi koja nije ravna"},
        "summary": {"en": "Moving the game onto hexes, building waves in the editor, swarms, and an elevation bug I first covered with a magic number.",
                    "bs": "Prebacivanje igre na heksagone, pravljenje valova u editoru, rojevi i greška s visinom koju sam prvo prekrio magičnim brojem."},
        "body": {"en": WAVES_EN, "bs": WAVES_BS},
    },
    "four-support-towers": {
        "num": 3, "date": "2026-07-09", "project": "arcanetd",
        "title": {"en": "Four support towers on one base class",
                  "bs": "Četiri tornja podrške na jednoj osnovnoj klasi"},
        "summary": {"en": "Spotter, Deceiver, Extraction Beacon and Attacher: what they share, how the Deceiver reroutes enemies, and the fork bug that hid half the forks.",
                    "bs": "Spotter, Deceiver, Extraction Beacon i Attacher: šta dijele, kako Deceiver preusmjerava neprijatelje i greška koja je sakrila pola račvanja."},
        "body": {"en": SUPPORT_EN, "bs": SUPPORT_BS},
    },
    "crew-stress-and-toxicity": {
        "num": 4, "date": "2026-07-22", "project": "arcanetd",
        "title": {"en": "Crew, stress and toxicity: three systems that push on each other",
                  "bs": "Posada, stres i toksičnost: tri sistema koji pritišću jedan drugog"},
        "summary": {"en": "Why an empty crew slot switches part of the base off, how venting liquid feeds toxicity, and what is still unfinished.",
                    "bs": "Zašto prazan slot posade gasi dio baze, kako ispuštanje tečnosti hrani toksičnost i šta još nije završeno."},
        "body": {"en": CREW_EN, "bs": CREW_BS},
    },
    "seven-enemy-classes": {
        "num": 6, "date": "2026-08-24", "project": "arcanetd",
        "title": {"en": "Seven enemy classes from one Enemy script",
                  "bs": "Sedam klasa neprijatelja iz jedne Enemy skripte"},
        "summary": {"en": "Camo, disruptors and decoys built as switches in data, the counter each one asks for, and a save bug I found while writing.",
                    "bs": "Camo, disruptori i mamci napravljeni kao prekidači u podacima, odgovor koji svaki traži i greška sa snimanjem koju sam našao dok sam pisao."},
        "body": {"en": ENEMY_EN, "bs": ENEMY_BS},
    },
    "designing-on-a-board": {
        "num": 7, "date": "2026-10-17", "project": "arcanetd",
        "title": {"en": "Designing on a board before writing code",
                  "bs": "Dizajniranje na tabli prije pisanja koda"},
        "summary": {"en": "How a Miro board with tower sheets, an enemy roster and system arrows turned into ScriptableObjects, and why the code stays the source of truth.",
                    "bs": "Kako je Miro tabla s karticama tornjeva, spiskom neprijatelja i strelicama između sistema postala ScriptableObjecti i zašto kod ostaje izvor istine."},
        "body": {"en": MIRO_EN, "bs": MIRO_BS},
    },
}
