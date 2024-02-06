#!/usr/bin/env python3
import os, re, vdf
import json
import shutil
import binascii
import ctypes
import zipfile
import time
import sys
import subprocess
import sqlite3
from urllib.request import urlopen
from urllib.request import urlretrieve
import xml.etree.ElementTree as ET

# Path to the env_vars file
env_vars_path = f"{os.environ['HOME']}/.config/systemd/user/env_vars"

# Check if the env_vars file exists
if not os.path.exists(env_vars_path):
    print(f"Error: {env_vars_path} does not exist.")
    sys.exit(1)

# Read variables from the file
with open(env_vars_path, 'r') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith('export '):
        line = line[7:]  # Remove 'export '
    name, value = line.strip().split('=')
    os.environ[name] = value

# Variables from NonSteamLaunchers.sh
steamid3 = os.environ['steamid3']
logged_in_home = os.environ['logged_in_home']
compat_tool_name = os.environ['compat_tool_name']
epic_games_launcher = os.environ.get('epic_games_launcher', '')
ubisoft_connect_launcher = os.environ.get('ubisoft_connect_launcher', '')
ea_app_launcher = os.environ.get('ea_app_launcher', '')
gog_galaxy_launcher = os.environ.get('gog_galaxy_launcher', '')
bnet_launcher = os.environ.get('bnet_launcher', '')
amazon_launcher = os.environ.get('amazon_launcher', '')

# Define the parent folder
parent_folder = f"{logged_in_home}/.config/systemd/user/Modules"

# Now that the requests module has been downloaded, you can import it
sys.path.insert(0, parent_folder)
import requests
from steamgrid import SteamGridDB
print(sys.path)


#Set Up nslgamescanner.service
# Define the paths
service_path = f"{logged_in_home}/.config/systemd/user/nslgamescanner.service"

# Define the service file content
service_content = f"""
[Unit]
Description=NSL Game Scanner

[Service]
ExecStart=/usr/bin/python3 '{logged_in_home}/.config/systemd/user/NSLGameScanner.py'
Restart=always
RestartSec=10
StartLimitBurst=40
StartLimitInterval=240

[Install]
WantedBy=default.target
"""

# Check if the service file already exists
if not os.path.exists(service_path):
    # Create the service file
    with open(service_path, 'w') as f:
        f.write(service_content)

    print("Service file created.")


# Check if the service is already running
result = subprocess.run(['systemctl', '--user', 'is-active', 'nslgamescanner.service'], stdout=subprocess.PIPE)
if result.stdout.decode('utf-8').strip() != 'active':
    # Reload the systemd manager configuration
    subprocess.run(['systemctl', '--user', 'daemon-reload'])

    # Enable the service to start on boot
    subprocess.run(['systemctl', '--user', 'enable', 'nslgamescanner.service'])

    # Start the service immediately
    subprocess.run(['systemctl', '--user', 'start', 'nslgamescanner.service'])

    print("Service started.")
else:
    print("Service is already running.")





#Code
def get_steam_shortcut_id(exe_path, display_name):
    unique_id = "".join([exe_path, display_name])
    id_int = binascii.crc32(str.encode(unique_id)) | 0x80000000
    signed = ctypes.c_int(id_int)
    # print(f"Signed ID: {signed.value}")
    return signed.value
    
def get_unsigned_shortcut_id(signed_shortcut_id):
    unsigned = ctypes.c_uint(signed_shortcut_id)
    # print(f"Unsigned ID: {unsigned.value}")
    return unsigned.value

# Initialize an empty dictionary to serve as the cache
api_cache = {}

#API KEYS FOR NONSTEAMLAUNCHER USE ONLY
sgdb = SteamGridDB('412210605b01f8777debeaec5e58e119')
api_key = '412210605b01f8777debeaec5e58e119'

#GLOBAL VARS
created_shortcuts = []
new_shortcuts_added = False
shortcuts_updated = False
shortcut_id = None  # Initialize shortcut_id

# Load the existing shortcuts
with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'rb') as file:
    shortcuts = vdf.binary_loads(file.read())
# Open the config.vdf file
with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
    config_data = vdf.load(file)

def get_sgdb_art(game_id, app_id):
	for art_type in ["icons", "logos", "heroes", "grids"]:
		print(f"Downloading {art_type} artwork...")
		download_artwork(game_id, api_key, art_type, app_id)
	print("Downloading grids artwork of size 600x900...")
	download_artwork(game_id, api_key, "grids", app_id, "600x900")
	print("Downloading grids artwork of size 920x430...")
	download_artwork(game_id, api_key, "grids", app_id, "920x430")

def download_artwork(game_id, api_key, art_type, shortcut_id, dimensions=None):
    # Create a cache key based on the function's arguments
    cache_key = (game_id, art_type, dimensions)

    # Check if the artwork already exists
    if dimensions is not None:
        filename = get_file_name(art_type, shortcut_id, dimensions)
    else:
        filename = get_file_name(art_type, shortcut_id)
    file_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{filename}"
    
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    if os.path.exists(file_path):
        print(f"Artwork for {game_id} already exists. Skipping download.")
        return

    # If the result is in the cache, use it
    if cache_key in api_cache:
        data = api_cache[cache_key]
    else:
        # If the result is not in the cache, make the API call
        print(f"Game ID: {game_id}, API Key: {api_key}")
        url = f"https://www.steamgriddb.com/api/v2/{art_type}/game/{game_id}"
        if dimensions:
            url += f"?dimensions={dimensions}"
        headers = {'Authorization': f'Bearer {api_key}'}
        print(f"Sending request to: {url}")  # Added print statement
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Store the result in the cache
            api_cache[cache_key] = data

    # Continue with the rest of your function using `data`
    for artwork in data['data']:
        image_url = artwork['thumb']
        print(f"Downloading image from: {image_url}")  # Added print statement
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            if response.status_code == 200:
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                break
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            if art_type == 'icons':
                download_artwork(game_id, api_key, 'icons_ico', shortcut_id)

def get_game_id(game_name):
    print(f"Searching for game ID for: {game_name}")
    games = sgdb.search_game(game_name)
    for game in games:
        if game.name == game_name:  # Case-sensitive comparison
            print(f"Found game ID: {game.id}")
            return game.id
    # Fallback: return the ID of the first game in the search results
    if games:
        print(f"No exact match found. Using game ID of the first result: {games[0].name}: {games[0].id}")
        return games[0].id
    print("No game ID found")
    return "default_game_id"  # Return a default value when no games are found

def get_file_name(art_type, shortcut_id, dimensions=None):
    singular_art_type = art_type.rstrip('s')
    if art_type == 'icons':
        if os.path.exists(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{shortcut_id}-{singular_art_type}.png"):
            return f"{shortcut_id}-{singular_art_type}.png"
        else:
            return f"{shortcut_id}-{singular_art_type}.ico"
    elif art_type == 'grids':
        if dimensions == '600x900':
            return f"{shortcut_id}p.png"
        else:
            return f"{shortcut_id}.png"
    elif art_type == 'heroes':
        return f"{shortcut_id}_hero.png"
    elif art_type == 'logos':
        return f"{shortcut_id}_logo.png"
    else:
        return f"{shortcut_id}.png"

def is_match(name1, name2):
    if name1 and name2:
        return name1.lower() in name2.lower() or name2.lower() in name1.lower()
    else:
        return False

def add_compat_tool(app_id):
    if 'CompatToolMapping' not in config_data['InstallConfigStore']['Software']['Valve']['Steam']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}
        print(f"CompatToolMapping key not found in config.vdf, creating.")
    if str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] and config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] == f'{compat_tool_name}':
        return False
    elif str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] = f'{compat_tool_name}'
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['config'] = ''
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['priority'] = '250'
        print(f"Updated CompatToolMapping entry for appid: {app_id}")
        return True
    else:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)] = {'name': f'{compat_tool_name}', 'config': '', 'priority': '250'}
        print(f"Created new CompatToolMapping entry for appid: {app_id}")
        return True

def check_if_shortcut_exists(shortcut_id, display_name, exe_path, start_dir, launch_options):
    # Check if the game already exists in the shortcuts using the id
    if any(s.get('appid') == shortcut_id for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on shortcut ID for game {display_name}. Skipping.")
        return True
    # Check if the game already exists in the shortcuts using the fields (probably unnecessary)
    if any(s.get('appname') == display_name and s.get('exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on matching fields for game {display_name}. Skipping.")
        return True
#End of Code


#Finding the Launchers and applying artwork to already made shortcuts from NonSteamLaunchers.sh

# List of game launchers to look for
game_launchers = {
    'Epic Games',
    'Gog Galaxy',
    'Ubisoft Connect',
    'Battle.net',
    'EA App',
    'Amazon Games',
    'itch.io',
    'Legacy Games',
    'Humble Bundle',
    'Glyph',
    'IndieGala Client',
    'Rockstar Games Launcher',
    'Minecraft: Java Edition',
    'Playstation Plus',
    'DMM Games',
    'VK Play'
}

#Chrome Based "Launchers"
chrome_launchers = {
    'Hulu',
    'Twitch',
    'Amazon Luna',
    'Youtube',
    'Amazon Prime Video',
    'Disney+',
    'Netflix',
    'GeForce Now',
    'Xbox Game Pass',
    'movie-web'
}

# Mapping between shortcut names and SteamGridDB names
name_mapping = {
    'Epic Games': 'Epic Games Store (Program)',
    'Gog Galaxy': 'GOG Galaxy (Program)',
    'Ubisoft Connect': 'Ubisoft Connect (Program)',
    'Battle.net': 'Battle.net (Program)',
    'Legacy Games': 'Legacy Games (Program)',
    'Humble Bundle': 'Humble Bundle (Website)',
    'VK Play': 'VK Play (Website)',
    'Disney+': 'Disney+ (Website)'
    # Add more mappings as needed
}

# Iterate over the shortcuts
for shortcut in shortcuts['shortcuts'].values():
    # Check if the shortcut is a game launcher
    app_name = shortcut.get('appname')
    if app_name in game_launchers:
        print(f"Found game launcher: {app_name}")
        # Use the actual app ID instead of generating one
        app_id = shortcut.get('appid')
        display_name = shortcut.get('appname')
        exe_path = shortcut.get('exe')
        signed_shortcut_id = get_steam_shortcut_id(exe_path, display_name)
        unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
        print(f"App ID for {app_name}: {app_id}")
        # Check if the shortcut doesn't have artwork
        artwork_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{unsigned_shortcut_id}.png"
        if not os.path.exists(artwork_path):
            print(f"No artwork found for {app_name}, downloading...")
            # Get the game ID from SteamGridDB
            steamgriddb_name = name_mapping.get(app_name, app_name)
            game_id = get_game_id(steamgriddb_name)
            if game_id is not None:
                print(f"Got game ID from SteamGridDB: {game_id}")
                # Download and apply artwork
                get_sgdb_art(game_id, unsigned_shortcut_id)
                new_shortcuts_added = True
        # Only add compat tool if not a chrome launcher
        if app_name not in chrome_launchers:
            if add_compat_tool(unsigned_shortcut_id):
                shortcuts_updated = True



# End of finding the Launchers and applying artwork to already made shortcuts from NonSteamLaunchers.sh


# Print the existing shortcuts
print("Existing Shortcuts:")
for shortcut in shortcuts['shortcuts'].values():
	print(f"AppID for {shortcut.get('appname')}: {shortcut.get('appid')}")






# Epic Games Scanner
item_dir = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests/"
dat_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat"

if os.path.exists(dat_file_path) and os.path.exists(item_dir):
    with open(dat_file_path, 'r') as file:
        dat_data = json.load(file)

    #Epic Game Scanner
    for item_file in os.listdir(item_dir):
        if item_file.endswith('.item'):
            with open(os.path.join(item_dir, item_file), 'r') as file:
                item_data = json.load(file)

            # Initialize variables
            display_name = item_data['DisplayName']
            app_name = item_data['AppName']
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/\""
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}\" %command% -'com.epicgames.launcher://apps/{app_name}?action=launch&silent=true'"
            signed_shortcut_id = get_steam_shortcut_id(exe_path, display_name)
            unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
            # Check if the game already exists in the shortcuts
            if check_if_shortcut_exists(signed_shortcut_id, display_name, exe_path, start_dir, launch_options):
                if add_compat_tool(unsigned_shortcut_id):
                    shortcuts_updated = True
                continue


            # Check if the game is still installed
            for game in dat_data['InstallationList']:
                print(f"Checking game: {game['AppName']}")
                if game['AppName'] == item_data['AppName']:
                    print(f"Match found: {game['AppName']}")
                    game_id = get_game_id(display_name)
                    print(f"No existing shortcut found for game {display_name}. Creating new shortcut.")
                    created_shortcuts.append(display_name)
                    shortcuts['shortcuts'][str(signed_shortcut_id)] = {
                        'appid': str(signed_shortcut_id),
                        'appname': display_name,
                        'exe': exe_path,
                        'StartDir': start_dir,
                        'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
                        'LaunchOptions': launch_options,
                        'GameID': game_id if game_id is not None else "default_game_id"
                    }
                    new_shortcuts_added = True
                    if game_id is not None:
                        get_sgdb_art(game_id, unsigned_shortcut_id)
                    add_compat_tool(unsigned_shortcut_id)

else:
    print("Epic Games Launcher data not found. Skipping Epic Games Scanner.")
#End of the Epic Games Scanner




# Ubisoft Connect Scanner
def getUplayGameInfo(folderPath, filePath):
    # Get the game IDs from the folder
    listOfFiles = os.listdir(folderPath)
    uplay_ids = [re.findall(r'\d+', str(entry))[0] for entry in listOfFiles if re.findall(r'\d+', str(entry))]

    # Parse the registry file
    game_dict = {}
    with open(filePath, 'r') as file:
        uplay_id = None
        game_name = None
        uplay_install_found = False
        for line in file:
            if "Uplay Install" in line:
                uplay_id = re.findall(r'Uplay Install (\d+)', line)
                if uplay_id:
                    uplay_id = uplay_id[0]
                game_name = None  # Reset game_name
                uplay_install_found = True
            if "DisplayName" in line and uplay_install_found:
                game_name = re.findall(r'\"(.+?)\"', line.split("=")[1])
                if game_name:
                    game_name = game_name[0]
                uplay_install_found = False
            if uplay_id and game_name and uplay_id in uplay_ids:  # Add the game's info to the dictionary if its ID was found in the folder
                game_dict[game_name] = uplay_id
                uplay_id = None  # Reset uplay_id
                game_name = None  # Reset game_name

    return game_dict

# Define your paths
data_folder_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/data/"
registry_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/system.reg"

# Check if the paths exist
if not os.path.exists(data_folder_path) or not os.path.exists(registry_file_path):
    print("One or more paths do not exist.")
    print("Ubisoft Connect game data not found. Skipping Ubisoft Games Scanner.")
else:
    game_dict = getUplayGameInfo(data_folder_path, registry_file_path)

    for game, uplay_id in game_dict.items():
        if uplay_id:
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/\" %command% \"uplay://launch/{uplay_id}/0\""
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/\""
            signed_shortcut_id = get_steam_shortcut_id(exe_path, game)
            unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
            # Check if the game already exists in the shortcuts
            if check_if_shortcut_exists(signed_shortcut_id, game, exe_path, start_dir, launch_options):
                if add_compat_tool(unsigned_shortcut_id):
                    shortcuts_updated = True
                continue

            game_id = get_game_id(game)
            if game_id is not None:
                get_sgdb_art(game_id, unsigned_shortcut_id)
            new_shortcuts_added = True
            created_shortcuts.append(game)
            shortcuts['shortcuts'][str(len(shortcuts['shortcuts']))] = {
                'appid': str(signed_shortcut_id),
                'appname': game,
                'exe': exe_path,
                'StartDir': start_dir,
                'LaunchOptions': launch_options,
                'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}"
            }
            add_compat_tool(unsigned_shortcut_id)

# End of Ubisoft Game Scanner

# EA App Game Scanner

def get_ea_app_game_info(installed_games, game_directory_path):
    game_dict = {}
    for game in installed_games:
        xml_file = ET.parse(f"{game_directory_path}{game}/__Installer/installerdata.xml")
        xml_root = xml_file.getroot()
        ea_ids = None
        game_name = None
        for content_id in xml_root.iter('contentID'):
            if ea_ids is None:
                ea_ids = content_id.text
            else:
                ea_ids = ea_ids + ',' + content_id.text
        for game_title in xml_root.iter('gameTitle'):
            if game_name is None:
                game_name = game_title.text
                continue
        for game_title in xml_root.iter('title'):
            if game_name is None:
                game_name = game_title.text
                continue
        if game_name is None:
            game_name = game
        if ea_ids:  # Add the game's info to the dictionary if its ID was found in the folder
            game_dict[game_name] = ea_ids
    return game_dict

game_directory_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/EA Games/"

if not os.path.isdir(game_directory_path):
    print("EA App game data not found. Skipping EA App Scanner.")
else:
    installed_games = os.listdir(game_directory_path)  # Get a list of game folders
    game_dict = get_ea_app_game_info(installed_games, game_directory_path)

    for game, ea_ids in game_dict.items():
        launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/\" %command% \"origin2://game/launch?offerIds={ea_ids}\""
        exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EALaunchHelper.exe\""
        start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/\""
        signed_shortcut_id = get_steam_shortcut_id(exe_path, game)
        unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
        # Check if the game already exists in the shortcuts
        if check_if_shortcut_exists(signed_shortcut_id, game, exe_path, start_dir, launch_options):
            if add_compat_tool(unsigned_shortcut_id):
                shortcuts_updated = True
            continue

        game_id = get_game_id(game)
        if game_id is not None:
            get_sgdb_art(game_id, unsigned_shortcut_id)
        # Check if the game already exists in the shortcuts
        new_shortcuts_added = True
        created_shortcuts.append(game)
        shortcuts['shortcuts'][str(len(shortcuts['shortcuts']))] = {
            'appid': str(signed_shortcut_id),
            'appname': game,
            'exe': exe_path,
            'StartDir': start_dir,
            'LaunchOptions': launch_options,
            'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}"
        }
        add_compat_tool(unsigned_shortcut_id)

#End of EA App Scanner



# Gog Galaxy Scanner
def getGogGameInfo(filePath):
    # Check if the file contains any GOG entries
    with open(filePath, 'r') as file:
        if "GOG.com" not in file.read():
            print("No GOG entries found in the registry file. Skipping GOG Galaxy Games Scanner.")
            return {}

    # If GOG entries exist, parse the registry file
    game_dict = {}
    with open(filePath, 'r') as file:
        game_id = None
        game_name = None
        exe_path = None
        for line in file:
            split_line = line.split("=")
            if len(split_line) > 1:
                if "gameID" in line:
                    game_id = re.findall(r'\"(.+?)\"', split_line[1])
                    if game_id:
                        game_id = game_id[0]
                if "gameName" in line:
                    game_name = re.findall(r'\"(.+?)\"', split_line[1])
                    if game_name:
                        game_name = game_name[0]
                if "exe" in line and "GOG Galaxy" in line and not "unins000.exe" in line:
                    exe_path = re.findall(r'\"(.+?)\"', split_line[1])
                    if exe_path:
                        exe_path = exe_path[0].replace('\\\\', '\\')
            if game_id and game_name and exe_path:
                game_dict[game_name] = {'id': game_id, 'exe': exe_path}
                game_id = None
                game_name = None
                exe_path = None

    return game_dict

# Define your paths
gog_games_directory = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/Games"
registry_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/system.reg"

# Check if the paths exist
if not os.path.exists(gog_games_directory) or not os.path.exists(registry_file_path):
    print("One or more paths do not exist.")
    print("GOG Galaxy game data not found. Skipping GOG Galaxy Games Scanner.")
else:
    game_dict = getGogGameInfo(registry_file_path)

    for game, game_info in game_dict.items():
        if game_info['id']:
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/\" %command% /command=runGame /gameId={game_info['id']} /path=\"{game_info['exe']}\""
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/\""
            signed_shortcut_id = get_steam_shortcut_id(exe_path, game)
            unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
            # Check if the game already exists in the shortcuts
            if check_if_shortcut_exists(signed_shortcut_id, game, exe_path, start_dir, launch_options):
                if add_compat_tool(unsigned_shortcut_id):
                    shortcuts_updated = True
                continue

            game_id = get_game_id(game)
            if game_id is not None:
                get_sgdb_art(game_id, unsigned_shortcut_id)
            new_shortcuts_added = True
            created_shortcuts.append(game)
            shortcuts['shortcuts'][str(len(shortcuts['shortcuts']))] = {
                'appid': str(signed_shortcut_id),
                'appname': game,
                'exe': exe_path,
                'StartDir': start_dir,
                'LaunchOptions': launch_options,
                'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}"
            }
            add_compat_tool(unsigned_shortcut_id)

# End of Gog Galaxy Scanner






#Battle.net Scanner
# Define your mapping
flavor_mapping = {
    "Blizzard Arcade Collection": "RTRO",
    "Diablo": "D1",
    "Diablo II: Resurrected": "OSI",
    "Diablo III": "D3",
    "Diablo IV": "Fen",
    "Diablo Immortal (PC)": "ANBS",
    "Hearthstone": "WTCG",
    "Heroes of the Storm": "Hero",
    "Overwatch": "Pro",
    "Overwatch 2": "Pro",
    "StarCraft": "S1",
    "StarCraft 2": "S2",
    "Warcraft: Orcs & Humans": "W1",
    "Warcraft II: Battle.net Edition": "W2",
    "Warcraft III: Reforged": "W3",
    "World of Warcraft": "WoW",
    "World of Warcraft Classic": "WoWC",
    "Warcraft Arclight Rumble": "GRY",
    "Call of Duty: Black Ops - Cold War": "ZEUS",
    "Call of Duty: Black Ops 4": "VIPR",
    "Call of Duty: Modern Warfare": "ODIN",
    "Call of Duty": "AUKS",
    "Call of Duty: MW 2 Campaign Remastered": "LAZR",
    "Call of Duty: Vanguard": "FORE",
    "Call of Duty: Modern Warfare III": "SPOT",
    "Crash Bandicoot 4: It's About Time": "WLBY",
    # Add more games here...
}

def get_flavor_from_file(game_path):
    game_path = game_path.replace('\\', '/')
    flavor_file = os.path.join(game_path, '_retail_', '.flavor.info')
    if os.path.exists(flavor_file):
        with open(flavor_file, 'r') as file:
            for line in file:
                if 'STRING' in line:
                    return line.split(':')[-1].strip().capitalize()
    else:
        print(f"Flavor file not found: {flavor_file}")
        # Use the mapping as a fallback
        game_name = os.path.basename(game_path)
        print(f"Game name from file path: {game_name}")
        return flavor_mapping.get(game_name, 'unknown')

def getBnetGameInfo(filePath):
    # Check if the file contains any Battle.net entries
    with open(filePath, 'r') as file:
        if "Battle.net" not in file.read():
            print("No Battle.net entries found in the registry file. Skipping Battle.net Games Scanner.")
            return None

    # If Battle.net entries exist, parse the registry file
    game_dict = {}
    with open(filePath, 'r') as file:
        game_name = None
        exe_path = None
        publisher = None
        contact = None
        for line in file:
            split_line = line.split("=")
            if len(split_line) > 1:
                if "Publisher" in line:
                    publisher = re.findall(r'\"(.+?)\"', split_line[1])
                    if publisher:
                        publisher = publisher[0]
                        # Skip if the publisher is not Blizzard Entertainment
                        if publisher != "Blizzard Entertainment":
                            game_name = None
                            exe_path = None
                            publisher = None
                            continue
                if "Contact" in line:
                    contact = re.findall(r'\"(.+?)\"', split_line[1])
                    if contact:
                        contact = contact[0]
                if "DisplayName" in line:
                    game_name = re.findall(r'\"(.+?)\"', split_line[1])
                    if game_name:
                        game_name = game_name[0]
                if "InstallLocation" in line:
                    exe_path = re.findall(r'\"(.+?)\"', split_line[1])
                    if exe_path:
                        exe_path = exe_path[0].replace('\\\\', '\\')
                        # Skip if the install location is for the Battle.net launcher
                        if "Battle.net" in exe_path:
                            game_name = None
                            exe_path = None
                            publisher = None
                            continue
            if game_name and exe_path and publisher == "Blizzard Entertainment" and contact == "Blizzard Support":
                game_dict[game_name] = {'exe': exe_path}
                print(f"Game added to dictionary: {game_name}")
                game_name = None
                exe_path = None
                publisher = None
                contact = None

    # If no games were found, return None
    if not game_dict:
        print("No Battle.net games found. Skipping Battle.net Games Scanner.")
        return None

    return game_dict

# Define your paths
registry_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/system.reg"

game_dict = {}

# Check if the paths exist
if not os.path.exists(registry_file_path):
    print("One or more paths do not exist.")
    print("Battle.net game data not found. Skipping Battle.net Games Scanner.")
else:
    game_dict = getBnetGameInfo(registry_file_path)
    if game_dict is None:
        # Skip the rest of the Battle.net scanner
        pass
    else:
        # Extract the flavor for each game and create the launch options
        for game, game_info in game_dict.items():
            game_info['flavor'] = get_flavor_from_file(game_info['exe'])
            print(f"Flavor inferred: {game_info['flavor']}")

            # Check if the game name is "Overwatch" and update it to "Overwatch 2"
            if game == "Overwatch":
                game = "Overwatch 2"

            if game_info['flavor']:
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/\" %command% \"battlenet://{game_info['flavor']}\""
                exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net.exe\" --exec=\"launch {game_info['flavor']}\""
                start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/\""
                signed_shortcut_id = get_steam_shortcut_id(exe_path, game)
                unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
                # Check if the game already exists in the shortcuts
                if check_if_shortcut_exists(signed_shortcut_id, game, exe_path, start_dir, launch_options):
                    if add_compat_tool(unsigned_shortcut_id):
                        shortcuts_updated = True
                    continue

                game_id = get_game_id(game)
                if game_id is not None:
                    get_sgdb_art(game_id, unsigned_shortcut_id)
                new_shortcuts_added = True
                created_shortcuts.append(game)
                shortcuts['shortcuts'][str(len(shortcuts['shortcuts']))] = {
                    'appid': str(signed_shortcut_id),
                    'appname': game,
                    'exe': exe_path,
                    'StartDir': start_dir,
                    'LaunchOptions': launch_options,
                    'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}"
                }
                add_compat_tool(unsigned_shortcut_id)

# End of Battle.net Scanner




# Amazon Games Scanner
def get_sqlite_path():
    # Specify the full path to the SQLite file
    path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/Data/Games/Sql/GameInstallInfo.sqlite"
    if os.path.exists(path):
        return path
    else:
        print(f"Amazon GameInstallInfo.sqlite not found at {path}")
        return None

def get_launcher_path():
    # Specify the full path to the Amazon Games launcher executable
    path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
    if os.path.exists(path):
        return path
    else:
        print(f"Could not find Amazon Games.exe at {path}")
        return None

def get_amazon_games():
    sqllite_path = get_sqlite_path()
    launcher_path = get_launcher_path()
    if sqllite_path is None or launcher_path is None:
        print("Skipping Amazon Games Scanner due to missing paths.")
        return []
    result = []
    connection = sqlite3.connect(sqllite_path)
    cursor = connection.cursor()
    cursor.execute("SELECT Id, ProductTitle FROM DbSet WHERE Installed = 1")
    for row in cursor.fetchall():
        id, title = row
        result.append({"id": id, "title": title, "launcher_path": launcher_path})
    return result

amazon_games = get_amazon_games()
if amazon_games:
    for game in amazon_games:

        # Initialize variables
        display_name = game['title']
        exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe\""
        start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/\""
        launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}\" %command% -'amazon-games://play/{game['id']}'"
        signed_shortcut_id = get_steam_shortcut_id(exe_path, display_name)
        unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)

        # Check if the game already exists in the shortcuts
        if check_if_shortcut_exists(signed_shortcut_id, display_name, exe_path, start_dir, launch_options):
            if add_compat_tool(unsigned_shortcut_id):
                shortcuts_updated = True
            continue

        print(f"No existing shortcut found for game {display_name}. Creating new shortcut.")
        created_shortcuts.append(display_name)
        shortcuts['shortcuts'][str(signed_shortcut_id)] = {
            'appid': str(signed_shortcut_id),
            'appname': display_name,
            'exe': exe_path,
            'StartDir': start_dir,
            'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
            'LaunchOptions': launch_options,
            'GameID': get_game_id(display_name) if get_game_id(display_name) is not None else "default_game_id"
        }
        new_shortcuts_added = True
        if get_game_id(display_name) is not None:
            get_sgdb_art(get_game_id(display_name), unsigned_shortcut_id)
            add_compat_tool(unsigned_shortcut_id)


#End of Amazon Games Scanner




#Push down when more scanners are added
# Only write back to the shortcuts.vdf and config.vdf files if new shortcuts were added or compattools changed
if new_shortcuts_added or shortcuts_updated:
    print(f"Saving new config and shortcuts files")
    conf = vdf.dumps(config_data, pretty=True)
    with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
   	    file.write(conf)
    with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
        file.write(vdf.binary_dumps(shortcuts))
    # Print the created shortcuts
    if created_shortcuts:
        print("Created Shortcuts:")
        for name in created_shortcuts:
            print(name)

print("All finished!")
