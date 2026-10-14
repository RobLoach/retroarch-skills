# Contributing

Each skill teaches an assistant to play one game through RetroArch's MCP
server. To add a game:

1. Load the game in RetroArch, and ask the assistant to create a skill for
   it. The [`create-game-skill`](skills/create-game-skill/SKILL.md) skill
   has it work out the controls, memory addresses and a memory signature by
   experiment, then write `skills/<name>/SKILL.md` from its
   [template](skills/create-game-skill/assets/template.md). To write one by
   hand instead, copy the template and fill it in.
2. Read what it wrote, and test it against the real game. Check anything the
   assistant says it didn't verify. Make sure the game is in the Games list
   in `README.md`, under its system.
3. Run `python3 scripts/validate.py`.
4. Open a pull request.

## Naming

Start with the game's exact [No-Intro](https://no-intro.org) name, as listed in
[libretro-database](https://github.com/libretro/libretro-database), for example
`Super Mario Bros. (World)`.

The directory name and the `name` field are the system's code, a `-`, and the
slug of the No-Intro name. To slug the name:

1. Convert accented letters to plain ASCII (`Pokémon` becomes `pokemon`).
2. Lowercase it.
3. Remove apostrophes (`Kirby's` becomes `kirbys`).
4. Replace each run of other non-alphanumeric characters with a single `-`.
5. Trim leading and trailing `-`.

| Code | No-Intro name | Directory |
| --- | --- | --- |
| `nes` | `Super Mario Bros. (World)` | `nes-super-mario-bros-world` |
| `nes` | `Legend of Zelda, The (USA)` | `nes-legend-of-zelda-the-usa` |
| `nes` | `Kirby's Adventure (USA) (Rev 1)` | `nes-kirbys-adventure-usa-rev-1` |
| `md` | `Sonic The Hedgehog (USA, Europe)` | `md-sonic-the-hedgehog-usa-europe` |

The codes are in `SYSTEM_CODES` in
[`scripts/validate.py`](scripts/validate.py), such as `nes`, `snes`, `gb`,
`gba`, `md` and `psx`. For a system that isn't listed yet, add a short code
there. The prefix keeps games that share a name on different systems apart:
`Pac-Man (USA)` is a No-Intro name on five systems.

The [Agent Skills spec](https://agentskills.io/specification) requires these
rules. A skill's `name` must be lowercase letters, numbers, and hyphens, and it
must match its directory.

General skills that aren't about one game, such as `create-game-skill`, have no
`metadata` map. The validator checks their `name`, `description`, `license`,
`compatibility` and `allowed-tools`, but not `metadata`.

## Frontmatter

```yaml
---
name: nes-super-mario-bros-world
description: Plays Super Mario Bros. (World) on the Nintendo Entertainment System through RetroArch's MCP server. Use when GET_STATUS reports Super Mario Bros. (World) or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__PRESS ...
metadata:
  game: "Super Mario Bros. (World)"
  system: "Nintendo - Nintendo Entertainment System"
  cores: "fceumm_libretro nestopia_libretro mesen_libretro quicknes_libretro"
  crc32: "D445F698"
---
```

- `name`: the system code, a `-`, and the slug, matching the directory.
- `description`: one line, at most 1024 characters. Say what the skill does,
  then when to use it. The assistant sees only this text when it decides
  whether to load the skill.
- `license`: `MIT`, so the license travels with a skill copied out on its
  own.
- `compatibility`: what the skill needs to run, at most 500 characters. Copy
  it from the template.
- `allowed-tools`: the RetroArch tools the assistant may call without a
  prompt while the skill is active, separated by spaces. Copy the template's
  list: reads, input and frame stepping. Never add a tool that can lose
  progress, such as `RESET`, `WRITE_CORE_MEMORY`, `LOAD_CONTENT`, or the save
  state tools; the validator rejects them.
- `metadata.game`: the exact No-Intro name.
- `metadata.system`: the libretro-database system name, such as
  `Nintendo - Super Nintendo Entertainment System`.
- `metadata.cores`: the cores the skill works with, separated by spaces, most
  preferred first. A skill that reads memory needs a core that publishes a
  memory map (`GET_MEMORY_MAP`), and the map must place the RAM at the
  addresses the skill uses. List more than one core where you can, and don't
  write instructions that only one core needs.
- `metadata.crc32`: optional. The ROM's CRC32 as listed in No-Intro, as 8 hex
  digits. "Confirm the game" checks the name and a memory signature. An
  assistant that can read the ROM file, found through the system playlist,
  also compares CRCs when the name differs or the memory can't be read. It
  asks the user only when it can verify neither. For formats with a header,
  such as `.nes`, give the CRC without the header, because headers differ
  between dumps of the same ROM. Say in "Confirm the game" how many bytes to
  skip.

Keep every value on one line. The validator does not parse multi-line YAML.

## Writing a good game skill

- **Confirm the game by memory.** Give a few RAM bytes the game writes and
  keeps in every mode, such as a warm-boot marker or code copied into RAM.
  This also catches renamed ROMs and cores without a memory map.
- **Verify everything in the running game.** Test each memory address with
  `READ_CORE_MEMORY`, and test each input sequence with `PRESS` or
  `SET_INPUT`. Don't copy RAM maps without checking them.
- **Use frames, not seconds.** Tools such as `PRESS` and `RUN_FRAMES` count
  frames. Give timings as frame counts, and state the frame rate, for example
  60 for NTSC or 50 for PAL.
- **Use the RetroPad.** Give controls as RetroPad names (`a`, `b`, `start`,
  `right`, `right+a`), not as the original console's button labels.
- **Read state, don't guess it.** An addresses table beats screenshots. List
  each address with its size and meaning.
- **Save states use the AI Agent save slots, 990-999, only.** Skills share
  them, so the player's own slots are never touched.
- **Mark destructive steps.** `RESET`, `CLOSE_CONTENT`, and
  `WRITE_CORE_MEMORY` can lose the player's progress. Tell the assistant to ask
  first.
- **Keep it short.** Keep `SKILL.md` under about 500 lines. Put long material,
  such as full level routes, in separate files next to it and link to them.
- **Don't include ROMs or links to ROMs.**

## Validation

```sh
python3 scripts/validate.py
```

The validator checks names, frontmatter, duplicate games, and that every game
is in the README's Games list. CI runs it on every pull request.
