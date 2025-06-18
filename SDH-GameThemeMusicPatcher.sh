#!/bin/bash

logged_in_user=$(logname 2>/dev/null || whoami)
logged_in_home=$(eval echo "~${logged_in_user}")

PLUGIN_DIR="${logged_in_home}/homebrew/plugins/SDH-GameThemeMusic"
BIN_DIR="${PLUGIN_DIR}/bin"
MAIN_PY_PATH="${PLUGIN_DIR}/main.py"
YTDLP_PATH="${BIN_DIR}/yt-dlp"

MAIN_PY_URL="https://raw.githubusercontent.com/moraroy/SDH-GameThemeMusic/main/main.py"
YTDLP_URL="https://github.com/yt-dlp/yt-dlp/releases/download/2025.06.09/yt-dlp"

switch_to_game_mode() {
  qdbus org.kde.Shutdown /Shutdown org.kde.Shutdown.logout
}

show_message() {
  zenity --notification --text="$1" --timeout=2
}

zenity --question --text="Do you want to patch the SDH-GameThemeMusic Decky Plugin?" \
  --title="Patch SDH_GameThemeMusic?" --ok-label="Yes" --cancel-label="No"
patch_answer=$?

if [ "$patch_answer" -ne 0 ]; then
  show_message "Patch cancelled by user."
  exit 0
fi

mkdir -p "$BIN_DIR"
chmod u+w "$PLUGIN_DIR" "$BIN_DIR" 2>/dev/null || true
chmod u+w "$MAIN_PY_PATH" "$YTDLP_PATH" 2>/dev/null || true

rm -f "$MAIN_PY_PATH" "$YTDLP_PATH"

curl -fsSL "$MAIN_PY_URL" -o "$MAIN_PY_PATH" || { show_message "Failed to download main.py"; exit 1; }
curl -fsSL "$YTDLP_URL" -o "$YTDLP_PATH" || { show_message "Failed to download yt-dlp binary"; exit 1; }

chmod 644 "$MAIN_PY_PATH"
chmod 755 "$YTDLP_PATH"
chmod u-w "$PLUGIN_DIR" "$BIN_DIR" 2>/dev/null || true

# Removed sudo password and service restart logic here

zenity --question --text="Plugin installed or updated. Do you want to switch to Game Mode now? You may have to go to the Plugin Settings and Reload the SDH-GameThemeMusic plugin if it doesnt work at first." \
  --title="Switch to Game Mode?" --ok-label="Yes" --cancel-label="No"
zenity_exit_code=$?

if [ "$zenity_exit_code" -eq 0 ]; then
  switch_to_game_mode
else
  show_message "Remaining in Desktop Mode."
fi
