#!/usr/bin/env bash

set -x              # activate debugging (execution shown)
set -o pipefail     # capture error from pipes

# ENVIRONMENT VARIABLES
# $USER
logged_in_user=$(logname 2>/dev/null || whoami)

# DBUS
# Add the DBUS_SESSION_BUS_ADDRESS environment variable
if [[ -z "$DBUS_SESSION_BUS_ADDRESS" ]]; then
  eval $(dbus-launch --sh-syntax)
  export DBUS_SESSION_BUS_ADDRESS
fi


if ! zenity --notification --text="NonSteamLaunchers is running tests..." >/dev/null 2>&1; then
    # If Zenity fails, fallback
    export GSK_RENDERER=cairo
    export GDK_BACKEND=x11
    export LIBGL_ALWAYS_SOFTWARE=1
fi

export LD_LIBRARY_PATH=$(pwd)

# $UID
logged_in_uid=$(id -u "${logged_in_user}")

# $HOME
logged_in_home=$(eval echo "~${logged_in_user}")

# Log
download_dir=$(eval echo ~$user)/Downloads/NonSteamLaunchersInstallation
log_file=$(eval echo ~$user)/Downloads/NonSteamLaunchers-install.log



#Cleaning
# Define the path to the compatdata directory
compatdata_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata"

# Define the NonSteamLaunchers directory path for cleaning .tmp files
non_steam_launchers_dir="${compatdata_dir}/NonSteamLaunchers/pfx/drive_c/"

# Define an array of folder names
folder_names=("NonSteamLaunchers" "EpicGamesLauncher" "GogGalaxyLauncher" "UplayLauncher" "Battle.netLauncher" "TheEAappLauncher" "AmazonGamesLauncher" "itchioLauncher" "LegacyGamesLauncher" "HumbleGamesLauncher" "IndieGalaLauncher" "RockstarGamesLauncher" "GlyphLauncher" "PlaystationPlusLauncher" "VKPlayLauncher" "HoYoPlayLauncher" "NexonLauncher" "GameJoltLauncher" "ArtixGameLauncher" "ARCLauncher" "PokeTCGLauncher" "AntstreamLauncher" "PURPLELauncher" "PlariumLauncher" "VFUNLauncher" "TempoLauncher")

# Cleaning up empty directories in compatdata (maxdepth 1 to avoid subdirectories)
echo "Cleaning up empty directories in $compatdata_dir..."
find "${compatdata_dir}" -maxdepth 1 -type d -empty -delete
echo "Empty directories cleaned up."

# Cleaning up .tmp files in the NonSteamLaunchers directory
echo "Cleaning up .tmp files in $non_steam_launchers_dir..."
find "${non_steam_launchers_dir}" -maxdepth 1 -type f -name "*.tmp" -delete
echo ".tmp files cleaned up."

# Loop through each folder name for symlink checking and deletion
for folder in "${folder_names[@]}"; do
  SYMLINK="$compatdata_dir/$folder"

  # Check if it's a symlink and if the target is broken
  if [ -L "$SYMLINK" ] && [ ! -e "$(readlink "$SYMLINK")" ]; then
    echo "The symlink $SYMLINK is broken. Deleting it..."

    # Delete the broken symlink
    rm "$SYMLINK"
    echo "Symlink $SYMLINK deleted successfully."
  else
    echo "The symlink $SYMLINK is either not a symlink or not broken. No action taken."
  fi

  # Check if the folder exists and clean up any .tmp files in it if applicable
  TARGET_DIR="$compatdata_dir/$folder/pfx/drive_c/"
  if [ -d "$TARGET_DIR" ]; then
    echo "Cleaning up .tmp files in $TARGET_DIR..."
    find "$TARGET_DIR" -maxdepth 1 -type f -name "*.tmp" -delete
    echo ".tmp files cleaned up in $TARGET_DIR."
  else
    echo "No valid directory found for $folder at $TARGET_DIR. No .tmp cleanup needed."
  fi
done

echo "Cleanup completed!"




# Remove existing log file if it exists
if [[ -f $log_file ]]; then
  rm $log_file
fi

# Redirect all output to the log file
exec > >(tee -a "$log_file") 2>&1

# Version number (major.minor)
version=v4.1.8
#NSL Decky Plugin Latest Github Version
deckyversion=$(curl -s https://raw.githubusercontent.com/moraroy/NonSteamLaunchersDecky/refs/heads/main/package.json | grep -o '"version": "[^"]*' | sed 's/"version": "//')




# Function to display a Zenity message
show_message() {
  zenity --notification --text="$1" --timeout=1
}



# Check repo releases via GitHub API then display current stable version
check_for_updates() {
    local api_url="https://api.github.com/repos/moraroy/NonSteamLaunchers-On-Steam-Deck/releases/latest"
    local latest_version=$(curl -s "$api_url" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ "$version" != "$latest_version" ]; then
        zenity --info --text="A new version is available: $latest_version\nPlease download it from GitHub." --width=200 --height=100 --timeout=5
    else
        echo "You are already running the latest version: $version"
    fi
}

# Check if Zenity is installed
if ! command -v zenity &> /dev/null; then
    echo "Zenity is not installed. Installing Zenity..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y zenity
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y zenity
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm zenity
    else
        echo "Unknown package manager. Please install Zenity manually."
        exit 1
    fi
fi

# Check if Steam is installed (non-flatpak)
if ! command -v steam &> /dev/null; then
    echo "Steam is not installed. Please install the non-flatpak version of Steam."
    # Provide instructions for different package managers:
    if command -v apt-get &> /dev/null; then
        echo "To install Steam on a Debian-based system (e.g., Ubuntu, Pop!_OS), run:"
        echo "  sudo apt update && sudo apt install steam"
    elif command -v dnf &> /dev/null; then
        echo "To install Steam on a Fedora-based system, run:"
        echo "  sudo dnf install steam"
    elif command -v pacman &> /dev/null; then
        echo "To install Steam on an Arch-based system (e.g., ChimeraOS), run:"
        echo "  sudo pacman -S steam"
    else
        echo "Unknown package manager. Please install Steam manually."
        exit 1
    fi
fi

# Check if wget is installed
if ! command -v wget &> /dev/null; then
    echo "wget is not installed. Installing wget..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y wget
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y wget
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm wget
    else
        echo "Unknown package manager. Please install wget manually."
        exit 1
    fi
fi

# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "curl is not installed. Installing curl..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y curl
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y curl
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm curl
    else
        echo "Unknown package manager. Please install curl manually."
        exit 1
    fi
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Installing jq..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get install -y jq
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y jq
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm jq
    else
        echo "Unknown package manager. Please install jq manually."
        exit 1
    fi
fi

# Get the command line arguments
args=("$@")
echo "Arguments passed: ${args[@]}"  # Debugging the passed arguments
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







# --------------------------
# First Run: VARIABLE SETUP
# --------------------------

# Function to extract steamid3 from Steam config
get_steam_user_info() {
    if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]] || [[ -f "${logged_in_home}/.local/share/Steam/config/loginusers.vdf" ]]; then
        if [[ -f "${logged_in_home}/.steam/root/config/loginusers.vdf" ]]; then
            file_path="${logged_in_home}/.steam/root/config/loginusers.vdf"
        else
            file_path="${logged_in_home}/.local/share/Steam/config/loginusers.vdf"
        fi

        most_recent_user=$(sed -n '/"users"/,/"MostRecent" "1"/p' "$file_path")

        max_timestamp=0
        current_user=""
        current_steamid=""

        while IFS="," read steamid account timestamp; do
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
            print steamid "," account "," timestamp
        }')

        steamid3=$((current_steamid - 76561197960265728))
        echo "$steamid3"
    else
        return 0  # Graceful return if file not found
    fi
}

# Suppress all Steam ID output temporarily
{
    set +x
    steamid3=$(get_steam_user_info | tail -n1)
    set -x
} 2>/dev/null

# Get Proton compatibility tool name or fall back
proton_dir=$(find -L "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
if [[ -n "$proton_dir" ]]; then
    compat_tool_name=$(basename "$proton_dir")
else
    compat_tool_name="Proton Experimental"
fi

# Get Python version
python_version=$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null)

# Just check if Chrome is installed via Flatpak — don't use its path
if flatpak list --app | grep -q com.google.Chrome; then
    echo "Google Chrome is installed via Flatpak."
else
    echo "Google Chrome is not installed via Flatpak."
fi

# Always assign these for Steam shortcut compatibility
chromedirectory="/usr/bin/flatpak"
chrome_startdir="/usr/bin"

# Write to env_vars
env_file="${logged_in_home}/.config/systemd/user/env_vars"
mkdir -p "$(dirname "$env_file")"

# Declare vars to check and write
declare -A vars_to_set
[[ -n "$steamid3" ]] && vars_to_set["steamid3"]="$steamid3"
vars_to_set["logged_in_home"]="$logged_in_home"
vars_to_set["compat_tool_name"]="$compat_tool_name"
[[ -n "$python_version" ]] && vars_to_set["python_version"]="$python_version"
vars_to_set["chromedirectory"]="$chromedirectory"
vars_to_set["chrome_startdir"]="$chrome_startdir"

# If file is missing or empty, write everything at once
if [[ ! -s "$env_file" ]]; then
    {
        for key in "${!vars_to_set[@]}"; do
            echo "export $key=\"${vars_to_set[$key]}\""
        done
    } > "$env_file"
    echo "Environment variables written to $env_file (new or empty file)."
else
    # File exists with content: append only missing exports
    for key in "${!vars_to_set[@]}"; do
        if ! grep -qE "^export $key=" "$env_file"; then
            echo "export $key=\"${vars_to_set[$key]}\"" >> "$env_file"
            echo "Added: export $key=\"${vars_to_set[$key]}\""
        fi
    done
    echo "Environment variables updated in $env_file (if needed)."
fi
#End of First Run Env_vars




if [ "${deckyplugin}" = false ]; then
	# Download Modules
	repo_url='https://github.com/moraroy/NonSteamLaunchers-On-Steam-Deck/archive/refs/heads/main.zip'
	folders_to_clone=('requests' 'urllib3' 'steamgrid' 'vdf' 'charset_normalizer')

	logged_in_home=$(eval echo ~$user)
	parent_folder="${logged_in_home}/.config/systemd/user/Modules"
	mkdir -p "${parent_folder}"

	folders_exist=true
	for folder in "${folders_to_clone[@]}"; do
	  if [ ! -d "${parent_folder}/${folder}" ]; then
	    folders_exist=false
	    break
	  fi
	done

	if [ "${folders_exist}" = false ]; then
	  zip_file_path="${parent_folder}/repo.zip"
	  wget -O "${zip_file_path}" "${repo_url}" || { echo 'Download failed with error code: $?'; exit 1; }
	  unzip -d "${parent_folder}" "${zip_file_path}" || { echo 'Unzip failed with error code: $?'; exit 1; }

	  for folder in "${folders_to_clone[@]}"; do
	    destination_path="${parent_folder}/${folder}"
	    source_path="${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main/Modules/${folder}"
	    if [ ! -d "${destination_path}" ]; then
	      mv "${source_path}" "${destination_path}" || { echo 'Move failed with error code: $?'; exit 1; }
	    fi
	  done

	  rm "${zip_file_path}"
	  rm -r "${parent_folder}/NonSteamLaunchers-On-Steam-Deck-main"
	fi

	# Service File rough update
	rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py
	rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service
	unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service
	systemctl --user daemon-reload

	python_script_path="${logged_in_home}/.config/systemd/user/NSLGameScanner.py"
	github_link="https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/NSLGameScanner.py"
	curl -o $python_script_path $github_link

	env_vars="${logged_in_home}/.config/systemd/user/env_vars"

	if [ -f "$env_vars" ]; then
	    echo "env_vars file found. Running the .py file."
	    live="and is LIVE. Latest NSL Decky Plugin Version on Github: $deckyversion"
	else
	    echo "env_vars file not found. Not Running the .py file."
	    live="and is not LIVE. Latest NSL Decky Plugin Version on Github: $deckyversion"
	fi

	decky_plugin=false
	for arg in "${args[@]}"; do
	  if [ "$arg" = "Decky Plugin" ]; then
	    decky_plugin=true
	    break
	  fi
	done

	funny_messages=(
	  "Wow, you have a lot of games!"
	  "Getting artwork and descriptions for note system..."
	  "So many launchers, so little time..."
	  "Much game. Very library. Wow."
	  "Looking under the Steam Deck couch cushions..."
	  "Injecting metadata directly into your eyeballs..."
	  "Downloading more RAM... just kidding."
	  "Scanning your games like a barcode at checkout!"
	  "Adding +10 charm to your launcher list..."
	  "Man this is taking a long time..."
	  "Removing NSL from Decky Loader Store... jk that happend in real life."
	  "Learning your game choices and judging you for them..."
	  "But why is that game in here!!??"
	  "Downloading any boot videos for your enjoyment..."
	  "Thank you for being patient..."
	  "This may take a while..."
	  "You may need to grab a coffee..."
	)

	if [ "$decky_plugin" = true ]; then
	    if [ -f "$env_vars" ]; then
	        echo "Decky Plugin argument set and env_vars file found. Running the .py file..."

	        start_msg="${funny_messages[$RANDOM % ${#funny_messages[@]}]}"
	        show_message "Starting Scanner... looking for any games..."

	        (
	          while true; do
	            sleep 15
	            loop_msg="${funny_messages[$RANDOM % ${#funny_messages[@]}]}"
	            show_message "Still scanning... ${loop_msg}"
	          done
	        ) &
	        message_pid=$!

	        python3 $python_script_path

	        kill $message_pid
	        show_message "Scanning complete! Your game library looks good!"

	        echo "Python script ran. Continuing with the script..."
	    else
	        echo "Decky Plugin argument set but env_vars file not found. Exiting the script."
	        exit 0
	    fi
	else
	    echo "Decky Plugin argument not set. Continuing with the script..."

	    start_msg="${funny_messages[$RANDOM % ${#funny_messages[@]}]}"
	    show_message "Starting Scanner... looking for any games..."

	    (
	      while true; do
	        sleep 15
	        loop_msg="${funny_messages[$RANDOM % ${#funny_messages[@]}]}"
	        show_message "Still scanning... ${loop_msg}"
	      done
	    ) &
	    message_pid=$!

	    python3 $python_script_path

	    kill $message_pid
        show_message "Scanning complete! Your game library looks good!"
	    sleep 2
	    echo "env_vars file found. Running the .py file."
	    live="successfully. Decky Plugin Version on Github is: $deckyversion"
	fi

	nsl_config_dir="${logged_in_home}/.var/app/com.github.mtkennerly.ludusavi/config/ludusavi/NSLconfig"

	if [ -d "$nsl_config_dir" ]; then
	    if flatpak list --app | grep -q "com.github.mtkennerly.ludusavi"; then
	        echo "Running backup..."
	        nohup flatpak run com.github.mtkennerly.ludusavi --config "$nsl_config_dir" backup --force > /dev/null 2>&1 &
	        wait $!
	        echo "Backup completed"
	        show_message "Game Saves have been backed up! Please check here: /home/deck/NSLGameSaves"
	        sleep 2
	    else
	        echo "Flatpak com.github.mtkennerly.ludusavi not found. Skipping backup."
	    fi
	else
	    echo "Config directory $nsl_config_dir does not exist. Skipping backup."
	fi
fi
sleep 1
show_message "Finished! Welcome to NonSteamLaunchers!"



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
minecraft_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
minecraft_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher/pfx/drive_c/Program Files (x86)/Minecraft Launcher/MinecraftLauncher.exe"
psplus_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
psplus_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/pfx/drive_c/Program Files (x86)/PlayStationPlus/pspluslauncher.exe"
vkplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"
vkplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/pfx/drive_c/users/steamuser/AppData/Local/GameCenter/GameCenter.exe"
hoyoplay_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/HoYoPlay/launcher.exe"
hoyoplay_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher/pfx/drive_c/Program Files/HoYoPlay/launcher.exe"
nexon_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Nexon/Nexon Launcher/nexon_launcher.exe"
nexon_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher/pfx/drive_c/Program Files (x86)/Nexon/Nexon Launcher/nexon_launcher.exe"
gamejolt_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameJoltClient/GameJoltClient.exe"
gamejolt_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GameJoltLauncher/pfx/drive_c/users/steamuser/AppData/Local/GameJoltClient/GameJoltClient.exe"
artixgame_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Artix Game Launcher/Artix Game Launcher.exe"
artixgame_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/ArtixGameLauncher/pfx/drive_c/Program Files/Artix Game Launcher/Artix Game Launcher.exe"
arc_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Arc/Arc.exe"
arc_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/ARCLauncher/pfx/drive_c/Program Files (x86)/Arc/Arc.exe"
poketcg_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/The Pokémon Company International/Pokémon Trading Card Game Live/Pokemon TCG Live.exe"
poketcg_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PokeTCGLauncher/pfx/drive_c/users/steamuser/The Pokémon Company International/Pokémon Trading Card Game Live/Pokemon TCG Live.exe"
antstream_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd/Antstream/AntstreamArcade.exe"
antstream_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AntstreamLauncher/pfx/drive_c/Program Files (x86)/Antstream Ltd/Antstream/AntstreamArcade.exe"
purple_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/NCSOFT/Purple/PurpleLauncher.exe"
purple_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PURPLELauncher/pfx/drive_c/Program Files (x86)/NCSOFT/Purple/PurpleLauncher.exe"
plarium_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay/PlariumPlay.exe"
plarium_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay/PlariumPlay.exe"

vfun_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/VFUN/VLauncher/VFUNLauncher.exe"
vfun_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VFUNLauncher/pfx/drive_c/VFUN/VLauncher/VFUNLauncher.exe"
tempo_path1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Tempo Launcher - Beta/Tempo Launcher - Beta.exe"
tempo_path2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TempoLauncher/pfx/drive_c/Program Files/Tempo Launcher - Beta/Tempo Launcher - Beta.exe"






# Chrome File Path
# chrome_installpath="/app/bin/chrome"
chrome_path="/usr/bin/flatpak"
chrome_startdir="\"/usr/bin\""
chromedirectory="\"$chrome_path\""

#Zenity Launcher Check Installation
function CheckInstallations {
    declare -A paths1 paths2 names
    paths1=(["epic_games"]="$epic_games_launcher_path1" ["gog_galaxy"]="$gog_galaxy_path1" ["uplay"]="$uplay_path1" ["battlenet"]="$battlenet_path1" ["eaapp"]="$eaapp_path1" ["amazongames"]="$amazongames_path1" ["itchio"]="$itchio_path1" ["legacygames"]="$legacygames_path1" ["humblegames"]="$humblegames_path1" ["indiegala"]="$indiegala_path1" ["rockstar"]="$rockstar_path1" ["glyph"]="$glyph_path1" ["minecraft"]="$minecraft_path1" ["psplus"]="$psplus_path1" ["vkplay"]="$vkplay_path1" ["hoyoplay"]="$hoyoplay_path1" ["nexon"]="$nexon_path1" ["gamejolt"]="$gamejolt_path1" ["artixgame"]="$artixgame_path1" ["arc"]="$arc_path1" ["poketcg"]="$poketcg_path1" ["antstream"]="$antstream_path1" ["purple"]="$purple_path1" ["plarium"]="$plarium_path1" ["vfun"]="$vfun_path1" ["tempo"]="$tempo_path1")

    paths2=(["epic_games"]="$epic_games_launcher_path2" ["gog_galaxy"]="$gog_galaxy_path2" ["uplay"]="$uplay_path2" ["battlenet"]="$battlenet_path2" ["eaapp"]="$eaapp_path2" ["amazongames"]="$amazongames_path2" ["itchio"]="$itchio_path2" ["legacygames"]="$legacygames_path2" ["humblegames"]="$humblegames_path2" ["indiegala"]="$indiegala_path2" ["rockstar"]="$rockstar_path2" ["glyph"]="$glyph_path2" ["minecraft"]="$minecraft_path2" ["psplus"]="$psplus_path2" ["vkplay"]="$vkplay_path2" ["hoyoplay"]="$hoyoplay_path2" ["nexon"]="$nexon_path2" ["gamejolt"]="$gamejolt_path2" ["artixgame"]="$artixgame_path2" ["arc"]="$arc_path2" ["poketcg"]="$poketcg_path2" ["antstream"]="$antstream_path2" ["purple"]="$purple_path2" ["plarium"]="$plarium_path2" ["vfun"]="$vfun_path2" ["tempo"]="$tempo_path2")

    names=(["epic_games"]="Epic Games" ["gog_galaxy"]="GOG Galaxy" ["uplay"]="Ubisoft Connect" ["battlenet"]="Battle.net" ["eaapp"]="EA App" ["amazongames"]="Amazon Games" ["itchio"]="itch.io" ["legacygames"]="Legacy Games" ["humblegames"]="Humble Games Collection" ["indiegala"]="IndieGala" ["rockstar"]="Rockstar Games Launcher" ["glyph"]="Glyph Launcher" ["minecraft"]="Minecraft Launcher" ["psplus"]="Playstation Plus" ["vkplay"]="VK Play" ["hoyoplay"]="HoYoPlay" ["nexon"]="Nexon Launcher" ["gamejolt"]="Game Jolt Client" ["artixgame"]="Artix Game Launcher" ["arc"]="ARC Launcher" ["poketcg"]="Pokémon Trading Card Game Live" ["antstream"]="Antstream Arcade" ["purple"]="PURPLE Launcher" ["plarium"]="Plarium Play" ["vfun"]="VFUN Launcher" ["tempo"]="Tempo Launcher")

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
    paths=(["nonsteamlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ["epicgameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ["goggalaxylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ["uplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" ["battlenetlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ["eaapplauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ["amazongameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ["itchiolauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" ["legacygameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ["humblegameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ["indiegalalauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ["rockstargameslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" ["glyphlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" ["minecraftlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher" ["pspluslauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher" ["vkplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" ["hoyoplaylauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher" ["nexonlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher" ["gamejoltlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/GameJoltLauncher" ["artixgamelauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/ArtixGameLauncher" ["arc"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/ARCLauncher" ["poketcglauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PokeTCGLauncher" ["antstreamlauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/AntstreamLauncher" ["purplelauncher"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PURPLELauncher" ["plarium"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher" ["vfun"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/VFUNLauncher" ["tempo"]="${logged_in_home}/.local/share/Steam/steamapps/compatdata/TempoLauncher")

    names=(["nonsteamlauncher"]="NonSteamLaunchers" ["epicgameslauncher"]="EpicGamesLauncher" ["goggalaxylauncher"]="GogGalaxyLauncher" ["uplaylauncher"]="UplayLauncher" ["battlenetlauncher"]="Battle.netLauncher" ["eaapplauncher"]="TheEAappLauncher" ["amazongameslauncher"]="AmazonGamesLauncher" ["itchiolauncher"]="itchioLauncher" ["legacygameslauncher"]="LegacyGamesLauncher" ["humblegameslauncher"]="HumbleGamesLauncher" ["indiegalalauncher"]="IndieGalaLauncher" ["rockstargameslauncher"]="RockstarGamesLauncher" ["glyphlauncher"]="GlyphLauncher" ["minecraftlauncher"]="MinecraftLauncher" ["pspluslauncher"]="PlaystationPlusLauncher" ["vkplaylauncher"]="VKPlayLauncher" ["hoyoplaylauncher"]="HoYoPlayLauncher" ["nexonlauncher"]="NexonLauncher" ["gamejoltlauncher"]="GameJoltLauncher" ["artixgamelauncher"]="ArtixGameLauncher" ["arc"]="ARCLauncher" ["poketcg"]="PokeTCGLauncher" ["antstreamlauncher"]="AntstreamLauncher" ["purplelauncher"]="PURPLELauncher" ["plariumlauncher"]="PlariumLauncher" ["vfunlauncher"]="VFUNLauncher" ["tempolauncher"]="TempoLauncher")

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
    cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation" || { echo "Failed to change directory. Exiting."; exit 1; }

    # Download tarball
    tarball_url=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .tar.gz)
    if [ -z "$tarball_url" ]; then
        echo "Failed to get tarball URL. Exiting."
        exit 1
    fi
    curl --retry 5 --retry-delay 0 --retry-max-time 60 -sLOJ "$tarball_url"
    if [ $? -ne 0 ]; then
        echo "Curl failed to download tarball. Exiting."
        exit 1
    fi

    # Download checksum
    checksum_url=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep browser_download_url | cut -d\" -f4 | grep .sha512sum)
    if [ -z "$checksum_url" ]; then
        echo "Failed to get checksum URL. Exiting."
        exit 1
    fi
    curl --retry 5 --retry-delay 0 --retry-max-time 60 -sLOJ "$checksum_url"
    if [ $? -ne 0 ]; then
        echo "Curl failed to download checksum. Exiting."
        exit 1
    fi

    # Verify checksum
    sha512sum -c ./*.sha512sum
    if [ $? -ne 0 ]; then
        echo "Checksum verification failed. Exiting."
        exit 1
    fi

    # Extract tarball
    tar -xf GE-Proton*.tar.gz -C "${logged_in_home}/.steam/root/compatibilitytools.d/"
    if [ $? -ne 0 ]; then
        echo "Tar extraction failed. Exiting."
        exit 1
    fi

    proton_dir=$(find -L "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
    echo "All done :)"
}

function update_proton() {
    echo "0"
    echo "# Detecting, Updating and Installing GE-Proton...please wait..."

    # Check if compatibilitytools.d exists and create it if it doesn't
    if [ ! -d "${logged_in_home}/.steam/root/compatibilitytools.d" ]; then
        mkdir -p "${logged_in_home}/.steam/root/compatibilitytools.d" || { echo "Failed to create directory. Exiting."; exit 1; }
    fi

    # Create NonSteamLaunchersInstallation subfolder in Downloads folder
    mkdir -p "${logged_in_home}/Downloads/NonSteamLaunchersInstallation" || { echo "Failed to create directory. Exiting."; exit 1; }

    # Set the path to the Proton directory
    proton_dir=$(find -L "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

    # Check if GE-Proton is installed
    if [ -z "$proton_dir" ]; then
        download_ge_proton
    else
        # Check if installed version is the latest version
        installed_version=$(basename "$proton_dir" | sed 's/GE-Proton-//')
        latest_version=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep tag_name | cut -d '"' -f 4)
        if [ "$installed_version" != "$latest_version" ]; then
            download_ge_proton
        fi
    fi
}

# Function For Updating UMU Launcher
function download_umu_launcher() {
    echo "Downloading UMU Launcher using the GitHub API"
    cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation" || { echo "Failed to change directory. Exiting."; exit 1; }

    # Get the download URL for a file that matches the pattern 'umu-launcher-*zipapp*.tar.gz'
    zip_url=$(curl -s https://api.github.com/repos/Open-Wine-Components/umu-launcher/releases/latest | \
      grep '"browser_download_url":' | grep -E 'umu-launcher-.*-zipapp.*\.(zip|tar\.gz|tar)' | \
      cut -d '"' -f 4)

    if [ -z "$zip_url" ]; then
        echo "Failed to get zip/tar URL. Exiting."
    fi

    echo "Found download URL: $zip_url"

    # Download the file
    curl --retry 5 --retry-delay 0 --retry-max-time 60 -sLOJ "$zip_url"
    if [ $? -ne 0 ]; then
        echo "Curl failed to download the file. Exiting."
    fi

    # Ensure the bin directory exists
    if [ ! -d "${logged_in_home}/bin" ]; then
        mkdir -p "${logged_in_home}/bin" || { echo "Failed to create bin directory. Exiting."; exit 1; }
    fi

    # Get the downloaded file name
    downloaded_file=$(basename "$zip_url")

    # Check if the downloaded file is a .zip file or a .tar.gz file and extract accordingly
    if [[ "$downloaded_file" =~ \.zip$ ]]; then
        # Extract the .zip file into without preserving directory structure
        unzip -o -j "$downloaded_file" -d "${logged_in_home}/bin/"
        if [ $? -ne 0 ]; then
            echo "Zip extraction failed. Exiting."
        fi
    elif [[ "$downloaded_file" =~ \.tar\.gz$ ]] || [[ "$downloaded_file" =~ \.tar$ ]]; then
        # Check the actual file type using the `file` command
        file_type=$(file --mime-type -b "$downloaded_file")

        if [[ "$file_type" == "application/gzip" ]]; then
            # If it's a gzipped tar file, extract it without leading directory (strip umu/)
            tar --strip-components=1 -xvzf "$downloaded_file" -C "${logged_in_home}/bin/"
            if [ $? -ne 0 ]; then
                echo "Tar.gz extraction failed. Exiting."
                exit 1
            fi
        elif [[ "$file_type" == "application/x-tar" ]]; then
            # If it's a tar file (without gzip), extract it without leading directory
            tar --strip-components=1 -xvf "$downloaded_file" -C "${logged_in_home}/bin/"
            if [ $? -ne 0 ]; then
                echo "Tar extraction failed. Exiting."
            fi
        else
            echo "Unknown file type: $file_type. Exiting."
        fi
    else
        echo "Unsupported file type: $downloaded_file. Exiting."
    fi

    # Make all extracted files executable
    find "${logged_in_home}/bin/" -type f -exec chmod +x {} \;

    if [ -f "${logged_in_home}/bin/umu-run" ]; then
        "${logged_in_home}/bin/umu-run" winetricks --self-update
    else
        echo "umu-run not found. Skipping self-update."
    fi

    echo "UMU Launcher update completed :)"
}




function update_umu_launcher() {
    echo "0"
    echo "# Detecting, Updating and Installing UMU Launcher...please wait..."

    # Create NonSteamLaunchersInstallation subfolder in Downloads folder
    mkdir -p "${logged_in_home}/Downloads/NonSteamLaunchersInstallation" || { echo "Failed to create directory. Exiting."; exit 1; }

    # Set the path to the UMU Launcher directory
    umu_dir="${logged_in_home}/bin/umu-launcher"

    # Check if UMU Launcher is installed
    if [ ! -d "$umu_dir" ]; then
        download_umu_launcher
    else
        # Check if installed version is the latest version
        installed_version=$(cat "$umu_dir/version.txt")
        latest_version=$(curl -s https://api.github.com/repos/Open-Wine-Components/umu-launcher/releases/latest | grep tag_name | cut -d '"' -f 4)
        if [ "$installed_version" != "$latest_version" ]; then
            download_umu_launcher
        fi
    fi
}




# Pre-logic system cleanup
CheckInstallations
CheckInstallationDirectory

rm -rf "${logged_in_home}/.config/systemd/user/nslgamescanner.service"
unlink "${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service"
systemctl --user daemon-reload

# Define launcher entries
launcher_entries=(
  "FALSE|SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX"
  "$epic_games_value|$epic_games_text"
  "$gog_galaxy_value|$gog_galaxy_text"
  "$uplay_value|$uplay_text"
  "$battlenet_value|$battlenet_text"
  "$amazongames_value|$amazongames_text"
  "$eaapp_value|$eaapp_text"
  "$legacygames_value|$legacygames_text"
  "$itchio_value|$itchio_text"
  "$humblegames_value|$humblegames_text"
  "$indiegala_value|$indiegala_text"
  "$rockstar_value|$rockstar_text"
  "$glyph_value|$glyph_text"
  "$minecraft_value|$minecraft_text"
  "$psplus_value|$psplus_text"
  "$vkplay_value|$vkplay_text"
  "$hoyoplay_value|$hoyoplay_text"
  "$nexon_value|$nexon_text"
  "$gamejolt_value|$gamejolt_text"
  "$artixgame_value|$artixgame_text"
  "$arc_value|$arc_text"
  "$purple_value|$purple_text"
  "$plarium_value|$plarium_text"
  "$vfun_value|$vfun_text"
  "$tempo_value|$tempo_text"
  "$poketcg_value|$poketcg_text"
  "$antstream_value|$antstream_text"
  "FALSE|RemotePlayWhatever"
  "FALSE|NVIDIA GeForce NOW"
)

chrome_entries=(
  "FALSE|Fortnite"
  "FALSE|Venge"
  "FALSE|PokéRogue"
  "FALSE|Xbox Game Pass"
  "FALSE|Better xCloud"
  "FALSE|GeForce Now"
  "FALSE|Amazon Luna"
  "FALSE|Stim.io"
  "FALSE|Boosteroid Cloud Gaming"
  "FALSE|Rocketcrab"
  "FALSE|WebRcade"
  "FALSE|WebRcade Editor"
  "FALSE|Afterplay.io"
  "FALSE|OnePlay"
  "FALSE|AirGPU"
  "FALSE|CloudDeck"
  "FALSE|JioGamesCloud"
  "FALSE|WatchParty"
  "FALSE|Netflix"
  "FALSE|Hulu"
  "FALSE|Tubi"
  "FALSE|Disney+"
  "FALSE|Amazon Prime Video"
  "FALSE|Youtube"
  "FALSE|Youtube TV"
  "FALSE|Twitch"
  "FALSE|Apple TV+"
  "FALSE|Crunchyroll"
  "FALSE|Plex"
)

# Convert to newline-separated strings
launcher_data=$(IFS=$'\n'; echo "${launcher_entries[*]}")
chrome_data=$(IFS=$'\n'; echo "${chrome_entries[*]}")

# Export environment variables for GTK UI
export LAUNCHER_DATA="${launcher_data}"
export CHROME_DATA="${chrome_data}"
export UI_VERSION="${version}"
export UI_LIVE="${live}"

# Arrays and flags to be filled
selected_launchers=()
custom_websites=()
separate_appids=false

# --- Handle command line arguments or fallback to GTK UI ---

if [ $# -eq 0 ]; then
    # No CLI args — show GTK UI

    readarray -t gtk_output < <(python3 - <<'EOF'
import gi, os, sys
import subprocess
import re

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

def get_screen_resolution():
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
    resolutions = re.findall(r"(\d+)x(\d+)\s*\*+", xrandr_output)
    return map(int, resolutions[0]) if resolutions else (1920, 1080)

def is_multiple_monitors():
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
    return len(re.findall(r" connected", xrandr_output)) > 1

screen_width, screen_height = get_screen_resolution()
if is_multiple_monitors():
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
    match = re.search(r"(\d+)x(\d+)\s+connected", xrandr_output)
    if match:
        screen_width, screen_height = map(int, match.groups())

zenity_width = screen_width * 80 // 100
zenity_height = screen_height * 80 // 100

version = os.environ.get("UI_VERSION", "NSL")
live = os.environ.get("UI_LIVE", "")

launcher_lines = os.environ.get("LAUNCHER_DATA", "").splitlines()
chrome_lines = os.environ.get("CHROME_DATA", "").splitlines()

class LauncherUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Which launchers do you want to download and install?")
        self.set_default_size(zenity_width, zenity_height)

        self.store_launchers = Gtk.ListStore(bool, str)
        self.store_chrome = Gtk.ListStore(bool, str)

        for line in launcher_lines:
            if "|" in line:
                value, label = line.split("|", 1)
                active = value == "TRUE"
                self.store_launchers.append([active, label])

        for line in chrome_lines:
            if "|" in line:
                value, label = line.split("|", 1)
                active = value == "TRUE"
                self.store_chrome.append([active, label])

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin=10)
        self.add(main_box)

        header_label = Gtk.Label()
        header_label.set_markup(f"<b>{version}</b> — Default = one App ID Installation, One Prefix, NonSteamLaunchers - updated the NSLGameScanner.py {live}")
        header_label.set_line_wrap(True)
        header_label.set_xalign(0)
        main_box.pack_start(header_label, False, False, 0)

        def create_tree(model, toggle_callback):
            tree = Gtk.TreeView(model=model)
            toggle = Gtk.CellRendererToggle()
            toggle.connect("toggled", toggle_callback)
            tree.append_column(Gtk.TreeViewColumn("Select", toggle, active=0))
            tree.append_column(Gtk.TreeViewColumn("Launcher", Gtk.CellRendererText(), text=1))
            return tree

        launcher_label = Gtk.Label(label="Launchers:")
        launcher_label.set_xalign(0)
        main_box.pack_start(launcher_label, False, False, 0)

        launcher_tree = create_tree(self.store_launchers, self.on_toggle_launcher)
        scrolled1 = Gtk.ScrolledWindow()
        scrolled1.set_vexpand(True)
        scrolled1.add(launcher_tree)
        main_box.pack_start(scrolled1, True, True, 0)

        chrome_label = Gtk.Label(label="Google Chrome-based Services:")
        chrome_label.set_xalign(0)
        main_box.pack_start(chrome_label, False, False, 0)

        chrome_tree = create_tree(self.store_chrome, self.on_toggle_chrome)
        scrolled2 = Gtk.ScrolledWindow()
        scrolled2.set_vexpand(True)
        scrolled2.add(chrome_tree)
        main_box.pack_start(scrolled2, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter custom websites that you want shortcuts for, separated by commas. Leave blank and press ok if you don't want any. E.g. myspace.com, limewire.com, my.screenname.aol.com")
        main_box.pack_start(self.entry, False, False, 0)

        button_box = Gtk.Box(spacing=6)
        self.button_result = None
        for label in ["Cancel", "OK", "❤️", "Uninstall", "🔍", "Start Fresh", "Move to SD Card", "Update Proton-GE", "🖥️ Off", "NSLGameSaves", "README"]:
            btn = Gtk.Button(label=label)
            btn.connect("clicked", self.on_button_clicked, label)
            button_box.pack_start(btn, True, True, 0)

        main_box.pack_start(button_box, False, False, 0)

    def on_toggle_launcher(self, widget, path):
        self.store_launchers[path][0] = not self.store_launchers[path][0]

    def on_toggle_chrome(self, widget, path):
        self.store_chrome[path][0] = not self.store_chrome[path][0]

    def on_button_clicked(self, button, label):
        selected = [row[1] for row in self.store_launchers if row[0]] + [row[1] for row in self.store_chrome if row[0]]
        websites = self.entry.get_text().strip()
        print("|".join(selected))
        print(websites)
        print(label)
        sys.stdout.flush()
        Gtk.main_quit()

win = LauncherUI()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
EOF
)





    selected_launchers_str="${gtk_output[0]}"
    custom_websites_str="${gtk_output[1]}"
    extra_button="${gtk_output[2]}"

    IFS=',' read -ra custom_websites <<< "$custom_websites_str"
    IFS='|' read -ra selected_launchers <<< "$selected_launchers_str"

    # Determine what to put in options:
    if [[ "$extra_button" == "OK" ]]; then
        options="$selected_launchers_str"
    elif [[ "$selected_launchers_str" == "" ]]; then
        # Only a button was pressed, no launchers selected
        options="$extra_button"
    else
        # Button pressed with launchers selected, combine both
        options="$extra_button|$selected_launchers_str"
    fi
else
    # CLI args present — parse them
    for arg in "$@"; do
        if [[ "$arg" =~ ^https?:// ]]; then
            website=${arg#http://}
            website=${website#https://}
            IFS=',' read -ra websites <<< "$website"
            for site in "${websites[@]}"; do
                custom_websites+=("$site")
            done
        else
            selected_launchers+=("$arg")
        fi
    done

    # ✅ Add this line after building the custom_websites array
    custom_websites_str=$(IFS=', '; echo "${custom_websites[*]}")

    extra_button="OK"
    options="${selected_launchers[*]}"
fi



# Handle validation (skip if extra button is special)
case "$extra_button" in
    "Start Fresh"|"Uninstall"|"Move to SD Card"|"Update Proton-GE"|"NSLGameSaves"|"README"|"🖥️ Off"|"❤️"|"🔍")
        # Skip validation
        ;;
    *)
        if [ ${#selected_launchers[@]} -eq 0 ] && [ ${#custom_websites[@]} -eq 0 ]; then
            zenity --error --text="No launchers or websites selected. Exiting." --width=300 --timeout=5
            exit 1
        fi
        ;;
esac

# Handle special buttons
if [[ "$extra_button" == "🖥️ Off" ]]; then
    sleep 1
    xset dpms force off
    exit 0
fi

if [[ "$extra_button" == "README" ]]; then
    README_URL="https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/README.md"
    TEMP_FILE=$(mktemp)
    curl -s "$README_URL" |
        sed 's/<[^>]*>//g' |
        sed 's/^###\s*/---\n/g' |
        sed 's/^##\s*/--\n/g' |
        sed 's/^#\s*/\n/g' |
        sed 's/^[-*]\s*/- /g' > "$TEMP_FILE"
    zenity --text-info --title="NonSteamLaunchers README" --width=800 --height=600 --filename="$TEMP_FILE"
    rm "$TEMP_FILE"
    exit 1
fi

# Determine if separate app ID option was selected
for launcher in "${selected_launchers[@]}"; do
    if [[ "$launcher" == "SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX" ]]; then
        separate_appids=true
        break
    fi
done

# Check if the user selected to use separate app IDs
if [[ $options == *"SEPARATE APP IDS - CHECK THIS TO SEPARATE YOUR PREFIX"* ]]; then
    # User selected to use separate app IDs
    use_separate_appids=true
else
    # User did not select to use separate app IDs
    use_separate_appids=false
fi

# Debug Output (optional)
echo "Selected launchers: ${selected_launchers[*]}"
echo "Custom websites: ${custom_websites[*]}"
echo "Separate App IDs: $separate_appids"
echo "Extra button: $extra_button"
echo "Options: $options"






# Define the StartFreshFunction
function StartFreshFunction {
    # Define the path to the compatdata directory
    compatdata_dir="${logged_in_home}/.local/share/Steam/steamapps/compatdata"
    # Define the path to the other directory
    other_dir="${logged_in_home}/.local/share/Steam/steamapps/shadercache/"

    # Define an array of original folder names
    folder_names=("EpicGamesLauncher" "GogGalaxyLauncher" "UplayLauncher" "Battle.netLauncher" "TheEAappLauncher" "AmazonGamesLauncher" "itchioLauncher" "LegacyGamesLauncher" "HumbleGamesLauncher" "IndieGalaLauncher" "RockstarGamesLauncher" "GlyphLauncher" "PlaystationPlusLauncher" "VKPlayLauncher" "HoYoPlayLauncher" "NexonLauncher" "GameJoltLauncher" "ArtixGameLauncher" "ARCLauncher" "PokeTCGLauncher" "AntstreamLauncher" "PURPLELauncher" "PlariumLauncher" "VFUNLauncher" "TempoLauncher")

    # Define an array of app IDs
    app_ids=("3772819390" "4294900670" "4063097571" "3786021133" "3448088735" "3923904787" "3440562512" "2948446662" "3908676077" "4206469918" "3303169468" "3595505624" "4272271078" "3259996605" "2588786779" "4090616647" "3494943831" "2390200925" "4253976432" "2221882453" "2296676888" "2486751858" "3974004104" "3811372789" "3788101956" "3782277090" "3640061468" "3216372511" "2882622939" "2800812206" "2580882702" "4022508926" "4182617613" "1981254598" "2136059209" "1401184678" "3141683525")

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
    rm -rf "/run/media/mmcblk0p1/HoYoPlayLauncher/"
    rm -rf "/run/media/mmcblk0p1/NexonLauncher/"
    rm -rf "/run/media/mmcblk0p1/GameJoltLauncher/"
    rm -rf "/run/media/mmcblk0p1/ArtixGameLauncher/"
    rm -rf "/run/media/mmcblk0p1/ARCLauncher/"
    rm -rf "/run/media/mmcblk0p1/PokeTCGLauncher/"
    rm -rf "/run/media/mmcblk0p1/AntstreamLauncher/"
    rm -rf "/run/media/mmcblk0p1/PURPLELauncher/"
    rm -rf "/run/media/mmcblk0p1/PlariumLauncher/"
    rm -rf "/run/media/mmcblk0p1/VFUNLauncher/"
    rm -rf "/run/media/mmcblk0p1/TempoLauncher/"
    rm -rf ${logged_in_home}/Downloads/NonSteamLaunchersInstallation
    rm -rf ${logged_in_home}/.config/systemd/user/Modules
    rm -rf ${logged_in_home}/.config/systemd/user/env_vars
    rm -rf ${logged_in_home}/.config/systemd/user/NSLGameScanner.py
	rm -rf ${logged_in_home}/.config/systemd/user/shortcuts
    rm -rf ${logged_in_home}/.local/share/applications/RemotePlayWhatever
    rm -rf ${logged_in_home}/.local/share/applications/RemotePlayWhatever.desktop
    rm -rf ${logged_in_home}/Downloads/NonSteamLaunchers-install.log

    # Delete the service file
    rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service

    # Remove the symlink
    unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service

    # Reload the systemd user instance
    systemctl --user daemon-reload

    show_message "NonSteamLaunhers has been wiped!"

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
exe_url=https://content-system.gog.com/open_link/download?path=/open/galaxy/client/2.0.74.352/setup_galaxy_2.0.74.352.exe
#exe_url=https://webinstallers.gog-statics.com/download/GOG_Galaxy_2.0.exe

# Set the path to save the second file to
exe_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/setup_galaxy_2.0.74.352.exe
#exe_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/GOG_Galaxy_2.0.exe

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

# Set the URL to download the Hoyo Play Play Launcher file from
hoyoplay_url="https://download-porter.hoyoverse.com/download-porter/2025/02/21/VYTpXlbWo8_1.4.5.222_1_0_hyp_hoyoverse_prod_202502081529_XFGRLkBk.exe"

# Set the path to save the Hoyo Play Launcher to
hoyoplay_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/HoYoPlay_install.exe"

# Set the URL to download the Nexon Launcher file from
nexon_url="https://download.nxfs.nexon.com/download-launcher?file=NexonLauncherSetup.exe&client-id=959013368.1720525616"

# Set the path to save the Nexon Launcher to
nexon_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/NexonLauncherSetup.exe


# Set the URL to download the GameJolt Launcher file from
gamejolt_url="https://tinyurl.com/3z8wpv2v"

# Set the path to save the GameJolt Launcher to
gamejolt_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/gamejoltclientsetup.exe

# Set the URL to download the artix Launcher file from
artixgame_url=https://launch.artix.com/latest/ArtixLauncher_win_x64.exe

# Set the path to save the artix Launcher to
artixgame_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/ArtixLauncher_win_x64.exe"


# Set the URL to download the arc Launcher file from
arc_url=https://www.arcgames.com/download

# Set the path to save the arc Launcher to
arc_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/Ar3Setup.exe"

#PokemonTCGLIVE

poketcg_url=https://installer.studio-prod.pokemon.com/installer/PokemonTCGLiveInstaller.msi

poketcg_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/PokemonTCGLiveInstaller.msi

#Antstream Arcade

antstream_url=https://downloads.antstream.com/antstreamInstaller-2.1.2986.exe
antstream_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/antstreamInstaller-2.1.2986.exe


#PURPLE Launcher
purple_url=https://gs-purple-inst.download.ncupdate.com/Purple/PurpleInstaller_2_25_325_23.exe
purple_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/PurpleInstaller_2_25_325_23.exe

#Plarium Launcher
plarium_url="https://installer.plarium.com/desktop?lid=1&arc=64&os=windows"
plarium_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/PlariumPlaySetup.exe


#VFUNLauncher
vfun_url=https://vfun-cdn.qijisoft.com/vlauncher/fullclient/VFUNLauncherInstaller.exe
vfun_file=${logged_in_home}/Downloads/NonSteamLaunchersInstallation/VFUNLauncherInstaller.exe

# TempoLauncher
tempo_url="https://cdn.playthebazaar.com/launcher-0ca5d6/Tempo%20Launcher%20-%20Beta%20Setup%201.0.4.exe"
tempo_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/TempoLauncherSetup.exe"




#End of Downloads INFO






# Function to handle common uninstallation tasks
handle_uninstall_common() {
    compatdata_dir=$1
    uninstaller_path=$2
    uninstaller_options=$3
    app_name=$4

    # Set the path to the Proton directory
    proton_dir=$(find -L "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

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



# Uninstall EA App
if [[ $uninstall_options == *"Uninstall EA App"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts" ]]; then
        handle_uninstall_ea "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts" ]]; then
        handle_uninstall_ea "TheEAappLauncher"
    fi
fi




# Function to handle GOG Galaxy uninstallation
handle_uninstall_gog() {
    gog_uninstaller="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files (x86)/GOG Galaxy/unins000.exe"
    handle_uninstall_common "$1" "$gog_uninstaller" "/SILENT" "GOG Galaxy"
}


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

# Function to handle Artix uninstallation
handle_uninstall_artix() {
    artix_uninstaller="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files/Artix Game Launcher/Uninstall Artix Game Launcher.exe"
    handle_uninstall_common "$1" "$artix_uninstaller" "/S" "Artix Game Launcher"
}

# Uninstall Artix
if [[ $uninstall_options == *"Uninstall Artix Game Launcher"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Artix Game Launcher" ]]; then
        handle_uninstall_artix "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/ArtixGameLauncher/pfx/drive_c/Program Files/Artix Game Launcher" ]]; then
        handle_uninstall_artix "ArtixGameLauncher"
    fi
fi


# Function to handle Antstream uninstallation
handle_uninstall_antstream() {
    mkdir -p ${logged_in_home}/Downloads/NonSteamLaunchersInstallation

    # Download Antstream file
    if [ ! -f "$antstream_file" ]; then
        echo "Downloading Antstream Arcade file"
        wget $antstream_url -O $antstream_file
    fi

    handle_uninstall_common "$1" "$antstream_file" "/uninstall /quiet" "AntStream Arcade"
}

# Uninstall Antstream Arcade
if [[ $uninstall_options == *"Uninstall Antstream Arcade"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
        handle_uninstall_antstream "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AntstreamLauncher/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
        handle_uninstall_antstream "AntstreamLauncher"
    fi
fi

# Function to handle PURPLE uninstallation
handle_uninstall_purple() {
    # Define the path to the Purple uninstaller
    purpleun_file="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files (x86)/NCSOFT/Purple/Uninstall.exe"

    # Call the common uninstallation handler with necessary parameters
    handle_uninstall_common "$1" "$purpleun_file" "/S" "PURPLE Launcher"

    sleep 5

    # Timeout duration (30 seconds)
    timeout=30
    elapsed=0
    while [ $elapsed -lt $timeout ]; do
        # Check if Un_A.exe is running
        if pgrep -f "Un_A.exe" > /dev/null; then
            # Kill the Un_A.exe process
            pkill -f "Un_A.exe"
            echo "Un_A.exe has been terminated."
            return
        fi

        # Wait for 1 second before checking again
        sleep 1
        elapsed=$((elapsed + 1))
    done

    # If we reach here, Un_A.exe wasn't found within the timeout
    echo "Un_A.exe was not found within the $timeout seconds timeout."
}



# Uninstall PURPLE
if [[ $uninstall_options == *"Uninstall PURPLE Launcher"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
        handle_uninstall_purple "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
        handle_uninstall_purple "PURPLELauncher"
    fi
fi




# Function to handle Plarium Play folder deletion
handle_uninstall_plarium() {
    # Define the two possible paths
    plarium_play_dir_1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay"
    plarium_play_dir_2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay"

    # Check if either of the directories exists and delete the first one found
    if [ -d "$plarium_play_dir_1" ]; then
        echo "Deleting PlariumPlay folder from path 1... and is now uninstalled."
        rm -rf "$plarium_play_dir_1"
        # Notify the user via Zenity
        zenity --info --text="Plarium Play folder has been successfully deleted from path 1." --width=300 --height=150 &
        sleep 3
        killall zenity
    elif [ -d "$plarium_play_dir_2" ]; then
        echo "Deleting PlariumPlay folder from path 2...and is now uninstalled."
        rm -rf "$plarium_play_dir_2"
        # Notify the user via Zenity
        zenity --info --text="Plarium Play folder has been successfully deleted from path 2." --width=300 --height=150 &
        sleep 3
        killall zenity
    else
        # Notify the user if neither folder exists
        zenity --error --text="Plarium Play folder not found at either path. Please check the paths." --width=300 --height=150 &
    fi
}


# Function to handle Tempo uninstallation
handle_uninstall_tempo() {
    tempo_uninstaller="${logged_in_home}/.local/share/Steam/steamapps/compatdata/${1}/pfx/drive_c/Program Files/Tempo Launcher - Beta/Uninstall Tempo Launcher - Beta.exe"
    handle_uninstall_common "$1" "$tempo_uninstaller" "/S" "Tempo Launcher"
}


# Uninstall Tempo
if [[ $uninstall_options == *"Uninstall Tempo Launcher"* ]]; then
    if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Tempo Launcher - Beta" ]]; then
        handle_uninstall_tempo "NonSteamLaunchers"
    elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TempoLauncher/pfx/drive_c/Program Files/Tempo Launcher - Beta" ]]; then
        handle_uninstall_tempo "TempoLauncher"
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
                rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GOG.com"
                uninstall_launcher "$uninstall_options" "GOG Galaxy" "$gog_galaxy_path1" "$gog_galaxy_path2" "" "" "gog"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy" ]]; then
                handle_uninstall_gog "GogGalaxyLauncher"
                rm -rf "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/users/steamuser/AppData/Local/GOG.com"
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

        if [[ $uninstall_options == *"Uninstall Artix Game Launcher"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Artix Game Launcher" ]]; then
                handle_uninstall_artix "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Artix Game Launcher" "$artixgame_path1" "$artixgame_path2" "" "" "artixgame"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/ArtixGameLauncher/pfx/drive_c/Program Files/Artix Game Launcher" ]]; then
                handle_uninstall_artix "ArtixGameLauncher"
                uninstall_launcher "$uninstall_options" "Artix Game Launcher" "$artixgame_path1" "$artixgame_path2" "" "" "artixgame"
            fi
        fi

        if [[ $uninstall_options == *"Uninstall Antstream Arcade"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
                handle_uninstall_antstream "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Antstream Arcade" "$antstream_path1" "$antstream_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" "antstream" "antstream"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AntstreamLauncher/pfx/drive_c/Program Files (x86)/Antstream Ltd" ]]; then
                handle_uninstall_antstream "AntstreamLauncher"
                uninstall_launcher "$uninstall_options" "Antstream Arcade" "$antstream_path1" "$antstream_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Antstream Ltd" "antstream" "antstream"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            fi
        fi
        # Uninstall PURPLE Launcher
        if [[ $uninstall_options == *"Uninstall PURPLE Launcher"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/NCSOFT" ]]; then
                handle_uninstall_purple "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "PURPLE Launcher" "$purple_path1" "$purple_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/NCSOFT" "" "purple"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PURPLELauncher/pfx/drive_c/Program Files (x86)/NCSOFT" ]]; then
                handle_uninstall_purple "PURPLELauncher"
                uninstall_launcher "$uninstall_options" "PURPLE Launcher" "$purple_path1" "$purple_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PURPLELauncher/pfx/drive_c/Program Files (x86)/NCSOFT" "" "purple"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            fi
        fi

        if [[ $uninstall_options == *"Uninstall Plarium Play"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay" ]]; then
                handle_uninstall_plarium "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Plarium Play" "$plarium_path1" "$plarium_path2" "plarium" "plarium"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher" ]]; then
                handle_uninstall_plarium "PlariumLauncher"
                uninstall_launcher "$uninstall_options" "Plarium Play" "$eaapp_path1" "$eaapp_path2" "plarium" "plarium"
                sed -i '' "${logged_in_home}/.config/systemd/user/env_vars"
            fi
        fi


        if [[ $uninstall_options == *"Uninstall Tempo Launcher"* ]]; then
            if [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Tempo Launcher - Beta" ]]; then
                handle_uninstall_tempo "NonSteamLaunchers"
                uninstall_launcher "$uninstall_options" "Tempo Launcher" "$tempo_path1" "$tempo_path2" "" "" "tempo"
            elif [[ -d "${logged_in_home}/.local/share/Steam/steamapps/compatdata/TempoLauncher/pfx/drive_c/Program Files/Tempo Launcher - Beta" ]]; then
                handle_uninstall_tempo "TempoLauncher"
                uninstall_launcher "$uninstall_options" "Tempo Launcher" "$tempo_path1" "$tempo_path2" "" "" "tempo"
            fi
        fi






        if [[ $uninstall_options == *"Uninstall RemotePlayWhatever"* ]]; then
            rm -rf "${logged_in_home}/.local/share/applications/RemotePlayWhatever"
            rm -rf "${logged_in_home}/.local/share/applications/RemotePlayWhatever.desktop"

            zenity --info --text="RemotePlayWhatever has been uninstalled." --width=200 --height=150 &
            sleep 3
            killall zenity
        fi


        if [[ $uninstall_options == *"Uninstall NVIDIA GeForce NOW"* ]]; then
            # Uninstall GeForce NOW Flatpak app and repository (user scope)
            flatpak uninstall -y --delete-data --force-remove --user com.nvidia.geforcenow
            flatpak remote-delete --user GeForceNOW

            zenity --info --text="NVIDIA GeForce NOW has been uninstalled." --width=250 --height=150 &
            sleep 3
            killall zenity
        fi

        uninstall_launcher "$uninstall_options" "Uplay" "$uplay_path1" "$uplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher" "uplay" "ubisoft"
        uninstall_launcher "$uninstall_options" "Battle.net" "$battlenet_path1" "$battlenet_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" "battle" "bnet"
        uninstall_launcher "$uninstall_options" "Epic Games" "$epic_games_launcher_path1" "$epic_games_launcher_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" "epic"
        uninstall_launcher "$uninstall_options" "Amazon Games" "$amazongames_path1" "$amazongames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" "amazon"
        uninstall_launcher "$uninstall_options" "itch.io" "$itchio_path1" "$itchio_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher" "itchio"
        uninstall_launcher "$uninstall_options" "Humble Games Collection" "$humblegames_path1" "$humblegames_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" "humble"
        uninstall_launcher "$uninstall_options" "IndieGala" "$indiegala_path1" "$indiegala_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" "indie"
        uninstall_launcher "$uninstall_options" "Rockstar Games Launcher" "$rockstar_path1" "$rockstar_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" "rockstar"
        uninstall_launcher "$uninstall_options" "Glyph Launcher" "$glyph_path1" "$glyph_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Glyph" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher" "glyph"
        uninstall_launcher "$uninstall_options" "Minecraft Launcher" "$minecraft_path1" "$minecraft_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Minecraft Launcher" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher" "minecraft"
        uninstall_launcher "$uninstall_options" "VK Play" "$vkplay_path1" "$vkplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameCenter" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher" "vkplay"
        uninstall_launcher "$uninstall_options" "HoYoPlay" "$hoyoplay_path1" "$hoyoplay_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/HoYoPlay" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher" "hoyoplay"
        uninstall_launcher "$uninstall_options" "Nexon Launcher" "$nexon_path1" "$nexon_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Nexon" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher" "nexon"
        uninstall_launcher "$uninstall_options" "Game Jolt Client" "$gamejolt_path1" "$gamejolt_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/GameJoltClient" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GameJoltLauncher" "gamejolt"
        uninstall_launcher "$uninstall_options" "ARC Launcher" "$arc_path1" "$arc_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Arc" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/ARCLauncher" "arc"
        uninstall_launcher "$uninstall_options" "Pokémon Trading Card Game Live" "$poketcg_path1" "$poketcg_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/The Pokémon Company International" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PokeTCGLauncher" "poketcg"
        uninstall_launcher "$uninstall_options" "Plarium Play" "$plarium_path1" "$plarium_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/PlariumPlay" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher" "plarium"

        uninstall_launcher "$uninstall_options" "VFUN Launcher" "$vfun_path1" "$vfun_path2" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/VFUN/VLauncher" "${logged_in_home}/.local/share/Steam/steamapps/compatdata/VFUNLauncher" "vfun"

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
            FALSE "Humble Games Collection" \
            FALSE "IndieGala" \
            FALSE "Rockstar Games Launcher" \
            FALSE "Glyph Launcher" \
            FALSE "Minecraft Launcher" \
            FALSE "Playstation Plus" \
            FALSE "VK Play" \
            FALSE "HoYoPlay" \
            FALSE "Nexon Launcher" \
            FALSE "Game Jolt Client" \
            FALSE "Artix Game Launcher" \
            FALSE "ARC Launcher" \
            FALSE "PURPLE Launcher" \
            FALSE "Plarium Play" \
            FALSE "VFUN Launcher" \
            FALSE "Tempo Launcher" \
            FALSE "Pokémon Trading Card Game Live" \
            FALSE "Antstream Arcade" \
            FALSE "RemotePlayWhatever" \
            FALSE "NVIDIA GeForce NOW" \
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

    move_options=$(zenity --list --text="Which launcher IDs do you want to move to the SD card?" --checklist --column="Select" --column="Launcher ID" $nonsteamlauncher_move_value "NonSteamLaunchers" $epicgameslauncher_move_value "EpicGamesLauncher" $goggalaxylauncher_move_value "GogGalaxyLauncher" $uplaylauncher_move_value "UplayLauncher" $battlenetlauncher_move_value "Battle.netLauncher" $eaapplauncher_move_value "TheEAappLauncher" $amazongameslauncher_move_value "AmazonGamesLauncher" $itchiolauncher_move_value "itchioLauncher" $legacygameslauncher_move_value "LegacyGamesLauncher" $humblegameslauncher_move_value "HumbleGamesLauncher" $indiegalalauncher_move_value "IndieGalaLauncher" $rockstargameslauncher_move_value "RockstarGamesLauncher" $glyphlauncher_move_value "GlyphLauncher" "$minecraftlauncher_move_value" "MinecraftLauncher" $pspluslauncher_move_value "PlaystationPlusLauncher" $vkplaylauncher_move_value "VKPlayLauncher" $hoyoplaylauncher_move_value "HoYoPlayLauncher" $nexonlauncher_move_value "NexonLauncher" $gamejoltlauncher_move_value "GameJoltLauncher" $artixgame_move_value "ArtixGameLauncher" $arc_move_value "ARCLauncher" $purple_move_value "PURPLELauncher" $plarium_move_value "PlariumLauncher" $vfun_move_value "VFUNLauncher" $tempo_move_value "TempoLauncher" $poketcg_move_value "PokeTCGLauncher" $antstream_move_value "AntstreamLauncher" --width=335 --height=524)

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

# Check if the 🔍 option was passed as a command line argument or clicked in the GUI
if [[ " ${args[@]} " =~ " 🔍 " ]] || [[ $options == "🔍" ]]; then
    stop_service

    # If command line arguments were provided, exit the script
    if [ ${#args[@]} -ne 0 ]; then
        rm -rf ${logged_in_home}/.config/systemd/user/env_vars
        exit 0
    fi

    # If no command line arguments were provided, display the zenity window
    zenity --question --text="NSLGameScanner has been stopped and is no longer scanning for games. Do you want to run it again? Pressing 'Yes' will turn on 'Auto Scan' until you stop it again." --width=200 --height=150
    if [ $? = 0 ]; then
        # User wants to run NSLGameScanner again
        python3 $python_script_path
        show_message "NSLGameScanner is now restarting!"
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
update_umu_launcher

# Also call the function when the button is pressed
if [[ $options == *"Update Proton-GE"* ]]; then
    update_proton
    update_umu_launcher
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




if [[ $options == *"NSLGameSaves"* ]]; then
    zenity --info --text="Restoring your game saves from: /home/deck/NSLGameSaves, back into your prefix and launchers, all at once." --timeout=5
    echo "Running restore..."
    nohup flatpak run com.github.mtkennerly.ludusavi --config "${logged_in_home}/.var/app/com.github.mtkennerly.ludusavi/config/ludusavi/NSLconfig/" restore --force > /dev/null 2>&1 &
    wait $!
    echo "Restore completed"
    zenity --info --text="Restore was successful, you may now download your games from your launchers, and verify if the game saves are restored." --timeout=5
    exit 0
fi

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
    end=$((SECONDS+90))  # Timeout after 90 seconds
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

    # Check both Temp directories for Galaxy installer folder
    temp_dir1="${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/AppData/Local/Temp"
    temp_dir2="${logged_in_home}/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/Temp"

    # First check temp_dir1 (AppData/Local/Temp)
    if [ -d "$temp_dir1" ]; then
        cd "$temp_dir1"
        # Check if we found the installer folder
        for dir in GalaxyInstaller_*; do
            if [ -d "$dir" ]; then
                galaxy_installer_folder="$dir"
                break
            fi
        done
    fi

    # If not found, check temp_dir2 (Temp)
    if [ -z "$galaxy_installer_folder" ] && [ -d "$temp_dir2" ]; then
        cd "$temp_dir2"
        # Now check if we found the installer folder in the second directory
        for dir in GalaxyInstaller_*; do
            if [ -d "$dir" ]; then
                galaxy_installer_folder="$dir"
                break
            fi
        done
    fi

    # If no installer folder was found in either directory, exit
    if [ -z "$galaxy_installer_folder" ]; then
        echo "Galaxy installer folder not found in either Temp directory"
        return 1
    fi

    # Copy the GalaxyInstaller_* folder to Downloads
    echo "Found Galaxy installer folder: $galaxy_installer_folder"
    cp -r "$galaxy_installer_folder" "${logged_in_home}/Downloads/NonSteamLaunchersInstallation/"

    # Navigate to the copied folder in Downloads
    cd "${logged_in_home}/Downloads/NonSteamLaunchersInstallation/$(basename "$galaxy_installer_folder")"

    # Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
    echo "Running GalaxySetup.exe with the /VERYSILENT and /NORESTART options"
    "$STEAM_RUNTIME" "$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART &

    # Wait for the GalaxySetup.exe to finish running with a timeout of 90 seconds
    end=$((SECONDS+90))  # Timeout after 90 seconds
    while true; do
        # Kill GalaxyClient.exe every 10 seconds if it's running
        if [ $((SECONDS % 20)) -eq 0 ]; then
            if pgrep -f "GalaxyClient.exe" > /dev/null; then
                echo "Killing GalaxyClient.exe"
                pkill -f "GalaxyClient.exe"
            fi
        fi

        # Break the loop when GalaxySetup.exe finishes
        if ! pgrep -f "GalaxySetup.exe" > /dev/null; then
            echo "GalaxySetup.exe has finished running"
            break
        fi

        # Timeout check (90 seconds)
        if [ $SECONDS -gt $end ]; then
            echo "Timeout while waiting for GalaxySetup.exe to finish"
            break
        fi

        sleep 1
    done
}

function install_gog2 {
    echo "45"
    echo "# Downloading & Installing GOG Galaxy... Please wait..."

    # Check if either of the GOG Galaxy executables exists
    if [ -e "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe" ] || \
       [ -e "${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe" ]; then

        echo "GOG Galaxy executable found. Checking for setup_galaxy_2 process..."

        # Now, check if setup_galaxy_2 is running and kill it
        end=$((SECONDS+90))  # Timeout after 90 seconds
        while true; do
            if pgrep -f "setup_galaxy_2." > /dev/null; then
                pkill -f "setup_galaxy_2."
                echo "Setup process killed."
                break
            fi
            if [ $SECONDS -gt $end ]; then
                echo "Timeout while trying to kill setup_galaxy_2."
                break
            fi
            sleep 1
        done
    else
        echo "GOG Galaxy executable not found, skipping process kill."
    fi
}



# Battle.net specific installation steps
function install_battlenet {
    # Terminate any existing Battle.net processes before starting installation
    #terminate_processes "Battle.net.exe" #"BlizzardError.exe"


    # Start the first installation
    echo "Starting first installation of Battle.net"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net"

    # Optional: kill wineserver after installation is completely done
    #pkill wineserver
    echo "Battle.net installation complete."

    sleep 1
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
    installer_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/HoYoPlay_install.exe"
    target_dir="${hoyo_dir}/1.4.5.222"

    echo "Creating directory for HoYoPlay..."
    mkdir -p "${hoyo_dir}" || { echo "Failed to create directory"; return 1; }

    echo "Copying installer to the target directory..."
    cp "${installer_file}" "${hoyo_dir}" || { echo "Failed to copy installer"; return 1; }

    echo "Changing directory to the target directory..."
    cd "${hoyo_dir}" || { echo "Failed to change directory"; return 1; }

    echo "Running 7z extraction..."
    output=$(7z x "HoYoPlay_install.exe" -o"${hoyo_dir}" -aoa)
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
    rm -f "${hoyo_dir}/HoYoPlay_install.exe" || { echo "Failed to remove installer file"; return 1; }

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
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$exe_file" /silent &
                install_gog2
            elif [ "$launcher_name" = "Battle.net" ]; then


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
            elif [ "$launcher_name" = "ARC Launcher" ]; then
                "$STEAM_RUNTIME" "$proton_dir/proton" run "$arc_file"
                pid=$!
                while pgrep -x "Arc3Install_202" > /dev/null; do
                    sleep 1
                done
                sleep 5
                echo "ARC Launcher installation complete."
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

        wait
        pkill -f wineserver
    fi
}
# Install Epic Games Launcher
install_launcher "Epic Games" "EpicGamesLauncher" "$msi_file" "$msi_url" "MsiExec.exe /i "$msi_file" -opengl /qn" "70" "" ""

# Install GOG Galaxy
install_launcher "GOG Galaxy" "GogGalaxyLauncher" "$exe_file" "$exe_url" "$exe_file /silent" "71" "" "" true

# Install Ubisoft Connect
install_launcher "Ubisoft Connect" "UplayLauncher" "$ubi_file" "$ubi_url" "$ubi_file /S" "72" "" ""

# Install Battle.net
install_launcher "Battle.net" "Battle.netLauncher" "$battle_file" "$battle_url" "" "73" "" "" true

#Install Amazon Games
install_launcher "Amazon Games" "AmazonGamesLauncher" "$amazon_file" "$amazon_url" "" "74" "" "" true

#Install EA App
install_launcher "EA App" "TheEAappLauncher" "$eaapp_file" "$eaapp_url" "$eaapp_file /quiet" "75" "" "install_eaapp" true

# Install itch.io
install_launcher "itch.io" "itchioLauncher" "$itchio_file" "$itchio_url" "$itchio_file --silent" "76" "" "install_itchio" true

# Install Legacy Games
install_launcher "Legacy Games" "LegacyGamesLauncher" "$legacygames_file" "$legacygames_url" "$legacygames_file /S" "77" "" ""

# Install Humble Games
install_launcher "Humble Games Collection" "HumbleGamesLauncher" "$humblegames_file" "$humblegames_url" "" "78" "" "" true

# Install IndieGala
install_launcher "IndieGala" "IndieGalaLauncher" "$indiegala_file" "$indiegala_url" "$indiegala_file /S" "79" "" ""

# Install Rockstar Games Launcher
install_launcher "Rockstar Games Launcher" "RockstarGamesLauncher" "$rockstar_file" "$rockstar_url" "" "80" "" "" true

# Install Glyph Launcher
install_launcher "Glyph Launcher" "GlyphLauncher" "$glyph_file" "$glyph_url" "$glyph_file" "81" "" ""

# Install Minecraft Legacy Launcher
install_launcher "Minecraft Launcher" "MinecraftLauncher" "$minecraft_file" "$minecraft_url" "MsiExec.exe /i "$minecraft_file" /q" "82" "" ""

# Install Playstation Plus Launcher
install_launcher "Playstation Plus" "PlaystationPlusLauncher" "$psplus_file" "$psplus_url" "$psplus_file /q" "83" "" ""

# Install VK Play
install_launcher "VK Play" "VKPlayLauncher" "$vkplay_file" "$vkplay_url" "$vkplay_file" "84" "" "install_vkplay" true

# Install Hoyo Play
install_launcher "HoYoPlay" "HoYoPlayLauncher" "$hoyoplay_file" "$hoyoplay_url" "" "85" "" "install_hoyo" true

# Install Nexon Launcher
install_launcher "Nexon Launcher" "NexonLauncher" "$nexon_file" "$nexon_url" "$nexon_file" "86" "" "install_nexon" true

# Install GameJolt Launcher
install_launcher "Game Jolt Client" "GameJoltLauncher" "$gamejolt_file" "$gamejolt_url" "$gamejolt_file /silent" "67" "" ""

# Install artix Launcher
install_launcher "Artix Game Launcher" "ArtixGameLauncher" "$artixgame_file" "$artixgame_url" "$artixgame_file /S" "88" "" ""

# Install ARC Launcher
install_launcher "ARC Launcher" "ARCLauncher" "$arc_file" "$arc_url" "$arc_file" "89" "" "" true

# Install PokemonTCGLIVE
install_launcher "Pokémon Trading Card Game Live" "PokeTCGLauncher" "$poketcg_file" "$poketcg_url" "MsiExec.exe /i "$poketcg_file" /qn" "90" "" ""

# Install Antstream Arcade
install_launcher "Antstream Arcade" "AntstreamLauncher" "$antstream_file" "$antstream_url" "$antstream_file /quiet" "91" "" ""

# Install Purple Launcher
install_launcher "PURPLE Launcher" "PURPLELauncher" "$purple_file" "$purple_url" "$purple_file /S" "92" "" ""

# Install Plarium Launcher
install_launcher "Plarium Play" "PlariumLauncher" "$plarium_file" "$plarium_url" "$plarium_file /S" "93" "" ""

#Install VFUN Launcher
install_launcher "VFUN Launcher" "VFUNLauncher" "$vfun_file" "$vfun_url" "$vfun_file /S" "94" "" ""

#Install Tempo Launcher
install_launcher "Tempo Launcher" "TempoLauncher" "$tempo_file" "$tempo_url" "$tempo_file /S" "95" "" ""


#End of Launcher Installations

# Temporary fix for Epic
if [[ $options == *"Epic Games"* ]]; then

    function install_epic {

        pkill -f wineserver

        # Check if the first path exists, otherwise use the second one
        if [[ -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe" ]]; then
            echo "Starting first installation of Epic Games Launcher"
            "$STEAM_RUNTIME" "$proton_dir/proton" run "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe" &
            first_install_pid=$!
        elif [[ -f "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe" ]]; then
            echo "First path doesn't exist, trying the alternative path"
            "$STEAM_RUNTIME" "$proton_dir/proton" run "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe" &
            first_install_pid=$!
        else
            echo "Neither of the expected paths exist. Exiting."
            exit 1
        fi

        # Wait for the installation to complete
        wait $first_install_pid
        sleep 5

        # Rsync for syncing engine files (using logged_in_home)
        rsync -av --progress \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Update/Install/Engine/" \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Engine/"

        # Rsync for syncing portal files (using logged_in_home)
        rsync -av --progress \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Update/Install/Portal/" \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/"


        rsync -av --progress \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Update/Install/Engine/" \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Engine/"

        # Rsync for syncing portal files (using logged_in_home)
        rsync -av --progress \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/ProgramData/Epic/EpicGamesLauncher/Data/Update/Install/Portal/" \
          "${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/"

        # Download and run Epic Online Services installer
        eos_dir="${logged_in_home}/Downloads/NonSteamLaunchersInstallation"
        eos_file="${eos_dir}/EpicOnlineServicesInstaller.exe"
        eos_url="https://tinyurl.com/mt8bce8k"

        echo "Downloading Epic Online Services installer..."
        mkdir -p "$eos_dir"
        wget -L -O "$eos_file" "$eos_url"

        echo "Running Epic Online Services installer with Proton..."
        "$STEAM_RUNTIME" "$proton_dir/proton" run "$eos_file"
    }

    # Call the install_epic function
    install_epic
fi








echo "99"
echo "# Checking if Chrome is installed...please wait..."

# Check if user selected any of the options
if [[ $options == *"Apple TV+"* ]] || [[ $options == *"Plex"* ]] || [[ $options == *"Crunchyroll"* ]] || [[ $options == *"WebRcade"* ]] || [[ $options == *"WebRcade Editor"* ]] || [[ $options == *"Netflix"* ]] || [[ $options == *"Fortnite"* ]] || [[ $options == *"Venge"* ]] || [[ $options == *"Xbox Game Pass"* ]] || [[ $options == *"Better xCloud"* ]] || [[ $options == *"Geforce Now"* ]] || [[ $options == *"Boosteroid Cloud Gaming"* ]] || [[ $options == *"Amazon Luna"* ]] || [[ $options == *"Hulu"* ]] || [[ $options == *"Tubi"* ]] || [[ $options == *"Disney+"* ]] || [[ $options == *"Amazon Prime Video"* ]] || [[ $options == *"Youtube"* ]] || [[ $options == *"Youtube TV"* ]] || [[ $options == *"Twitch"* ]] || [[ $options == *"Stim.io"* ]] || [[ $options == *"WatchParty"* ]] || [[ $options == *"PokéRogue"* ]] || [[ $options == *"Afterplay.io"* ]] || [[ $options == *"OnePlay"* ]] || [[ $options == *"AirGPU"* ]] || [[ $options == *"CloudDeck"* ]] || [[ $options == *"JioGamesCloud"* ]]; then

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






echo "99.1"
echo "# Installing NVIDIA GeForce NOW (Native Linux) ...please wait..."

if flatpak info --user com.nvidia.geforcenow &>/dev/null || flatpak info --system com.nvidia.geforcenow &>/dev/null; then
    echo "NVIDIA GeForce NOW is already installed (user or system)."
else
    echo "Adding NVIDIA GeForce NOW Flatpak repository..."
    flatpak remote-add --user --if-not-exists GeForceNOW https://international.download.nvidia.com/GFNLinux/flatpak/geforcenow.flatpakrepo

    echo "Installing NVIDIA GeForce NOW Flatpak app (user scope)..."
    if flatpak install -y --user GeForceNOW com.nvidia.geforcenow; then
        echo "NVIDIA GeForce NOW installed successfully."
    else
        echo "Failed to install NVIDIA GeForce NOW."
    fi
fi

echo "99.2"
echo "# Checking if Ludusavi is installed...please wait..."

# AutoInstall Ludusavi
# Check if Ludusavi is already installed
if flatpak list | grep com.github.mtkennerly.ludusavi &> /dev/null; then
    echo "Ludusavi is already installed"
else
    # Check if the Flathub repository exists
    if flatpak remote-list | grep flathub &> /dev/null; then
        echo "Flathub repository exists"
    else
        # Add the Flathub repository
        flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
    fi

    # Install Ludusavi
    flatpak install --user flathub com.github.mtkennerly.ludusavi -y
fi

echo "Ludusavi installation script completed"

# Ensure Ludusavi is installed before proceeding
if ! flatpak list | grep com.github.mtkennerly.ludusavi &> /dev/null; then
    echo "Ludusavi installation failed. Exiting script."
fi


rclone_zip_url="https://downloads.rclone.org/rclone-current-linux-amd64.zip"
rclone_zip_file="${logged_in_home}/Downloads/NonSteamLaunchersInstallation/rclone-current-linux-amd64.zip"
rclone_base_dir="${logged_in_home}/Downloads/NonSteamLaunchersInstallation"
nsl_config_dir="${logged_in_home}/.var/app/com.github.mtkennerly.ludusavi/config/ludusavi/NSLconfig"

# Function to download and extract rclone
download_and_extract_rclone() {
    # Check if rclone already exists in the NSLconfig directory
    if [ -f "${nsl_config_dir}/rclone" ]; then
        echo "rclone already exists in ${nsl_config_dir}. Skipping download."
        return
    fi

    if [ -d "$rclone_base_dir" ]; then
        echo "Downloading rclone..."
        if ! wget -O "$rclone_zip_file" "$rclone_zip_url"; then
            echo "Failed to download rclone. Exiting script."
            exit 1
        fi

        echo "Extracting rclone..."
        if ! unzip -o "$rclone_zip_file" -d "$rclone_base_dir"; then
            echo "Failed to extract rclone. Exiting script."
            exit 1
        fi

        echo "rclone downloaded and extracted"
    else
        echo "Download directory does not exist. Exiting script."
        return
    fi

    # Find the extracted rclone directory dynamically
    rclone_extract_dir=$(find "$rclone_base_dir" -maxdepth 1 -type d -name "rclone-v*-linux-amd64" | head -n 1)
    rclone_bin="${rclone_extract_dir}/rclone"

    # Debug: Check if rclone_bin exists
    if [ -f "$rclone_bin" ]; then
        echo "rclone binary found at $rclone_bin"
    else
        echo "rclone binary not found at $rclone_bin. Exiting script."
        return
    fi

    # Ensure the NSLconfig directory exists
    mkdir -p "$nsl_config_dir"

    # Move rclone to the NSLconfig directory
    if [ -f "$rclone_bin" ]; then
        echo "Moving rclone to $nsl_config_dir"
        mv "$rclone_bin" "$nsl_config_dir"
        rclone_path="${nsl_config_dir}/rclone"
        echo "rclone moved to $nsl_config_dir"
    else
        echo "rclone binary not found. Exiting script."
    fi
}

# Run the function in a separate process
download_and_extract_rclone &
rclone_pid=$!
wait $rclone_pid

# Setting up Backup Saves through Ludusavi

# Define the directory and file path
config_dir="${logged_in_home}/.var/app/com.github.mtkennerly.ludusavi/config/ludusavi"
nsl_config_dir="$config_dir/NSLconfig"
backup_dir="$config_dir/config_backups"
timestamp=$(date +%m-%d-%Y_%H:%M:%S)
backup_config_file="$backup_dir/config.yaml.bak_$timestamp"

# Create the backup directory if it doesn't exist
mkdir -p "$backup_dir"

# Backup existing config.yaml if it exists
if [ -f "$config_dir/config.yaml" ]; then
    cp "$config_dir/config.yaml" "$backup_config_file"
    echo "Existing config.yaml backed up to $backup_config_file"
fi

# Create the NSLconfig directory if it doesn't exist
mkdir -p "$nsl_config_dir"

# Write the configuration to the NSLconfig file
cat <<EOL > "$nsl_config_dir/config.yaml"
---
runtime:
  threads: ~
release:
  check: true
manifest:
  enable: true
language: en-US
theme: light
roots:
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/UplayLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/itchioLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/GlyphLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlaystationPlusLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/VKPlayLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/HoYoPlayLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/NexonLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/GameJoltLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/ArtixGameLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/ARCLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/PokeTCGLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/MinecraftLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/AntstreamLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/PURPLELauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/PlariumLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/VFUNLauncher/pfx/drive_c/
  - store: otherWindows
    path: ${logged_in_home}/.local/share/Steam/steamapps/compatdata/TempoLauncher/pfx/drive_c/
redirects: []
backup:
  path: ${logged_in_home}/NSLGameSaves
  ignoredGames: []
  filter:
    excludeStoreScreenshots: false
    cloud:
      exclude: false
      epic: false
      gog: false
      origin: false
      steam: false
      uplay: false
    ignoredPaths: []
    ignoredRegistry: []
  toggledPaths: {}
  toggledRegistry: {}
  sort:
    key: status
    reversed: false
  retention:
    full: 1
    differential: 0
  format:
    chosen: simple
    zip:
      compression: deflate
    compression:
      deflate:
        level: 6
      bzip2:
        level: 6
      zstd:
        level: 10
restore:
  path: ${logged_in_home}/NSLGameSaves
  ignoredGames: []
  toggledPaths: {}
  toggledRegistry: {}
  sort:
    key: status
    reversed: false
scan:
  showDeselectedGames: true
  showUnchangedGames: true
  showUnscannedGames: true
cloud:
  remote: ~
  path: NSLGameSaves
  synchronize: true
apps:
  rclone:
    path: "${logged_in_home}/.var/app/com.github.mtkennerly.ludusavi/config/ludusavi/NSLconfig/rclone"
    arguments: "--fast-list --ignore-checksum"
customGames: []
EOL

# Run Once
echo "Running backup..."
nohup flatpak run com.github.mtkennerly.ludusavi --config "$nsl_config_dir" backup --force > /dev/null 2>&1 &
wait $!
echo "Backup completed"
# End of Ludusavi configuration



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
check_and_write "minecraft" "$minecraft_path1" "$minecraft_path2" "NonSteamLaunchers" "MinecraftLauncher" "" "minecraft_launcher"
check_and_write "psplus" "$psplus_path1" "$psplus_path2" "NonSteamLaunchers" "PlaystationPlusLauncher" "" "psplus_launcher"
check_and_write "vkplay" "$vkplay_path1" "$vkplay_path2" "NonSteamLaunchers" "VKPlayLauncher" "" "vkplay_launcher"
check_and_write "hoyoplay" "$hoyoplay_path1" "$hoyoplay_path2" "NonSteamLaunchers" "HoYoPlayLauncher" "" "hoyoplay_launcher"
check_and_write "nexon" "$nexon_path1" "$nexon_path2" "NonSteamLaunchers" "NexonLauncher" "" "nexon_launcher"
check_and_write "gamejolt" "$gamejolt_path1" "$gamejolt_path2" "NonSteamLaunchers" "GameJoltLauncher" "" "gamejolt_launcher"
check_and_write "artixgame" "$artixgame_path1" "$artixgame_path2" "NonSteamLaunchers" "ArtixGameLauncher" "" "artixgame_launcher"
check_and_write "arc" "$arc_path1" "$arc_path2" "NonSteamLaunchers" "ARCLauncher" "" "arc_launcher"
check_and_write "poketcg" "$poketcg_path1" "$poketcg_path2" "NonSteamLaunchers" "PokeTCGLauncher" "" "poketcg_launcher"
check_and_write "antstream" "$antstream_path1" "$antstream_path2" "NonSteamLaunchers" "AntstreamLauncher" "" "antstream_launcher"
check_and_write "purple" "$purple_path1" "$purple_path2" "NonSteamLaunchers" "PURPLELauncher" "" "purple_launcher"
check_and_write "plarium" "$plarium_path1" "$plarium_path2" "NonSteamLaunchers" "PlariumLauncher" "" "plarium_launcher"

check_and_write "vfun" "$vfun_path1" "$vfun_path2" "NonSteamLaunchers" "VFUNLauncher" "" "vfun_launcher"
check_and_write "tempo" "$tempo_path1" "$tempo_path2" "NonSteamLaunchers" "TempoLauncher" "" "tempo_launcher"

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
# Function to set Chrome launch options for a given service
set_chrome_launch_options() {
    local option_var="${1}chromelaunchoptions"
    local launch_options="run --branch=stable --arch=x86_64 --command=/app/bin/chrome --file-forwarding com.google.Chrome @@u @@ --window-size=1280,800 --force-device-scale-factor=1.00 --device-scale-factor=1.00 --start-fullscreen $2 --no-first-run --enable-features=OverlayScrollbar"

    # Write to environment variables file
    echo $option_var=$launch_options >> ${logged_in_home}/.config/systemd/user/env_vars
}

# Array of options, command names, and corresponding URLs
declare -A services=(
    ["Xbox Game Pass"]="xbox|https://www.xbox.com/play"
    ["WatchParty"]="watchparty|https://www.watchparty.me"
    ["Netflix"]="netflix|https://www.netflix.com"
    ["GeForce Now"]="geforce|https://play.geforcenow.com"
    ["Hulu"]="hulu|https://www.hulu.com/welcome"
    ["Tubi"]="tubi|https://tubitv.com"
    ["Disney+"]="disney|https://www.disneyplus.com"
    ["Amazon Prime Video"]="amazon|https://www.amazon.com/primevideo"
    ["Youtube"]="youtube|https://www.youtube.com"
    ["Youtube TV"]="youtubetv|https://youtube.com/tv"
    ["Amazon Luna"]="luna|https://luna.amazon.com"
    ["Twitch"]="twitch|https://www.twitch.tv"
    ["Fortnite"]="fortnite|https://www.xbox.com/en-US/play/games/fortnite/BT5P2X999VH2"
    ["Better xCloud"]="xcloud|https://better-xcloud.github.io"
    ["Venge"]="venge|https://venge.io"
    ["PokéRogue"]="pokerogue|https://pokerogue.net"
    ["Boosteroid Cloud Gaming"]="boosteroid|https://cloud.boosteroid.com"
    ["WebRcade"]="webrcade|https://play.webrcade.com"
    ["WebRcade Editor"]="webrcadeedit|https://editor.webrcade.com"
    ["Afterplay.io"]="afterplayio|https://afterplay.io/play/recently-played"
    ["OnePlay"]="oneplay|https://www.oneplay.in/dashboard/home"
    ["AirGPU"]="airgpu|https://app.airgpu.com"
    ["CloudDeck"]="clouddeck|https://clouddeck.app"
    ["JioGamesCloud"]="jio|https://cloudplay.jiogames.com"
    ["Plex"]="plex|https://www.plex.tv"
    ["Crunchyroll"]="crunchy|https://www.crunchyroll.com"
    ["Apple TV+"]="apple|https://tv.apple.com"
    ["Stim.io"]="stimio|https://stim.io"
    ["Rocketcrab"]="rocketcrab|https://rocketcrab.com"
)

# Check user selection and call the function for each option
for option in "${!services[@]}"; do
    if [[ $options == *"$option"* ]]; then
        IFS='|' read -r name url <<< "${services[$option]}"
        set_chrome_launch_options "$name" "$url"
    fi
done


# Check if any custom websites were provided
if [ ${#custom_websites[@]} -gt 0 ]; then
    echo "DEBUG: custom_websites array content: ${custom_websites[@]}"
    echo "DEBUG: custom_websites array length: ${#custom_websites[@]}"

    # Sanity check: try to split any single string containing commas into multiple array items
    if [ ${#custom_websites[@]} -eq 1 ] && [[ "${custom_websites[0]}" == *,* ]]; then
        IFS=',' read -ra custom_websites <<< "${custom_websites[0]}"
        echo "DEBUG: Re-split single comma string into array: ${custom_websites[@]}"
    fi

    # Strip leading/trailing whitespace from each website
    for i in "${!custom_websites[@]}"; do
        # Remove leading/trailing whitespace from each entry
        custom_websites[$i]=$(echo "${custom_websites[$i]}" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
    done

    # Join array with ', ' separator
    custom_websites_str=""
    for i in "${!custom_websites[@]}"; do
        if [ "$i" -gt 0 ]; then
            custom_websites_str+=", "
        fi
        custom_websites_str+="${custom_websites[$i]}"
    done

    echo "DEBUG: Final custom_websites_str = $custom_websites_str"

    # Export the properly formatted value to env_vars
    echo "export custom_websites_str=$custom_websites_str" >> "${logged_in_home}/.config/systemd/user/env_vars"
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

set +x

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









# Send Notes
if [[ $options == *"❤️"* ]]; then
    show_message "Sending any #nsl notes to the community!<3"

    # Check if steamid3 is not empty
    if [[ -n "$steamid3" ]]; then
        remote_dir="${logged_in_home}/.steam/root/userdata/${steamid3}/2371090/remote"
        echo "Searching directory: $remote_dir"

        # Create the remote directory if it doesn't exist
        mkdir -p "$remote_dir"
        echo "Directory $remote_dir is ready."

        # Check if the remote directory exists now
        if [[ -d "$remote_dir" ]]; then
            echo "Found matching remote directory: $remote_dir"
        else
            echo "Error: No matching remote directory found."
        fi
    else
        echo "Error: steamid3 variable is not set."
    fi

    # Path for the new "NSL Notes" folder
    nsl_notes_folder="$remote_dir/NSL Notes"
    echo "NSL Notes folder path: $nsl_notes_folder"

    # Create the "NSL Notes" folder if it doesn't exist
    echo "Creating NSL Notes folder if it doesn't exist..."
    mkdir -p "$nsl_notes_folder" > /dev/null 2>&1
    echo "NSL Notes folder created."

    # Output JSON file
    output_file="$nsl_notes_folder/nsl_notes_cache.json"
    echo "Output file will be: $output_file"

    # Initialize an empty array for collected data
    collected_notes="[]"
    note_count=0
    echo "Initializing collection of notes..."

    # Check if the file exists
    if [[ -f "$output_file" ]]; then
        # Read the existing data from the file (which should be a valid JSON array)
        collected_notes=$(<"$output_file")
    else
        # If the file doesn't exist, start with an empty array
        collected_notes="[]"
    fi

    # Loop through all files matching the pattern "notes_shortcut_*"
    echo "Processing notes_shortcut_* files..."
    for note_file in "$remote_dir"/notes_shortcut_*; do
        [[ -f "$note_file" ]] || continue  # Skip if it's not a regular file

        echo "Processing file: $note_file"

        # Read the content of the current file all at once
        data=$(<"$note_file")

        # Parse the JSON structure and iterate over "notes" array
        note_count_in_file=$(echo "$data" | jq '.notes | length')

        echo "Found $note_count_in_file notes in file $note_file."

        for i in $(seq 0 $((note_count_in_file - 1))); do
            echo "Processing note $i..."

            # Extract data for each note
            id=$(echo "$data" | jq -r ".notes[$i].id")
            shortcut_name=$(echo "$data" | jq -r ".notes[$i].shortcut_name")
            ordinal=0  # Ordinal is always 0
            time_created=$(echo "$data" | jq -r ".notes[$i].time_created")
            time_modified=$(echo "$data" | jq -r ".notes[$i].time_modified")
            title=$(echo "$data" | jq -r ".notes[$i].title")
            content=$(echo "$data" | jq -r ".notes[$i].content")

            echo "Processing note with ID: $id, Title: $title"

            # Skip if ID contains the word "note"
            [[ "$id" == *"note"* ]] && continue

            # Process only the entries with #nsl in the title
            [[ "$title" =~ "#nsl" ]] || continue

            # Clean the content by removing #nsl and HTML tags
            cleaned_content=$(echo "$content" | sed 's/#nsl//g' | sed 's/<[^>]*>//g')

            # Decode HTML entities (such as &amp; to &)
            cleaned_content=$(echo "$cleaned_content" | sed -e 's/&amp;/\&/g' -e 's/&lt;/</g' -e 's/&gt;/>/g' -e 's/&quot;/"/g' -e 's/&apos;/\'\''/g')

            # Get just the file name (without the full path)
            file_name=$(basename "$note_file")

            # Ensure Time Created and Time Modified are treated as integers
            time_created_int=$(echo "$time_created" | sed 's/^0*//')  # Remove leading zeros if any
            time_modified_int=$(echo "$time_modified" | sed 's/^0*//')  # Remove leading zeros if any

            # Add data to the collected_notes array (as a valid JSON object)
            collected_notes=$(echo "$collected_notes" | jq ". += [{
                \"ID\": \"$id\",
                \"Shortcut Name\": \"$shortcut_name\",
                \"Ordinal\": $ordinal,
                \"Time Created\": $time_created_int,
                \"Time Modified\": $time_modified_int,
                \"Title\": \"$title\",
                \"Content\": \"$cleaned_content\",
                \"File Name\": \"$file_name\"
            }]")

            # Increment the note count
            note_count=$((note_count + 1))
        done
    done

    # Write the updated collected_notes array to the output file (appending properly formatted JSON)
    echo "Writing collected notes to output file: $output_file"
    echo "$collected_notes" > "$output_file" 2>/dev/null

    # Send the collected data to the API
    echo "Sending collected data to API..."
    url="https://nslnotes.onrender.com/api/notes/"
    response=$(curl -s -w "%{http_code}" -o /dev/null -X POST -H "Content-Type: application/json" -d "$collected_notes" "$url")

    # Check if the request was successful
    if [[ "$response" == "200" ]]; then
        echo "$note_count notes successfully sent to the API."
    else
        echo "Failed to send data to the API. Status code: $response"
    fi

    show_message "#nsl notes have been sent :) looking for new ones!<3"
fi








#recieve noooooooooooootes
# Paths
proton_dir=$(find -L "${logged_in_home}/.steam/root/compatibilitytools.d" -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
CSV_FILE="$proton_dir/protonfixes/umu-database.csv"
echo "$CSV_FILE"
shortcuts_file="${logged_in_home}/.steam/root/userdata/${steamid3}/config/shortcuts.vdf"
output_dir="${logged_in_home}/.steam/root/userdata/${steamid3}/2371090/remote"
descriptions_file="${logged_in_home}/.config/systemd/user/descriptions.json"

# Function to get the current Unix timestamp
get_current_timestamp() {
    date +%s
}

# Function to validate JSON
validate_json() {
    local file_path="$1"
    if ! jq . "$file_path" > /dev/null 2>&1; then
        echo "Error: Invalid JSON in file $file_path"
        return 1
    fi
    return 0
}

# Function to URL encode a string (replace spaces with %20 and other special characters)
urlencode() {
    local raw="$1"
    echo -n "$raw" | jq -sRr @uri
}

# Function to read descriptions from a file
read_descriptions() {
    if [[ -f "$descriptions_file" ]]; then
        if ! validate_json "$descriptions_file"; then
            echo "Error: Invalid JSON in descriptions file $descriptions_file"
            return 1
        fi
        cat "$descriptions_file"
    else
        echo "Descriptions file does not exist, creating a new one."
        echo "[]" > "$descriptions_file"  # Create an empty JSON array
    fi
}

# Function to fetch all notes from the API at once
fetch_all_notes_from_api() {
    # Get the JSON response from the API
    response=$(curl -s "https://nslnotes.onrender.com/api/notes")

    # Check if the response is valid JSON
    if ! jq . <<< "$response" > /dev/null 2>&1; then
        echo "Error: Invalid JSON response from the API"
        return 1
    fi

    echo "$response"
}

# Function to update notes in the file for a game
update_notes_in_file() {
    local file_path="$1"
    local game_name="$2"
    local api_response="$3"  # All notes are passed in at once

    # Sanitize the game name (replace spaces with underscores, etc.)
    sanitized_game_name="$game_name"
    sanitized_game_name="${sanitized_game_name// /_}"
    sanitized_game_name="${sanitized_game_name//[^a-zA-Z0-9]/_}"

    # URL encode the sanitized game name
    encoded_game_name=$(urlencode "$sanitized_game_name")

    # Filter the notes to only get the ones for the current game using `jq`
    filtered_notes=$(echo "$api_response" | jq -r ".[] | select(.\"File Name\" == \"notes_shortcut_${encoded_game_name}\")")

    # If no notes are found for this game, exit early
    if [[ -z "$filtered_notes" ]]; then
        echo "No notes found for game $game_name"
        return
    fi

    # Start with an empty string to hold the formatted content for all notes
    nsl_content=""

    # Loop through the filtered notes for this game
    for note in $(echo "$filtered_notes" | jq -r '@base64'); do
        # Decode the note
        note_decoded=$(echo "$note" | base64 --decode)

        # Extract the relevant information for each note
        user=$(echo "$note_decoded" | jq -r '."user"')
        content=$(echo "$note_decoded" | jq -r '."Content"')
        time_created=$(echo "$note_decoded" | jq -r '."Time Created"')

        # Clean up content by replacing newline characters with <br> tags
        content_cleaned=$(echo "$content" | sed 's/\n/<br>/g')

        # Construct the content block for this note
        nsl_content+=$"[p][i]A note called \"$user\" says,[/i][/p][p][b]$content_cleaned[/b][/p][p]$time_created[/p][p][/p]"
    done

    # Generate the current timestamp
    local current_time=$(get_current_timestamp)

    # Get the game details from the CSV file
    game_details=$(grep -i "$game_name" "$CSV_FILE")

    # If no details are found, use default values for the game
    if [[ -z "$game_details" ]]; then
        game_details="N/A,N/A,N/A,N/A,N/A,N/A"
    fi

    # Loop through each matching result and print each field without colons
    echo "$game_details" | while IFS=',' read -r title store codename umu_id common_acronym note; do
        # Handle missing fields by replacing them with "N/A"
        title=${title:-N/A}
        store=${store:-N/A}
        codename=${codename:-N/A}
        umu_id=${umu_id:-N/A}
        common_acronym=${common_acronym:-N/A}
        note=${note:-N/A}

        # Construct the Proton-GE note with the game details
        proton_ge_content="[p]Title: $title[/p][p]Store: $store[/p][p]Codename: $codename[/p][p]UMU ID: $umu_id[/p][p]Common Acronym: $common_acronym[/p][p]Note: $note[/p]"

        # Construct the notes using jq (dynamically including the new Proton-GE content)
        local note_1=$(jq -n --arg shortcut_name "$game_name" --argjson time_created "$current_time" --arg proton_ge_content "$proton_ge_content" \
            '{"id":"note1675","shortcut_name":$shortcut_name,"ordinal":0,"time_created":$time_created,"time_modified":$time_created,"title":"Proton-GE & UMU","content":$proton_ge_content}')

        local note_2=$(jq -n --arg shortcut_name "$game_name" --argjson time_created "$current_time" --arg nsl_content "$nsl_content" \
            '{"id":"note2675","shortcut_name":$shortcut_name,"ordinal":0,"time_created":$time_created,"time_modified":$time_created,"title":"NSL Community Notes","content":$nsl_content}')

        # Read the descriptions from the JSON file
        descriptions=$(read_descriptions)

        # Find the description for the current game
        game_description=$(echo "$descriptions" | jq -r ".[] | select(.game_name == \"$game_name\") | .about_the_game")

        # Use a default description if none is found
        if [[ -z "$game_description" ]]; then
            game_description="No description found in the JSON file."
        fi

        #create a description note
        local note_3=$(jq -n --arg shortcut_name "$game_name" --argjson time_created "$current_time" --arg game_description "$game_description" \
            '{"id":"note3675","shortcut_name":$shortcut_name,"ordinal":0,"time_created":$time_created,"time_modified":$time_created,"title":"Game Description","content":$game_description}')

            # Check if the file exists and is valid
            if [[ -f "$file_path" ]]; then
                # Validate if the file contains valid JSON
                if validate_json "$file_path"; then
                    # Check if the file contains an array of notes
                    if jq -e '.notes | type == "array"' "$file_path" > /dev/null; then
                        # Replace the existing notes with the new ones on top
                        jq --argjson note1 "$note_1" --argjson note2 "$note_2" --argjson note3 "$note_3" \
                            '.notes = [$note1, $note2, $note3] + (.notes | map(select(.id != "note1675" and .id != "note2675" and .id != "note3675")))' \
                            "$file_path" > "$file_path.tmp" && mv "$file_path.tmp" "$file_path"
                        echo "Replaced Proton, NSL Community Notes, and Description Notes in $file_path"
                    else
                        echo "Error: The 'notes' field is not an array or is missing in $file_path."
                        return 1
                    fi
                else
                    echo "Invalid JSON. Skipping update."
                    return 1  # Exit if the JSON is invalid
                fi
            else
                # Create a new file with the notes structure if the file does not exist
                if jq -n --argjson note1 "$note_1" --argjson note2 "$note_2" --argjson note3 "$note_3" \
                    '{"notes":[$note1, $note2, $note3]}' > "$file_path"; then
                    echo "Created new file with notes: $file_path"
                else
                    echo "Error creating file: $file_path"
                    return 1  # Exit if the file creation fails
                fi
            fi
    done
}

# Function to list game names from the shortcuts file
list_game_names() {
    local skip_ext='\.(exe|sh|bat|msi|app|apk|url|desktop|appimage)$'

    if [[ ! -f "$shortcuts_file" ]]; then
        echo "No shortcuts.vdf found at $shortcuts_file"
        return 1
    fi

    echo "Reading game names from $shortcuts_file..."

    # Reset games array
    games=()

    # Parse shortcuts.vdf for appname entries
    mapfile -t lines < <(tr '\0\1\2' '\n\n\n' < "$shortcuts_file" | grep -v '^$')

    for ((i=0; i < ${#lines[@]} - 1; i++)); do
        if [[ "${lines[i],,}" == "appname" ]]; then
            local appname="${lines[i+1]}"
            # Trim whitespace
            appname="${appname#"${appname%%[![:space:]]*}"}"  # leading
            appname="${appname%"${appname##*[![:space:]]}"}"  # trailing

            # Skip if appname matches skip extensions (case-insensitive)
            if [[ -n "$appname" && ! "${appname,,}" =~ $skip_ext ]]; then
                games+=("$appname")
                echo "Added game: $appname"
            else
                echo "Skipped: $appname"
            fi
        fi
    done

    return 0
}

# Main process
echo "Starting script..."

# Fetch all notes from the API once
api_response=$(fetch_all_notes_from_api)
if [[ $? -ne 0 ]]; then
    echo "Failed to fetch all notes from the API"
    exit 1
fi

list_game_names  # Get the list of game names

# Loop over each game name
for game_name in "${games[@]}"; do
    # Create the file path for each game
    sanitized_game_name="$game_name"
    sanitized_game_name="${sanitized_game_name//\(/_}"
    sanitized_game_name="${sanitized_game_name//\)/_}"
    sanitized_game_name="${sanitized_game_name// /_}"
    sanitized_game_name="${sanitized_game_name//[^a-zA-Z0-9™]/_}"
    file_path="$output_dir/notes_shortcut_$sanitized_game_name"
    echo "Processing: $game_name (File: $file_path)"
    update_notes_in_file "$file_path" "$game_name" "$api_response"
done

echo "Notes execution complete."
show_message "Notes have been recieved!"
#noooooooooooooooootes










#set -x

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



# TODO: might be better to relocate temp files to `/tmp` or even use `mktemp -d` since `rm -rf` is potentially dangerous without the `-i` flag

# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf "$download_dir"



# Check if either directory does not exist
if [ "${deckyplugin}" = false ]; then
    # Function to display a Zenity message
    show_message() {
        zenity --notification --text="$1" --timeout=1
    }

    show_message "Activating Scanner..."

    # Setup NSLGameScanner.service
    python_script_path="${logged_in_home}/.config/systemd/user/NSLGameScanner.py"
    # Define your GitHub link
    github_link="https://raw.githubusercontent.com/moraroy/NonSteamLaunchers-On-Steam-Deck/main/NSLGameScanner.py"

    # Check if the service is already running
    service_status=$(systemctl --user is-active nslgamescanner.service)
    if [ "$service_status" = "active" ] || [ "$service_status" = "activating" ]; then
        echo "Service is already running or activating. Stopping the service..."
        systemctl --user stop nslgamescanner.service
    fi

    echo "Updating Python script from GitHub..."
    curl -o $python_script_path $github_link

    echo "Starting the service..."
    python3 $python_script_path

    show_message "Restarting Steam..."

    # Detach script from Steam process
    nohup sh -c 'sleep 10; /usr/bin/steam %U' &

    # Close all instances of Steam
    steam_pid() { pgrep -x steam ; }
    steam_running=$(steam_pid)
    [[ -n "$steam_running" ]] && killall steam

    # Wait for the steam process to exit
    while steam_pid > /dev/null; do
        sleep 5
    done
fi

show_message "Waiting to detect plugin..."
sleep 20




# Function to switch to Game Mode
switch_to_game_mode() {
  echo "Switching to Game Mode..."
  show_message "Switching to Game Mode..."
  rm -rf "$download_dir"
  echo "Removing user service..."
  rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service
  unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service
  echo "Reloading systemd user daemon..."
  systemctl --user daemon-reload
  echo "Logging out to complete Game Mode switch..."
  qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout
}

# Set the remote repository URL
REPO_URL="https://github.com/moraroy/NonSteamLaunchersDecky/archive/refs/heads/main.zip"

# Set the local directory path
LOCAL_DIR="${logged_in_home}/homebrew/plugins/NonSteamLaunchers"

# Function to check if a directory exists and contains files
directory_exists_and_not_empty() {
  [ -d "$1" ] && [ -n "$(ls -A "$1")" ]
}

# Function to fetch version from GitHub
fetch_github_version() {
    response=$(curl -s "https://raw.githubusercontent.com/moraroy/NonSteamLaunchersDecky/refs/heads/main/package.json")
    echo "$response" | jq -r '.version'
}

# Function to fetch local version from package.json
fetch_local_version() {
    if [ -f "$LOCAL_DIR/package.json" ]; then
        jq -r '.version' "$LOCAL_DIR/package.json"
    else
        echo "null"
    fi
}

# Function to compare versions
compare_versions() {
    local local_version=$(fetch_local_version)
    local github_version=$(fetch_github_version)

    echo "Fetched Local Version: $local_version"
    echo "Fetched GitHub Version: $github_version"

    if [ "$local_version" == "null" ]; then
        echo "Local version not found, need installation."
        return 1
    fi

    echo "Local Version: $local_version, GitHub Version: $github_version"
    if [ "$local_version" == "$github_version" ]; then
        echo "Plugin is up-to-date."
        return 0
    else
        echo "Update needed."
        return 1
    fi
}

# Function to check permissions for directories
check_permissions() {
    ls -ld "${logged_in_home}/homebrew" "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Function to adjust permissions temporarily to allow installation
adjust_permissions() {
    echo "Adjusting permissions for plugin directories..."
    chmod u+w "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Function to restore original permissions
restore_permissions() {
    echo "Restoring original permissions for plugin directories..."
    chmod u-w "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Main logic
set +x

show_message "Starting NSL Plugin installation/update script..."
echo "Detecting environment..."

# Check if Decky Loader exists
echo "Checking for Decky Loader..."
if ! directory_exists_and_not_empty "${logged_in_home}/homebrew/plugins"; then
  zenity --error --text="This is not an error. Decky Loader was not detected. Please install it from their website and re-run this script to access the plugin version of NSL."
fi

# Check if the NSL Plugin exists
echo "Checking if NSL Plugin already exists..."
if directory_exists_and_not_empty "$LOCAL_DIR"; then
  NSL_PLUGIN_EXISTS=true
  echo "NSL Plugin found at $LOCAL_DIR"
else
  NSL_PLUGIN_EXISTS=false
  echo "NSL Plugin not found."
fi

set +x
# Compare versions and update if necessary
echo "Comparing local and remote plugin versions..."
show_message "Checking for plugin updates..."
if compare_versions; then
  echo "No update needed. Plugin is already up-to-date."
  show_message "NSL Plugin is up-to-date."
else
  echo "Update required. Proceeding with update..."
  show_message "Updating NSL Plugin to the latest version..."

  # Remove existing plugin if it exists
  if $NSL_PLUGIN_EXISTS; then
    show_message "Removing existing plugin..."
    echo "Removing $LOCAL_DIR..."
    rm -rf "$LOCAL_DIR"
  fi

  # Adjust permissions before installation
  show_message "Creating base directory and setting permissions..."
  adjust_permissions

  echo "Creating plugin directory at $LOCAL_DIR"
  mkdir -p "$LOCAL_DIR"
  chmod -R u+rw "$LOCAL_DIR"
  chown -R $logged_in_user:$logged_in_user "$LOCAL_DIR"

  # Download, unzip, and copy the plugin files
  show_message "Downloading plugin from GitHub..."
  echo "Downloading plugin zip..."
  curl -L "$REPO_URL" -o /tmp/NonSteamLaunchersDecky.zip

  echo "Unzipping plugin..."
  unzip -o /tmp/NonSteamLaunchersDecky.zip -d /tmp/

  echo "Copying files to $LOCAL_DIR..."
  cp -r /tmp/NonSteamLaunchersDecky-main/* "$LOCAL_DIR"

  # Clean up temporary files
  echo "Cleaning up temporary files..."
  rm -rf /tmp/NonSteamLaunchersDecky*

  # Restore original permissions after installation
  restore_permissions

  set -x


  #Switch to Game Mode
  zenity --question --timeout=30 --text="NSL Plugin has been installed or updated. Do you want to switch to Game Mode now?"
  if [ $? -eq 0 ]; then
    show_message "Switching to Game Mode..."
    switch_to_game_mode
  else
    echo "User chose not to switch to Game Mode or timed out."
  fi
fi
















echo "Script completed successfully."



# Check if the symlink exists
if [ -L "${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service" ]; then
  # Symlink exists, show message
  show_message "Script finished...and the NSLGamesScanner is actively scanning!"
else
  # Symlink does not exist
  echo "Symlink does not exist."
fi

exit 0
