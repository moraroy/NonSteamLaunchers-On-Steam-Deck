#!/usr/bin/env bash

set -x              # activate debugging (execution shown)
set -o pipefail     # capture error from pipes
# set -eu           # exit immediately, undefined vars are errors

# ENVIRONMENT VARIABLES
# $USER
[[ -n $(logname >/dev/null 2>&1) ]] && logged_in_user=$(logname) || logged_in_user=$(whoami)

# $UID
# logged_in_uid=$(id -u "${logged_in_user}")

# $HOME
logged_in_home=$(eval echo "~${logged_in_user}")

# TODO: `/tmp` or `mktemp -d` might be a better option (see: EOF)
# $PWD (working directory)
download_dir="${logged_in_home}/Downloads/NonSteamLaunchersInstallation"

# Create a log file in the same directory as the desktop file/.sh file
exec >> "${logged_in_home}/Downloads/NonSteamLaunchers-install.log" 2>&1

# Version number (major.minor)
version=v3.5

# TODO: tighten logic to check whether major/minor version is up-to-date via `-eq`, `-lt`, or `-gt` operators
# Check repo releases via GitHub API then display current stable version
check_for_updates() {
    # Set the URL to the GitHub API for the repository
    local api_url="https://api.github.com/repos/moraroy/NonSteamLaunchers-On-Steam-Deck/releases/latest"

    # Get the latest release tag from the GitHub API
    local latest_version=$(curl -s "$api_url" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

    # Compare the version number in the script against the latest release tag
    if [ "$version" != "$latest_version" ]; then
        # Display a Zenity window to notify the user that a new version is available
        zenity --info --text="A new version is available: $latest_version\nPlease download it from GitHub." --width=200 --height=100
    else
        echo "You are already running the latest version: $version"
    fi
}


# Get the command line arguments
args=("$@")






# Check if "Decky Plugin" is one of the arguments
decky_plugin=false
for arg in "${args[@]}"; do
  if [ "$arg" = "Decky Plugin" ]; then
    decky_plugin=true
    break
  fi
done

# Define the repository and the folders to clone
repo_url='https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/archive/refs/heads/main.zip'
folders_to_clone=('requests' 'urllib3' 'steamgrid')

# Define the parent folder
logged_in_home=$(eval echo ~$user)
parent_folder="${logged_in_home}/.config/systemd/user/Modules"
mkdir -p "${parent_folder}"

# Check if the folders already exist
folders_exist=true
for folder in "${folders_to_clone[@]}"; do
  if [ ! -d "${parent_folder}/${folder}" ]; then
    folders_exist=false
    break
  fi
done

if [ "${folders_exist}" = false ]; then
  # Download the repository as a zip file
  zip_file_path="${parent_folder}/repo.zip"
  wget -O "${zip_file_path}" "${repo_url}"

  # Extract the zip file
  unzip -d "${parent_folder}" "${zip_file_path}"

  # Move the folders to the parent directory and delete the unnecessary files
  for folder in "${folders_to_clone[@]}"; do
    destination_path="${parent_folder}/${folder}"
    source_path="${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main/Modules/${folder}"
    if [ ! -d "${destination_path}" ]; then
      mv "${source_path}" "${destination_path}"
    fi
  done

  # Delete the downloaded zip file and the extracted repository folder
  rm "${zip_file_path}"
  rm -r "${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main"
fi

#Service File rough update
rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py

# Delete the service file
rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service

# Remove the symlink
unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service

# Reload the systemd user instance
systemctl --user daemon-reload

# Define your Python script path
python_script_path="${logged_in_home}/.config/systemd/user/NSLGameScanner.py"

# Define your GitHub link
github_link="https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/NSLGameScanner.py"
curl -o $python_script_path $github_link

# Define the path to the env_vars file
env_vars="${logged_in_home}/.config/systemd/user/env_vars"

# Check if the env_vars file exists
if [ -f "$env_vars" ]; then
    # If the file exists and the decky_plugin argument is set, run the .py file and then exit
    if [ "$decky_plugin" = true ]; then
        echo "env_vars file found and Decky Plugin argument set. Running the .py file..."
        python3 $python_script_path
        echo "Python script ran. Exiting the script."
        exit 0
    else
        # If the file exists but the decky_plugin argument is not set, run the .py file
        echo "env_vars file found but Decky Plugin argument not set. Running the .py file..."
        python3 $python_script_path
        live="and is LIVE."
    fi
else
    # If the file does not exist, do not run the .py file
    echo "env_vars file not found. Not running the .py file."
    live="and is NOT LIVE."
fi






# Check if any command line arguments were provided
if [ ${#args[@]} -eq 0 ]; then
    # No command line arguments were provided, so check for updates and display the zenity window if necessary
    check_for_updates
fi

# Check if the NonSteamLaunchersInstallation subfolder exists in the Downloads folder
if [ -d "$download_dir" ]; then
    # Delete the NonSteamLaunchersInstallation subfolder
    rm -rf "$download_dir"
    echo "Deleted NonSteamLaunchersInstallation subfolder"
else
    echo "NonSteamLaunchersInstallation subfolder does not exist"
fi

# Game Launchers

# TODO: parameterize hard-coded client versions (cf. 'app-25.6.2')
# Set the paths to the launcher executables
epic_games_launcher_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
epic_games_launcher_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
gog_galaxy_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
gog_galaxy_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
uplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
uplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
battlenet_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
battlenet_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
eaapp_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
eaapp_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
amazongames_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
amazongames_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
itchio_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch/app-25.6.2/itch.exe"
itchio_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher/pfx/drive_c/users/steamuser/AppData/Local/itch/app-25.6.2/itch.exe"
legacygames_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
legacygames_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
humblegames_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App/Humble App.exe"
humblegames_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/pfx/drive_c/Program Files/Humble App/Humble App.exe"
indiegala_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient/IGClient.exe"
indiegala_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/pfx/drive_c/Program Files/IGClient/IGClient.exe"
rockstar_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games/Launcher/Launcher.exe"
rockstar_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/pfx/drive_c/Program Files/Rockstar Games/Launcher/Launcher.exe"
glyph_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Glyph/GlyphClient.exe"
glyph_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher/pfx/drive_c/Program Files (x86)/Glyph/GlyphClient.exe"
minecraft_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
minecraft_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher/pfx/drive_c/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
psplus_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
psplus_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
vkplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"
vkplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"

# Chrome File Path
# chrome_installpath="/app/bin/chrome"
chrome_path="/usr/bin/flatpak"
chrome_startdir="\"/usr/bin\""

# Check if Epic Games Launcher is installed
function CheckInstallations {
if [[ -f "$epic_games_launcher_path1" ]]; then
    # Epic Games Launcher is installed in path 1
    epic_games_value="FALSE"
    epic_games_text="Epic Games ===> $epic_games_launcher_path1"
elif [[ -f "$epic_games_launcher_path2" ]]; then
    # Epic Games Launcher is installed in path 2
    epic_games_value="FALSE"
    epic_games_text="Epic Games ===> $epic_games_launcher_path2"
else
    # Epic Games Launcher is not installed
    epic_games_value="FALSE"
    epic_games_text="Epic Games"
fi

# Check if GOG Galaxy is installed
if [[ -f "$gog_galaxy_path1" ]]; then
    # GOG Galaxy is installed in path 1
    gog_galaxy_value="FALSE"
    gog_galaxy_text="GOG Galaxy ===> $gog_galaxy_path1"
elif [[ -f "$gog_galaxy_path2" ]]; then
    # GOG Galaxy is installed in path 2
    gog_galaxy_value="FALSE"
    gog_galaxy_text="GOG Galaxy ===> $gog_galaxy_path2"
else
    # GOG Galaxy is not installed
    gog_galaxy_value="FALSE"
    gog_galaxy_text="GOG Galaxy"
fi


# Check if Uplay is installed
if [[ -f "$uplay_path1" ]]; then
    # Uplay is installed in path 1
    uplay_value="FALSE"
    uplay_text="Ubisoft Connect ===> $uplay_path1"
elif [[ -f "$uplay_path2" ]]; then
    # Uplay is installed in path 2
    uplay_value="FALSE"
    uplay_text="Ubisoft Connect ===> $uplay_path2"
else
    # Uplay is not installed
    uplay_value="FALSE"
    uplay_text="Ubisoft Connect"
fi

# Check if Battle.net is installed
if [[ -f "$battlenet_path1" ]]; then
    # Battle.net is installed in path 1
    battlenet_value="FALSE"
    battlenet_text="Battle.net ===> $battlenet_path1"
elif [[ -f "$battlenet_path2" ]]; then
    # Battle.net is installed in path 2
    battlenet_value="FALSE"
    battlenet_text="Battle.net ===> $battlenet_path2"
else
    # Battle.net is not installed
    battlenet_value="FALSE"
    battlenet_text="Battle.net"
fi

# Check if EA App is installed
if [[ -f "$eaapp_path1" ]]; then
    # EA App is installed in path 1
    eaapp_value="FALSE"
    eaapp_text="EA App ===> $eaapp_path1"
elif [[ -f "$eaapp_path2" ]]; then
     # EA App is installed in path 2
     eaapp_value="FALSE"
     eaapp_text="EA App ===> $eaapp_path2"
else
     # EA App is not installed
     eaapp_value="FALSE"
     eaapp_text="EA App"
fi

# Check if Amazon Games is installed
if [[ -f "$amazongames_path1" ]]; then
    # Amazon Games is installed in path 1
    amazongames_value="FALSE"
    amazongames_text="Amazon Games ===> $amazongames_path1"
elif [[ -f "$amazongames_path2" ]]; then
    # Amazon Games is installed in path 2
    amazongames_value="FALSE"
    amazongames_text="Amazon Games ===> $amazongames_path2"
else
    # Amazon Games is not installed
    amazongames_value="FALSE"
    amazongames_text="Amazon Games"
fi

# Check if itch.io is installed
if [[ -f "$itchio_path1" ]]; then
    # itch.io is installed in path 1
    itchio_value="FALSE"
    itchio_text="itch.io ===> $itchio_path1"
elif [[ -f "$itchio_path2" ]]; then
    # itch.io is installed in path 2
    itchio_value="FALSE"
    itchio_text="itch.io ===> $itchio_path2"
else
    # itch.io is not installed
    itchio_value="FALSE"
    itchio_text="itch.io"
fi

# Check if Legacy Games Launcher is installed
if [[ -f "$legacygames_path1" ]]; then
    # Legacy Games is installed in path 1
    legacygames_value="FALSE"
    legacygames_text="Legacy Games ===> $legacygames_path1"
elif [[ -f "$legacygames_path2" ]]; then
    # Legacy Games is installed in path 2
    legacygames_value="FALSE"
    legacygames_text="Legacy Games ===> $legacygames_path2"
else
    # Legacy Games is not installed
    legacygames_value="FALSE"
    legacygames_text="Legacy Games - Broken, Use at own risk"
fi

# Check if Humble Games Launcher is installed
if [[ -f "$humblegames_path1" ]]; then
    # Humble Games is installed in path 1 on local drive
    humblegames_value="FALSE"
    humblegames_text="Humble Games Collection ===> $humblegames_path1"
elif [[ -f "$humblegames_path2" ]]; then
    # Humble Games is installed in path 2 on local drive
    humblegames_value="FALSE"
    humblegames_text="Humble Games Collection ===> $humblegames_path2"
else
    # Humble Games is not installed
    humblegames_value="FALSE"
    humblegames_text="Humble Games Collection - Use Desktop Mode to sign in, then launch Game Mode"
fi

# Check if indiegala is installed
if [[ -f "$indiegala_path1" ]]; then
    # indiegala is installed in path 1 on local drive
    indiegala_value="FALSE"
    indiegala_text="IndieGala ===> $indiegala_path1"
elif [[ -f "$indiegala_path2" ]]; then
    # indiegala is installed in path 2 on local drive
    indiegala_value="FALSE"
    indiegala_text="IndieGala ===> $indiegala_path2"
else
    # indiegala is not installed
    indiegala_value="FALSE"
    indiegala_text="IndieGala"
fi

# Check if Rockstar is installed
if [[ -f "$rockstar_path1" ]]; then
    # Rockstar is installed in path 1 on local drive
    rockstar_value="FALSE"
    rockstar_text="Rockstar Games Launcher ===> $rockstar_path1"
elif [[ -f "$rockstar_path2" ]]; then
    # Rockstar is installed in path 2 on local drive
    rockstar_value="FALSE"
    rockstar_text="Rockstar Games Launcher ===> $rockstar_path2"
else
    # Rockstar is not installed
    rockstar_value="FALSE"
    rockstar_text="Rockstar Games Launcher"
fi

# Check if Glyph is installed
if [[ -f "$glyph_path1" ]]; then
    # Glyph is installed in path 1 on local drive
    glyph_value="FALSE"
    glyph_text="Glyph Launcher ===> $glyph_path1"
elif [[ -f "$glyph_path2" ]]; then
    # Glyph is installed in path 2 on local drive
    glyph_value="FALSE"
    glyph_text="Glyph Launcher ===> $glyph_path2"
else
    # Glyph is not installed
    glyph_value="FALSE"
    glyph_text="Glyph Launcher"
fi

# Check if Minecraft is installed
if [[ -f "$minecraft_path1" ]]; then
    # Minecraft is installed in path 1 on local drive
    minecraft_value="FALSE"
    minecraft_text="Minecraft ===> $minecraft_path1"
elif [[ -f "$minecraft_path2" ]]; then
    # Minecraft is installed in path 2 on local drive
    minecraft_value="FALSE"
    minecraft_text="Minecraft ===> $minecraft_path2"
else
    # Minecraft is not installed
    minecraft_value="FALSE"
    minecraft_text="Minecraft - Close black screen to continue installation"
fi

# Check if PlaystationPlus is installed
if [[ -f "$psplus_path1" ]]; then
    # PlaystationPlus is installed in path 1 on local drive
    psplus_value="FALSE"
    psplus_text="Playstation Plus ===> $psplus_path1"
elif [[ -f "$psplus_path2" ]]; then
    # PlaystationPlus is installed in path 2 on local drive
    psplus_value="FALSE"
    psplus_text="Playstation Plus ===> $psplus_path2"
else
    # PlaystationPlus is not installed
    psplus_value="FALSE"
    psplus_text="Playstation Plus"
fi


# Check if VK Play is installed
if [[ -f "$vkplay_path1" ]]; then
    # VK Play is installed in path 1 on local drive
    vkplay_value="FALSE"
    vkplay_text="VK Play ===> $vkplay_path1"
elif [[ -f "$vkplay_path2" ]]; then
    # VK Play is installed in path 2 on local drive
    vkplay_value="FALSE"
    vkplay_text="VK Play ===> $vkplay_path2"
else
    # VK Play is not installed
    vkplay_value="FALSE"
    vkplay_text="VK Play"
fi }

# Verify launchers are installed
function CheckInstallationDirectory {
    # Check if NonSteamLaunchers is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ]]; then
        # NonSteamLaunchers is installed
        nonsteamlauncher_move_value="TRUE"
    else
        # NonSteamLaunchers is not installed
        nonsteamlauncher_move_value="FALSE"
    fi

    # Check if EpicGamesLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ]]; then
        # EpicGamesLauncher is installed
        epicgameslauncher_move_value="TRUE"
    else
        # EpicGamesLauncher is not installed
        epicgameslauncher_move_value="FALSE"
    fi

    # Check if GogGalaxyLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ]]; then
        # GogGalaxyLauncher is installed
        goggalaxylauncher_move_value="TRUE"
    else
        # GogGalaxyLauncher is not installed
        goggalaxylauncher_move_value="FALSE"
    fi


    # Check if UplayLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" ]]; then
        # UplayLauncher is installed
        uplaylauncher_move_value="TRUE"
    else
        # UplayLauncher is not installed
        uplaylauncher_move_value="FALSE"
    fi

    # Check if Battle.netLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ]]; then
        # Battle.netLauncher is installed
        battlenetlauncher_move_value="TRUE"
    else
        # Battle.netLauncher is not installed
        battlenetlauncher_move_value="FALSE"
    fi

    # Check if TheEAappLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ]]; then
        # TheEAappLauncher is installed
        eaapplauncher_move_value="TRUE"
    else
        # TheEAappLauncher is not installed
        eaapplauncher_move_value="FALSE"
    fi

    # Check if AmazonGamesLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ]]; then
        # AmazonGamesLauncher is installed
        amazongameslauncher_move_value="TRUE"
    else
        # AmazonGamesLauncher is not installed
        amazongameslauncher_move_value="FALSE"
    fi

    # Check if itchioLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" ]]; then
        # itchioLauncher is installed
        itchiolauncher_move_value="TRUE"
    else
        # itchioLauncher is not installed
        itchiolauncher_move_value="FALSE"
    fi

    # Check if LegacyGamesLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ]]; then
        # LegacyGamesLauncher is installed
        legacygameslauncher_move_value="TRUE"
    else
        # LegacyGamesLauncher is not installed
        legacygameslauncher_move_value="FALSE"
    fi

    # Check if HumbleGamesLauncher is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ]]; then
        # HumbleGamesLauncher is installed
        humblegameslauncher_move_value="TRUE"
    else
        # HumbleGamesLauncher is not installed
        humblegameslauncher_move_value="FALSE"
    fi

    # Check if indiegala is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ]]; then
        # indiegalaLauncher is installed
        indiegalalauncher_move_value="TRUE"
    else
        # indiegalaLauncher is not installed
        indiegalalauncher_move_value="FALSE"
    fi

    # Check if rockstar is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" ]]; then
        # rockstar games launcher is installed
        rockstargameslauncher_move_value="TRUE"
    else
        # rockstar games launcher is not installed
        rockstargameslauncher_move_value="FALSE"
    fi

    # Check if Glyph is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" ]]; then
        # Glyph is installed
        glyphlauncher_move_value="TRUE"
    else
        # Glyph is not installed
        glyphlauncher_move_value="FALSE"
    fi

    # Check if Minecraft is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher" ]]; then
        # Minecraft is installed
        minecraftlauncher_move_value="TRUE"
    else
        # Minecraft is not installed
        minecraftlauncher_move_value="FALSE"
    fi

    # TODO: `pspluslauncher_move_value` is unused (SC2034)
    # Check if PlaystationPlus is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" ]]; then
        # PlaystationPlus is installed
        pspluslauncher_move_value="TRUE"
    else
        # PlaystationPlus is not installed
        pspluslauncher_move_value="FALSE"
    fi


    # Check if VK Play is installed
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" ]]; then
        # VK Play is installed
        vkplaylauncher_move_value="TRUE"
    else
        # VK Play is not installed
        vkplay_move_value="FALSE"
    fi }




#Get SD Card Path
get_sd_path() {
    # This assumes that the SD card is mounted under /run/media/deck/
    local sd_path=$(df | grep '/run/media/deck/' | awk '{print $6}')
    echo $sd_path
}

# Check which app IDs are installed
CheckInstallations
CheckInstallationDirectory

# Get the command line arguments
args=("$@")

# Initialize an array to store the custom websites
custom_websites=()

# Initialize a variable to store whether the "Separate App IDs" option is selected or not
separate_app_ids=false

# Check if any command line arguments were provided
if [ ${#args[@]} -eq 0 ]; then
    # No command line arguments were provided, so display the main zenity window
    selected_launchers=$(zenity --list --text="Which launchers do you want to download and install?" --checklist --column="$version" --column="Default = one App ID Installation, One Prefix, NonSteamLaunchers - opening this window has updated NSLGameScanner.py $live" FALSE "SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX" $epic_games_value "$epic_games_text" $gog_galaxy_value "$gog_galaxy_text" $uplay_value "$uplay_text" $battlenet_value "$battlenet_text" $amazongames_value "$amazongames_text" $eaapp_value "$eaapp_text" $legacygames_value "$legacygames_text" $itchio_value "$itchio_text" $humblegames_value "$humblegames_text" $indiegala_value "$indiegala_text" $rockstar_value "$rockstar_text" $glyph_value "$glyph_text" $minecraft_value "$minecraft_text" $psplus_value "$psplus_text" $vkplay_value "$vkplay_text" FALSE "Xbox Game Pass" FALSE "GeForce Now" FALSE "Amazon Luna" FALSE "Netflix" FALSE "Hulu" FALSE "Disney+" FALSE "Amazon Prime Video" FALSE "movie-web" FALSE "Youtube" FALSE "Twitch" --width=580 --height=740 --extra-button="Uninstall" --extra-button="Find Games" --extra-button="Start Fresh" --extra-button="Move to SD Card" --extra-button="Stop NSLGameScanner")

    # Check if the user clicked the 'Cancel' button or selected one of the extra buttons
    if [ $? -eq 1 ] || [[ $selected_launchers == "Start Fresh" ]] || [[ $selected_launchers == "Move to SD Card" ]] || [[ $selected_launchers == "Uninstall" ]] || [[ $selected_launchers == "Find Games" ]]; then
        # The user clicked the 'Cancel' button or selected one of the extra buttons, so skip prompting for custom websites
        custom_websites=()
    else
        # The user did not click the 'Cancel' button or select one of the extra buttons, so prompt for custom websites
        custom_websites_str=$(zenity --entry --title="Shortcut Creator" --text="Enter custom websites that you want shortcuts for, separated by commas. Leave blank and press ok if you dont want any. E.g. myspace.com, limewire.com, my.screenname.aol.com")

        # Split the custom_websites_str variable into an array using ',' as the delimiter
        IFS=',' read -ra custom_websites <<< "$custom_websites_str"
    fi
else
    # Command line arguments were provided, so set the value of the options variable using the command line arguments

    # Initialize an array to store the selected launchers
    selected_launchers=()

    for arg in "${args[@]}"; do
        if [[ "$arg" =~ ^https?:// ]]; then
            # Check if the arg is not an empty string before adding it to the custom_websites array
            if [ -n "$arg" ]; then
                custom_websites+=("$arg")
            fi
        else
            selected_launchers+=("$arg")
        fi
    done

    # TODO: error handling for unbound variable $selected_launchers_str on line 564
    # Convert the selected_launchers array to a string by joining its elements with a `|` delimiter.
    selected_launchers_str=$(IFS="|"; echo "${selected_launchers[*]}")

    # TODO: SC2199
    # Check if the `SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX` option was included in the `selected_launchers` variable. If this option was included, set the value of the `separate_app_ids` variable to `true`, indicating that separate app IDs should be used. Otherwise, set it to `false`.
    if [[ "${selected_launchers[@]}" =~ "SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX" ]]; then
        separate_app_ids=true
    else
        separate_app_ids=false
    fi
fi

# TODO: SC2145
# Print the selected launchers and custom websites
echo "Selected launchers: $selected_launchers"
echo "Selected launchers: $selected_launchers_str"
echo "Custom websites: ${custom_websites[@]}"
echo "Separate App IDs: $separate_app_ids"

# Set the value of the options variable
if [ ${#args[@]} -eq 0 ]; then
    # No command line arguments were provided, so set the value of the options variable using the selected_launchers variable
    options="$selected_launchers"
else
    # Command line arguments were provided, so set the value of the options variable using the selected_launchers_str variable
    options="$selected_launchers_str"
fi

# Check if the cancel button was clicked
if [ $? -eq 1 ] && [[ $options != "Start Fresh" ]] && [[ $options != "Move to SD Card" ]] && [[ $options != "Uninstall" ]] && [[ $options != "Find Games" ]]; then
    # The cancel button was clicked
    echo "The cancel button was clicked"
    exit 1
fi

# Check if no options were selected and no custom website was provided
if [ -z "$options" ] && [ -z "$custom_websites" ]; then
    # No options were selected and no custom website was provided
    zenity --error --text="No options were selected and no custom website was provided. The script will now exit." --width=200 --height=150
    exit 1
fi

# Check if the user selected to use separate app IDs
if [[ $options == *"SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX"* ]]; then
    # User selected to use separate app IDs
    use_separate_appids=true
else
    # User did not select to use separate app IDs
    use_separate_appids=false
fi


# Define the StartFreshFunction
function StartFreshFunction {
    # Define the path to the compatdata directory
    compatdata_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata"
    # Define the path to the other directory
    other_dir="${logged_in_home}/.local/share/Steam/steamapps/shadercache/"

    # Define an array of original folder names
    folder_names=("EpicGamesLauncher" "GogGalaxyLauncher" "UplayLauncher" "Battle.netLauncher" "TheEAappLauncher" "AmazonGamesLauncher" "itchioLauncher" "LegacyGamesLauncher" "HumbleGamesLauncher" "IndieGalaLauncher" "RockstarGamesLauncher" "GlyphLauncher" "MinecraftLauncher" "PlaystationPlusLauncher" "VKPlayLauncher")

    # Define an array of app IDs
    app_ids=("3772819390" "4294900670" "4063097571" "3786021133" "3448088735" "3923904787" "3440562512" "2948446662" "3303169468" "3595505624" "4272271078" "3259996605" "2588786779" "4090616647" "3494943831" "2390200925" "4253976432" "2221882453" "2296676888" "2486751858" "3974004104" "3811372789" "3788101956" "3782277090" "3640061468" "3216372511" "2882622939" "2800812206" "2580882702")

    # Iterate over each folder name in the folder_names array
    for folder in "${folder_names[@]}"; do
        # Check if the folder exists
        if [ -e "${compatdata_dir}/${folder}" ]; then
            # Check if the folder is a symbolic link
            if [ -L "${compatdata_dir}/${folder}" ]; then
                # Get the path of the target of the symbolic link
                target_path=$(readlink -f "${compatdata_dir}/${folder}")

                # Delete the target of the symbolic link
                rm -rf "$target_path"

                # Delete the symbolic link
                unlink "${compatdata_dir}/${folder}"
            else
                # Delete the folder
                # shellcheck disable=SC2115
                rm -rf "${compatdata_dir}/${folder}"
            fi
        fi
    done

    # Iterate over each app ID in the app_ids array
    for app_id in "${app_ids[@]}"; do
        # Check if the folder exists
        if [ -e "${other_dir}/${app_id}" ]; then
            # Check if the folder is a symbolic link
            if [ -L "${other_dir}/${app_id}" ]; then
                # Get the path of the target of the symbolic link
                target_path=$(readlink -f "${other_dir}/${app_id}")

                # Delete the target of the symbolic link
                rm -rf "$target_path"

                # Delete the symbolic link
                unlink "${other_dir}/${app_id}"
            else
                # Delete the folder
                # shellcheck disable=SC2115
                rm -rf "${other_dir}/${app_id}"
            fi
        fi
    done

    # Check if the NonSteamLaunchers folder exists
    if [ -e "$compatdata_dir/NonSteamLaunchers" ]; then
        # Check if the NonSteamLaunchers folder is a symbolic link
        if [ -L "$compatdata_dir/NonSteamLaunchers" ]; then
            # Get the path of the target of the symbolic link
            target_path=$(readlink -f "$compatdata_dir/NonSteamLaunchers")

            # Delete the target of the symbolic link
            rm -rf "$target_path"

            # Delete the symbolic link
            unlink "$compatdata_dir/NonSteamLaunchers"
        else
            # Delete the NonSteamLaunchers folder
            rm -rf "$compatdata_dir/NonSteamLaunchers"
        fi
    fi

    # Iterate over each folder in the compatdata directory
    for folder_path in "$compatdata_dir"/*; do
        # Check if the current item is a folder
        if [ -d "$folder_path" ]; then
            # Check if the folder is empty
            if [ -z "$(ls -A "$folder_path")" ]; then
                # Delete the empty folder
                rmdir "$folder_path"
                echo "Deleted empty folder: $(basename "$folder_path")"
            fi
        fi
    done

    # TODO: declare array and use find/for loop to avoid duplicate `rm` processes
    rm -rf "/run/media/mmcblk0p1/NonSteamLaunchers/"
    rm -rf "/run/media/mmcblk0p1/EpicGamesLauncher/"
    rm -rf "/run/media/mmcblk0p1/GogGalaxyLauncher/"
    rm -rf "/run/media/mmcblk0p1/UplayLauncher/"
    rm -rf "/run/media/mmcblk0p1/Battle.netLauncher/"
    rm -rf "/run/media/mmcblk0p1/TheEAappLauncher/"
    rm -rf "/run/media/mmcblk0p1/AmazonGamesLauncher/"
    rm -rf "/run/media/mmcblk0p1/LegacyGamesLauncher/"
    rm -rf "/run/media/mmcblk0p1/itchioLauncher/"
    rm -rf "/run/media/mmcblk0p1/HumbleGamesLauncher/"
    rm -rf "/run/media/mmcblk0p1/IndieGalaLauncher/"
    rm -rf "/run/media/mmcblk0p1/RockstarGamesLauncher/"
    rm -rf "/run/media/mmcblk0p1/GlyphLauncher/"
    rm -rf "/run/media/mmcblk0p1/MinecraftLauncher/"
    rm -rf "/run/media/mmcblk0p1/PlaystationPlusLauncher/"
    rm -rf "/run/media/mmcblk0p1/VKPlayLauncher/"
    rm -rf ${logged_in_home}/Downloads/NonSteamLaunchersInstallation
    rm -rf ${logged_in_home}/.config/systemd/user/Modules
    rm -rf ${logged_in_home}/.config/systemd/user/env_vars
    rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py

    # Delete the service file
    rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service

    # Remove the symlink
    unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service

    # Reload the systemd user instance
    systemctl --user daemon-reload

    # Exit the script with exit code 0 to indicate success
    exit 0
}

# Check if the Start Fresh button was clicked or if the Start Fresh option was passed as a command line argument
if [[ $options == "Start Fresh" ]] || [[ $selected_launchers == "Start Fresh" ]]; then
    # The Start Fresh button was clicked or the Start Fresh option was passed as a command line argument
    if [ ${#args[@]} -eq 0 ]; then
        # No command line arguments were provided, so display the zenity window
        if zenity --question --text="aaahhh it always feels good to start fresh :) but...This will delete the App ID folders you installed inside the steamapps/compatdata/ directory as well as the Shader Cache associated with them in the steamapps/shadercache directory. The nslgamescanner.service will also be terminated at /.config/systemd/user/ This means anything youve installed (launchers or games) WITHIN THIS SCRIPT will be deleted if you have them there. Everything will be wiped. Are you sure?" --width=300 --height=260; then
            # The user clicked the "Yes" button, so call the StartFreshFunction
            StartFreshFunction
            # If the Start Fresh function was called, set an environment variable
            if [ "$?" -eq 0 ]; then
                export START_FRESH=true
            else
                export START_FRESH=false
            fi
        else
            # The user clicked the "No" button, so exit with exit code 0 to indicate success.
            exit 0
        fi
    else
        # Command line arguments were provided, so skip displaying the zenity window and directly perform any necessary actions to start fresh by calling the StartFreshFunction
        StartFreshFunction
    fi
fi

if [[ $options == "Uninstall" ]]; then
# Check if the cancel button was clicked
    # The OK button was not clicked
    # Define the launcher options
    options=$(zenity --list --checklist \
        --title="Uninstall Launchers" \
        --text="Select the launchers you want to Uninstall..." \
        --column="Select" --column="This will delete the launcher and all of its games and files." \
        --width=508 --height=507 \
        FALSE "Epic Games" \
        FALSE "Gog Galaxy" \
        FALSE "Uplay" \
        FALSE "Battle.net" \
        FALSE "EA App" \
        FALSE "Amazon Games" \
        FALSE "Legacy Games" \
        FALSE "itch.io" \
        FALSE "Humble Bundle" \
        FALSE "IndieGala" \
        FALSE "Rockstar Games Launcher" \
        FALSE "Glyph Launcher" \
        FALSE "Minecraft"\
        FALSE "Playstation Plus"\
        FALSE "VK Play")

    if [[ $options != "" ]]; then
        # The Uninstall button was clicked
    # Add code here to handle the uninstallation of the selected launcher(s)
    if [[ $options == *"Epic Games"* ]]; then
        # User selected to uninstall Epic Games Launcher
        # Check if Epic Games Launcher was installed using the NonSteamLaunchers prefix
        if [[ -f "$epic_games_launcher_path1" ]]; then
            # Epic Games Launcher was installed using the NonSteamLaunchers prefix
            # Add code here to run the Epic Games Launcher uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games"
        elif [[ -f "$epic_games_launcher_path2" ]]; then
            # Epic Games Launcher was installed using a separate app ID
            # Add code here to delete the EpicGamesLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher"
        fi
    fi

    if [[ $options == *"Gog Galaxy"* ]]; then
        # User selected to uninstall GOG Galaxy
        # Check if GOG Galaxy was installed using the NonSteamLaunchers prefix
        if [[ -f "$gog_galaxy_path1" ]]; then
            # GOG Galaxy was installed using the NonSteamLaunchers prefix
            # Add code here to run the GOG Galaxy uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy"
        elif [[ -f "$gog_galaxy_path2" ]]; then
            # GOG Galaxy was installed using a separate app ID
            # Add code here to delete the GogGalaxyLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher"
        fi
    fi

    if [[ $options == *"Uplay"* ]]; then
        # User selected to uninstall Uplay
        # Check if Uplay was installed using the NonSteamLaunchers prefix
        if [[ -f "$uplay_path1" ]]; then
            # Uplay was installed using the NonSteamLaunchers prefix
            # Add code here to run the Uplay uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft"
        elif [[ -f "$uplay_path2" ]]; then
            # Uplay was installed using a separate app ID
            # Add code here to delete the UplayLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher"
        fi
    fi

    if [[ $options == *"Battle.net"* ]]; then
        # User selected to uninstall Battle.net
        # Check if Battle.net was installed using the NonSteamLaunchers prefix
        if [[ -f "$battlenet_path1" ]]; then
            # Battle.net was installed using the NonSteamLaunchers prefix
            # Add code here to run the Battle.net uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net"
        elif [[ -f "$battlenet_path2" ]]; then
            # Battle.net was installed using a separate app ID
            # Add code here to delete the Battle.netLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher"
        fi
    fi

    if [[ $options == *"EA App"* ]]; then
        # User selected to uninstall EA App
        # Check if EA App was installed using the NonSteamLaunchers prefix
        if [[ -f "$eaapp_path1" ]]; then
            # EA App was installed using the NonSteamLaunchers prefix
            # Add code here to run the EA App uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts"
        elif [[ -f "$eaapp_path2" ]]; then
            # EA App was installed using a separate app ID
            # Add code here to delete the EALauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher"
        fi
    fi

    if [[ $options == *"Amazon Games"* ]]; then
        # User selected to uninstall Amazon Games
        # Check if Amazon Games was installed using the NonSteamLaunchers prefix
        if [[ -f "$amazongames_path1" ]]; then
            # Amazon Games was installed using the NonSteamLaunchers prefix
            # Add code here to run the Amazon Games uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games"
        elif [[ -f "$amazongames_path2" ]]; then
            # Amazon Games was installed using a separate app ID
            # Add code here to delete the AmazonGamesLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher"
        fi
    fi

    if [[ $options == *"Legacy Games"* ]]; then
        # User selected to uninstall Legacy Games
        # Check if Legacy Games was installed using the NonSteamLaunchers prefix
        if [[ -f "$legacygames_path1" ]]; then
            # Legacy Games was installed using the NonSteamLaunchers prefix
            # Add code here to run the Legacy Games uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games"
        elif [[ -f "$legacygames_path2" ]]; then
            # Legacy Games was installed using a separate app ID
            # Add code here to delete the LegacyGamesLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher"
        fi
    fi

    if [[ $options == *"itch.io"* ]]; then
        # User selected to uninstall Itch.io
        # Check if Itch.io was installed using the NonSteamLaunchers prefix
        if [[ -f "$itchio_path1" ]]; then
            # Itch.io was installed using the NonSteamLaunchers prefix
            # Add code here to run the Itch.io uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch"
        elif [[ -f "$itchio_path2" ]]; then
            # Itch.io was installed using a separate app ID
            # Add code here to delete the Itch.ioLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher"
        fi
    fi

    if [[ $options == *"Humble Bundle"* ]]; then
        # User selected to uninstall Humble Bundle
        # Check if Humble Bundle was installed using the NonSteamLaunchers prefix
        if [[ -f "$humblegames_path1" ]]; then
            # Humble Bundle was installed using the NonSteamLaunchers prefix
            # Add code here to run the Humble Bundle uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App"
        elif [[ -f "$humblegames_path2" ]]; then
            # Humble Bundle was installed using a separate app ID
            # Add code here to delete the HumbleBundleLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher"
        fi
    fi

    if [[ $options == *"IndieGala"* ]]; then
        # User selected to uninstall IndieGala
        # Check if IndieGala was installed using the NonSteamLaunchers prefix
        if [[ -f "$indiegala_path1" ]]; then
            # IndieGala was installed using the NonSteamLaunchers prefix
            # Add code here to run the IndieGala uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient"
        elif [[ -f "$indiegala_path2" ]]; then
            # IndieGala was installed using a separate app ID
            # Add code here to delete the IndieGalaLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher"
        fi
    fi

    if [[ $options == *"Rockstar Games Launcher"* ]]; then
        # User selected to uninstall Rockstar Games
        # Check if Rockstar Games was installed using the NonSteamLaunchers prefix
        if [[ -f "$rockstar_path1" ]]; then
            # Rockstar Games was installed using the NonSteamLaunchers prefix
            # Add code here to run the Rockstar Games uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games"
        elif [[ -f "$rockstar_path2" ]]; then
            # Rockstar Games was installed using a separate app ID
            # Add code here to delete the RockstarGamesLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher"
        fi
    fi

    if [[ $options == *"Glyph Launcher"* ]]; then
        # User selected to uninstall Glyph
        # Check if Glyph was installed using the NonSteamLaunchers prefix
        if [[ -f "$glyph_path1" ]]; then
            # Glyph was installed using NonSteamLaunchers prefix
            # Add code here to run the Glyph uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Glyph"
        elif [[ -f "$glyph_path2" ]]; then
            # Glyph was installed using a separate app ID
            # Add code here to delete the GlyphLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher"
        fi
    fi

    if [[ $options == *"Minecraft"* ]]; then
        # User selected to uninstall Minecraft
        # Check if Minecraft was installed using the NonSteamLaunchers prefix
        if [[ -f "$minecraft_path1" ]]; then
            # Minecraft was installed using NonSteamLaunchers prefix
            # Add code here to run the Minecraft uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Minecraft Launcher"
        elif [[ -f "$minecraft_path2" ]]; then
            # Minecraft was installed using a separate app ID
            # Add code here to delete the MinecraftLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher"
        fi
    fi

    if [[ $options == *"Playstation Plus"* ]]; then
        # User selected to uninstall Playstation
        # Check if Playstation was installed using the NonSteamLaunchers prefix
        if [[ -f "$psplus_path1" ]]; then
            # Playstation was installed using NonSteamLaunchers prefix
            # Add code here to run the Playstation uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus"
        elif [[ -f "$psplus_path2" ]]; then
            # Playstation was installed using a separate app ID
            # Add code here to delete the PlaystationPlusLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher"
        fi
    fi


    if [[ $options == *"VK Play"* ]]; then
        # User selected to uninstall VKPlayLauncher
        # Check if VKPlayLauncher was installed using the NonSteamLaunchers prefix
        if [[ -f "$vkplay_path1" ]]; then
            # VKPlayLauncher was installed using NonSteamLaunchers prefix
            # Add code here to run the VKPlayLauncher uninstaller
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter"
        elif [[ -f "$vkplay_path2" ]]; then
            # VKPlayLauncher was installed using a separate app ID
            # Add code here to delete the VKPlayLauncher app ID folder
            rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher"
        fi
    fi

    # Display a message to the user indicating that the operation was successful
        zenity --info --text="The selected launchers have now been deleted." --width=200 --height=150
    exit

  fi
  exit
fi



move_to_sd() {
    local launcher_id=$1
    local original_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${launcher_id}"
    local sd_path=$(get_sd_path)
    local new_dir="${sd_path}/${launcher_id}"

    # Resolve symbolic link to its target
    if [[ -L "${original_dir}" ]]; then
        original_dir=$(readlink "${original_dir}")
    fi

    if [[ -d "${original_dir}" ]] && [[ $move_options == *"${launcher_id}"* ]]; then
        mv "${original_dir}" "${new_dir}"
        ln -s "${new_dir}" "${original_dir}"
    fi
}

if [[ $options == "Move to SD Card" ]]; then
    CheckInstallationDirectory

    move_options=$(zenity --list --text="Which launcher IDs do you want to move to the SD card?" --checklist --column="Select" --column="Launcher ID" $nonsteamlauncher_move_value "NonSteamLaunchers" $epicgameslauncher_move_value "EpicGamesLauncher" $goggalaxylauncher_move_value "GogGalaxyLauncher" $uplaylauncher_move_value "UplayLauncher" $battlenetlauncher_move_value "Battle.netLauncher" $eaapplauncher_move_value "TheEAappLauncher" $amazongameslauncher_move_value "AmazonGamesLauncher" $itchiolauncher_move_value "itchioLauncher" $legacygameslauncher_move_value "LegacyGamesLauncher" $humblegameslauncher_move_value "HumbleGamesLauncher" $indiegalalauncher_move_value "IndieGalaLauncher" $rockstargameslauncher_move_value "RockstarGamesLauncher" $glyphlauncher_move_value "GlyphLauncher" $minecraftlauncher_move_value "MinecraftLauncher" $pspluslauncher_move_value "PlaystationPlusLauncher" $vkplaylauncher_move_value "VKPlayLauncher" --width=335 --height=524)

    if [ $? -eq 0 ]; then
        zenity --info --text="The selected directories have been moved to the SD card and symbolic links have been created." --width=200 --height=150

        IFS="|" read -ra selected_launchers <<< "$move_options"
        for launcher in "${selected_launchers[@]}"; do
            move_to_sd "$launcher"
        done
    fi

    # TODO: verify non-zero exit is necessary
    # ! Why the non-zero return?
    # Exit the script
    exit 1
fi

# Get the command line arguments
args=("$@")

# Check if the Stop NSLGameScanner option was passed as a command line argument or clicked in the GUI
if [[ " ${args[@]} " =~ " Stop NSLGameScanner " ]] || [[ $options == "Stop NSLGameScanner" ]]; then

    # Stop the service
    systemctl --user stop nslgamescanner.service

    # Delete the NSLGameScanner.py
    rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py

    # Delete the service file
    rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service

    # Remove the symlink
    unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service

    # Reload the systemd user instance
    systemctl --user daemon-reload

    # If command line arguments were provided, exit the script
    if [ ${#args[@]} -ne 0 ]; then
        rm -rf ${logged_in_home}/.config/systemd/user/env_vars
        exit 0
    fi

    # If no command line arguments were provided, display the zenity window
    zenity --question --text="NSLGameScanner has been stopped. Do you want to run it again?" --width=200 --height=150
    if [ $? = 0 ]; then
        # User wants to run NSLGameScanner again
        python3 $python_script_path
    else
        # User does not want to run NSLGameScanner again
        exit 1
    fi
fi




# Check if the user clicked the "Find Games" button
if [[ $options == "Find Games" ]]; then
    # The Find Games button was clicked
    # Check if the NonSteamLaunchersInstallation directory exists
    if [[ ! -d "$download_dir" ]]; then
        # The directory does not exist, so create it
        mkdir -p "$download_dir"
    fi

    # Download the latest BoilR from GitHub (Linux version)
    mkdir -p "$download_dir"
    cd "$download_dir"
    wget https://github.com/PhilipK/BoilR/releases/download/v.1.9.4/linux_BoilR

    # Add execute permissions to the linux_BoilR file
    chmod +x linux_BoilR

    # TODO: brittle subshell proces; should ~~create working directory variable~~ [edit: `download_dir`] and launch explicitly with `bash -c "linux_BoilR"`
    # Run BoilR from the current directory
    ./linux_BoilR

    # Exit the script
    exit
fi

# TODO: probably better to break this subshell into a function that can then be redirected to zenity
# Massive subshell pipes into `zenity --progress` around L2320 for GUI rendering
(

echo "0"
echo "# Detecting, Updating and Installing GE-Proton"

# check to make sure compatabilitytools.d exists and makes it if it doesnt
if [ ! -d "${logged_in_home}/.steam/root/compatibilitytools.d" ]; then
    mkdir -p "${logged_in_home}/.steam/root/compatibilitytools.d"
fi

# Create NonSteamLaunchersInstallation subfolder in Downloads folder
mkdir -p "${logged_in_home}/Downloads/NonSteamLaunchersInstallation"

# Set the path to the Proton directory
proton_dir=$(find "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

# Check if GE-Proton is installed
if [ -z "$proton_dir" ]; then
    # Download GE-Proton using the GitHub API
    echo "Downloading GE-Proton using the GitHub API"
    cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation"
    curl -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .tar.gz)"
    curl -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .sha512sum)"
    sha512sum -c ./*.sha512sum
    tar -xf GE-Proton*.tar.gz -C "${logged_in_home}/.steam/root/compatibilitytools.d/"
    proton_dir=$(find "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
    echo "All done :)"
else
    # Check if installed version is the latest version
    installed_version=$(basename $proton_dir | sed 's/GE-Proton-//')
    latest_version=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep tag_name | cut -d '"' -f 4)
    if [ "$installed_version" != "$latest_version" ]; then
        # Download GE-Proton using the GitHub API
        echo "Downloading GE-Proton using the GitHub API"
        cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation"
        curl -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .tar.gz)"
        curl -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .sha512sum)"
        sha512sum -c ./*.sha512sum
        tar -xf GE-Proton*.tar.gz -C "${logged_in_home}/.steam/root/compatibilitytools.d/"
        proton_dir=$(find "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
        echo "All done :)"
    fi
    #Delete old GE-Proton Versions
    for dir in "${logged_in_home}/.steam/root/compatibilitytools.d/GE-Proton"*; do
        if [ "$dir" != "$proton_dir" ]; then
            rm -rf "$dir"
        fi
    done
fi



echo "10"
echo "# Setting files in their place"

# Set the appid for the non-Steam game
appid=NonSteamLaunchers

# Set the URL to download the MSI file from
msi_url=https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi

# Set the path to save the MSI file to
msi_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/EpicGamesLauncherInstaller.msi

# Set the URL to download the second file from
exe_url=https://webinstallers.gog-statics.com/download/GOG_Galaxy_2.0.exe

# Set the path to save the second file to
exe_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/GOG_Galaxy_2.0.exe

# Set the URL to download the third file from
ubi_url=https://ubi.li/4vxt9

# Set the path to save the third file to
ubi_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/UbisoftConnectInstaller.exe

# Set the URL to download the fifth file from
battle_url="https://www.battle.net/download/getInstallerForGame?os=win&gameProgram=BATTLENET_APP&version=Live"

# Set the path to save the fifth file to
battle_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/Battle.net-Setup.exe

# Set the URL to download the sixth file from
amazon_url=https://download.amazongames.com/AmazonGamesSetup.exe

# Set the path to save the sixth file to
amazon_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/AmazonGamesSetup.exe

# Set the URL to download the seventh file from
eaapp_url=https://origin-a.akamaihd.net/EA-Desktop-Client-Download/installer-releases/EAappInstaller.exe

# Set the path to save the seventh file to
eaapp_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/EAappInstaller.exe

# Set the URL to download the eighth file from
itchio_url=https://itch.io/app/download?platform=windows

# Set the path to save the eighth file to
itchio_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/itch-setup.exe

# Set the URL to download the ninth file from
legacygames_url=https://cdn.legacygames.com/LegacyGamesLauncher/legacy-games-launcher-setup-1.10.0-x64-full.exe

# Set the path to save the ninth file to
legacygames_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/legacy-games-launcher-setup-1.10.0-x64-full.exe

# Set the URL to download the tenth file from
humblegames_url=https://www.humblebundle.com/app/download

# Set the path to save the tenth file to
humblegames_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/Humble-App-Setup-1.1.8+411.exe

# Set the URL to download the eleventh file from
indiegala_url=https://content.indiegalacdn.com/common/IGClientSetup.exe

# Set the path to save the eleventh file to
indiegala_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/IGClientSetup.exe

# Set the URL to download the twelfth file from
rockstar_url=https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe

# Set the path to save the twelfth file to
rockstar_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/Rockstar-Games-Launcher.exe

# Set the URL to download the Glyph Launcher file from
glyph_url=https://glyph.dyn.triongames.com/glyph/live/GlyphInstall.exe

# Set the path to save the Glyph Launcher to
glyph_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/GlyphInstall.exe

# Set the URL to download the Minecraft Launcher file from
minecraft_url=https://aka.ms/minecraftClientWindows

# Set the path to save the Minecraft Launcher to
minecraft_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/MinecraftInstaller.msi

# Set the URL to download the Playstation Launcher file from
psplus_url=https://download-psplus.playstation.com/downloads/psplus/pc/latest

# Set the path to save the Playstation Launcher to
psplus_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/PlayStationPlus-12.2.0.exe


# Set the URL to download the VK Play Launcher file from
vkplay_url=https://static.gc.vkplay.ru/VKPlayLoader.exe

# Set the path to save the VK Play Launcher to
vkplay_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/VKPlayLoader.exe

echo "20"
echo "# Creating files & folders"

# Check if the user selected any launchers
if [ -n "$options" ]; then
    # User selected at least one launcher

    # Create app id folder in compatdata folder if it doesn't exist and if the user selected to use a single app ID folder
    if [ "$use_separate_appids" = false ] && [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi
fi

# Change working directory to Proton's
cd $proton_dir

# Set the STEAM_RUNTIME environment variable
export STEAM_RUNTIME="${logged_in_home}/.steam/root/ubuntu12_32/steam-runtime/run.sh"

# Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

# Set the STEAM_COMPAT_DATA_PATH environment variable for the first file
export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

wait
echo "30"
echo "# Downloading & Installing Epic Games...please wait..."

# Check if the user selected Epic Games Launcher
if [[ $options == *"Epic Games"* ]]; then
    # User selected Epic Games Launcher
    echo "User selected Epic Games"

    # Set the appid for the Epic Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=EpicGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download MSI file
    if [ ! -f "$msi_file" ]; then
        echo "Downloading MSI file"
        wget $msi_url -O $msi_file
    fi

    # Run the MSI file using Proton with the /passive option
    echo "Running MSI file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run MsiExec.exe /i "$msi_file" /qn
fi

# TODO: capture PID of each `wait` process to make sure it's not an infinite loop
# Wait for the MSI file to finish running
wait
echo "40"
echo "# Downloading & Installing Gog Galaxy...please wait..."

# Check if the user selected GOG Galaxy
if [[ $options == *"GOG Galaxy"* ]]; then
    # User selected GOG Galaxy
    echo "User selected GOG Galaxy"

    # Set the appid for the Gog Galaxy 2.0
    if [ "$use_separate_appids" = true ]; then
        appid=GogGalaxyLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd "$proton_dir"

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download EXE file
    if [ ! -f "$exe_file" ]; then
        echo "Downloading EXE file"
        wget $exe_url -O $exe_file
    fi

    # Run the EXE file using Proton without the /passive option
    echo "Running EXE file using Proton without the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$exe_file" &

    echo "45"
    echo "# Downloading & Installing Gog Galaxy...Please wait..."

    # Cancel & Exit the GOG Galaxy Setup Wizard
    while true; do
        if pgrep -f "GalaxySetup.tmp" > /dev/null; then
            pkill -f "GalaxySetup.tmp"
            break
        fi
        sleep 1
    done

    # Navigate to %LocalAppData%\Temp
    cd "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/Temp"

    # Find the GalaxyInstaller_XXXXX folder and copy it to C:\Downloads
    galaxy_installer_folder=$(find . -maxdepth 1 -type d -name "GalaxyInstaller_*" | head -n1)
    cp -r "$galaxy_installer_folder" ${logged_in_home}/Downloads/NonSteamLaunchersInstallation/

    # Navigate to the C:\Downloads\GalaxyInstaller_XXXXX folder
    cd ${logged_in_home}/Downloads/NonSteamLaunchersInstallation/"$(basename $galaxy_installer_folder)"

    # Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
    echo "Running GalaxySetup.exe with the /VERYSILENT and /NORESTART options"
    "$STEAM_RUNTIME" "$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART

    # Wait for the EXE file to finish running
    wait
else
    # Gog Galaxy Launcher is already installed
    echo "Gog Galaxy Launcher is already installed"
fi

wait
echo "50"
echo "# Downloading & Installing Ubisoft Connect ...please wait..."

# Check if user selected Uplay
if [[ $options == *"Ubisoft Connect"* ]]; then
    # User selected Uplay
    echo "User selected Uplay"

    # Set the appid for the Ubisoft Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=UplayLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download UBI file
    if [ ! -f "$ubi_file" ]; then
        echo "Downloading UBI file"
        wget --no-check-certificate $ubi_url -O $ubi_file
    fi

    # Run the UBI file using Proton with the /passive option
    echo "Running UBI file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$ubi_file" /S
fi



wait
echo "70"
echo "# Downloading & Installing Battle.net...please wait..."

# Check if user selected Battle.net
if [[ $options == *"Battle.net"* ]]; then
    # User selected Battle.net
    echo "User selected Battle.net"

    # Set the appid for the Battlenet Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=Battle.netLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download BATTLE file
    if [ ! -f "$battle_file" ]; then
        echo "Downloading BATTLE file"
        wget $battle_url -O $battle_file
    fi

    # Run the BATTLE file using Proton with the /passive option
    echo "Running BATTLE file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net"

    while true; do
    if pgrep -f "Battle.net.exe" > /dev/null; then
        pkill -f "Battle.net.exe"
        break
    fi
    sleep 1
    done

fi

wait

echo "80"
echo "# Downloading & Installing Amazon Games...please wait..."

# Check if user selected Amazon Games
if [[ $options == *"Amazon Games"* ]]; then
    # User selected Amazon Games
    echo "User selected Amazon Games"

    # Set the appid for the Amazon Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=AmazonGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Amazon Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download Amazon file
    if [ ! -f "$amazon_file" ]; then
        echo "Downloading Amazon file"
        wget $amazon_url -O $amazon_file
    fi

    # Run the Amazon file using Proton with the /passive option
    echo "Running Amazon file using Proton with the /passive option"
    "$STEAM_RUNTIME" "${proton_dir}/proton" run "$amazon_file" &

    while true; do
        if pgrep -f "Amazon Games.exe" > /dev/null; then
            pkill -f "Amazon Games.exe"
            break
        fi
        sleep 1
    done

    # Wait for the Amazon file to finish running
    wait
fi

wait

echo "88"
echo "# Downloading & Installing EA App...please wait..."

# Check if user selected EA App
if [[ $options == *"EA App"* ]]; then
    # User selected EA App
    echo "User selected EA App"

    # Set the appid for the EA App Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=TheEAappLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download EA App file
    if [ ! -f "$eaapp_file" ]; then
        echo "Downloading EA App file"
        wget $eaapp_url -O $eaapp_file
    fi

    # Run the EA App file using Proton with the /passive option
    echo "Running EA App file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$eaapp_file" /quiet

    counter=0
    while true; do
        if pgrep -f "EABackgroundService.exe" > /dev/null; then
            pkill -f "EABackgroundService.exe"
            break
        fi
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge 10 ]; then
            break
        fi
    done

    # Wait for the EA App file to finish running
    wait
fi

wait
echo "89"
echo "# Downloading & Installing itch.io...please wait..."

# Check if the user selected itchio Launcher
if [[ $options == *"itch.io"* ]]; then
    # User selected itchio Launcher
    echo "User selected itch.io"

    # Set the appid for the itchio Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=itchioLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download itchio file
    if [ ! -f "$itchio_file" ]; then
        echo "Downloading itchio file"
        wget $itchio_url -O $itchio_file
    fi

    # Run the itchio file using Proton with the /passive option
    echo "Running itchio file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$itchio_file"
fi

wait
echo "90"
echo "# Downloading & Installing Legacy Games...please wait..."

# Check if user selected Legacy Games
if [[ $options == *"Legacy Games"* ]]; then
    # User selected Legacy Games
    echo "User selected Legacy Games"

    # Set the appid for the Legacy Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=LegacyGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download Legacy file
    if [ ! -f "$legacygames_file" ]; then
        echo "Downloading Legacy file"
        wget $legacygames_url -O $legacygames_file
    fi

    # Run the Legacy file using Proton with the /passive option
    echo "Running Legacy file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$legacygames_file" /S
fi

# Wait for the Legacy file to finish running
wait

echo "91"
echo "# Downloading & Installing Humble Games Collection...please wait..."

# Check if the user selected Humble Games Launcher
if [[ $options == *"Humble Games Collection"* ]]; then
    # User selected Humble Games Launcher
    echo "User selected Humble Games Collection"

    # Set the appid for the Humble Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=HumbleGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Humble Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download exe file
    if [ ! -f "$humblegames_file" ]; then
        echo "Downloading MSI file"
        wget $humblegames_url -O $humblegames_file
    fi

    # Run the exe file using Proton with the /passive option
    echo "Running Exe file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$humblegames_file" /S /D="C:\Program Files\Humble App"
    wait

    # Create the handle-humble-scheme script
    if [[ ! -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme" ]]; then
        echo '#!/usr/bin/env sh' > "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo 'set -e' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo 'export STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.local/share/Steam' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo 'export STEAM_COMPAT_DATA_PATH=~/.steam/steam/steamapps/compatdata/'$appid >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo 'FIXED_SCHEME="$(echo "$1" | sed "s/?/\//")"' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo 'echo $FIXED_SCHEME > /home/deck/.local/share/Steam/steamapps/compatdata/'$appid'/pfx/drive_c/.auth' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        echo "\"$STEAM_RUNTIME\" \"$proton_dir/proton\" run ~/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd" >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
        chmod +x "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
    fi
    wait

    # Create the Humble-scheme-handler.desktop file
    if [[ ! -f "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop" ]]; then
        echo "[Desktop Entry]" > "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        echo "Name=Humble App (Login)" >> "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        echo "Comment=Target for handling Humble App logins. You should not run this manually." >> "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        echo "Exec=${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme %u" >> "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        echo "Type=Application" >> "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        echo "MimeType=x-scheme-handler/humble;" >> "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
        desktop-file-install --rebuild-mime-info-cache --dir=${logged_in_home}/.local/share/applications "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
    fi

    wait

    # Create the start-humble.cmd script
    if [[ ! -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd" ]]; then
        echo '@echo off' > "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo 'cd /d "C:\Program Files\Humble App\"' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo 'set /p Url=<"C:\.auth"' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo 'if defined Url (' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo '    start "" "Humble App.exe" "%Url%"' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo ') else (' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo '    start "" "Humble App.exe" "%*"' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo ')' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
        echo 'exit' >> "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
    fi
fi

wait

echo "92"
echo "# Downloading & Installing Indie Gala...please wait..."

# Check if user selected indiegala
if [[ $options == *"IndieGala"* ]]; then
    # User selected indiegala
    echo "User selected IndieGala"

    # Set the appid for the indiegala Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=IndieGalaLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download indiegala file
    if [ ! -f "$indiegala_file" ]; then
        echo "Downloading indiegala file"
        wget $indiegala_url -O $indiegala_file
    fi

      # Run the indiegala file using Proton with the /passive option
      echo "Running IndieGala file using Proton with the /passive option"
      "$STEAM_RUNTIME" "$proton_dir/proton" run "$indiegala_file" /S
fi

# Wait for the Indie file to finish running
wait

echo "93"
echo "# Downloading & Installing Rockstar Games Launcher...please wait..."

# Check if user selected rockstar games launcher
if [[ $options == *"Rockstar Games Launcher"* ]]; then
    # User selected rockstar games
    echo "User selected Rockstar Games Launcher"

    # Set the appid for the indiegala Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=RockstarGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download rockstar games file
    if [ ! -f "$rockstar_file" ]; then
        echo "Downloading rockstar file"
        wget $rockstar_url -O $rockstar_file
    fi

    # Run the rockstar file using Proton with the /passive option
    echo "Running Rockstar Games Launcher file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$rockstar_file"
fi

# Wait for the rockstar file to finish running
wait

echo "94"
echo "# Downloading & Installing Glyph Launcher...please wait..."

# Check if user selected Glyph
if [[ $options == *"Glyph Launcher"* ]]; then
    # User selected Glyph
    echo "User selected Glyph Launcher"

    # Set the appid for Glyph
    if [ "$use_separate_appids" = true ]; then
        appid=GlyphLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download Glyph file
    if [ ! -f "$glyph_file" ]; then
        echo "Downloading Glyph file"
        wget $glyph_url -O $glyph_file
    fi

    # Run the Glyph file using Proton with the /passive option
    echo "Running Glyph Launcher file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$glyph_file"
fi

# Wait for the Glyph file to finish running
wait

echo "95"
echo "# Downloading & Installing Minecraft Launcher...please wait..."

# Check if user selected Minecraft
if [[ $options == *"Minecraft"* ]]; then
    # User selected Minecraft
    echo "User selected Minecraft"

    # Set the appid for Miencraft
    if [ "$use_separate_appids" = true ]; then
        appid=MinecraftLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Set MinecraftLauncher.exe Variable
    minecraftinstall_path="${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download Minecraft file
    if [ ! -f "$minecraft_file" ]; then
        echo "Downloading Minecraft file"
        wget $minecraft_url -O $minecraft_file
    fi

    # Run the Minecraft file using Proton with the /passive option
    echo "Running Minecraft Launcher file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run MsiExec.exe /i "$minecraft_file" /q

    if [ -f "$minecraftinstall_path" ]; then
        # Run MinecraftLauncher.exe for the first time
        "$STEAM_RUNTIME" "$proton_dir/proton" run "$minecraftinstall_path"
    else
        echo "Could not find MinecraftLauncher.exe at $minecraftinstall_path"
    fi

    echo "Minecraft is already installed at $minecraftinstall_path"
fi

# Wait for the Minecraft file to finish running
wait

echo "96"
echo "# Downloading & Installing Playstation Plus...please wait..."

# Check if the user selected Playstation Launcher
if [[ $options == *"Playstation Plus"* ]]; then
    # User selected PlayStation Plus Launcher
    echo "User selected PlayStation Plus"

    # Set the appid for the PlayStation Plus Launcher
    if [ "$use_separate_appids" = true ]; then
    appid=PlaystationPlusLauncher
    else
    appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download MSI file
    if [ ! -f "$psplus_file" ]; then
        echo "Downloading MSI file"
        wget $psplus_url -O $psplus_file
    fi

    # Run the Playstation file using Proton with the /passive option
    echo "Running Playstation file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$psplus_file" /q
fi

wait


echo "98"
echo "# Downloading & Installing VK Play...please wait..."

# Check if the user selected VK Play Launcher
if [[ "$options" == *"VK Play"* ]]; then
    # User selected VK Play Launcher
    echo "User selected VK Play"

    # Set the appid for the VK Play Launcher
    if [ "$use_separate_appids" = true ]; then
    	appid=VKPlayLauncher
    else
    	appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd "$proton_dir"

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for VK Play Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download VK Play file
    if [ ! -f "$vkplay_file" ]; then
        echo "Downloading VK Play file"
		wget "$vkplay_url" -O "$vkplay_file"
    fi

	# Run the VK Play file using Proton with the /passive option
	echo "Running VK Play file using Proton with the /passive option"
	"$STEAM_RUNTIME" "$proton_dir/proton" run "$vkplay_file"

	counter=0
    while true; do
        if pgrep -f "*GameCenter.exe*" > /dev/null; then
            pkill -f "*GameCenter.exe*"
            break
        fi
        sleep 1
        counter=$((counter + 1))
        if [ $counter -ge 30 ]; then
            break
        fi
    done

    # Wait for the VK Play file to finish running
    wait

	echo "VK Play Installation is complete."

fi

wait
echo "99"
echo "# Checking if Chrome is installed...please wait..."

# Check if user selected any of the options
if [[ $options == *"Netflix"* ]] || [[ $options == *"Xbox Game Pass"* ]] || [[ $options == *"Geforce Now"* ]] || [[ $options == *"Amazon Luna"* ]] || [[ $options == *"Hulu"* ]] || [[ $options == *"Disney+"* ]] || [[ $options == *"Amazon Prime Video"* ]] || [[ $options == *"Youtube"* ]] || [[ $options == *"Twitch"* ]] || [[ $options == *"movie-web"* ]]; then
    # User selected one of the options
    echo "User selected one of the options"

    # Check if Google Chrome is already installed
    if command -v google-chrome &> /dev/null; then
        echo "Google Chrome is already installed"
        flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
    else
        # Install the Flatpak runtime
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

        # Install Google Chrome
        flatpak install flathub com.google.Chrome

        # Run the flatpak --user override command
        flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
    fi
fi

# wait for Google Chrome to finish
wait

# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf "$download_dir"

    echo "100"
    echo "# Installation Complete - Steam will now restart. Your launchers will be in your library!...Food for thought...do Jedis use Force Compatability?"
) |
zenity --progress \
  --title="Update Status" \
  --text="Starting update...please wait..." --width=450 --height=350\
  --percentage=0 --auto-close

wait

# Initialize the env_vars file
> ${logged_in_home}/.config/systemd/user/env_vars


# Checking Files For Shortcuts and Setting Directories For Shortcuts
if [[ -f "$epic_games_launcher_path1" ]]; then
    # Epic Games Launcher is installed at path 1
    epicshortcutdirectory="\"$epic_games_launcher_path1\" -opengl"
    epiclaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    epicstartingdir="\"$(dirname "$epic_games_launcher_path1")\""
    echo "export epic_games_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Epic Games Launcher found at path 1"
elif [[ -f "$epic_games_launcher_path2" ]]; then
    # Epic Games Launcher is installed at path 2
    epicshortcutdirectory="\"$epic_games_launcher_path2\""
    epiclaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/\" %command%"
    epicstartingdir="\"$(dirname "$epic_games_launcher_path2")\""
    echo "export epic_games_launcher=EpicGamesLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Epic Games Launcher found at path 2"
fi

if [[ -f "$gog_galaxy_path1" ]]; then
    # Gog Galaxy Launcher is installed at path 1
    gogshortcutdirectory="\"$gog_galaxy_path1\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    gogstartingdir="\"$(dirname "$gog_galaxy_path1")\""
    echo "export gog_galaxy_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Gog Galaxy Launcher found at path 1"
elif [[ -f "$gog_galaxy_path2" ]]; then
    # Gog Galaxy Launcher is installed at path 2
    gogshortcutdirectory="\"$gog_galaxy_path2\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/\" %command%"
    gogstartingdir="\"$(dirname "$gog_galaxy_path2")\""
    echo "export gog_galaxy_launcher=GogGalaxyLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Gog Galaxy Launcher found at path 2"
fi


if [[ -f "$uplay_path1" ]]; then
    # Uplay Launcher is installed at path 1
    uplayshortcutdirectory="\"$uplay_path1\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    uplaystartingdir="\"$(dirname "$uplay_path1")\""
    echo "export ubisoft_connect_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Ubisoft Connect Launcher found at path 1"
elif [[ -f "$uplay_path2" ]]; then
    # Uplay Launcher is installed at path 2
    uplayshortcutdirectory="\"$uplay_path2\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher/\" %command%"
    uplaystartingdir="\"$(dirname "$uplay_path2")\""
    echo "export ubisoft_connect_launcher=UplayLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Ubisoft Connect Launcher found at path 1"
fi

if [[ -f "$battlenet_path1" ]]; then
    # Battlenet Launcher is installed at path 1
    battlenetshortcutdirectory="\"$battlenet_path1\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    battlenetstartingdir="\"$(dirname "$battlenet_path1")\""
elif [[ -f "$battlenet_path2" ]]; then
    # Battlenet Launcher is installed at path 2
    battlenetshortcutdirectory="\"$battlenet_path2\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/\" %command%"
    battlenetstartingdir="\"$(dirname "$battlenet_path2")\""
fi

if [[ -f "$eaapp_path1" ]]; then
    # EA App Launcher is installed at path 1
    eaappshortcutdirectory="\"$eaapp_path1\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    eaappstartingdir="\"$(dirname "$eaapp_path1")\""
	echo "export ea_app_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "EA App Launcher found at path 1"
elif [[ -f "$eaapp_path2" ]]; then
    # EA App Launcher is installed at path 2
    eaappshortcutdirectory="\"$eaapp_path2\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/\" %command%"
    eaappstartingdir="\"$(dirname "$eaapp_path2")\""
	echo "export ea_app_launcher=TheEAappLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "EA App Launcher found at path 2"
fi

if [[ -f "$amazongames_path1" ]]; then
    # Amazon Games Launcher is installed at path 1
    amazonshortcutdirectory="\"$amazongames_path1\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    amazonstartingdir="\"$(dirname "$amazongames_path1")\""
elif [[ -f "$amazongames_path2" ]]; then
    # Amazon Games Launcher is installed at path 2
    amazonshortcutdirectory="\"$amazongames_path2\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/\" %command%"
    amazonstartingdir="\"$(dirname "$amazongames_path2")\""
fi

if [[ -f "$itchio_path1" ]]; then
    # itchio Launcher is installed at path 1
    itchioshortcutdirectory="\"$itchio_path1\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    itchiostartingdir="\"$(dirname "$itchio_path1")\""
elif [[ -f "$itchio_path2" ]]; then
    # itchio Launcher is installed at path 2
    itchioshortcutdirectory="\"$itchio_path2\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher/\" %command%"
    itchiostartingdir="\"$(dirname "$itchio_path2")\""
fi

if [[ -f "$legacygames_path1" ]]; then
    # Legacy Games Launcher is installed at path 1
    legacyshortcutdirectory="\"$legacygames_path1\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    legacystartingdir="\"$(dirname "$legacygames_path1")\""
elif [[ -f "$legacygames_path2" ]]; then
    # Legacy Games Launcher is installed at path 2
    legacyshortcutdirectory="\"$legacygames_path2\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/\" %command%"
    legacystartingdir="\"$(dirname "$legacygames_path2")\""
fi

if [[ -f "$humblegames_path1" ]]; then
    # Humble Games Launcher is installed at path 1
    humbleshortcutdirectory="\"$humblegames_path1\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    humblestartingdir="\"$(dirname "$humblegames_path1")\""
elif [[ -f "$humblegames_path2" ]]; then
    # Humble Games Launcher is installed at path 2
    humbleshortcutdirectory="\"$humblegames_path2\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/\" %command%"
    humblestartingdir="\"$(dirname "$humblegames_path2")\""
fi

if [[ -f "$indiegala_path1" ]]; then
    # indiegala Launcher is installed at path 1
    indieshortcutdirectory="\"$indiegala_path1\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    indiestartingdir="\"$(dirname "$indiegala_path1")\""
elif [[ -f "$indiegala_path2" ]]; then
    # indiegala Launcher is installed at path 2
    indieshortcutdirectory="\"$indiegala_path2\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/\" %command%"
    indiestartingdir="\"$(dirname "$indiegala_path2")\""
fi

if [[ -f "$rockstar_path1" ]]; then
    # rockstar Launcher is installed at path 1
    rockstarshortcutdirectory="\"$rockstar_path1\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    rockstarstartingdir="\"$(dirname "$rockstar_path1")\""
elif [[ -f "$rockstar_path2" ]]; then
    # rockstar Launcher is installed at path 2
    rockstarshortcutdirectory="\"$rockstar_path2\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/\" %command%"
    rockstarstartingdir="\"$(dirname "$rockstar_path2")\""
fi

if [[ -f "$glyph_path1" ]]; then
    # Glyph is installed at path 1
    glyphshortcutdirectory="\"$glyph_path1\""
    glyphlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    glyphstartingdir="\"$(dirname "$glyph_path1")\""
elif [[ -f "$glyph_path2" ]]; then
    # Glyph is installed at path 2
    glyphshortcutdirectory="\"$glyph_path2\""
    glyphlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher/\" %command%"
    glyphstartingdir="\"$(dirname "$glyph_path2")\""
fi

if [[ -f "$minecraft_path1" ]]; then
    # Minecraft is installed at path 1
    minecraftshortcutdirectory="\"$minecraft_path1\""
    minecraftlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    minecraftstartingdir="\"$(dirname "$minecraft_path1")\""
elif [[ -f "$minecraft_path2" ]]; then
    # Minecraft is installed at path 2
    minecraftshortcutdirectory="\"$minecraft_path2\""
    minecraftlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher/\" %command%"
    minecraftstartingdir="\"$(dirname "$minecraft_path1")\""
fi

if [[ -f "$psplus_path1" ]]; then
    # Playstation is installed at path 1
    psplusshortcutdirectory="\"$psplus_path1\""
    pspluslaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    psplusstartingdir="\"$(dirname "$psplus_path1")\""
elif [[ -f "$psplus_path2" ]]; then
    # Playstation is installed at path 2
    psplusshortcutdirectory="\"$psplus_path2\""
    pspluslaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/\" %command%"
    psplusstartingdir="\"$(dirname "$psplus_path2")\""
fi

if [[ -f "$vkplay_path1" ]]; then
    # VK Play is installed at path 1
    vkplayhortcutdirectory="\"$vkplay_path1\""
    vkplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    vkplaystartingdir="\"$(dirname "$vkplay_path1")\""
elif [[ -f "$vkplay_path2" ]]; then
    # VK Play is installed at path 2
    vkplayhortcutdirectory="\"$vkplay_path2\""
    vkplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/\" %command%"
    vkplaystartingdir="\"$(dirname "$vkplay_path2")\""
fi



# Set Chrome options based on user's selection

if [[ $options == *"Xbox Game Pass"* ]]; then
    # User selected Xbox Game Pass
    chromedirectory="\"$chrome_path\""
    xboxchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.xbox.com/play --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Netflix"* ]]; then
    # User selected Netflix
    chromedirectory="\"$chrome_path\""
    netlfixchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.netflix.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"GeForce Now"* ]]; then
    # User selected GeForce Now
    chromedirectory="\"$chrome_path\""
    geforcechromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://play.geforcenow.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Hulu"* ]]; then
    # User selected Hulu
    chromedirectory="\"$chrome_path\""
    huluchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.hulu.com/welcome --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Disney+"* ]]; then
    # User selected Disney+
    chromedirectory="\"$chrome_path\""
    disneychromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.disneyplus.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Amazon Prime Video"* ]]; then
    # User selected Amazon Prime Video
    chromedirectory="\"$chrome_path\""
    amazonchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.amazon.com/primevideo --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Youtube"* ]]; then
    # User selected Youtube
    chromedirectory="\"$chrome_path\""
    youtubechromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.youtube.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Amazon Luna"* ]]; then
    # User selected Amazon Luna
    chromedirectory="\"$chrome_path\""
    lunachromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://luna.amazon.com/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"Twitch"* ]]; then
    # User selected Twitch
    chromedirectory="\"$chrome_path\""
    twitchchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.twitch.tv/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi

if [[ $options == *"movie-web"* ]]; then
    # User selected Twitch
    chromedirectory="\"$chrome_path\""
    twitchchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://movie-web.app/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
fi







# Check if any custom websites were provided
if [ ${#custom_websites[@]} -gt 0 ]; then
    # User entered one or more custom websites
    # Set the chromedirectory variable
    chromedirectory="\"$chrome_path\""

    # Convert the custom_websites array to a string
    custom_websites_str=$(IFS=", "; echo "${custom_websites[*]}")

    # Iterate over each custom website
    for custom_website in "${custom_websites[@]}"; do
        # Remove any leading or trailing spaces from the custom website URL
        custom_website="$(echo -e "${custom_website}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

        # Remove the 'http://' or 'https://' prefix and the 'www.' prefix, if present
        clean_website="${custom_website#http://}"
        clean_website="${clean_website#https://}"
        clean_website="${clean_website#www.}"

        # Extract the name of the website by removing everything after the first '/'
        website_name="${clean_website%%/*}"

        # Remove the top-level domain (e.g. '.com') from the website name
        website_name="${website_name%.*}"

        # Capitalize the first letter of the website name
        website_name="$(tr '[:lower:]' '[:upper:]' <<< "${website_name:0:1}")${website_name:1}"

        # TODO: `chromelaunchoptions` is unused (SC2034)
        # Set the chromelaunchoptions variable for this website
        chromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://$clean_website/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    done
fi

# Create the download directory if it doesn't exist
mkdir -p "$download_dir"

# Get the version of Python being used
python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')

# Create a directory for the vdf module
mkdir -p "${download_dir}/lib/python${python_version}/site-packages/vdf"

# Download the vdf module from the GitHub repository
download_url="https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/raw/main/Modules/vdf/__init__.py"
wget -P "${download_dir}/lib/python${python_version}/site-packages/vdf" "$download_url"

# Set the PYTHONPATH environment variable
export PYTHONPATH="${download_dir}/lib/python${python_version}/site-packages/:$PYTHONPATH"

# Set the default Steam directory
steam_dir="${logged_in_home}/.local/share/Steam"


# Check if the loginusers.vdf file exists
if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]]; then
    # Extract the block of text for the most recent user
    most_recent_user=$(sed -n '/"users"/,/"MostRecent" "1"/p' "${logged_in_home}/.steam/root/config/loginusers.vdf")

    # Initialize variables
    max_timestamp=0
    current_user=""
    current_steamid=""

    # Process each user block
    while read steamid account timestamp; do
        if (( timestamp > max_timestamp )); then
            max_timestamp=$timestamp
            current_user=$account
            current_steamid=$steamid
        fi
    done < <(echo "$most_recent_user" | awk -v RS='}\n' -F'\n' '
    {
        for(i=1;i<=NF;i++){
            if($i ~ /[0-9]{17}/){
                split($i,a, "\""); steamid=a[2];
            }
            if($i ~ /"AccountName"/){
                split($i,b, "\""); account=b[4];
            }
            if($i ~ /"Timestamp"/){
                split($i,c, "\""); timestamp=c[4];
            }
        }
        print steamid, account, timestamp
    }')

    # Print the currently logged in user
    if [[ -n $current_user ]]; then
        echo "Currently logged in user: $current_user"
        echo "SteamID: $current_steamid"
    else
        echo "No users found."
    fi

    # Convert steamid to steamid3
    steamid3=$((current_steamid - 76561197960265728))

    # Directly map steamid3 to userdata folder
    userdata_folder="${logged_in_home}/.steam/root/userdata/${steamid3}"

    # Check if userdata_folder exists
    if [[ -d "$userdata_folder" ]]; then
        echo "Found userdata folder for user with SteamID $current_steamid: $userdata_folder"
    else
        echo "Could not find userdata folder for user with SteamID $current_steamid"
    fi
else
    echo "Could not find loginusers.vdf file"
fi






# Check if userdata folder was found
if [[ -n "$userdata_folder" ]]; then
    # Userdata folder was found
    echo "Current user's userdata folder found at: $userdata_folder"

    # Find shortcuts.vdf file for current user
    shortcuts_vdf_path=$(find "$userdata_folder" -type f -name shortcuts.vdf)

    # Check if shortcuts_vdf_path is not empty
    if [[ -n "$shortcuts_vdf_path" ]]; then
        # Create backup of shortcuts.vdf file
        cp "$shortcuts_vdf_path" "$shortcuts_vdf_path.bak"
    else
        # Find config directory for current user
        config_dir=$(find "$userdata_folder" -maxdepth 1 -type d -name config)

        # Check if config_dir is not empty
        if [[ -n "$config_dir" ]]; then
            # Create new shortcuts.vdf file at expected location for current user
            touch "$config_dir/shortcuts.vdf"
            shortcuts_vdf_path="$config_dir/shortcuts.vdf"
        else
            # Create new config directory and new shortcuts.vdf file at expected location for current user
            mkdir "$userdata_folder/config/"
            touch "$userdata_folder/config/shortcuts.vdf"
            config_dir="$userdata_folder/config/"
            shortcuts_vdf_path="$config_dir/shortcuts.vdf"
        fi
    fi
else
    # Userdata folder was not found
    echo "Current user's userdata folder not found"
fi


# Pre check for updating the config file

# Set the default Steam directory
steam_dir_root="${logged_in_home}/.steam/root"

# Set the path to the config.vdf file
config_vdf_path="${steam_dir_root}/config/config.vdf"

# Check if the config.vdf file exists
if [ -f "$config_vdf_path" ]; then
    # Create a backup of the config.vdf file
    backup_path="${steam_dir_root}/config/config.vdf.bak"
    cp "$config_vdf_path" "$backup_path"

    # Set the name of the compatibility tool to use
    compat_tool_name=$(ls "${logged_in_home}/.steam/root/compatibilitytools.d" | grep "GE-Proton" | sort -V | tail -n1)
else
    echo "Could not find config.vdf file"
fi



# Write variables to a file before script is detached
echo "export steamid3=$steamid3" >> ${logged_in_home}/.config/systemd/user/env_vars
echo "export logged_in_home=$logged_in_home" >> ${logged_in_home}/.config/systemd/user/env_vars
echo "export compat_tool_name=$compat_tool_name" >> ${logged_in_home}/.config/systemd/user/env_vars


# Detach script from Steam process
nohup sh -c 'sleep 10; /usr/bin/steam' &

# Close all instances of Steam
steam_pid() { pgrep -x steam ; }
steam_running=$(steam_pid)
[[ -n "$steam_running" ]] && killall steam

# Wait for the steam process to exit
while steam_pid > /dev/null; do sleep 5; done






# Set the path to the configset_controller_neptune.vdf file
controller_config_path="${logged_in_home}/.local/share/Steam/steamapps/common/Steam Controller Configs/$steamid3/config/configset_controller_neptune.vdf"

# Check if the configset_controller_neptune.vdf file exists
if [[ -f "$controller_config_path" ]]; then
    # Create a backup copy of the configset_controller_neptune.vdf file
    cp "$controller_config_path" "$controller_config_path.bak"
else
    echo "Could not find $controller_config_path"
fi




# TODO: relocate to standalone python script
# ! editorconfig will likely break this since bash uses tabs and python needs 4 spaces
# Run the Python script to create a new entry for a Steam shortcut
python3 -c "
import sys
import os
import subprocess
sys.path.insert(0, os.path.expanduser('${logged_in_home}/Downloads/NonSteamLaunchersInstallation/lib/python$python_version/site-packages'))
print(sys.path)  # Add this line to print the value of sys.path
import vdf  # Updated import
import binascii
import re
import shutil

# Print the path to the file where the vdf module was loaded from
print(vdf.__file__)

# Load the shortcuts.vdf file
with open('$shortcuts_vdf_path', 'rb') as f:
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
epicshortcutdirectory = '$epicshortcutdirectory'
gogshortcutdirectory = '$gogshortcutdirectory'
uplayshortcutdirectory = '$uplayshortcutdirectory'
battlenetshortcutdirectory = '$battlenetshortcutdirectory'
eaappshortcutdirectory = '$eaappshortcutdirectory'
amazonshortcutdirectory = '$amazonshortcutdirectory'
itchioshortcutdirectory = '$itchioshortcutdirectory'
legacyshortcutdirectory = '$legacyshortcutdirectory'
humbleshortcutdirectory = '$humbleshortcutdirectory'
indieshortcutdirectory = '$indieshortcutdirectory'
rockstarshortcutdirectory = '$rockstarshortcutdirectory'
glyphshortcutdirectory = '$glyphshortcutdirectory'
minecraftshortcutdirectory = '$minecraftshortcutdirectory'
psplusshortcutdirectory = '$psplusshortcutdirectory'
vkplayhortcutdirectory = '$vkplayhortcutdirectory'
#Streaming
chromedirectory = '$chromedirectory'
websites_str = '$custom_websites_str'
custom_websites = websites_str.split(', ')
START_FRESH = '$START_FRESH'


app_ids = []


def get_steam_shortcut_id(exe, appname):
    unique_id = ''.join([exe, appname])
    id_int = binascii.crc32(str.encode(unique_id)) | 0x80000000
    return id_int


app_id_to_name = {}


def create_new_entry(shortcutdirectory, appname, launchoptions, startingdir):
    if shortcutdirectory != '' and launchoptions != '':
        exe = f'"{shortcutdirectory}"'
        appid = get_steam_shortcut_id(exe, appname)
        app_ids.append(appid)
        app_id_to_name[appid] = appname


        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': f'{str(appid)}' if appid is not None else '',
            'appname': appname,
            'exe': shortcutdirectory,
            'StartDir': startingdir,
            'icon': f'${logged_in_home}/.steam/root/userdata/$steamid3/config/grid/{str(appid)}-icon.ico',
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

        # Check if an entry with the same appid already exists
        for key in shortcuts['shortcuts'].keys():
            if shortcuts['shortcuts'][key]['appid'] == new_entry['appid']:
                # A duplicate entry exists, so don't add the new entry
                return


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


create_new_entry('$epicshortcutdirectory', 'Epic Games', '$epiclaunchoptions', '$epicstartingdir')
create_new_entry('$gogshortcutdirectory', 'Gog Galaxy', '$goglaunchoptions', '$gogstartingdir')
create_new_entry('$uplayshortcutdirectory', 'Ubisoft Connect', '$uplaylaunchoptions', '$uplaystartingdir')
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
create_new_entry('$vkplayhortcutdirectory', 'VK Play', '$vkplaylaunchoptions', '$vkplaystartingdir')
create_new_entry('$chromedirectory', 'Xbox Game Pass', '$xboxchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'GeForce Now', '$geforcechromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Netflix', '$netlfixchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Hulu', '$huluchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Disney+', '$disneychromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Amazon Prime Video', '$amazonchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Youtube', '$youtubechromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Amazon Luna', '$lunachromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'Twitch', '$twitchchromelaunchoptions', '$chrome_startdir')
create_new_entry('$chromedirectory', 'movie-web', '$twitchchromelaunchoptions', '$chrome_startdir')


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
        create_new_entry('$chromedirectory', game_name, chromelaunch_options, '$chrome_startdir')

print(f'app_id_to_name: {app_id_to_name}')

# Save the updated shortcuts dictionary to the shortcuts.vdf file
with open('$shortcuts_vdf_path', 'wb') as f:
    vdf.binary_dump(shortcuts, f)

# Writes to the config.vdf File

excluded_appids = []
streaming_sites = ['Netflix', 'Hulu', 'Disney+', 'Amazon Prime Video', 'Youtube', 'movie-web', 'Amazon Luna', 'Twitch', 'Xbox Game Pass', 'GeForce Now']

for app_id, name in app_id_to_name.items():
    if name in streaming_sites:
        excluded_appids.append(app_id)

# Remove the app IDs of the streaming sites from the app_ids list
app_ids = [app_id for app_id in app_ids if app_id_to_name[app_id] not in streaming_sites]

# Remove the app IDs of the streaming sites from the app_id_to_name dictionary
app_id_to_name = {app_id: name for app_id, name in app_id_to_name.items() if name not in streaming_sites}



# Update the config.vdf file
with open('$config_vdf_path', 'r') as f:
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

# Save the updated config dictionary to the configset_controller_neptune.vdf file
with open('$controller_config_path', 'w') as f:
    vdf.dump(config, f)

# Define the path to the compatdata directory
compatdata_dir = '${logged_in_home}/.local/share/Steam/steamapps/compatdata'

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
        os.symlink(new_path, symlink_path)"


# TODO: might be better to relocate temp files to `/tmp` or even use `mktemp -d` since `rm -rf` is potentially dangerous without the `-i` flag
# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf "$download_dir"




#Setup NSLGameScanner.service
# Define your Python script path
python_script_path="${logged_in_home}/.config/systemd/user/NSLGameScanner.py"

# Define your GitHub link
github_link="https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/NSLGameScanner.py"

# Check if the service is already running
service_status=$(systemctl --user is-active nslgamescanner.service)

if [ "$service_status" = "active" ] || [ "$service_status" = "activating" ]
then
    echo "Service is already running or activating. Stopping the service..."
    systemctl --user stop nslgamescanner.service
fi

echo "Updating Python script from GitHub..."
# Download the Python script from GitHub
curl -o $python_script_path $github_link

echo "Starting the service..."
# Call your Python script
python3 $python_script_path

