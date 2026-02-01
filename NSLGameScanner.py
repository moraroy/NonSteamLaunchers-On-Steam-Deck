#!/usr/bin/env python3
import os
import re
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
import certifi
import itertools
import shlex
import ssl
import socket
import base64
import http.client

from datetime import datetime
from base64 import b64encode

import xml.etree.ElementTree as ET

import urllib
import urllib.request
import urllib.error

from urllib.request import urlopen, urlretrieve
from urllib.parse import (
    urlparse,
    urlsplit,
    urlunsplit,
    quote
)




# Check the value of the DBUS_SESSION_BUS_ADDRESS environment variable
dbus_address = os.environ.get('DBUS_SESSION_BUS_ADDRESS')
if not dbus_address or not dbus_address.startswith('unix:path='):
    # Set the value of the DBUS_SESSION_BUS_ADDRESS environment variable
    dbus_address = f'unix:path=/run/user/{os.getuid()}/bus'
    os.environ['DBUS_SESSION_BUS_ADDRESS'] = dbus_address

# Path to the env_vars file
env_vars_path = f"{os.environ['HOME']}/.config/systemd/user/env_vars"
env_vars_dir = os.path.dirname(env_vars_path)

if not os.path.exists(env_vars_dir):
    os.makedirs(env_vars_dir)

# Check if the env_vars file exists
if not os.path.exists(env_vars_path):
    # If it doesn't exist, create it as an empty file
    with open(env_vars_path, 'w'):
        pass

print(f"Env vars file path is: {env_vars_path}")

# Read variables from the file
with open(env_vars_path, 'r') as f:
    lines = f.readlines()

separate_appids = None

for line in lines:
    if line.startswith('export '):
        line = line[7:]  # Remove 'export '

    # Parse the name and value
    if '=' in line:
        name, value = line.strip().split('=', 1)
        os.environ[name] = value

        # Track separate_appids if explicitly set to false
        if name == 'separate_appids' and value.strip().lower() == 'false':
            separate_appids = value.strip()





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
indie_launcher = os.environ.get('indie_launcher', '')
stove_launcher = os.environ.get('stove_launcher', '')
humble_launcher = os.environ.get('humble_launcher', '')
gryphlink_launcher = os.environ.get('gryphlink_launcher', '')


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
gryphlinkshortcutdirectory = os.environ.get('gryphlinkshortcutdirectory')

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
purpleshortcutdirectory = os.environ.get('purpleshortcutdirectory')
plariumshortcutdirectory = os.environ.get('plariumshortcutdirectory')
vfunshortcutdirectory = os.environ.get('vfunshortcutdirectory')
temposhortcutdirectory = os.environ.get('temposhortcutdirectory')
poketcgshortcutdirectory = os.environ.get('poketcgshortcutdirectory')
antstreamshortcutdirectory = os.environ.get('antstreamshortcutdirectory')
stoveshortcutdirectory = os.environ.get('stoveshortcutdirectory')
bigfishshortcutdirectory = os.environ.get('bigfishshortcutdirectory')

repaireaappshortcutdirectory = os.environ.get('repaireaappshortcutdirectory')
#Streaming
chromedirectory = os.environ.get('chromedirectory')
names_str = os.environ.get("custom_website_names_str", "")
websites_str = os.environ.get("custom_websites_str", "")
custom_names = [n.strip() for n in names_str.split(",") if n.strip()]
custom_websites = [w.strip() for w in websites_str.split(",") if w.strip()]
base_launch_options = os.environ.get("customchromelaunchoptions")





parent_folder = os.path.expanduser(f"{logged_in_home}/.config/systemd/user/Modules")

if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)

print(sys.path)

# Now import your modules after the single insert
import vdf



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
RestartSec=20
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
    #subprocess.run(['systemctl', '--user', 'start', 'nslgamescanner.service'])

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

    # Define the full path where artwork should be stored
    file_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{filename}"
    grid_folder_path = os.path.dirname(file_path)  # Get the parent directory (grid folder)

    # Ensure the grid folder exists
    if not os.path.exists(grid_folder_path):
        os.makedirs(grid_folder_path, exist_ok=True)  # Create grid folder if it doesn't exist
        print(f"Created grid folder at: {grid_folder_path}")

    # Check if the file already exists
    if file_exists_with_any_ext(file_path):
        print(f"Artwork for {art_type} already exists. Skipping download.")
        with open(file_path, 'rb') as image_file:
            return b64encode(image_file.read()).decode('utf-8')

    # If the artwork is not found locally, proceed with the download process
    if cache_key in api_cache:
        data = api_cache[cache_key]
    else:
        try:
            print(f"Game ID: {game_id}")
            url = f"{BASE_URL}/{art_type}/game/{game_id}"
            if dimensions:
                url += f"?dimensions={dimensions}"
            print(f"Request URL: {url}")

            with urllib.request.urlopen(url) as response:
                if response.status != 200:
                    raise Exception(f"Failed to fetch data, status code {response.status}")
                data = json.load(response)
            api_cache[cache_key] = data
        except (urllib.error.URLError, Exception) as e:
            print(f"Error making API call: {e}")
            api_cache[cache_key] = None
            return

    if not data or 'data' not in data:
        print(f"No data available for {game_id}. Skipping download.")
        return

    # If no local file and no cache, start downloading artwork
    for artwork in data['data']:
        image_url = artwork['thumb']
        print(f"Downloading image from: {image_url}")

        # Try both .png and .ico formats
        for ext in ['png', 'ico']:
            try:
                alt_file_path = file_path.replace('.png', f'.{ext}')
                # Use urllib to download the image
                with urllib.request.urlopen(image_url) as response:
                    if response.status == 200:
                        image_data = response.read()

                        # Save the image data to local file
                        with open(alt_file_path, 'wb') as file:
                            file.write(image_data)
                        print(f"Downloaded and saved {art_type} to: {alt_file_path}")

                        # Return base64 encoded image data
                        return b64encode(image_data).decode('utf-8')
            except (urllib.error.URLError, Exception) as e:
                print(f"Error downloading image in {ext}: {e}")

    print(f"Artwork download failed for {game_id}. Neither PNG nor ICO was available.")
    return None



def get_game_id(game_name):
    print(f"Searching for game ID for: {game_name}")
    try:
        encoded_game_name = urllib.parse.quote(game_name)
        url = f"{BASE_URL}/search/{encoded_game_name}"
        print(f"Encoded game name: {encoded_game_name}")
        print(f"Request URL: {url}")

        # Open the URL and get the response
        with urllib.request.urlopen(url) as response:
            # Manually check if the status code is 200
            if response.status == 200:
                data = json.load(response)
                if data.get('data'):
                    game_id = data['data'][0]['id']
                    print(f"Found game ID: {game_id}")
                    return game_id
                else:
                    print(f"No game ID found for game name: {game_name}")
            else:
                print(f"Error: Unexpected status code {response.status}")
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



steam_applist_cache = None


def get_steam_store_appid(steam_store_game_name):
    search_url = f"{BASE_URL}/search/{steam_store_game_name}"
    try:
        with urllib.request.urlopen(search_url) as response:
            data = json.load(response)
            if 'data' in data and data['data']:
                steam_store_appid = data['data'][0].get('steam_store_appid')
                if steam_store_appid:
                    print(f"Found App ID for {steam_store_game_name} via primary source: {steam_store_appid}")
                    return steam_store_appid
    except (urllib.error.URLError, Exception) as e:
        print(f"Primary store App ID lookup failed for {steam_store_game_name}: {e}")

    # Fallback using Steam AppList (cached)
    global steam_applist_cache
    if steam_applist_cache is None:
        steam_applist_cache = {}

    def normalize_name(name):
        name = name.lower()
        name = re.sub(r'[®™]', '', name)
        name = ' '.join(name.split())
        return name

    if steam_store_game_name not in steam_applist_cache:
        time.sleep(0.5)  # Small delay to avoid spamming Steam
        query = urllib.parse.quote(steam_store_game_name)
        url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.load(response)
        except (urllib.error.URLError, Exception) as e:
            print(f"Fallback Steam lookup failed for {steam_store_game_name}: {e}")
            return None

        target = normalize_name(steam_store_game_name)
        fallback_appid = None
        for item in data.get("items", []):
            if normalize_name(item.get("name", "")) == target:
                fallback_appid = str(item.get("id"))
                break

        steam_applist_cache[steam_store_game_name] = fallback_appid

    if steam_applist_cache[steam_store_game_name]:
        print(f"Found App ID for {steam_store_game_name} via fallback Steam search API: {steam_applist_cache[steam_store_game_name]}")
        return steam_applist_cache[steam_store_game_name]

    print(f"No App ID found for {steam_store_game_name} in fallback Steam search API.")
    return None



def create_steam_store_app_manifest_file(steam_store_appid, steam_store_game_name):
    steamapps_dir = f"{logged_in_home}/.steam/root/steamapps/"
    appmanifest_path = os.path.join(steamapps_dir, f"appmanifest_{steam_store_appid}.acf")

    os.makedirs(steamapps_dir, exist_ok=True)

    if os.path.exists(appmanifest_path):
        print(f"Manifest file for {steam_store_appid} already exists.")
        return

    vdf_content = "\n".join([
        '"AppState"',
        "{",
        f'\t"appid"\t\t"{steam_store_appid}"',
        '\t"Universe"\t\t"1"',
        f'\t"name"\t\t"{steam_store_game_name}"',
        '\t"StateFlags"\t\t"0"',
        f'\t"installdir"\t\t"{steam_store_game_name}"',
        '\t"LastUpdated"\t\t""',
        '\t"LastPlayed"\t\t""',
        '\t"SizeOnDisk"\t\t""',
        '\t"StagingSize"\t\t""',
        '\t"buildid"\t\t""',
        '\t"LastOwner"\t\t""',
        '\t"DownloadType"\t\t""',
        '\t"UpdateResult"\t\t""',
        '\t"BytesToDownload"\t\t""',
        '\t"BytesDownloaded"\t\t""',
        '\t"BytesToStage"\t\t""',
        '\t"BytesStaged"\t\t""',
        '\t"TargetBuildID"\t\t""',
        '\t"AutoUpdateBehavior"\t\t""',
        '\t"AllowOtherDownloadsWhileRunning"\t\t""',
        '\t"ScheduledAutoUpdate"\t\t""',
        "",
        '\t"InstalledDepots"',
        "\t{",
        "\t}",
        "",
        '\t"InstallScripts"',
        "\t{",
        "\t}",
        "",
        '\t"SharedDepots"',
        "\t{",
        "\t}",
        "",
        '\t"UserConfig"',
        "\t{",
        "\t}",
        "",
        '\t"MountedConfig"',
        "\t{",
        "\t}",
        "}",
        ""
    ])

    try:
        with open(appmanifest_path, 'w', encoding='utf-8') as file:
            file.write(vdf_content)
        print(f"Created appmanifest file at: {appmanifest_path}")
    except Exception as e:
        print(f"Failed to write manifest for '{steam_store_game_name}': {e}")





def get_steam_fallback_url(steam_store_appid, art_type):
    base_url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{steam_store_appid}/"

    candidates = []
    if art_type == "icons":
        candidates = [base_url + "icon.png", base_url + "icon.ico"]
    elif art_type == "logos":
        candidates = [base_url + "logo_2x.png", base_url + "logo.png"]
    elif art_type == "heroes":
        candidates = [base_url + "library_hero_2x.jpg", base_url + "library_hero.jpg"]
    elif art_type == "grids_600x900":
        candidates = [base_url + "library_600x900_2x.jpg", base_url + "library_600x900.jpg"]
    elif art_type == "grids_920x430":
        candidates = [base_url + "header_2x.jpg", base_url + "header.jpg"]
    else:
        return None

    for url in candidates:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return url
        except (urllib.error.URLError, Exception) as e:
            print(f"Error checking fallback URL: {url} — {e}")
            continue
    return None



def file_exists_with_any_ext(base_path):
    for ext in ['png', 'jpg', 'ico']:
        if os.path.exists(f"{base_path}.{ext}"):
            return True
    return False






def tag_artwork_files(shortcut_id, game_name, steamid3, logged_in_home):
    grid_dir = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid"
    base_name = str(shortcut_id)

    patterns = [
        f"{base_name}-icon",
        f"{base_name}_logo",
        f"{base_name}_hero",
        f"{base_name}p",
        f"{base_name}"
    ]

    found_files = []

    for pattern in patterns:
        for ext in ['png', 'jpg', 'ico']:
            file_path = os.path.join(grid_dir, f"{pattern}.{ext}")
            if os.path.exists(file_path):
                found_files.append(file_path)

    for file_path in found_files:
        try:
            # Check if file already has the correct tag
            result = subprocess.run(
                ['getfattr', '-n', 'user.xdg.tags', '--only-values', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True
            )

            existing_tags = result.stdout.strip().split(',') if result.returncode == 0 else []

            if game_name in existing_tags:
                print(f"Already tagged: {file_path}")
                continue

            subprocess.run(
                ['setfattr', '-n', 'user.xdg.tags', '-v', game_name, file_path],
                check=True
            )
            print(f"Tagged {file_path} with '{game_name}'")
        except subprocess.CalledProcessError as e:
            print(f"Failed to tag {file_path}: {e}")



def delete_old_artwork_by_tag(appname, shortcut_id, steamid3, logged_in_home):
    grid_path = os.path.join(logged_in_home, ".steam", "root", "userdata", str(steamid3), "config", "grid")

    try:
        for filename in os.listdir(grid_path):
            filepath = os.path.join(grid_path, filename)

            # Skip directories and .ico files
            if os.path.isdir(filepath) or filename.endswith(".ico"):
                continue

            # Skip any files tagged for the current shortcut ID
            if str(shortcut_id) in filename:
                continue

            try:
                result = subprocess.run(
                    ['getfattr', '-n', 'user.xdg.tags', '--only-values', filepath],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True
                )

                if result.returncode != 0:
                    continue  # No tag present

                tags = result.stdout.strip().split(',')

                if appname in tags:
                    os.remove(filepath)
                    print(f"Deleted old artwork tagged '{appname}': {filepath}")

            except Exception as e:
                print(f"Failed to process {filepath}: {e}")

    except FileNotFoundError:
        print(f"Grid path not found: {grid_path}")





#for local check
def file_tagged_with_appname(filepath, appname):
    try:
        result = subprocess.run(
            ['getfattr', '-n', 'user.xdg.tags', '--only-values', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        if result.returncode != 0:
            return False
        tags = result.stdout.strip().split(',')
        return appname in tags
    except Exception as e:
        print(f"Failed to get tags for {filepath}: {e}")
        return False





def scan_and_track_games(logged_in_home, steamid3):
    def normalize_appname(name):
        return name.strip().lower() if name else ""

    shortcuts_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/shortcuts.vdf"
    installed_apps_path = f"{logged_in_home}/.config/systemd/user/installedapps.json"

    current_scan = {}
    master_list = {}
    previous_master_list = {}

    def load_master_list():
        nonlocal master_list, previous_master_list
        if os.path.exists(installed_apps_path):
            try:
                with open(installed_apps_path, "r") as f:
                    master_list_raw = json.load(f)
                    if not isinstance(master_list_raw, dict):
                        raise ValueError("Expected dictionary.")
                    master_list = master_list_raw
                    previous_master_list = json.loads(json.dumps(master_list))  # deep copy
            except Exception as e:
                print(f"Failed to load master list: {e}")
                master_list = {}
                previous_master_list = {}
        else:
            master_list = {}
            previous_master_list = {}

    def track_game(appname, launcher):
        now = datetime.utcnow().isoformat() + "Z"
        if launcher not in current_scan:
            current_scan[launcher] = {}
        current_scan[launcher][appname] = {
            "first_seen": master_list.get(launcher, {}).get(appname, {}).get("first_seen", now),
            "last_seen": now,
            "still_installed": True
        }

    def load_shortcuts_appid_map():
        if not os.path.isfile(shortcuts_path):
            print("shortcuts.vdf not found!")
            return {}

        try:
            with open(shortcuts_path, "rb") as f:
                data = vdf.binary_load(f)

            shortcuts = data.get("shortcuts", data)
            appid_map = {}
            for key, entry in shortcuts.items():
                appname = entry.get("AppName") or entry.get("appname")
                appid = entry.get("appid") or entry.get("AppID")
                if appname and appid:
                    norm_name = normalize_appname(appname)
                    appid_map[norm_name] = appid
            return appid_map
        except Exception as e:
            print(f"Failed to load shortcuts.vdf: {e}")
            return {}

    def uninstall_removed_apps(removed_appnames, appid_map):
        for appname in removed_appnames:
            norm_name = normalize_appname(appname)
            appid = appid_map.get(norm_name)
            if appid:
                try:
                    subprocess.run(["steam", f"steam://uninstall/{appid}"], check=True)
                    print(f"Uninstall command sent for '{appname}' (AppID: {appid})")
                except subprocess.CalledProcessError:
                    print(f"Uninstall failed for '{appname}' (AppID: {appid})")
            else:
                print(f"AppID not found for '{appname}'")

    def finalize_game_tracking():
        now = datetime.utcnow().isoformat() + "Z"
        removed_apps = {}

        for launcher in list(master_list.keys()):
            if launcher not in current_scan:
                removed_apps[launcher] = list(master_list[launcher].keys())
                del master_list[launcher]
            else:
                for appname in list(master_list[launcher].keys()):
                    if appname not in current_scan[launcher]:
                        was_installed = previous_master_list.get(launcher, {}).get(appname, {}).get("still_installed", True)
                        if was_installed:
                            removed_apps.setdefault(launcher, []).append(appname)
                        master_list[launcher][appname]["still_installed"] = False
                        master_list[launcher][appname]["last_seen"] = now

        for launcher, games in current_scan.items():
            if launcher not in master_list:
                master_list[launcher] = {}
            master_list[launcher].update(games)

        # Remove volatile fields (like "last_seen") for comparison
        def cleaned(data):
            if isinstance(data, dict):
                return {k: cleaned(v) for k, v in data.items() if k != "last_seen"}
            elif isinstance(data, list):
                return [cleaned(i) for i in data]
            else:
                return data

        # Only write to file if the cleaned data has meaningful changes
        if cleaned(master_list) != cleaned(previous_master_list):
            os.makedirs(os.path.dirname(installed_apps_path), exist_ok=True)
            with open(installed_apps_path, "w") as f:
                json.dump(master_list, f, indent=4)
            print("Master list updated and saved.")
        else:
            print("No meaningful changes to master list. Skipping write.")

        if removed_apps:
            print(f"Removed apps: {removed_apps}")
            appid_map = load_shortcuts_appid_map()
            for launcher, apps in removed_apps.items():
                uninstall_removed_apps(apps, appid_map)
        else:
            print("No newly removed apps detected.")

        return removed_apps

    load_master_list()
    return track_game, finalize_game_tracking






#.desktop file logic
def create_exec_line_from_entry(logged_in_home, new_entry, m_gameid):
    try:
        appname = new_entry.get('appname')
        exe_path = new_entry.get('exe')  # full quoted command
        launch_options = new_entry.get('LaunchOptions')
        launcher_name = new_entry.get('Launcher')
        compattool = new_entry.get('CompatTool')

        print(f"Launch Options: {launch_options}")
        print(f"App Name: {appname}")
        print(f"Exe Path: {exe_path}")
        print(f"Launcher Name: {launcher_name}")
        print(f"Compat Tool: {compattool}")
        print(f"m_gameid: {m_gameid}")

        # Extract GOG/Epic/Origin/Amazon game_id
        game_id = None

        m = re.search(r'/gameId=(\d+)', launch_options)
        if m:
            game_id = m.group(1)
            print(f"Found GOG gameId: {game_id}")

            # Optional DOSBox / extra GOG args (quoted block after /path)
            extra_gog_args = None
            m = re.search(r'/path="[^"]+"\s+"([^"]+)"', launch_options)
            if m:
                extra_gog_args = m.group(1)
                print(f"desktopC: GOG Extra Args: {extra_gog_args}")

        if not game_id:
            m = re.search(r'com\.epicgames\.launcher://apps/([^/?&]+)', launch_options)
            if m:
                game_id = m.group(1)
                print(f"Found Epic gameId: {game_id}")

        if not game_id:
            m = re.search(r'amazon-games://play/([a-zA-Z0-9\-\.]+)', launch_options)
            if m:
                game_id = m.group(1)
                print(f"Found Amazon gameId: {game_id}")

        if not game_id:
            m = re.search(r'origin2://game/launch\?offerIds=([a-zA-Z0-9\-]+)', launch_options)
            if m:
                game_id = m.group(1)
                print(f"Found Origin gameId: {game_id}")

        # Ubisoft Connect
        if not game_id:
            m = re.search(r'uplay://launch/(\d+)', launch_options)
            if m:
                game_id = m.group(1)
                print(f"desktopC: Found Ubisoft gameId: {game_id}")



        if not game_id:
            print("No gameId found, skipping game ID-related steps.")
        else:
            print(f"Final game_id: {game_id}")

        # UMU GAMEID
        m = re.search(r'GAMEID="(\d+)"', launch_options)
        umugameid = m.group(1) if m else None
        print(f"UMU GameID: {umugameid}")

        # STEAM_COMPAT_DATA_PATH prefix
        compat_match = re.search(r'STEAM_COMPAT_DATA_PATH="([^"]+)"', launch_options)
        if not compat_match:
            print("ERROR: no STEAM_COMPAT_DATA_PATH")
            return None
        compat_data_prefix = os.path.basename(compat_match.group(1).rstrip("/"))
        print(f"Compat prefix: {compat_data_prefix}")


        dir_path = os.path.expanduser("~/.steam/root/compatibilitytools.d")
        pattern = re.compile(r"UMU-Proton-(\d+(?:\.\d+)*)(?:-(\d+(?:\.\d+)*))?")

        try:
            umu_folders = [
                (tuple(map(int, (m.group(1) + '.' + (m.group(2) or '0')).split('.'))), name)
                for name in os.listdir(dir_path)
                if (m := pattern.match(name)) and os.path.isdir(os.path.join(dir_path, name))
            ]
            if umu_folders:
                compat_tool_name = max(umu_folders)[1]  # Most recent version
                print(f"Found UMU Proton: {compat_tool_name}")
            else:
                print("No valid UMU Proton compatibility tool folders found.")
                compat_tool_name = None
        except Exception as e:
            print(f"Error reading UMU Proton folders: {e}")
            compat_tool_name = None

        if compat_tool_name:
            proton_path = os.path.join(logged_in_home, f".local/share/Steam/compatibilitytools.d/{compat_tool_name}")
        else:
            proton_path = f"{logged_in_home}/.local/share/Steam/compatibilitytools.d/{compattool}"

        print(f"Final Proton Path: {proton_path}")

        desktop_dir = os.path.join(logged_in_home, "Desktop")
        if not os.path.isdir(desktop_dir):
            print("Desktop not found")
            return None

        for filename in os.listdir(desktop_dir):
            if not filename.endswith(".desktop"):
                continue

            path = os.path.join(desktop_dir, filename)

            try:
                content = open(path).read()
            except:
                continue

            if f"steam://rungameid/{m_gameid}" not in content:
                continue

            print(f"Found .desktop: {path}")

            UMU = f"{logged_in_home}/bin/umu-run"

            tokens = shlex.split(exe_path)
            first = os.path.basename(tokens[0])

            if first == "umu-run":
                final_exe_path = exe_path
            else:
                # Prefix umu-run without quotes
                final_exe_path = f'{UMU} {exe_path}'

            # Remove quotes around umu-run only
            final_exe_path = re.sub(r'^"(/.*?umu-run)"', r'\1', final_exe_path)
            print(f"Final Exe Path: {final_exe_path}")

            env_vars = (
                f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{compat_data_prefix}/" '
                f'WINEPREFIX="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{compat_data_prefix}/pfx"'
            )

            if umugameid:
                env_vars += f' GAMEID={umugameid}'
                proton_path = f"{logged_in_home}/.local/share/Steam/compatibilitytools.d/{compat_tool_name}"
            else:
                proton_path = f"{logged_in_home}/.local/share/Steam/compatibilitytools.d/{compattool}"

            env_vars += f' PROTONPATH="{proton_path}"'
            print(f"Env Vars: {env_vars}")

            # Build runner command (GOG, UMU, Epic, Origin, Amazon)

            # Extract the path directly from the launch_options for gog only
            m = re.search(r'/path="([^"]+)"', launch_options)
            if m:
                gog_game_path = m.group(1)
                print(f"Extracted GOG Game Path: {gog_game_path}")
            else:
                gog_game_path = None
                print("ERROR: No game path found in launch_options")

            if "com.epicgames.launcher://" in launch_options:
                runner_cmd = f'{final_exe_path} -com.epicgames.launcher://apps/{game_id}?action=launch&silent=true'
            elif "origin2://" in launch_options:
                runner_cmd = f'{final_exe_path} origin2://game/launch?offerIds={game_id}'
            elif "amazon-games://" in launch_options:
                runner_cmd = f'{final_exe_path} -amazon-games://play/{game_id}'
            elif "uplay://" in launch_options and game_id:
                runner_cmd = f'{final_exe_path} uplay://launch/{game_id}/0'

            elif gog_game_path:
                runner_cmd = (
                    f'{final_exe_path} '
                    f'/command=runGame /gameId={game_id} '
                    f'/path="{gog_game_path}"'
                )
                if extra_gog_args:
                    runner_cmd += f' "{extra_gog_args}"'

            else:
                runner_cmd = f'{final_exe_path}'

            print(f"Runner Cmd: {runner_cmd}")

            exec_line = (
                f"Exec=sh -c '"
                f"if command -v kdialog >/dev/null; then "
                f"CHOICE=$(kdialog --yesno \"Standalone or with Steam?\" "
                f"--yes-label \"UMU + {launcher_name}\" --no-label \"Steam\"); "
                f"exit_code=$?; "
                f"if [ $exit_code -eq 2 ]; then exit 0; fi; "
                f"if [ $exit_code -eq 0 ]; then "
                f"CHOICE={launcher_name.lower()}; "
                f"elif [ $exit_code -eq 1 ]; then "
                f"CHOICE=steam; "
                f"fi; "
                f"else CHOICE=steam; fi; "
                f"if [ \"$CHOICE\" = \"steam\" ]; then steam steam://rungameid/{m_gameid}; "
                f"else \"pkill -9 -f wineserver\"; {env_vars} {runner_cmd}; fi'"
            )



            print("Updated Exec line:")
            print(exec_line)


            content = content.replace(f"Exec=steam steam://rungameid/{m_gameid}", exec_line)

            # Update the comment line
            content = content.replace("Comment=Play this game on Steam", "Comment=Play this game on Steam or Standalone")



            applications_dir = os.path.join(logged_in_home, ".local/share/applications/")
            if not os.path.exists(applications_dir):
                os.makedirs(applications_dir)


            # Delete broken or Desktop-pointing symlinks in applications folder
            # Delete broken symlinks in applications folder
            for f in os.listdir(applications_dir):
                full_path = os.path.join(applications_dir, f)
                if f.endswith(".desktop") and os.path.islink(full_path):
                    target = os.readlink(full_path)
                    # Resolve relative symlinks
                    real_target = os.path.join(os.path.dirname(full_path), target)
                    if not os.path.exists(real_target):
                        print(f"Deleting broken symlink in applications folder: {full_path} -> {target}")
                        os.remove(full_path)


            app_file_path = os.path.join(applications_dir, filename)

            with open(app_file_path, "w") as file:
                file.write(content)
            print(f"Moved and updated .desktop file in {app_file_path}")

            original_desktop_path = os.path.join(desktop_dir, filename)
            if os.path.exists(original_desktop_path):
                os.remove(original_desktop_path)

            os.symlink(app_file_path, original_desktop_path)
            print(f"Created symlink {original_desktop_path} -> {app_file_path}")


        print("No matching .desktop file")
        return None

    except Exception as e:
        print(f"Error creating Exec line: {e}")
        return None
#End of .desktop file logic



def check_if_shortcut_exists(display_name, exe_path, start_dir, launch_options):
    stripped_exe_path = exe_path.strip('\"') if exe_path else exe_path
    stripped_start_dir = start_dir.strip('\"') if start_dir else start_dir

    for s in shortcuts['shortcuts'].values():
        # Non-Chrome shortcut check: We remove the launch options comparison for non-Chrome shortcuts
        if (s.get('appname') == display_name or s.get('AppName') == display_name) and \
           ((s.get('exe') and s.get('exe').strip('\"') == stripped_exe_path) or (s.get('Exe') and s.get('Exe').strip('\"') == stripped_exe_path)) and \
           s.get('StartDir') and s.get('StartDir').strip('\"') == stripped_start_dir:

            # Check if the launch options are different (for non-Chrome, no comparison is done, so add a warning here)
            if s.get('LaunchOptions') != launch_options:
                print(f"Launch options for {display_name} differ from the default. This could be due to the user manually modifying the launch options. Will skip creation")

            print(f"Existing shortcut found for game {display_name}. Skipping creation.")
            return True

        # Chrome (website) shortcut check
        if (s.get('appname') == display_name or s.get('AppName') == display_name) and \
           (s.get('exe') and s.get('exe').strip('\"') == '/app/bin/chrome') and \
           s.get('LaunchOptions') and launch_options in s.get('LaunchOptions'):
            print(f"Existing website shortcut found for {display_name}. Skipping creation.")
            return True

    return False


# Start of Refactoring code from the .sh file
#sys.path.insert(0, os.path.expanduser(f"{logged_in_home}/Downloads/NonSteamLaunchersInstallation/lib/python{python_version}/site-packages"))
#print(sys.path)

track_game, finalize_tracking = scan_and_track_games(logged_in_home, steamid3)





# === CONFIGURATION ===
WS_HOST = "localhost"
WS_PORT = 8080
TARGET_TITLE = "SharedJSContext"
TARGET_TITLE2 = "Steam"
TARGET_TITLE3 = "Steam Big Picture Mode"



JS_CODE = """
// Create shared audio context once
window._sharedAudioCtx ??= new (window.AudioContext || window.webkitAudioContext)();
const ctx = window._sharedAudioCtx;

// Play a soft notification tone
function playTone({ type = 'sine', frequency = 440, volume = 0.1, duration = 1, startTime = null }) {
  const now = ctx.currentTime;
  const start = startTime ?? now;
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();

  osc.type = type;
  osc.frequency.setValueAtTime(frequency, start);

  gain.gain.setValueAtTime(volume, start);
  gain.gain.exponentialRampToValueAtTime(0.0005, start + duration);

  osc.connect(gain);
  gain.connect(ctx.destination);

  osc.start(start);
  osc.stop(start + duration);

  osc.onended = () => {
    osc.disconnect();
    gain.disconnect();
  };
}

function detectImageFormat(base64String) {
  if (base64String.startsWith("iVBORw0KGgo")) return "png";  // PNG
  if (base64String.startsWith("/9j/")) return "jpg";          // JPG
  if (base64String.startsWith("AAABAAEAEBA")) return "ico";   // ICO
  return "png"; // fallback
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

window.createShortcut = async function(data) {
  console.log("createShortcut called with", data);

  if (typeof SteamClient === 'undefined' || !SteamClient.Apps) {
    console.error("SteamClient API is unavailable.");
    return { success: false, message: "SteamClient API is unavailable." };
  }

  let shortcutId;

  try {
    // --- Always create new shortcut ---
    shortcutId = await SteamClient.Apps.AddShortcut(
      data.appname,
      data.exe,
      data.StartDir,
      data.LaunchOptions || ""
    );
    console.log("Shortcut created with ID:", shortcutId);

    // --- Set properties ---
    if (data.icon) {
      await SteamClient.Apps.SetShortcutIcon(shortcutId, data.icon);
      console.log("Icon set successfully!");
    }

    await SteamClient.Apps.SetShortcutName(shortcutId, data.appname);
    await SteamClient.Apps.SetShortcutExe(shortcutId, data.exe);
    await SteamClient.Apps.SetShortcutStartDir(shortcutId, data.StartDir);
    await SteamClient.Apps.SetAppLaunchOptions(shortcutId, data.LaunchOptions || "");
    console.log("Shortcut properties updated.");

    // --- Set 'Sort As' title ---
    if (data.Launcher && typeof data.Launcher === "string" && data.Launcher.trim()) {
    const sortName = `${data.appname} ${data.Launcher.trim()}`;
    await SteamClient.Apps.SetShortcutSortAs(shortcutId, sortName);
    console.log("Sort As title set to:", sortName);
    }

    // --- Set Compatibility Tool ---
    if (data.CompatTool && data.CompatTool.trim()) {
      const compatTool = data.CompatTool.trim();
      const availableTools = await SteamClient.Apps.GetAvailableCompatTools(shortcutId);
      const toolExists = availableTools.some(tool => tool.strToolName === compatTool);

      if (toolExists) {
        await SteamClient.Apps.SpecifyCompatTool(shortcutId, compatTool);
        console.log("Compat tool set to " + compatTool);
      } else {
        console.warn("Compat tool '" + compatTool + "' not found. Falling back to 'proton_experimental'.");
        await SteamClient.Apps.SpecifyCompatTool(shortcutId, 'proton_experimental');
      }
    }

    // --- Set custom artwork ---
    const artworks = [
      { key: "Hero", type: 1 },
      { key: "Logo", type: 2 },
      { key: "Grid", type: 0 },
      { key: "WideGrid", type: 3 },
    ];

    for (const art of artworks) {
      if (data[art.key]) {
        const format = detectImageFormat(data[art.key]);
        await SteamClient.Apps.SetCustomArtworkForApp(shortcutId, data[art.key], format, art.type);
        console.log(`${art.key} artwork set as ${format}`);
      }
    }

    // --- Add to collection ---
    if (data.Launcher && typeof data.Launcher === "string" && data.Launcher.trim()) {
      const tag = data.Launcher.trim();
      const appId = shortcutId;

      const collectionStore = window.g_CollectionStore || window.collectionStore;
      if (!collectionStore) {
        console.error("No collection store found.");
      } else {
        const existingCollectionId = collectionStore.GetCollectionIDByUserTag(tag);
        let collection;

        if (existingCollectionId) {
          collection = collectionStore.GetCollection(existingCollectionId);
          console.log("Using existing collection:", tag);
        } else {
          collection = collectionStore.NewUnsavedCollection(tag, undefined, []);
          if (collection) {
            await collection.Save();
            console.log("Created new collection:", tag);
          } else {
            console.error("Failed to create collection:", tag);
          }
        }

        if (collection && !collection.m_setApps.has(appId)) {
          collection.m_setApps.add(appId);
          collection.m_setAddedManually.add(appId);
          await collection.Save();
          console.log("Added app", appId, "to collection:", tag);
        } else {
          console.log("App already in collection or collection creation failed.");
        }
      }
    }

    if (data.appname !== "NonSteamLaunchers") {
      await SteamClient.Apps.CreateDesktopShortcutForApp(shortcutId);
      console.log("Desktop shortcut created for shortcut:", shortcutId);
    } else {
      const collectionStoreRef = window.g_CollectionStore || window.collectionStore;
      if (collectionStoreRef) {
        collectionStoreRef.SetAppsAsHidden([shortcutId], true);
        console.log("Shortcut 'NonSteamLaunchers' has been hidden instead of creating desktop shortcut.");
      } else {
        console.warn("Collection store not available. Cannot hide 'NonSteamLaunchers'.");
      }
    }

    const appDetails = appStore.m_mapApps.get(shortcutId);
    let m_gameid = null;

    if (appDetails) {
      m_gameid = appDetails.m_gameid;
      console.log("Found m_gameid:", m_gameid);
    } else {
      console.warn("No app details found in appStore for shortcutId:", shortcutId);
    }

    // --- Notification ---
    try {
      await sleep(300);

      // Play your custom soft notification sound here:
      playTone({ type: 'sine', frequency: 520, volume: 0.12, duration: 1.5 });
      playTone({ type: 'sine', frequency: 660, volume: 0.06, duration: 0.8, startTime: ctx.currentTime + 0.1 });

      const notificationPayload = {
        rawbody: data.appname + " was added to your library!",
        state: "ingame",
        steamid: "",
      };

      if (window.SteamClient && SteamClient.ClientNotifications) {
        SteamClient.ClientNotifications.DisplayClientNotification(3, JSON.stringify(notificationPayload), function(arg) {
          console.log("Notification callback", arg);
        });
      } else {
        console.warn("ClientNotifications API not available.");
      }
    } catch (notifyErr) {
      console.warn("Failed to send notification:", notifyErr);
    }

    if (m_gameid !== null) {
      return { success: true, shortcutId, m_gameid };
    }

    return { success: false, message: "App details not found in appStore." };

  } catch (e) {
    console.error("Failed to create shortcut:", e);

    if (typeof shortcutId === "number") {
      try {
        await SteamClient.Apps.RemoveShortcut(shortcutId);
        console.log("Removed partially created shortcut:", shortcutId);
      } catch (removeErr) {
        console.warn("Failed to remove shortcut after creation failure:", removeErr);
      }
    }

    return { success: false, message: e.message || e.toString() };
  }
};
"""


PLAYTIME_CODE = """
const STORAGE_KEY = "realPlaytimeData";

let memoryCache = null;
const appliedSessions = {};

function isValidPlaytimeDataEntry(entry) {
    return (
        typeof entry === "object" &&
        entry !== null &&
        typeof entry.total === "number" &&
        typeof entry.lastSessionEnd === "number"
    );
}

function sanitizePlaytimeData(data) {
    if (typeof data !== "object" || data === null) return {};
    const cleaned = {};
    for (const key in data) {
        if (isValidPlaytimeDataEntry(data[key])) {
            cleaned[key] = data[key];
        }
    }
    return cleaned;
}

function loadPlaytimeData() {
    try {
        if (memoryCache) return memoryCache;
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
            memoryCache = {};
            return memoryCache;
        }
        const parsed = JSON.parse(raw);
        const cleaned = sanitizePlaytimeData(parsed);
        if (Object.keys(cleaned).length !== Object.keys(parsed || {}).length) {
            savePlaytimeData(cleaned);
        }
        memoryCache = cleaned;
        return memoryCache;
    } catch {
        memoryCache = {};
        return memoryCache;
    }
}

function savePlaytimeData(data) {
    try {
        const latestFromStorage = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
        const merged = { ...latestFromStorage, ...data };
        memoryCache = merged;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(merged));
    } catch {
        memoryCache = data;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
}

function isEnvironmentReady() {
    try {
        localStorage.setItem("__rp_test__", "1");
        localStorage.removeItem("__rp_test__");
        if (!window.appStore || typeof window.appStore.GetAppOverviewByAppID !== "function") return false;
        if (!window.appInfoStore) return false;
        return true;
    } catch {
        return false;
    }
}

function restoreSavedPlaytimes() {
    const data = loadPlaytimeData();
    if (!window.appStore?.GetAppOverviewByAppID) return;

    let removedCount = 0;
    for (const id in data) {
        const entry = data[id];
        const ov = appStore.GetAppOverviewByAppID(Number(id));
        if (ov) {
            ov.minutes_playtime_forever = Math.max(ov.minutes_playtime_forever || 0, entry.total);
            ov.minutes_playtime_last_two_weeks = Math.max(ov.minutes_playtime_last_two_weeks || 0, entry.total);
            ov.nPlaytimeForever = Math.max(ov.nPlaytimeForever || 0, entry.total);
            ov.TriggerChange?.();
        } else {
            delete data[id];
            removedCount++;
        }
    }
    if (removedCount > 0) savePlaytimeData(data);
}

function applyRealSessionToOverview(appOverview) {
    try {
        if (!appOverview || appOverview.app_type !== 1073741824) return false;

        const start = appOverview.rt_last_time_played;
        const end = appOverview.rt_last_time_locally_played;
        if (!start || !end || end <= start) return false;

        const appId = String(appOverview.appid || (typeof appOverview.appid === "function" ? appOverview.appid() : appOverview.appId));
        const sessionSeconds = end - start;
        const sessionMinutes = Math.floor(sessionSeconds / 60);
        if (sessionMinutes <= 0) return false;

        const data = loadPlaytimeData();
        const prevEntry = data[appId] || { total: 0, lastSessionEnd: 0 };

        const effectiveEnd = Math.max(prevEntry.lastSessionEnd, end);
        const addedMinutes = effectiveEnd > prevEntry.lastSessionEnd ? sessionMinutes : 0;
        const newTotal = prevEntry.total + addedMinutes;
        if (newTotal === prevEntry.total) return false;

        data[appId] = { total: newTotal, lastSessionEnd: effectiveEnd };
        savePlaytimeData(data);
        appliedSessions[appId] = effectiveEnd;

        appOverview.minutes_playtime_forever = newTotal;
        appOverview.minutes_playtime_last_two_weeks = newTotal;
        appOverview.nPlaytimeForever = newTotal;
        appOverview.TriggerChange?.();

        return true;
    } catch {
        return false;
    }
}

function patchAppStore() {
    if (!window.appStore?.m_mapApps) return;
    if (appStore.m_mapApps._originalSet) return;

    appStore.m_mapApps._originalSet = appStore.m_mapApps.set;
    appStore.m_mapApps.set = function(appId, appOverview) {
        const result = appStore.m_mapApps._originalSet.call(this, appId, appOverview);
        restoreSavedPlaytimes();
        applyRealSessionToOverview(appOverview);
        return result;
    };
}

function patchAppInfoStore() {
    if (!window.appInfoStore) return;
    if (appInfoStore._originalOnAppOverviewChange) return;

    appInfoStore._originalOnAppOverviewChange = appInfoStore.OnAppOverviewChange;
    appInfoStore.OnAppOverviewChange = function(apps) {
        for (const a of apps || []) {
            const id = typeof a?.appid === "function" ? a.appid() : a?.appid;
            const overview = id && appStore?.GetAppOverviewByAppID ? appStore.GetAppOverviewByAppID(Number(id)) : a;
            if (overview) {
                restoreSavedPlaytimes();
                applyRealSessionToOverview(overview);
            }
        }
        return appInfoStore._originalOnAppOverviewChange.call(this, apps);
    };
}

function manualPatch() {
    try {
        const m = location.pathname.match(/\\/library\\/app\\/(\\d+)/);
        if (m) {
            const id = Number(m[1]);
            const ov = appStore.GetAppOverviewByAppID(id);
            if (ov) {
                restoreSavedPlaytimes();
                applyRealSessionToOverview(ov);
                appInfoStore?.OnAppOverviewChange?.([ov]);
            }
        }
    } catch {}
}

(function initRealPlaytime(retryCount = 0) {
    if (!isEnvironmentReady()) {
        if (retryCount < 100) {
            setTimeout(() => initRealPlaytime(retryCount + 1), 1000);
        }
        return;
    }
    try {
        setTimeout(() => {
            restoreSavedPlaytimes();
            patchAppStore();
            patchAppInfoStore();
            manualPatch();
        }, 100);
    } catch {}
})();
"""



THEMEMUSIC_CODE = r"""(function () {
  const LOCAL_STORAGE_KEY = "ThemeMusicData";

  const themeMusicEvents = new EventTarget();
  const originalSetItem = localStorage.setItem.bind(localStorage);

  localStorage.setItem = function (key, value) {
    originalSetItem(key, value);
    if (key === LOCAL_STORAGE_KEY) {
      let enabled = true;
      try {
        const data = JSON.parse(value || "{}");
        enabled = !(data.themeMusic === false || data.themeMusic === "off");
      } catch {}
      themeMusicEvents.dispatchEvent(new CustomEvent("themeMusicToggle", { detail: { enabled } }));
    }
  };

  themeMusicEvents.addEventListener("themeMusicToggle", (e) => {
      console.log("Theme music toggled (same tab):", e.detail.enabled);
      if (!e.detail.enabled && ytPlayer) {
          // Stop the music first
          fadeOutAndStop().then(() => {
              // Clear the currently playing music data after it has stopped
              clearCurrentlyPlaying();
          });
      }
  });


  // Listen to changes from other tabs
  window.addEventListener("storage", (e) => {
    if (e.key === LOCAL_STORAGE_KEY) {
      let enabled = true;
      try {
        const data = JSON.parse(e.newValue || "{}");
        enabled = !(data.themeMusic === false || data.themeMusic === "off");
      } catch {}
      console.log("Theme music toggled (other tab):", enabled);
      if (!enabled && ytPlayer) fadeOutAndStop();
    }
  });

  function isThemeMusicEnabled() {
    try {
      const data = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}");
      return !(data.themeMusic === false || data.themeMusic === "off");
    } catch {
      return false; // default off
    }
  }

  let stoppingMusic = false;
  let pausedForGame = false;

  if (window.SteamClient && SteamClient.Apps && SteamClient.Apps.RegisterForGameActionStart) {
    SteamClient.Apps.RegisterForGameActionStart((appID) => {
      if (stoppingMusic) return;
      stoppingMusic = true;

      console.log("Play clicked! Game starting… AppID:", appID);

      fadeOutAndStop().finally(() => { stoppingMusic = false; });

      var mgr = window.MainWindowBrowserManager;
      if (mgr) mgr.LoadURL("/library");
    });
  }

  var mgr = window.MainWindowBrowserManager;
  if (!mgr) return;

  var lastUrl = null;
  var lastAppID = null;

  var ytAudioIframe = null;
  var ytPlayer = null;
  var ytPlayerReady = false;
  var fadeInterval = null;
  var currentQuery = null;

  var sessionCache = new Map();
  const CACHE_EXPIRATION = 7 * 24 * 60 * 60 * 1000;

  if (!window.YT) {
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    document.head.appendChild(tag);
  }

  function waitForYouTubeAPI() {
    if (window.YT && window.YT.Player) return Promise.resolve();
    return new Promise(function (resolve) {
      window.onYouTubeIframeAPIReady = function () { resolve(); };
    });
  }

  function loadCache() {
    try { return JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}"); }
    catch { return {}; }
  }

  function saveCache(data) {
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(data));
  }

  function getCachedVideo(query) {
      // First, check if there's a cached video ID in the session cache
      if (sessionCache.has(query)) {
          // Retrieve the session cache entry
          const sessionEntry = sessionCache.get(query);
          const cache = loadCache();  // Load the localStorage cache
          const localStorageEntry = cache[query];

          if (localStorageEntry && localStorageEntry.timestamp > sessionEntry.timestamp) {
              // If the timestamp in localStorage is newer, use the localStorage entry
              sessionCache.set(query, localStorageEntry);  // Update the session cache with the newer entry
              return localStorageEntry.videoId;
          }

          // If session cache is newer or no localStorage entry, return session cache ID
          return sessionEntry.videoId;
      }

      // If no session cache, check the localStorage cache
      var cache = loadCache();
      var entry = cache[query];
      if (!entry) return null;

      // If the entry exists in localStorage and it's not expired, use it
      sessionCache.set(query, entry);  // Store the localStorage entry in session cache
      return entry.videoId;
  }


  function storeCachedVideo(query, videoId) {
    var cache = loadCache();
    const entry = { videoId: videoId, timestamp: Date.now() };

    cache[query] = entry;
    saveCache(cache);


    sessionCache.set(query, entry);
  }

  function fadeOutAndStop() {
    return new Promise(function (resolve) {
      if (!ytPlayer) return resolve();
      pausedForGame = true;
      var volume = 100;
      clearInterval(fadeInterval);
      fadeInterval = setInterval(function () {
        if (!ytPlayer) return cleanup();
        volume = Math.max(0, volume - 10);
        if (ytPlayer.setVolume) ytPlayer.setVolume(volume);
        if (volume <= 0) cleanup();
      }, 50);

      function cleanup() {
        clearInterval(fadeInterval);
        fadeInterval = null;
        try { ytPlayer.stopVideo && ytPlayer.stopVideo(); ytPlayer.destroy && ytPlayer.destroy(); } catch (e) {}
        ytAudioIframe && ytAudioIframe.remove();
        ytAudioIframe = null;
        ytPlayer = null;
        ytPlayerReady = false;
        currentQuery = null;
        setTimeout(() => { pausedForGame = false; }, 2000);

        resolve();
      }
    });
  }

  function createYTPlayer(videoId) {
    if (!isThemeMusicEnabled()) return Promise.resolve();
    return waitForYouTubeAPI().then(function () {
      ytAudioIframe && ytAudioIframe.remove();
      ytAudioIframe = document.createElement("div");
      ytAudioIframe.id = "yt-audio-player";
      Object.assign(ytAudioIframe.style, { width: "0", height: "0", position: "absolute", opacity: "0", pointerEvents: "none" });
      document.body.appendChild(ytAudioIframe);
      ytPlayerReady = false;
      ytPlayer = new YT.Player("yt-audio-player", {
        height: "0",
        width: "0",
        videoId: videoId,
        playerVars: { autoplay: 1 },
        events: {
          onReady: function () { ytPlayerReady = true; ytPlayer.setVolume && ytPlayer.setVolume(100); },
          onError: function () { fadeOutAndStop(); }
        }
      });
    });
  }




  function updateCurrentlyPlaying(query, videoId) {
      try {
          const themeData = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}");
          themeData.currentlyPlaying = {
              name: query,
              videoId: videoId || "loading",  // Temporary placeholder while loading
              timestamp: Date.now()
          };
          localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(themeData));

          // Dispatch an event to notify the update
          themeMusicEvents.dispatchEvent(new CustomEvent("currentlyPlayingUpdated", {
              detail: { name: query, videoId: videoId }
          }));
      } catch (e) {
          console.error("Error updating currentlyPlaying:", e);
      }
  }

  function playYouTubeAudio(query) {
      if (!isThemeMusicEnabled()) return;
      if (query === currentQuery) return;
      currentQuery = query;

      // Update "currentlyPlaying" state in localStorage immediately
      updateCurrentlyPlaying(query, "loading"); // Temporary placeholder for the videoId

      // Stop current track
      return fadeOutAndStop().then(function () {
          var cachedId = getCachedVideo(query);
          if (cachedId) {
              updateCurrentlyPlaying(query, cachedId);
              return createYTPlayer(cachedId);
          }

          // Fetch new track from API
          return fetch("https://nonsteamlaunchers.onrender.com/api/x7a9/" + encodeURIComponent(query))
              .then(function (res) { return res.json(); })
              .then(function (data) {
                  if (!data || !data.videoId) return;

                  // Cache the track
                  storeCachedVideo(query, data.videoId);

                  // Update "currentlyPlaying" state with the actual videoId
                  updateCurrentlyPlaying(query, data.videoId);

                  return createYTPlayer(data.videoId);
               })
               .catch(function () {
                   console.error("Theme music fetch failed");
                   updateCurrentlyPlaying(query, null); // optional: clear 'loading' state on error
               });
       });
  }

  // Handle the event when "currentlyPlaying" changes
  themeMusicEvents.addEventListener("currentlyPlayingUpdated", (e) => {
      const { name, videoId } = e.detail;
      console.log("Currently Playing:", name, videoId);
      // You can trigger UI updates or any other logic that depends on the new state here.
  });

  function clearCurrentlyPlaying() {
      try {
          const themeData = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY) || "{}");
          themeData.currentlyPlaying = null;
          localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(themeData));
          console.log("Currently playing data cleared");
      } catch (e) {
          console.error("Error clearing currentlyPlaying:", e);
      }
  }


  function handleAppId(appId) {
    if (!isThemeMusicEnabled()) return;
    if (pausedForGame) return;
    if (!window.appStore || !window.appStore.m_mapApps) return;
    var appInfo = window.appStore.m_mapApps.get(appId);
    if (!appInfo || !appInfo.display_name) return;
    var query = appInfo.display_name + " Theme Music";
    playYouTubeAudio(query);
  }

  function handleUrl(url) {
    if (!isThemeMusicEnabled()) return;
    var decoded = decodeURIComponent(url);
    var match = decoded.match(/\/library\/app\/(\d+)/);
    if (!match) match = window.location.pathname.match(/\/routes?\/library\/app\/(\d+)/);
    if (!match) return;
    var appId = Number(match[1]);
    if (appId === lastAppID) return;
    lastAppID = appId;
    handleAppId(appId);
  }

  lastUrl = mgr.m_URL;
  handleUrl(lastUrl);

  function watchUrl() {
    var current = mgr.m_URL;
    if (current && current !== lastUrl) {
      lastUrl = current;
      handleUrl(current);
    }
    requestAnimationFrame(watchUrl);
  }

  requestAnimationFrame(watchUrl);
})();"""









# Utility: Fetch debugger targets
def fetch_targets(host, port):
    conn = http.client.HTTPConnection(host, port)
    conn.request("GET", "/json")
    resp = conn.getresponse()
    if resp.status != 200:
        raise Exception(f"Failed to fetch targets: {resp.status} {resp.reason}")
    data = resp.read()
    conn.close()
    return json.loads(data)

# Find websocket debugger URL for the target title
def get_ws_url_by_title(host, port, title):
    targets = fetch_targets(host, port)
    for target in targets:
        if target.get("title") == title:
            return target.get("webSocketDebuggerUrl")
    raise Exception(f"Target with title '{title}' not found.")

# Create raw TCP socket and perform WebSocket handshake
def create_websocket_connection(ws_url):
    parsed = urlparse(ws_url)
    host = parsed.hostname
    port = parsed.port
    path = parsed.path + ("?" + parsed.query if parsed.query else "")

    sock = socket.create_connection((host, port))
    key = base64.b64encode(os.urandom(16)).decode('utf-8')
    headers = [
        f"GET {path} HTTP/1.1",
        f"Host: {host}:{port}",
        "Upgrade: websocket",
        "Connection: Upgrade",
        f"Sec-WebSocket-Key: {key}",
        "Sec-WebSocket-Version: 13",
        "\r\n"
    ]
    handshake = "\r\n".join(headers)
    sock.send(handshake.encode('utf-8'))

    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = sock.recv(4096)
        if not chunk:
            break
        resp += chunk

    if b"101" not in resp.split(b"\r\n")[0]:
        raise Exception("WebSocket upgrade failed:\n" + resp.decode('utf-8'))

    return sock

# Send a text frame (masked) over WebSocket
def send_ws_text(sock, message):
    frame = bytearray()
    frame.append(0x81)  # FIN + opcode text frame
    length = len(message)
    mask_bit = 0x80

    if length <= 125:
        frame.append(length | mask_bit)
    elif length <= 65535:
        frame.append(126 | mask_bit)
        frame += length.to_bytes(2, 'big')
    else:
        frame.append(127 | mask_bit)
        frame += length.to_bytes(8, 'big')

    mask_key = os.urandom(4)
    frame += mask_key

    msg_bytes = message.encode('utf-8')
    masked_bytes = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(msg_bytes))
    frame += masked_bytes

    sock.send(frame)

# Receive a single text message from WebSocket
def recv_ws_message(sock):
    first_byte = sock.recv(1)
    if not first_byte:
        return None
    fin = (first_byte[0] & 0x80) >> 7
    opcode = first_byte[0] & 0x0f

    if opcode == 0x8:
        return None  # Close frame
    if opcode != 0x1:
        return None  # Not text frame

    second_byte = sock.recv(1)
    masked = (second_byte[0] & 0x80) >> 7
    payload_len = second_byte[0] & 0x7f

    if payload_len == 126:
        extended = sock.recv(2)
        payload_len = int.from_bytes(extended, 'big')
    elif payload_len == 127:
        extended = sock.recv(8)
        payload_len = int.from_bytes(extended, 'big')

    if masked:
        mask_key = sock.recv(4)
    else:
        mask_key = None

    payload = bytearray()
    while len(payload) < payload_len:
        chunk = sock.recv(payload_len - len(payload))
        if not chunk:
            break
        payload.extend(chunk)

    if masked and mask_key:
        payload = bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload))

    return payload.decode('utf-8')





# Inject JS code and call createShortcut(data) directly
def recv_ws_message_for_id(sock, expected_id):
    while True:
        message = recv_ws_message(sock)
        if message is None:
            return None
        try:
            data = json.loads(message)
            if data.get("id") == expected_id:
                return data
            # Otherwise, it’s an event or unrelated message — ignore and continue waiting
        except Exception:
            continue


###Shortcut Creation ONLY
eval_id_counter = itertools.count(1000)
def inject_and_create_shortcut(ws_socket, shortcut_data):
    try:
        # Generate unique IDs
        enable_id = next(eval_id_counter)
        injected_check_id = next(eval_id_counter)
        inject_js_id = next(eval_id_counter)
        create_shortcut_id = next(eval_id_counter)

        # Enable Runtime domain
        send_ws_text(ws_socket, json.dumps({
            "id": enable_id,
            "method": "Runtime.enable"
        }))
        recv_ws_message_for_id(ws_socket, enable_id)

        # Step 0: Check if JS is already injected
        send_ws_text(ws_socket, json.dumps({
            "id": injected_check_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "window.__injectedSteamMod === true",
                "returnByValue": True
            }
        }))
        injected_check = recv_ws_message_for_id(ws_socket, injected_check_id)
        already_injected = injected_check.get("result", {}).get("result", {}).get("value") is True

        if not already_injected:
            # Step 1: Inject JS
            wrapped_code = f"(async () => {{ {JS_CODE}; window.__injectedSteamMod = true; return 'Injection successful!'; }})()"

            send_ws_text(ws_socket, json.dumps({
                "id": inject_js_id,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": wrapped_code,
                    "awaitPromise": True,
                }
            }))
            injection_response = recv_ws_message_for_id(ws_socket, inject_js_id)
            if not injection_response or injection_response.get("result", {}).get("result", {}).get("value") != "Injection successful!":
                print("JS injection failed or response invalid:")
                print(injection_response)
                return None
            print("JS injected successfully.")
        else:
            print("JS already injected. Skipping re-injection.")

        # Step 2: Call createShortcut with shortcut_data
        shortcut_json_str = json.dumps(shortcut_data)
        eval_expression = f"window.createShortcut({shortcut_json_str})"

        send_ws_text(ws_socket, json.dumps({
            "id": create_shortcut_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": eval_expression,
                "awaitPromise": True,
                "returnByValue": True
            }
        }))

        shortcut_result = recv_ws_message_for_id(ws_socket, create_shortcut_id)
        if not shortcut_result:
            print("No response from createShortcut call.")
            return None

        return shortcut_result

    except Exception as e:
        print(f"Exception during shortcut injection or creation: {e}")
        return None
###END of Shortcut creation




###For Uninstall Notifications only
def send_launcher_notification(ws_socket, message_text, removed_apps):
    notify_id = next(eval_id_counter)
    launcher_list = list(removed_apps.keys())
    js_launchers = json.dumps(launcher_list)
    js_message = json.dumps(message_text)

    JS_notify = f"""
    (function() {{
        try {{
            if (!window._sharedAudioCtx)
                window._sharedAudioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const ctx = window._sharedAudioCtx;

            function playTone({{ type='sine', frequency=440, frequencyEnd=null, volume=0.1, duration=1, startTime=null }}) {{
                const now = ctx.currentTime;
                const start = startTime ?? now;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = type;
                osc.frequency.setValueAtTime(frequency, start);
                if (frequencyEnd !== null)
                    osc.frequency.exponentialRampToValueAtTime(frequencyEnd, start + duration);
                gain.gain.setValueAtTime(volume, start);
                gain.gain.exponentialRampToValueAtTime(0.0005, start + duration);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(start);
                osc.stop(start + duration);
                osc.onended = () => {{ osc.disconnect(); gain.disconnect(); }};
            }}

            playTone({{ type:'sine', frequency:660, frequencyEnd:520, volume:0.12, duration:1.5 }});
            playTone({{ type:'sine', frequency:520, frequencyEnd:400, volume:0.08, duration:0.8, startTime: ctx.currentTime + 0.1 }});

            if (window.SteamClient && SteamClient.ClientNotifications) {{
                const payload = {{ rawbody: {js_message}, state: "ingame" }};
                SteamClient.ClientNotifications.DisplayClientNotification(
                    3,
                    JSON.stringify(payload),
                    function(arg) {{ console.log("Notification callback:", arg); }}
                );
            }}

            setTimeout(() => {{
                const launcherNames = {js_launchers};
                Array.from(collectionStore.collectionsFromStorage.values())
                    .forEach(c => {{
                        if (launcherNames.includes(c.m_strName)) {{
                            if ((c.visibleApps?.length || 0) === 0) {{
                                collectionStore.DeleteCollection(c.m_strId);
                                console.log(`Removed empty collection: ${{c.m_strName}}`);
                            }} else {{
                                console.log(`Collection not empty, skipped: ${{c.m_strName}} (Apps count: ${{c.visibleApps.length}})`);
                            }}
                        }}
                    }});
            }}, 5000);

        }} catch (err) {{
            console.error("Error in notification JS:", err);
        }}
    }})();
    """

    send_ws_text(ws_socket, json.dumps({
        "id": notify_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": JS_notify,
            "awaitPromise": False,
            "returnByValue": True
        }
    }))

    result = recv_ws_message_for_id(ws_socket, notify_id)
    return result


def inject_js_only(ws_socket):
    try:
        enable_id = next(eval_id_counter)
        inject_check_id = next(eval_id_counter)

        # Enable Runtime domain
        send_ws_text(ws_socket, json.dumps({
            "id": enable_id,
            "method": "Runtime.enable"
        }))
        recv_ws_message_for_id(ws_socket, enable_id)

        # Check if JS is already injected
        send_ws_text(ws_socket, json.dumps({
            "id": inject_check_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "window.__injectedSteamMod === true",
                "returnByValue": True
            }
        }))
        injected_check = recv_ws_message_for_id(ws_socket, inject_check_id)
        already_injected = injected_check.get("result", {}).get("result", {}).get("value") is True

        if not already_injected:
            print("Re-injecting Steam JS...")
            inject_id = next(eval_id_counter)
            wrapped_code = f"(async () => {{ {JS_notify}; window.__injectedSteamMod = true; return 'Injected Successfully'; }})()"
            send_ws_text(ws_socket, json.dumps({
                "id": inject_id,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": wrapped_code,
                    "awaitPromise": True,
                }
            }))
            result = recv_ws_message_for_id(ws_socket, inject_id)
            print("Injection result:", result)
        else:
            print("JS already injected. No re-injection needed.")

    except Exception as e:
        print("Injection failed:", e)
###End of Uninstall Notifcations



#Watch only
ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)

ws_socket = create_websocket_connection(ws_url)

eval_id_counter = itertools.count(1)
enable_id = next(eval_id_counter)

# Enable Runtime
send_ws_text(ws_socket, json.dumps({
    "id": enable_id,
    "method": "Runtime.enable"
}))
recv_ws_message_for_id(ws_socket, enable_id)

watch_code = r'''if (!window.__watcherInjected) {
    window.__watcherInjected = true;

    let gameRunning = false;
    let currentAppId = null;

    (function() {
        const originalLog = console.log;

        console.log = function(...args) {
            originalLog.apply(console, args);

            try {
                const line = args.join(' ');

                if (line.includes("OnGameActionUserRequest") &&
                    line.includes("LaunchApp CreatingProcess")) {

                    const match = line.match(/OnGameActionUserRequest:\s*(\d+)/);
                    if (match) {
                        const appId = match[1];
                        if (appId.length >= 18 && appId.length <= 20) {
                            gameRunning = true;
                            currentAppId = appId;
                            console.log("[Watcher] Game launch detected:", currentAppId);
                        }
                    }
                }

                if (gameRunning &&
                   (line.includes("Removing overlay browser window") ||
                    line.includes("NetworkDiagnosticsStore - unregistering for detailed connection state updates"))) {

                    gameRunning = false;

                    if (currentAppId) {
                        setTimeout(() => {
                            try {
                                SteamClient.Apps.TerminateApp(currentAppId, false);
                                console.log("[Watcher] App terminated:", currentAppId);
                                currentAppId = null;
                            } catch (e) {
                                console.error("[Watcher] Termination error:", e);
                            }
                        }, 10000);
                    }
                }
            } catch (e) {
                originalLog("[Watcher] Watcher error:", e);
            }
        };
    })();
}'''

def inject_watcher_once(ws_socket, watch_code):
    inject_id = next(eval_id_counter)
    check_id = next(eval_id_counter)

    # Check if watcher already injected
    send_ws_text(ws_socket, json.dumps({
        "id": check_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__watcherInjected === true",
            "returnByValue": True
        }
    }))
    result = recv_ws_message_for_id(ws_socket, check_id)
    if result.get("result", {}).get("result", {}).get("value") is True:
        print("Watcher already running. No reinjection.")
        return

    # Inject watcher
    send_ws_text(ws_socket, json.dumps({
        "id": inject_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": watch_code,
        }
    }))
    recv_ws_message_for_id(ws_socket, inject_id)
    print("Watcher injected and running.")
inject_watcher_once(ws_socket, watch_code)
###end of watch





###PLAYTIME ONLY
# Ensure eval_id_counter exists
eval_id_counter = iter(range(1, 1000000))

def inject_playtime_code(ws_socket):
    try:
        inject_id = next(eval_id_counter)

        wrapped_code = f"(async () => {{ {PLAYTIME_CODE}; return 'Playtime injection done'; }})()"

        send_ws_text(ws_socket, json.dumps({
            "id": inject_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": wrapped_code,
                "awaitPromise": True
            }
        }))

        response = recv_ws_message_for_id(ws_socket, inject_id)
        print("Playtime injection response:", response)
        return response
    except Exception as e:
        print("Error during Playtime injection:", e)
        return None

# Usage
try:
    ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)
    ws_socket = create_websocket_connection(ws_url)

    send_ws_text(ws_socket, json.dumps({"id": 1, "method": "Runtime.enable"}))
    recv_ws_message_for_id(ws_socket, 1)

    inject_playtime_code(ws_socket)
except Exception as e:
    print("Failed to connect or inject Playtime code:", e)

#END OF PLAYTIME





###THEMEMUSIC ONLY
# Usage
eval_id_counter = iter(range(1, 1000000))  # Ensure counter exists

def inject_thememusic_code(ws_socket):
    try:
        inject_id = next(eval_id_counter)

        wrapped_code = f"(async () => {{ {THEMEMUSIC_CODE}; return 'ThemeMusic injection done'; }})()"

        send_ws_text(ws_socket, json.dumps({
            "id": inject_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": wrapped_code,
                "awaitPromise": True
            }
        }))

        response = recv_ws_message_for_id(ws_socket, inject_id)
        print("ThemeMusic injection response:", response)
        return response
    except Exception as e:
        print("Error during ThemeMusic injection:", e)
        return None

# Usage
try:
    ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)
    ws_socket = create_websocket_connection(ws_url)

    send_ws_text(ws_socket, json.dumps({"id": 1, "method": "Runtime.enable"}))
    recv_ws_message_for_id(ws_socket, 1)

    inject_thememusic_code(ws_socket)
except Exception as e:
    print("Failed to connect or inject ThemeMusic code:", e)

#END OF THEMEMUSIC



### METADATA ONLY
METADATA_CODE = r"""
(function () {
    if (window.__MY_METADATA_SCRIPT_LOADED__) {
        return;
    } else {
        window.__MY_METADATA_SCRIPT_LOADED__ = true;

        // Cache object to store game details
        const gameCache = {};


        async function getSteamGameDetails(gameName) {
            if (gameCache[gameName]) return gameCache[gameName];

            try {
                const searchRes = await fetch(`https://store.steampowered.com/search/?term=${encodeURIComponent(gameName)}`, {
                    credentials: "omit"
                });
                const searchHtml = await searchRes.text();
                const searchDoc = new DOMParser().parseFromString(searchHtml, "text/html");

                const results = [...searchDoc.querySelectorAll("a.search_result_row")].map(r => ({
                    appid: r.dataset.dsAppid,
                    title: r.querySelector(".title")?.innerText.trim()
                }));

                if (!results.length) {
                    return await getWikipediaGameDetails(gameName);
                }

                const normalize = str => str?.toLowerCase().replace(/[-()]/g, "").replace(/\s+/g, " ").trim();
                const match = results.find(r => normalize(r.title) === normalize(gameName));

                if (!match) {
                    return await getWikipediaGameDetails(gameName);
                }

                const appid = match.appid;
                const apiRes = await fetch(`https://store.steampowered.com/api/appdetails?appids=${appid}`);
                const apiData = await apiRes.json();
                const info = apiData[appid].data;

                if (info) {
                    const platformsStr = info.platforms
                        ? Object.entries(info.platforms)
                            .filter(([k,v]) => v)
                            .map(([k]) => k)
                            .join(", ")
                        : "Unknown";

                    const gameData = {
                        appid: appid,
                        about_the_game: info.short_description || null,
                        developer: info.developers?.join(", ") || "Unknown",
                        publisher: info.publishers?.join(", ") || "Unknown",
                        release_date: info.release_date?.date || null,
                        genres: info.genres?.map(g => g.description).join(", ") || null,
                        platforms: platformsStr,
                        metacritic_score: info.metacritic?.score || null,
                        metacritic_url: info.metacritic?.url || null,
                        image_url: info.screenshots?.[0]?.path_full || null
                    };

                    gameCache[gameName] = gameData;
                    return gameData;
                }

                return await getWikipediaGameDetails(gameName);
            } catch (err) {
                return await getWikipediaGameDetails(gameName);
            }
        }

        async function getWikipediaGameDetails(gameName) {
            if (gameCache[gameName]) return gameCache[gameName];

            try {
                let gameTitle = gameName.replace(/\s+/g, "_");
                let url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(gameTitle)}`;
                let res = await fetch(url);

                if (!res.ok) {
                    const searchUrl = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(gameName)}&format=json&origin=*`;
                    const searchRes = await fetch(searchUrl);
                    const searchData = await searchRes.json();
                    if (!searchData.query.search.length) return null;

                    gameTitle = searchData.query.search[0].title.replace(/\s+/g, "_");
                    url = `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(gameTitle)}`;
                    res = await fetch(url);
                    if (!res.ok) return null;
                }

                const data = await res.json();
                const sentences = data.extract?.match(/[^.!?]+[.!?]+/g) || [];
                const description = sentences.slice(0, 2).join(" ").trim();
                const displayTitle = data.displaytitle?.replace(/<[^>]+>/g, "").replace(/\//g, "").trim();

                const game = {
                    appid: null,
                    displayTitle,
                    about_the_game: description || data.extract || null,
                    developer: "Unknown",
                    publisher: "Unknown",
                    release_date: null,
                    genres: null,
                    platforms: "Unknown",
                    metacritic_score: null,
                    metacritic_url: null,
                    image_url: data.originalimage?.source || null
                };

                const wikidataId = data.wikibase_item;
                if (wikidataId) {
                    const wdRes = await fetch(`https://www.wikidata.org/wiki/Special:EntityData/${wikidataId}.json`);
                    const wdData = await wdRes.json();
                    const claims = wdData.entities[wikidataId].claims;

                    const getClaimId = prop => claims?.[prop]?.[0]?.mainsnak?.datavalue?.value?.id || null;
                    const getClaimTime = prop => claims?.[prop]?.[0]?.mainsnak?.datavalue?.value?.time || null;
                    const getClaimIdList = prop => claims?.[prop]?.map(c => c.mainsnak.datavalue.value.id) || [];

                    const developerId = getClaimId("P178");
                    const publisherId = getClaimId("P123");
                    const releaseTime = getClaimTime("P577");
                    const genreIds = getClaimIdList("P136");
                    const platformIds = getClaimIdList("P400");

                    const idsToResolve = [developerId, publisherId, ...genreIds, ...platformIds].filter(Boolean);
                    let labelsData = {};

                    if (idsToResolve.length) {
                        const labelsRes = await fetch(
                            `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${idsToResolve.join("|")}&props=labels&languages=en&format=json&origin=*`
                        );
                        const labelsJson = await labelsRes.json();
                        labelsData = labelsJson.entities || {};
                    }

                    game.developer = developerId ? labelsData[developerId]?.labels?.en?.value ?? "Unknown" : "Unknown";
                    game.publisher = publisherId ? labelsData[publisherId]?.labels?.en?.value ?? "Unknown" : "Unknown";
                    game.release_date = releaseTime ? releaseTime.match(/\d{4}/)[0] : null;

                    if (genreIds.length) {
                        const genreLabel = labelsData[genreIds[0]]?.labels?.en?.value ?? "Unknown";
                        game.genres = genreLabel.replace(/\s*\(.*?\)\s*/g, "").trim();
                    }

                    const platformsClean = platformIds.map(id => {
                        const label = labelsData[id]?.labels?.en?.value ?? "Unknown";
                        return label.replace(/\s*\(.*?\)\s*/g, "").trim();
                    });
                    game.platforms = platformsClean.length
                        ? platformsClean.join(", ")
                        : "Unknown"; // <- Always string
                }

                gameCache[gameName] = game;
                return game;

            } catch (err) {
                return null;
            }
        }

        async function getGameDetails(gameName) {
            let gameData = await getSteamGameDetails(gameName);
            if (!gameData) gameData = await getWikipediaGameDetails(gameName);
            return gameData;
        }



        function replaceText() {
            document.querySelectorAll("div").forEach(div => {
                if (
                    div.childNodes.length === 1 &&
                    div.firstChild.nodeType === Node.TEXT_NODE
                ) {
                    const originalText = div.firstChild.nodeValue;
                    const match = originalText.match(/Some detailed information on (.*?) is unavailable/i);
                    if (match) {
                        const gameName = match[1];
                        const key = gameName.toUpperCase();
                        // Fetch game details from Steam (from cache or API)
                        getSteamGameDetails(gameName).then(gameData => {
                            if (!gameData) return;
                            const descriptionText = gameData.about_the_game || "No description available.";
                            const bgImage = gameData.image_url || "https://images-1.gog-statics.com/6f3d015c3029fea5221ccd9802de5e2f92c6afccc0196b15540677341936a656.jpg";
                            div.textContent = '';

                            //Check div
                            const currentDiv = div;

                            const nextDiv = currentDiv.nextElementSibling;

                            if (nextDiv) {
                                nextDiv.appendChild(currentDiv);
                            }


                // Main div styling
                div.style.position = "relative";
                div.style.overflow = "hidden";
                div.style.height = "250px";
                div.style.borderRadius = "6px";
                div.style.fontFamily = '"Roboto", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif';
                div.style.color = "white";
                div.style.outline = "none";
                div.style.border = "none";

                // Background image
                const img = document.createElement('img');
                img.src = bgImage;
                img.alt = gameName;
                img.style.width = "100%";
                img.style.height = "100%";
                img.style.objectFit = "cover";
                img.style.position = "absolute";
                img.style.top = 0;
                img.style.left = 0;
                img.style.opacity = 0.5;

                // Overlay
                const overlay = document.createElement('div');
                overlay.style.position = "absolute";
                overlay.style.top = 0;
                overlay.style.left = 0;
                overlay.style.width = "100%";
                overlay.style.height = "100%";
                overlay.style.padding = "10px";
                overlay.style.display = "flex";
                overlay.style.flexDirection = "column";
                overlay.style.justifyContent = "flex-start";
                overlay.style.background =
                "linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7))";

                // Content row
                const contentRow = document.createElement('div');
                contentRow.style.display = "flex";
                contentRow.style.flexDirection = "row";
                contentRow.style.flex = "1 1 auto";

                // Left column (launcher icon + tags)
                const leftColumn = document.createElement('div');
                leftColumn.style.display = "flex";
                leftColumn.style.flexDirection = "column";
                leftColumn.style.alignItems = "flex-start";
                leftColumn.style.marginRight = "15px";
                leftColumn.style.flexShrink = "0";


                // Add these:
                leftColumn.style.maxWidth = "250px"; // or a % like "35%" depending on your layout
                leftColumn.style.overflow = "visible"; // ensures it doesn’t break layout

                // New method for obtaining launcher info
                let foundLauncher = null;
                let ancestor = div;
                for (let i = 0; i < 9; i++) {
                if (!ancestor.parentElement) break;
                ancestor = ancestor.parentElement;
                }

                if (ancestor) {
                const launcher = ancestor.querySelector('div[role="button"], div.Focusable');
                if (launcher) {
                    foundLauncher = launcher.textContent.trim();
                }
                }

                // Launcher icons
                const launcherIcons = {
                "Epic Games": "https://cdn2.steamgriddb.com/icon/34ffeb359a192eb8174b6854643cc046/32/96x96.png",
                "GOG Galaxy": "https://cdn2.steamgriddb.com/icon/a928731e103dfc64c0027fa84709689e/32/96x96.png",
                "NonSteamLaunchers": "https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/refs/heads/main/logo.png",
                "Ubisoft Connect": "https://cdn2.steamgriddb.com/icon/dabcff9ba10224b01fd2ce83f7d73ad6/32/96x96.png",
                "EA App": "https://cdn2.steamgriddb.com/icon/ff51fb7a9bcb22c595616b4fa368880a/32/96x96.png",
                "Amazon Games": "https://cdn2.steamgriddb.com/icon_thumb/6e88ec1459f337d5bea6353f8bff8026.png",
                "itch.io": "https://cdn2.steamgriddb.com/icon/2ad9e5e943e43cad612a7996c12a8796/32/96x96.png",
                "Battle.net": "https://cdn2.steamgriddb.com/icon/739465804a0e17d2a47c9bc9c805d60a/32/96x96.png",
                "Legacy Games": "https://cdn2.steamgriddb.com/icon_thumb/5225802cb9758f9fcd34a679bf9326ec.png",
                "VK Play": "https://cdn2.steamgriddb.com/icon_thumb/5d35998237b55b8778a75732afc080aa.png",
                "HoyoPlay": "https://cdn2.steamgriddb.com/icon/817fccd834f01fb5e1770c8679c0824e/32/256x256.png",
                "Game Jolt Client": "https://cdn2.steamgriddb.com/icon_thumb/17df67628bb89193838f83015a3e7d30.png",
                "Minecraft Launcher": "https://cdn2.steamgriddb.com/icon/0678c572b0d5597d2d4a6b5bd135754c/32/96x96.png",
                "Humble Games Collection": "https://cdn2.steamgriddb.com/icon_thumb/3126ed973cbecde2bbffe419f139f456.png",
                "NVIDIA GeForce NOW": "https://cdn2.steamgriddb.com/icon_thumb/f91ee142269ec908c23e1cd87286e254.png",
                "Waydroid": "https://cdn2.steamgriddb.com/icon_thumb/d6de4f0418bf4015017f5c65cdecc46e.png",
                "Google Chrome": "https://cdn2.steamgriddb.com/icon/3941c4358616274ac2436eacf67fae05/32/256x256.png",
                "Brave": "https://cdn2.steamgriddb.com/icon_thumb/192d80a88b27b3e4115e1a45a782fe1b.png",
                "Vivaldi": "https://cdn2.steamgriddb.com/icon_thumb/51934729f32d36841a17e43e9390483a.png",
                "Mozilla Firefox": "https://cdn2.steamgriddb.com/icon_thumb/fe998b49c41c4208c968bce204fa1cbb.png",
                "LibreWolf": "https://cdn2.steamgriddb.com/icon/791608b685d1c61fb2fe8acdc69dc6b5/32/128x128.png",
                "Microsoft Edge": "https://cdn2.steamgriddb.com/icon_thumb/714cb7478d98b1cb51d1f5f515f060c7.png",
                "Gryphlink": "https://i.namu.wiki/i/1CZOhlpjxh3owDKXC9axrnMHtotdDaoFMmnzBvQ0yOqCDOL3rIZpH2DyLfX2UCRul9CxIH0gCn1DmRodHnKr6-IUmEzSZpZ6p4r9zRbDvwPe94gZnek0VaIvKfsWsx6L28czwaiz0Mj1NNayAkypNQ.webp"
                };

                const launcherName = foundLauncher;
                const launcherIcon = (launcherName && launcherIcons[launcherName]) || null;

                if (launcherIcon) {
                // Row that holds launcher icon + music button
                const launcherRow = document.createElement('div');
                launcherRow.style.display = "flex";
                launcherRow.style.alignItems = "center";
                launcherRow.style.gap = "8px";
                launcherRow.style.marginBottom = "8px";

                // Launcher icon
                const icon = document.createElement('img');
                icon.src = launcherIcon;
                icon.alt = launcherName;
                icon.style.width = "60px";
                icon.style.height = "60px";
                icon.style.objectFit = "contain";
                icon.onerror = () => icon.remove();

                launcherRow.appendChild(icon);

                // Placeholder music button (no logic)
                const musicBtn = document.createElement('button');
                musicBtn.textContent = "🎵";
                musicBtn.style.background = "rgba(36,40,47,0.7)";
                musicBtn.style.color = "white";
                musicBtn.style.border = "none";
                musicBtn.style.borderRadius = "12px";
                musicBtn.style.padding = "6px 10px";
                musicBtn.style.fontSize = "14px";
                musicBtn.style.lineHeight = "1";
                musicBtn.style.cursor = "pointer";
                musicBtn.style.display = "flex";
                musicBtn.style.alignItems = "center";
                musicBtn.style.justifyContent = "center";
                musicBtn.style.transition = "background 0.2s ease";


                launcherRow.appendChild(musicBtn);
                attachThemeMusicBehavior(musicBtn);


                // Add row to left column
                leftColumn.appendChild(launcherRow);
                }


                function createTag(text, fontSize) {
                const tag = document.createElement('span');
                tag.textContent = text;
                tag.style.fontSize = fontSize; // ← use the value passed in
                tag.style.background = "rgba(36,40,47,0.7)";
                tag.style.padding = "3px 8px";
                tag.style.borderRadius = "12px";
                tag.style.whiteSpace = "normal";
                tag.style.display = "inline-block";
                tag.style.wordBreak = "break-word";
                tag.style.marginRight = "4px";
                tag.style.marginBottom = "4px";
                return tag;
                }

                function createTagRow(items) {
                const row = document.createElement('div');
                row.style.display = "flex";
                row.style.flexWrap = "wrap";
                row.style.gap = "4px";

                // Determine font size based on number of items
                const fontSize = items.length > 3 ? "7.8px" : "12px";

                items.forEach(item => row.appendChild(createTag(item, fontSize)));
                return row;
                }


                leftColumn.appendChild(createTagRow((gameData.platforms || "Unknown").split(",").map(p => p.trim())));
                leftColumn.appendChild(createTagRow((gameData.developer || "Unknown").split(",").map(d => d.trim())));
                leftColumn.appendChild(createTagRow((gameData.publisher || "Unknown").split(",").map(p => p.trim())));
                leftColumn.appendChild(createTagRow([gameData.release_date || "Unknown"]));
                leftColumn.appendChild(createTagRow((gameData.genres || "Unknown").split(",").map(g => g.trim())));

            // Right column (description + Metacritic tab)
                const rightColumn = document.createElement('div');
                rightColumn.style.display = "flex";
                rightColumn.style.flexDirection = "column";
                rightColumn.style.flex = "1";

                // Wrap description in a container for absolute tabs
                const descriptionWrapper = document.createElement('div');
                descriptionWrapper.style.position = "relative";
                descriptionWrapper.style.width = "100%"; // ensures tab positions correctly

                const description = document.createElement('p');
                description.textContent = descriptionText;
                description.style.fontSize = "14px";
                description.style.lineHeight = "1.4";
                description.style.background = "rgba(36,40,47,0.7)";
                description.style.padding = "8px 12px";
                description.style.borderRadius = "12px";
                description.style.wordBreak = "break-word";
                description.style.overflowWrap = "break-word";

                descriptionWrapper.appendChild(description);

                // --- Metacritic tab ---
                if (gameData.metacritic_score && gameData.metacritic_url) {
                    const metaTab = document.createElement('a');
                    metaTab.href = gameData.metacritic_url;
                    metaTab.target = "_blank";
                    metaTab.style.position = "absolute";
                    metaTab.style.top = "14px";
                    metaTab.style.left = "-18px";
                    metaTab.style.display = "flex";
                    metaTab.style.flexDirection = "column";
                    metaTab.style.alignItems = "center";
                    metaTab.style.justifyContent = "center";
                    metaTab.style.background = "rgba(36,40,47,0.85)";
                    metaTab.style.color = "white";
                    metaTab.style.fontSize = "12px";
                    metaTab.style.padding = "4px 6px";
                    metaTab.style.borderRadius = "8px";
                    metaTab.style.textDecoration = "none";
                    metaTab.style.cursor = "pointer";
                    metaTab.style.boxShadow = "0 2px 6px rgba(0,0,0,0.3)";
                    metaTab.style.zIndex = "10";

                    metaTab.onmouseover = () => metaTab.style.background = "rgba(80,80,80,0.9)";
                    metaTab.onmouseout = () => metaTab.style.background = "rgba(36,40,47,0.85)";

                    const metaLogo = document.createElement('img');
                    metaLogo.src = "https://static.wikia.nocookie.net/logopedia/images/1/1f/Metacritic_2.svg";
                    metaLogo.style.width = "16px";
                    metaLogo.style.height = "16px";
                    metaLogo.style.marginBottom = "2px";

                    const scoreText = document.createElement('span');
                    scoreText.textContent = gameData.metacritic_score;
                    scoreText.style.fontWeight = "bold";
                    scoreText.style.fontSize = "12px";


                    // Set color based on Metacritic score using RGB
                    const score = parseInt(gameData.metacritic_score, 10);

                    if (score >= 0 && score <= 49) {
                        // Dark faded pink (red-ish)
                        scoreText.style.color = "rgb(139, 75, 90)"; // muted/dark pink
                    } else if (score >= 50 && score <= 79) {
                        // Dark faded orange
                        scoreText.style.color = "rgb(166, 106, 58)"; // muted/dark orange
                    } else if (score >= 80) {
                        // Dark faded green
                        scoreText.style.color = "rgb(75, 139, 90)"; // muted/dark green
                    }

                    metaTab.appendChild(metaLogo);
                    metaTab.appendChild(scoreText);

                    // Attach to wrapper (so it floats above description)
                    descriptionWrapper.appendChild(metaTab);
                }

                rightColumn.appendChild(descriptionWrapper);
                contentRow.appendChild(leftColumn);
                contentRow.appendChild(rightColumn);
                overlay.appendChild(contentRow);



                // Bottom links
                const bottomLinks = document.createElement('div');
                bottomLinks.style.position = "absolute";
                bottomLinks.style.bottom = "34px";
                bottomLinks.style.left = "10px";
                bottomLinks.style.right = "10px";
                bottomLinks.style.display = "flex";
                bottomLinks.style.flexWrap = "wrap";
                bottomLinks.style.gap = "6px";

                const searchSites = [
                { name: "Google", url: "https://www.google.com/search?q=", icon: "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" },

                { name: "PCGW", url: "https://www.pcgamingwiki.com/w/index.php?search=", extra: "&title=Special%3ASearch", icon: "https://pbs.twimg.com/profile_images/876511628258418689/Joehp5YI_400x400.jpg" },
                { name: "HLTB", url: "https://howlongtobeat.com/?q=", icon: "https://howlongtobeat.com/favicon.ico" },
                { name: "SDHQ", url: "https://steamdeckhq.com/?s=", icon: "https://pbs.twimg.com/profile_images/1539310786614419459/5ohiy0ZX_400x400.jpg" },
                { name: "GameFAQs", url: "https://gamefaqs.gamespot.com/search?game=", icon: "https://gamefaqs.gamespot.com/favicon.ico" },
                { name: "AWACY", url: "https://areweanticheatyet.com/?search=", icon: "https://areweanticheatyet.com/icon.webp" },
                { name: "ProtonDB", url: "https://www.protondb.com/search?q=", icon: "https://www.protondb.com/sites/protondb/images/site-logo.svg"},
                ];

                searchSites.forEach(site => {
                const link = document.createElement('a');
                // Minimal change: only modify IsThereAnyDeal URL
                let gameUrl = site.url + encodeURIComponent(gameName) + (site.extra || "");
                if (site.name === "IsThereAnyDeal") {
                    // Convert gameName into ITAD slug
                    const slug = gameName
                    .toLowerCase()
                    .replace(/[^a-z0-9 ]/g, '') // remove special chars
                    .trim()
                    .replace(/\s+/g, '-');      // spaces → hyphens
                    gameUrl = `${site.url}${slug}/info/`;
                }


                link.href = gameUrl;
                link.target = "_blank";
                link.style.display = "inline-flex";
                link.style.alignItems = "center";
                link.style.background = "rgba(36,40,47,0.7)";
                link.style.color = "white";
                link.style.fontSize = "13px";
                link.style.padding = "4px 4px";
                link.style.borderRadius = "6px";
                link.style.textDecoration = "none";
                link.style.transition = "background 0.2s"; // Smooth transition on hover

                // Set initial background on hover state using CSS
                link.onmouseover = () => {
                    link.style.background = "rgba(80,80,80,0.9)";
                };
                link.onmouseout = () => {
                    link.style.background = "rgba(36,40,47,0.7)";
                };

                const linkIcon = document.createElement('img');
                linkIcon.src = site.icon;
                linkIcon.style.width = "16px";
                linkIcon.style.height = "16px";
                linkIcon.style.marginRight = "4px";
                link.prepend(linkIcon);

                link.appendChild(document.createTextNode(site.name));
                bottomLinks.appendChild(link);
                });


                // --- ITAD button directly under description ---
                const itadSite = {
                    name: "",
                    url: "https://isthereanydeal.com/game/",
                    icon: "https://isthereanydeal.com/public/assets/logo-GBHE6XF2.svg"
                };

                const slug = gameName.toLowerCase()
                    .replace(/[^a-z0-9 ]/g, '')
                    .trim()
                    .replace(/\s+/g, '-');

                const itadUrl = `${itadSite.url}${slug}/info/`;

                const itadLink = document.createElement('a');
                itadLink.href = itadUrl;
                itadLink.target = "_blank";
                itadLink.style.display = "inline-flex";
                itadLink.style.alignItems = "center";
                itadLink.style.background = "rgba(36,40,47,0.7)";
                itadLink.style.color = "white";
                itadLink.style.fontSize = "13px";
                itadLink.style.padding = "6px 12px";
                itadLink.style.borderRadius = "12px";
                itadLink.style.textDecoration = "none";
                itadLink.style.width = "max-content"; // ← keeps button snug
                rightColumn.style.display = "flex";
                rightColumn.style.flexDirection = "column";
                rightColumn.style.alignItems = "flex-end"; // ← aligns all children (including ITAD) to the right


                itadLink.style.marginTop = "0px"; // spacing below description

                itadLink.onmouseover = () => itadLink.style.background = "rgba(80,80,80,0.9)";
                itadLink.onmouseout = () => itadLink.style.background = "rgba(36,40,47,0.7)";

                const itadIcon = document.createElement('img');
                itadIcon.src = itadSite.icon;
                itadIcon.style.width = "16px";
                itadIcon.style.height = "16px";
                itadIcon.style.marginRight = "6px";
                itadLink.prepend(itadIcon);

                itadLink.appendChild(document.createTextNode(itadSite.name));

                // append it **directly under description** in right column
                rightColumn.appendChild(itadLink);





                overlay.appendChild(bottomLinks);
                div.appendChild(img);
                div.appendChild(overlay);
            });
            }
        }
        });
    }


    function attachThemeMusicBehavior(musicBtn) {
        const KEY = "ThemeMusicData";

        const load = () => {
            try { return JSON.parse(localStorage.getItem(KEY) || "{}"); }
            catch { return {}; }
        };

        const save = (data) => {
            try { localStorage.setItem(KEY, JSON.stringify(data)); }
            catch(e){ console.error(e); }
        };

        let data = load();
        let on = data.themeMusic === undefined ? true : !!data.themeMusic;

        // --- Container ---
        const container = document.createElement("div");
        Object.assign(container.style, {
            display: "inline-flex",
            alignItems: "center",
            position: "relative"
        });
        musicBtn.parentElement.insertBefore(container, musicBtn);
        container.appendChild(musicBtn);

        // Initial icon
        musicBtn.textContent = on ? "🎵" : "🔇";

        // --- Bubble tooltip ---
        const bubble = document.createElement("div");
        bubble.innerHTML = "Don't like what you hear? Use paste!";
        Object.assign(bubble.style, {
            position: "absolute",
            bottom: "30px",       // ← move above the button
            top: "auto",           // reset top
            left: "0",
            background: musicBtn.style.background,
            color: musicBtn.style.color,
            border: "none",
            borderRadius: musicBtn.style.borderRadius,
            padding: musicBtn.style.padding,
            fontSize: musicBtn.style.fontSize,
            whiteSpace: "nowrap",
            opacity: "0",
            transform: "translateY(10px)", // ← nudge down slightly for animation
            transition: "opacity 0.3s ease, transform 0.3s ease",
            pointerEvents: "auto",
            zIndex: "1000",
            cursor: "default"
        });

        container.appendChild(bubble);

        const showBubble = (text, isError=false) => {
            if (!on) return;

            if (text) {
                bubble.innerHTML = text;
            } else {
                const themeData = load();
                const current = themeData.currentlyPlaying;
                let linkHTML = "hear";
                if (current?.videoId) {
                    const videoUrl = `https://youtu.be/${current.videoId}`;
                    linkHTML = `<a href="${videoUrl}" target="_blank" style="color:#0af;text-decoration:underline; cursor:pointer;">hear</a>`;
                }
                bubble.innerHTML = `Don't like what you ${linkHTML}? Use paste!`;
            }

            bubble.style.opacity = "1";
            bubble.style.transform = "translateY(0)";
            bubble.style.backgroundColor = isError ? "#F44336" : musicBtn.style.background;
        };

        const hideBubble = () => {
            bubble.style.opacity = "0";
            bubble.style.transform = "translateY(-10px)";
        };

        // --- Paste button (pill style like music button) ---
        const pasteBtn = document.createElement("button");
        pasteBtn.textContent = "📋";
        Object.assign(pasteBtn.style, {
            background: musicBtn.style.background,
            color: musicBtn.style.color,
            border: "none",
            borderRadius: musicBtn.style.borderRadius,  // pill shape
            padding: musicBtn.style.padding,
            fontSize: musicBtn.style.fontSize,
            cursor: "pointer",
            marginLeft: "6px",
            opacity: 0,
            pointerEvents: "none",
            transition: "opacity 0.3s"
        });
        container.appendChild(pasteBtn);

        // --- Paste button logic ---
        pasteBtn.onclick = async () => {
            try {
                const text = await navigator.clipboard.readText();
                const match = text.match(/(?:youtube\.com\/.*v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
                if (!match) return showBubble("Invalid YouTube link!", true);

                const newVideoId = match[1];
                const themeData = load();
                const currentThemeName = themeData.currentlyPlaying?.name;
                if (!currentThemeName || !themeData[currentThemeName])
                    return showBubble("No theme currently playing!", true);

                themeData[currentThemeName].videoId = newVideoId;
                themeData[currentThemeName].timestamp = Date.now();
                save(themeData);

                musicBtn.textContent = "🎵";
                showBubble(`Updated "${currentThemeName}"!`);
                setTimeout(() => {
                    pasteBtn.style.opacity = "0";
                    pasteBtn.style.pointerEvents = "none";
                }, 3000);
            } catch (e) {
                console.error(e);
                showBubble("Failed to read clipboard.", true);
            }
        };

        // --- Hover logic (includes bubble itself) ---
        [musicBtn, pasteBtn, bubble].forEach(el => {
            el.addEventListener("mouseenter", () => {
                if (on) {
                    showBubble();
                    pasteBtn.style.opacity = "1";
                    pasteBtn.style.pointerEvents = "auto";
                }
            });
            el.addEventListener("mouseleave", () => {
                setTimeout(() => {
                    if (!on || ![musicBtn, pasteBtn, bubble].some(el => el.matches(':hover'))) {
                        hideBubble();
                        pasteBtn.style.opacity = "0";
                        pasteBtn.style.pointerEvents = "none";
                    }
                }, 200); // slightly longer delay to allow moving into bubble
            });
        });

        // --- Toggle music on/off ---
        musicBtn.onclick = () => {
            on = !on;
            musicBtn.textContent = on ? "🎵" : "🔇";
            const saved = load();
            saved.themeMusic = on;
            save(saved);
            if (!on) {
                hideBubble();
                pasteBtn.style.opacity = "0";
                pasteBtn.style.pointerEvents = "none";
            }
        };
    }

    replaceText();

    // Only create a new observer if one doesn’t already exist
    if (!window.steamEnhancerObserver) {
        const observer = new MutationObserver(replaceText);
        observer.observe(document.body, { childList: true, subtree: true });

        // Save it globally so future runs know it exists
        window.steamEnhancerObserver = observer;
    }

}
})();
"""

def inject_metadata_code(ws_socket):
    inject_id = next(eval_id_counter)

    wrapped_code = f"""
    (function () {{
        {METADATA_CODE}
    }})();
    """

    send_ws_text(ws_socket, json.dumps({
        "id": inject_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": wrapped_code,
            "awaitPromise": True
        }
    }))

    recv_ws_message(ws_socket)


for target in (TARGET_TITLE2, TARGET_TITLE3):
    try:
        ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, target)
        ws_socket = create_websocket_connection(ws_url)

        send_ws_text(ws_socket, json.dumps({
            "id": 1,
            "method": "Runtime.enable"
        }))
        recv_ws_message(ws_socket)

        inject_metadata_code(ws_socket)

    except Exception as e:
        print(f"Metadata injection failed for {target}: {e}")
















# Create an empty dictionary to store the app IDs
app_ids = {}

# Get the next available key for the shortcuts
def get_next_available_key(shortcuts):
    key = 0
    while str(key) in shortcuts['shortcuts']:
        key += 1
    return str(key)


def get_compat_tool_if_needed(launchoptions):
    steam_compat_marker = 'STEAM_COMPAT_DATA_PATH'
    # Check for UMU-related Proton (UMU-Proton) and return None immediately if found
    if 'UMU-Proton' in launchoptions:  # If it's an UMU-related shortcut, return None immediately
        print("Exclusion: UMU-related shortcut detected.")
        return None

    if ('chrome' in launchoptions or
        'brave' in launchoptions or
        'edge' in launchoptions or
        'firefox' in launchoptions or
        'librewolf' in launchoptions or
        'vivaldi' in launchoptions or
        '--appid 0' in launchoptions):
        print("Exclusion: Chrome, Brave, Edge, Firefox, LibreWolf, Vivaldi or AppID 0 detected.")
        return None

    if any(x in launchoptions for x in ['jp.', 'com.', 'online.']):
        print("Exclusion: App region detected.")
        if steam_compat_marker not in launchoptions:
            print(f"Exclusion: {steam_compat_marker} not in launch options.")
            return None

    print("No exclusions applied. Returning compat tool.")
    return compat_tool_name






def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir, launcher_name=None):
    global new_shortcuts_added
    global shortcuts_updated
    global created_shortcuts

    global grid64
    global gridp64
    global logo64
    global hero64
    global counter

    grid64 = ""
    gridp64 = ""
    logo64 = ""
    hero64 = ""

    # Check if the launcher is installed
    if not shortcutdirectory or not appname or not launchoptions or not startingdir:
        print(f"{appname} is not installed. Skipping.")
        return

    exe_path = f"{shortcutdirectory}"

    # --- FIX: Modify shortcut first ---
    exe_path, startingdir, launchoptions = modify_shortcut_for_umu(appname, exe_path, launchoptions, startingdir)
    umu_id = extract_umu_id_from_launch_options(launchoptions)

    # --- Now generate IDs using modified exe_path ---
    signed_shortcut_id = get_steam_shortcut_id(exe_path, appname)
    unsigned_shortcut_id = get_unsigned_shortcut_id(signed_shortcut_id)

    # Only store app ID for specific launchers
    if appname in ['Epic Games', 'Gog Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App', 'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client', 'Rockstar Games Launcher', 'Glyph', 'Minecraft Launcher', 'Playstation Plus', 'VK Play', 'HoYoPlay', 'Nexon Launcher', 'Game Jolt Client', 'Artix Game Launcher', 'ARC Launcher', 'PURPLE Launcher', 'Plarium Play', 'VFUN Launcher', 'Tempo Launcher', 'Pokémon Trading Card Game Live', 'Antstream Arcade', 'STOVE Client', 'Big Fish Games Manager', 'Gryphlink']:
        app_ids[appname] = unsigned_shortcut_id

    # Check if shortcut already exists with final values
    if check_if_shortcut_exists(appname, exe_path, startingdir, launchoptions):
        shortcuts_updated = True
        return

    # Skip artwork download for specific shortcuts
    if appname not in ['Repair EA App']:
        #delete_old_artwork_by_tag(appname, unsigned_shortcut_id, steamid3, logged_in_home)
        game_id = get_game_id(appname)
        if game_id is not None:
            get_sgdb_art(game_id, unsigned_shortcut_id)

    # Try Steam fallback artwork
    steam_store_appid = get_steam_store_appid(appname)
    if steam_store_appid:
        print(f"Found Steam App ID for {appname}: {steam_store_appid}")
        create_steam_store_app_manifest_file(steam_store_appid, appname)

        for art_type in ["icons", "logos", "heroes", "grids_600x900", "grids_920x430"]:
            url = get_steam_fallback_url(steam_store_appid, art_type)
            if not url:
                print(f"Fallback URL invalid for {art_type} - No valid URL found")
                continue

            try:
                # Use urllib to perform a HEAD request (check URL status)
                req = urllib.request.Request(url, method='HEAD')
                with urllib.request.urlopen(req) as response:
                    if response.status == 200:
                        ext = url.split('.')[-1]

                        if art_type == "icons":
                            filename = get_file_name("icons", unsigned_shortcut_id)
                        elif art_type == "logos":
                            filename = f"{unsigned_shortcut_id}_logo.{ext}"
                        elif art_type == "heroes":
                            filename = f"{unsigned_shortcut_id}_hero.{ext}"
                        elif art_type == "grids_600x900":
                            filename = f"{unsigned_shortcut_id}p.{ext}"
                        elif art_type == "grids_920x430":
                            filename = f"{unsigned_shortcut_id}.{ext}"
                        else:
                            continue

                        file_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{filename}"

                        # Download and use artwork directly — no file existence checks
                        with urllib.request.urlopen(url) as img_response:
                            img_data = img_response.read()

                            if art_type == "icons":
                                with open(file_path, 'wb') as f:
                                    f.write(img_data)
                                print(f"Downloaded and saved fallback icon: {filename}")
                            else:
                                encoded = b64encode(img_data).decode('utf-8')
                                print(f"Downloaded fallback {art_type} as base64")

                                if art_type == "logos" and not logo64:
                                    logo64 = encoded
                                elif art_type == "heroes" and not hero64:
                                    hero64 = encoded
                                elif art_type == "grids_600x900" and not gridp64:
                                    gridp64 = encoded
                                elif art_type == "grids_920x430" and not grid64:
                                    grid64 = encoded
                    else:
                        print(f"Fallback URL invalid for {art_type} - {url}")
            except Exception as e:
                print(f"Error downloading fallback artwork for {art_type}: {e}")



    tag_artwork_files(unsigned_shortcut_id, appname, steamid3, logged_in_home)



    new_entry = {
        'appname': appname,
        'exe': exe_path,
        'StartDir': startingdir,
        'icon': f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{get_file_name('icons', unsigned_shortcut_id)}",
        'LaunchOptions': launchoptions,
        'WideGrid': grid64,
        'Grid': gridp64,
        'Hero': hero64,
        'Logo': logo64,
    }

    if launcher_name:
        new_entry['Launcher'] = launcher_name






    compat_tool = get_compat_tool_if_needed(launchoptions)

    # Skip setting compat tool if UMU already processed it
    if not (umu_id and umu_processed_shortcuts.get(umu_id)) and compat_tool:
        new_entry['CompatTool'] = compat_tool



    # Add the new entry to the shortcuts dictionary and add proton
    #key = get_next_available_key(shortcuts)
    #shortcuts['shortcuts'][key] = new_entry
    print(f"Added new entry for {appname} to shortcuts.")
    new_shortcuts_added = True
    created_shortcuts.append(appname)




    # Inject JS + Send data over WebSocket
    shortcut_id = None
    try:
        ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)
        print(f"Connecting to WebSocket URL: {ws_url}")

        ws = create_websocket_connection(ws_url)
        print("WebSocket connected")

        result = inject_and_create_shortcut(ws, new_entry)
        time.sleep(3.0)
        print("Shortcut creation result:", result)

        shortcut_id = None
        m_gameid = None
        if result and 'result' in result:
            value = result['result']['result'].get('value')
            if isinstance(value, dict) and value.get('success'):
                shortcut_id = value.get('shortcutId')
                m_gameid = value.get('m_gameid')
                print("App ID returned from JS:", shortcut_id)
                print(f"Found m_gameid: {m_gameid}")




                create_exec_line_from_entry(logged_in_home, new_entry, m_gameid)




                if shortcut_id:
                    print(f"Tagging artwork files for final Steam shortcut ID: {shortcut_id}")
                    tag_artwork_files(shortcut_id, appname, steamid3, logged_in_home)


                    #Delete other artwork files tagged with the same appname
                    delete_old_artwork_by_tag(appname, shortcut_id, steamid3, logged_in_home)

            else:
                print("JS returned unexpected structure:", value)
        else:
            print("No result returned from JS")





        ws.close()
        print("WebSocket closed.")
    except Exception as e:
        print(f"WebSocket error: {e}")



    #Final return
    return new_entry



# UMU-related functions
umu_processed_shortcuts = {}
CSV_URL = "https://raw.githubusercontent.com/Open-Wine-Components/umu-database/main/umu-database.csv"

# Global variable to store CSV data
csv_data = []

def fetch_and_parse_csv():
    global csv_data

    # Try local UMU database first
    try:
        dir_path = f"{logged_in_home}/.steam/root/compatibilitytools.d"
        pattern = re.compile(r"(UMU|GE)-Proton-?(\d+(?:\.\d+)*)(?:-(\d+(?:\.\d+)*))?")

        def parse_version(m):
            main, sub = m.groups()[1:]
            return tuple(map(int, (main + '.' + (sub or '0')).split('.')))

        compat_folders = [
            (parse_version(m), name)
            for name in os.listdir(dir_path)
            if (m := pattern.match(name)) and os.path.isdir(os.path.join(dir_path, name))
        ]

        if not compat_folders:
            print("No compatible UMU or GE-Proton folders found for local UMU database.")
        else:
            latest_folder = max(compat_folders)[1]
            local_csv_path = os.path.join(
                dir_path, latest_folder, "protonfixes", "umu-database.csv"
            )

            with open(local_csv_path, 'r', encoding='utf-8') as f:
                csv_data = [row for row in csv.DictReader(f.readlines())]
                print(f"Successfully loaded UMU data from local file: {local_csv_path}")
                return csv_data

    except Exception as local_e:
        print(f"Failed to load local UMU database: {local_e}")

    # Fallback to online if local fails
    try:
        with urllib.request.urlopen(CSV_URL, timeout=5) as response:
            if response.status != 200:
                raise Exception(f"HTTP {response.status}")
            content = response.read().decode('utf-8')
            csv_data = [row for row in csv.DictReader(content.splitlines())]
            print("Fetched UMU database from online as fallback.")
    except (urllib.error.URLError, Exception) as e:
        print(f"Failed to fetch UMU data from the internet: {e}")
        csv_data = []

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
    # Skip UMU modification for specific titles
    skip_titles = ["genshin impact", "zenless zone zero"]
    if appname.lower() in skip_titles:
        print(f"Skipping UMU modification for {appname}.")
        return exe, startingdir, launchoptions
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
                #match = re.search(r'--game=(\w+)', launchoptions)
                #
                #if match:
                    #codename = match.group(1)  # Capture the identifier
                    #updated_launch = f"'--game={codename}'"

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


                #Set compat tool name to UMU-Proton(Latest)
                dir_path = f"{logged_in_home}/.steam/root/compatibilitytools.d"
                pattern = re.compile(r"UMU-Proton-(\d+(?:\.\d+)*)(?:-(\d+(?:\.\d+)*))?")

                def parse_version(m):
                    main, sub = m.groups()
                    return tuple(map(int, (main + '.' + (sub or '0')).split('.')))

                umu_folders = [
                    (parse_version(m), name)
                    for name in os.listdir(dir_path)
                    if (m := pattern.match(name)) and os.path.isdir(os.path.join(dir_path, name))
                ]

                if umu_folders:
                    compat_tool_name = max(umu_folders)[1]

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





def track_create_entry(directory, name, launch_options, starting_dir, launcher_name="NonSteamLaunchers"):
    if not any([directory, launch_options, starting_dir]):
        return  # Skip if not installed

    create_new_entry(directory, name, launch_options, starting_dir, launcher_name)
    track_game(name, "Launcher")



track_create_entry(os.environ.get('epicshortcutdirectory'), 'Epic Games', os.environ.get('epiclaunchoptions'), os.environ.get('epicstartingdir'))
track_create_entry(os.environ.get('gogshortcutdirectory'), 'GOG Galaxy', os.environ.get('goglaunchoptions'), os.environ.get('gogstartingdir'))
track_create_entry(os.environ.get('uplayshortcutdirectory'), 'Ubisoft Connect', os.environ.get('uplaylaunchoptions'), os.environ.get('uplaystartingdir'))
track_create_entry(os.environ.get('battlenetshortcutdirectory'), 'Battle.net', os.environ.get('battlenetlaunchoptions'), os.environ.get('battlenetstartingdir'))
track_create_entry(os.environ.get('eaappshortcutdirectory'), 'EA App', os.environ.get('eaapplaunchoptions'), os.environ.get('eaappstartingdir'))
track_create_entry(os.environ.get('amazonshortcutdirectory'), 'Amazon Games', os.environ.get('amazonlaunchoptions'), os.environ.get('amazonstartingdir'))
track_create_entry(os.environ.get('itchioshortcutdirectory'), 'itch.io', os.environ.get('itchiolaunchoptions'), os.environ.get('itchiostartingdir'))
track_create_entry(os.environ.get('legacyshortcutdirectory'), 'Legacy Games', os.environ.get('legacylaunchoptions'), os.environ.get('legacystartingdir'))
track_create_entry(os.environ.get('humbleshortcutdirectory'), 'Humble Bundle', os.environ.get('humblelaunchoptions'), os.environ.get('humblestartingdir'))
track_create_entry(os.environ.get('indieshortcutdirectory'), 'IndieGala Client', os.environ.get('indielaunchoptions'), os.environ.get('indiestartingdir'))
track_create_entry(os.environ.get('rockstarshortcutdirectory'), 'Rockstar Games Launcher', os.environ.get('rockstarlaunchoptions'), os.environ.get('rockstarstartingdir'))
track_create_entry(os.environ.get('glyphshortcutdirectory'), 'Glyph', os.environ.get('glyphlaunchoptions'), os.environ.get('glyphstartingdir'))
track_create_entry(os.environ.get('minecraftshortcutdirectory'), 'Minecraft Launcher', os.environ.get('minecraftlaunchoptions'), os.environ.get('minecraftstartingdir'))
track_create_entry(os.environ.get('psplusshortcutdirectory'), 'Playstation Plus', os.environ.get('pspluslaunchoptions'), os.environ.get('psplusstartingdir'))
track_create_entry(os.environ.get('vkplayshortcutdirectory'), 'VK Play', os.environ.get('vkplaylaunchoptions'), os.environ.get('vkplaystartingdir'))
track_create_entry(os.environ.get('hoyoplayshortcutdirectory'), 'HoYoPlay', os.environ.get('hoyoplaylaunchoptions'), os.environ.get('hoyoplaystartingdir'))
track_create_entry(os.environ.get('nexonshortcutdirectory'), 'Nexon Launcher', os.environ.get('nexonlaunchoptions'), os.environ.get('nexonstartingdir'))
track_create_entry(os.environ.get('gamejoltshortcutdirectory'), 'Game Jolt Client', os.environ.get('gamejoltlaunchoptions'), os.environ.get('gamejoltstartingdir'))
track_create_entry(os.environ.get('artixgameshortcutdirectory'), 'Artix Game Launcher', os.environ.get('artixgamelaunchoptions'), os.environ.get('artixgamestartingdir'))
track_create_entry(os.environ.get('purpleshortcutdirectory'), 'PURPLE Launcher', os.environ.get('purplelaunchoptions'), os.environ.get('purplestartingdir'))
track_create_entry(os.environ.get('plariumshortcutdirectory'), 'Plarium Play', os.environ.get('plariumlaunchoptions'), os.environ.get('plariumstartingdir'))
track_create_entry(os.environ.get('vfunshortcutdirectory'), 'VFUN Launcher', os.environ.get('vfunlaunchoptions'), os.environ.get('vfunstartingdir'))
track_create_entry(os.environ.get('temposhortcutdirectory'), 'Tempo Launcher', os.environ.get('tempolaunchoptions'), os.environ.get('tempostartingdir'))
track_create_entry(os.environ.get('arcshortcutdirectory'), 'ARC Launcher', os.environ.get('arclaunchoptions'), os.environ.get('arcstartingdir'))
track_create_entry(os.environ.get('poketcgshortcutdirectory'), 'Pokémon Trading Card Game Live', os.environ.get('poketcglaunchoptions'), os.environ.get('poketcgstartingdir'))
track_create_entry(os.environ.get('antstreamshortcutdirectory'), 'Antstream Arcade', os.environ.get('antstreamlaunchoptions'), os.environ.get('antstreamstartingdir'))
track_create_entry(os.environ.get('stoveshortcutdirectory'), 'STOVE Client', os.environ.get('stovelaunchoptions'), os.environ.get('stovestartingdir'))
track_create_entry(os.environ.get('bigfishshortcutdirectory'), 'Big Fish Games Manager', os.environ.get('bigfishlaunchoptions'), os.environ.get('bigfishstartingdir'))
track_create_entry(os.environ.get('gryphlinkshortcutdirectory'), 'Gryphlink', os.environ.get('gryphlinklaunchoptions'), os.environ.get('gryphlinkstartingdir'))


track_create_entry(os.environ.get('repaireaappshortcutdirectory'), 'Repair EA App', os.environ.get('repaireaapplaunchoptions'), os.environ.get('repaireaappstartingdir'))





def detect_browser_name(chromedir: str, launch_opts: str) -> str:
    combined = f"{chromedir} {launch_opts}"
    if "com.google.Chrome" in combined:
        return "Google Chrome"
    elif "org.mozilla.firefox" in combined:
        return "Mozilla Firefox"
    elif "com.microsoft.Edge" in combined:
        return "Microsoft Edge"
    elif "com.brave.Browser" in combined:
        return "Brave"
    elif "com.vivaldi.Vivaldi" in combined:
        return "Vivaldi"
    elif "io.gitlab.librewolf-community" in combined:
        return "LibreWolf"
    else:
        return "Unknown"

def browser_for_env(envvar: str) -> str:
    opts = os.environ.get(envvar, "")
    return detect_browser_name(chromedirectory, opts)


create_new_entry(chromedirectory, 'Xbox Game Pass', os.environ.get('xboxchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('xboxchromelaunchoptions'))
create_new_entry(chromedirectory, 'Better xCloud', os.environ.get('xcloudchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('xcloudchromelaunchoptions'))
create_new_entry(chromedirectory, 'GeForce Now', os.environ.get('geforcechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('geforcechromelaunchoptions'))
create_new_entry(chromedirectory, 'Boosteroid Cloud Gaming', os.environ.get('boosteroidchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('boosteroidchromelaunchoptions'))
create_new_entry(chromedirectory, 'Stim.io', os.environ.get('stimiochromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('stimiochromelaunchoptions'))
create_new_entry(chromedirectory, 'WatchParty', os.environ.get('watchpartychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('watchpartychromelaunchoptions'))
create_new_entry(chromedirectory, 'Netflix', os.environ.get('netflixchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('netflixchromelaunchoptions'))
create_new_entry(chromedirectory, 'Hulu', os.environ.get('huluchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('huluchromelaunchoptions'))
create_new_entry(chromedirectory, 'Tubi', os.environ.get('tubichromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('tubichromelaunchoptions'))
create_new_entry(chromedirectory, 'Disney+', os.environ.get('disneychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('disneychromelaunchoptions'))
create_new_entry(chromedirectory, 'Amazon Prime Video', os.environ.get('amazonchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('amazonchromelaunchoptions'))
create_new_entry(chromedirectory, 'Youtube', os.environ.get('youtubechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('youtubechromelaunchoptions'))
create_new_entry(chromedirectory, 'Youtube TV', os.environ.get('youtubetvchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('youtubetvchromelaunchoptions'))
create_new_entry(chromedirectory, 'Amazon Luna', os.environ.get('lunachromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('lunachromelaunchoptions'))
create_new_entry(chromedirectory, 'Twitch', os.environ.get('twitchchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('twitchchromelaunchoptions'))
create_new_entry(chromedirectory, 'Venge', os.environ.get('vengechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('vengechromelaunchoptions'))
create_new_entry(chromedirectory, 'Rocketcrab', os.environ.get('rocketcrabchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('rocketcrabchromelaunchoptions'))
create_new_entry(chromedirectory, 'Fortnite', os.environ.get('fortnitechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('fortnitechromelaunchoptions'))
create_new_entry(chromedirectory, 'Cloudy Pad', os.environ.get('cloudychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('cloudychromelaunchoptions'))
create_new_entry(chromedirectory, 'WebRcade', os.environ.get('webrcadechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('webrcadechromelaunchoptions'))
create_new_entry(chromedirectory, 'WebRcade Editor', os.environ.get('webrcadeeditchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('webrcadeeditchromelaunchoptions'))
create_new_entry(chromedirectory, 'Afterplay.io', os.environ.get('afterplayiochromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('afterplayiochromelaunchoptions'))
create_new_entry(chromedirectory, 'OnePlay', os.environ.get('oneplaychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('oneplaychromelaunchoptions'))
create_new_entry(chromedirectory, 'AirGPU', os.environ.get('airgpuchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('airgpuchromelaunchoptions'))
create_new_entry(chromedirectory, 'CloudDeck', os.environ.get('clouddeckchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('clouddeckchromelaunchoptions'))
create_new_entry(chromedirectory, 'JioGamesCloud', os.environ.get('jiochromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('jiochromelaunchoptions'))
create_new_entry(chromedirectory, 'Plex', os.environ.get('plexchromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('plexchromelaunchoptions'))
create_new_entry(chromedirectory, 'Apple TV+', os.environ.get('applechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('applechromelaunchoptions'))
create_new_entry(chromedirectory, 'Crunchyroll', os.environ.get('crunchychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('crunchychromelaunchoptions'))
create_new_entry(chromedirectory, 'PokéRogue', os.environ.get('pokeroguechromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('pokeroguechromelaunchoptions'))



# Iterate over each custom website
for i, website in enumerate(custom_websites):
    if not website.startswith(("http://", "https://")):
        website = f"https://{website}"

    parts = urlsplit(website)
    encoded_path = quote(parts.path, safe="/")
    url = urlunsplit((
        parts.scheme,
        parts.netloc,
        encoded_path,
        parts.query,
        parts.fragment
    ))

    if i < len(custom_names) and custom_names[i]:
        game_name = custom_names[i]
    else:
        clean = (
            website.replace("http://", "")
                   .replace("https://", "")
                   .replace("www.", "")
                   .rstrip("/")
        )

        match = re.search(r"/games/([^/]+)", website)
        if match:
            game_name = (
                match.group(1)
                .replace("-", " ")
                .replace("%27", "'")
                .title()
            )
        else:
            game_name = clean.split("/")[0].title()

    launch_options = f"{base_launch_options} {url}"

    create_new_entry(
        os.environ["chromedirectory"],
        game_name,
        launch_options,
        os.environ["chrome_startdir"],
        launcher_name=browser_for_env('customchromelaunchoptions')
    )



def remove_unwanted_lines(lines, remove_keys):
    lines_to_keep = []
    modified = False

    for line in lines:
        if not any(key in line for key in remove_keys):
            lines_to_keep.append(line)
        else:
            modified = True

    return lines_to_keep, modified


remove_lines = {
    'chromelaunchoptions',
    'websites_str',
    'custom_website_names_str'
}

lines_to_keep, modified = remove_unwanted_lines(lines, remove_lines)

if modified:
    with open(env_vars_path, 'w') as f:
        f.writelines(lines_to_keep)

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
    'PURPLE Launcher': 'PURPLELauncher',
    'Plarium Play': 'PlariumLauncher',
    'VFUN Launcher': 'VFUNLauncher',
    'Tempo Launcher': 'TempoLauncher',
    'Pokémon Trading Card Game Live': 'PokeTCGLauncher',
    'Antstream Arcade': 'AntstreamLauncher',
    'STOVE Client': 'STOVELauncher',
    'Big Fish Games Manager': 'BigFishLauncher',
    'Gryphlink': 'GryphlinkLauncher',
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
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files/Epic Games/Launcher/Portal/Binaries/Win64/EpicGamesLauncher.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files/Epic Games/Launcher/Portal/Binaries/Win64/\""
            launch_options = f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/\" %command% -'com.epicgames.launcher://apps/{app_name}?action=launch&silent=true'"

            # Check if the game is still installed and if the LaunchExecutable is valid, not content-related, and is a .exe file
            if item_data['LaunchExecutable'].endswith('.exe') and "Content" not in item_data['DisplayName'] and "Content" not in item_data['InstallLocation']:
                for game in dat_data['InstallationList']:
                    if game['AppName'] == item_data['AppName']:
                        create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="Epic Games")
                        track_game(display_name, "Epic Games")

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

    # Optional mapping for known sub-launch games
    sublaunch_map = {
        "Assassin's Creed III Remastered": {
            "Assassin's Creed Liberation Remastered": "/1"
        },
        # Add more bundles here if needed
    }

    # Inject bundled sub-games based on known mappings
    for parent, subs in sublaunch_map.items():
        if parent in game_dict:
            for sub_name, suffix in subs.items():
                if sub_name not in game_dict:
                    game_dict[sub_name] = (game_dict[parent], suffix)

    for game, data in game_dict.items():
        if isinstance(data, tuple):
            uplay_id, suffix = data
        else:
            uplay_id = data
            suffix = "/0"

        launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/" %command% "uplay://launch/{uplay_id}{suffix}"'
        exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"'
        start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ubisoft_connect_launcher}/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/"'
        create_new_entry(exe_path, game, launch_options, start_dir, launcher_name="Ubisoft Connect")
        track_game(game, "Ubisoft Connect")

# End of Ubisoft Game Scanner



#EA App Scanner
def fix_encoding(text):
    # Encode as latin1 bytes, then decode as utf-8 to fix mojibake
    return text.encode('latin1').decode('utf-8')

def extract_games_fixed(filename):
    games = {}
    key_re = re.compile(r'\[Software\\\\Wow6432Node\\\\Origin Games\\\\(\d+)\]')
    name_re = re.compile(r'"DisplayName"="(.+)"')
    current_id = None

    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            key_match = key_re.search(line)
            if key_match:
                current_id = key_match.group(1)
                continue

            if current_id:
                name_match = name_re.search(line)
                if name_match:
                    raw_name = name_match.group(1)
                    raw_name = raw_name.replace(r'\x2122', '™')
                    name = bytes(raw_name, "utf-8").decode("unicode_escape")
                    name = fix_encoding(name)
                    games[current_id] = name
                    current_id = None

    return games

def get_ea_app_game_info(installed_games, game_directory_path, sys_reg_file=None):
    sys_reg_games = {}
    if sys_reg_file and os.path.isfile(sys_reg_file):
        try:
            sys_reg_games = extract_games_fixed(sys_reg_file)
            sys_reg_name_to_id = {v: k for k, v in sys_reg_games.items()}
        except Exception as e:
            print(f"Error reading sys reg fallback file: {e}")
            sys_reg_name_to_id = {}
    else:
        sys_reg_name_to_id = {}

    game_dict = {}
    for game in installed_games:
        try:
            xml_path = os.path.join(game_directory_path, game, "__Installer", "installerdata.xml")
            if not os.path.isfile(xml_path):
                continue

            xml_file = ET.parse(xml_path)
            xml_root = xml_file.getroot()

            ea_ids = None
            game_name = None

            for content_id in xml_root.iter('contentID'):
                ea_ids = content_id.text
                break

            for game_title in xml_root.iter('gameTitle'):
                if game_name is None:
                    game_name = game_title.text

            for game_title in xml_root.iter('title'):
                if game_name is None:
                    game_name = game_title.text

            if game_name is None:
                game_name = game

            game_name = re.sub(r'\s*\([^)]*\)$', '', game_name)


            matched_id = None

            if not ea_ids and sys_reg_name_to_id:
                print(f"No ID found in XML for '{game_name}', checking registry fallback...")
                for reg_name, reg_id in sys_reg_name_to_id.items():

                    clean_reg_name = re.sub(r'\s*\([^)]*\)$', '', reg_name)
                    if reg_name == game_name:
                        matched_id = reg_id
                        break
                if matched_id:
                    ea_ids = matched_id

            if ea_ids:
                if matched_id:
                    print(f"Found ID in registry fallback for '{game_name}': {ea_ids}")
                else:
                    print(f"Found ID in XML for '{game_name}': {ea_ids}")
                game_dict[game_name] = ea_ids
            else:
                print(f"Skipping '{game_name}' - no OfferID found in XML or registry.")

        except Exception as e:
            print(f"Error parsing XML for {game}: {e}")

    return game_dict

def find_ea_games_path_from_registry():
    registry_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/system.reg"
    if not os.path.isfile(registry_path):
        print("EA App registry file not found. Skipping registry check.")
        return None

    try:
        with open(registry_path, 'r', encoding='utf-16-le', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading EA registry file: {e}")
        return None

    matches = re.findall(r'\[Software\\\\EA Games\\\\.*?\]\s*[^[]*?"Install Dir"="(.*?)"', content, re.DOTALL)
    if not matches:
        return None

    example_path = matches[0]
    if "EA Games" in example_path:
        ea_games_index = example_path.find("EA Games")
        ea_games_path = example_path[:ea_games_index + len("EA Games")]
        ea_games_path_unix = ea_games_path.replace("C:\\", "").replace("\\", "/")
        return f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/{ea_games_path_unix}/"

    return None

def find_external_game_paths():
    possible_paths = []
    base_path = "/run/media/deck/"

    for folder_name in ["EA Games", "Origin Games"]:
        if os.path.isdir(base_path):
            for user_folder in os.listdir(base_path):
                full_path = os.path.join(base_path, user_folder, folder_name)
                if os.path.isdir(full_path):
                    possible_paths.append(full_path)

    top_level_dirs = []
    if os.path.isdir(base_path):
        for user_folder in os.listdir(base_path):
            user_path = os.path.join(base_path, user_folder)
            if os.path.isdir(user_path):
                for subfolder in os.listdir(user_path):
                    full_path = os.path.join(user_path, subfolder)
                    if os.path.isdir(full_path):
                        top_level_dirs.append(full_path + "/")

    for path in top_level_dirs:
        try:
            for sub in os.listdir(path):
                sub_path = os.path.join(path, sub)
                if os.path.isdir(os.path.join(sub_path, "__Installer")):
                    possible_paths.append(path)
                    break
        except Exception:
            continue

    return [p for p in possible_paths if os.path.isdir(p)]

# --- Main EA App Scanner ---
if not ea_app_launcher:
    print("EA App launcher ID not set. Skipping EA App Scanner.")
else:
    game_directory_path = None

    # 1. Default paths
    default_paths = [
        f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/EA Games/",
        f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files (x86)/EA Games/"
    ]
    for path in default_paths:
        if os.path.isdir(path):
            game_directory_path = path
            print(f"Found EA App games in default path: {path}")
            break

    # 2. Registry fallback
    if not game_directory_path:
        detected_path = find_ea_games_path_from_registry()
        if detected_path and os.path.isdir(detected_path):
            game_directory_path = detected_path
            print(f"Found EA App games via registry: {detected_path}")

    # 3. External drives
    if not game_directory_path:
        external_paths = find_external_game_paths()
        if external_paths:
            game_directory_path = external_paths[0]
            print(f"Using external EA App game path: {game_directory_path}")

    # 4. Validate path
    if not game_directory_path or not os.path.isdir(game_directory_path):
        print("EA App game data not found. Skipping EA App Scanner.")
        print("Paths tried:", default_paths)
        print("Registry detected path:", detected_path if 'detected_path' in locals() else None)
        print("External paths:", external_paths if 'external_paths' in locals() else None)
    else:
        try:
            installed_games = [g for g in os.listdir(game_directory_path)
                               if os.path.isdir(os.path.join(game_directory_path, g))]

            sys_reg_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/system.reg"

            game_dict = get_ea_app_game_info(installed_games, game_directory_path, sys_reg_file=sys_reg_path)

            if not game_dict:
                print("No EA App games found in scanned directories.")
            else:
                for game, ea_ids in game_dict.items():
                    launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/" %command% "origin2://game/launch?offerIds={ea_ids}"'
                    exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EALaunchHelper.exe"'
                    start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/"'

                    create_new_entry(exe_path, game, launch_options, start_dir, launcher_name="EA App")
                    track_game(game, "EA App")

        except Exception as e:
            print(f"Error scanning EA App games: {e}")
# End of EA App Scanner






#GOG Galaxy Scanner

def getGogGameInfoDB(db_path, logged_in_home, gog_galaxy_launcher):
    if not os.path.exists(db_path):
        print(f"GOG Galaxy DB not found, skipping GOG Scanner: {db_path}")
        return {}

    game_dict = {}

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Pull only the *default* PlayTask using isPrimary = 1
            cursor.execute("""
                SELECT
                    ibp.productId,
                    ld.title,
                    ibp.installationPath,
                    ptl.executablePath,
                    ptl.commandLineArgs
                FROM InstalledBaseProducts ibp
                JOIN LimitedDetails ld
                    ON ibp.productId = ld.productId
                LEFT JOIN PlayTasks pt
                    ON pt.gameReleaseKey = 'gog_' || ibp.productId
                   AND pt.isPrimary = 1
                LEFT JOIN PlayTaskLaunchParameters ptl
                    ON ptl.playTaskId = pt.id
                WHERE ld.is_production = 1
            """)

            for pid, title, install_path, ptl_exe, ptl_args in cursor.fetchall():
                if not ptl_exe:
                    continue

                exe_win_path = ptl_exe.replace("/", "\\").strip()

                proton_root = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx"
                win_no_drive = re.sub(r"^[A-Za-z]:/", "", exe_win_path.replace("\\", "/"))
                exe_proton_path = os.path.join(proton_root, "drive_c", win_no_drive)

                if not os.path.exists(exe_proton_path):
                    print(f"Skipping {title}: EXE not on disk -> {exe_proton_path}")
                    continue

                game_dict[title] = {
                    "id": pid,
                    "exe": exe_win_path,
                    "launchParams": ptl_args or ""
                }

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    return game_dict


def adjust_dosbox_launch_options(launch_command, game_id, logged_in_home, gog_galaxy_launcher, launch_args=""):
    """Build Steam launch string, including DOSBox arguments if present."""
    launch_lower = launch_command.lower()

    exe_path = launch_command

    if "dosbox.exe" in launch_lower:
        args = launch_args.strip()
        return (
            f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/" '
            f'%command% /command=runGame /gameId={game_id} /path="{exe_path}" "{args}"'
        )

    return (
        f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/" '
        f'%command% /command=runGame /gameId={game_id} /path="{exe_path}"'
    )



db_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/ProgramData/GOG.com/Galaxy/storage/galaxy-2.0.db"

if os.path.exists(db_path):
    game_dict = getGogGameInfoDB(db_path, logged_in_home, gog_galaxy_launcher)

    for game, info in game_dict.items():
        launch_options = adjust_dosbox_launch_options(
            info['exe'], info['id'], logged_in_home, gog_galaxy_launcher, launch_args=info['launchParams']
        )

        exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe\""
        start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gog_galaxy_launcher}/pfx/drive_c/Program Files (x86)/GOG Galaxy/\""

        create_new_entry(exe_path, game, launch_options, start_dir, launcher_name="GOG Galaxy")
        track_game(game, "GOG Galaxy")
else:
    print(f"GOG Galaxy DB not found at {db_path}")


#End of GOG Galaxy Scanner










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
    "GRY": "Warcraft Rumble",
    "ZEUS": "Call of Duty: Black Ops - Cold War",
    "VIPR": "Call of Duty: Black Ops 4",
    "ODIN": "Call of Duty: Modern Warfare",
    "AUKS": "Call of Duty",
    "LAZR": "Call of Duty: MW 2 Campaign Remastered",
    "FORE": "Call of Duty: Vanguard",
    "SPOT": "Call of Duty: Modern Warfare III",
    "WLBY": "Crash Bandicoot 4: It's About Time",
    "Aqua": "Avowed",
    "LBRA": "Tony Hawk's Pro Skater 3 + 4",
    "SCOR": "Sea of Thieves",
    "ARK": "The Outer Worlds 2",





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
        elif game_key == "diablo3":
            print("Handling 'diablo3' as 'D3'")
            game_key = "D3"
        elif game_key == "hs_beta":
            print("Handling 'hs_beta' as 'WTCG'")
            game_key = "WTCG"
        elif game_key == "wow_classic":
            print("Handling 'wow_classic' as 'WoWC'")
            game_key = "WoWC"
        elif game_key == "wow":
            print("Handling 'wow' as 'WoW'")
            game_key = "WoW"
        elif game_key == "aqua":
            print("Handling 'aqua' as 'Aqua'")
            game_key = "Aqua"
        elif game_key == "aris":
            print("Handling 'aris' as 'Aris'")
            game_key = "Aris"
        elif game_key == "heroes":
            game_key = "Hero"
        elif game_key == "gryphon":
            game_key = "GRY"
        elif game_key == "lbra":
            print("Handling 'lbra' as 'LBRA'")
            game_key = "LBRA"
        elif game_key == "wow_classic_era":
            print("Handling 'wow_classic_era' as 'WoWC'")
            game_key = "WoWC"





        elif game_key == "seaofthieves":
            print("Handling 'seaofthieves' as 'SCOR'")
            game_key = "SCOR"
        elif game_key == "sot":
            print("Handling 'sot' as 'SCOR'")
            game_key = "SCOR"
        elif game_key == "scor":
            game_key = "SCOR"


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
        create_new_entry(exe_path, game_name, launch_options, start_dir, launcher_name="Battle.net")
        track_game(game_name, "Battle.net")

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
        create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="Amazon Games")
        track_game(display_name, "Amazon Games")



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
        create_new_entry(exe_path, game_title, launchoptions, start_dir, launcher_name="itch.io")
        track_game(game_title, "itch.io")

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
                create_new_entry(f'"{exe_path}"', game_name, launch_options, f'"{start_dir}"', launcher_name="Legacy Games")
                track_game(game_name, "Legacy Games")
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

                create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="VK Play")
                track_game(display_name, "VK Play")

# End of VK Play Scanner


# HoYo Play Scanner

file_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/users/steamuser/AppData/Roaming/Cognosphere/HYP/1_0/data/gamedata.dat"

# Check if the file exists
if not os.path.exists(file_path):
    print("Skipping HoYo Play scanner: File does not exist.")
else:
    def extract_json_objects(data):
        decoder = json.JSONDecoder()
        json_objects = []

        decoded = data.decode("utf-8", errors="ignore")
        idx = 0
        length = len(decoded)

        while idx < length:
            try:
                json_obj, end = decoder.raw_decode(decoded[idx:])
                if isinstance(json_obj, dict):
                    json_objects.append(json_obj)
                idx += end
            except json.JSONDecodeError:
                idx += 1

        return json_objects

    with open(file_path, "rb") as f:
        f.read(8)
        raw_data = f.read()

    json_objects = extract_json_objects(raw_data)

    games = {}
    for entry in json_objects:
        exe = entry.get("gameInstallStatus", {}).get("gameExeName", "").strip()
        path = entry.get("installPath", "").strip()
        persist = entry.get("persistentInstallPath", "").strip()
        name = entry.get("gameShortcutName", "").strip()
        biz = entry.get("gameBiz", "").strip()

        if exe and path:
            key = name or exe
            if key not in games:
                games[key] = {
                    "exe_name": exe,
                    "install_path": path,
                    "persistent_path": persist,
                    "shortcut_name": name,
                    "gamebiz": biz,
                }

    if games:
        for game, details in sorted(games.items()):
            display_name = details["shortcut_name"] or game
            game_biz = details["gamebiz"]
            launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/" %command% "--game={game_biz}"'
            exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/Program Files/HoYoPlay/launcher.exe"'
            start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{hoyoplay_launcher}/pfx/drive_c/Program Files/HoYoPlay"'

            if not details["install_path"] and not details["persistent_path"]:
                continue

            create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="HoYoPlay")
            track_game(display_name, "HoYoPlay")

# End of HoYo Play Scanner



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
                create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="Game Jolt Client")
                track_game(display_name, "Game Jolt Client")

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
                create_new_entry(exe_path, display_name, launch_options, start_dir, launcher_name="Minecraft Launcher")
                track_game(display_name, "Minecraft Launcher")

            else:
                print("Key 'productLibraryDir' not found in the JSON.")
    except json.JSONDecodeError:
        print("Error decoding the JSON file.")
else:
    print("Skipping Minecraft Legacy Launcher Scanner")

# End of the Minecraft Legacy Launcher




#IndieGala Scanner
real_indie_launcher_path = os.path.realpath(
    f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{indie_launcher}"
)
print(f"Resolved indie_launcher path: {real_indie_launcher_path}")

installed_json_path = os.path.join(
    real_indie_launcher_path,
    "pfx/drive_c/users/steamuser/AppData/Roaming/IGClient/storage/installed.json"
)
default_install_path_file = os.path.join(
    real_indie_launcher_path,
    "pfx/drive_c/users/steamuser/AppData/Roaming/IGClient/storage/default-install-path.json"
)

def file_is_valid(file_path):
    return os.path.exists(file_path) and os.path.getsize(file_path) > 0

def windows_to_linux_path(windows_path):
    linux_base = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{indie_launcher}/pfx/drive_c/"
    if windows_path.startswith("C:/"):
        return linux_base + windows_path[3:].replace("\\", "/")
    return windows_path.replace("\\", "/")

def find_exe_file(base_path, slugged_name, game_name):
    search_dir = os.path.join(base_path, slugged_name)
    if not os.path.exists(search_dir):
        print(f"Game folder not found: {search_dir}")
        return None

    possible_names = [
        f"{game_name}.exe",
        f"{game_name.title().replace(' ', '')}.exe",
        f"{game_name.replace(' ', '')}.exe",
        f"{game_name.lower().replace(' ', '').replace('-', '')}.exe",
        f"{slugged_name}.exe",
        f"{slugged_name.replace('-', '')}.exe",
    ]

    for name in possible_names:
        full_path = windows_to_linux_path(os.path.join(search_dir, name))
        if os.path.exists(full_path):
            return full_path
    return None

if not file_is_valid(installed_json_path) or not file_is_valid(default_install_path_file):
    print("Required JSON files missing or empty. Skipping scan.")
else:
    with open(default_install_path_file, "r") as f:
        default_data = json.load(f)
        default_install_path = default_data if isinstance(default_data, str) else default_data.get("default-install-path", "C:/IGClientGames")
    default_install_path = windows_to_linux_path(default_install_path)

    with open(installed_json_path, "r") as f:
        data = json.load(f)

    for game_entry in data:
        game_data = game_entry["target"]["game_data"]
        game_info = game_entry["target"]["item_data"]

        game_name = game_info.get("name", "Unnamed Game")
        slugged_name = game_info.get("slugged_name", "missing-slug")
        location = windows_to_linux_path(game_entry.get("path", default_install_path))
        exe_path = game_data.get("exe_path")

        game_path = None

        if exe_path:
            guessed_path = windows_to_linux_path(os.path.join(location, exe_path))
            if os.path.exists(guessed_path):
                game_path = guessed_path
            else:
                parts = exe_path.replace("\\", "/").split("/")
                if len(parts) > 1:
                    parts[0] = slugged_name
                    alt_path = windows_to_linux_path(os.path.join(location, *parts))
                    if os.path.exists(alt_path):
                        game_path = alt_path
                    else:
                        print(f"Exe path invalid for {game_name}, trying fallback.")
                        game_path = find_exe_file(location, slugged_name, game_name)
                else:
                    game_path = find_exe_file(location, slugged_name, game_name)
        else:
            print(f"No exe_path for {game_name}, using fallback.")
            game_path = find_exe_file(location, slugged_name, game_name)

        if not game_path or not os.path.exists(game_path):
            print(f"Skipping {game_name}: Executable not found.")
            continue

        start_dir = os.path.dirname(game_path)
        launchoptions = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{indie_launcher}/" %command%'
        create_new_entry(f"\"{game_path}\"", game_name, launchoptions, f"\"{start_dir}\"", launcher_name="IndieGala Client")
        track_game(game_name, "IndieGala Client")
#End of IndieGala Scanner




#chrome scanner for xbox, geforce now, and amazon luna bookmarks
bookmarks_file_path = f"{logged_in_home}/.var/app/com.google.Chrome/config/google-chrome/Default/Bookmarks"

# Lists to store results
geforce_now_urls = []
xbox_urls = []
luna_urls = []
seen_urls = set()

def process_bookmark_item(item):
    if item['type'] == "url":
        name = item['name'].strip()
        url = item['url']

        if not name or url in seen_urls:
            return

        # GeForce NOW
        if "play.geforcenow.com/games" in url:
            if name == "GeForce NOW":
                return
            game_name = name.replace(" on GeForce NOW", "").strip()
            url = url.split("&")[0] if "&" in url else url
            if url in seen_urls:
                return
            geforce_now_urls.append(("GeForce NOW", game_name, url))
            seen_urls.add(url)

        # Xbox Cloud Gaming
        elif "xbox.com/" in url and ("/play/launch/" in url or "/play/games/" in url):
            if name.startswith("Play "):
                game_name = name.replace("Play ", "").split(" |")[0].strip()
            else:
                game_name = name.split(" |")[0].strip()

            if game_name:
                xbox_urls.append(("Xbox", game_name, url))
                seen_urls.add(url)

        # Amazon Luna
        elif "luna.amazon." in url and "/game/" in url:
            if name.startswith("Play "):
                game_name = name.replace("Play ", "").split(" |")[0].strip()
            else:
                game_name = name.split(" |")[0].strip()

            if game_name:
                luna_urls.append(("Amazon Luna", game_name, url))
                seen_urls.add(url)

def scan_children(children):
    for item in children:
        if item['type'] == "folder":
            scan_children(item.get('children', []))
        else:
            process_bookmark_item(item)

if not os.path.exists(bookmarks_file_path):
    print("Chrome Bookmarks not found. Skipping scanning for Bookmarks.")
else:
    with open(bookmarks_file_path, 'r') as f:
        data = json.load(f)

    # Scan bookmarks in bookmark_bar, other, and synced folders recursively
    scan_children(data['roots']['bookmark_bar'].get('children', []))
    scan_children(data['roots']['other'].get('children', []))
    scan_children(data['roots']['synced'].get('children', []))

    # Merge all platforms' URLs into a single list for processing
    all_urls = geforce_now_urls + xbox_urls + luna_urls

    for platform_name, game_name, url in all_urls:
        print(f"{platform_name}: {game_name} - {url}")

        # Encode URL to prevent issues with special characters
        encoded_url = quote(url, safe=":/?=&")

        chromelaunch_options = (
            f'run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ '
            f'--window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 '
            f'--start-fullscreen {encoded_url} --no-first-run --enable-features=OverlayScrollbar'
        )

        chromedirectory = os.environ.get("chromedirectory", "/usr/bin/flatpak")
        chrome_startdir = os.environ.get("chrome_startdir", "/usr/bin")

        # Replace this with your existing method to handle the entries
        create_new_entry(
            chromedirectory,
            game_name,
            chromelaunch_options,
            chrome_startdir,
            launcher_name="Google Chrome"
        )
        track_game(game_name, "Google Chrome")

# end of chrome scanner for xbox, geforce now, and amazon luna bookmarks





# Waydroid scanner
# Check for Waydroid
if shutil.which("waydroid") is None:
    print("Waydroid not found. Skipping Waydroid scanner.")
else:
    applications_dir = f"{logged_in_home}/.local/share/applications/"
    ignored_files = {
        "waydroid.com.android.inputmethod.latin.desktop",
        "waydroid.com.android.gallery3d.desktop",
        "waydroid.com.android.documentsui.desktop",
        "waydroid.com.android.settings.desktop",
        "waydroid.org.lineageos.eleven.desktop",
        "waydroid.com.android.calculator2.desktop",
        "waydroid.com.android.contacts.desktop",
        "waydroid.org.lineageos.etar.desktop",
        "waydroid.org.lineageos.jelly.desktop",
        "waydroid.com.android.camera2.desktop",
        "waydroid.com.android.deskclock.desktop",
        "waydroid.org.lineageos.recorder.desktop",
        "waydroid.com.google.android.apps.messaging.desktop",
        "waydroid.com.google.android.contacts.desktop",
        "waydroid.org.lineageos.aperture.desktop",
    }

    # Possible cage launchers
    possible_launchers = [
        f"{logged_in_home}/Android_Waydroid/Android_Waydroid_Cage.sh",
        f"{logged_in_home}/bin/waydroid-cage.sh",
        f"{logged_in_home}/.local/bin/waydroid-cage.sh",
    ]

    launcher_path = next((p for p in possible_launchers if os.path.isfile(p)), None)

    if launcher_path is None:
        search_dirs = [logged_in_home, "/run/media", "/mnt", "/media"]
        for base in search_dirs:
            if not os.path.isdir(base):
                continue
            for root, dirs, files in os.walk(base):
                # Limit recursion to 2 levels deep
                if root[len(base):].count(os.sep) > 2:
                    dirs[:] = []
                    continue
                if "waydroid-cage.sh" in files:
                    launcher_path = os.path.join(root, "waydroid-cage.sh")
                    print(f"Found Waydroid launcher: {launcher_path}")
                    break
            if launcher_path:
                break

    use_cage = bool(launcher_path)
    exe_path = launcher_path if use_cage else "waydroid"
    start_dir = os.path.dirname(launcher_path) if use_cage else "./"

    print(f"Waydroid Cage Detected: {use_cage}")
    print(f"Launcher Path: {exe_path}")

    if os.path.isdir(applications_dir):
        for file_name in os.listdir(applications_dir):
            if not file_name.endswith(".desktop") or file_name in ignored_files:
                continue

            file_path = os.path.join(applications_dir, file_name)
            try:
                parser = configparser.RawConfigParser(strict=False)
                parser.read(file_path)

                if "Desktop Entry" not in parser:
                    continue

                display_name = parser.get("Desktop Entry", "Name", fallback=None)
                exec_cmd = parser.get("Desktop Entry", "Exec", fallback="").lower()

                if not display_name or "waydroid app launch" not in exec_cmd:
                    continue

                parts = exec_cmd.strip().split()
                app_name = parts[-1] if len(parts) >= 3 else None
                if not app_name:
                    continue

                if use_cage:
                    target = f'"{exe_path}"'
                    launch_opts = f'"{app_name}"'
                    start_in = start_dir
                else:
                    target = '"waydroid"'
                    launch_opts = f'"app" "launch" "{app_name}"'
                    start_in = start_dir

                create_new_entry(
                    shortcutdirectory=target,
                    appname=display_name,
                    launchoptions=launch_opts,
                    startingdir=start_in,
                    launcher_name="Waydroid"
                )
                track_game(display_name, "Waydroid")

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
    else:
        print(f"Applications directory not found: {applications_dir}")
# End of Waydroid scanner






#Flatpak Scanner
flatpak_apps = [
    {
        "id": "com.nvidia.geforcenow",
        "display_name": "NVIDIA GeForce NOW"
    },
    {
        "id": "com.moonlight_stream.Moonlight",
        "display_name": "Moonlight Game Streaming"
    },
    {
        "id": "com.hypixel.HytaleLauncher",
        "display_name": "Hytale"
    }
]

exe_path = "/usr/bin/flatpak"
start_dir = "/usr/bin"

def is_flatpak_installed(app_id):
    try:
        subprocess.run(["flatpak", "info", "--user", app_id],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["flatpak", "info", "--system", app_id],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

for app in flatpak_apps:
    app_id = app["id"]
    display_name = app["display_name"]
    if not is_flatpak_installed(app_id):
        print(f"Skipping {display_name} scanner — Flatpak not found or app not installed.")
        continue

    # Custom launch options for specific apps
    if app_id == "com.moonlight_stream.Moonlight":
        app_launch_options = '"run" "--branch=stable" "--arch=x86_64" "--command=moonlight" "com.moonlight_stream.Moonlight"'
    elif app_id == "com.hypixel.HytaleLauncher":
        app_launch_options = '"run" "--branch=master" "--arch=x86_64" "--command=hytale-launcher-wrapper" "com.hypixel.HytaleLauncher"'
    else:
        app_launch_options = f"run {app_id}"

    create_new_entry(
        shortcutdirectory=f'"{exe_path}"',
        appname=display_name,
        launchoptions=app_launch_options,
        startingdir=f'"{start_dir}"',
        launcher_name="NonSteamLaunchers"
    )
    track_game(display_name, "Launcher")
# End of Flatpak Scanner





#STOVE Client Scanner
steam_compat_base = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{stove_launcher}"
stove_launcher_path = os.path.join(steam_compat_base, "pfx/drive_c/ProgramData/Smilegate/STOVE/STOVE.exe")
client_config_path = os.path.join(steam_compat_base, "pfx/drive_c/users/steamuser/AppData/Local/STOVE/Config/ClientConfig.json")

if not os.path.isfile(client_config_path):
    print("Skipping STOVE Scanner ClientConfig.json not found at", client_config_path)
else:
    with open(client_config_path, "r", encoding="utf-8") as f:
        client_config = json.load(f)

    win_games_dir = client_config.get("defaultPath", "")
    if not win_games_dir:
        print("No defaultPath found in ClientConfig.json")
    else:
        linux_games_dir = win_games_dir.replace("C:\\", f"{steam_compat_base}/pfx/drive_c/").replace("\\", "/")
        if not os.path.isdir(linux_games_dir):
            print("Games directory not found at", linux_games_dir)
        else:
            manifest_files = []
            for subdir_name in os.listdir(linux_games_dir):
                subdir_path = os.path.join(linux_games_dir, subdir_name)
                combinedata_path = os.path.join(subdir_path, "combinedata_manifest")
                if os.path.isdir(combinedata_path):
                    for filename in os.listdir(combinedata_path):
                        if filename.startswith("GameManifest_") and filename.endswith(".upf"):
                            manifest_files.append(os.path.join(combinedata_path, filename))

            if not manifest_files:
                print("No game manifest files found")
            else:
                for manifest_path in manifest_files:
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as mf:
                            game_data = json.load(mf)

                        game_id = game_data.get("game_id")
                        game_title = game_data.get("game_title", game_id)

                        if not game_id:
                            print("Missing game_id in manifest:", manifest_path)
                            continue

                        launch_options = f'STEAM_COMPAT_DATA_PATH="{steam_compat_base}/" %command% "sgup://run/{game_id}"'

                        create_new_entry(
                            shortcutdirectory=f'"{stove_launcher_path}"',
                            appname=game_title,
                            launchoptions=launch_options,
                            startingdir=f'"{os.path.dirname(stove_launcher_path)}"',
                            launcher_name="STOVE Client"
                        )
                        track_game(game_title, "STOVE Client")

                    except Exception as e:
                        print("Error reading manifest", manifest_path, ":", e)

#End of STOVE Client Scanner




# Humble Games Collection Scanner (Humble Bundle, Humble Games, Humble Games Collection)
proton_prefix = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{humble_launcher}/pfx"

# JSON config file path inside Proton prefix
config_path = os.path.join(
    proton_prefix,
    "drive_c/users/steamuser/AppData/Roaming/Humble App/config.json"
)

# Convert Windows-style path to Linux path inside Proton prefix drive_c
def windows_to_linux_path(win_path):
    if not win_path:
        return ""
    if win_path.startswith("C:\\"):
        rel_path = win_path.replace("C:\\", "").replace("\\", "/")
        return os.path.join(proton_prefix, "drive_c", rel_path)
    return win_path

# Skip scanner if config doesn't exist
if not os.path.isfile(config_path):
    print("Skipping Humble Games Scanner (config not found)")
else:
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Skipping Humble Games Scanner (invalid config)")
    else:
        games = data.get("game-collection-4", [])

        for idx, game in enumerate(games, 1):
            status = game.get("status")
            if status not in ("downloaded", "installed"):
                continue

            game_name = game.get("gameName", "Unknown")
            win_install_path = game.get("filePath", "")
            exe_rel_path = game.get("executablePath", "")


            if not exe_rel_path or not win_install_path:
                print("  Missing executable or install path, skipping")
                continue

            linux_install_path = windows_to_linux_path(win_install_path)
            linux_exe_path = os.path.join(linux_install_path, exe_rel_path.replace("\\", "/"))

            if not os.path.isfile(linux_exe_path):
                print("  Executable not found, skipping game")
                continue

            start_dir = os.path.dirname(linux_exe_path)
            launch_options = f'STEAM_COMPAT_DATA_PATH="{proton_prefix}" %command%'

            # Your shortcut creation function (should be defined elsewhere)
            create_new_entry(f'"{linux_exe_path}"', game_name, launch_options, f'"{start_dir}"', launcher_name="Humble Bundle")
            track_game(game_name, "Humble Bundle")

# End of Humble Scanner







#NVIDIA GEFORCE NOW NATIVE LINUX Game SCANNER
def extract_block_info(block):
    full_game_name = None
    short_name = None
    parent_game_id = None

    for line in block:
        if not full_game_name:
            m = re.search(r"Add game to favorites for\s+(.+?)\s+\[", line)
            if m:
                full_game_name = m.group(1).strip()

        if not short_name:
            m = re.search(r"Attempting add to favorite, game\s+(\S+)\[", line)
            if m:
                short_name = m.group(1)

        if not parent_game_id:
            m = re.search(r"\[([0-9a-fA-F-]{36})\]", line)
            if m:
                parent_game_id = m.group(1)

    return full_game_name, short_name, parent_game_id

log_path = os.path.join(
    logged_in_home,
    ".var/app/com.nvidia.geforcenow/.local/state/NVIDIA/GeForceNOW/console.log"
)

if not os.path.exists(log_path):
    print(f"GeForce NOW log not found at: {log_path}. Skipping scan.")
else:
    try:
        with open(log_path) as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to read GeForce NOW log: {e}")
    else:
        viewgame_events = []
        for i, line in enumerate(lines):
            if "JsEventsService" in line and "events request" in line:
                try:
                    json_part = line.split("events request", 1)[1].strip()
                    data = json.loads(json_part)
                    for event in data.get("events", []):
                        if event.get("name") == "Click":
                            params = event.get("parameters", {})
                            if params.get("itemType") == "ViewGameDetails":
                                item_label = params.get("itemLabel")
                                if item_label and re.match(r"^\d+$", item_label):
                                    viewgame_events.append({
                                        "line_index": i,
                                        "cmsId": item_label
                                    })
                except Exception:
                    continue

        favorites = []
        for i, line in enumerate(lines):
            if "UserGesture clicked on add to favorites" in line:
                block = lines[i:i+30]
                full_game_name, short_name, parent_game_id = extract_block_info(block)

                if not short_name or not parent_game_id:
                    continue

                closest_view = None
                closest_distance = None
                for view in viewgame_events:
                    distance = abs(view["line_index"] - i)
                    if closest_distance is None or distance < closest_distance:
                        closest_distance = distance
                        closest_view = view

                cms_id = closest_view["cmsId"] if closest_view else None

                favorites.append({
                    "shortName": short_name,
                    "parentGameId": parent_game_id,
                    "cmsId": cms_id,
                    "fullGameName": full_game_name
                })

        for fav in favorites:
            display_name = fav['fullGameName'] or fav['shortName']
            exe_path = '"/usr/bin/flatpak"'
            start_dir = '"/usr/bin/"'

            if fav["cmsId"]:
                url_route = (
                    f"#?cmsId={fav['cmsId']}"
                    f"&launchSource=External&shortName={fav['shortName']}"
                    f"&parentGameId={fav['parentGameId']}"
                )
            else:
                print(f"Missing cmsId for favorite game: {display_name}")
                url_route = (
                    f"#?launchSource=External&shortName={fav['shortName']}"
                    f"&parentGameId={fav['parentGameId']}"
                )

            launch_options = (
                f"run --command=sh com.nvidia.geforcenow -c "
                f"\"/app/cef/GeForceNOW --url-route='{url_route}'\""
            )

            print(f"Creating shortcut for: {display_name}")
            create_new_entry(exe_path, display_name, launch_options, start_dir, "NVIDIA GeForce NOW")
            #track_game(display_name, "NVIDIA GeForce NOW")
#End NVIDIA GeForce NOW Game Scanner



# Gryphlink Scanner (Endfield)

endfield_exe = (
    f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{gryphlink_launcher}/"
    "pfx/drive_c/Program Files/GRYPHLINK/games/EndField Game/Endfield.exe"
)

# Check if Endfield exists
if os.path.exists(endfield_exe):
    print(f"File exists: {endfield_exe}")

    display_name = "Arknights: Endfield"
    launch_options = (
        f"STEAM_COMPAT_DATA_PATH=\"{logged_in_home}/.local/share/Steam/"
        f"steamapps/compatdata/{gryphlink_launcher}/\" %command%"
    )

    exe_path = f"\"{endfield_exe}\""
    start_dir = f"\"{os.path.dirname(endfield_exe)}\""

    create_new_entry(
        exe_path,
        display_name,
        launch_options,
        start_dir,
        launcher_name="Gryphlink"
    )

    track_game(display_name, "Gryphlink")

else:
    print("Skipping Gryphlink Scanner — Endfield.exe not found")

# End of Gryphlink Game Scanner



# Call finalize_tracking and capture removed apps
removed_apps = finalize_tracking()

# List of game names to skip fetching descriptions for
skip_games = {'Epic Games', 'GOG Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App',
    'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client',
    'Rockstar Games Launcher', 'Glyph', 'Minecraft Launcher', 'Playstation Plus',
    'VK Play', 'HoYoPlay', 'Nexon Launcher', 'Game Jolt Client', 'Artix Game Launcher',
    'PURPLE Launcher', 'Plarium Play', 'VFUN Launcher', 'Tempo Launcher', 'ARC Launcher',
    'Pokémon Trading Card Game Live', 'Antstream Arcade', 'STOVE Client', 'Big Fish Games Manager', 'Xbox Game Pass',
    'Better xCloud', 'GeForce Now', 'Boosteroid Cloud Gaming', 'Stim.io', 'WatchParty',
    'Netflix', 'Hulu', 'Tubi', 'Disney+', 'Amazon Prime Video', 'Youtube', 'Youtube TV',
    'Amazon Luna', 'Twitch', 'Venge', 'Rocketcrab', 'Fortnite', 'WebRcade', 'Cloudy Pad',
    'WebRcade Editor', 'Afterplay.io', 'OnePlay', 'AirGPU', 'CloudDeck', 'JioGamesCloud',
    'Plex', 'Apple TV+', 'Crunchyroll', 'PokéRogue', 'NonSteamLaunchers', 'Repair EA App', 'Gryphlink'}


# --- Boot Video Logic ---
def get_boot_video(game_name, logged_in_home):
    excluded_apps = skip_games

    OVERRIDE_PATH = os.path.expanduser(f'{logged_in_home}/.steam/root/config/uioverrides/movies')
    REQUEST_RETRIES = 5
    API_URL = "https://steamdeckrepo.com/api/posts/all"
    DOWNLOAD_BASE = "https://steamdeckrepo.com/post/download"
    ssl_ctx = ssl.create_default_context()

    def sanitize_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def download_video(video, target_dir):
        """Download video if it does not already exist."""
        sanitized_name = sanitize_filename(video['name'])
        file_path = os.path.join(target_dir, f"{sanitized_name}.webm")

        if os.path.exists(file_path):
            print(f"Skipping {file_path}, already exists.")
            return

        os.makedirs(target_dir, exist_ok=True)

        download_url = video.get('download_url')
        if download_url:
            try:
                with urllib.request.urlopen(download_url, context=ssl_ctx, timeout=60) as response:
                    if response.status == 200:
                        with open(file_path, 'wb') as f:
                            while True:
                                chunk = response.read(8192)
                                if not chunk:
                                    break
                                f.write(chunk)
                        print(f"Downloaded {file_path}")
                    else:
                        print(f"Failed to download {file_path}, status code: {response.status}")
            except urllib.error.URLError as e:
                print(f"Download failed for {file_path}: {e}")
        else:
            print("No download URL found for video.")

    try:
        # Skip if game is in excluded list
        if game_name.lower() in [app.lower() for app in excluded_apps]:
            print(f"Skipping boot video for {game_name}, as it's in the excluded apps list.")
            return

        data = []
        for attempt in range(REQUEST_RETRIES):
            try:
                req = urllib.request.Request(API_URL, headers={"User-Agent": "SteamDeckBootFetcher/1.0"})
                with urllib.request.urlopen(req, context=ssl_ctx, timeout=20) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode('utf-8')).get('posts', [])
                        break
                    elif response.status == 429:
                        raise Exception('Rate limit exceeded, try again in a minute')
                    else:
                        print(f"steamdeckrepo fetch failed, status={response.status}")
            except urllib.error.URLError as e:
                print(f"Request failed: {e}")
            time.sleep(2)  # brief wait before retry
        else:
            raise Exception("Retry attempts exceeded")

        search_terms = [game_name.lower()]

        # First try full game name
        for term in search_terms:
            filtered_videos = sorted(
                (
                    {
                        'id': entry['id'],
                        'name': entry['title'],
                        'preview_video': entry['video'],
                        'download_url': f"{DOWNLOAD_BASE}/{entry['id']}",
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if term in entry['title'].lower() and entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'], reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]
                print(f"Downloading boot video: {video['name']}")
                download_video(video, OVERRIDE_PATH)
                return

        # If no video, try first two words of game name
        if len(game_name.split()) > 1:
            first_two_words = ' '.join(game_name.split()[:2]).lower()
            filtered_videos = sorted(
                (
                    {
                        'id': entry['id'],
                        'name': entry['title'],
                        'preview_video': entry['video'],
                        'download_url': f"{DOWNLOAD_BASE}/{entry['id']}",
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if first_two_words in entry['title'].lower() and entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'], reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]
                download_video(video, OVERRIDE_PATH)
                return

        # No video found
        print(f"No top boot video found for {game_name}.")

    except Exception as e:
        print(f"Failed to fetch steamdeckrepo: {e}")
# --- End of Boot Video Logic ---

# --- Main block (MUST remain untouched) ---
if new_shortcuts_added or shortcuts_updated:

    # --- Additional Logic ---
    notified_games = set()
    if created_shortcuts:
        print("Created Shortcuts:")

        for name in created_shortcuts:
            print(name)

            if name.lower() not in [app.lower() for app in skip_games]:
                print(f"Fetching boot video for: {name}")
                get_boot_video(name, logged_in_home)

        for name in created_shortcuts:
            if name in notified_games:
                continue

            shortcut_entry = next(
                (entry for entry in shortcuts.get('shortcuts', {}).values()
                 if entry.get('appname') == name), None
            )

            if shortcut_entry:
                message = f"A new game has been added to your library! {name}"

                # send_steam_notification(ws_socket, message)
                notified_games.add(name)
                time.sleep(0.1)  # Stagger notifications
            else:
                print(f"Warning: Game '{name}' not found in shortcuts dictionary.")

        print("All finished, Scanner was successful!")
else:
    print("No new shortcuts were added.")
    print("All finished, Scanner was successful!")

# Notify about removed games (if any)
if removed_apps:
    removed_game_names = [f"{app} ({launcher})" for launcher, apps in removed_apps.items() for app in apps]
    removed_message = "Removed from library:\n" + "\n".join(removed_game_names)

    ws_socket = None
    try:
        ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)
        print(f"Connecting to WebSocket URL: {ws_url}")
        ws_socket = create_websocket_connection(ws_url)

        # Inject JS once
        inject_js_only(ws_socket)

        # Send notification and remove empty collections
        result = send_launcher_notification(ws_socket, removed_message, removed_apps)

    except Exception as e:
        print(f"Failed to send removal notification or cleanup collections: {e}")

    finally:
        if ws_socket:
            ws_socket.close()

    directories = [
        os.path.join(logged_in_home, 'Desktop'),
        os.path.join(logged_in_home, '.local', 'share', 'applications')
    ]

    for game_name in removed_game_names:
        base_game_name = game_name.split(' (')[0].strip().lower()
        desktop_filename = f"{base_game_name}.desktop"

        found_file = False

        print(f"Looking for .desktop file for: {game_name}")

        for directory in directories:
            try:
                files_in_directory = os.listdir(directory)
            except Exception as e:
                continue

            for f in files_in_directory:
                if f.lower() == desktop_filename:
                    full_path = os.path.join(directory, f)
                    try:
                        os.remove(full_path)
                        print(f"Deleted .desktop file for: {game_name} from {directory}")
                    except Exception as e:
                        print(f"Failed to delete {full_path} due to: {e}")
                        continue
                    found_file = True


        if not found_file:
            print(f"No .desktop file found for: {game_name}")


