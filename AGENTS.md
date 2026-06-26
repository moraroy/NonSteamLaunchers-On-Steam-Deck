# AGENTS.md

This file provides guidance to LLMs when working with code in this repository.

## Project Overview

NonSteamLaunchers is a tool that installs various game launchers (Epic Games, EA App, GOG Galaxy, etc.) under a single Proton prefix on Steam Deck and Linux systems. It automatically adds these launchers to the Steam Library and can scan for installed games in real-time.

## Development Commands

### Python Environment Setup

```bash
# Create the environment and install dependencies (runtime + dev group)
uv sync
source .venv/bin/activate
```

This project is run as a collection of scripts, not an installable package, so
`pyproject.toml` sets `[tool.uv] package = false`. uv installs the declared
dependencies without attempting to build a wheel. (Without this, hatchling fails
with "Unable to determine which files to ship inside the wheel".)

### Code Quality

```bash
# Format Python code
ruff format .

# Check Python linting
ruff check .

# Fix linting issues automatically
ruff check . --fix

# Run pre-commit hooks manually
uvx pre-commit run --all-files
```

Use `uvx pre-commit` rather than `uv run pre-commit`: pre-commit manages its own
isolated hook environments and does not need this project installed, and `uvx`
avoids triggering a project build. The repo's PostToolUse hook in
`.claude/settings.json` runs `uvx pre-commit run --files` on edited files.

### Running the Project

> **Run the app with system Python, not the project venv.** The launcher-picker
> GUI imports PyGObject (`gi`), which is a system package and cannot be installed
> into a uv/virtualenv. If the `.venv` is active, `python3` resolves to the venv
> interpreter, `gi` import fails, and the script misreports it as
> "No launchers or websites selected. Exiting." Run `deactivate` first (or use a
> shell where the venv is not active). The venv is only for ruff/pytest/pre-commit.

```bash
# Main installer script (deactivate the venv first if it is active)
./NonSteamLaunchers.sh

# Passing a launcher name skips the GTK GUI entirely (no gi needed)
./NonSteamLaunchers.sh "GOG Galaxy"

# Game scanner service
python NSLGameScanner.py

# Install specific launcher via command line
/bin/bash -c 'curl -Ls https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/NonSteamLaunchers.sh | nohup /bin/bash -s -- "Epic Games"'
```

## Architecture

### Core Components

- **NonSteamLaunchers.sh**: Main Bash script that handles launcher installation, Steam integration, and UI
- **NSLGameScanner.py**: Python service that monitors installed launchers and automatically adds games to Steam library
- **config.py**: Configuration management for paths and settings
- **Modules/**: Vendored Python dependencies (steamgrid, requests, vdf, etc.)

### Key Paths

- Compatdata directory: `~/.local/share/Steam/steamapps/compatdata/`
- NonSteamLaunchers prefix: `~/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/`
- Logs: `/home/deck/Downloads/NonSteamLaunchers-install.log`
- Game saves backup: `/home/deck/NSLGameSaves`

### Integration Points

- **Steam**: Adds shortcuts via Steam's shortcuts.vdf file
- **Proton**: Uses UMU Launcher and GE-Proton for Windows compatibility
- **Decky Loader**: Plugin available for Steam Deck Game Mode
- **Ludusavi**: Pre-configured for game save backups

## Code Style

### Python

- Formatter: Ruff (Black-compatible, 130 char line length)
- Python version: 3.11-3.12
- Indentation: 4 spaces
- Follow PEP 8 with exceptions defined in ruff.toml

### Shell Scripts

- Indentation: Tabs
- Follow shellcheck rules (see .shellcheckrc)
- Use bash shebang: `#!/bin/bash`

### Pre-commit Hooks

Pre-commit is configured with:

- Ruff for Python formatting and linting
- File checks (YAML, JSON, large files, private keys)
- End-of-file fixing and line ending normalization

## Testing

Currently, there is no formal test suite. When implementing new features:

- Test installation of launchers manually
- Verify Steam library integration
- Check game scanner functionality
- Test on both Desktop and Game Mode

## Command Line Arguments

The main script supports:

- Launcher names: `"Epic Games"`, `"EA App"`, `"GOG Galaxy"`, etc.
- Uninstall: `"Uninstall Epic Games"`
- Utilities: `"Start Fresh"`, `"Update Proton-GE"`, `"Stop NSLGameScanner"`
- SD Card: `"Move to SD Card" "LauncherName"`

## Environment Variables

`NonSteamLaunchers.sh` reads several `NSL_*` variables to control otherwise
hardcoded or interactive behavior. All default to the safe/off value shown.

| Variable | Default | Effect |
|----------|---------|--------|
| `NSL_DEBUG` | `0` | `1` enables `set -x` execution tracing (off by default to avoid leaking values into the log). |
| `NSL_DRY_RUN` | `0` | `1` reports destructive actions (deletes, Start Fresh) without performing them. |
| `NSL_AUTO_INSTALL_DEPS` | `0` | `1` allows the script to install missing tools (zenity/curl/jq) via the system package manager. Otherwise it exits with instructions. |
| `NSL_AUTO_SCAN_ON_START` | `0` | `1` runs the game-scanner update + scan (and Steam restart) at startup. |
| `NSL_ALLOW_REMOTE_SCANNER_UPDATE` | `0` | `1` permits downloading scanner modules / `NSLGameScanner.py` from the remote repo. Default prefers vendored `Modules/`. |
| `NSL_CONFIRM_START_FRESH` | `0` | Must be `1` to run a non-interactive (CLI) "Start Fresh" wipe. |
| `NSL_UMU_SELF_UPDATE` | `0` | `1` runs `umu-run winetricks --self-update` after installing UMU. |
| `NSL_PROTON_DIR` | _(auto)_ | Override the GE-Proton directory instead of auto-detecting under `compatibilitytools.d`. |
| `NSL_REPO_OWNER` / `NSL_REPO_NAME` / `NSL_REPO_REF` | `dadtronics` / `NonSteamLaunchers-On-Steam-Deck` / `main` | Source repo/ref for remote raw + archive downloads. |
| `NSL_DRY_RUN_SD_PATH` | _(placeholder)_ | SD path used during a dry run when no card is detected. |
| `NSL_GOG_USE_WEB_INSTALLER` | `0` | `1` forces GOG Galaxy's online web installer. Default uses the more Proton-reliable full offline installer, falling back to the web installer only if the offline install fails. |
| `GOG_GALAXY_VERSION` | `2.0.74.352` | Version used to build the GOG Galaxy offline installer URL. Bump when GOG ships a newer build (the installed client also self-updates). |

`NSLPluginInstaller.sh` additionally reads `DECKY_REPO_OWNER` / `DECKY_REPO_NAME`
/ `DECKY_REPO_REF` (default `moraroy` / `NonSteamLaunchersDecky` / `main`) and
`NSL_DEBUG`.

Downloads go through HTTPS-only helpers (`nsl_download` / `download_https`) and
destructive removals are restricted to an allowlist of expected NSL paths via
`nsl_safe_rm` / `delete_path`.

## Important Notes

- The script modifies Steam configuration files - handle with care
- Game scanner runs as a systemd service
- Community notes feature uses `#nsl` hashtag
- MicroSD card support requires proper mount points
- Cloud saves via Ludusavi are backed up to `/home/deck/NSLGameSaves`
