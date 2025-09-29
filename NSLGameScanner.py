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
import certifi
import glob
import itertools
from datetime import datetime

from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote
from base64 import b64encode
import xml.etree.ElementTree as ET

import socket
import base64

from urllib.parse import urlparse
import http.client


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
    with open(env_vars_path, 'w') as f:
        pass

print(f"Env vars file path is: {env_vars_path}")

# Read variables from the file
with open(env_vars_path, 'r') as f:
    lines = f.readlines()

# Determine which lines to keep
modified = False
separate_appids = None
lines_to_keep = []

# Lines to remove
remove_lines = {'chromelaunchoptions', 'websites_str'}

for line in lines:
    original_line = line  # Keep the original line for writing later
    if line.startswith('export '):
        line = line[7:]  # Remove 'export '

    # Parse the name and value
    if '=' in line:
        name, value = line.strip().split('=', 1)
        os.environ[name] = value

        # Track separate_appids if explicitly set to false
        if name == 'separate_appids' and value.strip().lower() == 'false':
            separate_appids = value.strip()

    # Only keep lines that do not contain the unwanted keys
    if not any(remove_key in original_line for remove_key in remove_lines):
        lines_to_keep.append(original_line)
    else:
        modified = True  # Mark as modified if a line is removed

# If there were changes, write the cleaned-up lines back to the file
if modified:
    with open(env_vars_path, 'w') as f:
        f.writelines(lines_to_keep)





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
purpleshortcutdirectory = os.environ.get('purpleshortcutdirectory')
plariumshortcutdirectory = os.environ.get('plariumshortcutdirectory')
vfunshortcutdirectory = os.environ.get('vfunshortcutdirectory')
temposhortcutdirectory = os.environ.get('temposhortcutdirectory')
poketcgshortcutdirectory = os.environ.get('poketcgshortcutdirectory')
antstreamshortcutdirectory = os.environ.get('antstreamshortcutdirectory')
stoveshortcutdirectory = os.environ.get('stoveshortcutdirectory')
repaireaappshortcutdirectory = os.environ.get('repaireaappshortcutdirectory')
#Streaming
chromedirectory = os.environ.get('chromedirectory')
websites_str = os.environ.get('custom_websites_str')
custom_websites = websites_str.split(', ') if websites_str else []





# Fix sys.path insertion to avoid duplicates
parent_folder = os.path.expanduser(f"{logged_in_home}/.config/systemd/user/Modules")

if parent_folder not in sys.path:
    sys.path.insert(0, parent_folder)

print(sys.path)

# Now import your modules after the single insert
import requests
import vdf
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
RestartSec=30
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
    file_path = f"{logged_in_home}/.steam/root/userdata/{steamid3}/config/grid/{filename}"

    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)





    if os.path.exists(file_path):
        if art_type == 'icons':
            print(f"Icon artwork for {game_id} already exists. Skipping download.")
            with open(file_path, 'rb') as image_file:
                return b64encode(image_file.read()).decode('utf-8')
        else:
            print(f"{art_type} artwork already exists, but skipping file read. Will redownload for base64.")


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



                    if art_type == 'icons':
                        with open(alt_file_path, 'wb') as file:
                            file.write(response.content)
                        print(f"Downloaded and saved icon to: {alt_file_path}")
                    else:
                        print(f"Downloaded {art_type} artwork as base64 (not saved to disk)")
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




steam_applist_cache = None

def get_steam_store_appid(steam_store_game_name):
    search_url = f"{BASE_URL}/search/{steam_store_game_name}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and data['data']:
            steam_store_appid = data['data'][0].get('steam_store_appid')
            if steam_store_appid:
                print(f"Found App ID for {steam_store_game_name} via primary source: {steam_store_appid}")
                return steam_store_appid
    except requests.exceptions.RequestException as e:
        print(f"Primary store App ID lookup failed for {steam_store_game_name}: {e}")

    # Fallback using Steam AppList (cached)
    global steam_applist_cache
    if steam_applist_cache is None:
        try:
            STEAM_BASE_URL = "https://api.steampowered.com"
            app_list_url = f"{STEAM_BASE_URL}/ISteamApps/GetAppList/v2/"
            response = requests.get(app_list_url)
            response.raise_for_status()
            steam_applist_cache = response.json()['applist']['apps']
            print("Cached Steam app list from Steam API.")
        except requests.exceptions.RequestException as e:
            print(f"Steam AppList fallback failed for {steam_store_game_name}: {e}")
            return None

    for app in steam_applist_cache:
        if steam_store_game_name.lower() in app['name'].lower():
            print(f"Found App ID for {steam_store_game_name} via cached Steam AppList: {app['appid']}")
            return app['appid']

    print(f"No App ID found for {steam_store_game_name} in cached Steam AppList.")
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
            response = requests.head(url, timeout=3)
            if response.status_code == 200:
                return url
        except requests.RequestException as e:
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



# === CONFIGURATION ===
WS_HOST = "localhost"
WS_PORT = 8080
TARGET_TITLE = "SharedJSContext"

JS_CODE = """
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
      await SteamClient.Apps.SetShortcutSortAs(shortcutId, data.Launcher.trim());
      console.log("Sort As title set to:", data.Launcher.trim());
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

    // --- Notification ---
    try {
      await sleep(300);
      const notificationPayload = {
        rawbody: data.appname + " was added to your library!",
        state: "ingame"
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

    return { success: true, shortcutId };

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






###For Uninstall Notifications only
def send_steam_notification(ws_socket, message_text):
    notify_id = next(eval_id_counter)

    js_notify = f"""
    (function() {{
        if (window.SteamClient && SteamClient.ClientNotifications) {{
            const payload = {{
                rawbody: {json.dumps(message_text)},
                state: "ingame"
            }};
            const jsonStr = JSON.stringify(payload);
            SteamClient.ClientNotifications.DisplayClientNotification(3, jsonStr, function(arg) {{
                console.log("Notification callback", arg);
            }});
            return true;
        }} else {{
            console.warn("SteamClient.ClientNotifications not available");
            return false;
        }}
    }})()
    """

    send_ws_text(ws_socket, json.dumps({
        "id": notify_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_notify,
            "awaitPromise": False,
            "returnByValue": True
        }
    }))

    # Optional: wait for a response if needed
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
            wrapped_code = f"(async () => {{ {JS_CODE}; window.__injectedSteamMod = true; return 'Injected'; }})()"
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

    # Exclude Chrome and AppID 0
    if 'chrome' in launchoptions or '--appid 0' in launchoptions:
        print("Exclusion: Chrome or AppID 0 detected.")
        return None

    # Exclude based on app regions like jp., com., online.
    if any(x in launchoptions for x in ['jp.', 'com.', 'online.']):
        print("Exclusion: App region detected.")
        if steam_compat_marker not in launchoptions:
            print(f"Exclusion: {steam_compat_marker} not in launch options.")
            return None

    # If none of the exclusions apply, return the compat tool name
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
    if appname in ['Epic Games', 'Gog Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App', 'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client', 'Rockstar Games Launcher', 'Glyph', 'Minecraft Launcher', 'Playstation Plus', 'VK Play', 'HoYoPlay', 'Nexon Launcher', 'Game Jolt Client', 'Artix Game Launcher', 'ARC Launcher', 'PURPLE Launcher', 'Plarium Play', 'VFUN Launcher', 'Tempo Launcher', 'Pokémon Trading Card Game Live', 'Antstream Arcade', 'STOVE Client']:
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
                response = requests.head(url)
                if response.status_code == 200:
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
                    img_data = requests.get(url).content
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
        if result and 'result' in result:
            value = result['result']['result'].get('value')
            if isinstance(value, dict) and value.get('success'):
                shortcut_id = value.get('shortcutId')
                print("App ID returned from JS:", shortcut_id)




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
        pattern = re.compile(r"(UMU|GE)-Proton-(\d+(?:\.\d+)*)(?:-(\d+(?:\.\d+)*))?")

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
        response = requests.get(CSV_URL, timeout=5)
        response.raise_for_status()
        csv_data = [row for row in csv.DictReader(response.text.splitlines())]
        print("Fetched UMU database from online as fallback.")
    except requests.exceptions.RequestException as e:
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





def track_create_entry(directory, name, launch_options, starting_dir):
    if not any([directory, launch_options, starting_dir]):
        return  # Skip if not installed

    create_new_entry(directory, name, launch_options, starting_dir)
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
track_create_entry(os.environ.get('repaireaappshortcutdirectory'), 'Repair EA App', os.environ.get('repaireaapplaunchoptions'), os.environ.get('repaireaappstartingdir'))





create_new_entry(os.environ.get('chromedirectory'), 'Xbox Game Pass', os.environ.get('xboxchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Better xCloud', os.environ.get('xcloudchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'GeForce Now', os.environ.get('geforcechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Boosteroid Cloud Gaming', os.environ.get('boosteroidchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Stim.io', os.environ.get('stimiochromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WatchParty', os.environ.get('watchpartychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Netflix', os.environ.get('netflixchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Hulu', os.environ.get('huluchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Tubi', os.environ.get('tubichromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Disney+', os.environ.get('disneychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Prime Video', os.environ.get('amazonchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Youtube', os.environ.get('youtubechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Youtube TV', os.environ.get('youtubetvchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Amazon Luna', os.environ.get('lunachromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Twitch', os.environ.get('twitchchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Venge', os.environ.get('vengechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Rocketcrab', os.environ.get('rocketcrabchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Fortnite', os.environ.get('fortnitechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Cloudy Pad', os.environ.get('cloudychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WebRcade', os.environ.get('webrcadechromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'WebRcade Editor', os.environ.get('webrcadeeditchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'Afterplay.io', os.environ.get('afterplayiochromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'OnePlay', os.environ.get('oneplaychromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'AirGPU', os.environ.get('airgpuchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'CloudDeck', os.environ.get('clouddeckchromelaunchoptions'), os.environ.get('chrome_startdir'))
create_new_entry(os.environ.get('chromedirectory'), 'JioGamesCloud', os.environ.get('jiochromelaunchoptions'), os.environ.get('chrome_startdir'))
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
    'PURPLE Launcher': 'PURPLELauncher',
    'Plarium Play': 'PlariumLauncher',
    'VFUN Launcher': 'VFUNLauncher',
    'Tempo Launcher': 'TempoLauncher',
    'Pokémon Trading Card Game Live': 'PokeTCGLauncher',
    'Antstream Arcade': 'AntstreamLauncher',
    'STOVE Client': 'STOVELauncher',
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
            exe_path = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe\""
            start_dir = f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/\""
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
                    # Replace \x2122 with trademark symbol
                    raw_name = raw_name.replace(r'\x2122', '™')
                    # Decode other escaped sequences like \x21 etc.
                    name = bytes(raw_name, "utf-8").decode("unicode_escape")
                    # Fix mojibake by re-encoding/decoding
                    name = fix_encoding(name)
                    games[current_id] = name
                    current_id = None

    return games

def get_ea_app_game_info(installed_games, game_directory_path, sys_reg_file=None):
    # If provided, parse the sys reg file once for fallback IDs
    sys_reg_games = {}
    if sys_reg_file and os.path.isfile(sys_reg_file):
        try:
            sys_reg_games = extract_games_fixed(sys_reg_file)
            # Reverse mapping for lookup by game name:
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

            matched_id = None  # Track fallback match

            # If no ID found in XML, fallback to sys reg lookup by matching name
            if not ea_ids and sys_reg_name_to_id:
                print(f"No ID found in XML for '{game_name}', looking in system registry fallback...")

                # Match game_name exactly or case-insensitive if needed
                for reg_name, reg_id in sys_reg_name_to_id.items():
                    if reg_name == game_name:
                        matched_id = reg_id
                        break
                if matched_id:
                    ea_ids = matched_id

            if ea_ids:
                if matched_id:
                    print(f"Found ID in system registry fallback for '{game_name}': {ea_ids}")
                else:
                    print(f"Found ID in XML for '{game_name}': {ea_ids}")
                game_dict[game_name] = ea_ids
            else:
                print(f"Skipping '{game_name}' - no OfferID found in installerdata.xml or sys reg fallback.")

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

    # Replace glob: /run/media/deck/*/{folder_name}/
    for folder_name in ["EA Games", "Origin Games"]:
        if os.path.isdir(base_path):
            for user_folder in os.listdir(base_path):
                full_path = os.path.join(base_path, user_folder, folder_name)
                if os.path.isdir(full_path):
                    possible_paths.append(full_path)

    # Replace glob: /run/media/deck/*/*/
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
            continue  # Permission errors etc.

    return [p for p in possible_paths if os.path.isdir(p)]



if not ea_app_launcher:
    print("EA App launcher ID not set. Skipping EA App Scanner.")
else:
    # 1. Try default and legacy EA Games paths
    default_paths = [
        f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/EA Games/",
        f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files (x86)/EA Games/"
    ]

    game_directory_path = None
    for path in default_paths:
        if os.path.isdir(path):
            game_directory_path = path
            break

    detected_path = find_ea_games_path_from_registry()
    if detected_path and os.path.isdir(detected_path):
        game_directory_path = detected_path

    # 3. Check external SD card folders
    if not os.path.isdir(game_directory_path):
        external_paths = find_external_game_paths()
        if external_paths:
            game_directory_path = external_paths[0]
            print(f"Using external EA App game path: {game_directory_path}")

    # Final scan
    if not os.path.isdir(game_directory_path):
        print("EA App game data not found. Skipping EA App Scanner.")
    else:
        try:
            installed_games = [g for g in os.listdir(game_directory_path) if os.path.isdir(os.path.join(game_directory_path, g))]

            # Pass sys reg file path here for fallback (adjust the path accordingly)
            sys_reg_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/system.reg"

            game_dict = get_ea_app_game_info(installed_games, game_directory_path, sys_reg_file=sys_reg_path)

            for game, ea_ids in game_dict.items():
                launch_options = f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/" %command% "origin2://game/launch?offerIds={ea_ids}"'
                exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EALaunchHelper.exe"'
                start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{ea_app_launcher}/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/"'

                create_new_entry(exe_path, game, launch_options, start_dir, launcher_name="EA App")
                track_game(game, "EA App")
        except Exception as e:
            print(f"Error scanning EA App games: {e}")

# End of EA App Scanner



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
            create_new_entry(exe_path, game, launch_options, start_dir, launcher_name="GOG Galaxy")
            track_game(game, "GOG Galaxy")

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



# chrome bookmark scanner for xbox and geforce

# Path to the Chrome Bookmarks file
bookmarks_file_path = f"{logged_in_home}/.var/app/com.google.Chrome/config/google-chrome/Default/Bookmarks"

# Check if the bookmarks file exists
if not os.path.exists(bookmarks_file_path):
    print("Chrome Bookmarks not found. Skipping scanning for Bookmarks.")
else:
    # Lists to store results
    geforce_now_urls = []
    xbox_urls = []
    luna_urls = []

    with open(bookmarks_file_path, 'r') as f:
        data = json.load(f)

    # Loop through the "Other bookmarks" folder
    for item in data['roots']['other']['children']:
        if item['type'] == "url":
            name = item['name'].strip()
            url = item['url']

            if not name:
                continue
                
            # GeForce NOW
            if "play.geforcenow.com/games" in url:
                if name == "GeForce NOW":
                    continue
                game_name = name.replace(" on GeForce NOW", "").strip()
                url = url.split("&")[0] if "&" in url else url
                geforce_now_urls.append(("GeForce NOW", game_name, url))


            # Xbox Cloud Gaming
            elif "www.xbox.com/en-US/play/games/" in url:
                # Clean up the name
                if name.startswith("Play "):
                    game_name = name.replace("Play ", "").split(" |")[0].strip()
                else:
                    game_name = name.split(" |")[0].strip()

                if game_name:
                    xbox_urls.append(("Xbox", game_name, url))

            # Amazon Luna
            elif "luna.amazon.com/game/" in url:
                # Clean up the name
                if name.startswith("Play "):
                    game_name = name.replace("Play ", "").split(" |")[0].strip()
                else:
                    game_name = name.split(" |")[0].strip()

                if game_name:
                    luna_urls.append(("Amazon Luna", game_name, url))

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


        # Replace this with whatever function or method you're using to handle the entries
        create_new_entry(
            chromedirectory,
            game_name,
            chromelaunch_options,
            chrome_startdir,
            launcher_name="Google Chrome"
        )
        track_game(game_name, "Google Chrome")

#end of chrome scanner for xbox and geforce bookmarks






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

    exe_path = f'{logged_in_home}/Android_Waydroid/Android_Waydroid_Cage.sh'
    start_dir = f'{logged_in_home}/Android_Waydroid/'

    if os.path.isdir(applications_dir):
        for file_name in os.listdir(applications_dir):
            if not file_name.endswith(".desktop") or file_name in ignored_files:
                continue

            file_path = os.path.join(applications_dir, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    if "waydroid" not in content:
                        continue

                parser = configparser.ConfigParser(strict=False)
                parser.read(file_path)

                display_name = parser.get("Desktop Entry", "Name", fallback=None)
                exec_cmd = parser.get("Desktop Entry", "Exec", fallback="")

                if not display_name or "waydroid app launch" not in exec_cmd:
                    continue

                parts = exec_cmd.strip().split()
                app_name = parts[-1] if len(parts) >= 3 else None
                if not app_name:
                    continue

                create_new_entry(
                    shortcutdirectory=f'"{exe_path}"',
                    appname=display_name,
                    launchoptions=f'"{app_name}"',
                    startingdir=start_dir,
                    launcher_name="Waydroid"
                )
                track_game(display_name, "Waydroid")

            except Exception as e:
                print(f"Failed to process {file_name}: {e}")
    else:
        print(f"Applications directory not found: {applications_dir}")
#end of waydroid scanner





#Flatpak Scanner
flatpak_apps = [
    {
        "id": "com.nvidia.geforcenow",
        "display_name": "NVIDIA GeForce NOW"
    },
    {
        "id": "com.moonlight_stream.Moonlight",
        "display_name": "Moonlight Game Streaming"
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

    # Custom launch options for Moonlight
    if app_id == "com.moonlight_stream.Moonlight":
        app_launch_options = '"run" "--branch=stable" "--arch=x86_64" "--command=moonlight" "com.moonlight_stream.Moonlight"'
    else:
        app_launch_options = f"run {app_id}"

    create_new_entry(
        shortcutdirectory=f'"{exe_path}"',
        appname=display_name,
        launchoptions=app_launch_options,
        startingdir=f'"{start_dir}"'
    )

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
            search_pattern = os.path.join(linux_games_dir, "*/combinedata_manifest/GameManifest_*.upf")
            manifest_files = glob.glob(search_pattern)

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







# Call finalize_tracking and capture removed apps
removed_apps = finalize_tracking()

# List of game names to skip fetching descriptions for
skip_games = {'Epic Games', 'GOG Galaxy', 'Ubisoft Connect', 'Battle.net', 'EA App',
    'Amazon Games', 'itch.io', 'Legacy Games', 'Humble Bundle', 'IndieGala Client',
    'Rockstar Games Launcher', 'Glyph', 'Minecraft Launcher', 'Playstation Plus',
    'VK Play', 'HoYoPlay', 'Nexon Launcher', 'Game Jolt Client', 'Artix Game Launcher',
    'PURPLE Launcher', 'Plarium Play', 'VFUN Launcher', 'Tempo Launcher', 'ARC Launcher',
    'Pokémon Trading Card Game Live', 'Antstream Arcade', 'STOVE Client', 'Xbox Game Pass',
    'Better xCloud', 'GeForce Now', 'Boosteroid Cloud Gaming', 'Stim.io', 'WatchParty',
    'Netflix', 'Hulu', 'Tubi', 'Disney+', 'Amazon Prime Video', 'Youtube', 'Youtube TV',
    'Amazon Luna', 'Twitch', 'Venge', 'Rocketcrab', 'Fortnite', 'WebRcade', 'Cloudy Pad',
    'WebRcade Editor', 'Afterplay.io', 'OnePlay', 'AirGPU', 'CloudDeck', 'JioGamesCloud',
    'Plex', 'Apple TV+', 'Crunchyroll', 'PokéRogue', 'NonSteamLaunchers', 'Repair EA App'}




# --- Game Descriptions Update Logic ---
def update_game_details(games_to_check, logged_in_home, skip_games):
    descriptions_file_path = os.path.join(logged_in_home, '.config/systemd/user/descriptions.json')

    def create_descriptions_file():
        if not os.path.exists(descriptions_file_path):
            try:
                with open(descriptions_file_path, 'w') as file:
                    json.dump([], file, indent=4)
                print(f"{descriptions_file_path} created successfully.")
            except IOError as e:
                print(f"Error creating {descriptions_file_path}: {e}")

    def load_game_data():
        create_descriptions_file()
        try:
            with open(descriptions_file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def game_exists_in_data(existing_data, game_name):
        return any(game['game_name'] == game_name for game in existing_data)

    def get_game_details(game_name):
        url = f"https://nonsteamlaunchers.onrender.com/api/details/{game_name}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to retrieve data for {game_name}. Status code {response.status_code}")
            return None

    def strip_html_tags(text):
        return re.sub(r'<[^>]*>', '', text)

    def decode_html_entities(text):
        return text.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2019", "'").replace("\u2122", "™")

    def write_game_details(existing_data, game_details):
        if not game_details:
            return existing_data

        if 'about_the_game' in game_details:
            if game_details['about_the_game'] is not None:
                game_details['about_the_game'] = strip_html_tags(game_details['about_the_game'])
                game_details['about_the_game'] = decode_html_entities(game_details['about_the_game'])
            else:
                game_details['about_the_game'] = None

        if 'game_details' in game_details:
            del game_details['game_details']

        if not game_exists_in_data(existing_data, game_details['game_name']):
            existing_data.append(game_details)
            print(f"Game details for {game_details['game_name']} added successfully.")
        else:
            print(f"Game details for {game_details['game_name']} already exist.")

        return existing_data

    existing_data = load_game_data()
    changed = False

    for game_name in games_to_check:
        if game_name.lower() in (label.lower() for label in skip_games):
            continue

        existing_game = next((game for game in existing_data if game['game_name'] == game_name), None)
        if existing_game and existing_game.get('about_the_game') is None:
            continue

        if not game_exists_in_data(existing_data, game_name):
            game_details = get_game_details(game_name)
            if game_details:
                existing_data = write_game_details(existing_data, game_details)
                changed = True
            else:
                existing_data = write_game_details(existing_data, {
                    "game_name": game_name,
                    "about_the_game": None
                })
                print(f"Inserted placeholder with null for {game_name}")
                changed = True

    if changed:
        try:
            with open(descriptions_file_path, 'w', encoding='utf-8') as file:
                json.dump(existing_data, file, indent=4, ensure_ascii=False)

            print(f"Updated {descriptions_file_path} with new game details.")
        except IOError as e:
            print(f"Error writing to {descriptions_file_path}: {e}")
    else:
        print("No new game details added.")
# --- End of Game Descriptions Update Logic ---



# --- Boot Video Logic ---
def get_boot_video(game_name, logged_in_home):
    # Dynamically build the list of app names to exclude from API requests
    excluded_apps = skip_games

    OVERRIDE_PATH = os.path.expanduser(f'{logged_in_home}/.steam/root/config/uioverrides/movies')
    REQUEST_RETRIES = 5

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
                response = requests.get(download_url)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {file_path}")
                else:
                    print(f"Failed to download {file_path}, status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Download failed for {file_path}: {e}")
        else:
            print("No download URL found for video.")

    try:
        # Check if the game_name is in the excluded list and skip if so
        if game_name.lower() in [app.lower() for app in excluded_apps]:
            print(f"Skipping boot video for {game_name}, as it's in the excluded apps list.")
            return  # Skip downloading this video

        for _ in range(REQUEST_RETRIES):
            try:
                response = requests.get('https://steamdeckrepo.com/api/posts/all', verify=certifi.where())
                if response.status_code == 200:
                    data = response.json().get('posts', [])
                    break
                elif response.status_code == 429:
                    raise Exception('Rate limit exceeded, try again in a minute')
                else:
                    print(f'steamdeckrepo fetch failed, status={response.status_code}')
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
        else:
            raise Exception(f'Retry attempts exceeded')

        # Use the game_name directly instead of splitting it into words
        search_terms = [game_name.lower()]

        # Attempt to find a matching boot video for the full game name
        for term in search_terms:
            filtered_videos = sorted(
                (
                    {
                        'id': entry['id'],
                        'name': entry['title'],
                        'preview_video': entry['video'],
                        'download_url': f'https://steamdeckrepo.com/post/download/{entry["id"]}',
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if term in entry['title'].lower() and
                    entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'], reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]
                print(f"🎬 Downloading boot video: {video['name']}")
                download_video(video, OVERRIDE_PATH)
                return  # Exit after downloading the first matching video

        # If no video was found, check if the game_name has more than one word and use the first two words
        if len(game_name.split()) > 1:
            first_two_words = ' '.join(game_name.split()[:2]).lower()

            filtered_videos = sorted(
                (
                    {
                        'id': entry['id'],
                        'name': entry['title'],
                        'preview_video': entry['video'],
                        'download_url': f'https://steamdeckrepo.com/post/download/{entry["id"]}',
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if first_two_words in entry['title'].lower() and
                    entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'], reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]
                download_video(video, OVERRIDE_PATH)
                return  # Exit after downloading the first matching video

        # If no video was found at all
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

            update_game_details([name], logged_in_home, skip_games)

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
    removed_game_names = []
    for launcher, apps in removed_apps.items():
        removed_game_names.extend([f"{app} ({launcher})" for app in apps])

    removed_message = "Removed from library:\n" + "\n".join(removed_game_names)

    try:
        # Only connect & inject JS if a game was actually removed
        ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE)
        ws_socket = create_websocket_connection(ws_url)
        inject_js_only(ws_socket)

        send_steam_notification(ws_socket, removed_message)
    except Exception as e:
        print("Failed to send removal notification:", e)
    finally:
        ws_socket.close()
