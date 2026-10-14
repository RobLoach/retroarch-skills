---
name: nes-kirbys-adventure-usa-rev-1
description: Plays Kirby's Adventure (USA) (Rev 1) on the Nintendo Entertainment System through RetroArch's MCP server. Use when GET_STATUS reports Kirby's Adventure (USA) (Rev 1) or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__SET_INPUT mcp__retroarch__RELEASE_INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST
metadata:
  game: "Kirby's Adventure (USA) (Rev 1)"
  system: "Nintendo - Nintendo Entertainment System"
  cores: "fceumm_libretro"
  crc32: "5ED6F221"
---

# Kirby's Adventure

A side-scrolling platformer: Kirby walks, jumps and flies through stages
reached from doors in each level's hub, inhaling enemies and copying their
abilities. Stages scroll right; each ends at a door.

## Confirm the game

Call `GET_STATUS`. Its reply should name `nes` and
`Kirby's Adventure (USA) (Rev 1)`. If nothing is loaded, follow Setup first.

Then read `0x0029`, 10 bytes. It is `48 A9 ?? 8D 00 E0 8D 01 20 4C`, where
`??` varies: a short routine the game copies into RAM at power-on, there from
the title screen through play. Other revisions of the game may share the
routine.

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
places system RAM at `0x0000`-`0x07FF` and cartridge RAM at
`0x6000`-`0x7FFF`.

- **Nothing loaded:** `LIST_CORES <content path>` lists the installed cores
  that can run the ROM. `LOAD_CONTENT` with `fceumm_libretro`.
- **Check the memory:** `GET_MEMORY_MAP` must have regions covering
  `0x0000`-`0x07FF` and `0x6000`-`0x7FFF`. The core splits RAM into 0x400-byte
  regions, and a read stops at the end of a region, so never read across a
  multiple of `0x400`. If the map is missing or short, tell the user.

The game keeps running after `LOAD_CONTENT`, and after a few seconds an
attract demo shows Kirby playing. Don't take that for gameplay.

1. `PRESS start 4`, `RUN_FRAMES 90`. Repeat until the title screen gives way
   to the file menu (`KIRBY 1/2/3`, `Delete Saved Game`). A Start pressed
   while the title is still appearing is dropped.
2. The cursor starts on `KIRBY 1`. Ask the user which file to use; `PRESS a 4`
   opens the highlighted file. Never choose `Delete Saved Game`.
3. A "LEVEL 1 VEGETABLE VALLEY" card appears and waits for input:
   `RUN_FRAMES 120`, `PRESS start 4`, `RUN_FRAMES 180`. This is a new file;
   one with progress may start elsewhere.
4. Kirby stands in the level hub just right of the stage 1 door.
   `PRESS left 12`, `RUN_FRAMES 10`, `PRESS up 4`, `RUN_FRAMES 180`.
5. In the stage, Kirby's X (`0x0095`, `0x0083`) is `00`, `28`.

## Controls

Measured at 60 frames per second.

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Walk   | `left`, `right` | About 1.1 px per frame. |
| Run    | double-tap a direction and hold the second tap | `PRESS left 2`, `RUN_FRAMES 2`, `PRESS left 36` covers 53 px against 44 for a plain 40-frame walk. |
| Jump   | `a` | `PRESS a 3` rises 8 px and lands in about 20 frames. `PRESS a 16` rises about 40 px and lands about 55 frames after the press. |
| Fly    | `up` (in the open) | Kirby puffs up and rises about 1.2 px per frame while `up` is held, keeps drifting up briefly after release, and floats. |
| Stop flying | `b` | Exhales; Kirby falls, about 80 px in 60 frames. |
| Inhale | `b` (held) | Holding `b` for 60 frames sucked in a Waddle Dee that started 57 px ahead, walking toward Kirby. |
| Swallow | `down` | With an enemy in the mouth. A Waddle Dee gives no ability ("NOTHING"). |
| Use power | `b` | With a power, `b` attacks instead of inhaling. Spark surrounds Kirby with sparks while held. |
| Drop power | `select` | Only while Kirby is idle; ignored during an attack. The power leaves as a bouncing star and `0x05E3` returns to `FF`. |
| Enter door | `up` | Only when Kirby overlaps the door. Anywhere else `up` starts flying. |
| Pause  | `start` | Shows a help screen for the current ability. |

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed by
`GET_MEMORY_MAP`. Read each array in one call (`0x0083`, 16 bytes), not as one
large dump.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0596`, `0x0597` | 1, 1 | Health: max, current. `2F` is full (6 bars); each hit takes `08`. Bars on the HUD = current / 8, rounded up. Current is `FF` while Kirby is dying. |
| `0x0599` | 1 | Lives, as shown on the HUD (`04` on a new file). Drops by 1 about 300 frames after health reaches `FF`. |
| `0x0593` | 3 | Score / 10, low byte first (`68 01 00` = 3600). |
| `0x62C7` | 1 | Kirby's action: `00` standing, `14` walking, `22` in the air, `52` flying with `up` held, `54` floating puffed up, `02` inhaling, `1A` mouth full, `24` knocked back by a hit. Other values appear on slopes and during transitions. |
| `0x05E2`, `0x05E3` | 1, 1 | Power of the enemy in Kirby's mouth, and Kirby's current power: `FF` none (HUD "NORMAL"), `01` Spark. |
| `0x0521` | 1 | Level 1 stage clear bits; bit 0 is stage 1-1. It became `01` after clearing 1-1. |
| `0x0095`, `0x0083` | 1, 1 | Kirby's X: page, X within page. Absolute X = page * 256 + X. Reset to `00`, `28` on entering a stage room. |
| `0x00B9` | 1 | Kirby's Y, in level pixels; smaller is higher. Standing on the ground in the first room of stage 1: `89`. |
| `0x0084`, `0x0096`, `0x00BA` | 15 each | Other object slots (enemies, projectiles): X, page, Y, parallel to Kirby's at slot 0. |
| `0x627F` | 16 | Slot in use: `86` empty, anything else live. Slot 0 is Kirby. Dead slots keep their old X and Y, so check this first. |

The current room's terrain is at `0x67EE`: width and height in screens, then
from `0x67F6` the screen order (one byte per screen, left to right). Screen
`k`'s tiles are at `0x68C8 + k * 0xC0`, 16 columns by 12 rows of 16-pixel
tiles, row by row. A tile's collision is the byte at `0x7F00 + tile`: `FF`
empty, `0D` solid, `10`-`15` slopes. Kirby is in the screen listed at
position `X / 256` of the screen order, at column `(X mod 256) / 16` and row
`Y / 16`; standing on a floor in row `r` puts his Y near `r * 16 - 7`. Rooms
taller than one screen are untested.

## Playing

Loop: read Kirby (`0x0083`, `0x0095`, `0x00B9`) and health, decide, `PRESS`,
read again. Times are in frames at 60 per second.

- Stages are lined with steps. When holding `right` stops changing X, Kirby
  is against one: `PRESS right+a 16` clears a low step. For a tall wall,
  `PRESS up+right 90`, then `PRESS b 3` once over it.
- **Fly high to cross a room:** `PRESS up 60`, then `PRESS up+right 600`
  (the most `PRESS` allows) until X stops growing. Kirby crosses near the top
  of the screen at about 0.7 px per frame, above most enemies. `PRESS b 3`
  exhales to land.
- Touching an enemy cost one bar each time in stage 1, and the enemy
  touched was destroyed. Inhaling one (`b` held, facing it) costs nothing,
  and the puff of air Kirby exhales destroys an enemy it hits.
- **Copy an ability:** hold `b` facing an enemy within about 50 px until
  `0x05E2` changes, then `PRESS down 3`. `0x05E3` shows the new power; a
  Sparky gave Spark (`01`).
- At the end of a room, stand in the doorway and `PRESS up 4`, then
  `RUN_FRAMES 150`. X returns to `00`, `28` in the next room.
- A stage's last door is marked with a star and leads to a GOAL bonus game:
  `PRESS a 4`, `RUN_FRAMES 600`. Kirby returns to the hub and the stage's bit
  in `0x0521` is set.
- In the level 1 hub, stage 1's door is at X 76 and stage 2's at X 245. Kirby
  must be within a few pixels of a door: `up` at X 257 did nothing.

## Pitfalls

- `up` away from a door starts flying. Line Kirby up with the door first.
- While puffed up (`0x62C7` is `52` or `54`), `b` exhales instead of
  inhaling.
- After a death, Kirby respawns at the start of the room with full health
  about 300 frames after `0x0597` reaches `FF`.
- The file menu's three files are battery-backed saves. Opening an empty one
  starts a new game in it.

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress. Ask which save file to play, and never choose
`Delete Saved Game` on the file menu.
