---
name: create-game-skill
description: Creates a new game skill by working out a game's controls and memory addresses through experiment in RetroArch's MCP server. Use only when the user explicitly asks to create or learn a skill for a game.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__SET_INPUT mcp__retroarch__RELEASE_INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST
---

# Create a game skill

Work out how to play the loaded game by experiment, then record what you
verified as a new game skill.

## Before starting

1. Call `GET_STATUS`. If a skill already covers the game, tell the user and
   offer to improve it instead.
2. Save and load only the AI Agent save slots, 990-999, and never touch any
   other slot. Keep a title-screen save in one of them, so you can return
   without a reset. Ask before `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`.
3. Call `GET_MEMORY_MAP`. If the core publishes no map, memory reads fail. Tell
   the user, and suggest a core from `LIST_CORES <content path>` that
   publishes one.

## Gather leads

Treat these as guesses until tested in the game.

- **Cheat files.** RetroArch keeps them under
  `database/cht/<system>/<game>.cht` in its config directory, from
  [libretro-database](https://github.com/libretro/libretro-database/tree/master/cht).
  Only `ADDR:VALUE` codes such as `075A:09` are RAM addresses, and their
  descriptions say what the byte holds ("Infinite Lives"). Letter codes such as
  Game Genie patch the ROM; skip them.
- **Your own knowledge** of published RAM maps for the game.

## Find state by experiment

Save to an AI Agent slot, read a small range, change one thing, read again,
compare. Reload to repeat.

- **Position:** hold a direction for a known number of frames. X grows by about
  speed times frames, and a page byte nearby usually counts each 256.
- **Counters** (lives, coins, score, timer): trigger the event and look for the
  byte that moves by the expected amount. Digits are often one per byte.
- **Modes and states:** compare the same byte on the title screen, in play,
  while dying, and at the end of a level.
- **Enemies and objects:** usually parallel arrays, one byte per slot at
  consecutive addresses for active, type, X, Y and state.
- **Terrain:** look for a block of RAM whose bytes repeat where the screen shows
  ground, and whose gaps line up with pits.
- **Signature** for Confirm the game: bytes that are the same in every mode.
  Read all of RAM, in reads that stay inside one memory map region, soon after
  loading, on the title screen, in the demo, and in play from several saves.
  Keep the bytes that never change and aren't `00` or `FF`. Prefer a warm-boot
  marker (Super Mario Bros. keeps `A5` at `0x07FF`) or code the game copies
  into RAM (Kirby's Adventure keeps a routine at `0x0029`). Skip sprite tables
  and the stack, and check that another game's RAM doesn't match.
- **CRC** for the CRC check: if you can read the ROM file, compute its CRC32
  after any header (16 bytes for `.nes`) and compare it with the No-Intro
  entry in libretro-database, which settles the exact revision.

Rules:

- Confirm each address with two different changes, including one where a
  coincidence could fool you, such as the same X on the title screen.
- Read narrow ranges. Counting bytes in a large dump goes wrong.
- Use screenshots only to check what the memory says. Each one saves a file.
- Save only when nothing is about to hit the player. A save taken mid-collision
  reloads straight into a death.

## Learn controls and timing

- Press each RetroPad button with `PRESS` and watch what changes.
- Measure in frames, and note the frame rate (60 NTSC, 50 PAL): a short versus
  full jump, walk and run speed in pixels per frame, how far momentum carries
  after release, and how long input is ignored after boot or a transition.
- For each common hazard, find a pattern that works and record the numbers,
  such as the gap to an enemy at which a jump clears it.

## Write the skill

Follow the [template](../../template/SKILL.md) and
[CONTRIBUTING.md](../../CONTRIBUTING.md): frontmatter with `name`, `description`, and `metadata` (`game`,
`system`, `cores`, optional `crc32`), then the sections Confirm the game,
Setup, Controls, Memory, Playing, Pitfalls and Ask first.

- Name the directory with the slug of the game's No-Intro name. Write it to
  `skills/<slug>/` when working in the repository, otherwise to
  `~/.claude/skills/<slug>/`.
- Include only what you verified. Tell the user what you didn't test, rather
  than guessing in the skill.
- In the repository, run `python3 scripts/validate.py`.
- Tell the user how many screenshots you took, and which AI Agent save
  slots hold your saves.
