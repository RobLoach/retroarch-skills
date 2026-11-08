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
2. Setup's steps reach Scene 1 with Donatello: the title, the turtle, then
   `until 3c == 3` through the intro.
3. `WATCH px 47e gy 4a2 act 412 face 436 hp 568 lives 4d score 3f0
   e7x 485 e7g 4a9 e7h 56f e9x 487 e9g 4ab e9h 571`, once. Labels from
   an earlier session survive a state load and count toward the 16: turn
   any others off first (`<label> off`).
4. Fight each wave in short `STEPS` calls: line up, face, chain three
   swings, with `stop 568 == 0` for a death. Then walk right.
5. A `checkpoint` step before each wave; `STATE rollback` after a death.

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
  `0x0000`-`0x07FF`. If the map is missing or short, tell the user.

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
   each is enough; a second can overshoot.
3. An intro and a "SCENE 1" card play for about 820 frames. Pressing Start
   doesn't skip them. `STEPS until 3c == 3` ends on the first frame of play;
   one request runs 540 frames at most, so send it again until it answers
   `done`. Lives (`0x004D`) become `02` and health `3C` (60) during the
   intro. The turtle starts at X 128, Y 176, moves at once, and a Foot
   soldier is already on its way.

## Controls

Measured at 60 frames per second, with Donatello.

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Walk   | `left`, `right` | About 1 px per frame. Turns the turtle at once; `press 1 left 1` turns him without moving. |
| Step in depth | `up`, `down` | About 0.6 px per frame; moves the ground line (`0x04A2`). |
| Attack | `b` | One swing locks him for about 17 frames (`0x0412` is `02`). Three in a row, `b 4; run 10` each, chain into a longer thrust: the third reached an enemy 55 px away. |
| Jump   | `a` | Lands 57 frames after a 4-frame press, peaking about 88 px up. Moves only about 6 px sideways even with a direction held. |
| Break a hold | `left+b`, `right+b` alternately | When a Foot soldier holds him (`0x0412` is `04`), 6 alternating 3-frame presses broke free. |

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed by
`GET_MEMORY_MAP`. Objects are parallel arrays of 18 slots: an object's byte is
at the array's address plus its slot. Read each array in one call (`0x047E`,
18 bytes) rather than one large dump.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0018` | 1 | Screen: `01` title, `04` turtle select, `05` intro and play. |
| `0x003C` | 1 | Scene status: `00` on the title and select screens, `01` intro text, `06` scene starting, `03` play. |
| `0x03EA` | 1 | Enemies defeated by player 1; it rose by 1 with each defeat. |
| `0x0033` | 1 | Player 1's turtle: `00` Leonardo, `01` Michelangelo, `02` Donatello, `03` Raphael. |
| `0x004D` | 1 | Player 1's lives in reserve, as the HUD's REST shows (`02` at the start). |
| `0x03F0` | 1 | Player 1's score, last two digits, in BCD (`10` is 10 PTS). A Foot soldier is worth 1. |
| `0x007E` | 1 | Scene progress: `01` at the start of Scene 1, then it rose (`02`, `03`, `05`) as the scene scrolled, some dozens of frames behind the scroll. It has never gone down. |
| `0x047E` | 18 | X on screen, 0-255. Slot 0 is player 1. The screen scrolls under the turtle, so his X stays between about 128 and 230. X is one byte and wraps at both edges; `0x0556` says which side. |
| `0x0556` | 18 | Which screen the object is on: `00` this one, `01` off the right edge, `02` off the left edge. A soldier entering from the left read X 226 with `02`, then X 0 with `00`; one entering from the right read X 16 with `01`, then X 254 with `00`. |
| `0x04A2` | 18 | Ground line (depth): larger is nearer the bottom of the screen. Player 1 walks between about 135 and 190. Stays put during a jump. |
| `0x046C` | 18 | Y on screen: the ground line minus height in the air (176 standing, 88 at the top of a jump). |
| `0x0436` | 1 | Player 1 faces: `00` right, `40` left. |
| `0x0412` | 1 | Player 1's action: `00` free, `01` jumping, `02` attacking, `04` held or hit, `06` knocked down, `10` respawning. |
| `0x0568` | 18 | Health. Slot 0 is player 1, `3C` (60) full; a soldier's hit takes 1 to 3. Slot 2 also reads `3C` in a one-player game; it isn't an enemy. Enemies use the odd slots 7, 9, 11, 13, 15 and 17; a Foot soldier starts at `04`, and each of the turtle's hits takes `02`. |

An enemy slot is live while its health is above `00`. A defeated soldier's
slot keeps its X and ground line for a while, so check health first.

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
2. **Keep the gap about 15-25 px.** Chains at 29-31 px missed, and closer
   than about 10 a soldier holds the turtle. Soldiers move up to about
   2.5 px per frame, so close in with short taps (`press 1 right 6`) and read
   the gap again, rather than one long walk. Too close: step away 14 frames
   and turn back.
3. **Face it and chain:** `STEPS until 412 == 0; press 1 left 1; press 1 b 4;
   run 10; press 1 b 4; run 10; press 1 b 4; run 10` (`right 1` to face
   right). Two hits defeat a Foot soldier; one chain often does it, and can
   hit two soldiers on the same line.
4. Read the watched values and repeat. Soldiers move fast and change lines,
   so keep each call to one chain, about 50 frames.

When every enemy slot reads health `00`, the screen unlocks: hold right
(`STEPS press 1 right 120`, with `stop 571 != 0` or another odd slot) until
the next wave arrives. The turtle stops near X 145 and the screen scrolls
under him.

If `act` reads `04` and doesn't clear, a soldier holds the turtle: `STEPS
press 1 left+b 3; press 1 right+b 3` repeated 3 times, then `until 412 ==
0`.

A death: health reaches `00`, and about 97 frames later `lives` drops by 1
and the turtle returns at X 128 with full health, `act` `10` for about 80
frames. Put `stop 568 == 0` in each `STEPS` call to catch it.

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

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress.
