# RetroArch Skills

[Agent Skills](https://agentskills.io) that teach an AI assistant how to play
specific games through [RetroArch](https://www.retroarch.com)'s MCP server.

Each skill covers one game. It tells the assistant how to recognize the game,
how to map the game's controls to the RetroPad, which memory addresses to read
for state such as lives or position, and how to play it well.

For a game without a skill, ask the assistant to create one. The
`create-game-skill` skill has it work these out by experiment and write a new
skill. See the [skills](skills) directory for added games.

## Requirements

- A RetroArch build with the MCP server (`HAVE_MCP`)
- An MCP client that supports skills, such as
  [Claude Code](https://claude.com/claude-code)
- Your own legally obtained game content

## Setup

### 1. Enable the MCP server in RetroArch

Open **Settings > Network** and turn on **MCP Server**, or set these keys in
`retroarch.cfg`:

```ini
mcp_server_enable = "true"
mcp_server_port = "55357"
mcp_server_token = "choose-a-secret"
```

### 2. Connect your MCP client

For Claude Code:

```sh
claude mcp add --transport http retroarch http://localhost:55357/mcp \
  --header "Authorization: Bearer choose-a-secret"
```

Name the server `retroarch`. The skills pre-approve tools such as
`mcp__retroarch__PRESS` by that name, so under another name every call
prompts for permission. Tools that can lose progress, such as `RESET` and the
save state tools, always prompt.

### 3. Install the skills

As a Claude Code plugin:

```text
/plugin marketplace add RobLoach/retroarch-skills
/plugin install retroarch-skills@retroarch-skills
```

Or with `skills`:

```
npx skills add robloach/retroarch-skills
```

Or GitHub CLI:

```
gh skill install robloach/retroarch-skills --scope user
```

Alternatively, manually copy individual skill directories from [`skills/`](skills/) into
`~/.claude/skills/`, or into the skills directory of another agent.

## Usage

Load a game in RetroArch, then ask the assistant to play it:

> Play the first level of Super Mario Bros.
>
> Get Kirby the Spark ability, then clear stage 1-1.
>
> How many lives and how much health does Kirby have?
>
> Help Mario jump over this ledge.
>
> Improve the Kirby skill, find the byte that says which stage we're currently in.
>
> Create a skill for the game that's loaded.

## Layout

```text
skills/
  create-game-skill/
    SKILL.md
  super-mario-bros-world/
    SKILL.md
```

Directory names are slugs of the game's
[No-Intro](https://no-intro.org) name, which is the name RetroArch's database
uses. The exact name and the system are stored in the skill's frontmatter,
next to the cores the skill works with, so a running game can be matched to
its skill. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the full conventions.

## Contributing

New game skills are welcome. Start from
[`template/SKILL.md`](template/SKILL.md) and read
[CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE). This repository does not include or link to game content.
