#!/usr/bin/env python3
import os, re
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
    name, value = line.strip().split('=', 1)
    os.environ[name] = value

# Delete env_vars entries for Chrome shortcuts so that they're only added once
with open(env_vars_path, 'w') as f:
    for line in lines:
        if line.find('chromelaunchoptions') == -1 and line.find('websites_str') == -1:
            f.write(line)

# Variables from NonSteamLaunchers.sh
steamid3 = os.environ['steamid3']
logged_in_home = os.environ['logged_in_home']
compat_tool_name = os.environ['compat_tool_name']
controller_config_path = os.environ['controller_config_path']
python_version = os.environ['python_version']
#Scanner Variables
epic_games_launcher = os.environ.get('epic_games_launcher', '')
ubisoft_connect_launcher = os.environ.get('ubisoft_connect_launcher', '')
ea_app_launcher = os.environ.get('ea_app_launcher', '')
gog_galaxy_launcher = os.environ.get('gog_galaxy_launcher', '')
bnet_launcher = os.environ.get('bnet_launcher', '')
amazon_launcher = os.environ.get('amazon_launcher', '')


#Variables of the Launchers
# Define the path of the Launchers
epicshortcutdirectory = os.environ.get('epicshortcutdirectory')
gogshortcutdirectory = os.environ.get('gogshortcutdirectory')
uplayshortcutdirectory = os.environ.get('uplayshortcutdirectory')
battlenetshortcutdirectory = os.environ.get('battlenetshortcutdirectory')
eaappshortcutdirectory = os.environ.get('eaappshortcutdirectory')
amazonshortcutdirectory = os.environ.get('amazonshortcutdirectory')
itchioshortcutdirectory = os.environ.get('itchioshortcutdirectory')
legacyshortcutdirectory = os.environ.get('legacyshortcutdirectory')
humbleshortcutdirectory = os.environ.get('humbleshortcutdirectory')
indieshortcutdirectory = os.environ.get('indieshortcutdirectory')
rockstarshortcutdirectory = os.environ.get('rockstarshortcutdirectory')
glyphshortcutdirectory = os.environ.get('glyphshortcutdirectory')
minecraftshortcutdirectory = os.environ.get('minecraftshortcutdirectory')
psplusshortcutdirectory = os.environ.get('psplusshortcutdirectory')
vkplayhortcutdirectory = os.environ.get('vkplayhortcutdirectory')
#Streaming
chromedirectory = os.environ.get('chromedirectory')
websites_str = os.environ.get('custom_websites_str')
custom_websites = websites_str.split(', ') if websites_str else []



# Define the parent folder
parent_folder = f"{logged_in_home}/.config/systemd/user/Modules"
sys.path.insert(0, os.path.expanduser(f"{logged_in_home}/.config/systemd/user/Modules"))
print(sys.path)
# Now that the requests module has been downloaded, you can import it
sys.path.insert(0, parent_folder)
import requests
import vdf
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
sgdb = SteamGridDB('36e4bedbfdda27f42f9ef4a44f80955c')
api_key = '36e4bedbfdda27f42f9ef4a44f80955c'

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
        else:
            print(f"Error making API call: {response.status_code}")
            # Store the failed status in the cache
            api_cache[cache_key] = None
            return

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

# Add or update the proton compatibility settings
def add_compat_tool(app_id, launchoptions):
    if 'CompatToolMapping' not in config_data['InstallConfigStore']['Software']['Valve']['Steam']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}
        print(f"CompatToolMapping key not found in config.vdf, creating.")
    if str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] and config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] == f'{compat_tool_name}':
        return False
    if 'chrome' in launchoptions:
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
        print(f"Existing shortcut found based on shortcut ID for game {display_name}. Skipping creation.")
        return True
    # Check if the game already exists in the shortcuts using the fields (probably unnecessary)
    if any(s.get('appname') == display_name and s.get('exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on matching fields for game {display_name}. Skipping creation.")
        return True
#End of Code


#Start of Refactoring code from the .sh file
sys.path.insert(0, os.path.expanduser(f"{logged_in_home}/Downloads/NonSteamLaunchersInstallation/lib/python{python_version}/site-packages"))
print(sys.path)


# Create an empty dictionary to store the app IDs
app_ids = {}

#Create Launcher Shortcuts
def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir):
    global new_shortcuts_added
    global shortcuts_updated
    global created_shortcuts
    # Check if the launcher is installed
    if not shortcutdirectory or not appname or not launchoptions or not startingdir:
        print(f"{appname} is not installed. Skipping.")
        return
    exe_path = f"{shortcutdirectory}"
    signed_shortcut_id = get_steam_shortcut_id(exe_path, appname)
    unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
    # Only store the app ID for specific launchers
    if appname in ['Epic Games', 'Gog Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App', 'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client', 'Rockstar Games Launcher', 'Glyph', 'Minecraft: Java Edition', 'Playstation Plus', 'VK Play']:
        app_ids[appname] = unsigned_shortcut_id
    # Check if the game already exists in the shortcuts
    if check_if_shortcut_exists(signed_shortcut_id, appname, exe_path, startingdir, launchoptions):
        # Check if proton needs applying or updating
        if add_compat_tool(unsigned_shortcut_id, launchoptions):
            shortcuts_updated = True
        return
    #Get artwork
    game_id = get_game_id(appname)
    if game_id is not None:
        get_sgdb_art(game_id, unsigned_shortcut_id)

    # Create a new entry for the Steam shortcut
    new_entry = {
        'appid': str(signed_shortcut_id),
        'appname': appname,
        'exe': exe_path,
        'StartDir': startingdir,
        'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
        'LaunchOptions': launchoptions,
    }
    # Add the new entry to the shortcuts dictionary and add proton
    shortcuts['shortcuts'][str(signed_shortcut_id)] = new_entry
    print(f"Added new entry for {appname} to shortcuts.")
    new_shortcuts_added = True
    created_shortcuts.append(appname)
    add_compat_tool(unsigned_shortcut_id, launchoptions)


create_new_entry(os.environ.get('epicshortcutdirectory'), 'Epic Games', os.environ.get('epiclaunchoptions'), os.environ.get('epicstartingdir'))
create_new_entry(os.environ.get('gogshortcutdirectory'), 'Gog Galaxy', os.environ.get('goglaunchoptions'), os.environ.get('gogstartingdir'))
create_new_entry(os.environ.get('uplayshortcutdirectory'), 'Ubisoft Connect', os.environ.get('uplaylaunchoptions'), os.environ.get('uplaystartingdir'))
create_new_entry(os.environ.get('battlenetshortcutdirectory'), 'Battle.net', os.environ.get('battlenetlaunchoptions'), os.environ.get('battlenetstartingdir'))
create_new_entry(os.environ.get('eaappshortcutdirectory'), 'EA App', os.environ.get('eaapplaunchoptions'), os.environ.get('eaappstartingdir'))
create_new_entry(os.environ.get('amazonshortcutdirectory'), 'Amazon Games', os.environ.get('amazonlaunchoptions'), os.environ.get('amazonstartingdir'))
create_new_entry(os.environ.get('itchioshortcutdirectory'), 'itch.io', os.environ.get('itchiolaunchoptions'), os.environ.get('itchiostartingdir'))
create_new_entry(os.environ.get('legacyshortcutdirectory'), 'Legacy Games', os.environ.get('legacylaunchoptions'), os.environ.get('legacystartingdir'))
create_new_entry(os.environ.get('humbleshortcutdirectory'), 'Humble Bundle', os.environ.get('humblelaunchoptions'), os.environ.get('humblestartingdir'))
create_new_entry(os.environ.get('indieshortcutdirectory'), 'IndieGala Client', os.environ.get('indielaunchoptions'), os.environ.get('indiestartingdir'))
create_new_entry(os.environ.get('rockstarshortcutdirectory'), 'Rockstar Games Launcher', os.environ.get('rockstarlaunchoptions'), os.environ.get('rockstarstartingdir'))
create_new_entry(os.environ.get('glyphshortcutdirectory'), 'Glyph', os.environ.get('glyphlaunchoptions'), os.environ.get('glyphstartingdir'))
create_new_entry(os.environ.get('minecraftshortcutdirectory'), 'Minecraft: Java Edition', os.environ.get('minecraftlaunchoptions'), os.environ.get('minecraftstartingdir'))
create_new_entry(os.environ.get('psplusshortcutdirectory'), 'Playstation Plus', os.environ.get('pspluslaunchoptions'), os.environ.get('psplusstartingdir'))
create_new_entry(os.environ.get('vkplayhortcutdirectory'), 'VK Play', os.environ.get('vkplaylaunchoptions'), os.environ.get('vkplaystartingdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Xbox Game Pass', os.environ.get('xboxchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'GeForce Now', os.environ.get('geforcechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Netflix', os.environ.get('netlfixchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Hulu', os.environ.get('huluchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Disney+', os.environ.get('disneychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Prime Video', os.environ.get('amazonchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Youtube', os.environ.get('youtubechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Luna', os.environ.get('lunachromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Twitch', os.environ.get('twitchchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'movie-web', os.environ.get('moviewebchromelaunchoptions'), os.environ.get('chrome_startdir'))



# Iterate over each custom website
for custom_website in custom_websites:
    # Check if the custom website is not an empty string
    if custom_website:
        # Remove any leading or trailing spaces from the custom website URL
        custom_website = custom_website.strip()

        # Remove the 'http://' or 'https://' prefix and the 'www.' prefix, if present
        clean_website = custom_website.replace('http://', '').replace('https://', '').replace('www.', '')

        # Define a regular expression pattern to extract the game name from the URL
        pattern = r'/games/([\w-]+)'

        # Use the regular expression to search for the game name in the custom website URL
        match = re.search(pattern, custom_website)

        # Check if a match was found
        if match:
            # Extract the game name from the match object
            game_name = match.group(1)

            # Replace hyphens with spaces
            game_name = game_name.replace('-', ' ')

            # Capitalize the first letter of each word in the game name
            game_name = game_name.title()
        else:
            # Use the entire URL as the entry name
            game_name = clean_website

        # Define the launch options for this website
        chromelaunch_options = f'run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://{clean_website}/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar'

        # Call the create_new_entry function for this website
        create_new_entry(os.environ['chromedirectory'], game_name, chromelaunch_options, os.environ['chrome_startdir'])

#End of Creating Launcher Shortcuts







# Iterate over each launcher in the app_ids dictionary
for launcher_name, appid in app_ids.items():
    print(f"The app ID for {launcher_name} is {appid}")

# Get the app ID for the first launcher that the user chose to install
if app_ids:
    appid = app_ids.get(launcher_name)


#Create User Friendly Symlinks for the launchers
# Define the path to the compatdata directory
compatdata_dir = f'{logged_in_home}/.local/share/Steam/steamapps/compatdata'

# Define a dictionary of original folder names
folder_names = {
    'Epic Games': 'EpicGamesLauncher',
    'Gog Galaxy': 'GogGalaxyLauncher',
    'Ubisoft Connect': 'UplayLauncher',
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
    'VK Play': 'VKPlayLauncher',
}

# Iterate over each launcher in the folder_names dictionary
for launcher_name, folder in folder_names.items():
    # Define the current path of the folder
    current_path = os.path.join(compatdata_dir, folder)

    # Check if the folder exists
    if os.path.exists(current_path):
        print(f'{launcher_name}: {folder} exists')
        # Get the app ID for this launcher from the app_id_to_name dictionary
        appid = app_ids.get(launcher_name)

        # Define the new path of the folder
        new_path = os.path.join(compatdata_dir, str(appid))

        # Rename the folder
        os.rename(current_path, new_path)

        # Define the path of the symbolic link
        symlink_path = os.path.join(compatdata_dir, folder)

        # Create a symbolic link to the renamed folder
        os.symlink(new_path, symlink_path)
    else:
        print(f'{launcher_name}: {folder} does not exist')


# Check if the NonSteamLaunchers folder exists
if app_ids and os.path.exists(os.path.join(compatdata_dir, 'NonSteamLaunchers')):
    # Get the first app ID from the app_ids list
    first_app_id = next(iter(app_ids.values()))

    # Define the current path of the NonSteamLaunchers folder
    current_path = os.path.join(compatdata_dir, 'NonSteamLaunchers')

    # Check if NonSteamLaunchers is already a symbolic link
    if os.path.islink(current_path):
        print('NonSteamLaunchers is already a symbolic link')
    else:
        # Define the new path of the NonSteamLaunchers folder
        new_path = os.path.join(compatdata_dir, str(first_app_id))

        # Move the NonSteamLaunchers folder to the new path
        shutil.move(current_path, new_path)

        # Define the path of the symbolic link
        symlink_path = os.path.join(compatdata_dir, 'NonSteamLaunchers')

        # Create a symbolic link to the renamed NonSteamLaunchers folder
        os.symlink(new_path, symlink_path)

#End of Refactoring python code from .sh file



# Print the existing shortcuts
print("Existing Shortcuts:")
for shortcut in shortcuts['shortcuts'].values():
    if shortcut.get('appname') is None:
        print(f"AppID for {shortcut.get('AppName')}: {shortcut.get('appid')}")
    else:
        print(f"AppID for {shortcut.get('appname')}: {shortcut.get('appid')}")





#Scanners
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

            # Check if the game is still installed
            for game in dat_data['InstallationList']:
                if game['AppName'] == item_data['AppName']:
                    create_new_entry(exe_path, display_name, launch_options, start_dir)

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
            create_new_entry(exe_path, game, launch_options, start_dir)

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
        create_new_entry(exe_path, game, launch_options, start_dir)

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
            create_new_entry(exe_path, game, launch_options, start_dir)

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
                create_new_entry(exe_path, game, launch_options, start_dir)

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
        create_new_entry(exe_path, display_name, launch_options, start_dir)


#End of Amazon Games Scanner




# Only write back to the shortcuts.vdf and config.vdf files if new shortcuts were added or compattools changed
if new_shortcuts_added or shortcuts_updated:
    print(f"Saving new config and shortcuts files")
    conf = vdf.dumps(config_data, pretty=True)
    with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
        file.write(conf)
    with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
        file.write(vdf.binary_dumps(shortcuts))

    # Load the configset_controller_neptune.vdf file
    with open(controller_config_path, 'r') as f:
        config = vdf.load(f)

    # Add new entries for the games
    for app_id in app_ids:
        config['controller_config'][str(app_id)] = {
            'workshop': 'workshop_id'
        }
        # Add new entries for the installed launchers and games
        config['controller_config']['epic games'] = {
            'workshop': '2800178806'
        }
        config['controller_config']['gog galaxy'] = {
            'workshop': '2877189386'
        }
        config['controller_config']['ubisoft connect'] = {
            'workshop': '2804140248'
        }
        config['controller_config']['amazon games'] = {
            'workshop': '2871935783'
        }
        config['controller_config']['battlenet'] = {
            'workshop': '2887894308'
        }
        config['controller_config']['rockstar games launcher'] = {
            'workshop': '1892570391'
        }
        config['controller_config']['indiegala'] = {
            'template': 'controller_neptune_webbrowser.vdf'
        }
        config['controller_config']['legacy games'] = {
            'template': 'controller_neptune_webbrowser.vdf'
        }
        config['controller_config']['ea app'] = {
            'workshop': '2899822740'
        }
        config['controller_config']['itchio'] = {
            'workshop': '2845891813'
        }
        config['controller_config']['humble games collection'] = {
            'workshop': '2883791560'
        }
        config['controller_config']['minecraft java edition'] = {
            'workshop': '2980553929'
        }
        config['controller_config']['playstation plus'] = {
            'workshop': 'controller_neptune_webbrowser.vdf'
        }
        config['controller_config']['glyph'] = {
            'template': 'controller_neptune_webbrowser.vdf'
        }
        config['controller_config']['vk play'] = {
            'workshop': '3202642880'
        }
        config['controller_config']['amazon prime video'] = {
            'workshop': '2970669392'
        }
        config['controller_config']['hulu'] = {
            'workshop': '2970669392'
        }
        config['controller_config']['netflix'] = {
            'workshop': '2970669392'
        }
        config['controller_config']['disney+'] = {
            'workshop': '2970669392'
        }
        config['controller_config']['youtube'] = {
            'workshop': '2970669392'
        }
        config['controller_config']['geforce now'] = {
            'template': 'controller_neptune_gamepad+mouse.vdf'
        }
        config['controller_config']['amazon luna'] = {
            'template': 'controller_neptune_gamepad+mouse.vdf'
        }
        config['controller_config']['twitch'] = {
            'workshop': '2875543745'
        }
        config['controller_config']['movie-web'] = {
            'workshop': 'controller_neptune_webbrowser.vdf'
        }

    # Save the updated config
    with open(controller_config_path, 'w') as f:
        vdf.dump(config, f)

    # Print the created shortcuts
    if created_shortcuts:
        print("Created Shortcuts:")
        for name in created_shortcuts:
            print(name)

    # Assuming 'games' is a list of game dictionaries
    games = [shortcut for shortcut in shortcuts['shortcuts'].values()]

    for game in games:
        # Skip if 'appname' or 'exe' is None
        if game.get('appname') is None or game.get('exe') is None:
            continue

        # Create a dictionary to hold the shortcut information
        shortcut_info = {
            'appid': str(game.get('appid')),
            'appname': game.get('appname'),
            'exe': game.get('exe'),
            'StartDir': game.get('StartDir'),
            'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', game.get('appid'))}",
            'LaunchOptions': game.get('LaunchOptions'),
            'GameID': game.get('GameID', "default_game_id")  # Use a default value if game_id is not defined
        }

        # Print the shortcut information in JSON format
        message = json.dumps(shortcut_info)
        print(message, flush=True)  # Print to stdout

print("All finished!")



