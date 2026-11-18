# Pokémon Red: move IDs

Move IDs, as read at party slot `+0x08`, `0xD01C` and `0xCFED`. Power `0` is a
status move; `1` is a fixed-damage or one-hit-KO move. Type decides
physical or special in this game: Normal to Ghost use Attack and Defense,
Fire to Dragon use Special. From [pokered](https://github.com/pret/pokered)'s
`data/moves/moves.asm`.

| ID | Move | Type | Power | Acc. | PP |
| -- | ---- | ---- | ----- | ---- | -- |
| `01` | Pound | Normal | 40 | 100 | 35 |
| `02` | Karate Chop | Normal | 50 | 100 | 25 |
| `03` | DoubleSlap | Normal | 15 | 85 | 10 |
| `04` | Comet Punch | Normal | 18 | 85 | 15 |
| `05` | Mega Punch | Normal | 80 | 85 | 20 |
| `06` | Pay Day | Normal | 40 | 100 | 20 |
| `07` | Fire Punch | Fire | 75 | 100 | 15 |
| `08` | Ice Punch | Ice | 75 | 100 | 15 |
| `09` | ThunderPunch | Electric | 75 | 100 | 15 |
| `0A` | Scratch | Normal | 40 | 100 | 35 |
| `0B` | Vicegrip | Normal | 55 | 100 | 30 |
| `0C` | Guillotine | Normal | 1 | 30 | 5 |
| `0D` | Razor Wind | Normal | 80 | 75 | 10 |
| `0E` | Swords Dance | Normal | 0 | 100 | 30 |
| `0F` | Cut | Normal | 50 | 95 | 30 |
| `10` | Gust | Normal | 40 | 100 | 35 |
| `11` | Wing Attack | Flying | 35 | 100 | 35 |
| `12` | Whirlwind | Normal | 0 | 85 | 20 |
| `13` | Fly | Flying | 70 | 95 | 15 |
| `14` | Bind | Normal | 15 | 75 | 20 |
| `15` | Slam | Normal | 80 | 75 | 20 |
| `16` | Vine Whip | Grass | 35 | 100 | 10 |
| `17` | Stomp | Normal | 65 | 100 | 20 |
| `18` | Double Kick | Fighting | 30 | 100 | 30 |
| `19` | Mega Kick | Normal | 120 | 75 | 5 |
| `1A` | Jump Kick | Fighting | 70 | 95 | 25 |
| `1B` | Rolling Kick | Fighting | 60 | 85 | 15 |
| `1C` | Sand-Attack | Normal | 0 | 100 | 15 |
| `1D` | Headbutt | Normal | 70 | 100 | 15 |
| `1E` | Horn Attack | Normal | 65 | 100 | 25 |
| `1F` | Fury Attack | Normal | 15 | 85 | 20 |
| `20` | Horn Drill | Normal | 1 | 30 | 5 |
| `21` | Tackle | Normal | 35 | 95 | 35 |
| `22` | Body Slam | Normal | 85 | 100 | 15 |
| `23` | Wrap | Normal | 15 | 85 | 20 |
| `24` | Take Down | Normal | 90 | 85 | 20 |
| `25` | Thrash | Normal | 90 | 100 | 20 |
| `26` | Double-Edge | Normal | 100 | 100 | 15 |
| `27` | Tail Whip | Normal | 0 | 100 | 30 |
| `28` | Poison Sting | Poison | 15 | 100 | 35 |
| `29` | Twineedle | Bug | 25 | 100 | 20 |
| `2A` | Pin Missile | Bug | 14 | 85 | 20 |
| `2B` | Leer | Normal | 0 | 100 | 30 |
| `2C` | Bite | Normal | 60 | 100 | 25 |
| `2D` | Growl | Normal | 0 | 100 | 40 |
| `2E` | Roar | Normal | 0 | 100 | 20 |
| `2F` | Sing | Normal | 0 | 55 | 15 |
| `30` | Supersonic | Normal | 0 | 55 | 20 |
| `31` | Sonicboom | Normal | 1 | 90 | 20 |
| `32` | Disable | Normal | 0 | 55 | 20 |
| `33` | Acid | Poison | 40 | 100 | 30 |
| `34` | Ember | Fire | 40 | 100 | 25 |
| `35` | Flamethrower | Fire | 95 | 100 | 15 |
| `36` | Mist | Ice | 0 | 100 | 30 |
| `37` | Water Gun | Water | 40 | 100 | 25 |
| `38` | Hydro Pump | Water | 120 | 80 | 5 |
| `39` | Surf | Water | 95 | 100 | 15 |
| `3A` | Ice Beam | Ice | 95 | 100 | 10 |
| `3B` | Blizzard | Ice | 120 | 90 | 5 |
| `3C` | Psybeam | Psychic | 65 | 100 | 20 |
| `3D` | Bubblebeam | Water | 65 | 100 | 20 |
| `3E` | Aurora Beam | Ice | 65 | 100 | 20 |
| `3F` | Hyper Beam | Normal | 150 | 90 | 5 |
| `40` | Peck | Flying | 35 | 100 | 35 |
| `41` | Drill Peck | Flying | 80 | 100 | 20 |
| `42` | Submission | Fighting | 80 | 80 | 25 |
| `43` | Low Kick | Fighting | 50 | 90 | 20 |
| `44` | Counter | Fighting | 1 | 100 | 20 |
| `45` | Seismic Toss | Fighting | 1 | 100 | 20 |
| `46` | Strength | Normal | 80 | 100 | 15 |
| `47` | Absorb | Grass | 20 | 100 | 20 |
| `48` | Mega Drain | Grass | 40 | 100 | 10 |
| `49` | Leech Seed | Grass | 0 | 90 | 10 |
| `4A` | Growth | Normal | 0 | 100 | 40 |
| `4B` | Razor Leaf | Grass | 55 | 95 | 25 |
| `4C` | SolarBeam | Grass | 120 | 100 | 10 |
| `4D` | Poisonpowder | Poison | 0 | 75 | 35 |
| `4E` | Stun Spore | Grass | 0 | 75 | 30 |
| `4F` | Sleep Powder | Grass | 0 | 75 | 15 |
| `50` | Petal Dance | Grass | 70 | 100 | 20 |
| `51` | String Shot | Bug | 0 | 95 | 40 |
| `52` | Dragon Rage | Dragon | 1 | 100 | 10 |
| `53` | Fire Spin | Fire | 15 | 70 | 15 |
| `54` | ThunderShock | Electric | 40 | 100 | 30 |
| `55` | Thunderbolt | Electric | 95 | 100 | 15 |
| `56` | Thunder Wave | Electric | 0 | 100 | 20 |
| `57` | Thunder | Electric | 120 | 70 | 10 |
| `58` | Rock Throw | Rock | 50 | 65 | 15 |
| `59` | Earthquake | Ground | 100 | 100 | 10 |
| `5A` | Fissure | Ground | 1 | 30 | 5 |
| `5B` | Dig | Ground | 100 | 100 | 10 |
| `5C` | Toxic | Poison | 0 | 85 | 10 |
| `5D` | Confusion | Psychic | 50 | 100 | 25 |
| `5E` | Psychic M | Psychic | 90 | 100 | 10 |
| `5F` | Hypnosis | Psychic | 0 | 60 | 20 |
| `60` | Meditate | Psychic | 0 | 100 | 40 |
| `61` | Agility | Psychic | 0 | 100 | 30 |
| `62` | Quick Attack | Normal | 40 | 100 | 30 |
| `63` | Rage | Normal | 20 | 100 | 20 |
| `64` | Teleport | Psychic | 0 | 100 | 20 |
| `65` | Night Shade | Ghost | 0 | 100 | 15 |
| `66` | Mimic | Normal | 0 | 100 | 10 |
| `67` | Screech | Normal | 0 | 85 | 40 |
| `68` | Double Team | Normal | 0 | 100 | 15 |
| `69` | Recover | Normal | 0 | 100 | 20 |
| `6A` | Harden | Normal | 0 | 100 | 30 |
| `6B` | Minimize | Normal | 0 | 100 | 20 |
| `6C` | Smokescreen | Normal | 0 | 100 | 20 |
| `6D` | Confuse Ray | Ghost | 0 | 100 | 10 |
| `6E` | Withdraw | Water | 0 | 100 | 40 |
| `6F` | Defense Curl | Normal | 0 | 100 | 40 |
| `70` | Barrier | Psychic | 0 | 100 | 30 |
| `71` | Light Screen | Psychic | 0 | 100 | 30 |
| `72` | Haze | Ice | 0 | 100 | 30 |
| `73` | Reflect | Psychic | 0 | 100 | 20 |
| `74` | Focus Energy | Normal | 0 | 100 | 30 |
| `75` | Bide | Normal | 0 | 100 | 10 |
| `76` | Metronome | Normal | 0 | 100 | 10 |
| `77` | Mirror Move | Flying | 0 | 100 | 20 |
| `78` | Selfdestruct | Normal | 130 | 100 | 5 |
| `79` | Egg Bomb | Normal | 100 | 75 | 10 |
| `7A` | Lick | Ghost | 20 | 100 | 30 |
| `7B` | Smog | Poison | 20 | 70 | 20 |
| `7C` | Sludge | Poison | 65 | 100 | 20 |
| `7D` | Bone Club | Ground | 65 | 85 | 20 |
| `7E` | Fire Blast | Fire | 120 | 85 | 5 |
| `7F` | Waterfall | Water | 80 | 100 | 15 |
| `80` | Clamp | Water | 35 | 75 | 10 |
| `81` | Swift | Normal | 60 | 100 | 20 |
| `82` | Skull Bash | Normal | 100 | 100 | 15 |
| `83` | Spike Cannon | Normal | 20 | 100 | 15 |
| `84` | Constrict | Normal | 10 | 100 | 35 |
| `85` | Amnesia | Psychic | 0 | 100 | 20 |
| `86` | Kinesis | Psychic | 0 | 80 | 15 |
| `87` | Softboiled | Normal | 0 | 100 | 10 |
| `88` | Hi Jump Kick | Fighting | 85 | 90 | 20 |
| `89` | Glare | Normal | 0 | 75 | 30 |
| `8A` | Dream Eater | Psychic | 100 | 100 | 15 |
| `8B` | Poison Gas | Poison | 0 | 55 | 40 |
| `8C` | Barrage | Normal | 15 | 85 | 20 |
| `8D` | Leech Life | Bug | 20 | 100 | 15 |
| `8E` | Lovely Kiss | Normal | 0 | 75 | 10 |
| `8F` | Sky Attack | Flying | 140 | 90 | 5 |
| `90` | Transform | Normal | 0 | 100 | 10 |
| `91` | Bubble | Water | 20 | 100 | 30 |
| `92` | Dizzy Punch | Normal | 70 | 100 | 10 |
| `93` | Spore | Grass | 0 | 100 | 15 |
| `94` | Flash | Normal | 0 | 70 | 20 |
| `95` | Psywave | Psychic | 1 | 80 | 15 |
| `96` | Splash | Normal | 0 | 100 | 40 |
| `97` | Acid Armor | Poison | 0 | 100 | 40 |
| `98` | Crabhammer | Water | 90 | 85 | 10 |
| `99` | Explosion | Normal | 170 | 100 | 5 |
| `9A` | Fury Swipes | Normal | 18 | 80 | 15 |
| `9B` | Bonemerang | Ground | 50 | 90 | 10 |
| `9C` | Rest | Psychic | 0 | 100 | 10 |
| `9D` | Rock Slide | Rock | 75 | 90 | 10 |
| `9E` | Hyper Fang | Normal | 80 | 90 | 15 |
| `9F` | Sharpen | Normal | 0 | 100 | 30 |
| `A0` | Conversion | Normal | 0 | 100 | 30 |
| `A1` | Tri Attack | Normal | 80 | 100 | 10 |
| `A2` | Super Fang | Normal | 1 | 90 | 10 |
| `A3` | Slash | Normal | 70 | 100 | 20 |
| `A4` | Substitute | Normal | 0 | 100 | 10 |
| `A5` | Struggle | Normal | 50 | 100 | 10 |
