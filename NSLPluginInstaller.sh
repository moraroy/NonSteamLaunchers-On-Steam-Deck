#!/bin/bash

# ENVIRONMENT VARIABLES
logged_in_user=$(logname 2>/dev/null || whoami)
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

# Ask the user if they want to install/update the plugin
user_input=$(zenity --question --text="Would you like to install or update the NonSteamLaunchers Decky Plugin?" --title="Install/Update Plugin" --ok-label="Yes" --cancel-label="No")

if [ $? -eq 1 ]; then
  echo "User canceled the installation/update."
  exit 0
fi

# Check if the Decky Loader and NSL Plugin exist
DECKY_LOADER_EXISTS=false
NSL_PLUGIN_EXISTS=false

if [ -d "${logged_in_home}/homebrew/plugins" ]; then
  DECKY_LOADER_EXISTS=true
fi

if [ -d "$LOCAL_DIR" ] && [ -n "$(ls -A $LOCAL_DIR)" ]; then
  NSL_PLUGIN_EXISTS=true
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
            return 1
        fi
    else
        return 1
    fi
}

# Function to compare versions
compare_versions() {
    if [ ! -d "$LOCAL_DIR" ] || [ ! -f "$LOCAL_DIR/package.json" ]; then
        return 1
    fi

    local_version=$(fetch_local_version)
    github_version=$(fetch_github_version)

    if [ "$local_version" == "Error:" ] || [ "$github_version" == "Error:" ]; then
        return 1
    fi

    if [ "$local_version" == "$github_version" ]; then
        return 0
    else
        return 1
    fi
}

# Check permissions for directories
check_permissions() {
    ls -ld "${logged_in_home}/homebrew" "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Adjust permissions temporarily to allow the installation
adjust_permissions() {
    chmod u+w "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Restore original permissions
restore_permissions() {
    chmod u-w "${logged_in_home}/homebrew/plugins" "${logged_in_home}/homebrew/plugins/NonSteamLaunchers"
}

# Main logic
set +x

check_permissions

if $DECKY_LOADER_EXISTS; then
  if ! $NSL_PLUGIN_EXISTS; then
    zenity --info --text="Decky Loader is detected but no NSL plugin found. It will now be injected into Game Mode."
  fi
else
  zenity --error --text="Decky Loader not found. Please install it and re-run the script."
  exit 1
fi

# Compare versions before proceeding with installation
compare_versions
if [ $? -eq 0 ]; then
  show_message "No update needed. The plugin is already up-to-date."
else
  local_version=$(fetch_local_version)
  github_version=$(fetch_github_version)

  show_update_message "$local_version" "$github_version"

  if $NSL_PLUGIN_EXISTS; then
    show_message "NSL Plugin detected. Deleting and updating..."
    rm -rf "$LOCAL_DIR"
  fi

  show_message "Creating base directory and setting permissions..."

  adjust_permissions

  mkdir -p "$LOCAL_DIR"
  chmod -R u+rw "$LOCAL_DIR"
  chown -R $logged_in_user:$logged_in_user "$LOCAL_DIR"

  curl -L "$REPO_URL" -o /tmp/NonSteamLaunchersDecky.zip
  unzip -o /tmp/NonSteamLaunchersDecky.zip -d /tmp/
  cp -r /tmp/NonSteamLaunchersDecky-main/* "$LOCAL_DIR"

  rm -rf /tmp/NonSteamLaunchersDecky*

  restore_permissions
fi

set -x
cd "$LOCAL_DIR"

show_message "Plugin installed. Switching to Game Mode..."
switch_to_game_mode
