---
name: use-retroarch
description: Drives RetroArch itself through its MCP server - finds and loads games from playlists, turns options on and off, and reads and moves through its menu to change settings. Use when the user asks RetroArch to do something other than play a game, such as load a game, change a setting or find something in the menu.
license: MIT
compatibility: Requires RetroArch with the MCP server enabled, added to the client as "retroarch", with the MENU, OPTION and CORE_OPTION tools.
allowed-tools: mcp__retroarch__GET_STATUS mcp__retroarch__LIST_PLAYLISTS mcp__retroarch__GET_PLAYLIST mcp__retroarch__LIST_CORES mcp__retroarch__OPTION mcp__retroarch__CORE_OPTION mcp__retroarch__GET_LOG mcp__retroarch__GET_FRAME
---

# Use RetroArch

RetroArch as an application: its games, its options and its menu. To play
a game once it runs, use that game's skill, or `create-game-skill`.

## Quick start

1. `GET_STATUS`: `PLAYING`, `PAUSED` or `CONTENTLESS`, with the system and
   the content's file name.
2. A game: `LIST_PLAYLISTS`, `GET_PLAYLIST`, then `LOAD_CONTENT`.
3. A setting: `OPTION show` first; the menu only for what it doesn't list.
4. The menu: `MENU open`, pick entries by their label, `MENU close`.

## Find and load a game

- `LIST_PLAYLISTS` names the playlists, `.lpl` and all.
- `GET_PLAYLIST` with that name lists its entries, 200 at a time: index,
  label, content path and core path. `first` asks for the next 200, from
  the `next` the reply gives.
- `LOAD_CONTENT` with the entry's content and core paths. A core of
  `DETECT` picks one that supports the content; `LIST_CORES` with the
  content path lists the installed ones that can. `paused` on stops the game
  before it runs on, ready for a game skill.

## Options before the menu

`OPTION show` lists about thirty options and their values in one call,
where the menu takes four or five calls per setting: `pause`,
`fast_forward`, `slow_motion`, `mute`, `fps` (the frame rate on screen),
`statistics`, `fullscreen`, `shader`, `rewind`, `runahead`, `turbo_fire`,
`game_focus`, `recording`, the state and replay slots, the frame count, and
the configured directories. `OPTION set <option> on|off` changes one;
asking for the state it already has changes nothing. Some only report, and
say so.

`CORE_OPTION show` lists the running core's own options - key, value and
description; with a key, the values it takes. `CORE_OPTION set <key>
<value>` picks one.

## The menu

Every `MENU` call answers with what the menu shows once the action has
run:

- `title`, and `path` - the lists above it, such as
  `Main Menu > Settings > Drivers`. The menu opens where it was left, so
  read the path after `open`.
- `rows`: each entry's index, label and value. `...` opens a list;
  `checked` marks the choice in use in a list of choices, such as the
  driver.
- `selected` and `count`, and `more` with `next` when the list runs past
  50 entries: `MENU show from <next>` lists the rest.

Moving:

- `MENU a <index>` opens or confirms the entry at that index; find the
  index by label in the rows, never by memory. `MENU select <index>` only
  moves there. `left` and `right` with an index change a setting's value.
- `MENU b` goes back up the path.
- The top level differs by menu driver. RGUI has Settings in Main Menu. XMB
  keeps it in tabs: `left` and `right` at the top switch tabs. Ozone keeps
  them in a sidebar: `left` moves to the tabs, `up` and `down` pick one,
  and `right` returns to the list; there `a` only returns too. About four
  calls reach the Settings tab on Ozone.
- `message` is something the menu shows over the list, such as
  "Press again to close content": `MENU a` confirms it, `MENU b` dismisses
  it.
- `keyboard` means the menu asks for text, such as a username:
  `MENU type <text>` enters one line and confirms it; `MENU b` cancels.
- `MENU close` closes it. With no content running, the menu cannot close,
  and says so.

## Pitfalls

- Settings changed through the menu are written to the configuration when
  RetroArch saves it, usually on exit. Tell the user what you changed.
- Username is the netplay nickname too: changing one changes the other.
- `MENU` acts on the menu's next frame. A second `MENU` sent before the
  first answers replaces it.

## Ask first

`MENU` always asks, because its entries include Quit, Close Content, Reset
and Delete. Ask before `LOAD_CONTENT` while a game runs - it replaces the
game, and unsaved progress with it - and before confirming any of those
entries.
