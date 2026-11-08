# Teenage Mutant Ninja Turtles II: Scene 1

Scene 1 in detail: getting past the bombs, what each stretch brings, and
the boss. Addresses, controls and the step-in chain are in
[SKILL.md](../SKILL.md); `0x007E` is progress, `0x0419` the boss's action.

## Bombs

Bombs start whenever a bomb slot is free and the turtle is right of about
X 58 (see [SKILL.md](../SKILL.md#playing)). What got past, with no damage:

- **First staircase** (progress `07`): wait on the bottom line below the
  stairs until the bomb above has rolled below him (`until 4ab >= 205` for
  the bomb in slot 9), then hold right: the next bomb starts behind him.
  More blue soldiers wait past the stairs, and bombs still roll into that
  fight, so check every odd slot before each chain.
- **Second staircase** (progress `0D`): the moment the first bomb appears
  (X 174, ground line 80) with the turtle at X 227, keep pushing right.
  The scroll carries the stairs and their bombs left faster than a bomb
  comes down, and 90 frames later he was clear. Standing still there was
  hit.

## Route

What one Raphael run met, by progress (`0x007E`). Counts are soldiers
seen in that stretch, approximate; slots refill as soldiers fall.

| Progress | What comes |
| -------- | ---------- |
| `01` | The first soldier, sprinting in from the left (see [SKILL.md](../SKILL.md#playing)). |
| `02` | 4 soldiers from both edges; one comes up behind the turtle. |
| `03` | 4, one with a spear. |
| `05` | 3. |
| `06` | 4; the first staircase is in view. |
| `07` | First staircase: bombs. |
| `08`-`09` | Past the stairs: about 5 blue soldiers with shuriken, bombs still rolling. |
| `0B` | A burning doorway throws debris; about 4 soldiers. |
| `0C` | 3-4, one throwing shuriken. |
| `0D` | Second staircase: bombs. |
| `0E` | 2 blue soldiers. |
| `0F` | 2-3, one rising from the bottom edge. |
| `11` | 3, one out of a burning door. |
| `13` | 4. |
| `14` | A red elevator door; 3. |
| `15` | White soldiers (hit for 4), 3-4. |
| `16`-`17` | 3 out of doors. |
| `1A` | The three white ninjas, then the door to the boss room. |

What hurts, per hit:

| Source | Damage |
| ------ | ------ |
| Purple soldier's punch | 1-3 |
| White soldier | 4 |
| Shuriken, ninja knife | 1 |
| Bomb | 8 |
| Boss: charge or swing | 4 |
| Boss: shot | 1-4 |
| A hold, not broken | Repeated hits: 38 in one call |

The score (`0x03F0`) read 70 PTS at the end of Scene 1: about one per
soldier.

## Boss

After the white ninjas, the turtle walks out through a door (`0x003C`
`05`, then `02`) into an apartment (`0x0042` `01`, progress from `00`).
Five Foot soldiers come first, in twos, walking right to trigger the
next. At progress `04` the boss steps out of the capsule door at the back:
slot 7, health `40` (64), two per hit, so 32 hits. It hits for 4 and:

- Charges along its own ground line at about 4 px per frame, about 45
  frames after it stands still (`0x0419` `03`), hitting from about 38 px.
  Swinging into the charge doesn't stop it. Jumping does: `STEPS until 485
  >= 100; press 1 a 4; until 412 == 0` with the boss charging right from
  X 63 and the turtle at X 185 landed with the boss 30 px behind him.
- Shoots along its line when the turtle is far away: 1 to 4 per shot. One
  wait at range for a charge that never came cost 8.
- Follows the turtle's ground line; this room's lines run only from about
  151 to 196, so stepping out of its way doesn't work.

**The exchange.** One chain of three swings from 33-38 px, then get off
its line: `STEPS checkpoint; stop 568 < <hp - 4>; press 1 b 4; run 10;
press 1 b 4; run 10; press 1 b 4; run 10; until 412 == 0; press 1 right+a
4; until 412 == 0` (`left+a` when the boss is to the right). In a second
session, eight chains from 33-38 px all landed, each taking 4 off the
boss. After the chain:

| Then | Tries | Cost to the turtle |
| ---- | ----- | ------------------ |
| Jump away (`right+a`, boss on the left) | 5 | 0, 0, 0, 1, 1 |
| Jump toward it (`left+a`) | 1 | 1 |
| `down 30`, off its line | 1 | 0 |
| `up 30`, off its line | 1 | 4: too slow at 0.6 px a frame |
| A second chain straight away | 2 | 4 each |

The clean jumps came while the boss walked in (`0x0419` `02`); against the
left wall it shot as the turtle jumped (1 each) and threw him back to about
X 197. After every two exchanges or so the boss backs off 80-130 px and
shoots: walk straight back in to 35 px (`stop 47e <= <boss X + 35>; press 1
left 140`, which cost about 2 to shots each time) and chain the moment the
walk stops. Waiting at range for a charge got shot instead, so jump the
charge only when it comes. By those costs, 16 exchanges from full health
would cost about 20-25 (an estimate, not a run); Raphael won it on his last life from 31 the first time, by
trading. Defeating the boss (`0x0419` `05`) plays a short scene, then
`0x003C` `05`, `02`, and the SCENE 2 card with `0x003C` `01`.
