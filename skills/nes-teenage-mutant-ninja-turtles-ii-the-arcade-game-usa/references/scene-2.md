# Teenage Mutant Ninja Turtles II: Scene 2

Scene 2 in detail, as far as it has been played: a city street, from the
SCENE 2 card to progress `0B`. The stretch past `0B` and the boss haven't
been reached yet. Addresses, controls and the step-in chain are in
[SKILL.md](../SKILL.md); `0x007E` is progress, and `0x0042` reads `02`.

## Start

- Health refills to `3C` (60) when the scene starts; it read `32` (50) at
  the end of Scene 1. Lives in reserve don't refill: `00` stayed `00`.
- The turtle starts at X 128 on ground line 206. The street's lines run
  from about 175 to 224, deeper than Scene 1's hallway.
- A Continue here (see [SKILL.md](../SKILL.md#setup)) restarted Scene 2
  from its start, not Scene 1, with lives `02`, health 60 and the score kept.

## Route

What two Raphael runs met, by progress (`0x007E`). Counts are soldiers
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
| `0B` | Firebomb throwers, 4 or more. Not passed: both runs lost 20 or more here. |

What hurts, per hit:

| Source | Damage |
| ------ | ------ |
| Purple soldier's punch | 1-3 |
| Manhole cover | 4 |
| Firebomb, and the fire it leaves | 4 a touch, again while the turtle stands in it |
| A hold, waited out | 12 in 128 frames |

## Manhole covers

The first soldier stays at the manhole (X 47) and throws covers along its
line: slot 9 reads `FF` while one flies, at Y about 186. Walking straight
at it on the start line lost 8. Walking down and left to the bottom line
(`STEPS stop 47e <= 82; press 1 down+left 140`, ending at ground line 224)
took nothing, and a step-in chain from 35 px, 9 lines from its own,
defeated it: `press 1 left 4;` then the two chains.

## Firebombs

From progress `0B` a soldier carries a firebomb: slot 8 reads `FF` and
follows that soldier's X. Thrown, it bursts into a small fire on the
ground (an `FF` slot, 8 or 15, sitting at the turtle's feet), which keeps
hurting while he stands in it. Read every slot, the even ones too, when
the turtle loses health with no soldier close: step 20 or more lines off
the fire (`press 1 up+left 25` worked) before fighting on. Kill the
carrier first; both runs lost most of their health here to fire and to
soldiers behind the turtle.

## Holds

Scene 2's soldiers often come in from behind and hold the turtle (`0x0412`
`04`, his X and ground line shifted toward the holder). Don't start a call
with `until 412 == 0` while it reads `04`: that call waited 128 frames
while the hold took 12. Mash at once and stop when it lets go: `STEPS stop
412 != 4; press 1 left+b 3; press 1 right+b 3` repeated 6 times freed him
in 22-26 frames for no further damage.
