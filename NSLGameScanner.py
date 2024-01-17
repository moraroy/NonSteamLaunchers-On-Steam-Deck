#!/usr/bin/env python3
import os, re, vdf
import json
import shutil
import binascii
import zipfile
import time
import sys
import subprocess
from urllib.request import urlopen
from urllib.request import urlretrieve

# Read variables from a file
with open(f"{os.environ['HOME']}/.config/systemd/user/env_vars", 'r') as f:
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

# Create Folders
# Define the repository and the folders to clone
repo_url = 'https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/archive/refs/heads/main.zip'
folders_to_clone = ['requests', 'urllib3', 'steamgrid']

# Get the directory of the Python script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Define the parent folder
parent_folder = os.path.join(current_dir, 'Modules')
os.makedirs(parent_folder, exist_ok=True)

# Check if the folders already exist
folders_exist = all(os.path.exists(os.path.join(current_dir, parent_folder, folder)) for folder in folders_to_clone)

if not folders_exist:
    # Download the repository as a zip file
    zip_file_path = os.path.join(current_dir, 'repo.zip')
    urlretrieve(repo_url, zip_file_path)

    # Extract the zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(current_dir)

    # Move the folders to the current directory and delete the unnecessary files
    for folder in folders_to_clone:
        destination_path = os.path.join(current_dir, parent_folder, folder)
        source_path = os.path.join(current_dir, 'NonSteamLaunchers-On-Steam-Deck-main', 'Modules', folder)
        if not os.path.exists(destination_path):
            shutil.move(source_path, destination_path)

    # Delete the downloaded zip file and the extracted repository folder
    os.remove(zip_file_path)
    shutil.rmtree(os.path.join(current_dir, 'NonSteamLaunchers-On-Steam-Deck-main'))

# Now that the requests module has been downloaded, you can import it
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), parent_folder))
import requests
from steamgrid import SteamGridDB

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
    crc_input = bytes(display_name + exe_path, 'utf-8')
    crc = binascii.crc32(crc_input) | 0x80000000
    return crc

# Initialize an empty dictionary to serve as the cache
api_cache = {}

def download_artwork(game_id, api_key, art_type, shortcut_id, dimensions=None):
    # Create a cache key based on the function's arguments
    cache_key = (game_id, art_type, dimensions)

    # Check if the artwork already exists
    if dimensions is not None:
        filename = get_file_name(art_type, shortcut_id, dimensions)
    else:
        filename = get_file_name(art_type, shortcut_id)
    file_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{filename}"
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
            print(f"Error downloading image: {e}")  # Added print statement
            if art_type == 'icons':
                download_artwork(game_id, api_key, 'icons_ico', shortcut_id)
    if art_type in ['wide_grid', 'big_picture']:
        download_artwork(game_id, api_key, 'hero', shortcut_id)


def get_game_id(game_name):
    print(f"Searching for game ID for: {game_name}")
    games = sgdb.search_game(game_name)
    for game in games:
        if game.name == game_name:  # Case-sensitive comparison
            print(f"Found game ID: {game.id}")
            return game.id
        elif game.name.lower() in game_name.lower() or game_name.lower() in game.name.lower():  # Substring comparison
            print(f"Found game ID: {game.id} for game: {game.name}")
            return game.id
    # Fallback: return the ID of the first game in the search results
    if games:
        print(f"No exact match found. Using game ID of the first result: {games[0].id}")
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



#FOR NONSTEAMLAUNCHER USE ONLY
sgdb = SteamGridDB('239745e39536fdc12bfa84ce0056b036')
api_key = '239745e39536fdc12bfa84ce0056b036'
created_shortcuts = []



#Finding the Launchers and applying artwork to already made shortcuts from NonSteamLaunchers.sh
# Load the existing shortcuts
with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'rb') as file:
    shortcuts = vdf.binary_loads(file.read())

# Open the config.vdf file
with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
    config_data = vdf.load(file)

# List of game launchers to look for
game_launchers = {
    'Epic Games',
    'Gog Galaxy',
    'Ubisoft Connect',
    'Origin',
    'Battle.net',
    'EA App',
    'Amazon Games',
    'itch.io',
    'Legacy Games',
    'Humble Bundle',
    'IndieGala Client',
    'Rockstar Games Launcher',
    'Minecraft: Java Edition',
    'Playstation Plus',
    'DMM Games',
    'VK Play',
    'Hulu',
    'Twitch',
    'Amazon Luna',
    'Youtube',
    'Amazon Prime Video',
    'Disney+',
    'Netflix',
    'GeForce Now',
    'Xbox Game Pass'
}  # replace with your actual game launchers

# Mapping between shortcut names and SteamGridDB names
name_mapping = {
    'Epic Games': 'Epic Games Store (Program)',
    'Gog Galaxy': 'GOG Galaxy (Program)',
    'Ubisoft Connect': 'Ubisoft Connect (Program)',
    'Origin': 'Origin (Program)',
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
        print(f"App ID for {app_name}: {app_id}")
        # Check if the shortcut doesn't have artwork
        artwork_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{app_id}.png"
        if not os.path.exists(artwork_path):
            print(f"No artwork found for {app_name}, downloading...")
            # Get the game ID from SteamGridDB
            steamgriddb_name = name_mapping.get(app_name, app_name)
            game_id = get_game_id(steamgriddb_name)
            if game_id is not None:
                print(f"Got game ID from SteamGridDB: {game_id}")
                # Download and apply artwork
                for art_type in ["icons", "logos", "heroes", "grids"]:
                    print(f"Downloading {art_type} artwork...")
                    download_artwork(game_id, api_key, art_type, app_id)
                print("Downloading grids artwork of size 600x900...")
                download_artwork(game_id, api_key, "grids", app_id, "600x900")
                print("Downloading grids artwork of size 920x430...")
                download_artwork(game_id, api_key, "grids", app_id, "920x430")

                if 'CompatToolMapping' not in config_data['InstallConfigStore']['Software']['Valve']['Steam']:
                    config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}
                if str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
                    config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] = f'{compat_tool_name}'
                    config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['config'] = ''
                    config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['priority'] = '250'
                else:
                    config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)] = {'name': '', 'config': '', 'priority': '250'}

# Save the updated shortcuts back to the file
with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
    file.write(vdf.binary_dumps(shortcuts))



#End of Finding the Launchers and applying artwork to already made shortcuts from NonSteamLaunchers.sh


# Epic Games Scanner
item_dir = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests/"
dat_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/ProgramData/Epic/UnrealEngineLauncher/LauncherInstalled.dat"

if os.path.exists(dat_file_path):
    with open(dat_file_path, 'r') as file:
        dat_data = json.load(file)

    # Load the shortcuts and config_data objects
    with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'rb') as file:
        shortcuts = vdf.binary_loads(file.read())

    # Print the existing shortcuts
    print("Existing Shortcuts:")
    for shortcut in shortcuts['shortcuts'].values():
        print(shortcut.get('AppName'))

    # Open the config.vdf file
    with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
        config_data = vdf.load(file)

    # Keep track of whether any new shortcuts were added
    new_shortcuts_added = False

    shortcut_id = None  # Initialize shortcut_id

    #Epic Game Scanner
    for item_file in os.listdir(item_dir):
        if item_file.endswith('.item'):
            with open(os.path.join(item_dir, item_file), 'r') as file:
                item_data = json.load(file)

            # Check if the game is still installed
            for game in dat_data['InstallationList']:
                print(f"Checking game: {game['AppName']}")
                if game['AppName'] == item_data['AppName']:
                    print(f"Match found: {game['AppName']}")
                    display_name = item_data['DisplayName']
                    app_name = item_data['AppName']
                    launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}\" %command% -'com.epicgames.launcher://apps/{app_name}?action=launch&silent=true'"
                    exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe\""
                    start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/\""
                    shortcut_id = get_steam_shortcut_id(exe_path, display_name)
                    game_id = get_game_id(display_name)
                    # Check if the game already exists in the shortcuts
                    if str(shortcut_id) not in shortcuts['shortcuts']:
                        if not any(is_match(s.get('AppName'), display_name) and s.get('Exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
                            print(f"No existing shortcut found for game {display_name}. Creating new shortcut.")
                            created_shortcuts.append(display_name)
                            shortcuts['shortcuts'][str(shortcut_id)] = {
                                'appid': str(shortcut_id),
                                'AppName': display_name,
                                'Exe': exe_path,
                                'StartDir': f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/\"",
                                'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', shortcut_id)}",
                                'LaunchOptions': launch_options,
                                'GameID': game_id if game_id is not None else "default_game_id"
                            }
                            new_shortcuts_added = True

                    if game_id is not None:
                        print(f"Creating new shortcut for game {display_name} with appid {shortcut_id}")
                        for art_type in ["icons", "logos", "heroes", "grids"]:
                            download_artwork(game_id, api_key, art_type, shortcut_id)
                        download_artwork(game_id, api_key, "grids", shortcut_id, "600x900")
                        download_artwork(game_id, api_key, "grids", shortcut_id, "920x430")
            if str(shortcut_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['name'] = f'{compat_tool_name}'
                print(f"Setting compat tool for {shortcut_id} to {compat_tool_name}")
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['config'] = ''
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['priority'] = '250'
            else:
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)] = {'name': '', 'config': '', 'priority': '250'}
                print(f"Creating new entry for {shortcut_id} in CompatToolMapping")



    # Write the shortcuts and config_data objects back to their files
    if new_shortcuts_added:
        with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
            file.write(vdf.binary_dumps(shortcuts))
        with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
            vdf.dump(config_data, file)

else:
    print("Epic Games Launcher data not found. Skipping Epic Games Scanner.")
#End of the Epic Games Scanner



#Ubisoft Connect Scanner
def getUplayIDsFromGitHub():
    url = 'https://raw.githubusercontent.com/Haoose/UPLAY_GAME_ID/master/README.md'
    try:
        response = urlopen(url)
        data = response.read().decode()
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}

    game_dict = {}
    for line in data.split('\n'):
        match = re.match(r'\s*(\d+)\s*-\s*(.*)', line)
        if match:
            id, game = match.groups()
            game_dict[game.strip()] = id.strip()

    return game_dict

def getUplayIDsFromDataFolder(filePath):
    if not os.path.exists(filePath):
        print(f"Path {filePath} does not exist.")
        return {}

    listOfFiles = os.listdir(filePath)
    def findIDs(entry):
        result = re.findall(r'\d+', str(entry))
        try: return result[0]
        except: pass

    data_dict = {}
    for entry in listOfFiles:
        uPlayID = findIDs(entry)
        if uPlayID != None:
            gameName = entry.replace(uPlayID, '').strip()
            data_dict[gameName] = uPlayID

    return data_dict

def getInstalledGames(filePath):
    if not os.path.exists(filePath):
        print(f"Path {filePath} does not exist.")
        return []

    return os.listdir(filePath)

# Define your paths
data_folder_path = f"{logged_in_home}/Desktop/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/data/"
games_folder_path = f"{logged_in_home}/Desktop/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/games/"

# Check if the paths exist
if not os.path.exists(data_folder_path) or not os.path.exists(games_folder_path):
    print("One or more paths do not exist.")
else:
    game_dict = getUplayIDsFromGitHub()
    data_dict = getUplayIDsFromDataFolder(data_folder_path)
    installed_games = getInstalledGames(games_folder_path)

    # Load the shortcuts and config_data objects
    with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'rb') as file:
        shortcuts = vdf.binary_loads(file.read())

    # Open the config.vdf file
    with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
        config_data = vdf.load(file)

    # Keep track of whether any new shortcuts were added
    new_shortcuts_added = False

    for game in installed_games:
        game_id = game_dict.get(game) or data_dict.get(game)
        if game_id:
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/\" %command% \"uplay://launch/{game_id}/0\""
            exe_path = f"\"{logged_in_home}/.local/share/Steam/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/\""
            shortcut_id = get_steam_shortcut_id(exe_path, game)
            game_id = get_game_id(game)
            if game_id is not None:
                for art_type in ["icons", "logos", "heroes", "grids"]:
                    download_artwork(game_id, api_key, art_type, shortcut_id)
                download_artwork(game_id, api_key, "grids", shortcut_id, "600x900")
                download_artwork(game_id, api_key, "grids", shortcut_id, "920x430")
            # Check if the game already exists in the shortcuts
            if not any(s.get('AppName') == game and s.get('Exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
                new_shortcuts_added = True
                shortcuts['shortcuts'][str(len(shortcuts['shortcuts']))] = {
                    'appid': str(shortcut_id),
                    'AppName': game,
                    'Exe': exe_path,
                    'StartDir': start_dir,
                    'LaunchOptions': launch_options,
                    'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', shortcut_id)}"
                }
            if 'CompatToolMapping' not in config_data['InstallConfigStore']['Software']['Valve']['Steam']:
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}
            if str(shortcut_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['name'] = f'{compat_tool_name}'
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['config'] = ''
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)]['priority'] = '250'
            else:
                config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(shortcut_id)] = {'name': '', 'config': '', 'priority': '250'}

    # Only write back to the shortcuts.vdf file if new shortcuts were added
    if new_shortcuts_added:
        with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
            file.write(vdf.binary_dumps(shortcuts))


#End of Ubisoft Game Scanner

with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
    vdf.dump(config_data, file)

# Print the created shortcuts
    print("Created Shortcuts:")
    for name in created_shortcuts:
        print(name)


print("All finished!")

