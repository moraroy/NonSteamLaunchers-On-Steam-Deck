#!/bin/bash

# ENVIRONMENT VARIABLES
# $USER
logged_in_user=$(logname 2>/dev/null || whoami)
# $HOME
logged_in_home=$(eval echo "~${logged_in_user}")

# Function to switch to Game Mode
switch_to_game_mode() {
  echo "Switching to Game Mode..."
  rm -rf "$download_dir"
  rm -rf ${logged_in_home}/.config/systemd/user/nslgamescanner.service
  unlink ${logged_in_home}/.config/systemd/user/default.target.wants/nslgamescanner.service
  systemctl --user daemon-reload
  qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout
}

# Function to display a Zenity message
show_message() {
  zenity --notification --text="$1" --timeout=1
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

set +x

if $DECKY_LOADER_EXISTS; then
  USER_INPUT=$(zenity --forms --title="Authentication Required" --text="Decky Loader detected! $(if $NSL_PLUGIN_EXISTS; then echo 'NSL Plugin also detected and will be updated to the latest version 🚀.'; else echo 'But no NSL plugin :(. Would you like to inject it and go to Game Mode?
  '; fi) Please enter your password to proceed:" --separator="|" --add-password="Password")
else
  zenity --error --text="Decky Loader not detected. Please download and install it from their website first and re-run this script to get the NSL Plugin."
  rm -rf "$download_dir"
  exit 1
fi

USER_PASSWORD=$(echo $USER_INPUT | cut -d'|' -f1)

if [ -z "$USER_PASSWORD" ]; then
  zenity --error --text="No password entered. Exiting."
  exit 1
fi

if $NSL_PLUGIN_EXISTS; then
  show_message "NSL Plugin detected. Deleting and updating..."
  echo "Plugin directory exists. Removing..."
  echo "$USER_PASSWORD" | sudo -S rm -rf "$LOCAL_DIR"
fi

show_message "Creating base directory and setting permissions..."
echo "$USER_PASSWORD" | sudo -S mkdir -p "$LOCAL_DIR"
echo "$USER_PASSWORD" | sudo -S chmod -R u+rw "$LOCAL_DIR"
echo "$USER_PASSWORD" | sudo -S chown -R $USER:$USER "$LOCAL_DIR"

echo "Downloading and extracting the repository..."
curl -L "$REPO_URL" -o /tmp/NonSteamLaunchersDecky.zip
echo "$USER_PASSWORD" | sudo -S unzip -o /tmp/NonSteamLaunchersDecky.zip -d /tmp/
echo "$USER_PASSWORD" | sudo -S cp -r /tmp/NonSteamLaunchersDecky-main/* "$LOCAL_DIR"


echo "$USER_PASSWORD" | sudo -S rm -rf /tmp/NonSteamLaunchersDecky*

set -x
cd "$LOCAL_DIR"

show_message "Plugin installed. Switching to Game Mode..."
switch_to_game_mode

sudo systemctl restart plugin_loader.service

