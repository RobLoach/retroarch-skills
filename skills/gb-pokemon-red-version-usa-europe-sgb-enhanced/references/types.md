# Pokémon Red: types

Type IDs, as read at party slot `+0x05` and `+0x06`, `0xD019` and `0xCFEA`. A
Pokémon with one type has it in both bytes. From
[pokered](https://github.com/pret/pokered)'s `constants/type_constants.asm`
and `data/types/type_matchups.asm`.

| ID | Type | ID | Type |
| -- | ---- | -- | ---- |
| `00` | Normal | `14` | Fire |
| `01` | Fighting | `15` | Water |
| `02` | Flying | `16` | Grass |
| `03` | Poison | `17` | Electric |
| `04` | Ground | `18` | Psychic |
| `05` | Rock | `19` | Ice |
| `07` | Bug | `1A` | Dragon |
| `08` | Ghost |  | |

## Damage

Attacking type down the side, defending type across the top. `2` is super
effective, `½` not very effective, `0` no effect, blank normal. Against two
types, multiply both. A move of the attacker's own type does 1.5×.

This is the game's own table, with its Gen 1 quirks: Ghost does nothing to
Psychic, Ice is neutral on Fire, and Bug and Poison are super effective on
each other.

| | Nor | Fig | Fly | Poi | Gro | Roc | Bug | Gho | Fir | Wat | Gra | Ele | Psy | Ice | Dra |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Nor** |  |  |  |  |  | ½ |  | 0 |  |  |  |  |  |  |  |
| **Fig** | 2 |  | ½ | ½ |  | 2 | ½ | 0 |  |  |  |  | ½ | 2 |  |
| **Fly** |  | 2 |  |  |  | ½ | 2 |  |  |  | 2 | ½ |  |  |  |
| **Poi** |  |  |  | ½ | ½ | ½ | 2 | ½ |  |  | 2 |  |  |  |  |
| **Gro** |  |  | 0 | 2 |  | 2 | ½ |  | 2 |  | ½ | 2 |  |  |  |
| **Roc** |  | ½ | 2 |  | ½ |  | 2 |  | 2 |  |  |  |  | 2 |  |
| **Bug** |  | ½ | ½ | 2 |  |  |  | ½ | ½ |  | 2 |  | 2 |  |  |
| **Gho** | 0 |  |  |  |  |  |  | 2 |  |  |  |  | 0 |  |  |
| **Fir** |  |  |  |  |  | ½ | 2 |  | ½ | ½ | 2 |  |  | 2 | ½ |
| **Wat** |  |  |  |  | 2 | 2 |  |  | 2 | ½ | ½ |  |  |  | ½ |
| **Gra** |  |  | ½ | ½ | 2 | 2 | ½ |  | ½ | 2 | ½ |  |  |  | ½ |
| **Ele** |  |  | 2 |  | 0 |  |  |  |  | 2 | ½ | ½ |  |  | ½ |
| **Psy** |  | 2 |  | 2 |  |  |  |  |  |  |  |  | ½ |  |  |
| **Ice** |  |  | 2 |  | 2 |  |  |  |  | ½ | 2 |  |  | ½ | 2 |
| **Dra** |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 2 |
