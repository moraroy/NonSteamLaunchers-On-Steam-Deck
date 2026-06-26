# Changelog

## [Unreleased]

### Features

* parameterize the source repo via `NSL_REPO_*` / `DECKY_REPO_*` env vars instead of hardcoding `moraroy`
* route all downloads through HTTPS-only helpers (`nsl_download` / `download_https`) with optional SHA-256 verification
* restrict destructive deletes to an allowlist of expected NSL paths (`nsl_safe_rm` / `delete_path`)
* add `NSL_DRY_RUN` to preview destructive actions (deletes, Start Fresh) without performing them
* gate execution tracing behind `NSL_DEBUG` so `set -x` no longer leaks values into the log by default
* make missing-dependency installation opt-in via `NSL_AUTO_INSTALL_DEPS`
* prefer vendored `Modules/` for the scanner, with remote download gated behind `NSL_ALLOW_REMOTE_SCANNER_UPDATE`
* make the startup game scan opt-in via `NSL_AUTO_SCAN_ON_START`
* require `NSL_CONFIRM_START_FRESH=1` for non-interactive "Start Fresh" wipes
* rework GOG Galaxy installer detection and install/handoff flow
* replace the password-piped-to-sudo flow in the Decky plugin installer with standard `sudo` credential handling
* run pre-commit on edited files via a PostToolUse hook in `.claude/settings.json`

### Bug Fixes

* fix `hoyoplayshortcutfirectory` env var typo that prevented the HoYoPlay shortcut directory from resolving
* quote the launcher choice and fix the `pkill wineserver` invocation in the generated `Exec=` line
* replace deprecated `datetime.utcnow()` with timezone-aware `datetime.now(UTC)`
* fix the project build by setting `[tool.uv] package = false` so `uv sync` / `uv run` no longer fail on the hatchling wheel step
* fall back gracefully when `xrandr` is unavailable instead of crashing the resolution probe
* quote `cd "$proton_dir"` paths and fail fast when Proton is missing

### Documentation

* document the `NSL_*` / `DECKY_*` env vars, `uvx pre-commit` usage, and the `uv` build fix in AGENTS.md

## [3.8.2](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/compare/v3.8.1...v3.8.2) (2024-08-06)


### Bug Fixes

* use correct home folder for user ([76466fd](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/commit/76466fdcc6f5473dc004aec365a4c58a9057eeee))

## [3.8.1](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/compare/v3.8.0...v3.8.1) (2024-02-29)


### Documentation

* conventional commits ([6b41710](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/commit/6b4171090dca8695856c1e98330973f729547081))
* formatting and pre-commit hooks ([b8f72f2](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/commit/b8f72f2dd1a542d08225e9ffbdebd1187262e468))
* update README.md ([61e19be](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/commit/61e19bee16871aeb46a9f8ee9734ca89f5b0a82c))
* update README.md ([3f6a7c9](https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/commit/3f6a7c952665d1ec4146bd454a8ef38c1c2fbe46))
