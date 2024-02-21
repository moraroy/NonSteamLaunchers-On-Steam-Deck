#!/usr/bin/env python3

from pathlib import Path

# paths
logged_in_home = str(Path.home())
steam_apps = f"{logged_in_home}/.local/share/Steam/steamapps"
compat_data = f"{steam_apps}/compatdata"
compat_data_path = f"{compat_data}/NonSteamLaunchers/pfx/drive_c"
steamuser_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local"

#  launchers
amazongames_path1 = f"{compat_data_path}/Program Files/Amazon Games/App/Amazon Games.exe"
amazongames_path2 = f"{steamuser_path}/Amazon Games/App/Amazon Games.exe"
battlenet_path1 = f"{compat_data_path}/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
battlenet_path2 = f"{steamuser_path}/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
dmm_path1 = f"{compat_data_path}/Program Files/DMMGamePlayer/DMMGamePlayer.exe"
dmm_path2 = f"{steamuser_path}/Program Files/DMMGamePlayer/DMMGamePlayer.exe"
eaapp_path1 = f"{compat_data_path}/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
eaapp_path2 = f"{steamuser_path}/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
epic_games_launcher_path1 = f"{compat_data_path}/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
epic_games_launcher_path2 = f"{steamuser_path}/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
glyph_path1 = f"{compat_data_path}/Program Files (x86)/Glyph/GlyphClient.exe"
glyph_path2 = f"{steamuser_path}/Program Files (x86)/Glyph/GlyphClient.exe"
gog_galaxy_path1 = f"{compat_data_path}/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
gog_galaxy_path2 = f"{steamuser_path}/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
humblegames_path1 = f"{compat_data_path}/Program Files/Humble App/Humble App.exe"
humblegames_path2 = f"{steamuser_path}/Program Files/Humble App/Humble App.exe"
indiegala_path1 = f"{compat_data_path}/Program Files/IGClient/IGClient.exe"
indiegala_path2 = f"{steamuser_path}/Program Files/IGClient/IGClient.exe"
itchio_path1 = f"{compat_data_path}/users/steamuser/AppData/Local/itch/app-25.6.2/itch.exe"
itchio_path2 = f"{steamuser_path}/itch/app-25.6.2/itch.exe"
legacygames_path1 = f"{compat_data_path}/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
legacygames_path2 = f"{steamuser_path}/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
minecraft_path1 = f"{compat_data_path}/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
minecraft_path2 = f"{steamuser_path}/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
origin_path1 = f"{compat_data_path}/Program Files (x86)/Origin/Origin.exe"
origin_path2 = f"{steamuser_path}/Program Files (x86)/Origin/Origin.exe"
psplus_path1 = f"{compat_data_path}/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
psplus_path2 = f"{steamuser_path}/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
rockstar_path1 = f"{compat_data_path}/Program Files/Rockstar Games/Launcher/Launcher.exe"
rockstar_path2 = f"{steamuser_path}/Program Files/Rockstar Games/Launcher/Launcher.exe"
uplay_path1 = f"{compat_data_path}/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
uplay_path2 = f"{steamuser_path}/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"

# streaming
chromedirectory = "/usr/bin/flatpak"

# Define a dictionary of original folder names
folder_names = {
    'Epic Games': 'EpicGamesLauncher',
    'Gog Galaxy': 'GogGalaxyLauncher',
    'Ubisoft Connect': 'UplayLauncher',
    'Origin': 'OriginLauncher',
    'Battle.net': 'Battle.netLauncher',
    'EA App': 'TheEAappLauncher',
    'Amazon Games': 'AmazonGamesLauncher',
    'itch.io': 'itchioLauncher',
    'Legacy Games': 'LegacyGamesLauncher',
    'Humble Bundle': 'HumbleGamesLauncher',
    'IndieGala Client': 'IndieGalaLauncher',
    'Rockstar Games Launcher': 'RockstarGamesLauncher',
    'Minecraft: Java Edition': 'MinecraftLauncher',
    'Playstation Plus': 'PlaystationPlusLauncher',
    'DMM Games': 'DMMGameLauncher',
}
