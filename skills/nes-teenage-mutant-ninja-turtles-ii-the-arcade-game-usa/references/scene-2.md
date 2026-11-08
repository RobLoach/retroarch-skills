# Teenage Mutant Ninja Turtles II: Scene 2

Scene 2 in detail, as far as it has been played: a city street, from the
SCENE 2 card to progress `10`, where the street ended and nothing more
came (see The end of the street). The boss hasn't been reached. Addresses,
controls and the step-in chain are in [SKILL.md](../SKILL.md); `0x007E` is
progress, and `0x0042` reads `02`.

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
| `10` | The street's end: no more soldiers and no scrolling. |

What hurts, per hit:

| Source | Damage |
| ------ | ------ |
| Purple soldier's punch | 1-3 |
| Manhole cover | 4 |
| Firebomb burst | 4 |
| A hold, waited out | 12 in 128 frames; 27 in 268 frames once |

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

## The end of the street

Twice, from the save after the progress-`0F` wave, walking right stopped
at progress `10`: on the ledge at X 216, or on the street at X 228 on
ground line 216, where `up` didn't move him. No enemy slot held anything,
the screen didn't scroll, and nothing came in 1,080 frames of waiting.
`0x003C` stayed `03`. Jumping right on the ledge, and standing at the
building's door on the left (X 41, ground line 200), did nothing.

What triggers the rest of the scene is unknown. Two guesses, untested:
something earlier wasn't finished (the PIZZA sign object, or a soldier
that left the screen without being beaten), or this run's health writes
upset a check. A normal run that reaches `10` would settle it.
