# AGENTS.md

This file provides guidance to LLMs when working with code in this repository.

## Project Overview

NonSteamLaunchers is a tool that installs various game launchers (Epic Games, EA App, GOG Galaxy, etc.) under a single Proton prefix on Steam Deck and Linux systems. It automatically adds these launchers to the Steam Library and can scan for installed games in real-time.

## Development Commands

### Python Environment Setup

```bash
# Create and activate virtual environment using UV
uv venv --python ">=3.11,<3.13"
source .venv/bin/activate

# Install dependencies
uv pip install -r pyproject.toml --all-extras
```

### Code Quality

```bash
# Format Python code
ruff format .

# Check Python linting
ruff check .

# Fix linting issues automatically
ruff check . --fix

# Run pre-commit hooks manually
pre-commit run --all-files
```

### Running the Project

```bash
# Main installer script
./NonSteamLaunchers.sh

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

## Important Notes

- The script modifies Steam configuration files - handle with care
- Game scanner runs as a systemd service
- Community notes feature uses `#nsl` hashtag
- MicroSD card support requires proper mount points
- Cloud saves via Ludusavi are backed up to `/home/deck/NSLGameSaves`
