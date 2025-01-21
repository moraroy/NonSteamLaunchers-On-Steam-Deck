#!/usr/bin/env python3

from decouple import config
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
    'Amazon Games': 'AmazonGamesLauncher',
    'Battle.net': 'Battle.netLauncher',
    'DMM Games': 'DMMGameLauncher',
    'EA App': 'TheEAappLauncher',
    'Epic Games': 'EpicGamesLauncher',
    'Gog Galaxy': 'GogGalaxyLauncher',
    'Humble Bundle': 'HumbleGamesLauncher',
    'IndieGala Client': 'IndieGalaLauncher',
    'itch.io': 'itchioLauncher',
    'Legacy Games': 'LegacyGamesLauncher',
    'Minecraft: Java Edition': 'MinecraftLauncher',
    'Origin': 'OriginLauncher',
    'Playstation Plus': 'PlaystationPlusLauncher',
    'Rockstar Games Launcher': 'RockstarGamesLauncher',
    'Ubisoft Connect': 'UplayLauncher',
    'VK Play': 'VKPlayLauncher',
}

# Variables from NonSteamLaunchers.sh
steamid3 = config('steamid3', default='')
logged_in_home = config('logged_in_home')
compat_tool_name = config('compat_tool_name')
controller_config_path = config('controller_config_path')
python_version = config('python_version')
#Scanner Variables
epic_games_launcher = config('epic_games_launcher')
ubisoft_connect_launcher = config('ubisoft_connect_launcher')
ea_app_launcher = config('ea_app_launcher')
gog_galaxy_launcher = config('gog_galaxy_launcher')
bnet_launcher = config('bnet_launcher')
amazon_launcher = config('amazon_launcher')

# Variables of the Launchers
# Define the path of the Launchers
epicshortcutdirectory = config('epicshortcutdirectory')
gogshortcutdirectory = config('gogshortcutdirectory')
uplayshortcutdirectory = config('uplayshortcutdirectory')
battlenetshortcutdirectory = config('battlenetshortcutdirectory')
eaappshortcutdirectory = config('eaappshortcutdirectory')
amazonshortcutdirectory = config('amazonshortcutdirectory')
itchioshortcutdirectory = config('itchioshortcutdirectory')
legacyshortcutdirectory = config('legacyshortcutdirectory')
humbleshortcutdirectory = config('humbleshortcutdirectory')
indieshortcutdirectory = config('indieshortcutdirectory')
rockstarshortcutdirectory = config('rockstarshortcutdirectory')
glyphshortcutdirectory = config('glyphshortcutdirectory')
minecraftshortcutdirectory = config('minecraftshortcutdirectory')
psplusshortcutdirectory = config('psplusshortcutdirectory')
vkplayhortcutdirectory = config('vkplayhortcutdirectory')

# Streaming
chromedirectory = config('chromedirectory')
websites_str = config('custom_websites_str')
custom_websites = websites_str.split(', ') if websites_str else []

# Define your mapping
flavor_mapping = {
    "Blizzard Arcade Collection": "RTRO",
    "Call of Duty: Black Ops - Cold War": "ZEUS",
    "Call of Duty: Black Ops 4": "VIPR",
    "Call of Duty: Modern Warfare III": "SPOT",
    "Call of Duty: Modern Warfare": "ODIN",
    "Call of Duty: MW 2 Campaign Remastered": "LAZR",
    "Call of Duty: Vanguard": "FORE",
    "Call of Duty": "AUKS",
    "Crash Bandicoot 4: It's About Time": "WLBY",
    "Diablo II: Resurrected": "OSI",
    "Diablo III": "D3",
    "Diablo Immortal (PC)": "ANBS",
    "Diablo IV": "Fen",
    "Diablo": "D1",
    "Hearthstone": "WTCG",
    "Heroes of the Storm": "Hero",
    "Overwatch 2": "Pro",
    "Overwatch": "Pro",
    "StarCraft 2": "S2",
    "StarCraft": "S1",
    "Warcraft Arclight Rumble": "GRY",
    "Warcraft II: Battle.net Edition": "W2",
    "Warcraft II: Remastered": "W2R",
    "Warcraft III: Reforged": "W3",
    "Warcraft: Orcs & Humans": "W1",
    "Warcraft I: Remastered": "W1R",
    "World of Warcraft Classic": "WoWC",
    "World of Warcraft": "WoW",
}
