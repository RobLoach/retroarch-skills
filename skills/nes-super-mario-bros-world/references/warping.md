# Super Mario Bros.: warping to a level

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
