---
name: nes-teenage-mutant-ninja-turtles-ii-the-arcade-game-usa
description: Plays Teenage Mutant Ninja Turtles II - The Arcade Game (USA) on the Nintendo Entertainment System through RetroArch's MCP server. Use when GET_STATUS reports Teenage Mutant Ninja Turtles II - The Arcade Game (USA) or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST mcp__retroarch__WATCH mcp__retroarch__RUN_UNTIL mcp__retroarch__STEPS mcp__retroarch__GET_FRAME
metadata:
  game: "Teenage Mutant Ninja Turtles II - The Arcade Game (USA)"
  system: "Nintendo - Nintendo Entertainment System"
  cores: "fceumm_libretro"
  crc32: "A9217EA2"
---

# Teenage Mutant Ninja Turtles II - The Arcade Game

A side-scrolling beat-'em-up: a turtle walks right through each scene,
fighting waves of Foot soldiers. Each wave locks the screen until it is
beaten; then the scene scrolls on to the next.

## Quick start

1. `GET_STATUS`, then read `0x06F9`, 7 bytes: `FE 00 3F FE 00 00 FF` is this
   game (Confirm the game).
2. Setup's steps reach Scene 1 with the chosen turtle: the title, the
   turtle, then `until 3c == 3` through the intro.
3. `WATCH px 47e gy 4a2 act 412 face 436 hp 568 lives 4d score 3f0
   e7x 485 e7g 4a9 e7h 56f e9x 487 e9g 4ab e9h 571`, once; again after
   loading content. Labels from
   an earlier session survive a state load and count toward the 16: turn
   any others off first (`<label> off`).
4. Fight each wave in short `STEPS` calls: line up, face, step in, chain
   three swings, twice. Stop on a health drop (`stop 568 < <hp - 4>`), not
   only on `== 0`: a hold drained 38 health inside one call. Then walk right.
5. A `checkpoint` step first in each call before a wave; `STATE rollback`
   after a death. Save to slots 990-999 at each cleared wave.
6. Each scene in detail, read when it starts: Scene 1 - bombs, route,
   boss: [references/scene-1.md](references/scene-1.md). Scene 2 - route,
   manhole covers, firebombs, the way past the street's dead ends, and
   the boss: [references/scene-2.md](references/scene-2.md).

## Confirm the game

Call `GET_STATUS`. Its reply should name `nes` and
`Teenage Mutant Ninja Turtles II - The Arcade Game (USA)`. If nothing is
loaded, follow Setup first.

Then read `0x06F9`, 7 bytes. It is `FE 00 3F FE 00 00 FF` from the title
screen on: the end of the game's palette upload buffer, which starts with
`3F` at `0x06D8`. It held on the title, the turtle select screen, during the
intro and in play.

- Memory matches: go on. If the name differs, the ROM is probably renamed:
  run the CRC check if you can, and tell the user what you found.
- Memory doesn't match: another game, or a hack of this one. Stop and tell
  the user what `GET_STATUS` reported.
- The read fails: run the CRC check. If it matches, go on to Setup to fix the
  core. Ask the user only if you can verify neither the memory nor the CRC.

**CRC check**, when you can read files: find the loaded file's path in
`GET_PLAYLIST "Nintendo - Nintendo Entertainment System.lpl"` by the name
`GET_STATUS` reported; if it isn't there, skip the check. For a `.zip#` path,
read the `.nes` inside. Skip the 16-byte iNES header; the CRC32 of the rest
should be `metadata.crc32`. A mismatch means another dump, revision or hack:
go on, and tell the user that addresses may differ.

## Setup

Use `fceumm_libretro`, the only core this skill was tested with. Its map
places system RAM at `0x0000`-`0x07FF`.

- **Nothing loaded:** `LIST_CORES <content path>` lists the installed cores
  that can run the ROM. `LOAD_CONTENT` with `fceumm_libretro` and `paused`
  on. RAM reads `FF` until a frame has run.
- **Check the memory:** `GET_MEMORY_MAP` must have regions covering
  `0x0000`-`0x07FF` with an empty `space` (fceumm lists two of `0x400`). Its
  other regions (`PPUREG`, `NTARAM`, `PALRAM`, `OAM`) are video memory this
  skill doesn't use. If the map is missing or short, or lists only space
  `core`, tell the user.

`0x0018` tells the screens apart: `01` title, `04` turtle select, `05` intro
and play. Within `05`, `0x003C` is `01` during the intro text, `06` as the
scene starts, and `03` in play.

1. `STEPS run 300` reaches the title (`1 TURTLE`, `2 TURTLES`; the cursor
   starts on `1 TURTLE`). The title ignores Start for about two seconds after
   it appears, and a 4-frame press is often dropped, so press it repeatedly
   and stop on the select screen: `STEPS stop 18 == 4; press 1 start 10;
   run 30`, with the `press` and `run` repeated 8 times.
2. `0x0018` turns `04` a few frames before the select screen takes input: a
   `down` pressed straight away was dropped. Wait for the cursor first:
   `STEPS until 47e == 52`. The cursor (`0x0033`) starts on Leonardo.
   `0x0033`: `00` Leonardo (top left), `01` Michelangelo (top right), `02`
   Donatello (bottom left), `03` Raphael (bottom right). Ask the user which
   turtle they want; suggest Donatello, whose bo reaches farthest. Move with
   the D-pad and choose with `a`; Start doesn't choose. Both take effect
   some frames after the press, so end each on the change rather than
   reading straight after: `STEPS press 1 down 4; until 33 == 2` reaches
   Donatello, then `STEPS press 1 a 4; until 18 == 5` chooses him. One press
   each is enough; a second can overshoot. Raphael: `STEPS until 47e == 52;
   press 1 down 4; until 33 == 2; run 10; press 1 right 4; until 33 == 3`.
   Michelangelo: `STEPS until 47e == 52; press 1 right 4; until 33 == 1`.
   Leonardo: `STEPS until 47e == 52; run 10; press 1 a 4; until 18 == 5`.
   The `run 300` and the Start presses don't fit one request together
   (540 frames): send them as two.
3. An intro and a "SCENE 1" card play for about 820 frames. Pressing Start
   doesn't skip them. `STEPS until 3c == 3` ends on the first frame of play;
   one request runs 540 frames at most, so send it again until it answers
   `done`. Lives (`0x004D`) become `02` and health `3C` (60) during the
   intro. The turtle starts at X 128, Y 176, moves at once, and a Foot
   soldier is already on its way.

**Two players.** On the title, `select` (10 frames, about 140 frames after
the title appeared) moves the cursor to `2 TURTLES`, and a second `select`
moves it back; `down` does nothing. The cursor's Y (`0x046C`) reads `B4` on
`1 TURTLE` and `C4` on `2 TURTLES`. Start then opens the select screen with
two cursors: player 1's (`0x0033`) on Leonardo and player 2's (`0x0034`) on
Michelangelo. `0x0047` reads `01` for two players, but only some frames
after `0x0018` turns `04`: read straight away, it still showed `00`
(`STEPS run 60` first). Player 2
moves with `press 2 ...`: `STEPS press 2 down 4; until 34 == 3; run 10;
press 2 left 4; until 34 == 2` reached Donatello. Each player chooses with
their own `a`. In play, player 1 starts at X 128 and player 2 at X 92.

**Continue.** When both players are out of lives, `0x003C` reads `07` and a
`CONTINUE` / `END` menu shows the continues left (`0x03D3`, `03` at the
start; it read `02` after one was used). Player 1's Start on `CONTINUE`
brings the players back with lives `02` and health 60, keeps the score,
and restarts the current scene from its beginning: Scene 1 with two
players, Scene 2 with one. In one player, GAME OVER showed about 230
frames after the last life's health reached `00`, and the menu about 500
frames after that. A player whose lives ran out while the other still
plays reads `FF` in their lives byte, and their own Start didn't bring
them back.

## Controls

Measured at 60 frames per second, with Donatello unless noted.

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Walk   | `left`, `right` | About 1 px per frame. Turns the turtle at once; `press 1 left 1` turns him without moving. |
| Step in depth | `up`, `down` | About 0.6 px per frame; moves the ground line (`0x04A2`). |
| Attack | `b` | One swing locks him for about 17 frames (`0x0412` is `02`). Three in a row, `b 4; run 10` each, chain into a longer thrust: Donatello's third reached an enemy 55 px away. See Reach for the others. |
| Jump   | `a` | Lands 57 frames after a 4-frame press, peaking about 88 px up. Moves only about 6 px sideways even with a direction held. Clears the Scene 1 boss's charge; doesn't dodge shuriken (hit mid-air, `0x0412` `05`). `right+a` then `b` mid-air (a jump kick) moved 3 px and didn't reach a boss 43 px away. |
| Break a hold | `left+b`, `right+b` alternately | When a Foot soldier holds him (`0x0412` is `04`), 6 alternating 3-frame presses broke free. The mash also hits the holder: twice it took a soldier from `04` to `02`, and once finished one. |

**Reach.** Scene 1's first soldier lines up 29 px to the right of a turtle
that waits at the start (X 128, ground line 176; the soldier at X 157,
ground line 166-167). From there:

| Turtle | Weapon | Measured |
| ------ | ------ | -------- |
| Leonardo | katana | The first swing hit within 2 frames. Backing off 10 or 30 px first changed nothing: the soldier followed and was hit at 31 px each time. A second chain from 31 px without stepping in missed, and the soldier hit back. |
| Michelangelo | nunchaku | The first swing hit within 2 frames. Chain, `until 412 == 0; press 1 right 6`, chain defeated the soldier in 64 frames, taking nothing. |
| Donatello | bo | The third swing of a chain reached 55 px. |
| Raphael | sai | Chains landed at 20-33 px and missed at 44. The step-in pattern below cleared Scene 1. |

Foot soldiers stop about 29-31 px from a turtle and punch from there, and
follow him when he backs off, so every turtle meets them at that distance
and every weapon reaches it. The step-in before the second chain is what
matters, not the weapon.

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed by
`GET_MEMORY_MAP`. Objects are parallel arrays of 18 slots: an object's byte is
at the array's address plus its slot. Read each array in one call (`0x047E`,
18 bytes) rather than one large dump.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0018` | 1 | Screen: `01` title, `04` turtle select, `05` intro and play. |
| `0x003C` | 1 | Scene status: `00` on the title and select screens, `01` intro text (also the next scene's card), `06` scene starting, `03` play, `05` the turtle walking out through a door (into the boss room, and after the boss), `04` briefly after Scene 2's boss, `02` briefly on the black screen between, `07` game over (the continue menu). Object arrays and `0x007E` read `00` during `05` and `02`: don't read a death into it. |
| `0x0042` | 1 | Area: `00` Scene 1's hallway, `01` Scene 1's apartment (the boss room), `02` Scene 2's street, `03` Scene 3's sewer. |
| `0x0047` | 1 | `00` one player, `01` two players. |
| `0x0034`, `0x004E` | 1, 1 | Player 2's turtle (as `0x0033`) and lives in reserve (as `0x004D`); `FF` once player 2 is out. |
| `0x03D3` | 1 | Continues left: `03` at the start. |
| `0x0043` | 1 | `01` while player 1 is pushing the screen to scroll, `00` otherwise. |
| `0x03EA` | 1 | Enemies defeated by player 1; it rose by 1 with each defeat. |
| `0x0033` | 1 | Player 1's turtle: `00` Leonardo, `01` Michelangelo, `02` Donatello, `03` Raphael. |
| `0x004D` | 1 | Player 1's lives in reserve, as the HUD's REST shows (`02` at the start). |
| `0x03F0` | 1 | Player 1's score, last two digits, in BCD (`10` is 10 PTS). A Foot soldier is worth 1. |
| `0x007E` | 1 | Scene progress: `00` on the first frame of play, `01` a few frames later, then it rose as the scene scrolled, some dozens of frames behind the scroll. In Scene 1's hallway: `07` first staircase (bombs), `0D`-`0E` second staircase, `1A` the white ninjas, the last wave. It starts again from `00` in the boss room (`04` at the boss). |
| `0x047E` | 18 | X on screen, 0-255. Slot 0 is player 1. The screen scrolls under the turtle, so his X stays between about 128 and 230. X is one byte and wraps at both edges; `0x0556` says which side. |
| `0x0556` | 18 | Which screen the object is on: `00` this one, `01` off the right edge, `02` off the left edge. A soldier entering from the left read X 226 with `02`, then X 0 with `00`; one entering from the right read X 16 with `01`, then X 254 with `00`. |
| `0x04A2` | 18 | Ground line (depth): larger is nearer the bottom of the screen. Player 1 walks between about 135 and 190. Stays put during a jump. |
| `0x046C` | 18 | Y on screen: the ground line minus height in the air (176 standing, 88 at the top of a jump). |
| `0x0436` | 1 | Player 1 faces: `00` right, `40` left. |
| `0x0412` | 1 | Player 1's action: `00` free, `01` jumping, `02` attacking, `04` held, hit or thrown, `05` hit in the air, `06` knocked down, `10` respawning (can't be hurt; about 80 frames). |
| `0x0419` | 1 | Slot 7's action; the Scene 1 boss uses slot 7. Boss: `03` standing and charging, `02` walking, `04` just hit, `05` defeated. |
| `0x0568` | 18 | Health. Slot 0 is player 1, `3C` (60) full; a soldier's hit takes 1 to 4. Slot 2 is player 2 (it reads `3C` in a one-player game too). Enemies use the odd slots 7, 9, 11, 13, 15 and 17; a Foot soldier starts at `04`, a white ninja at `10` (16), the Scene 1 boss at `40` (64), and each of the turtle's hits takes `02`. Bombs and thrown knives read `FF`, and can't be hurt. Even slots hold extra sprites and projectiles: a blue soldier's shuriken read `80` in slot 8. A defeated soldier's knockback can briefly show `FF` in slots 8-10. |

Player 2 uses slot 2 in every array: X `0x0480`, ground line `0x04A4`, Y
`0x046E`, facing `0x0438`, action `0x0414`, health `0x056A`.

An enemy slot is live while its health is above `00`. A defeated soldier's
slot keeps its X and ground line for a while, so check health first. A new
soldier takes over a freed slot at once, so a slot reading `04` again is a
new soldier.

## Playing

`WATCH` once: `px 47e gy 4a2 act 412 face 436 hp 568 lives 4d score 3f0`,
plus X, ground line and health for the enemy slots in use. Sixteen bytes
fit, so watch two or three slots and read the others in one call each
(`0x047E`, `0x04A2`, `0x0556` and `0x0568`, 18 bytes) when a wave starts.
Watched values come back in decimal.

A wave: soldiers walk or drop in, and the screen stops scrolling until each
is beaten. For each soldier:

1. **Line up in depth.** Within about 10 of its ground line, hits land; 25 or
   more apart, they miss. `STEPS stop 4a2 <= 144; press 1 up 90` (or
   `stop 4a2 >= ...; press 1 down 90`) walks to a line and stops there.
2. **Let it come to you.** Chasing a soldier fails: they move up to about
   2.5 px per frame and back off. Face it on its line and wait until it
   walks into range, then chain: `STEPS until 412 == 0; press 1 left 2;
   until 489 >= 194; press 1 b 4; run 10; press 1 b 4; run 10; press 1 b 4;
   run 10`, where `0x0489` is the soldier's X and 194 is the turtle's X
   minus about 34. This landed again and again; one chain hit three
   soldiers on the same line at once. Chains at 29-35 px hit soldiers
   walking in and missed ones backing away. Closer than about 10 px a
   soldier holds the turtle: step away 14 frames and turn back.
3. **Face it and chain:** `STEPS until 412 == 0; press 1 left 1; press 1 b 4;
   run 10; press 1 b 4; run 10; press 1 b 4; run 10` (`right 1` to face
   right). Two hits defeat a Foot soldier.
4. Read the watched values and repeat. Keep each call to one chain, about
   50 frames.

**The step-in chain (any turtle).** A purple Foot soldier punches from about
29 px once it is on the turtle's line, so waiting for it to walk closer
gets the turtle hit first. Wait instead for its ground line to come within
about 10 (`stop 4ab >= 166` for a turtle on 176), then step in and chain
twice in one call: `STEPS stop 568 == 0; stop 571 == 0; press 1 right 5;
press 1 b 4; run 10; press 1 b 4; run 10; press 1 b 4; run 10; until 412 ==
0; press 1 right 6; press 1 b 4; run 10; press 1 b 4; run 10; press 1 b 4;
run 10`. From 29-33 px this defeated soldier after soldier through Scene 1,
often taking nothing. From 45 px or more, walk most of the way first
(`press 1 right 18` or so) and then chain. One chain hit two soldiers
standing on the same line.

**The first soldier** of Scene 1 sprints along its own line (about 2.4 px a
frame) straight past the turtle to about X 156, turns, then steps to the
turtle's line about 29 px to his right. Face right and wait for it there
rather than facing it as it enters from the left.

**Throws.** A soldier that reaches the turtle often throws him: `act` reads
`04` and his X jumps 60-140 px (to X 22 from 137, once). Read every odd
slot again after a throw; the soldiers are usually now on the other side.

**Foot soldier types.** Purple soldiers (`04`) punch for 1 to 3 from about
29 px. A spear soldier hit from 44 px; close in quickly. Blue soldiers,
from the first staircase on, throw shuriken along their line (an even slot
reading `80`, 1 damage, not dodged by jumping): walk in rather than wait.
White soldiers, near the end of the hallway and in the boss room, hit for
4. Three white ninjas (`10` each, slots 7, 9 and 11) form the hallway's
last wave and throw knives (`FF` in slots 13-15, 1 damage). Standing on
their line and chaining each time slot 9 came within about 35 px
(`until 487 >= 189; press 1 left 1;` then the three swings), three times
per call, took all three from 16 to 0 for 3 health, one chain often
hitting all three at once. Walking into them instead lost 38 health to a
hold in one call.

**Wait out an attack before moving.** While `0x0412` reads `02`, presses to
turn or walk are dropped: a turtle sent `left`, `b` and `right` in quick
succession stayed put and faced the wrong way. Start each turtle's moves
with `until 412 == 0` (`until 414 == 0` for player 2).

When every enemy slot reads health `00`, hold right to move on: `STEPS stop
56f == 4; stop 571 == 4; stop 573 == 4; stop 575 == 4; press 1 right 300`
stops when a new soldier appears. Stop on `== 4`, not `!= 0`: a bomb reads
`FF` and would stop the walk at once. The screen scrolls only while a
player pushes against its right side (`0x0043` reads `01`), so a turtle
standing still at X 228 holds it.

**Two turtles.** Steps are sequential, so `press 1 ...` and `press 2 ...`
alternate rather than run together. To walk both, hold player 2 with
`INPUT set 2 right 1` while `STEPS` drives player 1, then `INPUT release 2`
before fighting. Side by side on one line, both facing the incoming
soldiers, is the strongest position: `press 1 b 4; run 4; press 2 b 4; run
10` repeated gives both chains.

**Bombs.** In the later part of Scene 1, round bombs roll down two
staircases. They take any odd slot (seen in 9, 11, 13 and 15), read health
`FF`, can't be hurt, and hit for 8 (16 when two land), from as far as
17 px across and 13 in depth. They start at the top of the stairs (X 174,
ground line 80 when the stairs first appear) and roll down and to the
right, about 1.1 px across and 1.3 in depth per frame, though some fall
more steeply. Track every odd slot, not only two, when bombs are about: a
stop on slots 9 and 11 missed the bomb in 15 that hit.

They aren't on a timer. A new bomb starts whenever a bomb slot is free and
the turtle is right of about X 58; at X 50 none came for 400 frames, and
one started 10 frames after he walked back to X 59. So waiting at the left
doesn't empty the stairs.

Ways past both staircases, a stretch-by-stretch route and the boss are
in [references/scene-1.md](references/scene-1.md).

Turtles pushing the screen keep their X (about 145 at the stairs, 227
elsewhere) while the scene scrolls; `0x0043` reads `01`. An X that doesn't
change while `right` is held isn't a turtle stuck.

If `act` reads `04` and doesn't clear, a soldier holds the turtle; in
Scene 2 a hold also read `06`. `STEPS stop 412 == 0; press 1 left+b 3;
press 1 right+b 3`, the pair repeated 6 times, freed him in 7-26 frames.
Don't wait a hold out with `until 412 == 0`: calls doing that lost 12 in
128 frames, and 27 in 268.

A death: health reaches `00`, and about 97 frames later `lives` drops by 1
and the turtle returns at X 128 with full health, `act` `10` for about 80
frames. Put `stop 568 == 0` in each `STEPS` call to catch it, and a stop a
few points below the current health too, so a hold or a bomb ends the call
while there is still something to roll back to. While `act` reads `10`
nothing hurts him: walk in and chain.

## Pitfalls

- The title drops Start for about two seconds after it appears; press it
  repeatedly until `0x0018` is `04`.
- Standing still during Scene 1's third wave let health fall from 37 to 0
  within about 540 frames. Keep fighting.
- Soldiers drop in from above and from the edges at once; read all the odd
  slots when a wave starts, not only the watched ones.
- X wraps at both screen edges: a soldier entering from the left can read
  X 226, and one entering from the right X 16. Read the slot's `0x0556` byte
  before trusting its X, and trust X only while its health is above `00`.
- Near the Pizza Hut sign after the first staircase, turtles on the top
  line (ground 135) seemed unable to walk right. Check `0x0043` first: a
  turtle pushing the screen keeps his X while the scene scrolls.
- `STEPS` checks its stops from the first step, so a `checkpoint` placed
  after an `until` never ran when a stop fired first, and the rollback
  went to an older one. Put `checkpoint` first. A stop such as `412 == 4`
  fires at once if the turtle is still recovering from a hit; start with
  a plain `until 412 == 0` call instead. One call takes 4 stops at most.
- `WATCH` refuses a list that would pass 16 labels even if it also turns
  some off; send the `off` pairs in their own call first.
- `stop 489 <= 210`, meant for a soldier coming from the right, fired on
  X 0 when it went round to enter from the left (its `0x0556` byte read
  `00`). Pair a condition on X with one on the ground line.
- Playing alongside a person in real time doesn't work well: a read and a
  reply take seconds, in which soldiers cross the screen. Queued `STEPS`
  keep the game running only while the queue lasts; when it runs dry the
  game pauses. With the user's agreement, step the game in short paused
  chunks instead.

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress.
