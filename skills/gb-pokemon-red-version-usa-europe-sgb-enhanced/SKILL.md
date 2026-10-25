---
name: gb-pokemon-red-version-usa-europe-sgb-enhanced
description: Plays Pokemon - Red Version (USA, Europe) (SGB Enhanced) on the Game Boy through RetroArch's MCP server. Use when GET_STATUS reports Pokemon - Red Version (USA, Europe) (SGB Enhanced) or the user asks to play Pokémon Red.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST mcp__retroarch__WATCH mcp__retroarch__RUN_UNTIL mcp__retroarch__STEPS mcp__retroarch__GET_FRAME
metadata:
  game: "Pokemon - Red Version (USA, Europe) (SGB Enhanced)"
  system: "Nintendo - Game Boy"
  cores: "gambatte_libretro mgba_libretro"
  crc32: "9F7FDD53"
---

# Pokémon Red

A turn-based RPG: walk a tile grid between towns and routes, talk to people,
and fight wild Pokémon and trainers in menu-driven battles to build a team and
earn the eight gym badges.

## Confirm the game

Call `GET_STATUS`. Its reply should name `game_boy` and
`Pokemon - Red Version (USA, Europe) (SGB Enhanced)`. If nothing is loaded,
follow Setup first.

Then read `0x0134`, 11 bytes. It is `50 4F 4B 45 4D 4F 4E 20 52 45 44`
("POKEMON RED"): the cartridge header, readable through the map from the
moment the game loads, before any frame has run. Pokémon Blue reads
`POKEMON BLUE` there. The global checksum at `0x014E`, 2 bytes, is `91 E6`.

- Memory matches: go on. If the name differs, the ROM is probably renamed:
  run the CRC check if you can, and tell the user what you found.
- Memory doesn't match: another game, or a hack of this one. Stop and tell
  the user what `GET_STATUS` reported.
- The read fails: run the CRC check. If it matches, go on to Setup to fix the
  core. Ask the user only if you can verify neither the memory nor the CRC.

**CRC check**, when you can read files: find the loaded file's path in
`GET_PLAYLIST "Nintendo - Game Boy.lpl"` by the name `GET_STATUS` reported;
if it isn't there, skip the check. For a `.zip#` path, read the `.gb` inside.
There is no header to skip: the CRC32 of the whole 1 MB file should be
`metadata.crc32`. A mismatch means another dump, revision or hack: go on, and
tell the user that addresses may differ.

## Setup

Any Game Boy core works if it publishes a memory map with work RAM at
`0xC000`-`0xDFFF`, HRAM at `0xFF80` and the ROM at `0x0000`.
`gambatte_libretro` and `mgba_libretro` both do. Prefer them in that order.

- **Nothing loaded:** `LIST_CORES <content path>` lists the installed cores
  that can run the ROM. `LOAD_CONTENT` with the first of them that's in the
  list above, and `paused` on.
- **Check the memory:** `GET_MEMORY_MAP` must have regions covering
  `0xC000`-`0xDFFF`. mGBA publishes its map only after a frame has run:
  `RUN_FRAMES 10` before deciding it has none. If the map is still missing,
  tell the user and suggest one of the cores above.

Save states are per core: a state saved under Gambatte doesn't load under
mGBA. mGBA also runs the game in Super Game Boy mode, so `GET_FRAME` returns
256x224 with a border around the 160x144 screen; memory is the same.

**Boot to the main menu**, about 850 frames from `LOAD_CONTENT`: Start skips
the intro and opens the menu from the title, so press it until the menu's box
corner appears at the top left:

1. `RUN_FRAMES 360`.
2. `STEPS`: `press 1 start 4; run 40` ten times, then `stop c3a0 == 121`.
   Repeat the call until it stops; it took two calls.
3. `RUN_FRAMES 60`: the box is drawn before the screen fades in.

The main menu is `NEW GAME`, `OPTION` with no battery save, and adds
`CONTINUE` first when there is one. `0xCC26` is the cursor, 0 at the top.
`NEW GAME` puts the player in Professor Oak's speech; about 120 frames later
`0xD35E` reads `26` (Red's room) with the player at Y 6, X 3 once the speech
ends.

**Ask first, then speed up text.** In `OPTION`, `left` on the first row picks
FAST text, `down` then `right` turns battle animation OFF, `b` leaves. `0xD355`
goes from `03` (medium, animation on) to `81`. It saves with the game, so it
is the player's setting: ask before changing it.

## Controls

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Walk   | `up`, `down`, `left`, `right` | 16 frames per tile. Short presses are unreliable: they sometimes only turn and sometimes take a step, so walk by coordinate (see Playing). |
| Talk, check, confirm | `a` | Faces the tile in front. |
| Cancel, back | `b` | Also says NO at a YES/NO prompt and declines a nickname. |
| Start menu | `start` | In the overworld. Also skips the intro and opens the main menu from the title. |

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed
by `GET_MEMORY_MAP`. Text uses the game's own character set: `80`-`99` are
`A`-`Z`, `7F` is a space, `50` ends a name.

`WATCH` the state you play by once:
`map d35e y d361 x d362 face c109 ign cd6b font cfc4 battle d057 cur cc26`.
Watched values come back in decimal, while this table is in hex.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0134` | 11 | ROM header title, `POKEMON RED` |
| `0xFF80` | 10 | `3E C3 E0 46 3E 28 3D 20 FD C9`, a routine the game copies to HRAM about 600 frames after power-on and keeps |
| `0xD35E` | 1 | Map: `00` Pallet Town, `0C` Route 1, `25` Red's house 1F, `26` Red's room, `28` Oak's lab |
| `0xD361`, `0xD362` | 1, 1 | Player Y, X in tiles, within the current map |
| `0xC109` | 1 | Facing: `00` down, `04` up, `08` left, `0C` right |
| `0xCD6B` | 1 | Input ignored while nonzero (`FC`, `FF` in cutscenes and door transitions). Wait for `00` before walking |
| `0xCFC4` | 1 | `01` while a text box or menu is open in the overworld, `00` when the player is free |
| `0xC490` | 1 | `79` when a text box is on screen (its top-left corner); a map tile otherwise |
| `0xC4F2` | 1 | `EE` while a text box shows the ▼ "press A" arrow. Not every box has one: the last box of a conversation waits for A with no arrow |
| `0xC3A0` | 1 | `79` while the main menu (or another box at the top left) is drawn |
| `0xCC26` | 1 | Cursor in the current menu, 0 at the top. In the move list it starts at 1 |
| `0xD355` | 1 | Options: low bits text speed (`01` fast, `03` medium, `05` slow), bit 7 battle animation off |
| `0xD158` | 11 | Player name, `50`-terminated (`91 84 83 50` = RED) |
| `0xD34A` | 11 | Rival name |
| `0xD347` | 3 | Money, BCD: `00 30 00` = ₽3000 |
| `0xD31D` | 1 | Number of items in the bag |
| `0xD31E` | 2 each | Bag: item ID and quantity per slot, `FF` after the last (`14 01` = 1 Potion) |
| `0xD163` | 1 | Number of Pokémon in the party |
| `0xD164` | 6 | Party species, `FF` after the last |
| `0xD16B` | 44 each | Party Pokémon, 6 slots `0x2C` apart. Offsets: `+0x00` species, `+0x01` HP (2, big-endian), `+0x08` moves (4), `+0x0E` experience (3), `+0x1D` PP (4), `+0x21` level, `+0x22` max HP (2) |
| `0xD2B5` | 11 each | Party nicknames |
| `0xD057` | 1 | Battle: `00` none, `01` wild, `02` trainer |
| `0xD014` | 1 | Your Pokémon in battle: species |
| `0xD015` | 2 | Its HP, big-endian. Stale after the battle, even after healing; the party slot's HP updates live in battle too, so prefer it |
| `0xD01C` | 4 | Its moves |
| `0xCFE5` | 1 | Enemy species |
| `0xCFE6` | 2 | Enemy HP, big-endian |
| `0xCFF3` | 1 | Enemy level |
| `0xC4C0` | 1 | `7C` while the battle menu (FIGHT, PKMN, ITEM, RUN) is up |
| `0xC4C1`, `0xC4C7`, `0xC4E9`, `0xC4EF` | 1 each | `ED` where the battle menu cursor is: FIGHT, PKMN, ITEM, RUN |

Species and item numbers are the game's internal IDs, not Pokédex numbers:
`99` Bulbasaur, `24` Pidgey, `A5` Rattata; `14` Potion. Moves: `21` Tackle,
`2D` Growl. For any other ID, look at the battle with `GET_FRAME`.

Two-byte values watch as `high:low`: `ehp cfe6:cfe7`, `hp d16c:d16d`.

## Playing

Times are in frames at 60 per second.

Coordinates below are written as Y, X, the order the game keeps them in.

**Walking, by coordinate.** Hold the direction with `INPUT`, run until the
coordinate reaches the target, and let go. The coordinate changes as a step
begins, so releasing then finishes that step and stops on the target tile:

1. `INPUT set 1 down 1`
2. `STEPS until d361 >= 7` (add `stop d057 != 0` on grass, and
   `stop d35e != <map>` near doors)
3. `INPUT release`, then `run 20` before the next walk.

Y grows going down, X going right: use `>=` for down and right, `<=` for up
and left. A wall or person leaves the call waiting for its 540 frames; check
`y` and `x` in the reply. This landed exactly on the target each time tested.
Timed `press` walks (`press 1 right 48`, 16 frames a tile) work too, but
drift by a tile when the player has to turn first.

**Places.**

| Map | Where | Notes |
| --- | --- | --- |
| `26` Red's room | Stairs at Y 1, X 7 | Walk up column X 7 from below, or right along Y 1. The PC is at Y 1, X 0: stand at Y 2, X 0 facing up. You start a new game at Y 6, X 3 |
| `25` House 1F | Stairs arrival Y 1, X 7; exit at Y 7, X 2 | Walk down off Y 7 at X 2 to leave. Mom is at Y 4, X 5: stand at Y 5, X 5 facing up. The table blocks X 3-4 |
| `00` Pallet Town | Red's house door Y 5, X 5 | You come out at Y 6, X 5. Route 1 is north up column X 10 (Y 0 is the edge). Oak's lab door is Y 11, X 12; you come out at Y 12, X 12 |
| `0C` Route 1 | Enter at Y 35, X 10 | Battles started in grass at Y 30, X 12, at Y 22-24, X 12-13, and once at Y 35, X 10. Going north from X 10, a ledge stops you at Y 28; go round by X 8. Going back, X 8 down to Y 28, then X 10 down |
| `28` Oak's lab | Door Y 11, X 4-5 | Bookshelves fill Y 6-7 except X 4-5 |

**Finding a battle.** In grass, pace up and down:
`press 1 up 32; press 1 down 32` repeated, with `stop d057 != 0`. Encounters
came within a few steps.

**Doors and map edges.** Walking onto a door or stairs changes `0xD35E`
first; Y and X follow about 30-60 frames later, and `0xCD6B` is nonzero
meanwhile. Use `stop d35e == <map>`, then `run 60; until cd6b == 0` before
the next walk. Walking off a map's edge changes map, Y and X at once.

**Text.** To read a sign or talk, face it and `press 1 a 4`. To get through
the text: `press 1 a 4; run 20` repeated, with `stop cfc4 == 0`. The stop
ends the call on the frame the box closes, so the next A doesn't talk again.
A YES/NO box takes the A as YES; check with `GET_FRAME` when a conversation
may ask something. Cutscenes run with `0xCD6B` nonzero; keep pressing A until
it is `00`.

**Battles.** `0xD057` turns nonzero as the screen flashes. The opening text
needs A, then the game sends out your Pokémon by itself; reach the menu with
`press 1 a 4; run 30` repeated, `stop c4c0 == 124`. That took 360-520
frames, so expect a second call; repeat the call until the stop answers. Each
new battle starts with the cursor on FIGHT.

- **Fight**, two calls a turn. A stop ends a call after the first frame it
  holds, and `0xC4C0` is still `7C` as the turn begins, so the choice can't
  share a call with the stop:
  1. `press 1 a 4; run 16; press 1 a 4; run 40` picks FIGHT and the move under
     the cursor, which stays on the last move used. To pick another, split
     it: `press 1 a 4; run 16`, read `0xCC26` while the move list is open (1 is
     the first move), `down` or `up` to the move, then `press 1 a 4; run 40`.
     Once the list closes, `0xCC26` no longer means the move.
  2. `press 1 a 4; run 30` fifteen times, `stop c4c0 == 124; stop d057 == 0`;
     repeat until a stop answers. A turn with both sides moving took about
     300 frames with animation off and 340-370 with it on.
- **Run** from a wild battle: `press 1 right 4; run 8; press 1 down 4; run 8;
  until c4ef == 237; press 1 a 4; run 30` four times, `stop d057 == 0`. After
  it, `run 90` before walking.
- After a win, keep pressing A with `stop d057 == 0`: experience, level-ups
  and a trainer's prize money come first. A level-up changes the party slot's
  level and max HP.

Tested route: from a new game, walk out of Red's house (`26` → `25` → `00`),
go right to X 10 and north: Oak stops you at Y 1 and leads you to the lab.
In the lab the three balls are on the table at Y 3, X 6, 7 and 8; X 8 is
Bulbasaur (the other two weren't checked). Stand below one (Y 4), face up and
press A; `a` again says YES, `b` declines the nickname. After the
choice, walking down starts the rival battle (L5 starter against L5 starter;
Tackle alone won it with Bulbasaur at 6/22 HP). Mom heals the party and
refills PP; the PC in Red's room holds a Potion (WITHDRAW ITEM, then A twice).
Both are in Places above.

## Pitfalls

- `0xC4F2` and `0xC490` are tile-map cells: they mean a text box only while
  one is on screen. Don't wait on `c4f2 == 238` in the overworld or at the
  last box of a conversation, which has no arrow; the call runs out its 540
  frames. `stop cfc4 == 0` is the safe end condition.
- Holding A doesn't advance text; each box needs a new press.
- `0xD015` keeps the last battle's HP after the battle; the party slot holds
  the real value.
- Input is ignored in the second or so after loading a save state at the
  title screen: the first Start can be dropped. The stop-on-`c3a0` loop
  covers it.
- `STATE load` while paused can answer late or time out, and RAM reads `FF`
  until a frame has run. `RUN_FRAMES 2`, then read `0xD35E` to check the load.
- `GET_FRAME` can come back blank white while paused after a load; run a
  couple of frames first.
- A `stop` already true when a call starts may not end it at once if the
  first step changes things (an A that opens a text box). Start a call from a
  state where its stops are false.
- Escape from a wild battle can fail (not seen in testing): the enemy then
  gets a turn and the menu comes back. Add `stop c4c0 == 124` to the end of
  the RUN list's A presses if that matters, and check `0xD057` after.
- Walking into a person or wall burns the frames without moving; compare Y
  and X with what you expected after each walk.

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Don't choose SAVE in the start menu without asking: it overwrites the
player's battery save. Changing OPTION settings also persists; ask first.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress.
