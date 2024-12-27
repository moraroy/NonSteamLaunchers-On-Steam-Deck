#!/bin/bash

# ENVIRONMENT VARIABLES
# $USER
logged_in_user=$(logname 2>/dev/null || whoami)
# $HOME
logged_in_home=$(eval echo "~${logged_in_user}")

# Function to switch to Game Mode
switch_to_game_mode() {
  echo "Switching to Game Mode..."
  rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service
  unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service
  systemctl --user daemon-reload
  qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout
}

# Function to display a Zenity message
show_message() {
  zenity --notification --text="$1" --timeout=1
}

# Function to show the update message in Zenity notification
show_update_message() {
  zenity --notification --text="Updating from $1 to $2..." --timeout=5
}

# Set the remote repository URL
REPO_URL="https://github.com/moraroy/NonSteamLaunchersDecky/archive/refs/heads/main.zip"

# Set the local directory path
LOCAL_DIR="${logged_in_home}/homebrew/plugins/NonSteamLaunchers"

# Check if the Decky Loader and NSL Plugin exist
DECKY_LOADER_EXISTS=false
NSL_PLUGIN_EXISTS=false

if [ -d "${logged_in_home}/homebrew/plugins" ]; then
  DECKY_LOADER_EXISTS=true
fi

if [ -d "$LOCAL_DIR" ]; then
  if [ -z "$(ls -A $LOCAL_DIR)" ]; then
    NSL_PLUGIN_EXISTS=false
  else
    NSL_PLUGIN_EXISTS=true
  fi
fi

# Set version check variables
GITHUB_URL="https://raw.githubusercontent.com/moraroy/NonSteamLaunchersDecky/refs/heads/main/package.json"

# Function to fetch GitHub package.json
fetch_github_version() {
    response=$(curl -s "$GITHUB_URL")
    github_version=$(echo "$response" | jq -r '.version')

    if [ "$github_version" != "null" ]; then
        echo "$github_version"
    else
        echo "Error: Could not fetch or parse GitHub version"
        return 1
    fi
}

# Function to fetch the local package.json version
fetch_local_version() {
    if [ -f "$LOCAL_DIR/package.json" ]; then
        local_version=$(jq -r '.version' "$LOCAL_DIR/package.json")

        if [ "$local_version" != "null" ]; then
            echo "$local_version"
        else
            echo "Error: Failed to parse local version"
            return 1
        fi
    else
        echo "Error: Local package.json not found!"
        return 1
    fi
}

# Function to compare versions
compare_versions() {
    # Fetch local and GitHub versions
    local_version=$(fetch_local_version)
    github_version=$(fetch_github_version)

    if [ "$local_version" == "Error:" ] || [ "$github_version" == "Error:" ]; then
        echo "Error: Could not fetch version information"
        return 1
    fi

    echo "Local Version: $local_version, GitHub Version: $github_version"

    if [ "$local_version" == "$github_version" ]; then
        echo "Status: Up-to-date"
        return 0
    else
        echo "Status: Update available"
        return 1
    fi
}

set +x

if $DECKY_LOADER_EXISTS; then
  while true; do
    USER_INPUT=$(zenity --forms --title="Authentication Required" --text="Decky Loader detected! $(if $NSL_PLUGIN_EXISTS; then echo 'NSL Plugin also detected and will be updated to the latest version 🚀.'; else echo 'But no NSL plugin :( This is not an ERROR. Would you like to inject it and go to Game Mode?'; fi) Please enter your sudo password to proceed:" --separator="|" --add-password="Password")
    USER_PASSWORD=$(echo $USER_INPUT | cut -d'|' -f1)

    if [ -z "$USER_PASSWORD" ]; then
      zenity --error --text="No password entered. Exiting." --timeout=5
      exit 1
    fi

    echo "$USER_PASSWORD" | sudo -S echo "Password accepted" 2>/dev/null
    if [ $? -eq 0 ]; then
      break
    else
      zenity --error --text="Incorrect password. Please try again."
    fi
  done
else
  zenity --error --text="This is not an error but Decky Loader was not detected. Please download and install it from their website first and re-run this script to get the NSL Plugin."
  rm -rf "$download_dir"
  exit 1
fi

# Compare versions before proceeding with installation
compare_versions
if [ $? -eq 0 ]; then
  echo "No update needed. The plugin is already up-to-date."
  show_message "No update needed. The plugin is already up-to-date."
else
  # Get local and GitHub versions
  local_version=$(fetch_local_version)
  github_version=$(fetch_github_version)

  # Show update message in Zenity notification
  show_update_message "$local_version" "$github_version"

  if $NSL_PLUGIN_EXISTS; then
    show_message "NSL Plugin detected. Deleting and updating..."
    echo "Plugin directory exists. Removing..."
    echo "$USER_PASSWORD" | sudo -S rm -rf "$LOCAL_DIR"
  fi

  sudo systemctl stop plugin_loader.service

  show_message "Creating base directory and setting permissions..."
  echo "$USER_PASSWORD" | sudo -S mkdir -p "$LOCAL_DIR"
  echo "$USER_PASSWORD" | sudo -S chmod -R u+rw "$LOCAL_DIR"
  echo "$USER_PASSWORD" | sudo -S chown -R $USER:$USER "$LOCAL_DIR"

  echo "Downloading and extracting the repository..."
  curl -L "$REPO_URL" -o /tmp/NonSteamLaunchersDecky.zip
  echo "$USER_PASSWORD" | sudo -S unzip -o /tmp/NonSteamLaunchersDecky.zip -d /tmp/
  echo "$USER_PASSWORD" | sudo -S cp -r /tmp/NonSteamLaunchersDecky-main/* "$LOCAL_DIR"

  echo "$USER_PASSWORD" | sudo -S rm -rf /tmp/NonSteamLaunchersDecky*
fi

set -x
cd "$LOCAL_DIR"

show_message "Plugin installed. Switching to Game Mode..."
switch_to_game_mode

sudo systemctl restart plugin_loader.service
