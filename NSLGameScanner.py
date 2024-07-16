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
from urllib.request import urlopen
from urllib.request import urlretrieve
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
psplusshortcutdirectory = os.environ.get('psplusshortcutdirectory')
vkplayshortcutdirectory = os.environ.get('vkplayshortcutdirectory')
hoyoplayshortcutdirectory = os.environ.get('hoyoplayshortcutfirectory')
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
decky_shortcuts = {}
gridp64 = ""
grid64 = ""
logo64 = ""
hero64 = ""


# Load the existing shortcuts
with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'rb') as file:
    shortcuts = vdf.binary_loads(file.read())
# Open the config.vdf file
with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'r') as file:
    config_data = vdf.load(file)


def get_sgdb_art(game_id, app_id):
    global grid64
    global gridp64
    global logo64
    global hero64
    print(f"Downloading icons artwork...")
    download_artwork(game_id, api_key, "icons", app_id)
    print(f"Downloading logos artwork...")
    logo64 = download_artwork(game_id, api_key, "logos", app_id)
    print(f"Downloading heroes artwork...")
    hero64 = download_artwork(game_id, api_key, "heroes", app_id)
    print("Downloading grids artwork of size 600x900...")
    gridp64 = download_artwork(game_id, api_key, "grids", app_id, "600x900")
    print("Downloading grids artwork of size 920x430...")
    grid64 =download_artwork(game_id, api_key, "grids", app_id, "920x430")



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
        with open(file_path, 'rb') as image_file:
            return b64encode(image_file.read()).decode('utf-8')

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
                return b64encode(response.content).decode('utf-8')
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
    if 'chrome' in launchoptions:
        return False
    elif str(app_id) in config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] = f'{compat_tool_name}'
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['config'] = ''
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['priority'] = '250'
        print(f"Updated CompatToolMapping entry for appid: {app_id}")
        return compat_tool_name
    else:
        config_data['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)] = {'name': f'{compat_tool_name}', 'config': '', 'priority': '250'}
        print(f"Created new CompatToolMapping entry for appid: {app_id}")
        return compat_tool_name

def check_if_shortcut_exists(shortcut_id, display_name, exe_path, start_dir, launch_options):
    # Check if the game already exists in the shortcuts using the id
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
#End of Code


#Start of Refactoring code from the .sh file
sys.path.insert(0, os.path.expanduser(f"{logged_in_home}/Downloads/NonSteamLaunchersInstallation/lib/python{python_version}/site-packages"))
print(sys.path)


# Create an empty dictionary to store the app IDs
app_ids = {}

def find_first_available_key(shortcuts):
    # Start from 0
    key = 0
    # While the key exists in the shortcuts, increment the key
    while str(key) in shortcuts:
        key += 1
    # Return the first available key
    return key

def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir):
    global new_shortcuts_added
    global shortcuts_updated
    global created_shortcuts
    global decky_shortcuts
    global grid64
    global gridp64
    global logo64
    global hero64


    # Check if the launcher is installed
    if not shortcutdirectory or not appname or not launchoptions or not startingdir:
        print(f"{appname} is not installed. Skipping.")
        return
    exe_path = f"{shortcutdirectory}"
    signed_shortcut_id = get_steam_shortcut_id(exe_path, appname)
    unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)
    # Only store the app ID for specific launchers
    if appname in ['Epic Games', 'Gog Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App', 'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client', 'Rockstar Games Launcher', 'Glyph', 'Playstation Plus', 'VK Play', 'HoYoPlay']:
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
    compatTool= add_compat_tool(unsigned_shortcut_id, launchoptions)
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
    decky_entry = {
        'appname': appname,
        'exe': exe_path,
        'StartDir': startingdir,
        'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
        'LaunchOptions': launchoptions,
        'CompatTool': compatTool,
        'WideGrid': grid64,
        'Grid': gridp64,
        'Hero': hero64,
        'Logo': logo64,
    }
    # Add the new entry to the shortcuts dictionary and add proton    # Find the first available key
    key = find_first_available_key(shortcuts['shortcuts'])
    # Use the key for the new entry
    shortcuts['shortcuts'][str(key)] = new_entry
    print(f"Added new entry for {appname} to shortcuts.")
    new_shortcuts_added = True
    created_shortcuts.append(appname)


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
create_new_entry(os.environ.get('psplusshortcutdirectory'), 'Playstation Plus', os.environ.get('pspluslaunchoptions'), os.environ.get('psplusstartingdir'))
create_new_entry(os.environ.get('vkplayshortcutdirectory'), 'VK Play', os.environ.get('vkplaylaunchoptions'), os.environ.get('vkplaystartingdir'))
create_new_entry(os.environ.get('hoyoplayshortcutdirectory'), 'HoYoPlay', os.environ.get('hoyoplaylaunchoptions'), os.environ.get('hoyoplaystartingdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Xbox Game Pass', os.environ.get('xboxchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'GeForce Now', os.environ.get('geforcechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Netflix', os.environ.get('netflixchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Hulu', os.environ.get('huluchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Disney+', os.environ.get('disneychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Prime Video', os.environ.get('amazonchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Youtube', os.environ.get('youtubechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Luna', os.environ.get('lunachromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Twitch', os.environ.get('twitchchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'movie-web', os.environ.get('moviewebchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Fortnite', os.environ.get('fortnitechromelaunchoptions'), os.environ.get('chrome_startdir'))



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




# Only write back to the shortcuts.vdf and config.vdf files if new shortcuts were added or compattools changed
if new_shortcuts_added or shortcuts_updated:
    print(f"Saving new config and shortcuts files")
    conf = vdf.dumps(config_data, pretty=True)
    try:
        with open(f"{logged_in_home}/.steam/root/config/config.vdf", 'w') as file:
            file.write(conf)
    except IOError as e:
        print(f"Error writing to config.vdf: {e}")
    try:
        with open(f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf", 'wb') as file:
            file.write(vdf.binary_dumps(shortcuts))
    except IOError as e:
        print(f"Error writing to shortcuts.vdf: {e}")

    # Print the created shortcuts
    if created_shortcuts:
        print("Created Shortcuts:")
        for name in created_shortcuts:
            print(name)

    # Create the path to the output file
    output_file_path = f"{logged_in_home}/.config/systemd/user/NSLGameScanner_output.log"
    # Open the output file in write mode
    try:
        with open(output_file_path, 'w') as output_file:
            for game in decky_shortcuts.values():
                # Skip if 'appname' or 'exe' is None
                if game.get('appname') is None or game.get('exe') is None:
                    continue

                # Create a dictionary to hold the shortcut information
                shortcut_info = {
                    'appname': game.get('appname'),
                    'exe': game.get('exe'),
                    'StartDir': game.get('StartDir'),
                    'icon': game.get('icon'),
                    'LaunchOptions': game.get('LaunchOptions'),
                    'CompatTool': game.get('CompatTool'),
                    'WideGrid': game.get('WideGrid'),
                    'Grid': game.get('Grid'),
                    'Hero': game.get('Hero'),
                    'Logo': game.get('Logo'),
                }

                # Print the shortcut information in JSON format
                message = json.dumps(shortcut_info)
                print(message, flush=True)  # Print to stdout

                # Print the shortcut information to the output file
                print(message, file=output_file, flush=True)
    except IOError as e:
        print(f"Error writing to output file: {e}")

print("All finished!")

