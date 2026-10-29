# arm64 known issues

Problems found while testing NonSteamLaunchers on ArmadaOS (Fedora bootc, FEX, GE-Proton11-11-aarch64) that
NSL can't fully fix itself. Each has the evidence and what NSL does about it, so they can be reported upstream.

## ArmadaOS

### Per-game settings never apply to non-Steam shortcuts

`/usr/libexec/armada/armada-game-launch` picks the game id from `STEAM_COMPAT_APP_ID`, `SteamAppId` or
`SteamGameId`, taking the first all-digit value. For non-Steam shortcuts Steam sets `SteamAppId=0`, so the
id is always `0` (its generated FEX config is `~/.cache/armada-fex/0.<pid>.json`) and per-game entries in
`/etc/armada/game-tweaks.json` (FEX profile, cores, etc.) never match.

Suggested fix: skip `0` and prefer `SteamGameId` (the 64-bit shortcut id) or `STEAM_COMPAT_APP_ID`.

NSL workaround: Amazon Games needs the "compatible" FEX profile, so its launch options run
`armada-game-launch /usr/bin/env FEX_APP_CONFIG=<config> %command%` (set after the wrapper, which overwrites
`FEX_APP_CONFIG`).

### Steam UI deadlocks when a native multi-process app exits

When a native Linux app with many processes exits (Heroic, Silksong once), Steam can log
`IPC error: LockMgrMutex failed to acquire SysMgrMutex` and its UI (and CEF DevTools) stop responding until
Steam is killed. Steam preloads `gameoverlayrenderer.so` into every process of a launch (`AllowOverlay=0`
doesn't stop the preload); Electron SIGKILLs its helper processes on exit, so one dying inside the overlay's
IPC lock leaves it held. Seen 5 times in 441 app exits; never with Wine launchers.

NSL workaround: Heroic's and Amazon's shortcuts clear `LD_PRELOAD`, keeping the overlay out of them.

## FEX

### 32-bit apps that run code from read-only pages crash (Big Fish Games Manager)

`bfgclient.exe` (32-bit, `NX_COMPAT`) writes window-procedure thunks into memory, sets the page to
`PAGE_READONLY`, then executes it. Windows (ATL thunk emulation) and Wine on x86 run it; under FEX's WoW64 it
raises `EXCEPTION_ACCESS_VIOLATION` at the page start inside a window callback and the client exits.
`SMCChecks=2` avoids the fault but leaves the client spinning at 100% CPU with a black window. FEX only
treats readable pages as executable after `ProcessExecuteFlags` disables DEP: Wine does that for this app
because its bundled `zlib1.dll` and `unicows.dll` lack `NX_COMPAT`, and FEX then mishandles the DEP-off state.

NSL workaround: the installer sets the `NX_COMPAT` flag on those two DLLs, so DEP stays on and the client runs.

### Default profile deadlocks Amazon Games' .NET service

`Amazon Games Services.exe` (32-bit .NET) hangs forever at "Constructing container, resolving dependencies"
under ArmadaOS's default FEX profile (Multiblock on, relaxed vector TSO); every thread waits on one futex in
the WoW64 layer. The "compatible" profile fixes it. NSL applies that profile to Amazon only (see above).

## Wine on ARM

### `ProcessorNameString` is missing

On arm64 Wine creates `HKLM\HARDWARE\DESCRIPTION\System\CentralProcessor\0` with `Identifier` and
`VendorIdentifier` but no `ProcessorNameString`. STOVE's setup and client throw a C++ exception without it.
The key is volatile, so it can't be set once in the prefix.

NSL workaround: STOVE starts through `C:\ProgramData\Smilegate\STOVE\nsl-stove.bat`, which sets the value
for the session and then starts `STOVE.exe`.

## .NET 10 under emulation

### Exceptions through reflection stubs FailFast (Plarium Play)

Plarium's .NET 10 backend throws through emitted reflection `InvokeStub_*` frames; under FEX the runtime
can't unwind them and calls FailFast, so the launcher shows "Oops! Something Went Wrong".

NSL workaround: the installer sets `Switch.System.Reflection.ForceInterpretedInvoke` in the backend's
`runtimeconfig.json`.

## Gamescope

### Owned and hidden-parent dialogs never show

Gamescope shows one window per app, so dialogs owned by a hidden window never appear in Game Mode: ARC's
sign-in and Gryphlink's "Launcher version update detected" prompt.

NSL workaround: ARC and Gryphlink run inside a Wine virtual desktop
(`explorer.exe /desktop=<name>,1920x1080 <exe>`), which is one plain window.

## Launchers

- **PlayStation Plus** shows a "may not function correctly in a virtual machine" warning that needs one OK.
- **Gryphlink** asks to update on first start; its buttons are custom-drawn, so they need a click, not Enter.
