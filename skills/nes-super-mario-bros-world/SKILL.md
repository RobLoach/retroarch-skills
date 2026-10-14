---
name: nes-super-mario-bros-world
description: Plays Super Mario Bros. (World) on the Nintendo Entertainment System through RetroArch's MCP server. Use when GET_STATUS reports Super Mario Bros. (World) or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__SET_INPUT mcp__retroarch__RELEASE_INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST
metadata:
  game: "Super Mario Bros. (World)"
  system: "Nintendo - Nintendo Entertainment System"
  cores: "fceumm_libretro nestopia_libretro mesen_libretro quicknes_libretro"
  crc32: "D445F698"
---

# Super Mario Bros.

A side-scrolling platformer: run right through each level, avoid or stomp
enemies, clear pits and pipes, and touch the flagpole at the end.

## Confirm the game

Call `GET_STATUS`. Its reply should name `nes` and
`Super Mario Bros. (World)`. If nothing is loaded, follow Setup first.

Then read `0x07FF`, 1 byte. The game writes `A5` there at power-on and keeps
it through the title screen, the demo and play; Kirby's Adventure, for one,
leaves `FF`.

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

Any NES core works if it publishes a memory map with system RAM at `0x0000`.
`fceumm_libretro`, `nestopia_libretro`, `mesen_libretro` and
`quicknes_libretro` all do. Prefer them in that order.

- **Nothing loaded:** `LIST_CORES <content path>` lists the installed cores
  that can run the ROM. `LOAD_CONTENT` with the first of them that's in the
  list above.
- **Check the memory:** `GET_MEMORY_MAP` must have regions covering
  `0x0000`-`0x07FF`. A read stops at the end of a region, so keep each read
  inside one; fceumm splits RAM at `0x0400`. If the map is missing or short,
  tell the user and suggest one of the cores above.

To start: `RUN_FRAMES 120`, `PRESS start 4`, `RUN_FRAMES 200`, then read
`0x0770`. The first Start after loading is often dropped; if it is still `00`,
press Start again. `0x0770` turns `01` during the "WORLD 1-1" card, before
Mario can move. Play has begun when `0x0772` is `03` and `0x000E` is `08`,
about 180 frames after Start. Don't judge by position: Mario's X is `0x28` on
the title screen too.

## Controls

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Move   | `left`, `right` | Mario keeps sliding after release. |
| Jump   | `a` | Hold longer to jump higher: 12 frames is a hop, 32 a full jump. |
| Run, fireball | `b` | Hold with a direction. |
| Pause  | `start` | |

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed by
`GET_MEMORY_MAP`. Read each array in one call (`0x0087`, 5 bytes), not as one
large dump.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0770` | 1 | Game mode: `00` title screen, `01` playing |
| `0x0772` | 1 | `01` world card or loading, `03` level running |
| `0x0776` | 1 | Bit 0 set while paused |
| `0x074A` | 1 | Buttons the game sees this frame (`10` = Start); use it to check input arrives |
| `0x07F8` | 3 | Timer digits, one per byte (`03 09 09` = 399) |
| `0x000E` | 1 | Player state: `08` normal, `0B` dying (enemy or time up), `06` dying in a pit, `09` growing, `0A` shrinking, `03` going down a pipe, `02` into a sideways pipe, `07` entering an area, `04`/`05` flagpole and walk to the castle, `00` between areas or lives |
| `0x001D` | 1 | `00` ground, `01` jumping (up and down), `02` walked off a ledge, `03` on flagpole |
| `0x009F` | 1 | Vertical speed, signed: `FC` jump start, `00` at the top, up to `04` falling |
| `0x0057` | 1 | Horizontal speed, signed: `18` walk, `28` run |
| `0x006D`, `0x0086` | 1, 1 | Page, X. Absolute X = page * 256 + X |
| `0x00CE` | 1 | Y. On the ground = `B0` at either size; one block up = `0x10` less |
| `0x00B5` | 1 | `01` on screen, `02` and up below it (fell into a pit) |
| `0x071A`, `0x071C` | 1, 1 | Screen's left edge: page, X |
| `0x0723` | 1 | Nonzero while the screen can't scroll: bonus rooms, the flagpole |
| `0x074E` | 1 | Area type: `01` above ground, `02` underground |
| `0x079E` | 1 | Counts down after a hit; enemies can't hurt Mario while it's nonzero |
| `0x04AC` | 4 | Mario's hitbox on screen: x1, y1, x2, y2 |
| `0x04B0` | 20 | Enemy hitboxes, 4 bytes per slot; `FF FF FF FF` while off screen |
| `0x000F` | 5 | Enemy slots 0-4 active |
| `0x0016` | 5 | Enemy type: `06` Goomba, `00` green Koopa. A slot can also hold an object that isn't an enemy, such as `31`, the flag over the castle; ignore those |
| `0x001E` | 5 | Enemy state: `04` stomped |
| `0x006E`, `0x0087`, `0x00CF` | 5 each | Enemy page, X, Y (`B8` = on ground) |
| `0x0058` | 5 | Enemy speed: `F8` left, `08` right |
| `0x0756` | 1 | Power-up: 0 small, 1 big (2 blocks tall), 2 fire |
| `0x075A` | 1 | Lives minus one (`00` = last life) |
| `0x075F`, `0x075C` | 1, 1 | World, level (0-based) |

The terrain is a tile map at `0x0500`: two screens of 16 columns by 13 rows.
Screen `n` starts at `0x0500 + (n & 1) * 0xD0`; the tile at row `r`, column
`c` is `start + r * 16 + c`, covering X `n * 256 + c * 16`. Rows 11-12 are
ground, and a block `h` high sits in row `11 - h`. Tiles: `00` empty, `54`
ground, `61` stair block, `51` brick, `C0` question block with a coin, `C1`
question block with a power-up, `C4` used block, `C2` coin, `52` underground
brick, `10`/`11` top of a pipe Mario can go down, `12`/`13` top of any other
pipe, `14`/`15` pipe sides, `1C`-`21` sideways pipe, `24`/`25` flagpole. A
missing `54` in rows 11-12 is a pit. Only columns up to just past the
screen's right edge (left edge + 256) are current; read again as Mario
advances.

## Playing

Loop: read Mario and enemy positions, decide, `PRESS`, read again to check.
Gap = enemy absolute X - Mario absolute X. Times are in frames at 60 per
second.

- **Stomp:** stand still, with `0x0057` at `00`. When an approaching enemy's
  gap is 18-22, `PRESS a 12`, `RUN_FRAMES 24`, then check its state is `04`.
  The stomp lands when Mario's hitbox bottom (y2) reaches the enemy's top (y1)
  while they overlap in X and `0x009F` is positive (falling). For two Goombas
  close together, a running jump over both is safer than stomping.
- **Jump over:** while walking, at gap ~50, `PRESS right+a 20-32`.
- **Pipe, wall or stairs:** walk into it, then `PRESS right+a 32-35`. That
  clears 4 blocks; repeat to climb.
- **Pit:** 2 wide, a walking full jump from the edge. 3 wide,
  `PRESS right+b 20` to the edge, then `PRESS right+b+a 28`.
- **Power-up:** jump into a `C1` block from below. The mushroom slides along,
  bounces off pipes, and grows Mario on touch, so letting it come to Mario
  usually works. Big Mario survives one hit by shrinking.
- **Down a pipe:** stand on a pipe topped with `10`/`11`, no more than 12
  pixels right of its left edge, and `PRESS down 8`. `0x000E` turns `03`. To
  leave by a sideways pipe, walk into it.
- **Flagpole:** from the top step of the last staircase, `PRESS right+b 8`,
  `PRESS right+b+a 30`, `PRESS right+b 40`. Done when `0x001D` is `03` or
  `0x000E` is `04` or `05`; a grab near the bottom of the pole skips `03`.

## Pitfalls

- After a `PRESS`, check `0x0057`; brake with a few frames of `left` before
  standing still.
- Blocks 3 up leave little headroom: a full jump under them bonks and drops
  Mario short.
- A Goomba falling off a platform is dangerous until its Y is `B8`.
- Goombas reverse when they bump each other; recheck their speed before
  committing.
- Enemies spawn only as the screen scrolls, so standing still won't bring them.
- A pit death leaves `0x000E` at `08` for over 300 frames while Mario falls,
  until `0x00B5` reaches `06`. Treat `0x00B5` at `02` or more as dead.
- After any death, the life is taken and Mario respawns about 400 frames later.
- Time up kills Mario too (`0x000E` = `0B`). The timer only runs with frames,
  but retrying one obstacle many times can still use it up; check `0x07F8`.
- Start is ignored for a moment after pausing. If the game won't unpause, wait
  40 frames and press Start again.
- Check the enemy gaps before saving: a save taken with an enemy within about
  12 pixels reloads straight into a death.

## Warping to a world

Only when the user asks. These are memory writes, so see Ask first. Start the
game so `0x0772` is `03`, then write:

1. `0x075F` = world (0-based), `0x075C` = level (0-based), `0x0760` = `00`.
2. `0x0750` = the level's area ID. Bits 5-6 give the area type (`00` water,
   `20` ground, `40` underground, `60` castle). `00` loads a water level and
   leaves a stale ID from the previous level, so always write it.
3. `0x0772` = `00`, then `RUN_FRAMES 240` and check with `SCREENSHOT`.

Verified: 5-1 is world `04`, level `00`, area ID `2D`: a night level that
starts beside a castle. Other area IDs are unverified; try ground IDs near
`20`-`2F` and check the HUD and screenshot. The HUD shows the world from
`0x075F` even when the wrong level loaded.

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress. Cheats are writes and need the user's request: lives
`0x075A`, power-up `0x0756` (with `0x0754` = `00` for big), star timer
`0x079F`.
