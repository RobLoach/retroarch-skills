# Teenage Mutant Ninja Turtles II: Scene 2

Scene 2 in detail: a city street from the SCENE 2 card to its boss and on
to Scene 3. Addresses, controls and the step-in chain are in
[SKILL.md](../SKILL.md); `0x007E` is progress, and `0x0042` reads `02`.

The street stops scrolling twice, at progress `10` and `12`, until the
turtle walks a particular way: see Moving on.

From progress `08` on, these notes come from a run whose health was topped
up with `WRITE_CORE_MEMORY 568 3C` while mapping. Damage figures from that
stretch are what was lost between top-ups.

## Start

- Health refills to `3C` (60) when the scene starts; it read `32` (50) at
  the end of Scene 1. Lives in reserve don't refill: `00` stayed `00`.
- The turtle starts at X 128 on ground line 206. The street's lines run
  from about 175 to 224, deeper than Scene 1's hallway.
- A Continue here (see [SKILL.md](../SKILL.md#setup)) restarted Scene 2
  from its start, not Scene 1, with lives `02`, health 60 and the score kept.

## Route

What three Raphael runs met, by progress (`0x007E`). Counts are soldiers
seen in that stretch, approximate; slots refill as soldiers fall.

| Progress | What comes |
| -------- | ---------- |
| `01` | A soldier by the first manhole (slot 7, X 47, ground line 192-215) throwing manhole covers. |
| `02` | 4 from both edges and a second manhole. |
| `04` | By a broken wall: about 6. They hop past the turtle and come at him from both sides. |
| `06` | A storefront: 3. |
| `08` | Shredder on a TV in a shop window; 4, some blue. |
| `09` | One climbs out of an open manhole just above the turtle (slot 7, X 217, ground line 144), then walks down to his line. |
| `0A` | 4; one held the turtle from behind. |
| `0B` | Firebombs: about 7, more than one carrying bombs in turn. The costliest stretch. |
| `0C` | A red PIZZA sign on the wall is an object: slot 7 reads `FF` at Y 112. Walking under it restored nothing. |
| `0F` | About 6 jump down from the windows. Part of this block has a raised ledge (see below). |
| `10` | The street seems to end. Walk right along the bottom line (see Moving on). |
| `12` | A ramp down beside a building: 3. Then walk down and left. |
| `14` | Yellow soldiers out of the building: 3. They throw stars (an even slot reading `80`). |
| `16` | 3, purple and yellow. |
| `18` | 3 yellow, throwing stars; then walk down-left to the bottom left, then right. |
| `1B` | A Pizza Hut: its posters fall off the windows and about 6 yellow soldiers break out. |
| `1C` | A brick wall: about 6. Then a wrecked car, where the street stops again until the turtle walks right along the bottom line. |
| `1D`-`1E` | Another manhole-cover thrower, an open manhole (see below), and 3 yellow soldiers. |
| `1F` | The boss. |

What hurts, per hit:

| Source | Damage |
| ------ | ------ |
| Purple soldier's punch | 1-3 |
| Manhole cover | 4 |
| Firebomb burst | 4 |
| A hold, waited out | 12 in 128 frames; 27 in 268 frames once |
| Falling into an open manhole | 5 |
| Boss: shot | about 6 |
| Boss: swing or charge | 4 |

## Manhole covers

The first soldier stays at the manhole (X 47) and throws covers along its
line: slot 9 reads `FF` while one flies, at Y about 186. Walking straight
at it on the start line lost 8. Walking down and left to the bottom line
(`STEPS stop 47e <= 82; press 1 down+left 140`, ending at ground line 224)
took nothing, and a step-in chain from 35 px, 9 lines from its own,
defeated it: `press 1 left 4;` then the two chains.

## Firebombs

From progress `0B` a soldier carries a firebomb: an `FF` slot (8, 13 or
15) follows that soldier's X. Thrown, it lands near the turtle and bursts
(the frame shows a burst of flame at his feet), and the slot clears. The
carriers stand 45-55 px off and throw again, so waiting for them to come
in costs a burst each time. What worked:

- Go straight for the carrier, even to the top of the street (`stop 4a2
  <= 156; press 1 up+left 60` reached one on ground line 158), and chain.
- When an `FF` slot sits within about 10 px of the turtle's X on his line,
  step 15-20 lines away (`press 1 up+right 18`) before anything else.

## Holds

Scene 2's soldiers often come in from behind and hold the turtle. The
action byte reads `04`, and sometimes `06` (one hold read `06` for 268
frames). His X and ground line shift toward the holder. Don't start a
call with `until 412 == 0` while it reads either: one such call lost 12,
another 27. Mash at once and stop when it lets go: `STEPS stop 412 == 0;
press 1 left+b 3; press 1 right+b 3`, the pair repeated 6 times, freed him
in 7-26 frames. A plain knockdown also reads `06` and ends by itself
within about 10 frames; the mash does no harm then.

## The raised ledge

Past the PIZZA sign, the turtle's ground line 200 sits on a ledge: Y reads
116 there, 84 above the ground line, and the window jumpers fight him up
there. `down` steps him off it to the street (Y back on his ground line).

## Moving on

The street stops scrolling in a few places with no soldiers left, and
waiting or walking right on most lines does nothing:

- **Progress `10`**, past the window jumpers: walk right along the bottom
  line (ground line 224) to the bottom-right corner. The screen scrolls on
  and progress becomes `12`. Walking right on line 216, or on the raised
  ledge, stopped at X 228 and 216 for 1,080 frames.
- **Progress `12`-`18`**, down the ramp: this stretch scrolls when the
  turtle walks down and left (`press 1 down+left 400`), not right. At
  progress `14`, right for 300 frames stayed at `14`, and down-left reached
  `16` in 85 frames.
- **Progress `18`**, after the wave: walk down-left to the bottom left (X
  23, ground line 224), then right; progress became `19` after about 270
  frames, twice. Right on line 190, or right along the bottom line without
  the trip left, stayed at `18` for 400 frames.
- **Progress `1C`**, at the wrecked car: walk right along the bottom line
  (`press 1 down 70; press 1 right 300`); `1D` came after 122 frames. Right
  on line 185 for 450 frames stayed at `1C`.

The `14`, `18` and `1C` steps were checked again from saves with no memory
writes; the one at `10` was seen only in the run whose health was topped
up.

## Open manholes

An open manhole on the street (X 192, ground line 208 at progress `1E`)
swallows a turtle who walks over it: he vanishes, a bubble says "Who put
the lights out?", and about 100 frames later he climbs out 5 health down,
on the same spot. Standing there drops him in again, so step up and left
off it at once (`press 1 up+left 30`).

## Boss

At progress `1F`, beside the wrecked car, a big gunman like Scene 1's boss
arrives from the left: slot 7, health `50` (80), so 40 hits. It shot from
about 60 px or more (about 6 a shot), and the shots push the turtle back:
walking left at it for 120 frames moved him 28 px right instead. It walks
in and swings from about 30 px (4), and follows the turtle's ground line,
also to the top of the street.

What landed, from 80 to 0 (health topped up throughout):

- Three combos in a row from point-blank (under 10 px), with `press 1
  right 3` between them, did best: 6-8 for 4-8 lost a round, and 26 to 18
  for 4 once, while the boss stood against the left side of the street.
  It often steps behind the turtle mid-combo, and sometimes throws him
  60-90 px away: check its X between combos, and turn.
- Walking in and chaining from 30-35 px took 2-6 for 4-14 lost.
- Waiting at range to jump a charge, as in Scene 1, got shot instead.

The whole fight cost about 110 health in top-ups, so on a normal run plan
on losing one or two lives here.

Beaten, the boss reads `0x0419` `05`. About 150 frames later `0x003C`
reads `04` (a value seen only here so far), then `05`, the SCENE 3 card
(`01`), and play in the sewers: `0x0042` `03`, health refilled to 60,
progress from `00`, the turtle at X 128 on ground line 176.
