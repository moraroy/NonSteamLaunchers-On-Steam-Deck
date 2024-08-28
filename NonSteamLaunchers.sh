#!/usr/bin/env bash

set -x              # activate debugging (execution shown)
set -o pipefail     # capture error from pipes
# set -eu           # exit immediately, undefined vars are errors

# ENVIRONMENT VARIABLES
# $USER
logged_in_user=$(logname 2>/dev/null || whoami)

# DBUS
# Add the DBUS_SESSION_BUS_ADDRESS environment variable
if [[ -z "$DBUS_SESSION_BUS_ADDRESS" ]]; then
  eval $(dbus-launch --sh-syntax)
  export DBUS_SESSION_BUS_ADDRESS
fi

export LD_LIBRARY_PATH=$(pwd)

# $UID
logged_in_uid=$(id -u "${logged_in_user}")

# $HOME
logged_in_home=$(eval echo "~${logged_in_user}")

# Debugging: Check the value of the DBUS_SESSION_BUS_ADDRESS environment variable
zenity --info --text="DBus session address: $DBUS_SESSION_BUS_ADDRESS" --no-session-bus




#Log
download_dir=$(eval echo ~$user)/Downloads/NonSteamLaunchersInstallation
log_file=$(eval echo ~$user)/Downloads/NonSteamLaunchers-install.log

# Remove existing log file if it exists
if [[ -f $log_file ]]; then
  rm $log_file
fi

# Redirect all output to the log file
exec > >(tee -a $log_file) 2>&1


# Version number (major.minor)
version=v3.9.3

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
        zenity --info --text="A new version is available: $latest_version\nPlease download it from GitHub." --width=200 --height=100 --timeout=5
    else
        echo "You are already running the latest version: $version"
    fi
}



# Get the command line arguments
args=("$@")
deckyplugin=false
installchrome=false

for arg in "${args[@]}"; do
  if [ "$arg" = "DeckyPlugin" ]; then
    deckyplugin=true
  elif [ "$arg" = "Chrome" ]; then
    installchrome=true
  fi
  done

# Check if the user wants to install Chrome
if $installchrome; then
  # Check if Google Chrome is already installed for the current user
  if flatpak list --user | grep com.google.Chrome &> /dev/null; then
    echo "Google Chrome is already installed for the current user"
    flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
  else
    # Check if the Flathub repository exists for the current user
    if flatpak remote-list --user | grep flathub &> /dev/null; then
      echo "Flathub repository exists for the current user"
    else
      # Add the Flathub repository for the current user
      flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    fi

    # Install Google Chrome for the current user
    flatpak install --user flathub com.google.Chrome -y

    # Run the flatpak --user override command
    flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
  fi
fi

if [ "${deckyplugin}" = false ]; then
	#Download Modules
	# Define the repository and the folders to clone
	repo_url='https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/archive/refs/heads/main.zip'
	folders_to_clone=('requests' 'urllib3' 'steamgrid' 'vdf' 'charset_normalizer')

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
	  wget -O "${zip_file_path}" "${repo_url}" || { echo 'Download failed with error code: $?'; exit 1; }

	  # Extract the zip file
	  unzip -d "${parent_folder}" "${zip_file_path}" || { echo 'Unzip failed with error code: $?'; exit 1; }

	  # Move the folders to the parent directory and delete the unnecessary files
	  for folder in "${folders_to_clone[@]}"; do
	    destination_path="${parent_folder}/${folder}"
	    source_path="${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main/Modules/${folder}"
	    if [ ! -d "${destination_path}" ]; then
	      mv "${source_path}" "${destination_path}" || { echo 'Move failed with error code: $?'; exit 1; }
	    fi
	  done

	  # Delete the downloaded zip file and the extracted repository folder
	  rm "${zip_file_path}"
	  rm -r "${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main"
	fi
	#End of Download Modules


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
	#End of Rough Update of the .py




	if [ -f "$env_vars" ]; then
	    echo "env_vars file found. Running the .py file."
	    live="and is LIVE."
	else
	    echo "env_vars file not found. Not Running the .py file."
	    live="and is not LIVE."
	fi



	# Check if "Decky Plugin" is one of the arguments
	decky_plugin=false
	for arg in "${args[@]}"; do
	  if [ "$arg" = "Decky Plugin" ]; then
	    decky_plugin=true
	    break
	  fi
	done

	# If the Decky Plugin argument is set, check if the env_vars file exists
	if [ "$decky_plugin" = true ]; then
	    if [ -f "$env_vars" ]; then
	        # If the env_vars file exists, run the .py file and continue with the script
	        echo "Decky Plugin argument set and env_vars file found. Running the .py file..."
	        python3 $python_script_path
	        echo "Python script ran. Continuing with the script..."
	    else
	        # If the env_vars file does not exist, exit the script
	        echo "Decky Plugin argument set but env_vars file not found. Exiting the script."
	        exit 0
	    fi
	else
	    # If the Decky Plugin argument is not set, continue with the script
	    echo "Decky Plugin argument not set. Continuing with the script..."
	    python3 $python_script_path
	    echo "env_vars file found. Running the .py file."
	    live="and is LIVE."
	fi
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

# TODO: parameterize hard-coded client versions (cf. 'app-26.1.9')
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
itchio_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch/app-26.1.9/itch.exe"
itchio_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher/pfx/drive_c/users/steamuser/AppData/Local/itch/app-26.1.9/itch.exe"
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
psplus_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
psplus_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
vkplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"
vkplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"
hoyoplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/HoYoPlay/launcher.exe"
hoyoplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher/pfx/drive_c/Program Files/HoYoPlay/launcher.exe"
nexon_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Nexon/Nexon Launcher/nexon_launcher.exe"
nexon_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher/pfx/drive_c/Program Files (x86)/Nexon/Nexon Launcher/nexon_launcher.exe"

# Chrome File Path
# chrome_installpath="/app/bin/chrome"
chrome_path="/usr/bin/flatpak"
chrome_startdir="\"/usr/bin\""
chromedirectory="\"$chrome_path\""

#Zenity Launcher Check Installation
function CheckInstallations {
    declare -A paths1 paths2 names
    paths1=(["epic_games"]="$epic_games_launcher_path1" ["gog_galaxy"]="$gog_galaxy_path1" ["uplay"]="$uplay_path1" ["battlenet"]="$battlenet_path1" ["eaapp"]="$eaapp_path1" ["amazongames"]="$amazongames_path1" ["itchio"]="$itchio_path1" ["legacygames"]="$legacygames_path1" ["humblegames"]="$humblegames_path1" ["indiegala"]="$indiegala_path1" ["rockstar"]="$rockstar_path1" ["glyph"]="$glyph_path1" ["psplus"]="$psplus_path1" ["vkplay"]="$vkplay_path1" ["hoyoplay"]=$hoyoplay_path1 ["nexon"]=$nexon_path1)
    paths2=(["epic_games"]="$epic_games_launcher_path2" ["gog_galaxy"]="$gog_galaxy_path2" ["uplay"]="$uplay_path2" ["battlenet"]="$battlenet_path2" ["eaapp"]="$eaapp_path2" ["amazongames"]="$amazongames_path2" ["itchio"]="$itchio_path2" ["legacygames"]="$legacygames_path2" ["humblegames"]="$humblegames_path2" ["indiegala"]="$indiegala_path2" ["rockstar"]="$rockstar_path2" ["glyph"]="$glyph_path2" ["psplus"]="$psplus_path2" ["vkplay"]="$vkplay_path2" ["hoyoplay"]=$hoyoplay_path2 ["nexon"]=$nexon_path2)
    names=(["epic_games"]="Epic Games" ["gog_galaxy"]="GOG Galaxy" ["uplay"]="Ubisoft Connect" ["battlenet"]="Battle.net" ["eaapp"]="EA App" ["amazongames"]="Amazon Games" ["itchio"]="itch.io" ["legacygames"]="Legacy Games" ["humblegames"]="Humble Games Collection" ["indiegala"]="IndieGala" ["rockstar"]="Rockstar Games Launcher" ["glyph"]="Glyph Launcher" ["psplus"]="Playstation Plus" ["vkplay"]="VK Play" ["hoyoplay"]="HoYoPlay" ["nexon"]="Nexon Launcher")

    for launcher in "${!names[@]}"; do
        if [[ -f "${paths1[$launcher]}" ]]; then
            declare -g "${launcher}_value"="FALSE"
            declare -g "${launcher}_text"="${names[$launcher]} ===> ${paths1[$launcher]}"
        elif [[ -f "${paths2[$launcher]}" ]]; then
            declare -g "${launcher}_value"="FALSE"
            declare -g "${launcher}_text"="${names[$launcher]} ===> ${paths2[$launcher]}"
        else
            declare -g "${launcher}_value"="FALSE"
            declare -g "${launcher}_text"="${names[$launcher]}"
        fi
    done
}

# Verify launchers are installed
function CheckInstallationDirectory {
    declare -A paths names
    paths=(["nonsteamlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ["epicgameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ["goggalaxylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ["uplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" ["battlenetlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ["eaapplauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ["amazongameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ["itchiolauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" ["legacygameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ["humblegameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ["indiegalalauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ["rockstargameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" ["glyphlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" ["pspluslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" ["vkplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" ["hoyoplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher" ["nexonlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher")
    names=(["nonsteamlauncher"]="NonSteamLaunchers" ["epicgameslauncher"]="EpicGamesLauncher" ["goggalaxylauncher"]="GogGalaxyLauncher" ["uplaylauncher"]="UplayLauncher" ["battlenetlauncher"]="Battle.netLauncher" ["eaapplauncher"]="TheEAappLauncher" ["amazongameslauncher"]="AmazonGamesLauncher" ["itchiolauncher"]="itchioLauncher" ["legacygameslauncher"]="LegacyGamesLauncher" ["humblegameslauncher"]="HumbleGamesLauncher" ["indiegalalauncher"]="IndieGalaLauncher" ["rockstargameslauncher"]="RockstarGamesLauncher" ["glyphlauncher"]="GlyphLauncher" ["pspluslauncher"]="PlaystationPlusLauncher" ["vkplaylauncher"]="VKPlayLauncher" ["hoyoplaylauncher"]="HoYoPlayLauncher" ["nexonlauncher"]="NexonLauncher")

    for launcher in "${!names[@]}"; do
        if [[ -d "${paths[$launcher]}" ]]; then
            declare -g "${launcher}_move_value"="TRUE"
        else
            declare -g "${launcher}_move_value"="FALSE"
        fi
    done
}


#Get SD Card Path
get_sd_path() {
    # This assumes that the SD card is mounted under /run/media/deck/
    local sd_path=$(df | grep '/run/media/deck/' | awk '{print $6}')
    echo $sd_path
}

# Function For Updating Proton-GE
function download_ge_proton() {
    echo "Downloading GE-Proton using the GitHub API"
    cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation"
    curl --retry 5 --retry-delay 0 --retry-max-time 60 -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .tar.gz)"
    if [ $? -ne 0 ]; then
        echo "Curl failed. Exiting."
        exit 1
    fi
    curl --retry 5 --retry-delay 0 --retry-max-time 60 -sLOJ "$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .sha512sum)"
    if [ $? -ne 0 ]; then
        echo "Curl failed. Exiting."
        exit 1
    fi
    sha512sum -c ./*.sha512sum
    if [ $? -ne 0 ]; then
        echo "Checksum verification failed. Exiting."
        exit 1
    fi
    tar -xf GE-Proton*.tar.gz -C "${logged_in_home}/.steam/root/compatibilitytools.d/"
    if [ $? -ne 0 ]; then
        echo "Tar extraction failed. Exiting."
        exit 1
    fi
    proton_dir=$(find "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
    echo "All done :)"
}

function update_proton() {
    echo "0"
    echo "# Detecting, Updating and Installing GE-Proton...please wait..."

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
        download_ge_proton
    else
        # Check if installed version is the latest version
        installed_version=$(basename $proton_dir | sed 's/GE-Proton-//')
        latest_version=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep tag_name | cut -d '"' -f 4)
        if [ "$installed_version" != "$latest_version" ]; then
            download_ge_proton
        fi
    fi
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
    selected_launchers=$(zenity --list --text="Which launchers do you want to download and install?" --checklist --column="$version" --column="Default = one App ID Installation, One Prefix, NonSteamLaunchers - updated the NSLGameScanner.py $live" FALSE "SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX" $epic_games_value "$epic_games_text" $gog_galaxy_value "$gog_galaxy_text" $uplay_value "$uplay_text" $battlenet_value "$battlenet_text" $amazongames_value "$amazongames_text" $eaapp_value "$eaapp_text" $legacygames_value "$legacygames_text" $itchio_value "$itchio_text" $humblegames_value "$humblegames_text" $indiegala_value "$indiegala_text" $rockstar_value "$rockstar_text" $glyph_value "$glyph_text" $psplus_value "$psplus_text" $vkplay_value "$vkplay_text" $hoyoplay_value "$hoyoplay_text" $nexon_value "$nexon_text" FALSE "RemotePlayWhatever" FALSE "Fortnite" FALSE "Xbox Game Pass" FALSE "GeForce Now" FALSE "Amazon Luna" FALSE "Netflix" FALSE "Hulu" FALSE "Disney+" FALSE "Amazon Prime Video" FALSE "Youtube" FALSE "Twitch" --width=800 --height=740 --extra-button="Uninstall" --extra-button="Stop NSLGameScanner" --extra-button="Start Fresh" --extra-button="Move to SD Card" --extra-button="Update Proton-GE")

    # Check if the user clicked the 'Cancel' button or selected one of the extra buttons
    if [ $? -eq 1 ] || [[ $selected_launchers == "Start Fresh" ]] || [[ $selected_launchers == "Move to SD Card" ]] || [[ $selected_launchers == "Uninstall" ]]; then
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

	IFS=" "
    for arg in "${args[@]}"; do
        if [[ "$arg" =~ ^https?:// ]]; then
			website=${arg#https://}

            # Check if the arg is not an empty string before adding it to the custom_websites array
            if [ -n "$website" ]; then
                custom_websites+=("$website")
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
if [ $? -eq 1 ] && [[ $options != "Start Fresh" ]] && [[ $options != "Move to SD Card" ]] && [[ $options != "Uninstall" ]]; then
    # The cancel button was clicked
    echo "The cancel button was clicked"
    exit 1
fi

# Check if no options were selected and no custom website was provided
if [ -z "$options" ] && [ -z "$custom_websites" ]; then
    # No options were selected and no custom website was provided
    zenity --error --text="No options were selected and no custom website was provided. The script will now exit." --width=200 --height=150 --timeout=5
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
    folder_names=("EpicGamesLauncher" "GogGalaxyLauncher" "UplayLauncher" "Battle.netLauncher" "TheEAappLauncher" "AmazonGamesLauncher" "itchioLauncher" "LegacyGamesLauncher" "HumbleGamesLauncher" "IndieGalaLauncher" "RockstarGamesLauncher" "GlyphLauncher" "PlaystationPlusLauncher" "VKPlayLauncher" "HoYoPlayLauncher" "NexonLauncher")

    # Define an array of app IDs
    app_ids=("3772819390" "4294900670" "4063097571" "3786021133" "3448088735" "3923904787" "3440562512" "2948446662" "3908676077" "4206469918" "3303169468" "3595505624" "4272271078" "3259996605" "2588786779" "4090616647" "3494943831" "2390200925" "4253976432" "2221882453" "2296676888" "2486751858" "3974004104" "3811372789" "3788101956" "3782277090" "3640061468" "3216372511" "2882622939" "2800812206" "2580882702" "4022508926")

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
    rm -rf "/run/media/mmcblk0p1/PlaystationPlusLauncher/"
    rm -rf "/run/media/mmcblk0p1/VKPlayLauncher/"
    rm -rf "/run/media/mmcblk0p1/HoYoPlayLauncher/"
    rm -rf "/run/media/mmcblk0p1/NexonLauncher/"
    rm -rf ${logged_in_home}/Downloads/NonSteamLaunchersInstallation
    rm -rf ${logged_in_home}/.config/systemd/user/Modules
    rm -rf ${logged_in_home}/.config/systemd/user/env_vars
    rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py
    rm -rf ${logged_in_home}/.local/share/applications/RemotePlayWhatever
    rm -rf ${logged_in_home}/.local/share/applications/RemotePlayWhatever.desktop
    rm -rf ${logged_in_home}/Downloads/NonSteamLaunchers-install.log

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



#Set Downloads INFO
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


# Set the URL to download the Playstation Launcher file from
psplus_url=https://download-psplus.playstation.com/downloads/psplus/pc/latest

# Set the path to save the Playstation Launcher to
psplus_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/PlayStationPlus-12.2.0.exe


# Set the URL to download the VK Play Launcher file from
vkplay_url=https://static.gc.vkplay.ru/VKPlayLoader.exe

# Set the path to save the VK Play Launcher to
vkplay_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/VKPlayLoader.exe

# Set the URL to download the VK Play Launcher file from
hoyoplay_url="https://download-porter.hoyoverse.com/download-porter/2024/06/07/hyp_global_setup_1.0.5.exe?trace_key=HoYoPlay_install_ua_109daee2060b"

# Set the path to save the Hoyo Play Launcher to
hoyoplay_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/HoYoPlay_install_ua_109daee2060b.exe.exe

# Set the URL to download the Nexon Launcher file from
nexon_url="https://download.nxfs.nexon.com/download-launcher?file=NexonLauncherSetup.exe&client-id=959013368.1720525616"

# Set the path to save the Nexon Launcher to
nexon_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/NexonLauncherSetup.exe
#End of Downloads INFO





# Function to handle common uninstallation tasks
handle_uninstall_common() {
    compatdata_dir=$1
    uninstaller_path=$2
    uninstaller_options=$3
    app_name=$4

    # Set the path to the Proton directory
    proton_dir=$(find "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

    # Set the paths for the environment variables
    STEAM_RUNTIME="${logged_in_home}/.steam/root/ubuntu12_32/steam-runtime/run.sh"
    STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"
    STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${compatdata_dir}"

    # Export the STEAM_COMPAT_DATA_PATH variable
    export STEAM_COMPAT_DATA_PATH
    export STEAM_COMPAT_CLIENT_INSTALL_PATH

    # Run the uninstaller using Proton with the specified options
    echo "Running uninstaller using Proton with the specified options"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$uninstaller_path" $uninstaller_options

    # Display Zenity window
    zenity --info --text="$app_name has been uninstalled." --width=200 --height=150 &
    sleep 3
    killall zenity
}

# Function to handle EA App uninstallation
handle_uninstall_ea() {
    mkdir -p ${logged_in_home}/Downloads/NonSteamLaunchersInstallation

    # Download EA App file
    if [ ! -f "$eaapp_file" ]; then
        echo "Downloading EA App file"
        wget $eaapp_url -O $eaapp_file
    fi

    handle_uninstall_common "$1" "$eaapp_file" "/uninstall /quiet" "EA App"
}

# Function to handle GOG Galaxy uninstallation
handle_uninstall_gog() {
    gog_uninstaller="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files (x86)/GOG Galaxy/unins000.exe"
    handle_uninstall_common "$1" "$gog_uninstaller" "/SILENT" "GOG Galaxy"
}

# Uninstall EA App
if [[ $uninstall_options == *"Uninstall EA App"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts" ]]; then
        handle_uninstall_ea "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts" ]]; then
        handle_uninstall_ea "TheEAappLauncher"
    fi
fi

# Uninstall GOG Galaxy
if [[ $uninstall_options == *"Uninstall GOG Galaxy"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy" ]]; then
        handle_uninstall_gog "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy" ]]; then
        handle_uninstall_gog "GogGalaxyLauncher"
    fi
fi

# Function to handle Legacy Games Launcher uninstallation
handle_uninstall_legacy() {
    legacy_uninstaller="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher/Uninstall Legacy Games Launcher.exe"
    handle_uninstall_common "$1" "$legacy_uninstaller" "/allusers /S" "Legacy Games Launcher"
}

# Uninstall Legacy Games Launcher
if [[ $uninstall_options == *"Uninstall Legacy Games Launcher"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher" ]]; then
        handle_uninstall_legacy "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher" ]]; then
        handle_uninstall_legacy "LegacyGamesLauncher"
    fi
fi

# Function to handle PlayStation Plus uninstallation
handle_uninstall_psplus() {
    psplus_uninstaller="MsiExec.exe"
    psplus_uninstaller_options="/X{3DE02040-3CB7-4D4A-950E-773F04FC4DE8} /quiet"
    handle_uninstall_common "$1" "$psplus_uninstaller" "$psplus_uninstaller_options" "PlayStation Plus"
}

# Uninstall PlayStation Plus
if [[ $uninstall_options == *"Uninstall PlayStation Plus"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus" ]]; then
        handle_uninstall_psplus "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/pfx/drive_c/Program Files (x86)/PlayStationPlus" ]]; then
        handle_uninstall_psplus "PlaystationPlusLauncher"
    fi
fi



uninstall_launcher() {
    local uninstall_options=$1
    local launcher=$2
    local path1=$3
    local path2=$4
    local remove_path1=$5
    local remove_path2=$6
    shift 6

    if [[ $uninstall_options == *"Uninstall $launcher"* ]]; then
        if [[ -f "$path1" ]]; then
            rm -rf "$remove_path1"
            zenity --info --text="$launcher has been uninstalled." --width=200 --height=150 &
            sleep 3
            killall zenity
        elif [[ -f "$path2" ]]; then
            rm -rf "$remove_path2"
            zenity --info --text="$launcher has been uninstalled." --width=200 --height=150 &
            sleep 3
            killall zenity
        fi
        for env_var_prefix in "$@"; do  # Loop over the remaining arguments
            sed -i "/^export ${env_var_prefix}.*/Id" "${logged_in_home}/.config/systemd/user/env_vars"
        done
        echo "Deleted environment variables for $launcher"
    fi
}

# Function to process uninstall options
process_uninstall_options() {
    local uninstall_options=$1
    if [[ -n $uninstall_options ]]; then
        # Call uninstall_launcher for each launcher
        # Add more launchers as needed
        if [[ $uninstall_options == *"Uninstall GOG Galaxy"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy" ]]; then
                handle_uninstall_gog "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "GOG Galaxy" "$gog_galaxy_path1" "$gog_galaxy_path2" "" "" "gog"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy" ]]; then
                handle_uninstall_gog "GogGalaxyLauncher"
                uninstall_launcher "$uninstall_options" "GOG Galaxy" "$gog_galaxy_path1" "$gog_galaxy_path2" "" "" "gog"
            fi
        fi
        if [[ $uninstall_options == *"Uninstall EA App"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts" ]]; then
                handle_uninstall_ea "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "EA App" "$eaapp_path1" "$eaapp_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe" "eaapp" "ea_app"
                sed -i '/repaireaapp/d' "${logged_in_home}/.config/systemd/user/env_vars"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts" ]]; then
                handle_uninstall_ea "TheEAappLauncher"
                uninstall_launcher "$uninstall_options" "EA App" "$eaapp_path1" "$eaapp_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe" "eaapp" "ea_app"
                sed -i '/repaireaapp/d' "${logged_in_home}/.config/systemd/user/env_vars"
            fi
        fi
        if [[ $uninstall_options == *"Uninstall Legacy Games"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games" ]]; then
                handle_uninstall_legacy "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Legacy Games" "$legacygames_path1" "$legacygames_path2" "" "" "legacy"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/pfx/drive_c/Program Files/Legacy Games" ]]; then
                handle_uninstall_legacy "LegacyGamesLauncher"
                uninstall_launcher "$uninstall_options" "Legacy Games" "$legacygames_path1" "$legacygames_path2" "" "" "legacy"
            fi
        fi
        if [[ $uninstall_options == *"Uninstall Playstation Plus"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus" ]]; then
                handle_uninstall_psplus "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Playstation Plus" "$psplus_path1" "$psplus_path2" "" "" "psplus"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" ]]; then
                handle_uninstall_psplus "PlaystationPlusLauncher"
                uninstall_launcher "$uninstall_options" "Playstation Plus" "$psplus_path1" "$psplus_path2" "" "" "psplus"
            fi
        fi

        if [[ $uninstall_options == *"Uninstall RemotePlayWhatever"* ]]; then
            rm -rf "${logged_in_home}/.local/share/applications/RemotePlayWhatever"
            rm -rf "${logged_in_home}/.local/share/applications/RemotePlayWhatever.desktop"

            zenity --info --text="RemotePlayWhatever has been uninstalled." --width=200 --height=150 &
            sleep 3
            killall zenity
        fi
        uninstall_launcher "$uninstall_options" "Uplay" "$uplay_path1" "$uplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" "uplay" "ubisoft"
        uninstall_launcher "$uninstall_options" "Battle.net" "$battlenet_path1" "$battlenet_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" "battle" "bnet"
        uninstall_launcher "$uninstall_options" "Epic Games" "$epic_games_launcher_path1" "$epic_games_launcher_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" "epic"
        uninstall_launcher "$uninstall_options" "Amazon Games" "$amazongames_path1" "$amazongames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" "amazon"
        uninstall_launcher "$uninstall_options" "itch.io" "$itchio_path1" "$itchio_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" "itchio"
        uninstall_launcher "$uninstall_options" "Humble Bundle" "$humblegames_path1" "$humblegames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" "humble"
        uninstall_launcher "$uninstall_options" "IndieGala" "$indiegala_path1" "$indiegala_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" "indie"
        uninstall_launcher "$uninstall_options" "Rockstar Games Launcher" "$rockstar_path1" "$rockstar_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" "rockstar"
        uninstall_launcher "$uninstall_options" "Glyph Launcher" "$glyph_path1" "$glyph_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Glyph" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" "glyph"
        uninstall_launcher "$uninstall_options" "VK Play" "$vkplay_path1" "$vkplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" "vkplay"
        uninstall_launcher "$uninstall_options" "HoYoPlay" "$hoyoplay_path1" "$hoyoplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/HoYoPlay" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher" "hoyoplay"
        uninstall_launcher "$uninstall_options" "Nexon Launcher" "$nexon_path1" "$nexon_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Nexon" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher" "nexon"
    fi
    # If the uninstall was successful,  set uninstalled_any_launcher to true
    if [ $? -eq 0 ]; then
        uninstalled_any_launcher=true
    fi
}



if [ $# -gt 0 ]; then
    # Add a flag that gets set when any launcher is uninstalled
    uninstalled_any_launcher=false
    for arg in "$@"; do
        if [[ $arg == *"Uninstall "* ]]; then
            launcher=${arg#"Uninstall "}
            # Set the flag to true
            uninstalled_any_launcher=true
            if [[ -n $launcher ]]; then
                process_uninstall_options "Uninstall $launcher"
            fi
        fi
    done
    # Check the flag after the loop
    if $uninstalled_any_launcher; then
        echo "Uninstallation completed successfully."
        rm -rf "$download_dir"
        exit 0
    fi
else
    # No command line arguments were provided
    # Check if the Uninstall button was clicked in the GUI
    if [[ $options == "Uninstall" ]] || [[ $selected_launchers == "Uninstall" ]]; then
        # The Uninstall button was clicked in the GUI
        # Display the zenity window to select launchers to uninstall
        uninstall_options=$(zenity --list --checklist \
            --title="Uninstall Launchers" \
            --text="Select the launchers you want to Uninstall..." \
            --column="Select" --column="This will delete the launcher and all of its games and files." \
            --width=508 --height=507 \
            FALSE "Epic Games" \
            FALSE "GOG Galaxy" \
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
            FALSE "Playstation Plus" \
            FALSE "VK Play" \
            FALSE "HoYoPlay" \
            FALSE "Nexon Launcher" \
            FALSE "RemotePlayWhatever" \
        )
        # Convert the returned string to an array
        IFS='|' read -r -a uninstall_options_array <<< "$uninstall_options"
        # Loop through the array and uninstall each selected launcher
        for launcher in "${uninstall_options_array[@]}"; do
            process_uninstall_options "Uninstall $launcher"
        done
        echo "Uninstallation completed successfully."
        rm -rf "$download_dir"
        exit 0
    fi
fi
#End of Uninstall


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

# Check if the first command line argument is "Move to SD Card"
if [[ $1 == "Move to SD Card" ]]; then
    # Shift the arguments to remove the first one
    shift

    # Use the remaining arguments as the launcher IDs to move
    for launcher in "$@"; do
        move_to_sd "$launcher"
    done
else
    # The first command line argument is not "Move to SD Card"
    # Use Zenity to get the launcher IDs to move
    if [[ $options == "Move to SD Card" ]]; then
        CheckInstallationDirectory

    move_options=$(zenity --list --text="Which launcher IDs do you want to move to the SD card?" --checklist --column="Select" --column="Launcher ID" $nonsteamlauncher_move_value "NonSteamLaunchers" $epicgameslauncher_move_value "EpicGamesLauncher" $goggalaxylauncher_move_value "GogGalaxyLauncher" $uplaylauncher_move_value "UplayLauncher" $battlenetlauncher_move_value "Battle.netLauncher" $eaapplauncher_move_value "TheEAappLauncher" $amazongameslauncher_move_value "AmazonGamesLauncher" $itchiolauncher_move_value "itchioLauncher" $legacygameslauncher_move_value "LegacyGamesLauncher" $humblegameslauncher_move_value "HumbleGamesLauncher" $indiegalalauncher_move_value "IndieGalaLauncher" $rockstargameslauncher_move_value "RockstarGamesLauncher" $glyphlauncher_move_value "GlyphLauncher" $pspluslauncher_move_value "PlaystationPlusLauncher" $vkplaylauncher_move_value "VKPlayLauncher" $hoyoplaylauncher_move_value "HoYoPlayLauncher" $nexonlauncher_move_value "NexonLauncher" --width=335 --height=524)

    if [ $? -eq 0 ]; then
        zenity --info --text="The selected directories have been moved to the SD card and symbolic links have been created." --width=200 --height=150

        IFS="|" read -ra selected_launchers <<< "$move_options"
        for launcher in "${selected_launchers[@]}"; do
            move_to_sd "$launcher"
        done
    fi

        IFS="|" read -ra selected_launchers <<< "$move_options"
        for launcher in "${selected_launchers[@]}"; do
            move_to_sd "$launcher"
        done

        if [ $? -eq 0 ]; then
            zenity --info --text="The selected directories have been moved to the SD card and symbolic links have been created." --width=200 --height=150
        fi
        # Exit the script
        exit 0
    fi

fi

function stop_service {
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
}

# Get the command line arguments
args=("$@")

# Check if the Stop NSLGameScanner option was passed as a command line argument or clicked in the GUI
if [[ " ${args[@]} " =~ " Stop NSLGameScanner " ]] || [[ $options == "Stop NSLGameScanner" ]]; then
    stop_service

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
        stop_service
        exit 0
    fi
fi


# TODO: probably better to break this subshell into a function that can then be redirected to zenity
# Massive subshell pipes into `zenity --progress` around L2320 for GUI rendering
(

#Update Proton GE
# Call the function directly
update_proton

# Also call the function when the button is pressed
if [[ $options == *"Update Proton-GE"* ]]; then
    update_proton
fi


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




###Launcher Installations
#Terminate Processese
function terminate_processes {
    process_names=("$@")  # Array of process names
    for process_name in "${process_names[@]}"; do
        end=$((SECONDS+75))  # Timeout
        while ! pgrep -f "$process_name" > /dev/null; do
            if [ $SECONDS -gt $end ]; then
                echo "Timeout while waiting for $process_name to start"
                return 1
            fi
            sleep 1
        done
        echo "Attempting to terminate $process_name"
        pkill -f "$process_name"
        end=$((SECONDS+60))  # Timeout
        while pgrep -f "$process_name" > /dev/null; do
            if [ $SECONDS -gt $end ]; then
                echo "Timeout while trying to kill $process_name, force terminating"
                pkill -9 -f "$process_name"
                break
            fi
            sleep 1
        done
        echo "$process_name terminated successfully"
    done
}


function install_gog {
    echo "45"
    echo "# Downloading & Installing Gog Galaxy...Please wait..."

    # Cancel & Exit the GOG Galaxy Setup Wizard
    end=$((SECONDS+60))  # Timeout after 60 seconds
    while true; do
        if pgrep -f "GalaxySetup.tmp" > /dev/null; then
            pkill -f "GalaxySetup.tmp"
            break
        fi
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while trying to kill GalaxySetup.tmp"
            break
        fi
        sleep 1
    done

    # Navigate to %LocalAppData%\Temp
    cd "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/Temp"

    # Find the GalaxyInstaller_XXXXX folder and copy it to C:\Downloads
    for dir in GalaxyInstaller_*; do
        if [ -d "$dir" ]; then
            galaxy_installer_folder="$dir"
            break
        fi
    done
    cp -r "$galaxy_installer_folder" ${logged_in_home}/Downloads/NonSteamLaunchersInstallation/

    # Navigate to the C:\Downloads\GalaxyInstaller_XXXXX folder
    cd ${logged_in_home}/Downloads/NonSteamLaunchersInstallation/"$(basename $galaxy_installer_folder)"

    # Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
    echo "Running GalaxySetup.exe with the /VERYSILENT and /NORESTART options"
    "$STEAM_RUNTIME" "$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART
}




# Battle.net specific installation steps
function install_battlenet {
    terminate_processes "Battle.net.exe" #"BlizzardError.exe"
    # Second installation
    echo "Starting second installation of Battle.net"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net" &
    second_install_pid=$!
    # Wait for both installations to complete
    wait $first_install_pid
    wait $second_install_pid
    terminate_processes "Battle.net.exe" #"BlizzardError.exe"
}

# Amazon Games specific installation steps
function install_amazon {
    terminate_processes "Amazon Games.exe"
}

function install_eaapp {
    terminate_processes "EADesktop.exe"

    # Additional download for EA App
    eaapp_download_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/Downloads/"
    eaapp_file_name="EAappInstaller.exe"  # Replace with the actual file name if different

    # Create the directory if it doesn't exist
    mkdir -p "$eaapp_download_dir"

    # Download the file
    wget "$eaapp_url" -O "${eaapp_download_dir}${eaapp_file_name}"
}


# itch.io specific installation steps
function install_itchio {
    terminate_processes "itch.exe"
}

# Humble Games specific installation steps
function install_humblegames {
    # Create the handle-humble-scheme script
    if [[ ! -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme" ]]; then
        cat << EOF > "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
    #!/usr/bin/env sh
    set -e
    export STEAM_COMPAT_CLIENT_INSTALL_PATH=~/.local/share/Steam
    export STEAM_COMPAT_DATA_PATH=~/.steam/steam/steamapps/compatdata/$appid
    FIXED_SCHEME="\$(echo "\$1" | sed "s/?/\//")"
    echo \$FIXED_SCHEME > "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/.auth"
    "$STEAM_RUNTIME" "$proton_dir/proton" run ~/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd
EOF
        chmod +x "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme"
    fi

    # Create the Humble-scheme-handler.desktop file
    if [[ ! -f "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop" ]]; then
        cat << EOF > "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
    [Desktop Entry]
    Name=Humble App (Login)
    Comment=Target for handling Humble App logins. You should not run this manually.
    Exec=${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/handle-humble-scheme %u
    Type=Application
    MimeType=x-scheme-handler/humble;
EOF
        desktop-file-install --rebuild-mime-info-cache --dir=${logged_in_home}/.local/share/applications "${logged_in_home}/.local/share/applications/Humble-scheme-handler.desktop"
    fi

    # Create the start-humble.cmd script
    if [[ ! -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd" ]]; then
        cat << EOF > "${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/start-humble.cmd"
    @echo off
    cd /d "C:\Program Files\Humble App\"
    set /p Url=<"C:\.auth"
    if defined Url (
        start "" "Humble App.exe" "%Url%"
    ) else (
        start "" "Humble App.exe" "%*"
    )
    exit
EOF
    fi
    wait
}

# Rockstar Games Launcher specific installation steps
function install_rockstar {
    #Manually Install Rockstar Game Launcher

    # Define directories and files
    toolsDir=$(dirname "$(readlink -f "$0")")
    checksumType='sha256'
    rstarInstallUnzipFileDir="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/Rockstar"
    rstarInstallDir="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}/pfx/drive_c/Program Files/Rockstar Games/Launcher"
    rstarStartMenuRunShortcutFolder="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}/pfx/drive_c/users/steamuser/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Rockstar Games"
    rstarStartMenuRunShortcut="$rstarStartMenuRunShortcutFolder/Rockstar Games Launcher.lnk"
    rstarRunTarget="$rstarInstallDir/LauncherPatcher.exe"
    rstarInstallUnzipFile=$rockstar_file
    url=$rockstar_url

    # Define checksum
    checksum='589f6b251424e01dcd912e6a059d2d98f33fa73aadcd6376c0e1f1109f594b48'

    # Verify checksum (sha256sum command may vary based on distribution)
    echo "$checksum $rstarInstallUnzipFile" | sha256sum -c -

    # Extract files from EXE and capture the output
    output=$(7z e "$rockstar_file" -o"$rstarInstallUnzipFileDir" -aoa)

    # Parse the output to get the ProductVersion
    version=$(echo "$output" | grep 'ProductVersion:' | awk '{print $2}')

    ls -l "$rstarInstallUnzipFileDir"

    # Create Program Files folders to prepare for copying files
    mkdir -p "$rstarInstallDir/Redistributables/VCRed"
    mkdir -p "$rstarInstallDir/ThirdParty/Steam"
    mkdir -p "$rstarInstallDir/ThirdParty/Epic"

    cp "$rstarInstallUnzipFileDir/449" "$rstarInstallDir/Redistributables/VCRed/vc_redist.x64.exe"
    cp "$rstarInstallUnzipFileDir/450" "$rstarInstallDir/Redistributables/VCRed/vc_redist.x86.exe"
    cp "$rstarInstallUnzipFileDir/451" "$rstarInstallDir/ThirdParty/Steam/steam_api64.dll"

    while IFS=' ' read -r number dll; do
    dll=${dll//\//\\}
    filename=$(basename "$dll" | tr -d '\r')

    if [[ $dll == Redistributables\\* ]] || [[ $dll == ThirdParty\\Steam\\* ]] || [[ $number == 474 ]] || [[ $number == 475 ]]; then
        continue
    elif [[ $dll == ThirdParty\\Epic\\* ]]; then
        cp "$rstarInstallUnzipFileDir/$number" "$epicInstallDir/$filename"
    else
        cp "$rstarInstallUnzipFileDir/$number" "$rstarInstallDir/$filename"
    fi
    done < "$download_dir/Rockstar/211"

    cp "$rstarInstallUnzipFileDir/474" "$rstarInstallDir/ThirdParty/Epic/EOSSDK-Win64-Shipping.dll"
    cp "$rstarInstallUnzipFileDir/475" "$rstarInstallDir/ThirdParty/Epic/EOSSDK-Win64-Shipping-1.14.2.dll"

    # Use a loop for chmod commands
    for file in Launcher.exe LauncherPatcher.exe offline.pak RockstarService.exe RockstarSteamHelper.exe uninstall.exe; do
    chmod +x "$rstarInstallDir/$file"
    done

    size_kb=$(du -sk "$rstarInstallDir" | cut -f1)
    size_hex=$(printf '%08x\n' $size_kb)

    wine_registry_path="HKEY_LOCAL_MACHINE\\Software\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Rockstar Games Launcher"

    # Use a loop for registry commands
    declare -A registry_keys=(
    ["DisplayName"]="Rockstar Games Launcher"
    ["DisplayIcon"]="C:\\Program Files\\Rockstar Games\\Launcher\\Launcher.exe, 0"
    ["DisplayVersion"]="$version"
    ["Publisher"]="Rockstar Games"
    ["InstallLocation"]="C:\\Program Files\\Rockstar Games\\Launcher"
    ["EstimatedSize"]="0x$size_hex"
    ["UninstallString"]="C:\\Program Files\\Rockstar Games\\Launcher\\uninstall.exe"
    ["QuietUninstallString"]="\"C:\\Program Files\\Rockstar Games\\Launcher\\uninstall.exe\" /S"
    ["HelpLink"]="https://www.rockstargames.com/support"
    ["URLInfoAbout"]="https://www.rockstargames.com/support"
    ["URLUpdateInfo"]="https://www.rockstargames.com"
    ["NoModify"]="0x1"
    ["NoRepair"]="0x1"
    ["Comments"]="Rockstar Games Launcher"
    ["Readme"]="https://www.rockstargames.com/support"
    )

    for key in "${!registry_keys[@]}"; do
    "$STEAM_RUNTIME" "$proton_dir/proton" run reg add "$wine_registry_path" /v "$key" /t REG_SZ /d "${registry_keys[$key]}" /f
    done

    "$STEAM_RUNTIME" "$proton_dir/proton" run "$rstarInstallDir/Redistributables/VCRed/vc_redist.x64.exe" /install /quiet /norestart
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$rstarInstallDir/Redistributables/VCRed/vc_redist.x86.exe" /install /quiet /norestart
    wait
}

# VK Play specific installation steps
function install_vkplay {
    terminate_processes "GameCenter.exe"
}

# Nexon specific installation steps
function install_nexon {
    terminate_processes "nexon_runtime.e"
}


# HoYo specific installation steps
function install_hoyo {
    hoyo_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}/pfx/drive_c/Program Files/HoYoPlay"
    installer_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/HoYoPlay_install_ua_f368eee6d08d.exe"
    target_dir="${hoyo_dir}/1.0.5.88"

    echo "Creating directory for HoYoPlay..."
    mkdir -p "${hoyo_dir}" || { echo "Failed to create directory"; return 1; }

    echo "Copying installer to the target directory..."
    cp "${installer_file}" "${hoyo_dir}" || { echo "Failed to copy installer"; return 1; }

    echo "Changing directory to the target directory..."
    cd "${hoyo_dir}" || { echo "Failed to change directory"; return 1; }

    echo "Running 7z extraction..."
    output=$(7z x "HoYoPlay_install_ua_f368eee6d08d.exe" -o"${hoyo_dir}" -aoa)
    if [ $? -ne 0 ]; then
        echo "Extraction failed"
        echo "7z output: $output"
        return 1
    fi

    echo "Extraction completed successfully"

    echo "Copying launcher.exe to the HoYoPlay directory..."
    cp "${target_dir}/launcher.exe" "${hoyo_dir}/launcher.exe" || { echo "Failed to copy launcher.exe"; return 1; }

    echo "Running HYP.exe..."
    "$STEAM_RUNTIME" "$proton_dir/proton" run "${target_dir}/HYP.exe" || { echo "Failed to run HYP.exe"; return 1; } &
    sleep 5  # Wait for 5 seconds before terminating HYP.exe
    terminate_processes "HYP.exe"

    echo "Removing installer file..."
    rm -f "${hoyo_dir}/HoYoPlay_install_ua_f368eee6d08d.exe" || { echo "Failed to remove installer file"; return 1; }

    echo "HoYoPlay installation steps completed successfully"
}


#Launcher Installs
function install_launcher {
    launcher_name=$1
    appid_name=$2
    file_name=$3
    file_url=$4
    run_command=$5
    progress_update=$6
    pre_install_command=$7
    post_install_command=$8
    run_in_background=$9  # New parameter to specify if the launcher should run in the background

    echo "${progress_update}"
    echo "# Downloading & Installing ${launcher_name}...please wait..."

    # Check if the user selected the launcher
    if [[ $options == *"${launcher_name}"* ]]; then
        # User selected the launcher
        echo "User selected ${launcher_name}"

        # Set the appid for the launcher
        if [ "$use_separate_appids" = true ]; then
            appid=${appid_name}
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

        # Set the STEAM_COMPAT_DATA_PATH environment variable for the launcher
        export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

        # Download file
        if [ ! -f "$file_name" ]; then
            echo "Downloading ${file_name}"
            wget $file_url -O $file_name
        fi

        # Execute the pre-installation command, if provided
        if [ -n "$pre_install_command" ]; then
            echo "Executing pre-install command for ${launcher_name}"
            eval "$pre_install_command"
        fi

        # Run the file using Proton with the specified command
        echo "Running ${file_name} using Proton with the specified command"
        if [ "$run_in_background" = true ]; then
            if [ "$launcher_name" = "GOG Galaxy" ]; then
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$exe_file" &
                install_gog
            elif [ "$launcher_name" = "Battle.net" ]; then
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net" &
                install_battlenet
            elif [ "$launcher_name" = "Amazon Games" ]; then
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$amazon_file" &
                install_amazon
            elif [ "$launcher_name" = "Humble Games Collection" ]; then
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$humblegames_file" /S /D="C:\Program Files\Humble App"
                wait
                install_humblegames
            elif [ "$launcher_name" = "Rockstar Games Launcher" ]; then
                install_rockstar
            else
                "$STEAM_RUNTIME" "$proton_dir/proton" run ${run_command} &
            fi
        else
            "$STEAM_RUNTIME" "$proton_dir/proton" run ${run_command}
        fi


        # Execute the post-installation command, if provided
        if [ -n "$post_install_command" ]; then
            echo "Executing post-install command for ${launcher_name}"
            eval "$post_install_command"
        fi

        # Wait for the installation process to complete
        wait
    fi
}

# Install Epic Games Launcher
install_launcher "Epic Games" "EpicGamesLauncher" "$msi_file" "$msi_url" "MsiExec.exe /i "$msi_file" -opengl /qn" "30" "" ""

# Install GOG Galaxy
install_launcher "GOG Galaxy" "GogGalaxyLauncher" "$exe_file" "$exe_url" "$exe_file" "40" "" "" true

# Install Ubisoft Connect
install_launcher "Ubisoft Connect" "UplayLauncher" "$ubi_file" "$ubi_url" "$ubi_file /S" "50" "" ""

# Install Battle.net
install_launcher "Battle.net" "Battle.netLauncher" "$battle_file" "$battle_url" "" "70" "" "" true

#Install Amazon Games
install_launcher "Amazon Games" "AmazonGamesLauncher" "$amazon_file" "$amazon_url" "" "80" "" "" true

#Install EA App
install_launcher "EA App" "TheEAappLauncher" "$eaapp_file" "$eaapp_url" "$eaapp_file /quiet" "88" "" "install_eaapp" true

# Install itch.io
install_launcher "itch.io" "itchioLauncher" "$itchio_file" "$itchio_url" "$itchio_file --silent" "89" "" "install_itchio" true

# Install Legacy Games
install_launcher "Legacy Games" "LegacyGamesLauncher" "$legacygames_file" "$legacygames_url" "$legacygames_file /S" "90" "" ""

# Install Humble Games
install_launcher "Humble Games Collection" "HumbleGamesLauncher" "$humblegames_file" "$humblegames_url" "" "91" "" "" true

# Install IndieGala
install_launcher "IndieGala" "IndieGalaLauncher" "$indiegala_file" "$indiegala_url" "$indiegala_file /S" "92" "" ""

# Install Rockstar Games Launcher
install_launcher "Rockstar Games Launcher" "RockstarGamesLauncher" "$rockstar_file" "$rockstar_url" "" "93" "" "" true

# Install Glyph Launcher
install_launcher "Glyph Launcher" "GlyphLauncher" "$glyph_file" "$glyph_url" "$glyph_file" "94" "" ""

# Install Playstation Plus Launcher
install_launcher "Playstation Plus" "PlaystationPlusLauncher" "$psplus_file" "$psplus_url" "$psplus_file /q" "96" "" ""

# Install VK Play
install_launcher "VK Play" "VKPlayLauncher" "$vkplay_file" "$vkplay_url" "$vkplay_file" "98" "" "install_vkplay" true

# Install Hoyo Play
install_launcher "HoYoPlay" "HoYoPlayLauncher" "$hoyoplay_file" "$hoyoplay_url" "" "99" "" "install_hoyo" true

# Install Nexon Launcher
install_launcher "Nexon Launcher" "NexonLauncher" "$nexon_file" "$nexon_url" "$nexon_file" "99" "" "install_nexon" true
#End of Launcher Installations



wait
echo "99"
echo "# Checking if Chrome is installed...please wait..."

# Check if user selected any of the options
if [[ $options == *"Netflix"* ]] || [[ $options == *"Fortnite"* ]] || [[ $options == *"Xbox Game Pass"* ]] || [[ $options == *"Geforce Now"* ]] || [[ $options == *"Amazon Luna"* ]] || [[ $options == *"Hulu"* ]] || [[ $options == *"Disney+"* ]] || [[ $options == *"Amazon Prime Video"* ]] || [[ $options == *"Youtube"* ]] || [[ $options == *"Twitch"* ]]; then
    # User selected one of the options
    echo "User selected one of the options"

    # Check if Google Chrome is already installed
    if flatpak list | grep com.google.Chrome &> /dev/null; then
        echo "Google Chrome is already installed"
        flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
    else
        # Check if the Flathub repository exists
        if flatpak remote-list | grep flathub &> /dev/null; then
            echo "Flathub repository exists"
        else
            # Add the Flathub repository
            flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
        fi

        # Install Google Chrome
        flatpak install --user flathub com.google.Chrome -y

        # Run the flatpak --user override command
        flatpak --user override --filesystem=/run/udev:ro com.google.Chrome
    fi
fi





    echo "100"
    echo "# Installation Complete - Steam will now restart. Your launchers will be in your library!...Food for thought...do Jedis use Force Compatability?"
) |
zenity --progress \
  --title="Update Status" \
  --text="Starting update...please wait..." --width=450 --height=350\
  --percentage=0 --auto-close


# Write to env_vars
# Initialize the env_vars file
> ${logged_in_home}/.config/systemd/user/env_vars

write_env_vars() {
    local launcher_path="$1"
    local launcher_name="$2"
    local launcher_dir_name="$3"
    local launcher_args="$4" # Additional parameter for launcher-specific arguments
    local launcher_env_var_name="$5" # Additional parameter for the environment variable name

    local shortcut_directory="\"${launcher_path}\" ${launcher_args}"
    local launch_options="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/${launcher_dir_name}/\" %command%"
    local starting_dir="\"$(dirname "${launcher_path}")\""

    # Write the variables directly to the env_vars file
    echo "export ${launcher_name}shortcutdirectory=${shortcut_directory}" >> "${logged_in_home}/.config/systemd/user/env_vars"
    echo "export ${launcher_name}launchoptions=${launch_options}" >> "${logged_in_home}/.config/systemd/user/env_vars"
    echo "export ${launcher_name}startingdir=${starting_dir}" >> "${logged_in_home}/.config/systemd/user/env_vars"
    echo "export ${launcher_env_var_name}=${launcher_dir_name}" >> "${logged_in_home}/.config/systemd/user/env_vars"

    echo "${launcher_name^} Launcher found at ${launcher_path}"
}

check_and_write() {
    local launcher_name="$1"
    local path1="$2"
    local path2="$3"
    local launcher_dir_name_path1="$4"
    local launcher_dir_name_path2="$5"
    local launcher_args="$6"
    local launcher_env_var_name="$7"

    if [[ -f "$path1" ]]; then
        write_env_vars "$path1" "$launcher_name" "$launcher_dir_name_path1" "$launcher_args" "$launcher_env_var_name"
    elif [[ -f "$path2" ]]; then
        write_env_vars "$path2" "$launcher_name" "$launcher_dir_name_path2" "$launcher_args" "$launcher_env_var_name"
    else
        echo "${launcher_name^} Launcher not found"
    fi
}

# Env_vars Configuration Paths
check_and_write "epic" "$epic_games_launcher_path1" "$epic_games_launcher_path2" "NonSteamLaunchers" "EpicGamesLauncher" "-opengl" "epic_games_launcher"
check_and_write "gog" "$gog_galaxy_path1" "$gog_galaxy_path2" "NonSteamLaunchers" "GogGalaxyLauncher" "" "gog_galaxy_launcher"
check_and_write "uplay" "$uplay_path1" "$uplay_path2" "NonSteamLaunchers" "UplayLauncher" "" "ubisoft_connect_launcher"
check_and_write "battlenet" "$battlenet_path1" "$battlenet_path2" "NonSteamLaunchers" "Battle.netLauncher" "" "bnet_launcher"
check_and_write "eaapp" "$eaapp_path1" "$eaapp_path2" "NonSteamLaunchers" "TheEAappLauncher" "" "ea_app_launcher"
check_and_write "amazon" "$amazongames_path1" "$amazongames_path2" "NonSteamLaunchers" "AmazonGamesLauncher" "" "amazon_launcher"
check_and_write "itchio" "$itchio_path1" "$itchio_path2" "NonSteamLaunchers" "itchioLauncher" "" "itchio_launcher"
check_and_write "legacy" "$legacygames_path1" "$legacygames_path2" "NonSteamLaunchers" "LegacyGamesLauncher" "" "legacy_launcher"
check_and_write "humble" "$humblegames_path1" "$humblegames_path2" "NonSteamLaunchers" "HumbleGamesLauncher" "" "humble_launcher"
check_and_write "indie" "$indiegala_path1" "$indiegala_path2" "NonSteamLaunchers" "IndieGalaLauncher" "" "indie_launcher"
check_and_write "rockstar" "$rockstar_path1" "$rockstar_path2" "NonSteamLaunchers" "RockstarGamesLauncher" "" "rockstar_launcher"
check_and_write "glyph" "$glyph_path1" "$glyph_path2" "NonSteamLaunchers" "GlyphLauncher" "" "glyph_launcher"
check_and_write "psplus" "$psplus_path1" "$psplus_path2" "NonSteamLaunchers" "PlaystationPlusLauncher" "" "psplus_launcher"
check_and_write "vkplay" "$vkplay_path1" "$vkplay_path2" "NonSteamLaunchers" "VKPlayLauncher" "" "vkplay_launcher"
check_and_write "hoyoplay" "$hoyoplay_path1" "$hoyoplay_path2" "NonSteamLaunchers" "HoYoPlayLauncher" "" "hoyoplay_launcher"
check_and_write "nexon" "$nexon_path1" "$nexon_path2" "NonSteamLaunchers" "NexonLauncher" "" "nexon_launcher"

# Special Shortcut for EA App NoRepair
eaapp_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe"
eaapp_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/users/steamuser/Downloads/EAappInstaller.exe"
check_and_write "repaireaapp" "$eaapp_path1" "$eaapp_path2" "NonSteamLaunchers" "TheEAappLauncher" "" "repaireaapp"

# End of writing to env_vars

# Set the env_vars variable
if [ "$use_separate_appids" != true ]; then
    echo "export separate_appids=$use_separate_appids" >> ${logged_in_home}/.config/systemd/user/env_vars
fi




#Other Applications
if [[ $options == *"RemotePlayWhatever"* ]]; then
    # Set the directory path
    DIRECTORY="${logged_in_home}/.local/share/applications"

    # Check if the directory exists
    if [ ! -d "$DIRECTORY" ]; then
        mkdir -p "$DIRECTORY"
    fi

    # Get the latest release URL for RemotePlayWhatever
    RELEASE_URL=$(curl -s https://api.github.com/repos/m4dEngi/RemotePlayWhatever/releases/latest | grep -o 'https://github.com/m4dEngi/RemotePlayWhatever/releases/download/.*RemotePlayWhatever.*\.AppImage')

    # Download the latest RemotePlayWhatever AppImage
    wget -P "$DIRECTORY" "$RELEASE_URL"

    # Get the downloaded file name
    DOWNLOADED_FILE=$(basename "$RELEASE_URL")

    # Rename the downloaded file
    mv "$DIRECTORY/$DOWNLOADED_FILE" "$DIRECTORY/RemotePlayWhatever"

    # Make the file executable
    chmod +x "$DIRECTORY/RemotePlayWhatever"

    echo "RemotePlayWhatever downloaded, renamed to Remote Play Whatever, made executable, created in $DIRECTORY"

    # Create a new .desktop file
    echo "[Desktop Entry]
    Type=Application
    Exec=$DIRECTORY/RemotePlayWhatever \"--appid 0\"
    Name=RemotePlayWhatever
    Icon=$DIRECTORY/RemotePlayWhatever" > "$DIRECTORY/RemotePlayWhatever.desktop"

    # Make the .desktop file executable
    chmod +x "$DIRECTORY/RemotePlayWhatever.desktop"

    steamos-add-to-steam "$DIRECTORY/RemotePlayWhatever.desktop"
    sleep 5
    echo "added RemotePlayWhatever to steamos"
fi



# Set Chrome options based on user's selection

if [[ $options == *"Xbox Game Pass"* ]]; then
    # User selected Xbox Game Pass
    xboxchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.xbox.com/play --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export xboxchromelaunchoptions=$xboxchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Netflix"* ]]; then
    # User selected Netflix
    netflixchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.netflix.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export netflixchromelaunchoptions=$netflixchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"GeForce Now"* ]]; then
    # User selected GeForce Now
    geforcechromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://play.geforcenow.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export geforcechromelaunchoptions=$geforcechromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Hulu"* ]]; then
    # User selected Hulu
    huluchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.hulu.com/welcome --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export huluchromelaunchoptions=$huluchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Disney+"* ]]; then
    # User selected Disney+
    disneychromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.disneyplus.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export disneychromelaunchoptions=$disneychromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Amazon Prime Video"* ]]; then
    # User selected Amazon Prime Video
    amazonchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.amazon.com/primevideo --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export amazonchromelaunchoptions=$amazonchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Youtube"* ]]; then
    # User selected Youtube
    youtubechromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.youtube.com --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export youtubechromelaunchoptions=$youtubechromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Amazon Luna"* ]]; then
    # User selected Amazon Luna
    lunachromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://luna.amazon.com/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export lunachromelaunchoptions=$lunachromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ $options == *"Twitch"* ]]; then
    # User selected Twitch
    twitchchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.twitch.tv/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export twitchchromelaunchoptions=$twitchchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi


if [[ $options == *"Fortnite"* ]]; then
    # User selected Fortnite
    fortnitechromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://www.xbox.com/en-US/play/games/fortnite/BT5P2X999VH2/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export fortnitechromelaunchoptions=$fortnitechromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
fi



# Check if any custom websites were provided
if [ ${#custom_websites[@]} -gt 0 ]; then
    # User entered one or more custom websites

    # Convert the custom_websites array to a string
    custom_websites_str=$(IFS=", "; echo "${custom_websites[*]}")
    echo "export custom_websites_str=$custom_websites_str" >> ${logged_in_home}/.config/systemd/user/env_vars
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

# Check if the loginusers.vdf file exists in either of the two directories
if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]] || [[ -f "${logged_in_home}/.local/share/Steam/config/loginusers.vdf" ]]; then
    if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]]; then
        file_path="${logged_in_home}/.steam/root/config/loginusers.vdf"
    else
        file_path="${logged_in_home}/.local/share/Steam/config/loginusers.vdf"
    fi

    # Extract the block of text for the most recent user
    most_recent_user=$(sed -n '/"users"/,/"MostRecent" "1"/p' "$file_path")

    # Initialize variables
    max_timestamp=0
    current_user=""
    current_steamid=""

    # Process each user block
    # Set IFS to only look for Commas to avoid issues with Whitespace in older account names.
    while IFS="," read steamid account timestamp; do
        if (( timestamp > max_timestamp )); then
            max_timestamp=$timestamp
            current_user=$account
            current_steamid=$steamid
        fi
    # Output our discovered values as comma seperated string to be read into the IDs.
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
        print steamid "," account "," timestamp
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
        # Define backup directory
        backup_dir="$(dirname "$shortcuts_vdf_path")/shortcuts.vdf_backups"
        mkdir -p "$backup_dir"

        # Create backup of shortcuts.vdf file
		cp "$shortcuts_vdf_path" "$backup_dir/shortcuts.vdf.bak_$(date +%m-%d-%Y_%H:%M:%S)"
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
echo "export python_version=$python_version" >> ${logged_in_home}/.config/systemd/user/env_vars
echo "export chromedirectory=$chromedirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
echo "export chrome_startdir=$chrome_startdir" >> ${logged_in_home}/.config/systemd/user/env_vars



# Check if either directory does not exist
if [ "${deckyplugin}" = false ]; then
    # Detach script from Steam process
    nohup sh -c 'sleep 10; /usr/bin/steam %U' &

    # Close all instances of Steam
    steam_pid() { pgrep -x steam ; }
    steam_running=$(steam_pid)
    [[ -n "$steam_running" ]] && killall steam

    # Wait for the steam process to exit
    while steam_pid > /dev/null; do sleep 5; done

	#Setup NSLGameScanner.service
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

	curl -o $python_script_path $github_link

	echo "Starting the service..."

	python3 $python_script_path
fi



# TODO: might be better to relocate temp files to `/tmp` or even use `mktemp -d` since `rm -rf` is potentially dangerous without the `-i` flag
# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf "$download_dir"

echo "Script completed successfully."
exit 0
