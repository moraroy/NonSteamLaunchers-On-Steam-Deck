#!/usr/bin/env python3

import binascii
import _config
import os
import re
import shutil
import sys
import vdf
from _config import folder_names
from pathlib import Path

# Append the path to the vdf module to the system path
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
sys.path.insert(0, os.path.expanduser(
    f"~/Downloads/NonSteamLaunchersInstallation/lib/python{python_version}/site-packages")
)
print(sys.path)

# $HOME
logged_in_home = str(Path.home())

# TODO: test in holoiso
# Define the path of the shortcuts.vdf file
userdata_parent = Path(logged_in_home) / '.steam/root/userdata'
userdata_folder = userdata_folder.glob('*')
shortcuts_vdf_path = None
for file in userdata_folder:
    if file.name == 'shortcuts.vdf':
        shortcuts_vdf_path = file
        break

# TODO: ^^
# Load the shortcuts.vdf file
with open(shortcuts_vdf_path, 'rb') as f:
    shortcuts = vdf.binary_load(f)

# Check if the 'shortcuts' key exists in the dictionary
if 'shortcuts' not in shortcuts:
    # Create an empty 'shortcuts' entry
    shortcuts['shortcuts'] = {}

# Check the format of the 'shortcuts' entry
if isinstance(shortcuts['shortcuts'], dict):
    # The 'shortcuts' entry is a dictionary
    for key, value in shortcuts['shortcuts'].items():
        # Check the type of the value
        if not isinstance(value, (str, int, dict)):
            pass

# Define the path of the Launchers
# ! Moved to config.py

# Streaming
chromedirectory = '$chromedirectory'
websites_str = '$custom_websites_str'
custom_websites = websites_str.split(', ')

app_ids = []


def get_steam_shortcut_id(exe, appname):
    unique_id = ''.join([exe, appname])
    id_int = binascii.crc32(str.encode(unique_id)) | 0x80000000
    return id_int


app_id_to_name = {}


def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir):
    if shortcutdirectory != '' and launchoptions != '':
        exe = f'"{shortcutdirectory}"'
        if shortcutdirectory != chromedirectory:
            appid = get_steam_shortcut_id(exe, appname)
            app_ids.append(appid)
            app_id_to_name[appid] = appname
        else:
            appid = None

        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': f'{str(appid)}' if appid is not None else '',
            'appname': appname,
            'exe': shortcutdirectory,
            'StartDir': startingdir,
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': launchoptions,
            'IsHidden': 0,
            'AllowDesktopConfig': 1,
            'AllowOverlay': 1,
            'OpenVR': 0,
            'Devkit': 0,
            'DevkitGameID': '',
            'LastPlayTime': 0,
            'tags': {
                '0': 'favorite'
            }
        }

        # Add the new entry to the shortcuts dictionary
        entry_exists = False
        if type(shortcuts['shortcuts']) == list:
            for entry in shortcuts['shortcuts']:
                entry.setdefault('appname', '')
                entry.setdefault('exe', '')
                if entry['appname'] == new_entry['appname'] and entry['exe'] == new_entry['exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('appname', '')
                shortcuts['shortcuts'][key].setdefault('exe', '')
                if shortcuts['shortcuts'][key]['appname'] == new_entry['appname'] and shortcuts['shortcuts'][key]['exe'] == new_entry['exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                # Check if the shortcuts['shortcuts'] dictionary is empty
                if not shortcuts['shortcuts']:
                    max_key = -1
                else:
                    # Find the highest key value
                    max_key = max(int(key) for key in shortcuts['shortcuts'].keys())
                # Add the new entry with a key value one higher than the current maximum
                shortcuts['shortcuts'][str(max_key + 1)] = new_entry


# TODO: extract logic from shell script and move either here or config.py
create_new_entry('$epicshortcutdirectory', 'Epic Games', '$epiclaunchoptions', '$epicstartingdir')
create_new_entry('$gogshortcutdirectory', 'Gog Galaxy', '$goglaunchoptions', '$gogstartingdir')
create_new_entry('$uplayshortcutdirectory', 'Ubisoft Connect', '$uplaylaunchoptions', '$uplaystartingdir')
create_new_entry('$originshortcutdirectory', 'Origin', '$originlaunchoptions', '$originstartingdir')
create_new_entry('$battlenetshortcutdirectory', 'Battle.net', '$battlenetlaunchoptions', '$battlenetstartingdir')
create_new_entry('$eaappshortcutdirectory', 'EA App', '$eaapplaunchoptions', '$eaappstartingdir')
create_new_entry('$amazonshortcutdirectory', 'Amazon Games', '$amazonlaunchoptions', '$amazonstartingdir')
create_new_entry('$itchioshortcutdirectory', 'itch.io', '$itchiolaunchoptions', '$itchiostartingdir')
create_new_entry('$legacyshortcutdirectory', 'Legacy Games', '$legacylaunchoptions', '$legacystartingdir')
create_new_entry('$humbleshortcutdirectory', 'Humble Bundle', '$humblelaunchoptions', '$humblestartingdir')
create_new_entry('$indieshortcutdirectory', 'IndieGala Client', '$indielaunchoptions', '$indiestartingdir')
create_new_entry('$rockstarshortcutdirectory', 'Rockstar Games Launcher', '$rockstarlaunchoptions', '$rockstarstartingdir')
create_new_entry('$glyphshortcutdirectory', 'Glyph', '$glyphlaunchoptions', '$glyphstartingdir')
create_new_entry('$minecraftshortcutdirectory', 'Minecraft: Java Edition', '$minecraftlaunchoptions', '$minecraftstartingdir')
create_new_entry('$psplusshortcutdirectory', 'Playstation Plus', '$pspluslaunchoptions', '$psplusstartingdir')
create_new_entry('$dmmshortcutdirectory', 'DMM Games', '$dmmlaunchoptions', '$dmmstartingdir')
create_new_entry('$chromedirectory', 'Xbox Games Pass', '$xboxchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'GeForce Now', '$geforcechromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Netflix', '$netlfixchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Hulu', '$huluchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Disney+', '$disneychromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Amazon Prime Video', '$amazonchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Youtube', '$youtubechromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Amazon Luna', '$lunachromelaunchoptions', '$chrome_startdir')

# Iterate over each custom website
for custom_website in custom_websites:
    # Check if the custom website is not an empty string
    if custom_website:
        # Remove any leading or trailing spaces from the custom website URL
        custom_website = custom_website.strip()

        # Remove the 'http://' or 'https://' prefix and the 'www.' prefix, if present
        clean_website = custom_website.replace(
            'http://', '').replace('https://', '').replace('www.', '')

        # Define a regular expression pattern to extract the game name from the URL
        pattern = r'/games/([\w-]+)'

        # Use the regex to search for the game name in the custom website URL
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
        chromelaunch_options = f"""run
            --branch=stable
            --arch=x86_64
            --command=/app/bin/chrome
            --file-forwarding com.google.Chrome @@u @@ -
            -window-size=1280,800
            --force-device-scale-factor=1.00
            --device-scale-factor=1.00
            --kiosk https://{clean_website}/
            --chrome-kiosk-type=fullscreen
            --no-first-run
            --enable-features=OverlayScrollbar"""

        # Call the create_new_entry function for this website
        create_new_entry('$chromedirectory', game_name, chromelaunch_options, '$chrome_startdir')

print(f'app_id_to_name: {app_id_to_name}')

# Save the updated shortcuts dictionary to the shortcuts.vdf file
with open('$shortcuts_vdf_path', 'wb') as f:
    vdf.binary_dump(shortcuts, f)

# Writes to the config.vdf File

excluded_appids = []

# Update the config.vdf file
with open(config_vdf_path, 'r') as f:
    config = vdf.load(f)

# Check if the CompatToolMapping key exists
if 'CompatToolMapping' not in config['InstallConfigStore']['Software']['Valve']['Steam']:
    # Create the CompatToolMapping key and set its value to an empty dictionary
    config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'] = {}

for app_id in app_ids:
    # Check if the app_id is in the list of excluded appids
    if app_id not in excluded_appids:
        # Update the CompatToolMapping for this app_id
        if str(app_id) in config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping']:
            config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['name'] = '$compat_tool_name'
            config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['config'] = ''
            config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)]['priority'] = '250'
        else:
            config['InstallConfigStore']['Software']['Valve']['Steam']['CompatToolMapping'][str(app_id)] = {'name': '$compat_tool_name', 'config': '', 'priority': '250'}

# Save the updated config dictionary to the config.vdf file
with open('$config_vdf_path', 'w') as f:
    vdf.dump(config, f)

# Load the configset_controller_neptune.vdf file
with open('$controller_config_path', 'r') as f:
    config = vdf.load(f)

# Add new entries for the games
for app_id in app_ids:
    config['controller_config'][str(app_id)] = {
        'workshop': 'workshop_id'
    }

# TODO: convert to function
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
config['controller_config']['Origin'] = {
    'workshop': '2856043168'
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
config['controller_config']['dmm games'] = {
    'template': 'controller_neptune_webbrowser.vdf'
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

# Save the updated config dictionary to the configset_controller_neptune.vdf file
with open('$controller_config_path', 'w') as f:
    vdf.dump(config, f)

# Define the path to the compatdata directory
compatdata_dir = '${logged_in_home}/.local/share/Steam/steamapps/compatdata'

# Iterate over each launcher in the folder_names dictionary
for launcher_name, folder in folder_names.items():
    # Define the current path of the folder
    current_path = os.path.join(compatdata_dir, folder)

    # Check if the folder exists
    if os.path.exists(current_path):
        print(f'{launcher_name}: {folder} exists')
        # Get the app ID for this launcher from the app_id_to_name dictionary
        appid = next(key for key, value in app_id_to_name.items() if value == launcher_name)

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
if os.path.exists(os.path.join(compatdata_dir, 'NonSteamLaunchers')):
    # Get the first app ID from the app_ids list
    first_app_id = app_ids[0]

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
