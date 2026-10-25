---
name: system-game-title-region
description: Plays <Game Title> on the <System> through RetroArch's MCP server. Use when GET_STATUS reports <Game Title> or the user asks to play it.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", and a core that publishes a memory map.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__GET_MEMORY_MAP mcp__retroarch__READ_CORE_MEMORY mcp__retroarch__RUN_FRAMES mcp__retroarch__PRESS mcp__retroarch__INPUT mcp__retroarch__LIST_CORES mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST mcp__retroarch__WATCH mcp__retroarch__RUN_UNTIL mcp__retroarch__STEPS mcp__retroarch__GET_FRAME
metadata:
  game: "Game Title (Region)"
  system: "Manufacturer - System Name"
  cores: "first_libretro second_libretro"
  crc32: "00000000"
---

# <Game Title, without region or revision>

<One or two sentences: what the game is and what the player is trying to do.>

## Quick start

1. `GET_STATUS`, then read `<address>`: `<bytes>` is this game.
2. <The one `STEPS` call that goes from a paused load to play.>
3. `WATCH <the line under Memory>`, once.
4. <How each stretch is played: the `STEPS` shape and its death `stop`.>
5. A `checkpoint` step before a hard stretch; `STATE rollback` after a death.

## Confirm the game

Call `GET_STATUS`. Its reply should name `<system_id>` and
`<Game Title (Region)>`. If nothing is loaded, follow Setup first.

Then read `<address>`, `<n>` bytes. It is `<bytes>` <from when on>. <What the
bytes are, and why they hold in every mode.>

- Memory matches: go on. If the name differs, the ROM is probably renamed:
  run the CRC check if you can, and tell the user what you found.
- Memory doesn't match: another game, or a hack of this one. Stop and tell
  the user what `GET_STATUS` reported.
- The read fails: run the CRC check. If it matches, go on to Setup to fix the
  core. Ask the user only if you can verify neither the memory nor the CRC.

**CRC check**, when you can read files: find the loaded file's path in
`GET_PLAYLIST "<system playlist>.lpl"` by the name `GET_STATUS` reported; if
it isn't there, skip the check. For a `.zip#` path, read the file inside.
<If the format has a header, how many bytes to skip first.> The CRC32 should
be `metadata.crc32`. A mismatch means another dump, revision or hack: go on,
and tell the user that addresses may differ.

## Setup

Any core that publishes a memory map with <the RAM this skill reads> works.
<The cores from `metadata.cores`> do. Prefer them in that order.

- **Nothing loaded:** `LIST_CORES <content path>` lists the installed cores
  that can run the content. `LOAD_CONTENT` with the first of them that's in
  the list above, and `paused` on.
- **Check the memory:** `GET_MEMORY_MAP` must have regions covering <the RAM
  this skill reads>. A read runs on across regions, and says `truncated`
  where memory nothing maps begins. If the map is missing or short, tell the
  user and suggest one of the cores above.

<How to get from boot to gameplay: frames to wait, buttons to press, and the
memory value that confirms play has started.>

## Controls

| Action | RetroPad | Notes |
| ------ | -------- | ----- |
| Move   | `left`, `right` | |
| Jump   | `a` | Hold longer to jump higher. |
| Pause  | `start` | |

## Memory

Read these with `READ_CORE_MEMORY`. Addresses are system addresses, as listed by
`GET_MEMORY_MAP`.

| Address | Bytes | Meaning |
| ------- | ----- | ------- |
| `0x0000` | 1 | <What it holds, and how to decode it.> |

<Optional: structures that don't fit a table, such as a tile map, in a short
paragraph.>

## Playing

<What to `WATCH` once, so every step answers with it, and the `STEPS` lists
that play the common stretches, with a `stop` for a death. Give timings in
frames at the game's frame rate.>

## Pitfalls

- <Things that go wrong, such as input that a cutscene drops, or frames to
  wait after a screen transition.>

## Ask first

Save and load only the AI Agent save slots, 990-999, and never touch any
other slot.

Ask before calling `RESET`, `CLOSE_CONTENT`, or `WRITE_CORE_MEMORY`. These can
lose the user's progress.
