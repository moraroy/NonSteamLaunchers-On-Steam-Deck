#!/bin/bash

logged_in_user=$(logname 2>/dev/null || whoami)
logged_in_home=$(eval echo "~${logged_in_user}")

PLUGIN_DIR="$logged_in_home/homebrew/plugins/SDH-GameThemeMusic"
BIN_DIR="${PLUGIN_DIR}/bin"
MAIN_PY_PATH="${PLUGIN_DIR}/main.py"
YTDLP_PATH="${BIN_DIR}/yt-dlp"

MAIN_PY_URL="https://raw.githubusercontent.com/moraroy/SDH-GameThemeMusic/main/main.py"
YTDLP_URL="https://github.com/yt-dlp/yt-dlp/releases/download/2025.09.26/yt-dlp"

switch_to_game_mode() {
  qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout
}

show_message() {
  zenity --notification --text="$1" --timeout=2
}

zenity --question --text="Do you want to patch the SDH-GameThemeMusic Decky Plugin?" \
  --title="Patch SDH_GameThemeMusic?" --ok-label="Yes" --cancel-label="No"
if [ $? -ne 0 ]; then
  show_message "Patch cancelled by user."
  exit 0
fi

password=$(zenity --password --title="Authentication Required")
if [ -z "$password" ]; then
  show_message "Authentication cancelled."
  exit 1
fi

if ! echo "$password" | sudo -S -v >/dev/null 2>&1; then
  zenity --error --text="Incorrect password or sudo access denied."
  exit 1
fi

if ! echo "$password" | sudo -S mkdir -p "$BIN_DIR"; then
  echo "Failed to create plugin directory $BIN_DIR"
  exit 1
fi

if ! echo "$password" | sudo -S test -d "$PLUGIN_DIR" || ! echo "$password" | sudo -S test -d "$BIN_DIR"; then
  echo "Plugin or bin directory does not exist after creation."
  exit 1
fi

echo "$password" | sudo -S chmod u+w "$PLUGIN_DIR" "$BIN_DIR" 2>/dev/null

echo "$password" | sudo -S rm -f "$MAIN_PY_PATH" "$YTDLP_PATH"

if ! curl -fsSL "$MAIN_PY_URL" -o "/tmp/main.py"; then
  show_message "Failed to download main.py"
  exit 1
fi

if ! curl -fsSL "$YTDLP_URL" -o "/tmp/yt-dlp"; then
  show_message "Failed to download yt-dlp binary"
  exit 1
fi

if ! echo "$password" | sudo -S mv /tmp/main.py "$MAIN_PY_PATH" || ! echo "$password" | sudo -S mv /tmp/yt-dlp "$YTDLP_PATH"; then
  echo "Failed to move new files into place."
  exit 1
fi

if ! echo "$password" | sudo -S test -f "$MAIN_PY_PATH" || ! echo "$password" | sudo -S test -f "$YTDLP_PATH"; then
  echo "One or both plugin files missing after move."
  exit 1
fi

echo "$password" | sudo -S chmod 644 "$MAIN_PY_PATH"
echo "$password" | sudo -S chmod 755 "$YTDLP_PATH"

echo "$password" | sudo -S chmod u-w "$PLUGIN_DIR" "$BIN_DIR" 2>/dev/null

zenity --notification --text="Patch completed successfully." --timeout=2

zenity --question --text="Plugin patched. Do you want to switch to Game Mode now? You may have to go to the Plugin Settings and Reload the SDH-GameThemeMusic plugin if it doesn't work at first." \
  --title="Switch to Game Mode?" --ok-label="Yes" --cancel-label="No"
if [ $? -eq 0 ]; then
  switch_to_game_mode
else
  show_message "Remaining in Desktop Mode."
fi
