# Super Mario Bros.: World 1-1 in five queued calls

Hold `right+b` with `INPUT set 1 right+b 1` first, and `WATCH` the line in
[SKILL.md](../SKILL.md#memory). Each line below is one `STEPS` call with
`queue: on`.

This route cleared 1-1 twice with no deaths, holding `right+b` from the
start, queued one list after another (each line is one `STEPS` call; add
`stop e == 11; stop b5 > 1` to the first):

```
checkpoint; until 6d:86 >= 262; press 1 a 18; until 1d == 0; until 6d:86 >= 405; until 1d == 0; press 1 a 25; until 1d == 0; until 6d:86 >= 568; until 1d == 0; press 1 a 25; until 1d == 0; press 1 a 35; until 1d == 0; until 6d:86 >= 760; press 1 a 30; until 1d == 0
press 1 a 35; until 1d == 0; until 6d:86 >= 1082; until 1d == 0; press 1 a 20; until 1d == 0; until 6d:86 >= 1218; press 1 a 10; until 1d == 0; press 1 a 10; until 1d == 0; until 6d:86 >= 1346; until 1d == 0; press 1 a 22; until 1d == 0; checkpoint
press 1 a 14; until 1d == 0; until 6d:86 >= 1638; press 1 a 12; until 1d == 0; until 6d:86 >= 1768; until 1d == 0; press 1 a 14; until 1d == 0; until 6d:86 >= 1912; until 1d == 0; press 1 a 24; until 1d == 0; checkpoint
until 6d:86 >= 2110; press 1 a 30; until 1d == 0; press 1 a 30; until 1d == 0; until 6d:86 >= 2330; until 1d == 0; press 1 a 30; until 1d == 0; press 1 a 30; until 1d == 0; press 1 a 25; until 1d == 0
until 1d == 0; until 6d:86 >= 2722; until 1d == 0; press 1 a 14; until 1d == 0; until 6d:86 >= 2830; until 1d == 0; press 1 a 25; until 1d == 0; press 1 a 30; until 1d == 0; press 1 a 30; until 1d == 0; until 760 == 1
```

It ends with 1-2 loading, about 1,500 frames of play. The lists end against
pipe 4 (x 898), after gap 2 (1480), past the goomba group (2079) and on pipe
5 (2628), which the next list assumes; check `x` in each reply before trusting
the next. Played this way, 1-1 took 18 calls, against 48 one stretch at a
time.
