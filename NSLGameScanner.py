#!/usr/bin/env python3
import os, re
import json
import shutil
import binascii
import ctypes
import gzip
import zipfile
import time
import sys
import subprocess
import sqlite3
import csv
import configparser
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote
from base64 import b64encode
import xml.etree.ElementTree as ET

# Check the value of the DBUS_SESSION_BUS_ADDRESS environment variable
dbus_address = os.environ.get('DBUS_SESSION_BUS_ADDRESS')
if not dbus_address or not dbus_address.startswith('unix:path='):
    # Set the value of the DBUS_SESSION_BUS_ADDRESS environment variable
    dbus_address = f'unix:path=/run/user/{os.getuid()}/bus'
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus_address

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

# Store the value of separate_appids before deleting it
separate_appids = None

# Delete env_vars entries for Chrome shortcuts so that they're only added once
with open(env_vars_path, 'w') as f:
    for line in lines:
        if 'export separate_appids=false' in line:
            separate_appids = line.split('=')[1].strip()
        if line.find('chromelaunchoptions') == -1 and line.find('websites_str') == -1:
            f.write(line)






# Variables from NonSteamLaunchers.sh
steamid3 = os.environ['steamid3']
logged_in_home = os.environ['logged_in_home']
compat_tool_name = os.environ['compat_tool_name']
python_version = os.environ['python_version']
#Scanner Variables
epic_games_launcher = os.environ.get('epic_games_launcher', '')
ubisoft_connect_launcher = os.environ.get('ubisoft_connect_launcher', '')
ea_app_launcher = os.environ.get('ea_app_launcher', '')
gog_galaxy_launcher = os.environ.get('gog_galaxy_launcher', '')
bnet_launcher = os.environ.get('bnet_launcher', '')
amazon_launcher = os.environ.get('amazon_launcher', '')
itchio_launcher = os.environ.get('itchio_launcher', '')
legacy_launcher = os.environ.get('legacy_launcher', '')
vkplay_launcher = os.environ.get('vkplay_launcher', '')
hoyoplay_launcher = os.environ.get('hoyoplay_launcher', '')
gamejolt_launcher = os.environ.get('gamejolt_launcher', '')
minecraft_launcher = os.environ.get('minecraft_launcher', '')
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
vkplayshortcutdirectory = os.environ.get('vkplayshortcutdirectory')
hoyoplayshortcutdirectory = os.environ.get('hoyoplayshortcutfirectory')
nexonshortcutdirectory = os.environ.get('nexonshortcutdirectory')
gamejoltshortcutdirectory = os.environ.get('gamejoltshortcutdirectory')
artixgameshortcutdirectory = os.environ.get('artixgameshortcutdirectory')
arcshortcutdirectory = os.environ.get('arcshortcutdirectory')
poketcgshortcutdirectory = os.environ.get('poketcgshortcutdirectory')
repaireaappshortcutdirectory = os.environ.get('repaireaappshortcutdirectory')
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
BASE_URL = 'https://nonsteamlaunchers.onrender.com/api'

#GLOBAL VARS
created_shortcuts = []
new_shortcuts_added = False
shortcuts_updated = False
shortcut_id = None  # Initialize shortcut_id
decky_shortcuts = {}
gridp64 = ""
grid64 = ""
logo64 = ""
hero64 = ""


def create_empty_shortcuts():
    return {'shortcuts': {}}

def write_shortcuts_to_file(shortcuts_file, shortcuts):
    with open(shortcuts_file, 'wb') as file:
        file.write(vdf.binary_dumps(shortcuts))
    os.chmod(shortcuts_file, 0o755)

# Define the path to the shortcuts file
shortcuts_file = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf"

# Check if the file exists
if os.path.exists(shortcuts_file):
    # If the file is not executable, write the shortcuts dictionary and make it executable
    if not os.access(shortcuts_file, os.X_OK):
        print("The file is not executable. Writing an empty shortcuts dictionary and making it executable.")
        shortcuts = create_empty_shortcuts()
        write_shortcuts_to_file(shortcuts_file, shortcuts)
    else:
        # Load the existing shortcuts
        with open(shortcuts_file, 'rb') as file:
            try:
                shortcuts = vdf.binary_loads(file.read())
            except vdf.VDFError as e:
                print(f"Error reading file: {e}. The file might be corrupted or unreadable.")
                print("Exiting the program. Please check the shortcuts.vdf file.")
                sys.exit(1)
else:
    print("The shortcuts.vdf file does not exist.")
    sys.exit(1)




# Open the config.vdf file
with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
    config_data = vdf.load(file)


def get_sgdb_art(game_id, app_id):
    global grid64
    global gridp64
    global logo64
    global hero64
    print(f"Downloading icons artwork...")
    download_artwork(game_id, "icons", app_id)
    print(f"Downloading logos artwork...")
    logo64 = download_artwork(game_id, "logos", app_id)
    print(f"Downloading heroes artwork...")
    hero64 = download_artwork(game_id, "heroes", app_id)
    print("Downloading grids artwork of size 600x900...")
    gridp64 = download_artwork(game_id, "grids", app_id, "600x900")
    print("Downloading grids artwork of size 920x430...")
    grid64 = download_artwork(game_id, "grids", app_id, "920x430")

def download_artwork(game_id, art_type, shortcut_id, dimensions=None):
    if game_id is None:
        print("Invalid game ID. Skipping download.")
        return

    cache_key = (game_id, art_type, dimensions)
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
        with open(file_path, 'rb') as image_file:
            return b64encode(image_file.read()).decode('utf-8')

    if cache_key in api_cache:
        data = api_cache[cache_key]
    else:
        try:
            print(f"Game ID: {game_id}")
            url = f"{BASE_URL}/{art_type}/game/{game_id}"
            if dimensions:
                url += f"?dimensions={dimensions}"
            print(f"Request URL: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            api_cache[cache_key] = data
        except Exception as e:
            print(f"Error making API call: {e}")
            api_cache[cache_key] = None
            return

    if not data or 'data' not in data:
        print(f"No data available for {game_id}. Skipping download.")
        return

    for artwork in data['data']:
        image_url = artwork['thumb']
        print(f"Downloading image from: {image_url}")

        # Try both .png and .ico formats
        for ext in ['png', 'ico']:
            try:
                alt_file_path = file_path.replace('.png', f'.{ext}')
                response = requests.get(image_url, stream=True)
                response.raise_for_status()

                if response.status_code == 200:
                    with open(alt_file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Downloaded {alt_file_path}")
                    return b64encode(response.content).decode('utf-8')
            except requests.exceptions.RequestException as e:
                print(f"Error downloading image in {ext}: {e}")

    print(f"Artwork download failed for {game_id}. Neither PNG nor ICO was available.")
    return None

def get_game_id(game_name):
    print(f"Searching for game ID for: {game_name}")
    try:
        encoded_game_name = quote(game_name)
        url = f"{BASE_URL}/search/{encoded_game_name}"
        print(f"Encoded game name: {encoded_game_name}")
        print(f"Request URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data['data']:
            game_id = data['data'][0]['id']
            print(f"Found game ID: {game_id}")
            return game_id
        print(f"No game ID found for game name: {game_name}")
        return None
    except Exception as e:
        print(f"Error searching for game ID: {e}")
        return None

def get_file_name(art_type, shortcut_id, dimensions=None):
    singular_art_type = art_type.rstrip('s')
    if art_type == 'icons':
        # Check for the existing .png file first
        if os.path.exists(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{shortcut_id}-{singular_art_type}.png"):
            return f"{shortcut_id}-{singular_art_type}.png"
        # Fallback to .ico if .png doesn't exist
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



def get_steam_store_appid(steam_store_game_name):
    search_url = f"{BASE_URL}/search/{steam_store_game_name}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data['data']:
            steam_store_appid = data['data'][0].get('steam_store_appid')
            if steam_store_appid:
                return steam_store_appid
        return None

    except requests.exceptions.RequestException as e:
        return None

def create_steam_store_app_manifest_file(steam_store_appid, steam_store_game_name):
    steamapps_dir = f"{logged_in_home}/.steam/root/steamapps/"
    appmanifest_path = os.path.join(steamapps_dir, f"appmanifest_{steam_store_appid}.acf")

    # Ensure the directory exists
    os.makedirs(steamapps_dir, exist_ok=True)

    # Check if the file already exists
    if os.path.exists(appmanifest_path):
        print(f"Manifest file for {steam_store_appid} already exists.")
        return

    # Prepare the appmanifest data
    app_manifest_data = {
        "AppState": {
            "AppID": str(steam_store_appid),
            "Universe": "1",
            "installdir": steam_store_game_name,
            "StateFlags": "0"
        }
    }

    # Write the manifest to the file
    with open(appmanifest_path, 'w') as file:
        json.dump(app_manifest_data, file, indent=2)

    print(f"Created appmanifest file at: {appmanifest_path}")

# Add or update the proton compatibility settings


def add_compat_tool(app_id, launchoptions):
    if 'CompatToolMapping' not in config_data['InstallConfigStore']['Software']['Valve']['Steam']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}
        print(f"CompatToolMapping key not found in config.vdf, creating.")

    # Combine checks for 'chrome' and 'PROTONPATH'
    if 'chrome' in launchoptions or 'PROTONPATH' in launchoptions:
        if 'PROTONPATH' in launchoptions:
            print("PROTONPATH found in launch options. Skipping compatibility tool update.")
        return False

    elif str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] = f'{compat_tool_name}'
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['config'] = ''
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['priority'] = '250'
        print(f"Updated CompatToolMapping entry for appid: {app_id}")
        return compat_tool_name
    else:
        # Skip if the shortcut has already been processed by UMU
        if app_id in umu_processed_shortcuts:
            print(f"CompatTool update skipped for {app_id} because it was already processed by UMU.")
            return None
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)] = {'name': f'{compat_tool_name}', 'config': '', 'priority': '250'}
        print(f"Created new CompatToolMapping entry for appid: {app_id}")
        return compat_tool_name


# Check if the shortcut already exists in the shortcuts
def check_if_shortcut_exists(shortcut_id, display_name, exe_path, start_dir, launch_options):
    # Check if the game already exists in the shortcuts using the ID
    if any(s.get('appid') == shortcut_id for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on shortcut ID for game {display_name}. Skipping creation.")
        return True
    # Check if the game already exists in the shortcuts using the fields (probably unnecessary)
    if any(s.get('appname') == display_name and s.get('exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on matching fields for game {display_name}. Skipping creation.")
        return True
    if any(s.get('AppName') == display_name and s.get('Exe') == exe_path and s.get('StartDir') == start_dir and s.get('LaunchOptions') == launch_options for s in shortcuts['shortcuts'].values()):
        print(f"Existing shortcut found based on matching fields for game {display_name}. Skipping creation.")
        return True
    return False


# Start of Refactoring code from the .sh file
sys.path.insert(0, os.path.expanduser(f"{logged_in_home}/Downloads/NonSteamLaunchersInstallation/lib/python{python_version}/site-packages"))
print(sys.path)


# Create an empty dictionary to store the app IDs
app_ids = {}

# Get the next available key for the shortcuts
def get_next_available_key(shortcuts):
    key = 0
    while str(key) in shortcuts['shortcuts']:
        key += 1
    return str(key)


def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir):
    global new_shortcuts_added
    global shortcuts_updated
    global created_shortcuts
    global decky_shortcuts
    global grid64
    global gridp64
    global logo64
    global hero64
    global counter  # Add this line to access the counter variable

    # Check if the launcher is installed
    if not shortcutdirectory or not appname or not launchoptions or not startingdir:
        print(f"{appname} is not installed. Skipping.")
        return
    exe_path = f"{shortcutdirectory}"
    signed_shortcut_id = get_steam_shortcut_id(exe_path, appname)
    unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)

    # **Intercept and modify the shortcut based on UMU data**
    exe_path, startingdir, launchoptions = modify_shortcut_for_umu(appname, exe_path, launchoptions, startingdir)

    # Check if the shortcut has already been processed by UMU and skip compat tool if so
    if unsigned_shortcut_id in umu_processed_shortcuts:
        print(f"Skipping compatibility tool for {appname}, as it has already been processed by UMU.")
        compatTool = None  # Skip adding compatibility tool
    else:
        compatTool = add_compat_tool(unsigned_shortcut_id, launchoptions)

    # Only store the app ID for specific launchers
    if appname in ['Epic Games', 'Gog Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App', 'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client', 'Rockstar Games Launcher', 'Glyph', 'Minecraft Launcher' 'Playstation Plus', 'VK Play', 'HoYoPlay', 'Nexon Launcher', 'Game Jolt Client', 'Artix Game Launcher', 'ARC Launcher', 'Pokémon Trading Card Game Live']:
        app_ids[appname] = unsigned_shortcut_id

    # Check if the game already exists in the shortcuts
    if check_if_shortcut_exists(signed_shortcut_id, appname, exe_path, startingdir, launchoptions):
        # Check if proton needs applying or updating
        if add_compat_tool(unsigned_shortcut_id, launchoptions):
            shortcuts_updated = True
        return

    # Skip artwork download for specific shortcuts
    if appname not in ['NonSteamLaunchers', 'Repair EA App']:
        # Get artwork
        game_id = get_game_id(appname)
        if game_id is not None:
            get_sgdb_art(game_id, unsigned_shortcut_id)


    steam_store_appid = get_steam_store_appid(appname)
    if steam_store_appid:
        print(f"Found Steam App ID for {appname}: {steam_store_appid}")
        create_steam_store_app_manifest_file(steam_store_appid, appname)

    # Create a new entry for the Steam shortcut, only adding the compat tool if it's not processed by UMU
    new_entry = {
        'appid': str(signed_shortcut_id),
        'appname': appname,
        'exe': exe_path,
        'StartDir': startingdir,
        'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
        'ShortcutPath': "",
        'LaunchOptions': launchoptions,
        'IsHidden': 0,
        'AllowDesktopConfig': 1,
        'AllowOverlay': 1,
        'OpenVR': 0,
        'Devkit': 0,
        'DevkitGameID': "",
        'DevkitOverrideAppID': 0,
        'LastPlayTime': 0,
        'FlatpakAppID': "",
        'tags': {
            '0': 'NonSteamLaunchers'
        }
    }

    # Add the new entry to the shortcuts dictionary and add proton
    key = get_next_available_key(shortcuts)
    shortcuts['shortcuts'][key] = new_entry
    print(f"Added new entry for {appname} to shortcuts.")
    new_shortcuts_added = True
    created_shortcuts.append(appname)

    # Mark it as processed by UMU (if it wasn't already processed)
    if compatTool is not None:
        umu_processed_shortcuts[unsigned_shortcut_id] = True



# UMU-related functions
umu_processed_shortcuts = {}
CSV_URL = "https://raw.githubusercontent.com/Open-Wine-Components/umu-database/main/umu-database.csv"

# Global variable to store CSV data
csv_data = []

def fetch_and_parse_csv():
    global csv_data
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        csv_data = [row for row in csv.DictReader(response.text.splitlines())]
        print("Successfully fetched and parsed CSV data.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching UMU data: {e}")
    return csv_data

def list_all_entries():
    global csv_data
    if not csv_data:
        csv_data = fetch_and_parse_csv()
    return csv_data

def extract_umu_id_from_launch_options(launchoptions):
    if 'STEAM_COMPAT_DATA_PATH=' not in launchoptions:
        return None

    # EA
    match = re.search(r'offerIds=(\d+)', launchoptions)
    if match:
        return match.group(1)

    # Amazon
    match = re.search(r'(amzn1\.adg\.product\.\S+)', launchoptions)
    if match:
        return match.group(1).rstrip("'")

    # Epic
    match = re.search(r'com\.epicgames\.launcher://apps/(\w+)[?&]', launchoptions)
    if match:
        return match.group(1).lower() if not match.group(1).isdigit() else match.group(1)

    # Ubisoft
    match = re.search(r'uplay://launch/(\d+)/\d+', launchoptions)
    if match:
        return match.group(1)

    # GOG
    match = re.search(r'/gameId=(\d+)', launchoptions)
    if match:
        return match.group(1)

    return None

def extract_base_path(launchoptions):
    match = re.search(r'STEAM_COMPAT_DATA_PATH="([^"]+)"', launchoptions)
    if match:
        return match.group(1)
    raise ValueError("STEAM_COMPAT_DATA_PATH not found in launch options")

def modify_shortcut_for_umu(appname, exe, launchoptions, startingdir):
    # Skip processing if STEAM_COMPAT_DATA_PATH is not present
    if 'STEAM_COMPAT_DATA_PATH=' not in launchoptions:
        print(f"Launch options for {appname} do not contain STEAM_COMPAT_DATA_PATH. Skipping modification.")
        return exe, startingdir, launchoptions

    codename = extract_umu_id_from_launch_options(launchoptions)
    if not codename:
        print(f"No codename found in launch options for {appname}. Trying to match appname.")

    entries = list_all_entries()
    if not entries:
        print(f"No entries found in UMU database. Skipping modification for {appname}.")
        return exe, startingdir, launchoptions

    if not codename:
        for entry in entries:
            if entry.get('TITLE') and entry['TITLE'].lower() == appname.lower():
                codename = entry['CODENAME']
                break

    if codename:
        for entry in entries:
            if entry['CODENAME'] == codename:
                umu_id = entry['UMU_ID'].replace("umu-", "")  # Remove the "umu-" prefix
                base_path = extract_base_path(launchoptions)
                new_exe = f'"{logged_in_home}/bin/umu-run" {exe}'
                new_start_dir = f'"{logged_in_home}/bin/"'

                # Update only the launchoptions part for different game types
                updated_launch = launchoptions

                # Hoyoplay - Extract the game identifier
                match = re.search(r'--game=(\w+)', launchoptions)
                if match:
                    codename = match.group(1)  # Capture the identifier
                    updated_launch = f"'--game={codename}'"

                if "origin2://game/launch?offerIds=" in launchoptions:
                    updated_launch = f'"origin2://game/launch?offerIds={codename}"'
                elif "amazon-games://play/amzn1.adg.product." in launchoptions:
                    updated_launch = f"-'amazon-games://play/{codename}'"
                elif "com.epicgames.launcher://apps/" in launchoptions:
                    updated_launch = f"-'com.epicgames.launcher://apps/{codename}?action=launch&silent=true'"
                elif "uplay://launch/" in launchoptions:
                    updated_launch = f'"uplay://launch/{codename}/0"'
                elif "/command=runGame /gameId=" in launchoptions:
                    updated_launch = f'/command=runGame /gameId={codename} /path={launchoptions.split("/path=")[1]}'

                # Ensure the first STEAM_COMPAT_DATA_PATH is included and avoid adding it again
                if 'STEAM_COMPAT_DATA_PATH=' in updated_launch:
                    # Remove the existing STEAM_COMPAT_DATA_PATH if it exists in the launch options
                    updated_launch = re.sub(r'STEAM_COMPAT_DATA_PATH="[^"]+" ', '', updated_launch)

                # Always include the first STEAM_COMPAT_DATA_PATH at the start
                new_launch_options = (
                    f'STEAM_COMPAT_DATA_PATH="{base_path}" '
                    f'WINEPREFIX="{base_path}pfx" '
                    f'GAMEID="{umu_id}" '
                    f'PROTONPATH="{logged_in_home}/.steam/root/compatibilitytools.d/{compat_tool_name}" '
                )

                # Check if %command% is already in the launch options
                if '%command%' not in updated_launch:
                    updated_launch = f'%command% {updated_launch}'

                # Final new launch options
                new_launch_options += updated_launch

                umu_processed_shortcuts[umu_id] = True

                return new_exe, new_start_dir, new_launch_options

    print(f"No UMU entry found for {appname}. Skipping modification.")
    return exe, startingdir, launchoptions














create_new_entry(os.environ.get('epicshortcutdirectory'), 'Epic Games', os.environ.get('epiclaunchoptions'), os.environ.get('epicstartingdir'))
create_new_entry(os.environ.get('gogshortcutdirectory'), 'GOG Galaxy', os.environ.get('goglaunchoptions'), os.environ.get('gogstartingdir'))
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
create_new_entry(os.environ.get('minecraftshortcutdirectory'), 'Minecraft Launcher', os.environ.get('minecraftlaunchoptions'), os.environ.get('minecraftstartingdir'))
create_new_entry(os.environ.get('psplusshortcutdirectory'), 'Playstation Plus', os.environ.get('pspluslaunchoptions'), os.environ.get('psplusstartingdir'))
create_new_entry(os.environ.get('vkplayshortcutdirectory'), 'VK Play', os.environ.get('vkplaylaunchoptions'), os.environ.get('vkplaystartingdir'))
create_new_entry(os.environ.get('hoyoplayshortcutdirectory'), 'HoYoPlay', os.environ.get('hoyoplaylaunchoptions'), os.environ.get('hoyoplaystartingdir'))
create_new_entry(os.environ.get('nexonshortcutdirectory'), 'Nexon Launcher', os.environ.get('nexonlaunchoptions'), os.environ.get('nexonstartingdir'))
create_new_entry(os.environ.get('gamejoltshortcutdirectory'), 'Game Jolt Client', os.environ.get('gamejoltlaunchoptions'), os.environ.get('gamejoltstartingdir'))
create_new_entry(os.environ.get('artixgameshortcutdirectory'), 'Artix Game Launcher', os.environ.get('artixgamelaunchoptions'), os.environ.get('artixgamestartingdir'))
create_new_entry(os.environ.get('arcshortcutdirectory'), 'ARC Launcher', os.environ.get('arclaunchoptions'), os.environ.get('arcstartingdir'))
create_new_entry(os.environ.get('poketcgshortcutdirectory'), 'Pokémon Trading Card Game Live', os.environ.get('poketcglaunchoptions'), os.environ.get('poketcgstartingdir'))
create_new_entry(os.environ.get('repaireaappshortcutdirectory'), 'Repair EA App', os.environ.get('repaireaapplaunchoptions'), os.environ.get('repaireaappstartingdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Xbox Game Pass', os.environ.get('xboxchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'GeForce Now', os.environ.get('geforcechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Boosteroid Cloud Gaming', os.environ.get('boosteroidchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Stim.io', os.environ.get('stimiochromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WatchParty', os.environ.get('watchpartychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Netflix', os.environ.get('netflixchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Hulu', os.environ.get('huluchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Disney+', os.environ.get('disneychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Prime Video', os.environ.get('amazonchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Youtube', os.environ.get('youtubechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Luna', os.environ.get('lunachromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Twitch', os.environ.get('twitchchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Venge', os.environ.get('vengechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Rocketcrab', os.environ.get('rocketcrabchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Fortnite', os.environ.get('fortnitechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WebRcade', os.environ.get('webrcadechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WebRcade Editor', os.environ.get('webrcadeeditchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Plex', os.environ.get('plexchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Apple TV+', os.environ.get('applechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Crunchyroll', os.environ.get('crunchychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'PokéRogue', os.environ.get('pokeroguechromelaunchoptions'), os.environ.get('chrome_startdir'))

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
        chromelaunch_options = f'run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --start-fullscreen https://{clean_website}/ --no-first-run --enable-features=OverlayScrollbar'

        # Call the create_new_entry function for this website
        create_new_entry(os.environ['chromedirectory'], game_name, chromelaunch_options, os.environ['chrome_startdir'])

#End of Creating Launcher Shortcuts


#Custom Shortcut for NSL
# Define the parameters for the new shortcut
nslshortcutdirectory = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\""
nslappname = "NonSteamLaunchers"
nsllaunchoptions = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
nslstartingdir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\""
print(f"nslshortcutdirectory: {nslshortcutdirectory}")  # Debug print
print(f"nslappname: {nslappname}")  # Debug print
print(f"nsllaunchoptions: {nsllaunchoptions}")  # Debug print



# Check if separate_appids is set to 'false'
if separate_appids == 'false':
    print("separate_appids is set to 'false'. Creating new shortcut...")  # Debug print
    # Call the function to create the new shortcut and store the returned appid
    appid = create_new_entry(nslshortcutdirectory, nslappname, nsllaunchoptions, nslstartingdir)
    app_ids[nslappname] = appid
    print(f"appid: {appid}")  # Debug print
else:
    print("separate_appids is not set to 'false'. Skipping shortcut creation.")  # Debug print




# Iterate over each launcher in the app_ids dictionary
for launcher_name, appid in app_ids.items():
    print(f"The app ID for {launcher_name} is {appid}")

# Get the app ID for the first launcher that the user chose to install
if app_ids:
    appid = app_ids.get(launcher_name)
    print(f"App ID for the chosen launcher: {appid}")

# Create User Friendly Symlinks for the launchers
# Define the path to the compatdata directory
compatdata_dir = f'{logged_in_home}/.local/share/Steam/steamapps/compatdata'
print(f"Compatdata directory: {compatdata_dir}")

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
    'Glyph': 'GlyphLauncher',
    'Playstation Plus': 'PlaystationPlusLauncher',
    'VK Play': 'VKPlayLauncher',
    'HoYoPlay': 'HoYoPlayLauncher',
    'Nexon Launcher': 'NexonLauncher',
    'Game Jolt Client': 'GameJoltLauncher',
    'Artix Game Launcher': 'ArtixGameLauncher',
    'ARC Launcher': 'ARCLauncher',
    'Pokémon Trading Card Game Live': 'PokeTCGLauncher',
}


# Iterate over each launcher in the folder_names dictionary
for launcher_name, folder in folder_names.items():
    # Define the current path of the folder
    current_path = os.path.join(compatdata_dir, folder)
    print(f"Current path for {launcher_name}: {current_path}")

    # Check if the folder exists
    if os.path.exists(current_path):
        print(f'{launcher_name}: {folder} exists')
        # Get the app ID for this launcher from the app_id_to_name dictionary
        appid = app_ids.get(launcher_name)
        print(f"App ID for {launcher_name}: {appid}")

        # If appid is not None, proceed with renaming and symlink creation
        if appid is not None:
            # Define the new path of the folder
            new_path = os.path.join(compatdata_dir, str(appid))
            print(f"New path for {launcher_name}: {new_path}")

            # Check if the new path already exists
            if os.path.exists(new_path):
                print(f'{new_path} already exists. Skipping renaming and symlinking.')
            else:
                # Rename the folder
                os.rename(current_path, new_path)
                print(f"Renamed {current_path} to {new_path}")

                # Define the path of the symbolic link
                symlink_path = os.path.join(compatdata_dir, folder)
                print(f"Symlink path for {launcher_name}: {symlink_path}")

                # Create a symbolic link to the renamed folder
                os.symlink(new_path, symlink_path)
                print(f"Created symlink at {symlink_path} to {new_path}")
        else:
            print(f'App ID for {launcher_name} is not available yet.')
    else:
        print(f'{launcher_name}: {folder} does not exist')




# Define the appid for the custom shortcut
custom_app_id = 4206469918
print(f"App ID for the custom shortcut: {custom_app_id}")

# Check if the NonSteamLaunchers folder exists
non_steam_launchers_path = os.path.join(compatdata_dir, 'NonSteamLaunchers')
if os.path.exists(non_steam_launchers_path):
    print("NonSteamLaunchers already exists at the expected path.")

    # Define the current path of the NonSteamLaunchers folder
    current_path = os.path.join(compatdata_dir, 'NonSteamLaunchers')
    print(f"Current path for NonSteamLaunchers: {current_path}")

    # Check if NonSteamLaunchers is already a symbolic link
    if os.path.islink(current_path):
        print('NonSteamLaunchers is already a symbolic link')
        # Check if NonSteamLaunchers is a symlink to an appid folder
        if os.readlink(current_path) != os.path.join(compatdata_dir, str(custom_app_id)):
            print('NonSteamLaunchers is symlinked to a different folder')
            # Remove the existing symbolic link
            os.unlink(current_path)
            print(f'Removed existing symlink at {current_path}')
            # Create a symbolic link to the correct appid folder
            os.symlink(os.path.join(compatdata_dir, str(custom_app_id)), current_path)
            print(f'Created new symlink at {current_path} to {os.path.join(compatdata_dir, str(custom_app_id))}')
        else:
            print('NonSteamLaunchers is already correctly symlinked')
    else:
        print("NonSteamLaunchers is not a symbolic link.")
        # Check if the current path exists
        if os.path.exists(current_path):
            print("NonSteamLaunchers exists at the current path.")
            # Define the new path of the NonSteamLaunchers folder
            new_path = os.path.join(compatdata_dir, str(custom_app_id))
            print(f"New path for NonSteamLaunchers: {new_path}")

            # Check if the new path already exists
            if os.path.exists(new_path):
                print(f'{new_path} already exists. Skipping renaming and symlinking.')
            else:
                # Move the NonSteamLaunchers folder to the new path
                shutil.move(current_path, new_path)
                print(f"Moved NonSteamLaunchers folder to {new_path}")

                # Define the path of the symbolic link
                symlink_path = os.path.join(compatdata_dir, 'NonSteamLaunchers')

                # Create a symbolic link to the renamed NonSteamLaunchers folder
                os.symlink(new_path, symlink_path)
                print(f"Created symlink at {symlink_path} to {new_path}")
        else:
            print(f"The directory {current_path} does not exist. Skipping.")


#End of old refactored Code





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

    # Epic Game Scanner
    for item_file in os.listdir(item_dir):
        if item_file.endswith('.item'):
            with open(os.path.join(item_dir, item_file), 'r') as file:
                item_data = json.load(file)

            # Initialize variables
            display_name = item_data['DisplayName']
            app_name = item_data['AppName']
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/\""
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/\" %command% -'com.epicgames.launcher://apps/{app_name}?action=launch&silent=true'"

            # Check if the game is still installed and if the LaunchExecutable is valid, not content-related, and is a .exe file
            if item_data['LaunchExecutable'].endswith('.exe') and "Content" not in item_data['DisplayName'] and "Content" not in item_data['InstallLocation']:
                for game in dat_data['InstallationList']:
                    if game['AppName'] == item_data['AppName']:
                        create_new_entry(exe_path, display_name, launch_options, start_dir)

else:
    print("Epic Games Launcher data not found. Skipping Epic Games Scanner.")
# End of the Epic Games Scanner




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
            line = line.replace("\\x2019", "’")
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
            if uplay_id and game_name and uplay_id in uplay_ids:
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
            ea_ids = content_id.text
            break  # Exit the loop after the first ID is found
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
        depends_on = None
        launch_command = None
        start_menu_link = None
        gog_entry = False
        for line in file:
            split_line = line.split("=")
            if len(split_line) > 1:
                if "gameid" in line.lower():
                    game_id = re.findall(r'\"(.+?)\"', split_line[1])
                    if game_id:
                        game_id = game_id[0]
                if "gamename" in line.lower():
                    game_name = re.findall(r'\"(.+?)\"', split_line[1])
                    if game_name:
                        game_name = bytes(game_name[0], 'utf-8').decode('unicode_escape')
                        game_name = game_name.replace('!22', '™')
                if "exe" in line.lower() and not "unins000.exe" in line.lower():
                    exe_path = re.findall(r'\"(.+?)\"', split_line[1])
                    if exe_path:
                        exe_path = exe_path[0].replace('\\\\', '\\')
                if "dependson" in line.lower():
                    depends_on = re.findall(r'\"(.+?)\"', split_line[1])
                    if depends_on:
                        depends_on = depends_on[0]
                if "launchcommand" in line.lower():
                    launch_command = re.findall(r'\"(.+?)\"', split_line[1])
                    if launch_command:
                        launch_command = launch_command[0]
            if game_id and game_name and launch_command:
                game_dict[game_name] = {'id': game_id, 'exe': exe_path}
                game_id = None
                game_name = None
                exe_path = None
                depends_on = None
                launch_command = None

    return game_dict



def adjust_dosbox_launch_options(launch_command, game_id):
    print(f"Adjusting launch options for command: {launch_command}")
    if "dosbox.exe" in launch_command.lower():
        try:
            # Find the part of the command with DOSBox.exe and its arguments
            exe_part, args_part = launch_command.split("DOSBox.exe", 1)
            exe_path = exe_part.strip() + "DOSBox.exe"
            args = args_part.strip()

            # Form the launch options string
            launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/" %command% /command=runGame /gameId={game_id} /path="{exe_path}" "{args}"'
            return launch_options
        except ValueError as e:
            print(f"Error adjusting launch options: {e}")
            return launch_command
    else:
        # For non-DOSBox games, return the original launch command without trailing spaces
        launch_command = launch_command.strip()
        return f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/" %command% /command=runGame /gameId={game_id} /path="{launch_command}"'

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
            # Adjust the launch options for DOSBox games
            launch_options = adjust_dosbox_launch_options(game_info['exe'], game_info['id'])

            # Format the paths correctly
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/\""

            # Create the new entry
            create_new_entry(exe_path, game, launch_options, start_dir)

# End of Gog Galaxy Scanner






#Battle.net Scanner

# Define your mapping
flavor_mapping = {
    "RTRO": "Blizzard Arcade Collection",
    "D1": "Diablo",
    "OSI": "Diablo II Resurrected",
    "D3": "Diablo III",
    "Fen": "Diablo IV",
    "ANBS": "Diablo Immortal (PC)",
    "WTCG": "Hearthstone",
    "Hero": "Heroes of the Storm",
    "Pro": "Overwatch 2",
    "S1": "StarCraft",
    "S2": "StarCraft 2",
    "W1": "Warcraft: Orcs & Humans",
    "W1R": "Warcraft I: Remastered",
    "W2": "Warcraft II: Battle.net Edition",
    "W2R": "Warcraft II: Remastered",
    "W3": "Warcraft III: Reforged",
    "WoW": "World of Warcraft",
    "WoWC": "World of Warcraft Classic",
    "GRY": "Warcraft Arclight Rumble",
    "ZEUS": "Call of Duty: Black Ops - Cold War",
    "VIPR": "Call of Duty: Black Ops 4",
    "ODIN": "Call of Duty: Modern Warfare",
    "AUKS": "Call of Duty",
    "LAZR": "Call of Duty: MW 2 Campaign Remastered",
    "FORE": "Call of Duty: Vanguard",
    "SPOT": "Call of Duty: Modern Warfare III",
    "WLBY": "Crash Bandicoot 4: It's About Time",
    # Add more games here...
}

def parse_battlenet_config(config_file_path):
    print(f"Opening Battle.net config file at: {config_file_path}")
    with open(config_file_path, 'r') as file:
        config_data = json.load(file)

    games_info = config_data.get("Games", {})
    game_dict = {}

    for game_key, game_data in games_info.items():
        print(f"Processing game: {game_key}")
        if game_key == "battle_net":
            print("Skipping 'battle_net' entry")
            continue
        if "Resumable" not in game_data:
            print(f"Skipping {game_key}, no 'Resumable' key found")
            continue
        if game_data["Resumable"] == "false":
            print(f"Game {game_key} is not resumable, adding to game_dict")
            game_dict[game_key] = {
                "ServerUid": game_data.get("ServerUid", ""),
                "LastActioned": game_data.get("LastActioned", "")
            }

    print(f"Parsed config data: {game_dict}")
    return game_dict


game_dict = {}

print("Detected platform: Non-Windows")
config_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/users/steamuser/AppData/Roaming/Battle.net/Battle.net.config"

print(f"Config file path: {config_file_path}")

if os.path.exists(config_file_path):
    print("Battle.net config file found, parsing...")
    game_dict = parse_battlenet_config(config_file_path)
else:
    print("Battle.net config file not found. Skipping Battle.net Games Scanner.")

if game_dict:
    for game_key, game_info in game_dict.items():
        print(f"Processing game: {game_key}")

        if game_key == "prometheus":
            print("Handling 'prometheus' as 'Pro'")
            game_key = "Pro"
        elif game_key == "fenris":
            print("Handling 'fenris' as 'Fen'")
            game_key = "Fen"

        game_name = flavor_mapping.get(game_key, "unknown")

        if game_name == "unknown":
            game_name = flavor_mapping.get(game_key.upper(), "unknown")
            print(f"Trying uppercase for {game_key}: {game_name}")
            if game_name == "unknown":
                print(f"Game {game_key} remains unknown, skipping...")
                continue

        matched_key = next((k for k, v in flavor_mapping.items() if v == game_name), game_key)
        print(f"Matched key for {game_key}: {matched_key}")

        if game_name == "Overwatch":
            game_name = "Overwatch 2"
            print(f"Renaming 'Overwatch' to 'Overwatch 2'")

        if game_info['ServerUid'] == "unknown":
            print(f"Skipping game {game_key} due to unknown ServerUid")
            continue

        exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net.exe"'
        start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/"'
        launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}" %command% --exec="launch {matched_key}" battlenet://{matched_key}'

        print(f"Creating new entry for {game_name} with exe_path: {exe_path}")
        create_new_entry(exe_path, game_name, launch_options, start_dir)

print("Battle.net Games Scanner completed.")

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
        launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{amazon_launcher}/\" %command% -'amazon-games://play/{game['id']}'"
        create_new_entry(exe_path, display_name, launch_options, start_dir)


#End of Amazon Games Scanner



# Itchio Scanner

# Set up the path to the Butler database
itch_db_location = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{itchio_launcher}/pfx/drive_c/users/steamuser/AppData/Roaming/itch/db/butler.db"

# Check if the database path exists
if not os.path.exists(itch_db_location):
    print(f"Path not found: {itch_db_location}. Aborting Itch.io scan...")
else:
    # Connect to the SQLite database
    conn = sqlite3.connect(itch_db_location)
    cursor = conn.cursor()

    # Fetch data from the 'caves' table
    cursor.execute("SELECT * FROM caves;")
    caves = cursor.fetchall()

    # Fetch data from the 'games' table
    cursor.execute("SELECT * FROM games;")
    games = cursor.fetchall()

    # Create a dictionary to store game information by game_id
    games_dict = {game[0]: game for game in games}

    # List to store final Itch.io game details
    itchgames = []

    # Match game_id between 'caves' and 'games' tables and collect relevant game details
    for cave in caves:
        game_id = cave[1]
        if game_id in games_dict:
            game_info = games_dict[game_id]
            cave_info = json.loads(cave[11])
            base_path = cave_info['basePath']
            candidates = cave_info.get('candidates', [])

            # Check if candidates exist and are not empty
            if candidates:
                executable_path = candidates[0].get('path', None)
                
                # If there's no valid executable path, skip this entry
                if not executable_path:
                    print(f"Skipping game (no executable found): {game_info[2]}")
                    continue

                # Skip games with an executable that ends with '.html' (browser games)
                if executable_path.endswith('.html'):
                    print(f"Skipping browser game: {game_info[2]}")
                    continue

                # Extract the game title
                game_title = game_info[2]

                # Append the game info (base path, executable path, game title) to the list
                itchgames.append((base_path, executable_path, game_title))
            else:
                print(f"Skipping game (no candidates): {game_info[2]}")

    # Process each game for creating new entries
    for base_path, executable, game_title in itchgames:
        base_path_linux = base_path.replace("C:\\", f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{itchio_launcher}/pfx/drive_c/").replace("\\", "/")
        exe_path = "\"" + os.path.join(base_path_linux, executable).replace("\\", "/") + "\""
        start_dir = "\"" + base_path_linux + "\""
        launchoptions = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{itchio_launcher}/\" %command%"

        # Call the provided function to create a new entry for the game
        create_new_entry(exe_path, game_title, launchoptions, start_dir)

    # Close the database connection
    conn.close()
    
# End of Itch.io Scanner



#Legacy Games Scanner
legacy_dir = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{legacy_launcher}/pfx/drive_c/Program Files/Legacy Games/"

if not os.path.exists(legacy_dir):
    print("Legacy directory not found. Skipping creation.")
else:
    user_reg_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{legacy_launcher}/pfx/user.reg"
    with open(user_reg_path, 'r') as file:
        user_reg = file.read()

    for game_dir in os.listdir(legacy_dir):
        if game_dir == "Legacy Games Launcher":
            continue

        print(f"Processing game directory: {game_dir}")

        if game_dir == "100 Doors Escape from School":
            app_info_path = f"{legacy_dir}/100 Doors Escape from School/100 Doors Escape From School_Data/app.info"
            exe_path = f"{legacy_dir}/100 Doors Escape from School/100 Doors Escape From School.exe"
        else:
            app_info_path = os.path.join(legacy_dir, game_dir, game_dir.replace(" ", "") + "_Data", "app.info")
            exe_path = os.path.join(legacy_dir, game_dir, game_dir.replace(" ", "") + ".exe")

        if os.path.exists(app_info_path):
            print("app.info file found.")
            with open(app_info_path, 'r') as file:
                lines = file.read().split('\n')
                game_name = lines[1].strip()
                print(f"Game Name: {game_name}")
        else:
            print("No app.info file found.")

        if os.path.exists(exe_path):
            game_exe_reg = re.search(r'\[Software\\\\Legacy Games\\\\' + re.escape(game_dir) + r'\].*?"GameExe"="([^"]*)"', user_reg, re.DOTALL | re.IGNORECASE)
            if game_exe_reg and game_exe_reg.group(1).lower() == os.path.basename(exe_path).lower():
                print(f"GameExe found in user.reg: {game_exe_reg.group(1)}")
                start_dir = f"{legacy_dir}{game_dir}"
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{legacy_launcher}\" %command%"
                create_new_entry(f'"{exe_path}"', game_name, launch_options, f'"{start_dir}"')
            else:
                print(f"No matching .exe file found for game: {game_dir}")
        else:
            print(f"No .exe file found for game: {game_dir}")

#End of the Legacy Games Scanner



#VKPlay Scanner

# Define paths

gamecenter_ini_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{vkplay_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.ini"
cache_folder_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{vkplay_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/Cache/GameDescription/"

# Check if the GameCenter.ini file exists
if not os.path.exists(gamecenter_ini_path):
    print(f"VK Play scanner skipped: {gamecenter_ini_path} does not exist.")
else:
    print(f"Found file: {gamecenter_ini_path}")
    config = configparser.ConfigParser()

    # Read the GameCenter.ini file
    try:
        with open(gamecenter_ini_path, 'r', encoding='utf-16') as file:
            config.read_file(file)
        print("File read successfully.")
    except Exception as e:
        print(f"Error reading the file: {e}")
        exit(1)

    # Collect game IDs from different sections
    game_ids = set()

    # Parse game IDs from the 'StartDownloadingGames' section
    if 'StartDownloadingGames' in config:
        downloaded_games = dict(config.items('StartDownloadingGames'))
        game_ids.update(downloaded_games.keys())

    # Parse game IDs from the 'FirstOpeningGameIds' section
    if 'FirstOpeningGameIds' in config:
        first_opening_game_ids = config['FirstOpeningGameIds'].get('FirstOpeningGameIds', '').split(';')
        game_ids.update(first_opening_game_ids)

    # Parse game IDs from the 'GamePersIds' section
    if 'GamePersIds' in config:
        for key in config['GamePersIds']:
            game_id = key.split('_')[0]
            game_ids.add(game_id)

    # Parse game IDs from the 'RunningGameClients' section
    if 'RunningGameClients' in config:
        running_game_clients = config['RunningGameClients'].get('RunningGameClients', '').split(';')
        game_ids.update(running_game_clients)

    # Parse game IDs from the 'LastAccessGames' section
    if 'LastAccessGames' in config:
        last_access_games = dict(config.items('LastAccessGames'))
        game_ids.update(last_access_games.keys())

    # Parse game IDs from the 'UndoList' section
    if 'UndoList' in config:
        for key in config['UndoList']:
            if 'vkplay://show' in config['UndoList'][key]:
                game_id = config['UndoList'][key].split('/')[1]
                game_ids.add(game_id)

    # Parse game IDs from the 'LeftBar' section
    if 'LeftBar' in config:
        left_bar_ids = config['LeftBar'].get('Ids', '').split(';')
        game_ids.update(left_bar_ids)

    # Parse game IDs from the 'Ad' section
    if 'Ad' in config:
        for key in config['Ad']:
            if 'IdMTLink' in key:
                game_id = key.split('0.')[1]
                game_ids.add(game_id)

    print("\nGame IDs found in GameCenter.ini file:")
    for game_id in game_ids:
        print(f"ID: {game_id}")

    # Handle the Cache folder
    if not os.path.exists(cache_folder_path):
        print(f"VK Play scanner skipped: Cache folder {cache_folder_path} does not exist.")
    else:
        print(f"Found Cache folder: {cache_folder_path}")
        all_files = os.listdir(cache_folder_path)
        valid_xml_files = []

        for file_name in all_files:
            if file_name.endswith(".json"):
                continue  # Skip JSON files
            file_path = os.path.join(cache_folder_path, file_name)
            try:
                tree = ET.parse(file_path)
                valid_xml_files.append(file_path)
            except ET.ParseError:
                continue  # Skip invalid XML files

        processed_game_ids = set()
        found_games = []

        for xml_file in valid_xml_files:
            try:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                game_item = root.find('GameItem')

                if game_item is not None:
                    game_id_xml = game_item.get('Name') or game_item.get('PackageName')

                    if game_id_xml:
                        game_id_in_ini = game_id_xml.replace('_', '.')

                        if game_id_in_ini in game_ids and game_id_in_ini not in processed_game_ids:
                            game_name = game_item.get('TitleEn', 'Unnamed Game')
                            found_games.append(f"{game_name} (ID: {game_id_in_ini})")
                            processed_game_ids.add(game_id_in_ini)
            except ET.ParseError:
                continue  # Skip invalid XML files

        if found_games:
            print("\nFound the following games:")
            for game in found_games:
                print(game)
        else:
            print("No games found.")

        for game_id in game_ids:
            game_name = 'Unknown Game'
            for xml_file in valid_xml_files:
                try:
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    game_item = root.find('GameItem')

                    if game_item is not None:
                        game_id_xml = game_item.get('Name') or game_item.get('PackageName')

                        if game_id_xml and game_id_xml.replace('_', '.') == game_id:
                            game_name = game_item.get('TitleEn', 'Unnamed Game')
                            break
                except ET.ParseError:
                    continue

            if game_name != 'Unknown Game':
                display_name = game_name
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{vkplay_launcher}/\" %command% 'vkplay://play/{game_id}'"
                exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{vkplay_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe\""
                start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{vkplay_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/\""

                create_new_entry(exe_path, display_name, launch_options, start_dir)

# End of VK Play Scanner


# HoYo Play Scanner
file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/users/steamuser/AppData/Roaming/Cognosphere/HYP/1_0/data/gamedata.dat"

# Check if the file exists
if not os.path.exists(file_path):
    print("Skipping HoYoPlay Scanner - File not found.")
else:
    # Read the file with ISO-8859-1 encoding
    with open(file_path, 'r', encoding='ISO-8859-1') as file:
        file_content = file.read()

    # Function to manually extract JSON-like objects by finding balanced braces
    def extract_json_objects(content):
        objects = []
        brace_count = 0
        json_start = None

        for i, char in enumerate(content):
            if char == '{':
                if brace_count == 0:
                    json_start = i  # Mark the start of a JSON object
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    json_object = content[json_start:i+1]  # Extract the full JSON object
                    objects.append(json_object)
                    json_start = None

        return objects

    # Extract JSON objects from the file content
    json_objects = extract_json_objects(file_content)

    # Create a set to track seen gameBiz values and avoid duplicates
    seen_game_biz = set()

    # Parse each JSON object
    for json_object in json_objects:
        json_object = json_object.strip()

        # Skip empty JSON objects
        if json_object == "{}":
            continue

        if json_object:
            try:
                # Attempt to load the JSON object
                data = json.loads(json_object)

                # Extract gameBiz from the root and from the 'gameInstallStatus' object
                game_biz = data.get("gameBiz", "").strip()

                # If gameBiz is empty, check inside the 'gameInstallStatus' object
                if not game_biz:
                    game_biz = data.get("gameInstallStatus", {}).get("gameBiz", "").strip()

                # Skip JSON objects where gameBiz is empty or already processed
                if not game_biz or game_biz in seen_game_biz:
                    continue  # Skip this object and move to the next one

                # Add this gameBiz to the seen set
                seen_game_biz.add(game_biz)

                # Extract other relevant fields
                persistent_install_path = data.get("persistentInstallPath", None)
                game_install_status = data.get("gameInstallStatus", {})

                game_exe_name = game_install_status.get("gameExeName", None)
                install_path = game_install_status.get("gameInstallPath", None)
                game_shortcut_name = data.get("gameShortcutName", None)  # Get the game shortcut name

                # Check if all important fields are missing or empty
                if not game_exe_name and not install_path and not persistent_install_path:
                    print(f"Skipping empty game entry for gameBiz: {game_biz}")
                    continue  # Skip if all important fields are empty

                if not persistent_install_path:
                    print(f"Skipping gameBiz: {game_biz} - No persistent install path found.")
                    continue  # Skip if no persistent install path

                if game_shortcut_name:
                    print(f"  Game Shortcut Name: {game_shortcut_name}")

                # Set the display name to the game shortcut name from the JSON
                display_name = game_shortcut_name if game_shortcut_name else game_biz
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/\" %command% \"--game={game_biz}\""
                exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/Program Files/HoYoPlay/launcher.exe\""
                start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/Program Files/HoYoPlay\""

                # Create the new entry (this is where you can use your custom function for Steam shortcuts)
                create_new_entry(exe_path, display_name, launch_options, start_dir)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                print(f"Problematic JSON content (first 200 chars): {json_object[:200]}")

# End of HoYoPlay Scanner

# Game Jolt Scanner

# File paths for both the game list and package details
games_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gamejolt_launcher}/pfx/drive_c/users/steamuser/AppData/Local/game-jolt-client/User Data/Default/games.wttf"
packages_file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gamejolt_launcher}/pfx/drive_c/users/steamuser/AppData/Local/game-jolt-client/User Data/Default/packages.wttf"

# Check if both files exist before proceeding
if not os.path.exists(games_file_path) or not os.path.exists(packages_file_path):
    print("One or both of the files do not exist. Skipping Game Jolt Scanner.")
else:
    try:
        # Load the games file
        with open(games_file_path, 'r') as f:
            games_data = json.load(f)

        # Load the packages file
        with open(packages_file_path, 'r') as f:
            packages_data = json.load(f)

        # Check if 'objects' exists in the games data
        if 'objects' in games_data:
            # Iterate through each game object in the games file
            for game_id, game_info in games_data['objects'].items():
                # Default values if information is missing
                description = 'No Description'
                install_dir = 'No Install Directory'
                version = 'No Version Info'
                executable_path = 'No Executable Path'

                # Iterate over the 'objects' in the packages file to find a match
                for package_id, package_info in packages_data.get('objects', {}).items():
                    # Check if the game_id in the package matches the current game_id
                    if package_info.get('game_id') == int(game_id):  # Match on game_id
                        # Extract information from the matched package
                        description = package_info.get('description', description)
                        install_dir = package_info.get('install_dir', install_dir)

                        # Safe extraction of version_number from 'release'
                        release_info = package_info.get('release', {})
                        version = release_info.get('version_number', version)

                        # Handle missing or empty launch options
                        if package_info.get('launch_options'):
                            executable_path = package_info['launch_options'][0].get('executable_path', executable_path)

                        break

                # Print the combined game info
                #print(f"\nGame ID: {game_id}")
                #print(f"Title: {game_info.get('title', 'No Title')}")
                #print(f"Install Directory: {install_dir}")
                #print("-" * 40)  # Separator line for clarity

                # Set the display name to the game shortcut name from the JSON
                display_name = game_info.get('title', 'No Title')
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gamejolt_launcher}/\" %command% --dir \"{install_dir}\" run"
                exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gamejolt_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameJoltClient/GameJoltClient.exe\""
                start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gamejolt_launcher}/pfx/drive_c/users/steamuser/AppData/Local/GameJoltClient\""

                # Create the new entry (this is where you can use your custom function for Steam shortcuts)
                create_new_entry(exe_path, display_name, launch_options, start_dir)

        else:
            print("'objects' key not found in the games data.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# End of Game Jolt Scanner



#Minecraft Legacy Launcher Scanner

# Path to the JSON file
file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{minecraft_launcher}/pfx/drive_c/users/deck/AppData/Roaming/.minecraft/launcher_settings.json"

# Function to convert Windows path to Unix path dynamically
def convert_to_unix_path(windows_path, home_dir):
    unix_path = windows_path.replace('\\', '/')

    if len(windows_path) > 2 and windows_path[1] == ":":
        unix_path = unix_path[2:]
        unix_path = os.path.join(home_dir, unix_path.lstrip('/'))

    return unix_path

# Check if the JSON file exists
if os.path.exists(file_path):
    try:
        with open(file_path, 'r') as file:
            # Parse the JSON data
            data = json.load(file)

            # Extract the productLibraryDir
            product_library_dir = data.get('productLibraryDir')

            if product_library_dir:
                home_dir = os.path.expanduser("~")
                unix_product_library_dir = convert_to_unix_path(product_library_dir, home_dir)

                # Define the target file path
                target_file = os.path.join(unix_product_library_dir, 'dungeons', 'dungeons', 'Dungeons.exe')

                # Check if the file exists
                if os.path.exists(target_file):
                    print(f"File exists: {target_file}")
                else:
                    print(f"File does not exist: {target_file}")

                # Set the display name to the game shortcut name from the JSON
                display_name = "Minecraft Dungeons"
                launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{minecraft_launcher}/\" %command%"
                exe_path = f"\"{target_file}\""
                start_dir = f"\"{os.path.dirname(target_file)}\""


                # Create the new entry (this is where you can use your custom function for Steam shortcuts)
                create_new_entry(exe_path, display_name, launch_options, start_dir)

            else:
                print("Key 'productLibraryDir' not found in the JSON.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
else:
    print("Skipping Minecraft Legacy Launcher Scanner")

# End of the Minecraft Legacy Launcher






# Only write back to the shortcuts.vdf and config.vdf files if new shortcuts were added or compattools changed
# Function to send a notification with an optional icon
def send_notification(message, icon_path=None, expire_time=5000):
    """Send a notification with the message and optional icon."""
    if icon_path and os.path.exists(icon_path):
        subprocess.run(['notify-send', '-a', 'NonSteamLaunchers', message, '--icon', icon_path, f'--expire-time={expire_time}'])
    else:
        subprocess.run(['notify-send', '-a', 'NonSteamLaunchers', message, f'--expire-time={expire_time}'])

# Only write back to the shortcuts.vdf and config.vdf files if new shortcuts were added or compattools changed
if new_shortcuts_added or shortcuts_updated:
    print(f"Saving new config and shortcuts files")

    # Serialize the config data to VDF
    conf = vdf.dumps(config_data, pretty=True)
    try:
        with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
            file.write(conf)
    except IOError as e:
        print(f"Error writing to config.vdf: {e}")

    # Write the updated shortcuts to the shortcuts.vdf file
    try:
        with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
            file.write(vdf.binary_dumps(shortcuts))
    except IOError as e:
        print(f"Error writing to shortcuts.vdf: {e}")

    # Now that the files are updated, show the created shortcuts in the notification
    if created_shortcuts:
        print("Created Shortcuts:")
        for name in created_shortcuts:
            print(name)

        # Prepare notifications with game names and icons
        notifications = []
        num_notifications = len(created_shortcuts)

        for i, name in enumerate(created_shortcuts):
            # Loop through all entries in the shortcuts dictionary
            found = False  # Flag to check if the name is found

            # Iterate through each shortcut entry
            for shortcut_key, shortcut_data in shortcuts['shortcuts'].items():
                if shortcut_data.get('appname') == name:
                    icon_path = shortcut_data.get('icon', None)
                    message = f"New game added! Restart Steam to apply: {name}"

                    # For 10 or fewer shortcuts, each will last 5 seconds
                    if num_notifications <= 4:
                        expire_time = 5000
                    else:
                        # For more than 10 shortcuts, start applying the gradient effect
                        expire_time = min(5000, 500 + (i * (5000 // num_notifications)))

                    notifications.append((message, icon_path, expire_time))
                    found = True
                    break

            # If the game wasn't found in the shortcuts, log a warning
            if not found:
                print(f"Warning: Game '{name}' not found in shortcuts dictionary.")

        # Send all notifications with dynamic expire times
        for message, icon_path, expire_time in notifications:
            send_notification(message, icon_path, expire_time)

print("All finished!")
