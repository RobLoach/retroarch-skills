---
name: nes-super-mario-bros-world
description: Plays Super Mario Bros. (World) on the Nintendo Entertainment System through RetroArch's MCP server. Use when GET_STATUS reports Super Mario Bros. (World) or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__SET_INPUT mcp__retroarch__RELEASE_INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST mcp__retroarch__WATCH mcp__retroarch__RUN_UNTIL mcp__retroarch__STEPS mcp__retroarch__SCREENSHOT
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
leaves `FF`. Run some frames first: after `LOAD_CONTENT` with `paused` on,
RAM reads `FF` everywhere until the first frame has run.

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
the title screen too, and `0x000E` is already `08` there.

With `PRESS ... until` and `RUN_UNTIL`, starting takes three calls:
`RUN_FRAMES 120`, `PRESS 1 start 4 until "770 == 1"`, then `RUN_UNTIL e == 8`.
Only wait for `e == 8` once `0x0770` is `01`, because of the title screen
value above. One condition can't check `0x0772` as well.

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

Better, `WATCH` the ones you need once, so every step answers with them and
needs no reads after it. One call covers Mario and four enemy slots:
`st e air 1d x 6d:86 y ce vs b5 spd 57 e0 f e0x 6e:87 e1 10 e1x 6f:88 e2 11
e2x 70:89 e3 12 e3x 71:8a`. Watched values come back in decimal, while this
table is in hex: `57` running shows `40` (`0x28`), and `ce` on the ground
shows `176` (`0xB0`). A slot that isn't active keeps a stale X, so trust an
enemy's X only while its `0x000F` flag is `01`.

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
| `0x0760` | 1 | Area index within the world, as in the warp table. It changes when the next level loads, so it marks a clear: `00` to `01` after 1-1, about 640 frames after the flag |

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

Cheaper: with the `WATCH` above, `SET_INPUT 1 right+b 1` once to keep running
right, and play each obstacle as one `STEPS` call. Its reply carries the
watched values, so no read is needed after it:

```
until 6d:86 >= 412; press 1 a 20; until 1d == 0; stop e == 11; stop b5 > 1
```

- Always add `stop e == 11; stop b5 > 1`. A death then stops the call within
  a few frames instead of running on.
- `stop f == 1` (or `10 == 1` and so on) stops when an enemy slot spawns. It's
  a cheap way to learn where the next enemies are before committing.
- Several obstacles can go in one list, and a replay after a rollback is
  deterministic.
- Hold or release `right+b` with `SET_INPUT` and `RELEASE_INPUT`, not inside
  `STEPS`. It stays held through `STATE rollback`.
- `STATE checkpoint` before each enemy group. `STATE rollback` and one replay
  `STEPS` then cost two calls after a death, and touch no save slot.
- `RUN_UNTIL` and `STEPS` run 540 frames per request at most. Ask again when
  the reply says `waiting`.

Played this way, World 1-1 took 48 calls to the flagpole.

- **Stomp:** stand still, with `0x0057` at `00`. When an approaching enemy's
  gap is 18-22, `PRESS a 12`, `RUN_FRAMES 24`, then check its state is `04`.
  The stomp lands when Mario's hitbox bottom (y2) reaches the enemy's top (y1)
  while they overlap in X and `0x009F` is positive (falling). For two Goombas
  close together, a running jump over both is safer than stomping.
- **Jump over:** while walking, at gap ~50, `PRESS right+a 20-32`. While
  running (`0x0057` at `28`), a hop of `a 10-14` at gap 45-60 clears one
  Goomba or a pair. The four Goombas around X 1950-2030 in 1-1 need a full
  jump (`a 24` from X 1912): short hops land among them.
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
  In 1-1 the last staircase can be climbed and the pole reached in one call
  from its third step (Y `0x80`), holding `right+b`:
  `press 1 a 30; until 1d == 0; press 1 a 30; until 1d == 0; stop 1d == 3`.
  That grabbed the pole at Y `0x3B`.

## Pitfalls

- After a `PRESS`, check `0x0057`; brake with a few frames of `left` before
  standing still.
- Blocks 3 up leave little headroom: a full jump under them bonks and drops
  Mario short.
- Pressing `a` while `0x001D` is `02` (walked off a ledge) does nothing. After
  stepping off blocks or a pipe, wait for `1d == 0` before the jump.
- `1d == 0` also means landing on top of blocks: a hop near `?` blocks can
  leave Mario on them, with `0x00CE` at `70`. Check Y before assuming he is on
  the ground.
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
- 2-3 is a chain of bridges between brick pillars, with gaps up to about
  100 pixels. Mario can't jump once `0x001D` is `02` (walked off), so take
  off from the very end of the bridge, and take a `STATE checkpoint` (or save
  to 990-999) at each landing so a miss costs seconds, not the level.

## Warping to a level

Only when the user asks. These are memory writes, so see Ask first. Start the
game so `0x0772` is `03`, then write:

1. `0x0750` = the area ID from the table below. This picks the level; it is
   global, so the same ID loads the same level whatever the world is.
2. `0x075F` = world (0-based) and `0x0760` = the ID's index in that world's
   row. These mostly drive the HUD and progression, not the layout.
3. `0x0772` = `00`, then `RUN_FRAMES 240`.
4. The load resets `0x075C` (level) to `00`. Write the level (0-based) again
   afterwards, or the HUD keeps showing a stale level.

Area IDs per world, in `0x0760` order (from the ROM at file offset `0x1CC4`):

| World | IDs |
| ----- | --- |
| 1 | `25 29 C0 26 60` |
| 2 | `28 29 01 27 62` |
| 3 | `24 35 20 63` |
| 4 | `22 29 41 2C 61` |
| 5 | `2A 31 26 62` |
| 6 | `2E 23 2D 60` |
| 7 | `33 29 01 27 64` |
| 8 | `30 32 21 65` |

Checked: all 35 entries load, and `0x074E` always matches the ID's type bits
(`01` ground, `02` underground, `00` water, `03` castle). Seen on screen:
`C0` is the underground 1-2 start, `01` is water, `60`-`65` are castles, `41`
is underground, `2C` is giant mushroom platforms with red Koopas.

Confirmed by playing: warping to 2-3 (world `01`, index `03`, level `02`, ID
`27`) and finishing it made the game advance to 2-4 on its own with index
`04`, level `03`, ID `62` (castle), so World 2's row is right in order.

Not confirmed: the level name behind the other IDs (the table order is only
a guess), and why `0x0750` read `C2` after loading `25`. The HUD is
unreliable after a warp, so check with `SCREENSHOT`.

Warped levels start with the HUD of the previous level; it corrects itself
after a death or the next level load.

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress. Cheats are writes and need the user's request: lives
`0x075A`, power-up `0x0756` (with `0x0754` = `00` for big), star timer
`0x079F`.
