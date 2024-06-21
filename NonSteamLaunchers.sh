#!/usr/bin/env bash

set -x              # activate debugging (execution shown)
set -o pipefail     # capture error from pipes
# set -eu           # exit immediately, undefined vars are errors

# ENVIRONMENT VARIABLES
# $USER
[[ -n $(logname >/dev/null 2>&1) ]] && logged_in_user=$(logname) || logged_in_user=$(whoami)

#DBUS
# Add the DBUS_SESSION_BUS_ADDRESS environment variable
dbus_address=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/$(pgrep -u $LOGNAME gnome-session)/environ | cut -d= -f2-)
export DBUS_SESSION_BUS_ADDRESS=$dbus_address

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
version=v3.8.9

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
	folders_to_clone=('requests' 'urllib3' 'steamgrid' 'vdf')

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

# Chrome File Path
# chrome_installpath="/app/bin/chrome"
chrome_path="/usr/bin/flatpak"
chrome_startdir="\"/usr/bin\""
chromedirectory="\"$chrome_path\""

#Zenity Launcher Check Installation
function CheckInstallations {
    declare -A paths1 paths2 names
    paths1=(["epic_games"]="$epic_games_launcher_path1" ["gog_galaxy"]="$gog_galaxy_path1" ["uplay"]="$uplay_path1" ["battlenet"]="$battlenet_path1" ["eaapp"]="$eaapp_path1" ["amazongames"]="$amazongames_path1" ["itchio"]="$itchio_path1" ["legacygames"]="$legacygames_path1" ["humblegames"]="$humblegames_path1" ["indiegala"]="$indiegala_path1" ["rockstar"]="$rockstar_path1" ["glyph"]="$glyph_path1" ["psplus"]="$psplus_path1" ["vkplay"]="$vkplay_path1")
    paths2=(["epic_games"]="$epic_games_launcher_path2" ["gog_galaxy"]="$gog_galaxy_path2" ["uplay"]="$uplay_path2" ["battlenet"]="$battlenet_path2" ["eaapp"]="$eaapp_path2" ["amazongames"]="$amazongames_path2" ["itchio"]="$itchio_path2" ["legacygames"]="$legacygames_path2" ["humblegames"]="$humblegames_path2" ["indiegala"]="$indiegala_path2" ["rockstar"]="$rockstar_path2" ["glyph"]="$glyph_path2" ["psplus"]="$psplus_path2" ["vkplay"]="$vkplay_path2")
    names=(["epic_games"]="Epic Games" ["gog_galaxy"]="GOG Galaxy" ["uplay"]="Ubisoft Connect" ["battlenet"]="Battle.net" ["eaapp"]="EA App" ["amazongames"]="Amazon Games" ["itchio"]="itch.io" ["legacygames"]="Legacy Games" ["humblegames"]="Humble Games Collection" ["indiegala"]="IndieGala" ["rockstar"]="Rockstar Games Launcher" ["glyph"]="Glyph Launcher" ["psplus"]="Playstation Plus" ["vkplay"]="VK Play")

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
    paths=(["nonsteamlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ["epicgameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ["goggalaxylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ["uplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" ["battlenetlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ["eaapplauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ["amazongameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ["itchiolauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" ["legacygameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ["humblegameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ["indiegalalauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ["rockstargameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" ["glyphlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" ["pspluslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" ["vkplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher")
    names=(["nonsteamlauncher"]="NonSteamLaunchers" ["epicgameslauncher"]="EpicGamesLauncher" ["goggalaxylauncher"]="GogGalaxyLauncher" ["uplaylauncher"]="UplayLauncher" ["battlenetlauncher"]="Battle.netLauncher" ["eaapplauncher"]="TheEAappLauncher" ["amazongameslauncher"]="AmazonGamesLauncher" ["itchiolauncher"]="itchioLauncher" ["legacygameslauncher"]="LegacyGamesLauncher" ["humblegameslauncher"]="HumbleGamesLauncher" ["indiegalalauncher"]="IndieGalaLauncher" ["rockstargameslauncher"]="RockstarGamesLauncher" ["glyphlauncher"]="GlyphLauncher" ["pspluslauncher"]="PlaystationPlusLauncher" ["vkplaylauncher"]="VKPlayLauncher")

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
    selected_launchers=$(zenity --list --text="Which launchers do you want to download and install?" --checklist --column="$version" --column="Default = one App ID Installation, One Prefix, NonSteamLaunchers - updated the NSLGameScanner.py $live" FALSE "SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX" $epic_games_value "$epic_games_text" $gog_galaxy_value "$gog_galaxy_text" $uplay_value "$uplay_text" $battlenet_value "$battlenet_text" $amazongames_value "$amazongames_text" $eaapp_value "$eaapp_text" $legacygames_value "$legacygames_text" $itchio_value "$itchio_text" $humblegames_value "$humblegames_text" $indiegala_value "$indiegala_text" $rockstar_value "$rockstar_text" $glyph_value "$glyph_text" $psplus_value "$psplus_text" $vkplay_value "$vkplay_text" FALSE "RemotePlayWhatever" FALSE "Fortnite" FALSE "Xbox Game Pass" FALSE "GeForce Now" FALSE "Amazon Luna" FALSE "Netflix" FALSE "Hulu" FALSE "Disney+" FALSE "Amazon Prime Video" FALSE "movie-web" FALSE "Youtube" FALSE "Twitch" --width=800 --height=740 --extra-button="Uninstall" --extra-button="Stop NSLGameScanner" --extra-button="Start Fresh" --extra-button="Move to SD Card" --extra-button="Update Proton-GE")

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
    folder_names=("EpicGamesLauncher" "GogGalaxyLauncher" "UplayLauncher" "Battle.netLauncher" "TheEAappLauncher" "AmazonGamesLauncher" "itchioLauncher" "LegacyGamesLauncher" "HumbleGamesLauncher" "IndieGalaLauncher" "RockstarGamesLauncher" "GlyphLauncher" "PlaystationPlusLauncher" "VKPlayLauncher")

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
    rm -rf "/run/media/mmcblk0p1/PlaystationPlusLauncher/"
    rm -rf "/run/media/mmcblk0p1/VKPlayLauncher/"
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
        uninstall_launcher "$uninstall_options" "Epic Games" "$epic_games_launcher_path1" "$epic_games_launcher_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" "epic"
        uninstall_launcher "$uninstall_options" "Gog Galaxy" "$gog_galaxy_path1" "$gog_galaxy_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" "gog"
        uninstall_launcher "$uninstall_options" "Uplay" "$uplay_path1" "$uplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" "uplay" "ubisoft"
        uninstall_launcher "$uninstall_options" "Battle.net" "$battlenet_path1" "$battlenet_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" "battle" "bnet"
        uninstall_launcher "$uninstall_options" "EA App" "$eaapp_path1" "$eaapp_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" "eaapp" "ea_app"
        uninstall_launcher "$uninstall_options" "Amazon Games" "$amazongames_path1" "$amazongames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" "amazon"
        uninstall_launcher "$uninstall_options" "Legacy Games" "$legacygames_path1" "$legacygames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" "legacy"
        uninstall_launcher "$uninstall_options" "itch.io" "$itchio_path1" "$itchio_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" "itchio"
        uninstall_launcher "$uninstall_options" "Humble Bundle" "$humblegames_path1" "$humblegames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" "humble"
        uninstall_launcher "$uninstall_options" "IndieGala" "$indiegala_path1" "$indiegala_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" "indie"
        uninstall_launcher "$uninstall_options" "Rockstar Games Launcher" "$rockstar_path1" "$rockstar_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" "rockstar"
        uninstall_launcher "$uninstall_options" "Glyph Launcher" "$glyph_path1" "$glyph_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Glyph" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" "glyph"
        uninstall_launcher "$uninstall_options" "Playstation Plus" "$psplus_path1" "$psplus_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" "psplus"
        uninstall_launcher "$uninstall_options" "VK Play" "$vkplay_path1" "$vkplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" "vkplay"
        return 0
    fi
    # If the uninstall was successful, set uninstalled_any_launcher to true
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
            FALSE "Playstation Plus" \
            FALSE "VK Play" \
        )
        # Convert the returned string to an array
        IFS='|' read -r -a uninstall_options_array <<< "$uninstall_options"
        # Loop through the array and uninstall each selected launcher
        for launcher in "${uninstall_options_array[@]}"; do
            process_uninstall_options "Uninstall $launcher"
        done
        echo "Uninstallation completed successfully."
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

    move_options=$(zenity --list --text="Which launcher IDs do you want to move to the SD card?" --checklist --column="Select" --column="Launcher ID" $nonsteamlauncher_move_value "NonSteamLaunchers" $epicgameslauncher_move_value "EpicGamesLauncher" $goggalaxylauncher_move_value "GogGalaxyLauncher" $uplaylauncher_move_value "UplayLauncher" $battlenetlauncher_move_value "Battle.netLauncher" $eaapplauncher_move_value "TheEAappLauncher" $amazongameslauncher_move_value "AmazonGamesLauncher" $itchiolauncher_move_value "itchioLauncher" $legacygameslauncher_move_value "LegacyGamesLauncher" $humblegameslauncher_move_value "HumbleGamesLauncher" $indiegalalauncher_move_value "IndieGalaLauncher" $rockstargameslauncher_move_value "RockstarGamesLauncher" $glyphlauncher_move_value "GlyphLauncher" $pspluslauncher_move_value "PlaystationPlusLauncher" $vkplaylauncher_move_value "VKPlayLauncher" --width=335 --height=524)

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
    "$STEAM_RUNTIME" "$proton_dir/proton" run MsiExec.exe /i "$msi_file" -opengl /qn
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
    cd "$proton_dir"

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="${logged_in_home}/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${appid}"

    # Download BATTLE file if not already present
    if [ ! -f "$battle_file" ]; then
        echo "Downloading BATTLE file"
        wget "$battle_url" -O "$battle_file"
    fi

    # Run the BATTLE file using Proton with the /passive option
    echo "Running BATTLE file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net"

    # Wait for the process to finish or timeout after a certain number of attempts
    max_attempts=20
    attempt=0
    while true; do
        if pgrep -f "Battle.net.exe" > /dev/null || pgrep -f "BlizzardError.exe" > /dev/null; then
            pkill -f "Battle.net.exe" || pkill -f "BlizzardError.exe"
            sleep 5
            ((attempt++))
            if [ "$attempt" -ge "$max_attempts" ]; then
                echo "Timeout: Battle.net process did not terminate."
                break
            fi
        else
            break
        fi
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

    # Cancel & Exit the Amazon Games Setup Wizard
    end=$((SECONDS+60))  # Timeout after 60 seconds
    while true; do
        if pgrep -f "Amazon Games.exe" > /dev/null; then
            pkill -f "Amazon Games.exe"
            break
        fi
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while trying to kill Amazon Games.exe"
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
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$eaapp_file" /quiet &
    end=$((SECONDS+60))
    while true; do
        if pgrep -f "EADesktop.exe" > /dev/null; then
            pkill -f "EADesktop.exe"
            break
        fi
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while trying to kill EADesktop.exe"
            break
        fi
        sleep 1
    done

    # Wait for the EA App file to finish running
    echo "Attempting to kill EAappInstaller.exe"
    end=$((SECONDS+10))
    while true; do
        if pgrep -f "EAappInstaller.exe" > /dev/null; then
            pkill -f "EAappInstaller.exe"
            break
        fi
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while trying to kill EAappInstaller.exe"
            break
        fi
        sleep 1
    done
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
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$itchio_file" --silent
    end=$((SECONDS+60))
    while true; do
        if pgrep -f "itch.exe" > /dev/null; then
            pkill -f "itch.exe"
            break
        fi
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while trying to kill itch.exe"
            break
        fi
        sleep 1
    done

    # Wait for the itch file to finish running
    wait
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
        echo "Downloading Rockstar file"
        wget $rockstar_url -O $rockstar_file
    fi

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
if [[ $options == *"Netflix"* ]] || [[ $options == *"Fortnite"* ]] || [[ $options == *"Xbox Game Pass"* ]] || [[ $options == *"Geforce Now"* ]] || [[ $options == *"Amazon Luna"* ]] || [[ $options == *"Hulu"* ]] || [[ $options == *"Disney+"* ]] || [[ $options == *"Amazon Prime Video"* ]] || [[ $options == *"Youtube"* ]] || [[ $options == *"Twitch"* ]] || [[ $options == *"movie-web"* ]]; then
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


# wait for Google Chrome to finish
wait


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
    echo "export epicshortcutdirectory=$epicshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epiclaunchoptions=$epiclaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epicstartingdir=$epicstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epic_games_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Epic Games Launcher found at path 1"
elif [[ -f "$epic_games_launcher_path2" ]]; then
    # Epic Games Launcher is installed at path 2
    epicshortcutdirectory="\"$epic_games_launcher_path2\""
    epiclaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/\" %command%"
    epicstartingdir="\"$(dirname "$epic_games_launcher_path2")\""
    echo "export epicshortcutdirectory=$epicshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epiclaunchoptions=$epiclaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epicstartingdir=$epicstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export epic_games_launcher=EpicGamesLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Epic Games Launcher found at path 2"
fi


if [[ -f "$gog_galaxy_path1" ]]; then
    # Gog Galaxy Launcher is installed at path 1
    gogshortcutdirectory="\"$gog_galaxy_path1\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    gogstartingdir="\"$(dirname "$gog_galaxy_path1")\""
    echo "export gogshortcutdirectory=$gogshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export goglaunchoptions=$goglaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export gogstartingdir=$gogstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export gog_galaxy_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Gog Galaxy Launcher found at path 1"
elif [[ -f "$gog_galaxy_path2" ]]; then
    # Gog Galaxy Launcher is installed at path 2
    gogshortcutdirectory="\"$gog_galaxy_path2\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/\" %command%"
    gogstartingdir="\"$(dirname "$gog_galaxy_path2")\""
    echo "export gogshortcutdirectory=$gogshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export goglaunchoptions=$goglaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export gogstartingdir=$gogstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export gog_galaxy_launcher=GogGalaxyLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Gog Galaxy Launcher found at path 2"
fi


if [[ -f "$uplay_path1" ]]; then
    # Uplay Launcher is installed at path 1
    uplayshortcutdirectory="\"$uplay_path1\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    uplaystartingdir="\"$(dirname "$uplay_path1")\""
    echo "export uplayshortcutdirectory=$uplayshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export uplaylaunchoptions=$uplaylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export uplaystartingdir=$uplaystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export ubisoft_connect_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Ubisoft Connect Launcher found at path 1"
elif [[ -f "$uplay_path2" ]]; then
    # Uplay Launcher is installed at path 2
    uplayshortcutdirectory="\"$uplay_path2\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher/\" %command%"
    uplaystartingdir="\"$(dirname "$uplay_path2")\""
    echo "export uplayshortcutdirectory=$uplayshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export uplaylaunchoptions=$uplaylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export uplaystartingdir=$uplaystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export ubisoft_connect_launcher=UplayLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Ubisoft Connect Launcher found at path 1"
fi

if [[ -f "$battlenet_path1" ]]; then
    # Battlenet Launcher is installed at path 1
    battlenetshortcutdirectory="\"$battlenet_path1\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    battlenetstartingdir="\"$(dirname "$battlenet_path1")\""
    echo "export battlenetshortcutdirectory=$battlenetshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export battlenetlaunchoptions=$battlenetlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export battlenetstartingdir=$battlenetstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export bnet_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Battlenet Launcher found at path 1"
elif [[ -f "$battlenet_path2" ]]; then
    # Battlenet Launcher is installed at path 2
    battlenetshortcutdirectory="\"$battlenet_path2\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/\" %command%"
    battlenetstartingdir="\"$(dirname "$battlenet_path2")\""
    echo "export battlenetshortcutdirectory=$battlenetshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export battlenetlaunchoptions=$battlenetlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export battlenetstartingdir=$battlenetstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export bnet_launcher=Battle.netLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Battlenet Launcher found at path 2"
fi

if [[ -f "$eaapp_path1" ]]; then
    # EA App Launcher is installed at path 1
    eaappshortcutdirectory="\"$eaapp_path1\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    eaappstartingdir="\"$(dirname "$eaapp_path1")\""
    echo "export eaappshortcutdirectory=$eaappshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export eaapplaunchoptions=$eaapplaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export eaappstartingdir=$eaappstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
	echo "export ea_app_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "EA App Launcher found at path 1"
elif [[ -f "$eaapp_path2" ]]; then
    # EA App Launcher is installed at path 2
    eaappshortcutdirectory="\"$eaapp_path2\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/\" %command%"
    eaappstartingdir="\"$(dirname "$eaapp_path2")\""
    echo "export eaappshortcutdirectory=$eaappshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export eaapplaunchoptions=$eaapplaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export eaappstartingdir=$eaappstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
	echo "export ea_app_launcher=TheEAappLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "EA App Launcher found at path 2"
fi

if [[ -f "$amazongames_path1" ]]; then
    # Amazon Games Launcher is installed at path 1
    amazonshortcutdirectory="\"$amazongames_path1\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    amazonstartingdir="\"$(dirname "$amazongames_path1")\""
    echo "export amazonshortcutdirectory=$amazonshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazonlaunchoptions=$amazonlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazonstartingdir=$amazonstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazon_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Amazon Games Launcher found at path 1"
elif [[ -f "$amazongames_path2" ]]; then
    # Amazon Games Launcher is installed at path 2
    amazonshortcutdirectory="\"$amazongames_path2\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/\" %command%"
    amazonstartingdir="\"$(dirname "$amazongames_path2")\""
    echo "export amazonshortcutdirectory=$amazonshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazonlaunchoptions=$amazonlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazonstartingdir=$amazonstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export amazon_launcher=AmazonGamesLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "Amazon Games Launcher found at path 2"
fi

if [[ -f "$itchio_path1" ]]; then
    # itchio Launcher is installed at path 1
    itchioshortcutdirectory="\"$itchio_path1\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    itchiostartingdir="\"$(dirname "$itchio_path1")\""
    echo "export itchioshortcutdirectory=$itchioshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchiolaunchoptions=$itchiolaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchiostartingdir=$itchiostartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchio_launcher=NonSteamLaunchers" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "itchio Launcher found at path 1"
elif [[ -f "$itchio_path2" ]]; then
    # itchio Launcher is installed at path 2
    itchioshortcutdirectory="\"$itchio_path2\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher/\" %command%"
    itchiostartingdir="\"$(dirname "$itchio_path2")\""
    echo "export itchioshortcutdirectory=$itchioshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchiolaunchoptions=$itchiolaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchiostartingdir=$itchiostartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export itchio_launcher=itchioLauncher" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "itchio Launcher found at path 2"
fi

if [[ -f "$legacygames_path1" ]]; then
    # Legacy Games Launcher is installed at path 1
    legacyshortcutdirectory="\"$legacygames_path1\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    legacystartingdir="\"$(dirname "$legacygames_path1")\""
    echo "export legacyshortcutdirectory=$legacyshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export legacylaunchoptions=$legacylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export legacystartingdir=$legacystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$legacygames_path2" ]]; then
    # Legacy Games Launcher is installed at path 2
    legacyshortcutdirectory="\"$legacygames_path2\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/\" %command%"
    legacystartingdir="\"$(dirname "$legacygames_path2")\""
    echo "export legacyshortcutdirectory=$legacyshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export legacylaunchoptions=$legacylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export legacystartingdir=$legacystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ -f "$humblegames_path1" ]]; then
    # Humble Games Launcher is installed at path 1
    humbleshortcutdirectory="\"$humblegames_path1\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    humblestartingdir="\"$(dirname "$humblegames_path1")\""
    echo "export humbleshortcutdirectory=$humbleshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export humblelaunchoptions=$humblelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export humblestartingdir=$humblestartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$humblegames_path2" ]]; then
    # Humble Games Launcher is installed at path 2
    humbleshortcutdirectory="\"$humblegames_path2\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/\" %command%"
    humblestartingdir="\"$(dirname "$humblegames_path2")\""
    echo "export humbleshortcutdirectory=$humbleshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export humblelaunchoptions=$humblelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export humblestartingdir=$humblestartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ -f "$indiegala_path1" ]]; then
    # indiegala Launcher is installed at path 1
    indieshortcutdirectory="\"$indiegala_path1\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    indiestartingdir="\"$(dirname "$indiegala_path1")\""
    echo "export indieshortcutdirectory=$indieshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export indielaunchoptions=$indielaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export indiestartingdir=$indiestartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$indiegala_path2" ]]; then
    # indiegala Launcher is installed at path 2
    indieshortcutdirectory="\"$indiegala_path2\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/\" %command%"
    indiestartingdir="\"$(dirname "$indiegala_path2")\""
    echo "export indieshortcutdirectory=$indieshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export indielaunchoptions=$indielaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export indiestartingdir=$indiestartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ -f "$rockstar_path1" ]]; then
    # rockstar Launcher is installed at path 1
    rockstarshortcutdirectory="\"$rockstar_path1\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    rockstarstartingdir="\"$(dirname "$rockstar_path1")\""
    echo "export rockstarshortcutdirectory=$rockstarshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export rockstarlaunchoptions=$rockstarlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export rockstarstartingdir=$rockstarstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$rockstar_path2" ]]; then
    # rockstar Launcher is installed at path 2
    rockstarshortcutdirectory="\"$rockstar_path2\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/\" %command%"
    rockstarstartingdir="\"$(dirname "$rockstar_path2")\""
    echo "export rockstarshortcutdirectory=$rockstarshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export rockstarlaunchoptions=$rockstarlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export rockstarstartingdir=$rockstarstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ -f "$glyph_path1" ]]; then
    # Glyph is installed at path 1
    glyphshortcutdirectory="\"$glyph_path1\""
    glyphlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    glyphstartingdir="\"$(dirname "$glyph_path1")\""
    echo "export glyphshortcutdirectory=$glyphshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export glyphlaunchoptions=$glyphlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export glyphstartingdir=$glyphstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$glyph_path2" ]]; then
    # Glyph is installed at path 2
    glyphshortcutdirectory="\"$glyph_path2\""
    glyphlaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher/\" %command%"
    glyphstartingdir="\"$(dirname "$glyph_path2")\""
    echo "export glyphshortcutdirectory=$glyphshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export glyphlaunchoptions=$glyphlaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export glyphstartingdir=$glyphstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi


if [[ -f "$psplus_path1" ]]; then
    # Playstation is installed at path 1
    psplusshortcutdirectory="\"$psplus_path1\""
    pspluslaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    psplusstartingdir="\"$(dirname "$psplus_path1")\""
    echo "export psplusshortcutdirectory=$psplusshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export pspluslaunchoptions=$pspluslaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export psplusstartingdir=$psplusstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$psplus_path2" ]]; then
    # Playstation is installed at path 2
    psplusshortcutdirectory="\"$psplus_path2\""
    pspluslaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/\" %command%"
    psplusstartingdir="\"$(dirname "$psplus_path2")\""
    echo "export psplusshortcutdirectory=$psplusshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export pspluslaunchoptions=$pspluslaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export psplusstartingdir=$psplusstartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
fi

if [[ -f "$vkplay_path1" ]]; then
    # VK Play is installed at path 1
    vkplayshortcutdirectory="\"$vkplay_path1\""
    vkplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
    vkplaystartingdir="\"$(dirname "$vkplay_path1")\""
    echo "export vkplayshortcutdirectory=$vkplayshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export vkplaylaunchoptions=$vkplaylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export vkplaystartingdir=$vkplaystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
elif [[ -f "$vkplay_path2" ]]; then
    # VK Play is installed at path 2
    vkplayshortcutdirectory="\"$vkplay_path2\""
    vkplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/\" %command%"
    vkplaystartingdir="\"$(dirname "$vkplay_path2")\""
    echo "export vkplayshortcutdirectory=$vkplayshortcutdirectory" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export vkplaylaunchoptions=$vkplaylaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
    echo "export vkplaystartingdir=$vkplaystartingdir" >> ${logged_in_home}/.config/systemd/user/env_vars
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
    wait
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

if [[ $options == *"movie-web"* ]]; then
    # User selected movie-web
    moviewebchromelaunchoptions="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --kiosk https://sudo-flix.lol/ --chrome-kiosk-type=fullscreen --no-first-run --enable-features=OverlayScrollbar"
    echo "export moviewebchromelaunchoptions=$moviewebchromelaunchoptions" >> ${logged_in_home}/.config/systemd/user/env_vars
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
if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]] || [[ -f "/home/deck/.local/share/Steam/config/loginusers.vdf" ]]; then
    if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]]; then
        file_path="${logged_in_home}/.steam/root/config/loginusers.vdf"
    else
        file_path="/home/deck/.local/share/Steam/config/loginusers.vdf"
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





# Define backup directory
backup_dir="$userdata_folder/shortcuts.vdf_backups"
mkdir -p "$backup_dir"

# Check if userdata folder was found
if [[ -n "$userdata_folder" ]]; then
    # Userdata folder was found
    echo "Current user's userdata folder found at: $userdata_folder"

    # Find shortcuts.vdf file for current user
    shortcuts_vdf_path=$(find "$userdata_folder" -type f -name shortcuts.vdf)

    # Check if shortcuts_vdf_path is not empty
    if [[ -n "$shortcuts_vdf_path" ]]; then
        # Create backup of shortcuts.vdf file
        cp "$shortcuts_vdf_path" "$backup_dir/shortcuts_vdf.bak_$(date +%Y%m%d_%H%M%S)"
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
    nohup sh -c 'sleep 10; /usr/bin/steam' &

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
