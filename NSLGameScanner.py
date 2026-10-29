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
import platform
import subprocess
import sqlite3
import csv
import configparser
import itertools
import fcntl
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
from concurrent.futures import ThreadPoolExecutor



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
xodusnexusshortcutdirectory = os.environ.get('xodusnexusshortcutdirectory')
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




LOCK_FILE = "/tmp/nslgamescanner.lock"

def single_instance():
    global lockfile
    lockfile = open(LOCK_FILE, "w")

    try:
        fcntl.flock(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("Another instance is already running. Exiting.")
        sys.exit(0)

single_instance()


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




#Artwork
api_cache = {}
BASE_URL = "https://www.steamgriddb.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
}


HARDCODED_GAME_IDS = {
    "Disney+": 5260961,
    "NVIDIA GeForce NOW": 5258450,
    "Battle.net": 5248250,
    "Minecraft for Windows": 38365,

}


def get_json(url, method="GET", data=None):
    headers = HEADERS.copy()

    if data is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(data).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(
        request,
        timeout=15,
    ) as response:
        return json.loads(response.read().decode())


def normalize(name):
    name = re.sub(r"[™®©]", "", name.lower().strip())
    name = re.sub(r"[^\w\s]", "", name)
    return re.sub(r"\s+", " ", name).strip()


def sanitize(name):
    for suffix in (
        ".com", ".net", ".org", ".io", ".co",
        ".tv", ".app", ".edu", ".gov"
    ):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
            break

    return re.sub(r"[^\w\s]", "", name)


def search_games(name):
    params = urllib.parse.urlencode({
        "term": sanitize(name)
    })

    result = get_json(
        f"{BASE_URL}/api/public/search/autocomplete?{params}"
    )

    return result.get("data", [])


def find_game(name):
    if name in HARDCODED_GAME_IDS:
        return {
            "name": name,
            "id": HARDCODED_GAME_IDS[name],
        }

    games = search_games(name)
    target = normalize(name)

    for game in games:
        if normalize(game.get("name", "")) == target:
            return game

    return games[0] if games else None


def get_assets(game_id, asset_type, dimensions="all"):
    cache_key = (
        "assets",
        game_id,
        asset_type,
        dimensions,
    )

    if cache_key in api_cache:
        return api_cache[cache_key]

    payload = {
        "styles": ["all"],
        "languages": ["en"],
        "dimensions": (
            [dimensions]
            if dimensions != "all"
            else ["all"]
        ),
        "formats": ["all"],
        "order": "score_desc",
        "game_id": [game_id],
        "static": True,
        "animated": False,
        "nsfw": False,
        "epilepsy": False,
        "humor": False,
        "untagged": True,
        "asset_type": asset_type,
        "page": 0,
        "limit": 1,
        "user_steam64": None,
        "user_steam64_likes": None,
    }

    try:
        result = get_json(
            f"{BASE_URL}/api/public/search/assets",
            method="POST",
            data=payload,
        )

        assets = result.get("data", {}).get("assets", [])

        api_cache[cache_key] = assets

        return assets

    except Exception as e:
        print(f"Error getting {asset_type} artwork: {e}")
        api_cache[cache_key] = []
        return []


def first_asset(game_id, asset_type, dimensions="all"):
    try:
        assets = get_assets(
            game_id,
            asset_type,
            dimensions,
        )

        return assets[0] if assets else None

    except Exception as e:
        print(
            f"Error getting first {asset_type} asset: {e}"
        )
        return None


def get_grid(game_id):
    return first_asset(
        game_id,
        "grid",
        "600x900",
    )


def get_horizontal_grid(game_id):
    return first_asset(
        game_id,
        "grid",
        "920x430",
    )


def get_game_assets(game_id):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {
            "grid": executor.submit(
                get_grid,
                game_id,
            ),
            "grid_horizontal": executor.submit(
                get_horizontal_grid,
                game_id,
            ),
            "hero": executor.submit(
                first_asset,
                game_id,
                "hero",
            ),
            "logo": executor.submit(
                first_asset,
                game_id,
                "logo",
            ),
            "icon": executor.submit(
                first_asset,
                game_id,
                "icon",
            ),
        }

        assets = {}

        for name, future in futures.items():
            try:
                assets[name] = future.result()

            except Exception as e:
                print(
                    f"Error getting {name} artwork: {e}"
                )
                assets[name] = None

        return assets


def get_assets_for_game(game_name):
    try:
        game = find_game(game_name)

    except Exception as e:
        print(
            f"Error finding SteamGridDB game "
            f"for {game_name}: {e}"
        )
        return None, {}

    if not game:
        print(f"No SteamGridDB game found for: {game_name}")
        return None, {}

    print(
        f"Found SteamGridDB game: "
        f"{game.get('name', game_name)} "
        f"(ID: {game['id']})"
    )

    return game, get_game_assets(game["id"])


def get_sgdb_art(game_id, app_id):
    global grid64
    global gridp64
    global logo64
    global hero64

    print("Finding SteamGridDB artwork...")

    assets = get_game_assets(game_id)

    print("Downloading icons artwork...")

    icon_asset = assets.get("icon")

    if icon_asset:
        download_artwork(
            icon_asset,
            "icons",
            app_id,
        )
    else:
        print("No icon artwork found.")

    print("Downloading logos artwork...")

    logo_asset = assets.get("logo")

    if logo_asset:
        logo64 = download_artwork(
            logo_asset,
            "logos",
            app_id,
        )
    else:
        print("No logo artwork found.")
        logo64 = None

    print("Downloading heroes artwork...")

    hero_asset = assets.get("hero")

    if hero_asset:
        hero64 = download_artwork(
            hero_asset,
            "heroes",
            app_id,
        )
    else:
        print("No hero artwork found.")
        hero64 = None

    print("Downloading grids artwork of size 600x900...")

    gridp_asset = assets.get("grid")

    if gridp_asset:
        gridp64 = download_artwork(
            gridp_asset,
            "grids",
            app_id,
            "600x900",
        )
    else:
        print("No 600x900 grid artwork found.")
        gridp64 = None

    print("Downloading grids artwork of size 920x430...")

    grid_asset = assets.get("grid_horizontal")

    if grid_asset:
        grid64 = download_artwork(
            grid_asset,
            "grids",
            app_id,
            "920x430",
        )
    else:
        print("No 920x430 grid artwork found.")
        grid64 = None


def download_artwork(
    artwork,
    art_type,
    shortcut_id,
    dimensions=None,
):
    if artwork is None:
        print(
            f"No artwork supplied for {art_type}. "
            "Skipping download."
        )
        return None

    if dimensions is not None:
        filename = get_file_name(
            art_type,
            shortcut_id,
            dimensions,
        )
    else:
        filename = get_file_name(
            art_type,
            shortcut_id,
        )

    file_path = (
        f"{logged_in_home}/.steam/root/userdata/"
        f"{steamid3}/config/grid/{filename}"
    )

    grid_folder_path = os.path.dirname(file_path)

    if not os.path.exists(grid_folder_path):
        os.makedirs(
            grid_folder_path,
            exist_ok=True,
        )

        print(
            f"Created grid folder at: "
            f"{grid_folder_path}"
        )

    if file_exists_with_any_ext(file_path):
        print(
            f"Artwork for {art_type} already exists. "
            "Skipping download."
        )

        with open(file_path, "rb") as image_file:
            return b64encode(
                image_file.read()
            ).decode("utf-8")

    image_url = artwork.get("url")

    if not image_url:
        print(
            f"No artwork URL available for "
            f"{art_type}."
        )
        return None

    print(
        f"Downloading {art_type} artwork from: "
        f"{image_url}"
    )

    try:
        req = urllib.request.Request(
            image_url
        )

        req.add_header(
            "User-Agent",
            "Mozilla/5.0 (X11; Linux x86_64)",
        )

        req.add_header(
            "Referer",
            "https://www.steamgriddb.com/",
        )

        with urllib.request.urlopen(
            req,
            timeout=15,
        ) as response:
            if response.status != 200:
                raise Exception(
                    f"Failed to download artwork, "
                    f"status code {response.status}"
                )

            image_data = response.read()

        mime = artwork.get("mime", "").lower()

        if art_type == "icons":
            if "ico" in mime:
                extension = "ico"
            else:
                extension = "png"
        else:
            extension = "png"

        alt_file_path = file_path.replace(
            ".png",
            f".{extension}",
        )

        with open(
            alt_file_path,
            "wb",
        ) as file:
            file.write(image_data)

        print(
            f"Downloaded and saved {art_type} "
            f"to: {alt_file_path}"
        )

        return b64encode(
            image_data
        ).decode("utf-8")

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        Exception,
    ) as e:
        print(
            f"Error downloading {art_type} artwork: {e}"
        )
        return None



def get_game_id(game_name):
    print(f"Searching for game ID for: {game_name}")

    try:
        game = find_game(game_name)

        if game:
            game_id = game["id"]
            print(
                f"Found game ID: {game_id}"
            )
            return game_id

        print(
            f"No game ID found for game name: {game_name}"
        )
        return None

    except Exception as e:
        print(f"Error searching for game ID: {e}")
        return None



def get_file_name(
    art_type,
    shortcut_id,
    dimensions=None,
):
    singular_art_type = art_type.rstrip("s")

    if art_type == "icons":
        if os.path.exists(
            f"{logged_in_home}/.steam/root/userdata/"
            f"{steamid3}/config/grid/"
            f"{shortcut_id}-{singular_art_type}.png"
        ):
            return (
                f"{shortcut_id}-"
                f"{singular_art_type}.png"
            )
        else:
            return (
                f"{shortcut_id}-"
                f"{singular_art_type}.ico"
            )

    elif art_type == "grids":
        if dimensions == "600x900":
            return f"{shortcut_id}p.png"
        else:
            return f"{shortcut_id}.png"

    elif art_type == "heroes":
        return f"{shortcut_id}_hero.png"

    elif art_type == "logos":
        return f"{shortcut_id}_logo.png"

    else:
        return f"{shortcut_id}.png"


def is_match(name1, name2):
    if name1 and name2:
        return (
            name1.lower() in name2.lower()
            or name2.lower() in name1.lower()
        )
    else:
        return False



steam_applist_cache = None


def get_steam_store_appid(steam_store_game_name):

    global steam_applist_cache
    if steam_applist_cache is None:
        steam_applist_cache = {}

    def normalize_name(name):
        name = name.lower()
        name = re.sub(r'[®™]', '', name)
        name = re.sub(r'[-–—:]', ' ', name)
        name = ' '.join(name.split())
        return name

    if steam_store_game_name not in steam_applist_cache:
        time.sleep(0.5)

        query = urllib.parse.quote(steam_store_game_name)
        url = f"https://store.steampowered.com/api/storesearch/?term={query}&l=english&cc=US"

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.load(response)

            if not data.get("items"):
                relaxed_name = steam_store_game_name.replace(" - ", " ")
                relaxed_query = urllib.parse.quote(relaxed_name)
                relaxed_url = f"https://store.steampowered.com/api/storesearch/?term={relaxed_query}&l=english&cc=US"

                print(f"No exact Steam results. Trying relaxed search: {relaxed_name}")

                with urllib.request.urlopen(relaxed_url, timeout=10) as response:
                    data = json.load(response)

        except (urllib.error.URLError, Exception) as e:
            print(f"Fallback Steam lookup failed for {steam_store_game_name}: {e}")
            return None

        target = normalize_name(steam_store_game_name)
        fallback_appid = None

        for item in data.get("items", []):
            item_name = normalize_name(item.get("name", ""))

            if item_name == target:
                fallback_appid = str(item.get("id"))
                break

            if target in item_name or item_name in target:
                fallback_appid = str(item.get("id"))
                print(f"Using partial Steam match: {item.get('name')} ({fallback_appid})")
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
        try:
            url = f"https://steamcommunity.com/app/{steam_store_appid}"

            with urllib.request.urlopen(url) as response:
                html = response.read().decode("utf-8")

            match = re.search(
                rf"/apps/{steam_store_appid}/([a-f0-9]{{40}})(?:_full)?\.jpg",
                html,
                re.IGNORECASE,
            )

            if not match:
                return None

            hash_value = match.group(1)

            candidates = [
                f"https://shared.fastly.steamstatic.com/"
                f"community_assets/images/apps/{steam_store_appid}/{hash_value}_full.jpg",

                f"https://shared.fastly.steamstatic.com/"
                f"community_assets/images/apps/{steam_store_appid}/{hash_value}.jpg",
            ]

        except (urllib.error.URLError, Exception) as e:
            print(f"Error getting Steam icon for App ID {steam_store_appid}: {e}")
            return None

    elif art_type == "logos":
        candidates = [
            base_url + "logo_2x.png",
            base_url + "logo.png",
        ]

    elif art_type == "heroes":
        candidates = [
            base_url + "library_hero_2x.jpg",
            base_url + "library_hero.jpg",
        ]

    elif art_type == "grids_600x900":
        candidates = [
            base_url + "library_600x900_2x.jpg",
            base_url + "library_600x900.jpg",
        ]

    elif art_type == "grids_920x430":
        candidates = [
            base_url + "header_2x.jpg",
            base_url + "header.jpg",
        ]

    else:
        return None

    for url in candidates:
        try:
            with urllib.request.urlopen(url) as response:
                if response.status == 200:
                    return url
        except (urllib.error.URLError, Exception) as e:
            print(f"Error checking fallback URL: {url} — {e}")

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

            if os.path.lexists(app_file_path):
                os.remove(app_file_path)
                print(f"Removed existing applications file: {app_file_path}")

            with open(app_file_path, "w") as file:
                file.write(content)

            print(f"Created updated .desktop file: {app_file_path}")

            original_desktop_path = os.path.join(desktop_dir, filename)

            if os.path.lexists(original_desktop_path):
                os.remove(original_desktop_path)
                print(f"Removed existing Desktop entry: {original_desktop_path}")

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

        # Same target already added by another tool under its own wrapper/name
        # (e.g. ArmadaOS wraps Xodus games and Flatpaks with armada-game-launch)
        if is_wrapped_duplicate(s, stripped_exe_path, launch_options):
            print(f"Existing shortcut for the same target found for {display_name}. Skipping creation.")
            return True

    return False


ARMADA_LAUNCH_WRAPPER = "/usr/libexec/armada/armada-game-launch"


def wrap_for_armada(launch_options):
    # ArmadaOS applies per-game FEX/driver tweaks through this wrapper, but armada-control only
    # wraps shortcuts at startup; add it now in the same format so new shortcuts get it too
    if not os.path.exists(ARMADA_LAUNCH_WRAPPER):
        return launch_options
    opts = launch_options or ""
    if ARMADA_LAUNCH_WRAPPER in opts:
        return opts
    wrapped = f"{ARMADA_LAUNCH_WRAPPER} %command%"
    if "%command%" in opts:
        return opts.replace("%command%", wrapped, 1)
    return f"{wrapped} {opts.strip()}" if opts.strip() else wrapped


def strip_nsl_additions(launch_options):
    """Launch options without what NSL or ArmadaOS add around them, to tell NSL defaults from user edits"""
    return " ".join(
        token
        for token in (launch_options or "").split()
        if token not in (ARMADA_LAUNCH_WRAPPER, "LD_PRELOAD=", "/usr/bin/env", "%command%")
        and not token.startswith("FEX_APP_CONFIG=")
    )


def shortcut_target(exe):
    quoted = re.match(r'"([^"]*)"', exe or "")
    return os.path.basename(quoted.group(1) if quoted else (exe or "").strip())


def find_outdated_nsl_shortcut(appname, exe, launch_options):
    """The existing shortcut for appname if it still has an earlier NSL target or launch options, else None.

    NSL fixes change some launchers' targets (ARC's virtual desktop) or launch options (no Steam overlay for
    Heroic and Amazon, Amazon's FEX profile), but existing shortcuts are never touched again, so move the ones
    still on NSL's earlier values over. Anything the user edited is left alone.
    """
    for s in shortcuts['shortcuts'].values():
        if (s.get('appname') or s.get('AppName')) != appname:
            continue
        current_exe = s.get('exe') or s.get('Exe') or ''
        current_options = s.get('LaunchOptions') or ''
        if current_exe == exe and current_options == launch_options:
            return None
        target = shortcut_target(current_exe)
        if target and target in exe and strip_nsl_additions(current_options) == strip_nsl_additions(launch_options):
            return s
    return None


def is_wrapped_duplicate(shortcut, exe_path, launch_options):
    if not exe_path or not launch_options:
        return False
    try:
        key = shlex.split(launch_options)[-1]  # game id / Flatpak app id
    except ValueError:
        return False
    if len(key) < 8 or key.startswith(("%", "-")):
        return False
    target = os.path.basename(exe_path.rstrip("/"))
    combined = f"{shortcut.get('exe') or shortcut.get('Exe') or ''} {shortcut.get('LaunchOptions') or ''}"
    return key in combined and target in combined


# Start of Refactoring code from the .sh file


track_game, finalize_tracking = scan_and_track_games(logged_in_home, steamid3)





# === CONFIGURATION ===
WS_HOST = "localhost"
WS_PORT = 8080
TARGET_TITLE = "SharedJSContext"
TARGET_TITLE2 = "Steam"
TARGET_TITLE3 = "Steam Big Picture Mode"
TARGET_TITLE4 = r"^MainMenu_uid\d+$"




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
      try {
        await SteamClient.Apps.SpecifyCompatTool(shortcutId, compatTool);
        console.log("Compat tool set to " + compatTool);
      } catch (compatErr) {
        console.warn("Failed to set compat tool '" + compatTool + "', falling back to 'proton_experimental':", compatErr);
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
if (window.__REAL_PLAYTIME_LOADED__) {
} else {
    window.__REAL_PLAYTIME_LOADED__ = true;

    if (localStorage.getItem("realPlaytimeData") !== null) {
        localStorage.removeItem("realPlaytimeData");
        console.log("Removed deprecated 'realPlaytimeData' from localStorage.");
    }

    const pending = new Set();
    const playtimeCache = new Map();

    async function fetchAndCachePlaytime(appId) {
        if (pending.has(appId)) return;
        pending.add(appId);
        try {
            const playtime = await SteamClient.Apps.GetPlaytime(appId);
            if (playtime) {
                playtimeCache.set(appId, {
                    forever: Number(playtime.nPlaytimeForever) || 0,
                    twoWeeks: Number(playtime.nPlaytimeLastTwoWeeks) || 0,
                    lastPlayed: Number(playtime.rtLastTimePlayed) || 0
                });
            }
        } catch (err) {
            console.warn("Steam playtime fetch failed:", err);
        } finally {
            pending.delete(appId);
        }
    }

    // Keep track of running states to detect when a game session ends
    const runningStates = new Map();

    function applyPlaytime(appOverview) {
        if (!appOverview || appOverview.app_type !== 1073741824) return;

        const rawId = typeof appOverview.appid === "function"
            ? appOverview.appid()
            : appOverview.appid ?? appOverview.appId;

        const appId = Number(rawId);
        if (!Number.isFinite(appId) || appId <= 0) return;

        const isRunning = !!appOverview.bIsRunning;
        const wasRunning = runningStates.get(appId) || false;

        // If the game just closed (was running, now it's not), drop the cache to force a fresh Steam fetch
        if (wasRunning && !isRunning) {
            playtimeCache.delete(appId);
        }
        runningStates.set(appId, isRunning);

        if (!playtimeCache.has(appId)) {
            fetchAndCachePlaytime(appId).then(() => {
                appOverview.TriggerChange?.();
            });
        }

        const cached = playtimeCache.get(appId);
        if (cached) {
            appOverview.minutes_playtime_forever = cached.forever;
            appOverview.nPlaytimeForever = cached.forever;

            appOverview.minutes_playtime_last_two_weeks = cached.twoWeeks;
            appOverview.nPlaytimeLastTwoWeeks = cached.twoWeeks;

            if (cached.lastPlayed > 0) {
                appOverview.rt_last_time_played = cached.lastPlayed;
            }

            appOverview.TriggerChange?.();
        }
    }

    function patchAppStore() {
        const store = window.appStore;
        if (!store || store.__playtimeGettersPatched) return;

        if (typeof store.GetAppOverviewByAppID === "function") {
            const originalGet = store.GetAppOverviewByAppID;
            store.GetAppOverviewByAppID = function(appId) {
                const overview = originalGet.call(this, appId);
                applyPlaytime(overview);
                return overview;
            };
        }

        if (store.m_mapApps) {
            const map = store.m_mapApps;
            const originalSet = map.set;
            map.set = function(appId, overview) {
                applyPlaytime(overview);
                return originalSet.call(this, appId, overview);
            };
        }

        store.__playtimeGettersPatched = true;
    }

    function patchAppInfoStore() {
        const info = window.appInfoStore;
        if (!info || typeof info.OnAppOverviewChange !== "function" || info.__playtimePatched) return;

        const original = info.OnAppOverviewChange;
        info.OnAppOverviewChange = function(apps) {
            for (const app of apps || []) {
                const rawId = typeof app?.appid === "function" ? app.appid() : app?.appid;
                const overview = rawId != null
                    ? window.appStore?.GetAppOverviewByAppID(Number(rawId)) || app
                    : app;
                applyPlaytime(overview);
            }
            return original.apply(this, arguments);
        };

        info.__playtimePatched = true;
    }

    function init() {
        if (!window.appStore || !window.SteamClient?.Apps?.GetPlaytime) {
            setTimeout(init, 1000);
            return;
        }

        patchAppStore();
        patchAppInfoStore();

        if (window.appStore.m_mapApps) {
            for (const overview of window.appStore.m_mapApps.values()) {
                applyPlaytime(overview);
            }
        }
    }

    init();
}
"""




THEMEMUSIC_CODE = r"""
(function () {
    "use strict";

    if (window.__THEMEMUSIC_LOADED__) return;
    window.__THEMEMUSIC_LOADED__ = true;

    const LOCAL_STORAGE_KEY = "ThemeMusicData";
    const PLAYER_ID = "steam-theme-youtube";
    const YOUTUBE_ID_REGEX = /^[A-Za-z0-9_-]{11}$/;
    const MAX_SESSION_SONGS = 10;

    const sessionSongQueues = new Map();
    const sessionSearchCache = new Map();
    const reactPropsKeys = new WeakMap();
    const reactFiberKeys = new WeakMap();

    let ytAudioIframe = null;
    let detectedGame = null;
    let currentQuery = null;
    let currentVideoId = null;
    let searchingForGame = null;
    let observerScheduled = false;

    let gameModeContainer = null;
    let gameModeContainerValid = false;
    let cachedGameModeGame = null;
    let cachedDesktopGame = null;
    let cachedDesktopGameKey = null;

    let desktopControlState = null;
    let desktopControlStateTime = 0;
    let gameModeControlState = null;
    let gameModeControlStateTime = 0;

    let cacheData = null;
    let isNavigatingThemeMusic = false;

    const getThemeKey = (name) => {
        if (!name) return "";
        return name.endsWith(" Theme Music") ? name : `${name} Theme Music`;
    };

    function getReactKey(el, weakMap, prefix) {
        if (!el) return null;
        const cached = weakMap.get(el);
        if (cached !== undefined) return cached;
        const key = Object.keys(el).find(k => k.startsWith(prefix)) || null;
        weakMap.set(el, key);
        return key;
    }

    const getReactPropsKey = (el) => getReactKey(el, reactPropsKeys, "__reactProps");
    const getReactFiberKey = (el) => getReactKey(el, reactFiberKeys, "__reactFiber");

    function loadCache() {
        try {
            const raw = localStorage.getItem(LOCAL_STORAGE_KEY);
            if (raw === null) return (cacheData = {});
            const parsed = JSON.parse(raw);
            cacheData = (parsed && typeof parsed === "object" && !Array.isArray(parsed)) ? parsed : {};
        } catch {
            cacheData = {};
        }
        return cacheData;
    }

    function saveCache(data) {
        cacheData = data;
        try {
            localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(data));
        } catch {}
    }

    function masterMusicEnabled() {
        const themeData = loadCache();
        return themeData.themeMusic === undefined ? true : (themeData.themeMusic === true || themeData.themeMusic === "true");
    }

    function currentGameMuted(game = null) {
        const themeData = loadCache();
        const name = game?.name ? getThemeKey(game.name) : (window.__THEMEMUSIC_CURRENT_GAME_NAME__ || themeData.currentlyPlaying?.name);
        if (!name) return false;
        const entry = themeData[name];
        return !!(entry && (entry.muted === true || entry.muted === "true"));
    }

    function isThemeMusicAllowed(game = null) {
        if (!masterMusicEnabled()) return false;
        return !currentGameMuted(game);
    }

    function setCurrentlyPlaying(game, videoId) {
        const cache = loadCache();
        const key = getThemeKey(game.name);
        if (!cache[key]) cache[key] = { muted: false };
        cache[key].videoId = videoId;
        cache[key].timestamp = Date.now();
        cache.currentlyPlaying = {
            name: key,
            videoId,
            timestamp: Date.now()
        };
        saveCache(cache);
    }

    function clearCurrentlyPlaying() {
        const cache = loadCache();
        delete cache.currentlyPlaying;
        saveCache(cache);
    }

    function getCachedVideo(gameName) {
        const cache = loadCache();
        const entry = cache[getThemeKey(gameName)];
        return (entry && typeof entry.videoId === "string" && YOUTUBE_ID_REGEX.test(entry.videoId)) ? entry : null;
    }

    function cacheVideo(game, video) {
        const cache = loadCache();
        const key = getThemeKey(game.name);
        const existing = cache[key] || {};

        cache[key] = {
            ...existing,
            muted: existing.muted ?? false,
            videoId: video.videoId,
            timestamp: Date.now()
        };
        saveCache(cache);
    }

    function getGameOverviewFromFiber(start) {
        let node = start;
        for (let depth = 0; node && depth < 8; depth++) {
            const result = node?.stateNode?.props?.children?.props?.children?.[0]?.props?.overview;
            if (typeof result?.display_name === "string" && result.appid != null) {
                return result;
            }
            node = node.return;
        }
        return null;
    }

    function inspectGameModeContainer(el) {
        const propsKey = getReactPropsKey(el);
        if (!propsKey) return null;
        const innerRef = el[propsKey]?.children?.[0]?.ref?.current?.props?.innerRef?.current;
        if (!innerRef) return null;
        const fiberKey = getReactFiberKey(innerRef);
        return fiberKey ? getGameOverviewFromFiber(innerRef[fiberKey]) : null;
    }

    function getDesktopAppId() {
        const path = window.location?.pathname || "";
        const match = path.match(/\/library\/app\/(\d+)/);
        if (match) return match[1];

        const hash = window.location?.hash || "";
        const hashMatch = hash.match(/\/library\/app\/(\d+)/);
        return hashMatch ? hashMatch[1] : null;
    }

    function getDesktopGame() {
        try {
            const id = getDesktopAppId();
            if (!id) {
                cachedDesktopGame = null;
                cachedDesktopGameKey = null;
                return null;
            }

            if (cachedDesktopGame && cachedDesktopGameKey === id) {
                return cachedDesktopGame;
            }

            const cells = document.querySelectorAll('[role="gridcell"]');
            for (const el of cells) {
                const propsKey = getReactPropsKey(el);
                if (!propsKey) continue;

                const game = el[propsKey]?.children?.[1]?.props?.item;
                if (game?.appid != null && String(game.appid) === id && typeof game.display_name === "string") {
                    cachedDesktopGame = { mode: "desktop", name: game.display_name, appid: String(game.appid) };
                    cachedDesktopGameKey = id;
                    return cachedDesktopGame;
                }
            }

            cachedDesktopGame = null;
            cachedDesktopGameKey = id;
            return null;
        } catch {
            return null;
        }
    }

    function getGameModeContainer() {
        if (gameModeContainerValid && gameModeContainer && document.documentElement.contains(gameModeContainer)) {
            return gameModeContainer;
        }

        gameModeContainer = null;
        gameModeContainerValid = false;

        let bestElement = null;
        let bestArea = 0;

        for (const el of document.querySelectorAll("body *")) {
            const overview = inspectGameModeContainer(el);
            if (!overview) continue;

            const rect = el.getBoundingClientRect();
            if (rect.width <= 0 || rect.height <= 0 || rect.bottom <= 0 || rect.right <= 0) continue;

            const area = rect.width * rect.height;
            if (area > bestArea) {
                bestArea = area;
                bestElement = el;
            }
        }

        if (bestElement) {
            gameModeContainer = bestElement;
            gameModeContainerValid = true;
        }

        return gameModeContainer;
    }

    function getGameModeGame() {
        const container = getGameModeContainer();
        if (!container) {
            cachedGameModeGame = null;
            return null;
        }

        try {
            const overview = inspectGameModeContainer(container);
            if (overview && typeof overview.display_name === "string" && overview.appid != null) {
                cachedGameModeGame = { mode: "game", name: overview.display_name, appid: String(overview.appid) };
                return cachedGameModeGame;
            }
            cachedGameModeGame = null;
            return null;
        } catch {
            return null;
        }
    }

    function getCurrentGame() {
        return getDesktopGame() || getGameModeGame();
    }

    function scanControlState() {
        let foundPlay = false, foundStop = false, foundResume = false;
        const controls = document.querySelectorAll("[role='button'], button, [tabindex]");

        for (const el of controls) {
            const text = (el.innerText || el.textContent || "").replace(/\s+/g, " ").trim().toUpperCase();
            if (!["PLAY", "STOP", "RESUME"].includes(text)) continue;

            const rect = el.getBoundingClientRect();
            if (rect.width <= 0 || rect.height <= 0 || rect.bottom <= 0 || rect.right <= 0) continue;

            if (text === "PLAY") foundPlay = true;
            if (text === "STOP") foundStop = true;
            if (text === "RESUME") foundResume = true;

            if (foundPlay && foundStop && foundResume) break;
        }

        return { foundPlay, foundStop, foundResume };
    }

    function getCachedControlState(currentState, lastTime, ttl) {
        const now = performance.now();
        if (currentState && (now - lastTime < ttl)) return { state: currentState, time: lastTime };
        return { state: scanControlState(), time: now };
    }

    function getDesktopControlState() {
        const res = getCachedControlState(desktopControlState, desktopControlStateTime, 50);
        desktopControlState = res.state;
        desktopControlStateTime = res.time;
        return desktopControlState;
    }

    function getGameModeControlState() {
        const res = getCachedControlState(gameModeControlState, gameModeControlStateTime, 100);
        gameModeControlState = res.state;
        gameModeControlStateTime = res.time;
        return gameModeControlState;
    }

    function invalidateControlState() {
        desktopControlState = null;
        desktopControlStateTime = 0;
        gameModeControlState = null;
        gameModeControlStateTime = 0;
    }

    function checkGameRunning(getStateFn) {
        const state = getStateFn();
        if (state.foundStop || state.foundResume) return true;
        if (state.foundPlay) return false;
        return null;
    }

    const getDesktopGameRunning = () => checkGameRunning(getDesktopControlState);
    const getGameModeGameRunning = () => checkGameRunning(getGameModeControlState);

    const EXCLUDED_PATTERNS = /\b(how\s+to\s+play|tutorial|guitar\s+lesson|piano\s+lesson|cover|remix)\b/i;
    async function ytSearch(query, limit = 20) {
        const api = new URL("https://yt.chocolatemoo53.com/api/v1/search");
        api.searchParams.set("q", query);
        api.searchParams.set("type", "video");

        try {
            const response = await fetch(api);
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            const data = await response.json();
            const videos = [];
            for (const v of data) {
                if (v.type !== "video" || !v.videoId) continue;

                const title = v.title || "";
                const channel = v.author || "";

                const fullText = `${title} ${channel}`;
                if (EXCLUDED_PATTERNS.test(fullText)) continue;

                videos.push({
                    title,
                    channel,
                    videoId: v.videoId,
                    url: `https://www.youtube.com/watch?v=${v.videoId}`
                });

                if (videos.length >= limit) break;
            }

            return videos;
        } catch (error) {
            console.error("Search failed:", error);
            return [];
        }
    }

    async function findYouTubeVideo(gameName) {
        const searches = [
            `${gameName} Game Theme Music`
        ];

        for (const query of searches) {
            const results = await ytSearch(query, 1);
            if (results.length > 0) return results[0];
        }
        return null;
    }

    async function findYouTubeVideos(gameName) {
        if (sessionSearchCache.has(gameName)) {
            return sessionSearchCache.get(gameName);
        }

        const searches = [
            `${gameName} Game Theme Music`
        ];

        const songs = [];
        const seen = new Set();

        for (const query of searches) {
            if (songs.length >= MAX_SESSION_SONGS) break;

            const results = await ytSearch(query, MAX_SESSION_SONGS);
            for (const song of results) {
                if (songs.length >= MAX_SESSION_SONGS) break;
                if (!seen.has(song.videoId)) {
                    seen.add(song.videoId);
                    songs.push(song);
                }
            }
        }

        sessionSearchCache.set(gameName, songs);
        return songs;
    }


    function createYTPlayer(videoId) {
        if (!videoId) return;

        const existing = document.getElementById(PLAYER_ID);
        if (existing) {
            if (existing.getAttribute("src")?.includes(`/embed/${videoId}`)) {
                ytAudioIframe = existing;
                return;
            }
            existing.remove();
            if (ytAudioIframe === existing) ytAudioIframe = null;
        }

        const iframe = document.createElement("iframe");
        iframe.id = PLAYER_ID;
        iframe.src = `https://www.youtube.com/embed/${encodeURIComponent(videoId)}?autoplay=1&loop=1&playlist=${encodeURIComponent(videoId)}&controls=0&rel=0`;
        iframe.allow = "autoplay; encrypted-media";

        Object.assign(iframe.style, {
            position: "fixed",
            width: "1px",
            height: "1px",
            left: "0",
            top: "0",
            border: "0",
            opacity: "0",
            pointerEvents: "none",
            zIndex: "2147483647"
        });

        document.body.appendChild(iframe);
        ytAudioIframe = iframe;
    }

    function stopMusic() {
        if (ytAudioIframe) {
            try { ytAudioIframe.remove(); } catch {}
            ytAudioIframe = null;
        }

        document.getElementById(PLAYER_ID)?.remove();

        currentQuery = null;
        currentVideoId = null;
        clearCurrentlyPlaying();
    }

    function startSong(game, videoId) {
        if (!isThemeMusicAllowed(game)) {
            stopMusic();
            return;
        }

        if (ytAudioIframe) stopMusic();

        currentQuery = game.name;
        currentVideoId = videoId;
        setCurrentlyPlaying(game, videoId);
        createYTPlayer(videoId);
    }

    async function playThemeMusic(game) {
        if (!game) return;

        if (!isThemeMusicAllowed(game)) {
            if (ytAudioIframe) stopMusic();
            return;
        }

        const appid = String(game.appid);
        if (currentQuery === game.name && ytAudioIframe) return;

        const cached = getCachedVideo(game.name);
        if (cached) {
            if (currentVideoId === cached.videoId && ytAudioIframe) {
                currentQuery = game.name;
                setCurrentlyPlaying(game, cached.videoId);
                return;
            }
            startSong(game, cached.videoId);
            return;
        }

        if (searchingForGame === appid) return;
        searchingForGame = appid;

        const found = await findYouTubeVideo(game.name);

        if (searchingForGame !== appid) return;
        searchingForGame = null;

        if (!found || !isThemeMusicAllowed(game)) return;

        const current = getCurrentGame();
        if (!current || String(current.appid) !== appid) return;

        const isRunning = current.mode === "desktop" ? getDesktopGameRunning() : getGameModeGameRunning();
        if (isRunning === true) return;

        cacheVideo(game, found);
        startSong(game, found.videoId);
    }

    async function navigateThemeMusic(direction) {
        const game = detectedGame;
        if (!game || !isThemeMusicAllowed(game) || ![1, -1].includes(direction)) return;

        const appid = String(game.appid);
        let queue = sessionSongQueues.get(appid);

        if (!queue) {
            queue = { songs: [], index: -1, loading: true };
            sessionSongQueues.set(appid, queue);

            if (currentVideoId) {
                queue.songs.push({ videoId: currentVideoId, title: "Currently playing" });
                queue.index = 0;
            }

            try {
                const results = await findYouTubeVideos(game.name);
                const current = getCurrentGame();

                if (String(detectedGame?.appid) !== appid || !current?.appid || String(current.appid) !== appid) {
                    sessionSongQueues.delete(appid);
                    return;
                }

                const seen = new Set(queue.songs.map(song => song.videoId));
                for (const song of results) {
                    if (queue.songs.length >= MAX_SESSION_SONGS) break;
                    if (!seen.has(song.videoId)) {
                        seen.add(song.videoId);
                        queue.songs.push(song);
                    }
                }
            } catch (error) {
                console.error("[ThemeMusic] Failed to build song queue:", error);
                sessionSongQueues.delete(appid);
                return;
            } finally {
                queue.loading = false;
            }
        }

        if (sessionSongQueues.get(appid) !== queue || queue.loading || queue.songs.length === 0) return;
        if (!isThemeMusicAllowed(game)) return;

        const playingIndex = queue.songs.findIndex(song => song.videoId === currentVideoId);
        if (playingIndex >= 0) queue.index = playingIndex;

        let nextIndex = queue.index;
        let song = null;

        for (let i = 0; i < queue.songs.length; i++) {
            nextIndex = (nextIndex + direction + queue.songs.length) % queue.songs.length;
            const candidate = queue.songs[nextIndex];
            if (candidate?.videoId && candidate.videoId !== currentVideoId) {
                song = candidate;
                break;
            }
        }

        if (!song) return;
        queue.index = nextIndex;

        const current = getCurrentGame();
        if (!current || String(current.appid) !== appid || !isThemeMusicAllowed(game)) return;

        // Session-only playback update (No local storage write)
        currentVideoId = song.videoId;
        currentQuery = game.name;
        createYTPlayer(song.videoId);

        selectedSong = {
            name: getThemeKey(game.name),
            videoId: song.videoId
        };

        updateButtonsUI();
        showInlineMessage("Don't like it? Hold 🎵 to 📋/💾.");
    }

    function handleDetectedGame(game) {
        if (!game) return;

        window.__THEMEMUSIC_CURRENT_GAME_NAME__ = getThemeKey(game.name);
        const appid = String(game.appid);
        const changed = !detectedGame || String(detectedGame.appid) !== appid || detectedGame.mode !== game.mode;

        if (changed) {
            if (ytAudioIframe) stopMusic();
            detectedGame = { mode: game.mode, appid, name: game.name };
            searchingForGame = null;
            selectedSong = null;
        }

        updateButtonsUI();

        if (!isThemeMusicAllowed(game)) {
            if (ytAudioIframe) stopMusic();
            return;
        }

        const running = game.mode === "desktop" ? getDesktopGameRunning() : getGameModeGameRunning();

        if (running === true) {
            if (ytAudioIframe) stopMusic();
            return;
        }

        if (running === null) return;

        if (!ytAudioIframe && !isNavigatingThemeMusic) {
            playThemeMusic(game);
        }
    }

    function processGameState() {
        updateButtonsUI();

        if (!masterMusicEnabled()) {
            if (ytAudioIframe) stopMusic();
            return;
        }

        const desktopAppId = getDesktopAppId();
        if (desktopAppId) {
            const desktopGame = getDesktopGame();
            if (desktopGame) {
                handleDetectedGame(desktopGame);
                if (currentGameMuted(desktopGame) && ytAudioIframe) {
                    stopMusic();
                }
                return;
            }
        }

        const gameModeGame = getGameModeGame();
        if (gameModeGame) {
            handleDetectedGame(gameModeGame);
            if (currentGameMuted(gameModeGame) && ytAudioIframe) {
                stopMusic();
            }
            return;
        }

        if (detectedGame?.mode === "game") {
            stopMusic();
            detectedGame = null;
            searchingForGame = null;
            cachedGameModeGame = null;
            gameModeContainer = null;
            gameModeContainerValid = false;
        }
    }

    function scheduleStateCheck() {
        if (observerScheduled) return;
        observerScheduled = true;

        requestAnimationFrame(() => {
            observerScheduled = false;
            invalidateControlState();
            processGameState();
        });
    }

    const IDS = {
        left: "my-custom-left-arrow",
        music: "my-custom-music-button",
        mute: "my-custom-mute-button",
        right: "my-custom-right-arrow",
        message: "my-custom-paste-message"
    };

    const LABEL = "Configure Controller";

    window.music?.cleanup?.();
    window.customPaste?.cleanup?.();

    const el = n => n?.Element || n?.m_element || null;
    const kids = n => Array.isArray(n?.m_rgChildren) ? n.m_rgChildren : [];
    const par = n => n?.Parent || n?.m_Parent || null;

    const listeners = new AbortController();
    const opts = { signal: listeners.signal };

    const buttons = {};
    const navNodes = [];

    let parent;
    let originalStyle;
    let parentNode;
    let message;

    const restoreStyle = () => {
        if (!parent) return;
        if (originalStyle === null) parent.removeAttribute("style");
        else parent.setAttribute("style", originalStyle);
    };

    const cleanup = () => {
        listeners.abort();
        navNodes.forEach(node => {
            try { node.OnUnmount?.(); } catch {}
        });

        Object.values(buttons).forEach(button => button.remove());
        message?.remove();
        restoreStyle();

        if (window.music?.element === buttons.music) delete window.music;
        if (window.customPaste?.cleanup === cleanup) delete window.customPaste;
    };

    const makeButton = (source, id, label, content) => {
        const button = source.cloneNode(true);

        button.id = id;
        button.tabIndex = 0;
        button.setAttribute("aria-label", label);
        button.removeAttribute("aria-describedby");
        button.removeAttribute("disabled");
        button.removeAttribute("aria-disabled");

        button.querySelectorAll("[id],[aria-label]").forEach(node => {
            node.removeAttribute("id");
            node.removeAttribute("aria-label");
        });

        button.replaceChildren();

        const span = document.createElement("span");
        Object.assign(span.style, {
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            height: "100%",
            font: "500 1.1em/1 sans-serif",
            pointerEvents: "none",
            userSelect: "none",
            whiteSpace: "nowrap"
        });

        span.textContent = content;
        button.append(span);

        return button;
    };

    const registerNavigation = (button, navKey, tree, parentNode, referenceNode) => {
        if (!tree || !referenceNode) return null;

        const node = new referenceNode.constructor(tree, parentNode, null);
        node.SetProperties({
            layout: referenceNode.m_Properties?.layout ?? 0,
            focusable: true,
            preferredFocus: false,
            autoFocus: false,
            noFocusRing: referenceNode.m_Properties?.noFocusRing ?? true,
            navKey
        });

        node.OnMount(button);
        navNodes.push(node);

        return node;
    };

    const wireFocus = button => {
        ["focus", "blur", "vgp_onfocus", "vgp_onblur"].forEach((evt, i) => {
            button.addEventListener(evt, () => {
                button.style.filter = i % 2 === 0 ? "brightness(1.15)" : "";
            }, opts);
        });
    };

    const specs = [
        ["left", IDS.left, "Previous theme song", "❮", "custom-left-arrow"],
        ["music", IDS.music, "Music options", "🎵", "custom-music"],
        ["mute", IDS.mute, "Toggle master theme music", "🔇", "custom-mute"],
        ["right", IDS.right, "Next theme song", "❯", "custom-right-arrow"]
    ];

    let selectedSong = null;
    let isHoldingMusic = false;
    let holdStarted = false;
    let holdTimer = null;
    let holdActionInProgress = false;
    let suppressNextClick = false;
    let holdPointerId = null;

    const musicIsAudibleEnabled = () => masterMusicEnabled() && !currentGameMuted();

    const getMasterMuteIcon = () => masterMusicEnabled() ? "🔊" : "🔇";
    const getMusicActionIcon = () => currentGameMuted() ? "🔕" : "🎵";

    const showInlineMessage = (text, isError = false, persistent = false) => {
        if (!message) return;
        message.textContent = text;
        message.style.color = isError ? "#e05252" : "#ffffff";
        message.style.display = "inline-flex";

        if (!persistent) {
            setTimeout(() => {
                if (!holdStarted && !isHoldingMusic && message) {
                    message.style.display = "none";
                }
            }, 3000);
        }
    };

    const updateButtonsUI = () => {
        if (!buttons.mute) return;

        const isMasterEnabled = masterMusicEnabled();

        const otherButtons = [buttons.left, buttons.music, buttons.right];
        otherButtons.forEach(btn => {
            if (btn) {
                btn.style.display = isMasterEnabled ? "" : "none";
            }
        });

        navNodes.forEach(node => {
            const isCollapsible = otherButtons.some(btn => node.m_element === btn);
            if (isCollapsible) {
                try {
                    node.SetProperties({
                        layout: node.m_Properties?.layout ?? 0,
                        focusable: isMasterEnabled,
                        preferredFocus: false,
                        autoFocus: false,
                        noFocusRing: node.m_Properties?.noFocusRing ?? true,
                        navKey: node.m_Properties?.navKey
                    });
                } catch {}

                if (!isMasterEnabled) {
                    if (document.activeElement && otherButtons.includes(document.activeElement)) {
                        buttons.mute?.focus();
                    }
                }
            }
        });

        const muteSpan = buttons.mute.querySelector("span");
        if (muteSpan) muteSpan.textContent = getMasterMuteIcon();
        buttons.mute.setAttribute("aria-label", isMasterEnabled ? "Disable master theme music" : "Enable master theme music");

        if (isMasterEnabled && buttons.music) {
            const musicSpan = buttons.music.querySelector("span");
            if (musicSpan) {
                if (isHoldingMusic && holdStarted) {
                    musicSpan.textContent = selectedSong?.videoId ? "💾" : "📋";
                    buttons.music.setAttribute("aria-label", selectedSong?.videoId ? "Release to save this theme song" : "Release to paste a YouTube link");
                } else {
                    musicSpan.textContent = getMusicActionIcon();
                    buttons.music.setAttribute("aria-label", currentGameMuted() ? "Unmute this game's theme music" : "Mute this game's theme music");
                }
            }
        }

        if (!isMasterEnabled || (!isHoldingMusic && !holdStarted && !message?.textContent)) {
            if (message) message.style.display = "none";
        }
    };

    let isNavigating = false;
    const setNavigationBusy = (busy) => {
        isNavigating = busy;
        [buttons.left, buttons.right].forEach(btn => {
            if (!btn) return;
            btn.disabled = busy;
            btn.style.opacity = busy ? "0.4" : "1";
            btn.style.cursor = busy ? "wait" : "pointer";
        });
    };

    const triggerPreviousSong = async () => {
        if (isNavigating) return;
        setNavigationBusy(true);
        await navigateThemeMusic(-1);
        setNavigationBusy(false);
    };

    const triggerNextSong = async () => {
        if (isNavigating) return;
        setNavigationBusy(true);
        await navigateThemeMusic(1);
        setNavigationBusy(false);
    };

    const performPasteOrSave = async () => {
        if (holdActionInProgress || !musicIsAudibleEnabled()) return;
        holdActionInProgress = true;

        try {
            const themeData = loadCache();
            if (selectedSong?.videoId) {
                const gameName = selectedSong.name || window.__THEMEMUSIC_CURRENT_GAME_NAME__ || themeData.currentlyPlaying?.name;

                if (!gameName) {
                    showInlineMessage("No active game detected!", true);
                    return;
                }

                if (!themeData[gameName]) {
                    themeData[gameName] = { muted: false };
                }

                themeData[gameName].videoId = selectedSong.videoId;
                themeData[gameName].timestamp = Date.now();
                saveCache(themeData);
                showInlineMessage("Theme song saved to storage!");
                selectedSong = null;
                return;
            }

            const text = await navigator.clipboard.readText();
            if (!musicIsAudibleEnabled()) return;

            const match = text.match(/(?:youtube\.com\/.*v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
            if (!match) {
                showInlineMessage("Invalid YouTube link!", true);
                return;
            }

            const newVideoId = match[1];
            const currentThemeName = window.__THEMEMUSIC_CURRENT_GAME_NAME__ || themeData.currentlyPlaying?.name;

            if (!currentThemeName) {
                showInlineMessage("No theme currently playing!", true);
                return;
            }

            if (!themeData[currentThemeName]) {
                themeData[currentThemeName] = { muted: false };
            }

            themeData[currentThemeName].videoId = newVideoId;
            themeData[currentThemeName].timestamp = Date.now();
            saveCache(themeData);

            if (detectedGame && getThemeKey(detectedGame.name) === currentThemeName && isThemeMusicAllowed(detectedGame)) {
                startSong(detectedGame, newVideoId);
            }

            updateButtonsUI();
            showInlineMessage(`Pasted & saved "${currentThemeName}"!`);
        } catch (e) {
            console.error(e);
            showInlineMessage("Failed to read clipboard.", true);
        } finally {
            holdActionInProgress = false;
            isHoldingMusic = false;
            holdStarted = false;
            holdPointerId = null;
            updateButtonsUI();
        }
    };

    const toggleMasterMute = () => {
        const saved = loadCache();
        const newState = !masterMusicEnabled();
        saved.themeMusic = newState;
        saveCache(saved);

        updateButtonsUI();

        if (!newState) {
            stopMusic();
        } else {
            scheduleStateCheck();
        }
    };

    const toggleGameMute = () => {
        if (suppressNextClick || holdStarted || holdActionInProgress) {
            suppressNextClick = false;
            return;
        }

        const saved = loadCache();
        const gameName = window.__THEMEMUSIC_CURRENT_GAME_NAME__ || saved.currentlyPlaying?.name;
        if (!gameName) return;

        if (!saved[gameName]) {
            saved[gameName] = { muted: false };
        }

        const currentMuted = !!(saved[gameName].muted === true || saved[gameName].muted === "true");
        saved[gameName].muted = !currentMuted;

        saveCache(saved);
        updateButtonsUI();

        if (saved[gameName].muted) {
            stopMusic();
        } else {
            scheduleStateCheck();
        }
    };

    function injectButtons() {
        if (document.getElementById(IDS.music)?.isConnected) return;

        const trees = window.opener?.g_WindowFocusCoordinator?.m_rgTrees ?? [];
        const tree = trees.find(entry => entry.tree?.m_ID === "GamepadUI_Full_Root")?.tree;

        const walk = root => {
            const stack = [root];
            const seen = new Set();
            while (stack.length) {
                const n = stack.pop();
                if (!n || seen.has(n)) continue;
                seen.add(n);
                if (el(n)?.getAttribute?.("aria-label") === LABEL) return n;
                stack.push(...kids(n));
            }
            return null;
        };

        const referenceNode = tree?.Root ? walk(tree.Root) : null;
        const fallback = !tree || !referenceNode;

        const source = fallback ? document.querySelectorAll('[aria-label="Manage"]')[1] : el(referenceNode);
        if (!source || (!fallback && !par(referenceNode))) return;

        if (!fallback) parentNode = par(referenceNode);
        parent = source.parentElement;
        if (!parent) return;

        originalStyle = parent.getAttribute("style");
        parent.style.display = "flex";

        navNodes.length = 0;

        specs.forEach(([key, id, label, content, navKey]) => {
            document.getElementById(id)?.remove();
            const button = makeButton(source, id, label, content);
            buttons[key] = button;
            parent.insertBefore(button, source);
            if (!fallback && navKey) registerNavigation(button, navKey, tree, parentNode, referenceNode);
            wireFocus(button);
        });

        buttons.left.addEventListener("click", triggerPreviousSong, opts);
        buttons.left.addEventListener("vgp_onbuttondown", event => {
            if (event.detail?.button === 1 && event.detail.is_repeat !== true) {
                triggerPreviousSong();
            }
        }, opts);

        buttons.right.addEventListener("click", triggerNextSong, opts);
        buttons.right.addEventListener("vgp_onbuttondown", event => {
            if (event.detail?.button === 1 && event.detail.is_repeat !== true) {
                triggerNextSong();
            }
        }, opts);

        buttons.mute.addEventListener("click", (e) => {
            if (e.detail !== 0) toggleMasterMute();
        }, opts);
        buttons.mute.addEventListener("vgp_onbuttondown", event => {
            if (event.detail?.button === 1 && event.detail.is_repeat !== true) {
                toggleMasterMute();
            }
        }, opts);

        if (fallback) {
            const startMusicHold = (event) => {
                if (event.button !== undefined && event.button !== 0) return;
                if (!musicIsAudibleEnabled() || isHoldingMusic) return;

                clearTimeout(holdTimer);
                isHoldingMusic = true;
                holdStarted = false;
                holdPointerId = event.pointerId ?? null;

                holdTimer = setTimeout(() => {
                    if (!isHoldingMusic || !musicIsAudibleEnabled()) {
                        isHoldingMusic = false;
                        holdStarted = false;
                        updateButtonsUI();
                        return;
                    }

                    holdStarted = true;
                    updateButtonsUI();
                    showInlineMessage(selectedSong?.videoId ? "Release to save this theme song." : "Release to paste a YouTube link.", false, true);
                }, 450);
            };

            const endMusicHold = (event) => {
                if (!isHoldingMusic) return;
                if (holdPointerId !== null && event?.pointerId !== undefined && event.pointerId !== holdPointerId) return;

                clearTimeout(holdTimer);
                const wasFourthState = holdStarted;
                isHoldingMusic = false;
                holdStarted = false;
                holdPointerId = null;

                if (wasFourthState) {
                    suppressNextClick = true;
                    setTimeout(() => { suppressNextClick = false; }, 0);
                    if (musicIsAudibleEnabled()) performPasteOrSave();
                    else updateButtonsUI();
                    return;
                }

                updateButtonsUI();
            };

            buttons.music.addEventListener("pointerdown", startMusicHold, opts);
            window.addEventListener("pointerup", endMusicHold, opts);
            window.addEventListener("pointercancel", endMusicHold, opts);
            buttons.music.addEventListener("click", (e) => {
                if (e.detail !== 0) toggleGameMute();
            }, opts);
            buttons.music.addEventListener("contextmenu", event => {
                if (holdStarted) event.preventDefault();
            }, opts);
        } else {
            let controllerHoldTimer = null;
            let isButtonDown = false;

            buttons.music.addEventListener("vgp_onbuttondown", event => {
                if (event.detail?.button === 1 && event.detail.is_repeat !== true) {
                    isButtonDown = true;
                    isHoldingMusic = true;
                    holdStarted = false;
                    clearTimeout(controllerHoldTimer);

                    if (musicIsAudibleEnabled()) {
                        controllerHoldTimer = setTimeout(() => {
                            if (!isButtonDown || !musicIsAudibleEnabled()) return;
                            holdStarted = true;
                            updateButtonsUI();
                            showInlineMessage(selectedSong?.videoId ? "Release to save this theme song." : "Release to paste a YouTube link.", false, true);
                        }, 450);
                    }
                }
            }, opts);

            buttons.music.addEventListener("vgp_onbuttonup", event => {
                if (event.detail?.button === 1) {
                    if (!isButtonDown) return;
                    isButtonDown = false;
                    clearTimeout(controllerHoldTimer);

                    const wasFourthState = holdStarted;
                    holdStarted = false;
                    isHoldingMusic = false;

                    if (wasFourthState) {
                        suppressNextClick = true;
                        setTimeout(() => { suppressNextClick = false; }, 0);

                        if (musicIsAudibleEnabled()) performPasteOrSave();
                        else updateButtonsUI();
                        return;
                    }

                    updateButtonsUI();
                    toggleGameMute();
                }
            }, opts);
        }

        document.getElementById(IDS.message)?.remove();
        message = document.createElement("span");
        message.id = IDS.message;
        message.textContent = "";

        Object.assign(message.style, {
            display: "none",
            alignItems: "center",
            alignSelf: "center",
            marginRight: "10px",
            color: "#e05252",
            font: '500 13px/1.2 "Motiva Sans", Arial, sans-serif',
            whiteSpace: "nowrap",
            pointerEvents: "none",
            userSelect: "none"
        });

        parent.insertBefore(message, buttons.left);
        updateButtonsUI();
    }

    new MutationObserver(mutations => {
        if (mutations.some(m => m.type === "childList")) {
            invalidateControlState();
            gameModeContainerValid = false;
            scheduleStateCheck();
            injectButtons();
        }
    }).observe(document.body, { childList: true, subtree: true });

    window.music = {
        get element() { return buttons.music; },
        cleanup,
        get state() { return getMusicActionIcon(); },
        diagnose: () => ({
            buttonsConnected: Object.fromEntries(Object.entries(buttons).map(([k, b]) => [k, b?.isConnected])),
            musicState: getMusicActionIcon(),
            pasteMessageVisible: message?.style.display !== "none",
            navigationNodes: navNodes.length
        })
    };

    window.customPaste = {
        get left() { return buttons.left; },
        get right() { return buttons.right; },
        get message() { return message; },
        cleanup,
        diagnose: window.music.diagnose
    };

    injectButtons();
    processGameState();

})();
"""





# Utility: Fetch debugger targets with retry
def fetch_targets(host, port, max_retries=15, base_delay=2):
    """Fetch debugger targets from Steam CEF debugger, with retry logic.

    Steam's CEF debugger on port 8080 may not be listening on first run.
    Retries with exponential backoff (capped at 10s) up to max_retries times.

    Old behavior: called sys.exit(0) on any connection failure (silent exit).
    New behavior: retries up to max_retries times, then raises the last error.
    """
    import time

    last_error = None
    for attempt in range(max_retries):
        try:
            conn = http.client.HTTPConnection(host, port, timeout=5)
            conn.request("GET", "/json")
            resp = conn.getresponse()

            if resp.status != 200:
                msg = f"Failed to fetch targets: {resp.status} {resp.reason}"
                print(msg)
                raise Exception(msg)

            data = resp.read()
            targets = json.loads(data)

            if attempt > 0:
                print(f"Connected to Steam debugger on attempt {attempt + 1}/{max_retries}")

            return targets

        except (ConnectionRefusedError, socket.timeout,
                http.client.CannotSendRequest, http.client.RemoteDisconnected,
                OSError, Exception) as e:
            last_error = e
            if attempt < max_retries - 1:
                delay = min(base_delay * (attempt + 1), 10)
                print(f"Steam debugger not ready (attempt {attempt + 1}/{max_retries}), "
                      f"retrying in {delay}s... ({e})")
                time.sleep(delay)
            else:
                print(f"ERROR: Could not connect to Steam debugger at {host}:{port} "
                      f"after {max_retries} attempts.")
                print(f"Make sure Steam is running with these launch options:")
                print(f"  -dev -cef-enable-debugging -cef-single-process")
                raise last_error

        finally:
            try:
                conn.close()
            except:
                pass


# Find websocket debugger URL for the target title
def get_ws_url_by_title(host, port, title):
    targets = fetch_targets(host, port)

    for target in targets:
        target_title = target.get("title", "")

        if re.fullmatch(title, target_title):
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
window.__watcherInjected = 1;

if (!window.__originalOpen) {
    window.__originalOpen = window.open;
    window.__isScreensaverActive = false;

    window.open = function(...args) {
        const popup = window.__originalOpen.apply(this, args);
        try {
            const target = args[1];
            if (target && typeof target === 'string' && target.toLowerCase().includes('screensaver')) {
                window.__isScreensaverActive = true;
                const checkClosed = setInterval(() => {
                    if (popup && popup.closed) {
                        window.__isScreensaverActive = false;
                        clearInterval(checkClosed);
                    }
                }, 1000);
            }
        } catch (e) {}
        return popup;
    };
}


let desktopGameRunning = false, desktopCurrentAppId = null, desktopCurrentGameName = null;
window.__watcherLedSnapshot = null;
window.__watcherLedGeneration = 0;

async function runGameLEDPalette(gameId, gameName) {
    const generation = ++window.__watcherLedGeneration;

    try {
        const [PALETTE_SIZE, QUANTIZE, MIN_DISTANCE, MAX_SAMPLES] = [5,16,55,2e4];
        const sleep = ms => new Promise(r => setTimeout(r, ms));

        const req = window.__steam_require || await new Promise((resolve, reject) => {
            if (typeof window.webpackChunksteamui !== "object") return reject(Error("Steam Webpack runtime not available"));
            let done = 0, finish = (v,e) => {
                if (done) return;
                done = 1;
                e ? reject(e) : (window.__steam_require = v, resolve(v));
            };
            try {
                window.webpackChunksteamui.push([[Math.random()],{},r => finish(r)]);
            } catch(e) {
                finish(null,e);
            }
            setTimeout(() => finish(null,Error("Failed to acquire Steam Webpack runtime")),5e3);
        });

        let LED;
        for (const id of Object.keys(req.m)) {
            try {
                const m = req(id);
                if (m?.Om?.GetState && m.Om.SetColor && m.Om.SetEffect) {
                    LED = m.Om;
                    break;
                }
            } catch {}
        }

        if (!LED) throw Error("LEDManager module not found");

        const getDevices = async () => {
            const r = await LED.GetState({});
            if (!r.BSuccess()) throw Error("LEDManager.GetState failed");
            return r.Body().toObject()?.state?.devices ?? [];
        };

        const color = (id,i,c) => LED.SetColor({device_id:id,color_index:i,color:c});
        const effect = (id,e) => LED.SetEffect({device_id:id,effect:e});

        const apps = appStore.allApps.filter(a => a?.app_type === 1073741824);
        const gid = String(gameId);
        const app = apps.find(a => String(a?.m_gameid) === gid) || apps.find(a => String(a?.appid) === gid);

        if (!app) throw Error(`Non-Steam game not found: ${gameName || gid}`);

        const {appid,display_name,icon_data,icon_data_format} = app;

        if (!icon_data) {
            throw Error(`No icon_data found for ${display_name || gameName || gid} (${appid})`);
        }

        const format = String(icon_data_format || "png").toLowerCase();
        const mime = ({
            ico:"image/x-icon",
            jpg:"image/jpeg",
            jpeg:"image/jpeg",
            webp:"image/webp",
            gif:"image/gif",
            bmp:"image/bmp"
        })[format] || "image/png";

        const img = new Image();
        img.src = `data:${mime};base64,${icon_data}`;

        await new Promise((resolve,reject) => {
            img.onload = resolve;
            img.onerror = () => reject(Error(`Failed to decode Steam icon (${format})`));
        });

        const canvas = document.createElement("canvas");
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;

        const ctx = canvas.getContext("2d",{willReadFrequently:true});
        ctx.drawImage(img,0,0);

        const {data} = ctx.getImageData(0,0,canvas.width,canvas.height);
        const total = canvas.width * canvas.height;
        const step = Math.max(1,Math.floor(total/MAX_SAMPLES));
        const colors = new Map();
        const q = v => Math.floor(v/QUANTIZE)*QUANTIZE + QUANTIZE/2;

        for (let p=0;p<total;p+=step) {
            const o=p*4;
            if (data[o+3]<128) continue;

            const c=[q(data[o]),q(data[o+1]),q(data[o+2])];
            const k=c.join(",");

            colors.set(k,(colors.get(k)||0)+1);
        }

        if (!colors.size) throw Error("Icon contains no usable pixels");

        const dist = (a,b) =>
            Math.hypot(
                a[0]-b[0],
                a[1]-b[1],
                a[2]-b[2]
            );

        const palette = [];

        for (const [k] of [...colors].sort((a,b) => b[1]-a[1])) {
            const c=k.split(",").map(Number);

            if (palette.every(x => dist(c,x)>=MIN_DISTANCE)) {
                palette.push(c);
                if (palette.length===PALETTE_SIZE) break;
            }
        }

        if (!palette.length) throw Error("Could not extract a usable color palette");

        const ledPalette = palette.map(([r,g,b]) => ({
            r:r/255,
            g:g/255,
            b:b/255
        }));

        const devices = await getDevices();

        if (!devices.length) return;

        if (!window.__watcherLedSnapshot) {
            window.__watcherLedSnapshot = devices.map(d => ({
                id:d.id,
                effect:d.effect,
                colors:(d.color??[]).map(({r,g,b}) => ({r,g,b}))
            }));
        }

        if (generation !== window.__watcherLedGeneration) return;

        await Promise.all(
            devices.flatMap(d => {
                const n=d.color?.length??0;

                return Array.from({length:n},(_,i) =>
                    color(
                        d.id,
                        i,
                        ledPalette[
                            Math.min(
                                Math.floor(i*palette.length/n),
                                ledPalette.length-1
                            )
                        ]
                    )
                );
            })
        );

        await Promise.all(
            devices
                .filter(d => d.effects_available?.includes("breath"))
                .map(d => effect(d.id,"breath"))
        );

        await sleep(30e3);

        if (generation !== window.__watcherLedGeneration) return;

        const current = await getDevices();
        const snapshot = window.__watcherLedSnapshot;

        if (!snapshot) return;

        await Promise.all(
            snapshot.flatMap(s => {
                const d=current.find(x => x.id===s.id);

                if (!d) return [];

                return [
                    ...s.colors.map((c,i) => color(s.id,i,c)),
                    ...(s.effect != null ? [effect(s.id,s.effect)] : [])
                ];
            })
        );

        if (generation === window.__watcherLedGeneration) {
            window.__watcherLedSnapshot = null;
        }
    } catch (e) {
        console.log("Game LED palette error:",e);
    }
}

(function() {
    console.log = new Proxy(console.log,{
        apply(target,thisArg,args) {
            try {
                const line=args.join(" ");

                if (line.includes("OnGameActionUserRequest") && line.includes("LaunchApp CreatingProcess")) {
                    const m=line.match(/OnGameActionUserRequest:\s*(\d+)/);

                    if (m && m[1].length>=18 && m[1].length<=20) {
                        const app=appStore.allApps.find(a => String(a.m_gameid)===m[1]);

                        if (app?.app_type===1073741824) {
                            desktopGameRunning=true;
                            desktopCurrentAppId=m[1];
                            desktopCurrentGameName=app.display_name||null;
                        }
                    }
                }

                if (
                    desktopGameRunning &&
                    (
                        line.includes("Removing overlay browser window") ||
                        line.includes("NetworkDiagnosticsStore - unregistering for detailed connection state updates")
                    )
                ) {
                    desktopGameRunning=false;
                    const id=desktopCurrentAppId;

                    if (id) setTimeout(() => {
                        try {
                            SteamClient.Apps.TerminateApp(id,false);

                            if (desktopCurrentAppId===id) {
                                desktopCurrentAppId=desktopCurrentGameName=null;
                            }
                        } catch {}
                    },15e3);
                }
            } catch {}

            return Reflect.apply(target,thisArg,args);
        }
    });
})();

(function() {
    const
        MIN_STATE_GAP_MS=1e3,
        RAPID_TRANSITION_MS=250,
        TERMINATION_DELAY_MS=1e4,
        EXIT_CONFIRMATION_MS=1e4,
        MIN_GAME_RUNTIME_MS=3e4;

    const s={
        gameId:null,
        gameName:null,
        launchTime:0,
        inferredRunning:false,
        watchersEnabled:false,
        terminateScheduled:false,
        possibleExit:false,
        exitCandidateTime:0,
        qamActive:false,
        lastOverlayActive:null,
        lastOverlayChange:0,
        terminateTimer:null,
        exitConfirmationTimer:null
    };

    const clearExit = () => {
        if (s.exitConfirmationTimer) clearTimeout(s.exitConfirmationTimer);

        s.exitConfirmationTimer=null;
        s.possibleExit=false;
        s.exitCandidateTime=0;
    };

    const reset = (id,name) => {
        if (s.terminateTimer) clearTimeout(s.terminateTimer);

        clearExit();

        Object.assign(s,{
            gameId:String(id),
            gameName:name||null,
            launchTime:Date.now(),
            inferredRunning:true,
            watchersEnabled:true,
            terminateScheduled:false,
            possibleExit:false,
            exitCandidateTime:0,
            qamActive:false,
            lastOverlayActive:null,
            lastOverlayChange:0,
            terminateTimer:null
        });

        runGameLEDPalette(s.gameId,s.gameName);
    };

    const activateQAM = () => {
        if (!s.watchersEnabled) return;

        if (s.possibleExit) clearExit();

        s.qamActive=true;
    };

    try {
        if (!console.log.__steamDetectQAMHook) {
            const original=console.log;

            const hook=function(...args) {
                try {
                    if (
                        args.map(v => {
                            try {
                                return typeof v==="string" ? v : String(v);
                            } catch {
                                return "";
                            }
                        })
                        .join(" ")
                        .includes("onGlobalMenuButtonDown SP BPM_uid0")
                    ) {
                        activateQAM();
                    }
                } catch {}

                return original.apply(this,args);
            };

            hook.__steamDetectQAMHook=true;
            console.log=hook;
        }
    } catch {}

    const terminate = () => {
        if (!s.watchersEnabled || !s.gameId || s.terminateScheduled) return;

        s.terminateScheduled=true;

        const id=s.gameId;

        s.terminateTimer=setTimeout(() => {
            s.terminateTimer=null;

            if (s.gameId===id) {
                try {
                    SteamClient.Apps.TerminateApp(id,false);
                } catch {}
            }
        },TERMINATION_DELAY_MS);
    };

    const confirmExit = () => {
        if (
            !s.watchersEnabled ||
            !s.gameId ||
            s.terminateScheduled ||
            s.possibleExit ||
            s.qamActive ||
            window.__isScreensaverActive
        ) return;

        s.possibleExit=true;
        s.exitCandidateTime=Date.now();

        const id=s.gameId;
        const time=s.exitCandidateTime;

        s.exitConfirmationTimer=setTimeout(() => {
            s.exitConfirmationTimer=null;

            if (
                s.gameId!==id ||
                !s.watchersEnabled ||
                !s.possibleExit ||
                s.exitCandidateTime!==time ||
                window.__isScreensaverActive
            ) return;

            if (
                s.qamActive ||
                !s.inferredRunning ||
                s.lastOverlayActive===0
            ) {
                clearExit();
                return;
            }

            s.possibleExit=false;
            s.exitCandidateTime=0;

            terminate();
        },EXIT_CONFIRMATION_MS);
    };

    try {
        SteamClient.Apps.RegisterForGameActionStart((_actionId,id,action) => {
            if (action!=="LaunchApp") return;

            const gameId=String(id);
            const app=appStore.allApps.find(
                a => String(a.m_gameid)===gameId
            );

            if (app?.app_type===1073741824) {
                reset(gameId,app.display_name);
            }
        });
    } catch {}

    try {
        SteamClient.GameSessions.RegisterForAppLifetimeNotifications(evt => {
            if (
                !s.watchersEnabled ||
                String(evt.unAppID)!==String(s.gameId) ||
                window.__isScreensaverActive
            ) return;

            if (evt.bRunning===false && s.inferredRunning) {
                s.inferredRunning=false;
                clearExit();
            } else if (evt.bRunning===true && !s.inferredRunning) {
                s.inferredRunning=true;
            }
        });
    } catch {}

    try {
        const original=SteamClient.Overlay.SetOverlayState;

        SteamClient.Overlay.SetOverlayState=function(gameId,stateNum) {
            if (
                !s.watchersEnabled ||
                String(gameId)!==String(s.gameId)
            ) {
                return original.apply(this,arguments);
            }

            const now=Date.now();
            const prev=s.lastOverlayActive;
            const gap=s.lastOverlayChange
                ? now-s.lastOverlayChange
                : null;

            if (s.qamActive) {
                if (stateNum===0) s.qamActive=false;
            } else if (
                gap===null ||
                gap>=RAPID_TRANSITION_MS
            ) {
                if (
                    s.inferredRunning &&
                    stateNum===3 &&
                    prev===0 &&
                    gap>=MIN_STATE_GAP_MS &&
                    now-s.launchTime>MIN_GAME_RUNTIME_MS &&
                    !s.terminateScheduled &&
                    !s.possibleExit
                ) {
                    confirmExit();
                }

                if (
                    s.possibleExit &&
                    stateNum===0
                ) {
                    clearExit();
                }
            } else if (s.possibleExit) {
                clearExit();
            }

            s.lastOverlayActive=stateNum;
            s.lastOverlayChange=now;

            return original.apply(this,arguments);
        };
    } catch {}
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




### THEMEMUSIC ONLY
eval_id_counter = iter(range(1, 1000000))

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

try:
    for target_title in (TARGET_TITLE2, TARGET_TITLE3):
        if not target_title:
            continue

        try:
            ws_url = get_ws_url_by_title(
                WS_HOST,
                WS_PORT,
                target_title
            )
            ws_socket = create_websocket_connection(ws_url)

            send_ws_text(ws_socket, json.dumps({
                "id": 1,
                "method": "Runtime.enable"
            }))
            recv_ws_message_for_id(ws_socket, 1)

            inject_thememusic_code(ws_socket)

        except Exception as e:
            print(f"Failed with {target_title!r}:", e)

except Exception as e:
    print("Failed while processing TARGET_TITLE2 and TARGET_TITLE3:", e)

#END OF THEMEMUSIC





### METADATA ONLY
METADATA_CODE = r"""
(function () {
    if (window.__MY_METADATA_SCRIPT_LOADED__) return;
    window.__MY_METADATA_SCRIPT_LOADED__ = true;

    const gameCache = {};
    const playerCache = {};
    const hltbCache = {};


    const customGameOverrides = {
        "Xodus Nexus": {
            about_the_game: "Xodus Nexus is an open-source, independent game launcher that allows users to run Microsoft Store and PC Game Pass games locally on Linux systems and the Steam Deck without a Windows installation.",
            developer: "domsvoboda",
            publisher: "",
            release_date: "2026",
            genres: "",
            platforms: "",
            image_url: "",
            metacritic_score: null,
            metacritic_url: null
        }
    };

    async function getSteamPlayerCount(appId) {
        const now = Date.now();
        if (playerCache[appId] && now - playerCache[appId].timestamp < 30000) {
            return playerCache[appId].value;
        }
        try {
            const res = await fetch(`https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid=${appId}`);
            if (!res.ok) return null;
            const data = await res.json();
            const value = data?.response?.player_count ?? null;
            playerCache[appId] = { value, timestamp: now };
            return value;
        } catch {
            return null;
        }
    }

    async function getSteamGameDetails(gameName) {

        if (customGameOverrides[gameName]) {
                return {
                    appid: null,
                    current_players: null,
                    ...customGameOverrides[gameName]
                };
            }


        if (gameCache[gameName]) return gameCache[gameName];
        try {
            const searchRes = await fetch(`https://store.steampowered.com/search/?term=${encodeURIComponent(gameName)}`, { credentials: "omit" });
            const searchHtml = await searchRes.text();
            const searchDoc = new DOMParser().parseFromString(searchHtml, "text/html");
            const results = [...searchDoc.querySelectorAll("a.search_result_row")].map(r => ({
                appid: r.dataset.dsAppid,
                title: r.querySelector(".title")?.innerText.trim()
            }));

            if (!results.length) return await getWikipediaGameDetails(gameName);

            const normalize = str => str?.toLowerCase().replace(/[-()]/g, "").replace(/\s+/g, " ").trim();
            const match = results.find(r => normalize(r.title) === normalize(gameName));
            if (!match) return await getWikipediaGameDetails(gameName);

            const appid = match.appid;
            const apiRes = await fetch(`https://store.steampowered.com/api/appdetails?appids=${appid}`);
            const apiData = await apiRes.json();
            const info = apiData[appid]?.data;

            if (info) {
                const platformsStr = info.platforms ? Object.entries(info.platforms).filter(([k,v]) => v).map(([k]) => k).join(", ") : null;
                const gameData = {
                    appid,
                    about_the_game: info.short_description || null,
                    developer: info.developers?.join(", ") || null,
                    publisher: info.publishers?.join(", ") || null,
                    release_date: info.release_date?.date || null,
                    genres: info.genres?.map(g => g.description).join(", ") || null,
                    platforms: platformsStr,
                    metacritic_score: info.metacritic?.score || null,
                    metacritic_url: info.metacritic?.url || null,
                    image_url: info.screenshots?.[0]?.path_full || null,
                    discounted_price: info.price_overview?.discount_percent > 0 ? info.price_overview.final_formatted : null,
                    discount_percent: info.price_overview?.discount_percent > 0 ? info.price_overview.discount_percent : null,
                    current_players: await getSteamPlayerCount(appid)
                };
                gameCache[gameName] = gameData;
                return gameData;
            }
            return await getWikipediaGameDetails(gameName);
        } catch {
            return await getWikipediaGameDetails(gameName);
        }
    }

    async function getWikipediaGameDetails(gameName) {
        if (gameCache[gameName]) return gameCache[gameName];
        try {
            let gameTitle = gameName.replace(/\s+/g, "_");
            let res = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(gameTitle)}`);
            if (!res.ok) {
                const searchRes = await fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(gameName)}&format=json&origin=*`);
                const searchData = await searchRes.json();
                if (!searchData.query.search.length) return null;
                gameTitle = searchData.query.search[0].title.replace(/\s+/g, "_");
                res = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(gameTitle)}`);
                if (!res.ok) return null;
            }
            const data = await res.json();
            const sentences = data.extract?.match(/[^.!?]+[.!?]+/g) || [];
            const game = {
                appid: null,
                displayTitle: data.displaytitle?.replace(/<[^>]+>/g, "").replace(/\//g, "").trim(),
                about_the_game: sentences.slice(0, 2).join(" ").trim() || data.extract || null,
                developer: null,
                publisher: null,
                release_date: null,
                genres: null,
                platforms: null,
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
                    const labelsRes = await fetch(`https://www.wikidata.org/w/api.php?action=wbgetentities&ids=${idsToResolve.join("|")}&props=labels&languages=en&format=json&origin=*`);
                    labelsData = (await labelsRes.json()).entities || {};
                }

                game.developer = developerId ? labelsData[developerId]?.labels?.en?.value ?? null : null;
                game.publisher = publisherId ? labelsData[publisherId]?.labels?.en?.value ?? null : null;
                game.release_date = releaseTime ? releaseTime.match(/\d{4}/)[0] : null;
                if (genreIds.length) {
                    game.genres = labelsData[genreIds[0]]?.labels?.en?.value?.replace(/\s*\(.*?\)\s*/g, "").trim() || null;
                }
                const platformsClean = platformIds.map(id => labelsData[id]?.labels?.en?.value).filter(Boolean).map(l => l.replace(/\s*\(.*?\)\s*/g, "").trim());
                game.platforms = platformsClean.length ? platformsClean.join(", ") : null;
            }
            gameCache[gameName] = game;
            return game;
        } catch {
            return null;
        }
    }

    async function hltbSearch(query) {
        try {
            const r = await fetch("https://search.tiago.zip/api", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query, type: "web", page: 0 })
            });
            if (!r.ok) return [];
            const data = await r.json();
            return data.results?.web?.results || [];
        } catch {
            return [];
        }
    }
       

    function getMainStory(result) {
        const text = [result.title || "", result.description || "", result.snippet || ""].join(" ").replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
        const match = text.match(/(\d+(?:\.\d+)?[¼½¾]?)\s*Hours?\s*[.\s]*Main Story/i) || text.match(/main objectives.*?about\s+(\d+(?:\.\d+)?[¼½¾]?)\s*Hours?/i);
        return match ? `${match[1]} Hours` : null;
    }

    async function howLongToBeat(gameName) {
        if (hltbCache[gameName]) return hltbCache[gameName];
        const queries = [
            `site:howlongtobeat.com/game/ "${gameName}" "Main Story"`,
            `site:howlongtobeat.com/game/ "${gameName}"`,
            `site:howlongtobeat.com/game/ "${gameName.replace(/ - /g, ': ')}"`,
            `site:howlongtobeat.com/game/ "${gameName.split(" - ")[0]}"`
        ];
        for (const query of queries) {
            const results = await hltbSearch(query);
            for (const result of results) {
                const url = result.url || "";
                if (!/^https:\/\/howlongtobeat\.com\/game\/\d+\/?$/.test(url)) continue;
                const mainStory = getMainStory(result);
                if (mainStory) {
                    const resObj = { game: gameName, mainStory, url };
                    hltbCache[gameName] = resObj;
                    return resObj;
                }
            }
        }
        const resObj = { game: gameName, mainStory: null, url: null };
        hltbCache[gameName] = resObj;
        return resObj;
    }

    function replaceText() {
        document.querySelectorAll("div").forEach(div => {
            if (div.childNodes.length === 1 && div.firstChild.nodeType === Node.TEXT_NODE) {
                const match = div.firstChild.nodeValue.match(/Some detailed information on (.*?) is unavailable/i);
                if (!match) return;
                const gameName = match[1];

                getSteamGameDetails(gameName).then(gameData => {
                    if (!gameData) return;
                    div.textContent = '';
                    const nextDiv = div.nextElementSibling;
                    if (nextDiv) nextDiv.appendChild(div);

                    div.style.position = "relative";
                    div.style.overflow = "hidden";
                    div.style.height = "250px";
                    div.style.borderRadius = "6px";
                    div.style.fontFamily = '"Roboto", "Segoe UI", Tahoma, Geneva, Verdana, sans-serif';
                    div.style.color = "white";
                    div.style.outline = "none";
                    div.style.border = "none";

                    const img = document.createElement('img');
                    img.src = gameData.image_url || "https://images-1.gog-statics.com/6f3d015c3029fea5221ccd9802de5e2f92c6afccc0196b15540677341936a656.jpg";
                    img.alt = gameName;
                    Object.assign(img.style, { width: "100%", height: "100%", objectFit: "cover", position: "absolute", top: "0", left: "0", opacity: "0.5" });

                    const overlay = document.createElement('div');
                    Object.assign(overlay.style, {
                        position: "absolute", top: "0", left: "0", width: "100%", height: "100%",
                        padding: "10px", display: "flex", flexDirection: "column", justifyContent: "flex-start",
                        background: "linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7))"
                    });

                    const contentRow = document.createElement('div');
                    Object.assign(contentRow.style, { display: "flex", flexDirection: "row", flex: "1 1 auto" });

                    const leftColumn = document.createElement('div');
                    Object.assign(leftColumn.style, { display: "flex", flexDirection: "column", alignItems: "flex-start", marginRight: "15px", flexShrink: "0", maxWidth: "250px", overflow: "visible" });

                    let ancestor = div;
                    for (let i = 0; i < 7 && ancestor.parentElement; i++) ancestor = ancestor.parentElement;

                    let foundLauncher = null;
                    for (const child of ancestor.querySelectorAll("div, span, button, a")) {
                        let text = child.textContent?.trim();
                        if (!text || text.length >= 50) continue;
                        text = text.replace(/^Found in these collections/i, "").replace(/\s*\(.*?\)/g, "").trim();
                        if (text) { foundLauncher = text; break; }
                    }

                    const launcherIcons = {
                        "Epic Games": { icon: "https://cdn2.steamgriddb.com/icon/34ffeb359a192eb8174b6854643cc046/32/96x96.png", getUrl: name => `https://store.epicgames.com/browse?q=${encodeURIComponent(name.trim())}&sortBy=relevancy&sortDir=DESC&count=40` },
                        "GOG Galaxy": { icon: "https://cdn2.steamgriddb.com/icon/a928731e103dfc64c0027fa84709689e/32/96x96.png", getUrl: name => `https://www.gog.com/en/game/${name.toLowerCase().replace(/[^a-z0-9 ]/g, "").trim().replace(/\s+/g, "_")}` },
                        "Ubisoft Connect": { icon: "https://cdn2.steamgriddb.com/icon/dabcff9ba10224b01fd2ce83f7d73ad6/32/96x96.png", getUrl: name => `https://www.ubisoft.com/en-us/search?gss-q=${encodeURIComponent(name.trim())}` },
                        "EA App": { icon: "https://cdn2.steamgriddb.com/icon/ff51fb7a9bcb22c595616b4fa368880a/32/96x96.png" },
                        "Amazon Games": "https://cdn2.steamgriddb.com/icon_thumb/6e88ec1459f337d5bea6353f8bff8026.png",
                        "itch.io": "https://cdn2.steamgriddb.com/icon/2ad9e5e943e43cad612a7996c12a8796/32/96x96.png",
                        "Battle.net": "https://cdn2.steamgriddb.com/icon/739465804a0e17d2a47c9bc9c805d60a/32/96x96.png",
                        "Legacy Games": "https://cdn2.steamgriddb.com/icon_thumb/5225802cb9758f9fcd34a679bf9326ec.png",
                        "VK Play": "https://cdn2.steamgriddb.com/icon_thumb/5d35998237b55b8778a75732afc080aa.png",
                        "HoYoPlay": "https://cdn2.steamgriddb.com/icon/817fccd834f01fb5e1770c8679c0824e/32/256x256.png",
                        "Game Jolt Client": "https://cdn2.steamgriddb.com/icon_thumb/17df67628bb89193838f83015a3e7d30.png",
                        "Minecraft Launcher": "https://cdn2.steamgriddb.com/icon/0678c572b0d5597d2d4a6b5bd135754c/32/96x96.png",
                        "Humble Games Collection": "https://cdn2.steamgriddb.com/icon_thumb/3126ed973cbecde2bbffe419f139f456.png",
                        "NVIDIA GeForce NOW": "https://cdn2.steamgriddb.com/icon_thumb/f91ee142269ec908c23e1cd87286e254.png",
                        "Amazon Luna": "https://cdn2.steamgriddb.com/icon/408cebdf5e2849adedc881583586e74d/32/256x256.png",
                        "Xbox Game Pass": "https://cdn2.steamgriddb.com/icon_thumb/ecc6d2386883febda6306bb70216c846.png",
                        "Boosteroid Cloud Gaming": "https://cdn2.steamgriddb.com/icon_thumb/e3998932e2e851de8a24b733628c29de.png",
                        "Waydroid": "https://cdn2.steamgriddb.com/icon_thumb/d6de4f0418bf4015017f5c65cdecc46e.png",
                        "Google Chrome": "https://cdn2.steamgriddb.com/icon/3941c4358616274ac2436eacf67fae05/32/256x256.png",
                        "Brave": "https://cdn2.steamgriddb.com/icon_thumb/192d80a88b27b3e4115e1a45a782fe1b.png",
                        "Vivaldi": "https://cdn2.steamgriddb.com/icon_thumb/51934729f32d36841a17e43e9390483a.png",
                        "Mozilla Firefox": "https://cdn2.steamgriddb.com/icon_thumb/fe998b49c41c4208c968bce204fa1cbb.png",
                        "LibreWolf": "https://cdn2.steamgriddb.com/icon/791608b685d1c61fb2fe8acdc69dc6b5/32/128x128.png",
                        "Microsoft Edge": "https://cdn2.steamgriddb.com/icon_thumb/714cb7478d98b1cb51d1f5f515f060c7.png",
                        "Gryphlink": "https://i.namu.wiki/i/1CZOhlpjxh3owDKXC9axrnMHtotdDaoFMmnzBvQ0yOqCDOL3rIZpH2DyLfX2UCRul9CxIH0gCn1DmRodHnKr6-IUmEzSZpZ6p4r9zRbDvwPe94gZnek0VaIvKfsWsx6L28czwaiz0Mj1NNayAkypNQ.webp",
                        "WebRcade": "https://cdn2.steamgriddb.com/icon_thumb/4916ba26c0ec4e43588dcc3e019ede51.png",
                        "Nintendo": "https://cdn2.steamgriddb.com/icon_thumb/17b6114b9a9b8d8602ec9d9dfeb6a15f.png",
                        "Super Nintendo": "https://cdn2.steamgriddb.com/icon_thumb/d4dcf709a96dca127d0429d73c443afb.png",
                        "Nintendo 64": "https://cdn2.steamgriddb.com/icon_thumb/328de839e30893a67fc55ee2bf2ff5ae.png",
                        "Nintendo GameCube": "https://cdn2.steamgriddb.com/icon/3caf2d9b17ad63105399b122e2061eb1/32/256x256.png",
                        "Nintendo Wii": "https://cdn2.steamgriddb.com/icon_thumb/4c220c393016798aed81f9350e68f61c.png",
                        "Nintendo Wii U": "https://cdn2.steamgriddb.com/icon_thumb/c6c02ef92aa0dcb6c333a27cfb22d47c.png",
                        "Nintendo Switch": "https://cdn2.steamgriddb.com/icon_thumb/3b05af2c48dbaf6656fdf2d2f905b3b6.png",
                        "Sega": "https://cdn2.steamgriddb.com/icon_thumb/bdb4e8e60ca2bd614a1710438b37c08b.png",
                        "PlayStation": "https://cdn2.steamgriddb.com/icon_thumb/f6a81f703854985705a0cc479d221282.png",
                        "PlayStation 2": "https://cdn2.steamgriddb.com/icon/5e3600417e9ac9abf5a6fea026f9b05a/32/256x256.png",
                        "NonSteamLaunchers": "https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/refs/heads/main/logo.png"
                    };

                    const aliasGroups = {
                        "Super Nintendo": ["SNES", "Super NES", "SuperNintendo", "Super Nintendo Entertainment System"],
                        "Nintendo 64": ["N64", "Nintendo64"],
                        "Epic Games": ["Epic Game Store", "Epic Store", "EGS"],
                        "PlayStation": ["PS", "PS1", "Sony PlayStation", "PSX", "PS one", "PSOne", "playstation", "PSP", "PlayStation Portable", "Sony PSP"],
                        "Nintendo GameCube": ["GC", "NGC", "Gamecube", "NintendoGameCube"],
                        "Nintendo Wii": ["Wii", "NintendoWii", "RVL"],
                        "Sega": ["Genesis", "Mega Drive", "Dreamcast", "Saturn", "Game Gear", "Master System", "Sega Genesis", "Sega Dreamcast"],
                        "Nintendo Wii U": ["WiiU", "NintendoWiiU", "Wii U", "Cafe"],
                        "Nintendo Switch": ["Switch", "NintendoSwitch", "NS", "NSW", "HAC"],
                        "NVIDIA GeForce NOW": ["GeForce NOW", "Geforce Now"],
                        "Xbox Game Pass": ["Xbox Game Streaming", "Xbox", "Xbox Cloud Gaming", "Microsoft Xbox", "Windows", "Microsoft Windows"],
                        "Boosteroid Cloud Gaming": ["Boosteroid"]
                    };

                    const launcherAliases = {};
                    for (const [canonical, aliases] of Object.entries(aliasGroups)) {
                        for (const alias of aliases) launcherAliases[alias.trim().toLowerCase()] = canonical;
                        launcherAliases[canonical.trim().toLowerCase()] = canonical;
                    }
                    if (foundLauncher?.includes("NonSteamLaunchers")) foundLauncher = "NonSteamLaunchers";
                    const launcherName = foundLauncher;
                    const resolvedLauncher = launcherName ? (launcherAliases[launcherName.trim().toLowerCase()] || launcherName) : null;
                    const launcherIcon = resolvedLauncher ? launcherIcons[resolvedLauncher] : null;

                    const launcherRow = document.createElement('div');
                    Object.assign(launcherRow.style, { display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px", position: "relative" });

                    if (launcherIcon) {
                        const launcherLink = document.createElement('a');
                        if (typeof launcherIcon !== "string" && launcherIcon.getUrl) {
                            launcherLink.href = launcherIcon.getUrl(gameName);
                            launcherLink.target = "_blank";
                        }
                        Object.assign(launcherLink.style, { display: "inline-flex", alignItems: "center", justifyContent: "center", borderRadius: "10px", transition: "transform 0.15s ease", cursor: "pointer" });
                        launcherLink.onmouseover = () => launcherLink.style.transform = "scale(1.06)";
                        launcherLink.onmouseout = () => launcherLink.style.transform = "scale(1)";

                        const icon = document.createElement('img');
                        icon.src = typeof launcherIcon === "string" ? launcherIcon : launcherIcon.icon;
                        icon.alt = launcherName;
                        Object.assign(icon.style, { width: "60px", height: "60px", objectFit: "contain" });
                        icon.onerror = () => launcherLink.remove();

                        launcherLink.appendChild(icon);
                        launcherRow.appendChild(launcherLink);
                    } else {
                        const blankIcon = document.createElement('div');
                        Object.assign(blankIcon.style, { width: "60px", height: "60px", flexShrink: "0" });
                        launcherRow.appendChild(blankIcon);
                    }

                    leftColumn.appendChild(launcherRow);

                    function createTag(text, fontSize) {
                        const tag = document.createElement('span');
                        tag.textContent = text;
                        Object.assign(tag.style, { fontSize, background: "rgba(36,40,47,0.7)", padding: "3px 8px", borderRadius: "12px", whiteSpace: "normal", display: "inline-block", wordBreak: "break-word", marginRight: "4px", marginBottom: "4px" });
                        return tag;
                    }

                    function createTagRow(items) {
                        const row = document.createElement('div');
                        Object.assign(row.style, { display: "flex", flexWrap: "wrap", gap: "4px" });
                        const fontSize = items.length > 3 ? "7.8px" : "12px";
                        items.forEach(item => row.appendChild(createTag(item, fontSize)));
                        return row;
                    }

                    if (gameData.platforms) leftColumn.appendChild(createTagRow(gameData.platforms.split(",").map(p => p.trim())));
                    if (gameData.developer) leftColumn.appendChild(createTagRow(gameData.developer.split(",").map(d => d.trim())));
                    if (gameData.publisher) leftColumn.appendChild(createTagRow(gameData.publisher.split(",").map(p => p.trim())));
                    if (gameData.release_date) leftColumn.appendChild(createTagRow([gameData.release_date]));
                    if (gameData.genres) leftColumn.appendChild(createTagRow(gameData.genres.split(",").map(g => g.trim())));

                    const rightColumn = document.createElement('div');
                    Object.assign(rightColumn.style, { display: "flex", flexDirection: "column", flex: "1" });

                    const descriptionWrapper = document.createElement('div');
                    Object.assign(descriptionWrapper.style, { position: "relative", width: "100%" });

                    const description = document.createElement('p');
                    description.textContent = gameData.about_the_game || "No description available.";
                    Object.assign(description.style, { fontSize: "14px", lineHeight: "1.4", background: "rgba(36,40,47,0.7)", padding: "8px 12px", borderRadius: "12px", wordBreak: "break-word", overflowWrap: "break-word" });
                    descriptionWrapper.appendChild(description);

                    if (gameData.metacritic_score && gameData.metacritic_url) {
                        const metaTab = document.createElement('a');
                        metaTab.href = gameData.metacritic_url;
                        metaTab.target = "_blank";
                        Object.assign(metaTab.style, {
                            position: "absolute", top: "14px", left: "-18px", display: "flex", flexDirection: "column",
                            alignItems: "center", justifyContent: "center", background: "rgba(36,40,47,0.85)", color: "white",
                            fontSize: "12px", padding: "4px 6px", borderRadius: "8px", textDecoration: "none", cursor: "pointer",
                            boxShadow: "0 2px 6px rgba(0,0,0,0.3)", zIndex: "10"
                        });
                        metaTab.onmouseover = () => metaTab.style.background = "rgba(80,80,80,0.9)";
                        metaTab.onmouseout = () => metaTab.style.background = "rgba(36,40,47,0.85)";

                        const metaLogo = document.createElement('img');
                        metaLogo.src = "https://static.wikia.nocookie.net/logopedia/images/1/1f/Metacritic_2.svg";
                        Object.assign(metaLogo.style, { width: "16px", height: "16px", marginBottom: "2px" });

                        const scoreText = document.createElement('span');
                        scoreText.textContent = gameData.metacritic_score;
                        Object.assign(scoreText.style, { fontWeight: "bold", fontSize: "12px" });

                        const score = parseInt(gameData.metacritic_score, 10);
                        if (score >= 0 && score <= 49) scoreText.style.color = "rgb(139, 75, 90)";
                        else if (score >= 50 && score <= 79) scoreText.style.color = "rgb(166, 106, 58)";
                        else if (score >= 80) scoreText.style.color = "rgb(75, 139, 90)";

                        metaTab.appendChild(metaLogo);
                        metaTab.appendChild(scoreText);
                        descriptionWrapper.appendChild(metaTab);
                    }

                    rightColumn.appendChild(descriptionWrapper);
                    contentRow.appendChild(leftColumn);
                    contentRow.appendChild(rightColumn);
                    overlay.appendChild(contentRow);

                    const bottomLinks = document.createElement('div');
                    Object.assign(bottomLinks.style, {
                        position: "absolute", bottom: "34px", left: "42px", right: "42px",
                        display: "flex", flexWrap: "nowrap", gap: "6px", overflow: "hidden",
                        whiteSpace: "nowrap", scrollBehavior: "smooth", alignItems: "flex-end",
                        height: "42px", paddingLeft: "1px", paddingRight: "6px"
                    });

                    const searchSites = [
                        { name: "Google", url: "https://www.google.com/search?q=", icon: "https://upload.wikimedia.org/wikipedia/commons/2/2f/Google_2015_logo.svg" },
                        { name: "PCGW", url: "https://www.pcgamingwiki.com/w/index.php?search=", extra: "&title=Special%3ASearch", icon: "https://pbs.twimg.com/profile_images/876511628258418689/Joehp5YI_400x400.jpg" },
                        { name: "HLTB", url: "https://howlongtobeat.com/?q=", icon: "https://howlongtobeat.com/favicon.ico" },
                        { name: "SDHQ", url: "https://steamdeckhq.com/?s=", icon: "https://pbs.twimg.com/profile_images/1539310786614419459/5ohiy0ZX_400x400.jpg" },
                        { name: "GOS", url: "https://gamingonsteam.com/?post_type=post&s=", extra: "&btnSubmit=", icon: "https://gamingonsteam.com/wp-content/uploads/2025/12/X-BS-1-e1765643013126.png" },
                        { name: "SteamCharts", url: "https://steamcharts.com/search/?q=", icon: "https://pbs.twimg.com/profile_images/473239151924346880/5k2c-3Hv_400x400.png" },
                        { name: "ProtonDB", url: "https://www.protondb.com/search?q=", icon: "https://www.protondb.com/sites/protondb/images/site-logo.svg" },
                        { name: "SteamInputDB", url: "https://www.steaminputdb.com/config/search?searchtext=", extra: "&sort-by=vote", icon: "https://raw.githubusercontent.com/Alia5/steaminputdb.com/refs/heads/main/logo_mono.svg" },
                        { name: "AWACY", url: "https://areweanticheatyet.com/?search=", icon: "https://areweanticheatyet.com/icon.webp" },
                        { name: "GameFAQs", url: "https://gamefaqs.gamespot.com/search?game=", icon: "https://gamefaqs.gamespot.com/favicon.ico" },
                        { name: "SRC", url: "https://www.speedrun.com/search?q=", icon: "https://avatars.githubusercontent.com/u/11006616?s=200&v=4" }
                    ];

                    searchSites.forEach(site => {
                        const link = document.createElement('a');
                        let gameUrl = site.url + encodeURIComponent(gameName) + (site.extra || "");
                        if (site.name === "SRC") {
                            const slug = gameName.replace(/:/g, '').replace(/[^\w\s]/g, '').trim().replace(/\s+/g, '_');
                            gameUrl = `https://www.speedrun.com/${slug}`;
                        }
                        link.href = gameUrl;
                        link.target = "_blank";
                        Object.assign(link.style, { display: "inline-flex", alignItems: "center", background: "rgba(36,40,47,0.7)", color: "white", fontSize: "13px", padding: "4px 4px", borderRadius: "6px", textDecoration: "none", transition: "background 0.2s" });
                        link.onmouseover = () => link.style.background = "rgba(80,80,80,0.9)";
                        link.onmouseout = () => link.style.background = "rgba(36,40,47,0.7)";

                        const linkIcon = document.createElement('img');
                        linkIcon.src = site.icon;
                        Object.assign(linkIcon.style, { width: "16px", height: "16px", marginRight: "4px" });
                        link.prepend(linkIcon);
                        link.appendChild(document.createTextNode(site.name));

                        if (site.name === "HLTB") {
                            const hltbContainer = document.createElement('div');
                            Object.assign(hltbContainer.style, { position: "relative", display: "inline-flex", alignItems: "center", flexShrink: "0" });

                            const hltbLabel = document.createElement('div');
                            hltbLabel.textContent = "";
                            Object.assign(hltbLabel.style, {
                                position: "absolute", bottom: "100%", left: "50%", transform: "translateX(-50%)",
                                color: "white", fontSize: "10px", fontWeight: "600", lineHeight: "12px",
                                background: "rgba(100, 35, 45, 0.9)", padding: "2px 6px", borderRadius: "6px",
                                whiteSpace: "nowrap", textAlign: "center", boxShadow: "0 2px 4px rgba(0,0,0,0.4)"
                            });

                            hltbContainer.appendChild(hltbLabel);
                            hltbContainer.appendChild(link);
                            bottomLinks.appendChild(hltbContainer);

                            howLongToBeat(gameName).then(res => {
                                if (res?.mainStory) hltbLabel.textContent = res.mainStory;
                            }).catch(() => {});
                        } else if (site.name === "SteamCharts") {
                            const chartContainer = document.createElement('div');
                            Object.assign(chartContainer.style, { position: "relative", display: "inline-flex", alignItems: "center", flexShrink: "0" });

                            const chartLabel = document.createElement('div');
                            chartLabel.textContent = gameData.current_players != null ? "👥 Loading..." : "";
                            Object.assign(chartLabel.style, {
                                position: "absolute", bottom: "100%", left: "50%", transform: "translateX(-50%)",
                                color: "white", fontSize: "10px", fontWeight: "600", lineHeight: "12px",
                                background: "rgba(35, 120, 70, 0.9)", padding: "2px 6px", borderRadius: "6px",
                                whiteSpace: "nowrap", textAlign: "center", boxShadow: "0 2px 4px rgba(0,0,0,0.4)"
                            });

                            chartContainer.appendChild(chartLabel);
                            chartContainer.appendChild(link);
                            bottomLinks.appendChild(chartContainer);

                            if (gameData.current_players != null) {
                                let current = 0, raf;
                                const to = gameData.current_players;
                                const start = performance.now();
                                function frame(now) {
                                    const p = Math.min((now - start) / 1000, 1);
                                    current = Math.round(0 + to * (1 - Math.pow(1 - p, 3)));
                                    chartLabel.textContent = `👥 ${current.toLocaleString()} online`;
                                    if (p < 1) raf = requestAnimationFrame(frame);
                                }
                                raf = requestAnimationFrame(frame);
                            }
                        } else {
                            bottomLinks.appendChild(link);
                        }
                    });

                    if (gameData.discounted_price && gameData.discount_percent) {
                        const slug = gameName.toLowerCase().replace(/[^a-z0-9 ]/g, '').trim().replace(/\s+/g, '-');
                        const itadLink = document.createElement('a');
                        itadLink.href = `https://isthereanydeal.com/game/${slug}/info/`;
                        itadLink.target = "_blank";
                        Object.assign(itadLink.style, {
                            position: "absolute", top: "-2px", right: "12px", zIndex: "10",
                            display: "inline-flex", alignItems: "center", gap: "6px",
                            background: "rgba(36,40,47,0.7)", color: "white", fontSize: "12px",
                            padding: "6px 10px", borderRadius: "10px", textDecoration: "none",
                            width: "max-content", cursor: "pointer", transition: "background 0.2s ease"
                        });
                        itadLink.onmouseover = () => itadLink.style.background = "rgba(80,80,80,0.9)";
                        itadLink.onmouseout = () => itadLink.style.background = "rgba(36,40,47,0.7)";

                        const itadText = document.createElement('span');
                        itadText.textContent = `${gameData.discounted_price} (-${gameData.discount_percent}%)`;
                        Object.assign(itadText.style, { fontWeight: "bold", fontSize: "12px", color: "rgb(75, 139, 90)" });

                        const itadIcon = document.createElement('img');
                        itadIcon.src = "https://isthereanydeal.com/public/assets/logo-GBHE6XF2.svg";
                        Object.assign(itadIcon.style, { width: "16px", height: "16px" });

                        itadLink.appendChild(itadText);
                        itadLink.appendChild(itadIcon);
                        overlay.appendChild(itadLink);
                    }

                    const scrollAmount = 140;
                    const leftArrow = document.createElement('div');
                    leftArrow.innerHTML = "❮";
                    Object.assign(leftArrow.style, {
                        position: "absolute", left: "10px", bottom: "34px", width: "22px", height: "24px",
                        display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer",
                        color: "white", fontSize: "14px", background: "rgba(36,40,47,0.7)", borderRadius: "6px", zIndex: "10"
                    });
                    leftArrow.onmouseover = () => leftArrow.style.background = "rgba(80,80,80,0.9)";
                    leftArrow.onmouseout = () => leftArrow.style.background = "rgba(36,40,47,0.7)";
                    leftArrow.onclick = () => bottomLinks.scrollBy({ left: -scrollAmount, behavior: "smooth" });

                    const rightArrow = document.createElement('div');
                    rightArrow.innerHTML = "❯";
                    Object.assign(rightArrow.style, {
                        position: "absolute", right: "18px", bottom: "34px", width: "22px", height: "24px",
                        display: "flex", alignItems: "center", justifyContent: "center", cursor: "pointer",
                        color: "white", fontSize: "14px", background: "rgba(36,40,47,0.7)", borderRadius: "6px", zIndex: "10"
                    });
                    rightArrow.onmouseover = () => rightArrow.style.background = "rgba(80,80,80,0.9)";
                    rightArrow.onmouseout = () => rightArrow.style.background = "rgba(36,40,47,0.7)";
                    rightArrow.onclick = () => bottomLinks.scrollBy({ left: scrollAmount, behavior: "smooth" });

                    overlay.appendChild(leftArrow);
                    overlay.appendChild(rightArrow);
                    overlay.appendChild(bottomLinks);
                    div.appendChild(img);
                    div.appendChild(overlay);
                });
            }
        });
    }

    replaceText();
    if (!window.steamEnhancerObserver) {
        const observer = new MutationObserver(replaceText);
        observer.observe(document.body, { childList: true, subtree: true });
        window.steamEnhancerObserver = observer;
    }
})();
"""
### METADATA ONLY


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







#Scanner button and control for Frontend
ENVARS_FILE = f"{logged_in_home}/.config/systemd/user/env_vars"
TARGET_TITLES = [TARGET_TITLE2, TARGET_TITLE3]

SCANNER_CODE = r"""
(function () {
    if (window.__MY_SCANNER_LOADED__) return;
    window.__MY_SCANNER_LOADED__ = true;

    const css = (el, s) => Object.assign(el.style, s);

    const style = document.createElement("style");
    style.textContent = `
        .steam-hover { transition: filter 0.12s ease; }
        .steam-hover:hover { filter: brightness(1.25); }
        .no-hover:hover { filter: none !important; }
    `;
    document.head.appendChild(style);

    const findDesktopTarget = () => {
        return [...document.querySelectorAll("div")].find(
            (el) => el.textContent.trim() === "Add a Game"
        );
    };

    const inject = (addGame) => {
        if (!addGame || addGame.parentElement.querySelector(".my-steam-controls")) return;

        const parent = addGame.parentElement;
        css(parent, { position: "relative" });

        const wrapper = document.createElement("div");
        wrapper.className = "my-steam-controls";

        css(wrapper, {
            display: "flex",
            alignItems: "center",
            gap: "8px",
            position: "absolute",
            left: "125px",
            top: "50%",
            transform: "translateY(-50%)",
            zIndex: 9999,
            pointerEvents: "auto"
        });

        let autoScan = window.__scan_state === "ON";
        if (window.__scan_state === "MANUAL") autoScan = false;

        const toggle = document.createElement("div");
        const knob = document.createElement("div");
        const scanBtn = document.createElement("div");
        let scanLocked = false;

        toggle.classList.add("steam-hover");
        scanBtn.classList.add("steam-hover");

        css(toggle, {
            width: "34px", height: "18px", borderRadius: "999px",
            background: "#333", border: "1px solid rgba(255,255,255,0.12)",
            position: "relative", cursor: "pointer", transition: "0.12s ease"
        });

        css(knob, {
            width: "14px", height: "14px", borderRadius: "50%",
            background: "#bbb", position: "absolute", top: "50%", left: "2px",
            transform: "translateY(-50%)", transition: "0.2s"
        });

        toggle.appendChild(knob);

        css(scanBtn, {
            width: "28px", height: "28px", display: "flex",
            alignItems: "center", justifyContent: "center",
            borderRadius: "6px", background: "rgba(255,255,255,0.06)",
            border: "1px solid rgba(255,255,255,0.08)",
            color: "rgba(255,255,255,0.85)", cursor: "pointer",
            transition: "0.12s ease"
        });

        const render = () => {
            const on = autoScan;

            css(toggle, {
                background: on ? "rgba(255,122,24,0.85)" : "#333",
                opacity: scanLocked ? "0.4" : "1",
                pointerEvents: scanLocked ? "none" : "auto"
            });

            knob.style.left = on ? "18px" : "2px";
            knob.style.background = on ? "#fff" : "#bbb";

            scanBtn.style.opacity = autoScan ? "0.4" : "1";
            scanBtn.style.pointerEvents = autoScan ? "none" : "auto";
            scanBtn.style.cursor = autoScan ? "default" : "pointer";

            if (scanLocked) {
                scanBtn.textContent = "⏳";
                scanBtn.style.background = "rgba(255,122,24,0.85)";
                scanBtn.style.border = "none";
            } else {
                scanBtn.style.background = "rgba(255,255,255,0.06)";
                scanBtn.style.border = "1px solid rgba(255,255,255,0.08)";
                if (autoScan) {
                    scanBtn.textContent = "AUTO";
                    scanBtn.style.fontSize = "11px";
                    scanBtn.style.fontWeight = "700";
                } else {
                    scanBtn.textContent = "🔍";
                    scanBtn.style.fontSize = "16px";
                    scanBtn.style.fontWeight = "400";
                }
            }

            toggle.classList.toggle("no-hover", autoScan || scanLocked);
            scanBtn.classList.toggle("no-hover", autoScan || scanLocked);
        };

        toggle.onclick = () => {
            if (scanLocked) return;
            autoScan = !autoScan;
            window.__scan_state = autoScan ? "ON" : "OFF";
            console.log("STATE:", window.__scan_state);
            render();
        };

        scanBtn.onclick = () => {
            if (scanLocked || autoScan) return;
            scanLocked = true;
            autoScan = false;
            window.__scan_event = "MANUAL";
            console.log("EVENT: MANUAL");
            render();
            setTimeout(() => { scanLocked = false; render(); window.__scan_state = "OFF"; }, 30000);
        };

        render();
        wrapper.append(toggle, scanBtn);
        parent.appendChild(wrapper);
    };

    const tryInject = () => {
        const target = findDesktopTarget();
        if (target) inject(target);
    };

    tryInject();

    const observer = new MutationObserver(() => {
        tryInject();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

})();

// Game Mode
(() => {
    "use strict";
    if (window.__NSL_LISTENER_LOADED__) return;
    window.__NSL_LISTENER_LOADED__ = true;

    const channel = new BroadcastChannel("nsl_communication_channel");
    const PAGE_ID = "nsl-config-page";

    function openConfigPage() {
        const existingPage = document.getElementById(PAGE_ID);
        if (existingPage) {
            if (window.__nsl_take_focus) {
                window.__nsl_take_focus();
            }
            return;
        }

        const main = document.getElementById("Main");
        if (!main) return;

        const trees = window.g_WindowFocusCoordinator?.m_rgTrees ?? window.opener?.g_WindowFocusCoordinator?.m_rgTrees ?? [];
        const tree = trees.find(entry => entry.tree?.m_ID === "GamepadUI_Full_Root")?.tree;
        if (!tree?.Root) return;

        const stack = [tree.Root], seen = new Set();
        let refNode = null;
        while (stack.length) {
            const node = stack.pop();
            if (!node || seen.has(node)) continue;
            seen.add(node);
            if (node.Element || node.m_element) { refNode = node; break; }
            if (Array.isArray(node.m_rgChildren)) stack.push(...node.m_rgChildren);
        }
        if (!refNode) return;

        const D3 = refNode.constructor;
        const parent = refNode.Parent || refNode.m_Parent || refNode;
        const original = Array.from(main.children);
        original.forEach(el => { el._nslDisplay = el.style.display; el.style.display = "none"; });

        const page = document.createElement("div");
        page.id = PAGE_ID;
        // Balanced z-index: 10 sits above normal page content, but below Steam's system overlays (1000+)
        page.style.cssText = "position:relative;width:100%;height:100%;overflow-y:auto;background:#171d25;color:#fff;padding:40px;box-sizing:border-box;z-index:10;display:flex;flex-direction:column;gap:24px;font-family:'Motiva Sans',Arial,sans-serif;outline:2px solid transparent;transition:outline-color 0.2s ease;";

        page.innerHTML = `
            <div style="text-align:center;display:flex;flex-direction:column;align-items:center;">
                <h1 style="margin:0;font-size:26px;display:flex;align-items:center;justify-content:center;">
                    N<img src="https://raw.githubusercontent.com/moraroy/NonSteamLaunchersDecky/refs/heads/main/assets/logo.png" alt="NSL" style="height:15px;vertical-align:middle;position:relative;top:3px;">nSteamLaunchers
                </h1>
            </div>
            <div style="display:flex;align-items:center;gap:14px;max-width:650px;width:100%;margin:0 auto;padding:16px 20px;background:#222b38;border:1px solid #2e3b4e;border-radius:8px;box-sizing:border-box;">
                <span style="color:#dcdedf;font-size:16px;font-weight:600;">Scanner</span>
                <div style="flex:1"></div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
                    <div tabindex="0" class="Focusable nsl-toggle" role="switch" aria-checked="false" style="width:42px;height:24px;border-radius:999px;background:#3b4452;border:1px solid rgba(255,255,255,0.12);position:relative;cursor:pointer;box-sizing:border-box;flex-shrink:0;">
                        <div style="width:18px;height:18px;border-radius:50%;background:#8f98a0;position:absolute;top:2px;left:2px;transition:left .2s,background .2s;"></div>
                    </div>
                    <span style="font-size:11px;color:#8f98a0;font-weight:500;">Auto</span>
                </div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
                    <div tabindex="0" class="Focusable nsl-btn" role="button" style="min-width:48px;height:42px;padding:0 8px;display:flex;align-items:center;justify-content:center;box-sizing:border-box;border-radius:6px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);color:rgba(255,255,255,0.9);cursor:pointer;font-size:20px;flex-shrink:0;">🔍</div>
                    <span style="font-size:11px;color:#8f98a0;font-weight:500;">Manual</span>
                </div>
            </div>
            <div style="display:flex;align-items:center;gap:14px;max-width:650px;width:100%;margin:0 auto;padding:16px 20px;background:#222b38;border:1px solid #2e3b4e;border-radius:8px;box-sizing:border-box;">
                <span style="color:#dcdedf;font-size:16px;font-weight:600;">Boot Videos</span>
                <div style="flex:1"></div>
                <div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
                    <div tabindex="0" class="Focusable nsl-boot-toggle" role="switch" aria-checked="false" style="width:42px;height:24px;border-radius:999px;background:#3b4452;border:1px solid rgba(255,255,255,0.12);position:relative;cursor:pointer;box-sizing:border-box;flex-shrink:0;">
                        <div style="width:18px;height:18px;border-radius:50%;background:#8f98a0;position:absolute;top:2px;left:2px;transition:left .2s,background .2s;"></div>
                    </div>
                    <span style="font-size:11px;color:#8f98a0;font-weight:500;">Enable</span>
                </div>
            </div>
            <div style="max-width:650px;width:100%;margin:0 auto;padding:16px 20px;background:#222b38;border:1px solid #2e3b4e;border-radius:8px;box-sizing:border-box;color:#8f98a0;font-size:14px;line-height:1.5;">
                <span style="color:#dcdedf;font-weight:600;display:block;margin-bottom:8px;">Notice</span>
                Hey! Youre using the Desktop Version of NSL (v4.2.93)! Thanks for being cool. As NonSteamLaunchers continues to grow, so will the integration into Steam. The scanner has now been moved here instead of the footer lol, but soon, more options and settings will appear here too............ :) *For now open this page when on the "Home" page, it may break during gameplay.*
            </div>
        `;
        main.appendChild(page);

        const toggle = page.querySelector(".nsl-toggle");
        const knob = toggle.firstElementChild;
        const scanBtn = page.querySelector(".nsl-btn");
        const bootToggle = page.querySelector(".nsl-boot-toggle");
        const bootKnob = bootToggle.firstElementChild;

        if (window.__scan_state === "MANUAL" && window.__nsl_scan_end) {
            if (Date.now() >= window.__nsl_scan_end) {
                window.__scan_state = "OFF";
                window.__nsl_scan_end = 0;
            }
        }

        let autoScan = window.__scan_state === "ON";
        let scanLocked = window.__scan_state === "MANUAL";
        let bootVideos = window.__boot_videos_state === "ON";
        let closed = false, navNodes = [], navObserver = null;

        if (scanLocked && window.__nsl_scan_end) {
            const remaining = window.__nsl_scan_end - Date.now();
            if (remaining > 0) {
                setTimeout(() => {
                    if (closed) return;
                    scanLocked = false;
                    window.__scan_state = "OFF";
                    window.__nsl_scan_end = 0;
                    render();
                }, remaining);
            } else {
                scanLocked = false;
                window.__scan_state = "OFF";
                window.__nsl_scan_end = 0;
            }
        }

        function render() {
            toggle.style.background = autoScan ? "#1a9fff" : "#3b4452";
            toggle.style.opacity = scanLocked ? "0.4" : "1";
            toggle.setAttribute("aria-checked", String(autoScan));
            knob.style.left = autoScan ? "20px" : "2px";
            knob.style.background = autoScan ? "#fff" : "#8f98a0";

            scanBtn.style.opacity = (autoScan || scanLocked) ? "0.4" : "1";
            scanBtn.style.background = scanLocked ? "#1a9fff" : "rgba(255,255,255,0.06)";

            if (scanLocked) {
                scanBtn.textContent = "⏳";
            } else if (autoScan) {
                scanBtn.textContent = "AUTO";
                scanBtn.style.fontSize = "11px";
                scanBtn.style.fontWeight = "700";
            } else {
                scanBtn.textContent = "🔍";
                scanBtn.style.fontSize = "20px";
                scanBtn.style.fontWeight = "400";
            }

            bootToggle.style.background = bootVideos ? "#1a9fff" : "#3b4452";
            bootToggle.setAttribute("aria-checked", String(bootVideos));
            bootKnob.style.left = bootVideos ? "20px" : "2px";
            bootKnob.style.background = bootVideos ? "#fff" : "#8f98a0";

            [toggle, scanBtn, bootToggle].forEach((el) => {
                const focused = el.classList.contains("Focus");
                el.style.outline = focused ? "2px solid #1a9fff" : "none";
            });
        }

        function toggleScanner() {
            if (closed || scanLocked) return;
            autoScan = !autoScan;
            window.__scan_state = autoScan ? "ON" : "OFF";
            render();
        }

        function startManualScan() {
            if (closed || scanLocked || autoScan) return;
            scanLocked = true;
            autoScan = false;
            window.__scan_state = "MANUAL";
            window.__scan_event = "MANUAL";
            window.__nsl_scan_end = Date.now() + 30000;
            render();

            if (window.__nsl_scan_timer) clearTimeout(window.__nsl_scan_timer);
            window.__nsl_scan_timer = setTimeout(() => {
                scanLocked = false;
                window.__scan_state = "OFF";
                window.__nsl_scan_end = 0;
                window.__nsl_scan_timer = null;
                render();
            }, 30000);
        }

        function toggleBootVideos() {
            if (closed) return;
            bootVideos = !bootVideos;
            window.__boot_videos_state = bootVideos ? "ON" : "OFF";
            render();
        }

        function restore() {
            if (closed) return;
            closed = true;
            if (navObserver) {
                navObserver.disconnect();
                navObserver = null;
            }
            window.__nsl_take_focus = null;
            navNodes.forEach(n => { try { n.OnUnmount?.(); } catch {} });
            page.remove();
            original.forEach(el => { el.style.display = el._nslDisplay ?? ""; delete el._nslDisplay; });
        }

        let debounceTimer = null;
        let observerReady = false;

        navObserver = new MutationObserver((mutations) => {
            if (closed || !observerReady) return;

            const hasExternalChange = mutations.some(m => {
                const target = m.target.nodeType === Node.ELEMENT_NODE
                    ? m.target
                    : m.target.parentElement;

                if (target && (target === page || page.contains(target))) {
                    return false;
                }

                if (m.type === "attributes") {
                    const attr = m.attributeName;
                    if (
                        attr === "class" ||
                        attr === "style" ||
                        attr === "tabindex" ||
                        attr === "aria-checked"
                    ) {
                        return false;
                    }
                }

                if (m.type === "characterData") return false;

                if (m.type === "childList") {
                    const changedNodes = [
                        ...m.addedNodes,
                        ...m.removedNodes
                    ];

                    if (
                        changedNodes.length > 0 &&
                        changedNodes.every(node =>
                            node === page ||
                            (node.nodeType === Node.ELEMENT_NODE &&
                                (page.contains(node) ||
                                 node.contains(page)))
                        )
                    ) {
                        return false;
                    }
                }

                return true;
            });

            if (!hasExternalChange) return;

            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                if (closed) return;

                const stillMounted = document.getElementById(PAGE_ID);
                if (!stillMounted) {
                    restore();
                    return;
                }

                restore();
            }, 300);
        });

        setTimeout(() => {
            if (!closed) {
                navObserver.observe(main, {
                    childList: true,
                    subtree: true,
                    attributes: true,
                    attributeFilter: [
                        "class",
                        "style",
                        "tabindex",
                        "aria-checked"
                    ],
                    characterData: true
                });

                observerReady = true;
            }
        }, 600);

        const container = new D3(tree, parent, null);
        container.SetProperties({ focusable: true, autoFocus: true, isModal: false, navKey: "nsl-root" });
        container.OnMount(page);
        navNodes.push(container);

        const setPageFocus = (focused) => {
            page.style.outlineColor = focused ? "rgba(26, 159, 255, 0.4)" : "transparent";
        };
        page.addEventListener("focus", () => setPageFocus(true));
        page.addEventListener("blur", () => setPageFocus(false));
        page.addEventListener("vgp_onfocus", () => {
            setPageFocus(true);
            if (!document.activeElement || document.activeElement === page) {
                setTimeout(() => navNodes[1]?.BTakeFocus?.(), 50);
            }
        });
        page.addEventListener("vgp_onblur", () => setPageFocus(false));

        const controls = [
            { el: toggle, handler: toggleScanner },
            { el: scanBtn, handler: startManualScan },
            { el: bootToggle, handler: toggleBootVideos }
        ];

        controls.forEach((ctrl, i) => {
            const node = new D3(tree, container, null);
            node.SetProperties({
                layout: refNode.m_Properties?.layout ?? 0,
                focusable: true,
                preferredFocus: i === 0,
                autoFocus: i === 0,
                noFocusRing: true,
                navKey: `nsl-ctrl-${i}`,
                onMoveUp: () => {
                    const prev = i > 0 ? i - 1 : controls.length - 1;
                    navNodes[prev + 1]?.BTakeFocus?.();
                    return true;
                },
                onMoveDown: () => {
                    const next = (i + 1) % controls.length;
                    navNodes[next + 1]?.BTakeFocus?.();
                    return true;
                },
                onMoveLeft: () => {
                    const prev = i > 0 ? i - 1 : controls.length - 1;
                    navNodes[prev + 1]?.BTakeFocus?.();
                    return true;
                },
                onMoveRight: () => {
                    const next = (i + 1) % controls.length;
                    navNodes[next + 1]?.BTakeFocus?.();
                    return true;
                }
            });
            node.OnMount(ctrl.el);
            navNodes.push(node);

            const highlight = active => {
                ctrl.el.classList.toggle("Focus", active);
                ctrl.el.classList.toggle("FocusVisible", active);
                render();
            };
            ctrl.el.addEventListener("focus", () => highlight(true));
            ctrl.el.addEventListener("blur", () => highlight(false));
            ctrl.el.addEventListener("vgp_onfocus", () => highlight(true));
            ctrl.el.addEventListener("vgp_onblur", () => highlight(false));
            ctrl.el.addEventListener("click", ctrl.handler);
        });

        container.m_rgChildren = navNodes.slice(1);
        container.m_bChildrenSorted = true;

        window.__nsl_take_focus = () => {
            if (closed) return;
            container.BTakeFocus?.();
            navNodes[1]?.BTakeFocus?.();
        };

        const triggerFocusRecovery = () => {
            if (closed) return;
            setTimeout(() => window.__nsl_take_focus?.(), 100);
            setTimeout(() => window.__nsl_take_focus?.(), 300);
        };
        window.addEventListener("focus", triggerFocusRecovery);
        document.addEventListener("visibilitychange", () => {
            if (!document.hidden) triggerFocusRecovery();
        });

        page.addEventListener("vgp_onbuttondown", e => {
            if (closed || e.detail?.is_repeat) return;
            if (e.detail?.button === 1) {
                e.preventDefault(); e.stopPropagation();
                if (toggle.classList.contains("Focus") || toggle === document.activeElement) {
                    toggleScanner();
                } else if (bootToggle.classList.contains("Focus") || bootToggle === document.activeElement) {
                    toggleBootVideos();
                } else {
                    startManualScan();
                }
            } else if (e.detail?.button === 2) {
                e.preventDefault(); e.stopPropagation();
                restore();
            }
        });

        page.addEventListener("keydown", e => {
            if (e.key === "Enter" || e.key === " ") {
                e.preventDefault(); e.stopPropagation();
                if (toggle.classList.contains("Focus") || toggle === document.activeElement) {
                    toggleScanner();
                } else if (bootToggle.classList.contains("Focus") || bootToggle === document.activeElement) {
                    toggleBootVideos();
                } else {
                    startManualScan();
                }
            } else if (e.key === "Escape" || e.key === "Backspace") {
                e.preventDefault(); e.stopPropagation();
                restore();
            }
        });

        render();
        navNodes[1]?.BTakeFocus?.();
    }

    channel.onmessage = e => { if (e.data?.type === "open page") openConfigPage(); };
})();
"""


# Writing to env_vars from frontend
_last_written_state = None

def write_scan_state_to_file(state: str, variable: str = "NSL_SCAN_STATE"):
    try:
        current = read_scan_state_from_file(variable)
        if current == state:
            return

        try:
            with open(ENVARS_FILE, "r") as f:
                lines = f.readlines()
        except FileNotFoundError:
            lines = []

        found = False
        for i, line in enumerate(lines):
            key, sep, _ = line.partition("=")
            if sep and key.strip() == variable:
                lines[i] = f"{variable}={state}\n"
                found = True
                break

        if not found:
            lines.append(f"{variable}={state}\n")

        with open(ENVARS_FILE, "w") as f:
            f.writelines(lines)

        print(f"[ENVARS] Updated {variable}: {state}")

    except Exception as e:
        print(f"[ENVARS] Failed to write {variable}: {e}")


def read_scan_state_from_file(variable: str = "NSL_SCAN_STATE") -> str | None:
    try:
        with open(ENVARS_FILE, "r") as f:
            for line in f:
                key, sep, value = line.partition("=")
                if sep and key.strip() == variable:
                    return value.strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"[ENVARS] Failed to read {variable}: {e}")

    return None


eval_id_counter = itertools.count(1000)


def inject_scanner_code(sock, scan_state, boot_state):
    scan_state_js = scan_state if scan_state in ("ON", "OFF", "MANUAL") else "OFF"
    boot_state_js = boot_state if boot_state in ("ON", "OFF") else "OFF"

    send_ws_text(sock, json.dumps({
        "id": next(eval_id_counter),
        "method": "Runtime.evaluate",
        "params": {
            "expression": f"""
                window.__scan_state = '{scan_state_js}';
                window.__boot_videos_state = '{boot_state_js}';
                (function(){{ {SCANNER_CODE} }})();
            """,
            "awaitPromise": True
        }
    }))
    recv_ws_message(sock)


def sync_frontend_state_to_envars(sock):
    # 1. Check for manual scan event trigger
    request_id = next(eval_id_counter)
    send_ws_text(sock, json.dumps({
        "id": request_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__scan_event",
            "returnByValue": True
        }
    }))

    while True:
        msg = recv_ws_message(sock)
        if not msg:
            time.sleep(0.01)
            continue

        data = json.loads(msg)
        if data.get("id") != request_id:
            continue

        event = data.get("result", {}).get("result", {}).get("value")
        if event == "MANUAL":
            send_ws_text(sock, json.dumps({
                "id": next(eval_id_counter),
                "method": "Runtime.evaluate",
                "params": {
                    "expression": "window.__scan_event = null"
                }
            }))
            write_scan_state_to_file("MANUAL", "NSL_SCAN_STATE")
            break
        break

    # 2. Sync Scanner State
    request_id = next(eval_id_counter)
    send_ws_text(sock, json.dumps({
        "id": request_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__scan_state",
            "returnByValue": True
        }
    }))

    scan_state = "OFF"
    while True:
        msg = recv_ws_message(sock)
        if not msg:
            time.sleep(0.01)
            continue

        data = json.loads(msg)
        if data.get("id") != request_id:
            continue

        scan_state = data.get("result", {}).get("result", {}).get("value")
        if scan_state is not None:
            write_scan_state_to_file(scan_state, "NSL_SCAN_STATE")
        break

    # 3. Sync Boot Videos State (NEW)
    request_id = next(eval_id_counter)
    send_ws_text(sock, json.dumps({
        "id": request_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "window.__boot_videos_state",
            "returnByValue": True
        }
    }))

    boot_state = "OFF"
    while True:
        msg = recv_ws_message(sock)
        if not msg:
            time.sleep(0.01)
            continue

        data = json.loads(msg)
        if data.get("id") != request_id:
            continue

        boot_state = data.get("result", {}).get("result", {}).get("value")
        if boot_state is not None:
            write_scan_state_to_file(boot_state, "NSL_BOOT_VIDEOS")
        break

    return scan_state, boot_state


sockets = []

for title in TARGET_TITLES:
    try:
        ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, title)
        sock = create_websocket_connection(ws_url)

        send_ws_text(sock, json.dumps({
            "id": next(eval_id_counter),
            "method": "Runtime.enable"
        }))
        recv_ws_message(sock)


        scan_state, boot_state = sync_frontend_state_to_envars(sock)

        if scan_state is None:
            scan_state = read_scan_state_from_file("NSL_SCAN_STATE") or "OFF"

        if boot_state is None:
            boot_state = read_scan_state_from_file("NSL_BOOT_VIDEOS") or "OFF"

        inject_scanner_code(sock, scan_state, boot_state)

        print(f"RESUMED WITH STATES for '{title}' -> Scanner: {scan_state}, Boot Videos: {boot_state}")
        sockets.append(sock)

    except Exception as e:
        print(f"[ERROR] Failed for '{title}': {e}")
# End of Writing and control for Frontend





MAIN_MENU_BUTTON_CODE = r"""
(() => {
    "use strict";

    const ID = "my-custom-nsl-button";
    const LABEL = "NSL";
    const NAV_KEY = "custom-nsl-button";
    const WRAPPER = "._1BbM8Qq8OL5N8gL4PYH397";
    const LOGO_URL = "https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/refs/heads/main/logo.png";

    if (window.__nslMenuButtonInitializing ||
        window.__nslMenuButtonInjected) return;

    window.__nslMenuButtonInitializing = true;

    const channel = new BroadcastChannel("nsl_communication_channel");

    const observer = new MutationObserver(() => initialize());

    function cleanup() {
        observer.disconnect();
        window.__nslMenuButtonInitializing = false;
    }

    function getD3Node(element) {
        if (!element) return null;

        const key = Object.keys(element).find(k =>
            k.startsWith("__reactFiber$")
        );

        let node = key ? element[key] : null;

        while (node) {
            const result = node.memoizedProps?.node ||
                node.stateNode?.props?.node;

            if (result) return result;
            node = node.return;
        }

        return null;
    }

    function getMenuElement(wrapper) {
        return wrapper?.querySelector('[role="menuitem"]') ||
            wrapper?.firstElementChild;
    }

    function initialize() {
        if (document.getElementById(ID)) {
            window.__nslMenuButtonInjected = true;
            cleanup();
            return;
        }

        const settings = document.querySelector('[aria-label="Settings"]');
        const power = document.querySelector('[aria-label="Power"]');

        const settingsWrapper = settings?.closest(WRAPPER);
        const powerWrapper = power?.closest(WRAPPER);
        const menu = settingsWrapper?.parentElement;

        if (!settings || !power || !settingsWrapper ||
            !powerWrapper || !menu ||
            powerWrapper.parentElement !== menu) return;

        const settingsNode = getD3Node(getMenuElement(settingsWrapper));
        const powerNode = getD3Node(getMenuElement(powerWrapper));

        if (!settingsNode || !powerNode) return;

        const parent = settingsNode.m_Parent || settingsNode.Parent;
        const tree = settingsNode.m_Tree || settingsNode.Tree;

        if (!parent ||
            !tree ||
            parent !== (powerNode.m_Parent || powerNode.Parent) ||
            !Array.isArray(parent.m_rgChildren)) return;

        const children = parent.m_rgChildren;

        for (let i = children.length - 1; i >= 0; i--) {
            if (children[i]?.m_Properties?.navKey === NAV_KEY &&
                children[i] !== window.__nslMenuButtonNode) {
                children.splice(i, 1);
            }
        }

        const wrapper = settingsWrapper.cloneNode(true);
        const button = getMenuElement(wrapper);

        if (!button) return;

        button.id = ID;
        button.tabIndex = 0;
        button.setAttribute("aria-label", LABEL);
        button.classList.add("Focusable");

        button.querySelectorAll("[id], [aria-label]").forEach(element => {
            element.removeAttribute("id");
            element.removeAttribute("aria-label");
        });

        const icon = button.querySelector("._36qQ1jQx09c12WwFv-rQ0R") ||
            button.querySelector("svg")?.parentElement ||
            button.firstElementChild;

        if (icon) {
            icon.innerHTML = `<img src="${LOGO_URL}" alt=""
                style="width:20px;height:20px;object-fit:contain">`;
        }

        const label = button.querySelector("._2ADpTpv53dcY1uFpMWO1KT") ||
            button.querySelector("span");

        if (label) label.textContent = LABEL;

        menu.insertBefore(wrapper, settingsWrapper.nextSibling);

        let navNode;

        try {
            navNode = new settingsNode.constructor(tree, parent, null);

            navNode.SetProperties({
                ...(settingsNode.m_Properties || {}),
                focusable: true,
                preferredFocus: false,
                autoFocus: false,
                navKey: NAV_KEY,
                onMoveDown: () => {
                    if (typeof powerNode.BTakeFocus === "function") {
                        powerNode.BTakeFocus();
                    } else {
                        power.focus();
                    }
                    return true;
                }
            });

            navNode.OnMount(button);
        } catch (error) {
            wrapper.remove();
            console.error("NSL navigation initialization failed:", error);
            return;
        }

        const settingsIndex = children.indexOf(settingsNode);
        const powerIndex = children.indexOf(powerNode);

        if (settingsIndex < 0 || powerIndex < 0) {
            wrapper.remove();
            return;
        }

        children.splice(settingsIndex + 1, 0, navNode);
        parent.m_bChildrenSorted = false;
        window.__nslMenuButtonNode = navNode;

        const highlight = active => {
            button.style.backgroundColor = active
                ? "rgba(255,255,255,0.12)" : "";
            button.style.boxShadow = active
                ? "inset 2px 0 0 #1a9fff" : "";

            button.classList.toggle("Focus", active);
            button.classList.toggle("FocusVisible", active);
        };

        button.addEventListener("focus", () => highlight(true));
        button.addEventListener("blur", () => highlight(false));
        button.addEventListener("vgp_onfocus", () => highlight(true));
        button.addEventListener("vgp_onblur", () => highlight(false));

        let actionTriggered = false;

        const triggerAction = () => {
            if (actionTriggered) return;
            actionTriggered = true;

            setTimeout(() => {
                button.dispatchEvent(new CustomEvent("vgp_onbuttondown", {
                    bubbles: true,
                    detail: { button: 2, is_repeat: false }
                }));

                channel.postMessage({ type: "open page" });

                setTimeout(() => {
                    actionTriggered = false;
                }, 300);
            }, 100);
        };

        button.addEventListener("vgp_onbuttondown", event => {
            if (event.detail?.button === 1 &&
                event.detail?.is_repeat !== true) {
                triggerAction();
            }
        });

        button.addEventListener("click", triggerAction);

        window.__nslMenuButtonInjected = true;
        cleanup();

        console.log("NSL button initialized after Settings.");
    }

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true
    });

    initialize();
})();
"""


eval_id_counter = iter(range(1, 1000000))

def inject_button_code(ws_socket):
    try:
        inject_id = next(eval_id_counter)

        wrapped_code = f"(async () => {{ {MAIN_MENU_BUTTON_CODE}; return 'Button injection done'; }})()"

        send_ws_text(ws_socket, json.dumps({
            "id": inject_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": wrapped_code,
                "awaitPromise": True
            }
        }))

        response = recv_ws_message_for_id(ws_socket, inject_id)
        print("Button injection response:", response)
        return response

    except Exception as e:
        print("Error during Button injection:", e)
        return None


try:
    ws_url = get_ws_url_by_title(WS_HOST, WS_PORT, TARGET_TITLE4)
    ws_socket = create_websocket_connection(ws_url)

    send_ws_text(ws_socket, json.dumps({
        "id": 1,
        "method": "Runtime.enable"
    }))
    recv_ws_message_for_id(ws_socket, 1)

    inject_button_code(ws_socket)

except Exception as e:
    print("Failed to connect or inject Button code:", e)
#end of button code






# Create an empty dictionary to store the app IDs
app_ids = {}

# Get the next available key for the shortcuts
def get_next_available_key(shortcuts):
    key = 0
    while str(key) in shortcuts['shortcuts']:
        key += 1
    return str(key)


def get_compat_tool_if_needed(launchoptions, exe_path, startingdir):
    steam_compat_marker = 'STEAM_COMPAT_DATA_PATH'

    if 'xodus' in exe_path.lower() or 'xodus' in startingdir.lower():
        print("Exclusion: 'xodus' detected in target or start directory.")
        return None

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

    # Native Linux targets (e.g. /usr/bin/heroic, Flatpaks) must not be forced through Proton
    if steam_compat_marker not in launchoptions and \
       not exe_path.strip('"').lower().endswith(('.exe', '.msi', '.bat')):
        print("Exclusion: native Linux target without a Proton prefix.")
        return None

    print("No exclusions applied. Returning compat tool.")
    return compat_tool_name




def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir, launcher_name=None):
    gate_file = f"{logged_in_home}/.config/systemd/user/env_vars"
    scan_state = None
    try:
        with open(gate_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("NSL_SCAN_STATE="):
                    scan_state = line.split("=", 1)[1].strip().upper()
                    break
    except FileNotFoundError:
        print(f"[NSL] Gate file not found: {gate_file}. Allowing by default.")

    if scan_state == "OFF":
        print(f"[NSL] Scan state is OFF. Skipping shortcut creation for {appname}.")
        return

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


    # Check if the launcher is installed (allows blank launch options, but catches missing/None values)
    if not shortcutdirectory or not appname or launchoptions is None or not startingdir:
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

    outdated = find_outdated_nsl_shortcut(appname, exe_path, wrap_for_armada(launchoptions))
    if outdated is not None:
        print(f"Updating {appname} to NSL's current target and launch options.")
        outdated['exe' if 'exe' in outdated else 'Exe'] = exe_path
        outdated['LaunchOptions'] = wrap_for_armada(launchoptions)
        shortcuts_updated = True
        return

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
        #create_steam_store_app_manifest_file(steam_store_appid, appname)

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
        'LaunchOptions': wrap_for_armada(launchoptions),
        'WideGrid': grid64,
        'Grid': gridp64,
        'Hero': hero64,
        'Logo': logo64,
    }

    if launcher_name:
        new_entry['Launcher'] = launcher_name






    compat_tool = get_compat_tool_if_needed(launchoptions, exe_path, startingdir)

    # Skip setting compat tool if UMU already processed it
    if not (umu_id and umu_processed_shortcuts.get(umu_id)) and compat_tool:
        new_entry['CompatTool'] = compat_tool










    # Add the new entry to the shortcuts dictionary and add proton
    key = get_next_available_key(shortcuts)
    shortcuts['shortcuts'][key] = new_entry







    remove_lines = {
        'chromelaunchoptions',
        'websites_str',
        'custom_website_names_str'
    }

    try:
        with open(env_vars_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        lines_to_keep = []
        modified = False

        for line in lines:
            if not any(key in line for key in remove_lines):
                lines_to_keep.append(line)
            else:
                modified = True

        if modified:
            with open(env_vars_path, "w", encoding="utf-8") as f:
                f.writelines(lines_to_keep)

    except FileNotFoundError:
        pass

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

def norm(s):
    return s.strip().lower()


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

    # Fallback: match by appname if codename not found
    if not codename:
        for entry in entries:
            if entry.get('TITLE') and entry['TITLE'].lower() == appname.lower():
                codename = entry['CODENAME']
                break

    if codename:
        selected_entry = None

        for entry in entries:
            if norm(entry['CODENAME']) == norm(codename):
                selected_entry = entry
                break

        if not selected_entry:
            print(f"No UMU entry match for codename: {codename}")
            return exe, startingdir, launchoptions

        codename = selected_entry['CODENAME']  # preserve canonical casing
        umu_id = selected_entry['UMU_ID'].replace("umu-", "")

        base_path = extract_base_path(launchoptions)
        new_exe = f'"{logged_in_home}/bin/umu-run" {exe}'
        new_start_dir = f'"{logged_in_home}/bin/"'

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

        # Remove duplicate STEAM_COMPAT_DATA_PATH if present
        if 'STEAM_COMPAT_DATA_PATH=' in updated_launch:
            updated_launch = re.sub(
                r'STEAM_COMPAT_DATA_PATH="[^"]+" ',
                '',
                updated_launch
            )

        # Set compat tool name to latest UMU-Proton
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

        compat_tool_name = max(umu_folders)[1] if umu_folders else "UMU-Proton-Latest"

        new_launch_options = (
            f'STEAM_COMPAT_DATA_PATH="{base_path}" '
            f'WINEPREFIX="{base_path}pfx" '
            f'GAMEID="{umu_id}" '
            f'PROTONPATH="{logged_in_home}/.steam/root/compatibilitytools.d/{compat_tool_name}" '
        )

        if '%command%' not in updated_launch:
            updated_launch = f'%command% {updated_launch}'

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

track_create_entry(os.environ.get('xodusnexusshortcutdirectory'), 'Xodus Nexus', os.environ.get('xodusnexuslaunchoptions'), os.environ.get('xodusnexusstartingdir'))





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
create_new_entry(chromedirectory, 'Super Monkey Ball Online', os.environ.get('monkeychromelaunchoptions'), os.environ.get('chrome_startdir'), launcher_name=browser_for_env('monkeychromelaunchoptions'))
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





































# Xodus Nexus Games Scanner
xodus_config_dir = f"{logged_in_home}/.config/xodus-nexus"
xodus_state_file = f"{xodus_config_dir}/launcher-state.json"
xodus_launcher = f"{xodus_config_dir}/shortcuts/launch-game"


def xodus_read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError) as error:
        print(f"[Xodus] Failed to read {path}: {error}")
        return {}


if not os.path.isfile(xodus_state_file) or not os.path.isfile(xodus_launcher):
    print("Skipping Exodus Scanner")
else:
    print("[Xodus] Scanner starting")

    xodus_state = xodus_read_json(xodus_state_file)
    xodus_games = xodus_state.get("games", [])

    created_count = 0
    skipped_count = 0

    for game in xodus_games:
        if not isinstance(game, dict):
            skipped_count += 1
            continue

        display_name = game.get("title", "").strip()
        game_id = game.get("id", "").strip()
        game_path = game.get("path", "").strip()

        if not display_name or not game_id:
            skipped_count += 1
            continue

        if not game_path or not os.path.isdir(game_path):
            skipped_count += 1
            continue

        if (
            len(game_id) != 16
            or any(c not in "0123456789abcdef" for c in game_id)
        ):
            skipped_count += 1
            continue

        exe_path = f'"{xodus_launcher}"'
        start_dir = f'"{xodus_config_dir}"'
        launch_options = game_id

        try:
            create_new_entry(
                exe_path,
                display_name,
                launch_options,
                start_dir,
                launcher_name="Microsoft Windows"
            )
            track_game(display_name, "Microsoft Windows")
            created_count += 1

        except Exception as error:
            print(f"[Xodus] ERROR creating {display_name}: {error}")

    print(
        f"\n[Xodus] Finished. Created: {created_count}; "
        f"skipped: {skipped_count}"
    )

# End of Xodus Nexus Games Scanner




#Scanners
# Epic Games Scanner
item_dir = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Manifests/"
if os.path.exists(item_dir):

    for item_file in os.listdir(item_dir):
        if not item_file.endswith('.item'):
            continue

        item_file_path = os.path.join(item_dir, item_file)

        try:
            with open(item_file_path, 'r') as file:
                item_data = json.load(file)
        except (json.JSONDecodeError, OSError, KeyError):
            continue

        display_name = item_data.get('DisplayName', '')
        app_name = item_data.get('AppName', '')
        launch_executable = item_data.get('LaunchExecutable', '')
        install_location = item_data.get('InstallLocation', '')

        if not display_name or not app_name:
            continue

        if "Content" in display_name or "Content" in install_location:
            continue

        if not launch_executable.lower().endswith('.exe'):
            continue

        if install_location:
            install_location_linux = install_location.replace(
                "C:\\",
                f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{epic_games_launcher}/pfx/drive_c/"
            ).replace("\\", "/")

            if not os.path.exists(install_location_linux):
                continue


        exe_path = (
            f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/"
            f"{epic_games_launcher}/pfx/drive_c/Program Files/"
            f"Epic Games/Launcher/Portal/Binaries/Win64/"
            f"EpicGamesLauncher.exe\""
        )

        start_dir = (
            f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/"
            f"{epic_games_launcher}/pfx/drive_c/Program Files/"
            f"Epic Games/Launcher/Portal/Binaries/Win64/\""
        )

        launch_options = (
            f"STEAM_COMPAT_DATA_PATH="
            f"\"{logged_in_home}/.local/share/Steam/steamapps/compatdata/"
            f"{epic_games_launcher}/\" "
            f"%command% -"
            f"'com.epicgames.launcher://apps/{app_name}"
            f"?action=launch&silent=true'"
        )

        create_new_entry(
            exe_path,
            display_name,
            launch_options,
            start_dir,
            launcher_name="Epic Games"
        )

        track_game(display_name, "Epic Games")

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
    "OSI": "Diablo II: Resurrected",
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
            continue

        # INSTALL RULE: key existence only
        if "Resumable" not in game_data:
            print(f"Skipping {game_key}: not installed (no Resumable key)")
            continue

        game_dict[game_key] = {
            "ServerUid": game_data.get("ServerUid", game_key),
            "LastActioned": game_data.get("LastActioned", ""),
            "LastPlayed": game_data.get("LastPlayed", "")
        }

        print(f"{game_key} is INSTALLED")

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
    for raw_key, game_info in game_dict.items():

        print(f"Processing game: {raw_key}")

        game_key = raw_key

        if game_key == "prometheus":
            game_key = "Pro"
        elif game_key == "fenris":
            game_key = "Fen"
        elif game_key == "diablo3":
            game_key = "D3"
        elif game_key == "hs_beta":
            game_key = "WTCG"
        elif game_key == "wow_classic":
            game_key = "WoWC"
        elif game_key == "wow":
            game_key = "WoW"
        elif game_key == "aqua":
            game_key = "Aqua"
        elif game_key == "aris":
            game_key = "Aris"
        elif game_key == "heroes":
            game_key = "Hero"
        elif game_key == "gryphon":
            game_key = "GRY"
        elif game_key == "lbra":
            game_key = "LBRA"
        elif game_key == "wow_classic_era":
            game_key = "WoWC"
        elif game_key in ("seaofthieves", "sot", "scor"):
            game_key = "SCOR"


        game_name = flavor_mapping.get(game_key)

        if not game_name:
            game_name = flavor_mapping.get(game_key.upper())

        if not game_name:
            game_name = flavor_mapping.get(game_key.lower())

        if not game_name:
            game_name = flavor_mapping.get(game_key.title())

        if not game_name:
            print(f"Unknown game mapping: {game_key}, skipping")
            continue

        print(f"Resolved {raw_key} -> {game_name}")


        exe_path = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net.exe"'
        start_dir = f'"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}/pfx/drive_c/Program Files (x86)/Battle.net/"'

        launch_options = (
            f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{bnet_launcher}" '
            f'%command% --exec="launch {game_key}" battlenet://{game_key}'
        )

        print(f"Creating entry for {game_name}")

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

# Set up the path to itch-setup.exe
itch_setup_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{itchio_launcher}/pfx/drive_c/users/steamuser/AppData/Local/itch/itch-setup.exe"

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

    # Match game_id between 'caves' and 'games' tables
    for cave in caves:
        game_id = cave[1]

        if game_id in games_dict:
            game_info = games_dict[game_id]

            # Extract the game title and ID
            game_title = game_info[2]

            # Append the game ID and title
            itchgames.append((game_id, game_title))

    # Process each game for creating new entries
    for game_id, game_title in itchgames:
        exe_path = f'"{itch_setup_path}"'

        start_dir = f'"{os.path.dirname(itch_setup_path)}"'
        launchoptions = (
            f'STEAM_COMPAT_DATA_PATH="{logged_in_home}/.local/share/Steam/steamapps/compatdata/{itchio_launcher}/" '
            f'%command% --appname itch --run-game {game_id}'
        )

        # Call the provided function to create a new entry for the game
        create_new_entry(
            exe_path,
            game_title,
            launchoptions,
            start_dir,
            launcher_name="itch.io"
        )

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
chrome_app_paths = [
    os.path.join(logged_in_home, ".var/app/com.google.Chrome/config/google-chrome/Default"),
    os.path.join(logged_in_home, ".var/app/com.google.chrome/config/google-chrome/Default"),
]

possible_bookmark_files = [
    os.path.join(profile_path, filename)
    for profile_path in chrome_app_paths
    for filename in ("Bookmarks", "AccountBookmarks")
]

bookmarks_file_path = next(
    (path for path in possible_bookmark_files if os.path.isfile(path)),
    None
)

geforce_now_urls = []
xbox_urls = []
luna_urls = []
boosteroid_urls = []
webrcade_urls = []
seen_urls = set()


def process_bookmark_item(item):
    if item.get('type') == "url":
        name = item.get('name', '').strip()
        url = item.get('url', '')

        if not name or not url or url in seen_urls:
            return

        if "play.geforcenow.com/games" in url:
            if name == "GeForce NOW":
                return
            game_name = name.replace(" on GeForce NOW", "").strip()
            url = url.split("&")[0] if "&" in url else url
            if url in seen_urls:
                return
            geforce_now_urls.append(("GeForce NOW", game_name, url))
            seen_urls.add(url)

        elif "xbox.com/" in url and ("/play/launch/" in url or "/play/games/" in url):
            if name.startswith("Play "):
                game_name = name.replace("Play ", "").split(" |")[0].strip()
            else:
                game_name = name.split(" |")[0].strip()

            if game_name:
                xbox_urls.append(("Xbox", game_name, url))
                seen_urls.add(url)

        elif "luna.amazon." in url and "/game/" in url:
            if name.startswith("Play "):
                game_name = name.replace("Play ", "").split(" |")[0].strip()
            else:
                game_name = name.split(" |")[0].strip()

            if game_name:
                luna_urls.append(("Amazon Luna", game_name, url))
                seen_urls.add(url)

        elif "cloud.boosteroid.com/application/" in url:
            boosteroid_urls.append(("Boosteroid", name, url))
            seen_urls.add(url)

        elif "cloud.boosteroid.com/static/streaming/streaming.html" in url and "sessionId=" in url:
            boosteroid_urls.append(("Boosteroid", name, url))
            seen_urls.add(url)

        elif "play.webrcade.com/app/" in url:
            webrcade_urls.append(("WebRcade", name, url))
            seen_urls.add(url)


def scan_children(children):
    for item in children:
        if item.get('type') == "folder":
            scan_children(item.get('children', []))
        else:
            process_bookmark_item(item)


if not bookmarks_file_path:
    print("Chrome Bookmarks not found. Skipping scanning for Bookmarks.")
else:
    try:
        with open(bookmarks_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Scanning Chrome bookmarks: {bookmarks_file_path}")

        roots = data.get('roots', {})

        for root_name in ('bookmark_bar', 'other', 'synced'):
            root = roots.get(root_name, {})
            scan_children(root.get('children', []))

        all_urls = (
            geforce_now_urls
            + xbox_urls
            + luna_urls
            + boosteroid_urls
            + webrcade_urls
        )

        for platform_name, game_name, url in all_urls:
            print(f"{platform_name}: {game_name} - {url}")

            encoded_url = url

            chromelaunch_options = (
                f'run --branch=stable --arch=x86_64 '
                f'--command=/app/bin/chrome --file-forwarding '
                f'com.google.Chrome @@u @@ '
                f'--window-size=1280,800 '
                f'--force-device-scale-factor=1.00 '
                f'--device-scale-factor=1.00 '
                f'--start-fullscreen "{encoded_url}" '
                f'--no-first-run --enable-features=OverlayScrollbar'
            )

            chromedirectory = os.environ.get(
                "chromedirectory", "/usr/bin/flatpak"
            )
            chrome_startdir = os.environ.get(
                "chrome_startdir", "/usr/bin"
            )

            create_new_entry(
                chromedirectory,
                game_name,
                chromelaunch_options,
                chrome_startdir,
                launcher_name=platform_name
            )

            track_game(game_name, "Google Chrome")

    except (OSError, json.JSONDecodeError, TypeError) as e:
        print(f"Failed to read Chrome bookmarks: {e}")

# end of chrome scanner for xbox, geforce now, and amazon luna, boosteroid bookmarks








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
    },
    {
        "id": "org.prismlauncher.PrismLauncher",
        "display_name": "Prism Launcher"
    }
]

exe_path = "/usr/bin/flatpak"
start_dir = "/usr/bin"
# Native Flatpak arch for this machine; Hytale only ships x86_64 and runs via FEX on arm64
flatpak_arch = "aarch64" if platform.machine() == "aarch64" else "x86_64"

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
        app_launch_options = f'"run" "--branch=stable" "--arch={flatpak_arch}" "--command=moonlight" "com.moonlight_stream.Moonlight"'
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


#Heroic Games Launcher (native) Scanner
# Prefer a distro-provided Heroic (e.g. ArmadaOS /usr/bin/heroic), then the AppImage NSL installs
heroic_exe = shutil.which("heroic")
if not heroic_exe:
    heroic_appimage = f"{logged_in_home}/.local/share/applications/Heroic.AppImage"
    if os.path.isfile(heroic_appimage):
        heroic_exe = heroic_appimage

if heroic_exe:
    # Keep Steam's overlay library out of Heroic: Electron SIGKILLs its helper processes on exit, and one
    # killed while the preloaded overlay holds Steam's IPC lock (SysMgrMutex) freezes the whole Steam UI
    create_new_entry(
        shortcutdirectory=f'"{heroic_exe}"',
        appname="Heroic Games Launcher",
        launchoptions="LD_PRELOAD= %command%",
        startingdir=f'"{os.path.dirname(heroic_exe)}"',
        launcher_name="NonSteamLaunchers"
    )
    track_game("Heroic Games Launcher", "Launcher")
else:
    print("Skipping Heroic Games Launcher scanner — Heroic not found.")
# End of Heroic Games Launcher Scanner





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


# Rockstar Games Launcher Scanner
rockstar_launcher_id = os.environ.get('rockstar_launcher', '')
rockstar_sys_reg = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{rockstar_launcher_id}/pfx/system.reg"

if not rockstar_launcher_id or not os.path.exists(rockstar_sys_reg):
    print("Rockstar Games Launcher data not found. Skipping Rockstar Games Scanner.")
else:
    rockstar_games = {}
    current_game = None

    with open(rockstar_sys_reg, 'r') as f:
        for line in f:
            section_match = re.search(r'\[Software\\\\Wow6432Node\\\\Rockstar Games\\\\([^\\]+)\]', line)
            if section_match:
                game_title = section_match.group(1)
                if game_title in ("Launcher", "Rockstar Games Social Club"):
                    current_game = None
                else:
                    current_game = game_title
                continue

            if current_game and '"InstallFolder"' in line:
                folder_match = re.search(r'"InstallFolder"="(.+)"', line)
                if folder_match:
                    install_folder = folder_match.group(1)
                    linux_path = install_folder.replace(
                        "C:\\\\",
                        f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{rockstar_launcher_id}/pfx/drive_c/"
                    ).replace("\\\\", "/")
                    if os.path.exists(linux_path):
                        if current_game not in rockstar_games:
                            rockstar_games[current_game] = linux_path
                    else:
                        print(f"Rockstar game '{current_game}' found in registry but install path not in launcher prefix: {linux_path}")

    if not rockstar_games:
        print("No Rockstar games found in registry. Skipping Rockstar Games Scanner.")
    else:
        compat_path = f"{logged_in_home}/.local/share/Steam/steamapps/compatdata/{rockstar_launcher_id}/"

        for game_name, install_path in rockstar_games.items():
            game_exe = None
            if os.path.isdir(install_path):
                exe_candidates = [f for f in os.listdir(install_path) if f.lower().endswith('.exe') and 'uninstall' not in f.lower()]
                game_word = game_name.split()[-1].lower()
                game_exe = next((e for e in exe_candidates if game_word in e.lower()), exe_candidates[0] if exe_candidates else None)

            if game_exe:
                exe_path = f'"{os.path.join(install_path, game_exe)}"'
                dir_path = f'"{install_path}"'
                launch_options = f'STEAM_COMPAT_DATA_PATH="{compat_path}" %command%'
                create_new_entry(exe_path, game_name, launch_options, dir_path, launcher_name="Rockstar Games Launcher")
                track_game(game_name, "Rockstar Games Launcher")
                print(f"Added Rockstar game: {game_name}")
            else:
                print(f"Could not find game executable for {game_name} in {install_path}")

# End of Rockstar Games Scanner


# Call finalize_tracking and capture removed apps
removed_apps = finalize_tracking()

# List of game names to skip for
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
    'Plex', 'Apple TV+', 'Crunchyroll', 'PokéRogue', 'NonSteamLaunchers', 'Repair EA App', 'Gryphlink', 'Super Monkey Ball Online'}


# --- Boot Video Logic ---
def get_boot_video(game_name, logged_in_home):
    env_file = os.path.expanduser(
        f'{logged_in_home}/.config/systemd/user/env_vars'
    )
    boot_videos = "OFF"

    try:
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()

                if line.startswith("NSL_BOOT_VIDEOS="):
                    boot_videos = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    except OSError as e:
        print(f"Could not read {env_file}: {e}")

    print(f"NSL_BOOT_VIDEOS setting: {boot_videos}")

    if boot_videos.upper() != "ON":
        print("Boot videos are disabled.")
        return

    print("Boot videos are enabled.")
    excluded_apps = skip_games

    OVERRIDE_PATH = os.path.expanduser(f'{logged_in_home}/.steam/root/config/uioverrides/movies')
    REQUEST_RETRIES = 5
    API_URL = "https://steamdeckrepo.com/api/posts/all"
    ssl_ctx = ssl.create_default_context()

    def sanitize_filename(filename):
        return re.sub(r'[<>:"/\\|?*]', '_', filename)

    def download_video(video, target_dir):
        sanitized_name = sanitize_filename(video['name'])
        file_path = os.path.join(target_dir, f"{sanitized_name}.webm")

        if os.path.exists(file_path):
            print(f"Skipping {file_path}, already exists.")
            return

        os.makedirs(target_dir, exist_ok=True)

        download_url = video.get('download_url')

        if download_url:
            try:
                req = urllib.request.Request(
                    download_url,
                    headers={"User-Agent": "SteamDeckBootFetcher/1.0"}
                )

                with urllib.request.urlopen(
                    req,
                    context=ssl_ctx,
                    timeout=60
                ) as response:

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

            except urllib.error.HTTPError as e:
                print(f"Download failed for {file_path}: {e.code} {e.reason}")

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
                req = urllib.request.Request(
                    API_URL,
                    headers={"User-Agent": "SteamDeckBootFetcher/1.0"}
                )

                with urllib.request.urlopen(
                    req,
                    context=ssl_ctx,
                    timeout=20
                ) as response:

                    if response.status == 200:
                        data = json.loads(
                            response.read().decode('utf-8')
                        ).get('posts', [])
                        break

                    elif response.status == 429:
                        raise Exception(
                            'Rate limit exceeded, try again in a minute'
                        )

                    else:
                        print(
                            f"steamdeckrepo fetch failed, "
                            f"status={response.status}"
                        )

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
                        'download_url': entry['video'],
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if term in entry['title'].lower()
                    and entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'],
                reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]

                print(f"Downloading boot video: {video['name']}")
                download_video(video, OVERRIDE_PATH)
                return

        # If no video, try first two words of game name
        if len(game_name.split()) > 1:
            first_two_words = ' '.join(
                game_name.split()[:2]
            ).lower()

            filtered_videos = sorted(
                (
                    {
                        'id': entry['id'],
                        'name': entry['title'],
                        'preview_video': entry['video'],
                        'download_url': entry['video'],
                        'target': 'boot',
                        'likes': entry['likes'],
                    }
                    for entry in data
                    if first_two_words in entry['title'].lower()
                    and entry['type'] == 'boot_video'
                ),
                key=lambda x: x['likes'],
                reverse=True
            )

            if filtered_videos:
                video = filtered_videos[0]

                print(f"Downloading boot video: {video['name']}")
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
        base_game_name = game_name.split(' (')[0].strip()
        desktop_filename = f"{base_game_name}.desktop"

        found_file = False

        print(f"Looking for .desktop file for: {game_name}")

        for game_name in removed_game_names:
            base_game_name = game_name.split(' (')[0].strip()

            found_file = False
            print(f"Looking for .desktop file for: {game_name}")

            for directory in directories:
                try:
                    files_in_directory = os.listdir(directory)
                except Exception:
                    continue

                for f in files_in_directory:
                    if not f.endswith(".desktop"):
                        continue

                    full_path = os.path.join(directory, f)

                    try:
                        config = configparser.ConfigParser(interpolation=None)
                        config.read(full_path)

                        if "Desktop Entry" not in config:
                            continue

                        desktop_name = config["Desktop Entry"].get("Name", "").strip()

                        if desktop_name == base_game_name:
                            os.remove(full_path)
                            print(f"Deleted .desktop file for: {game_name} from {directory}")
                            found_file = True
                            break

                    except Exception as e:
                        print(f"Failed reading {full_path}: {e}")
                        continue

                if found_file:
                    break

            if not found_file:
                print(f"No .desktop file found for: {game_name}")
