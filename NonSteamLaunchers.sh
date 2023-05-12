#!/bin/bash

chmod +x "$0"

set -x

version=v2.5

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

check_for_updates






















# Set the paths to the launcher executables
epic_games_launcher_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
epic_games_launcher_path2="$HOME/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/pfx/drive_c/Program Files (x86)/Epic Games/Launcher/Portal/Binaries/Win32/EpicGamesLauncher.exe"
gog_galaxy_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
gog_galaxy_path2="$HOME/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/pfx/drive_c/Program Files (x86)/GOG Galaxy/GalaxyClient.exe"
origin_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Origin/Origin.exe"
origin_path2="$HOME/.local/share/Steam/steamapps/compatdata/OriginLauncher/pfx/drive_c/Program Files (x86)/Origin/Origin.exe"
uplay_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
uplay_path2="$HOME/.local/share/Steam/steamapps/compatdata/UplayLauncher/pfx/drive_c/Program Files (x86)/Ubisoft/Ubisoft Game Launcher/upc.exe"
battlenet_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
battlenet_path2="$HOME/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/pfx/drive_c/Program Files (x86)/Battle.net/Battle.net Launcher.exe"
eaapp_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
eaapp_path2="$HOME/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/pfx/drive_c/Program Files/Electronic Arts/EA Desktop/EA Desktop/EADesktop.exe"
amazongames_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
amazongames_path2="$HOME/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/pfx/drive_c/users/steamuser/AppData/Local/Amazon Games/App/Amazon Games.exe"
itchio_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/AppData/Local/itch/app-25.6.2/itch.exe"
itchio_path2="$HOME/.local/share/Steam/steamapps/compatdata/itchioLauncher/pfx/drive_c/users/steamuser/AppData/Local/itch/app-25.6.2/itch.exe"
legacygames_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
legacygames_path2="$HOME/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/pfx/drive_c/Program Files/Legacy Games/Legacy Games Launcher/Legacy Games Launcher.exe"
humblegames_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Humble App/Humble App.exe"
humblegames_path2="$HOME/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/pfx/drive_c/Program Files/Humble App/Humble App.exe"
indiegala_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/IGClient/IGClient.exe"
indiegala_path2="$HOME/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/pfx/drive_c/Program Files/IGClient/IGClient.exe"
rockstar_path1="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/Program Files/Rockstar Games/Launcher/Launcher.exe"
rockstar_path2="$HOME/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/pfx/drive_c/Program Files/Rockstar Games/Launcher/Launcher.exe"

function CheckInstallations {
# Check if Epic Games Launcher is installed
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
    epic_games_value="TRUE"
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
    gog_galaxy_value="TRUE"
    gog_galaxy_text="GOG Galaxy"
fi

# Check if Origin is installed
if [[ -f "$origin_path1" ]]; then
    # Origin is installed in path 1
    origin_value="FALSE"
    origin_text="Origin ===> $origin_path1"
elif [[ -f "$origin_path2" ]]; then
    # Origin is installed in path 2
    origin_value="FALSE"
    origin_text="Origin ===> $origin_path2"
else
    # Origin is not installed
    origin_value="TRUE"
    origin_text="Origin"
fi

# Check if Uplay is installed
if [[ -f "$uplay_path1" ]]; then
    # Uplay is installed in path 1
    uplay_value="FALSE"
    uplay_text="Uplay ===> $uplay_path1"
elif [[ -f "$uplay_path2" ]]; then
    # Uplay is installed in path 2
    uplay_value="FALSE"
    uplay_text="Uplay ===> $uplay_path2"
else
    # Uplay is not installed
    uplay_value="TRUE"
    uplay_text="Uplay"
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
    battlenet_value="TRUE"
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
    amazongames_value="TRUE"
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
    itchio_value="TRUE"
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
    legacygames_value="TRUE"
    legacygames_text="Legacy Games"
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
    humblegames_value="TRUE"
    humblegames_text="Humble Games Collection"
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
    indiegala_value="TRUE"
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
    rockstar_value="TRUE"
    rockstar_text="Rockstar Games Launcher"
fi }











function CheckInstallationDirectory {
    # Check if NonSteamLaunchers is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ]]; then
        # NonSteamLaunchers is installed
        nonsteamlauncher_move_value="TRUE"
    else
        # NonSteamLaunchers is not installed
        nonsteamlauncher_move_value="FALSE"
    fi

    # Check if EpicGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ]]; then
        # EpicGamesLauncher is installed
        epicgameslauncher_move_value="TRUE"
    else
        # EpicGamesLauncher is not installed
        epicgameslauncher_move_value="FALSE"
    fi

    # Check if GogGalaxyLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ]]; then
        # GogGalaxyLauncher is installed
        goggalaxylauncher_move_value="TRUE"
    else
        # GogGalaxyLauncher is not installed
        goggalaxylauncher_move_value="FALSE"
    fi

    # Check if OriginLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/OriginLauncher" ]]; then
        # OriginLauncher is installed
        originlauncher_move_value="TRUE"
    else
        # OriginLauncher is not installed
        originlauncher_move_value="FALSE"
    fi

    # Check if UplayLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/UplayLauncher" ]]; then
        # UplayLauncher is installed
        uplaylauncher_move_value="TRUE"
    else
        # UplayLauncher is not installed
        uplaylauncher_move_value="FALSE"
    fi

    # Check if Battle.netLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ]]; then
        # Battle.netLauncher is installed
        battlenetlauncher_move_value="TRUE"
    else
        # Battle.netLauncher is not installed
        battlenetlauncher_move_value="FALSE"
    fi

    # Check if TheEAappLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ]]; then
        # TheEAappLauncher is installed
        eaapplauncher_move_value="TRUE"
    else
        # TheEAappLauncher is not installed
        eaapplauncher_move_value="FALSE"
    fi


    # Check if AmazonGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ]]; then
        # AmazonGamesLauncher is installed
        amazongameslauncher_move_value="TRUE"
    else
        # AmazonGamesLauncher is not installed
        amazongameslauncher_move_value="FALSE"
    fi

    # Check if itchioLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/itchioLauncher" ]]; then
        # itchioLauncher is installed
        itchiolauncher_move_value="TRUE"
    else
        # itchioLauncher is not installed
        itchiolauncher_move_value="FALSE"
    fi

    # Check if LegacyGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ]]; then
        # LegacyGamesLauncher is installed
        legacygameslauncher_move_value="TRUE"
    else
        # LegacyGamesLauncher is not installed
        legacygameslauncher_move_value="FALSE"
    fi

    # Check if HumbleGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ]]; then
        # HumbleGamesLauncher is installed
        humblegameslauncher_move_value="TRUE"
    else
        # HumbleGamesLauncher is not installed
        humblegameslauncher_move_value="FALSE"
    fi

    # Check if indiegala is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ]]; then
        # indiegalaLauncher is installed
        indiegalalauncher_move_value="TRUE"
    else
        # indiegalaLauncher is not installed
        indiegalalauncher_move_value="FALSE"
    fi

    # Check if rockstar is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher" ]]; then
        # rockstar games launcher is installed
        rockstargameslauncher_move_value="TRUE"
    else
        # rockstar games launcher is not installed
        rockstargameslauncher_move_value="FALSE"
    fi }




# Check which app IDs are installed
CheckInstallations
CheckInstallationDirectory


# Display a list of options using zenity
options=$(zenity --list --text="Which launchers do you want to download and install?" --checklist --column="$version" --column="Default = one App ID Installation" FALSE "Separate App IDs" $epic_games_value "$epic_games_text" $gog_galaxy_value "$gog_galaxy_text" $uplay_value "$uplay_text" $origin_value "$origin_text" $battlenet_value "$battlenet_text" $amazongames_value "$amazongames_text" $eaapp_value "$eaapp_text" $legacygames_value "$legacygames_text" $itchio_value "$itchio_text" $humblegames_value "$humblegames_text" $indiegala_value "$indiegala_text" $rockstar_value "$rockstar_text" --width=435 --height=480  --extra-button="Start Fresh" --extra-button="Move to SD Card")

# Check if the cancel button was clicked
if [ $? -eq 1 ] && [[ $options != "Start Fresh" ]] && [[ $options != "Move to SD Card" ]]; then
    # The cancel button was clicked
    echo "The cancel button was clicked"
    exit 1
fi

# Check if no options were selected
if [ -z "$options" ]; then
    # No options were selected
    zenity --error --text="No options were selected. The script will now exit." --width=200 --height=150
    exit 1
fi

# Check if the user selected to use separate app IDs
if [[ $options == *"Separate App IDs"* ]]; then
    # User selected to use separate app IDs
    use_separate_appids=true
else
    # User did not select to use separate app IDs
    use_separate_appids=false
fi


# Check if the user selected both Origin and EA App
if [[ $options == *"Origin"* ]] && [[ $options == *"EA App"* ]] && [ "$use_separate_appids" = false ]; then
    # User selected both Origin and EA App without selecting separate app IDs
    zenity --error --text="You cannot select both Origin and EA App at the same time unless you select separate app IDs." --width=200 --height=150
    exit 1
fi

# Check if Origin is already installed
if [[ -f "$origin_path1" ]] || [[ -f "$origin_path2" ]]; then
    # Origin is installed
    if [[ $options == *"EA App"* ]] && [ "$use_separate_appids" = false ]; then
        # User selected EA App without selecting separate app IDs
        zenity --error --text="You cannot install EA App because Origin is already installed. Please select separate app IDs if you want to install both." --width=200 --height=150
        exit 1
    fi
fi

# Check if EA App is already installed
if [[ -f "$eaapp_path1" ]] || [[ -f "$eaapp_path2" ]]; then
    # EA App is installed
    if [[ $options == *"Origin"* ]] && [ "$use_separate_appids" = false ]; then
        # User selected Origin without selecting separate app IDs
        zenity --error --text="You cannot install Origin because EA App is already installed. Please select separate app IDs if you want to install both." --width=200 --height=150
        exit 1
    fi
fi


# Check if the Start Fresh button was clicked
if [[ $options == "Start Fresh" ]]; then
    # The Start Fresh button was clicked
    if zenity --question --text="aaahhh it always feels good to start fresh :) but...This will delete the App ID folders you installed inside the steamapps/compatdata/ directory. This means anything youve installed (launchers or games) WITH THIS SCRIPT ONLY will be deleted if you have them there. Are you sure?" --width=300 --height=260; then
        # The user clicked the "Yes" button
        # Add code here to delete the directories
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/OriginLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/UplayLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/Battle.netLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/TheEAappLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/itchioLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher"
        unlink & rm -rf "$HOME/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher"
        rm -rf "/run/media/mmcblk0p1/NonSteamLaunchers/"
        rm -rf "/run/media/mmcblk0p1/EpicGamesLauncher/"
        rm -rf "/run/media/mmcblk0p1/GogGalaxyLauncher/"
        rm -rf "/run/media/mmcblk0p1/OriginLauncher/"
        rm -rf "/run/media/mmcblk0p1/UplayLauncher/"
        rm -rf "/run/media/mmcblk0p1/Battle.netLauncher/"
        rm -rf "/run/media/mmcblk0p1/TheEAappLauncher/"
        rm -rf "/run/media/mmcblk0p1/AmazonGamesLauncher/"
        rm -rf "/run/media/mmcblk0p1/LegacyGamesLauncher/"
        rm -rf "/run/media/mmcblk0p1/itchioLauncher/"
        rm -rf "/run/media/mmcblk0p1/HumbleGamesLauncher/"
        rm -rf "/run/media/mmcblk0p1/IndieGalaLauncher/"
        rm -rf "/run/media/mmcblk0p1/RockstarGamesLauncher/"
        rm -rf ~/Downloads/NonSteamLaunchersInstallation

        # Exit the script
        exit 0
    else
        # The user clicked the "No" button
        # Add code here to exit the script
        exit 0
    fi
fi

if [[ $options == "Move to SD Card" ]]; then
    # The Move to SD Card button was clicked
    # Check which app IDs are installed

    # Add similar checks for other app IDs here
    CheckInstallationDirectory


    move_options=$(zenity --list --text="Which app IDs do you want to move to the SD card?" --checklist --column="Select" --column="App ID" $nonsteamlauncher_move_value "NonSteamLaunchers" $epicgameslauncher_move_value "EpicGamesLauncher" $goggalaxylauncher_move_value "GogGalaxyLauncher" $originlauncher_move_value "OriginLauncher" $uplaylauncher_move_value "UplayLauncher" $battlenetlauncher_move_value "Battle.netLauncher" $eaapplauncher_move_value "TheEAappLauncher" $amazongameslauncher_move_value "AmazonGamesLauncher" $itchiolauncher_move_value "itchioLauncher" $legacygameslauncher_move_value "LegacyGamesLauncher" $humblegameslauncher_move_value "HumbleGamesLauncher" $indiegalalauncher_move_value "IndieGalaLauncher" $rockstargameslauncher_move_value "RockstarGamesLauncher" --width=335 --height=470)

    # Check if the cancel button was clicked
    if [ $? -eq 0 ]; then
        # The OK button was clicked
        # Display a message to the user indicating that the operation was successful
        zenity --info --text="The selected directories have been moved to the SD card and symbolic links have been created." --width=200 --height=150
    fi

    # Set the path to the new directory on the SD card
    new_dir="/run/media/mmcblk0p1"


    # Check if NonSteamLaunchers is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers" ]]; then
    # NonSteamLaunchers is installed
    original_dir="$HOME/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers"
    else
    # NonSteamLaunchers is not installed
    original_dir=""
    fi

    # Check if the user selected to move NonSteamLaunchers
    if [[ $move_options == *"NonSteamLaunchers"* ]] && [[ -n $original_dir ]]; then
    # Move the NonSteamLaunchers directory to the SD card
    mv "$original_dir" "$new_dir/NonSteamLaunchers"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/NonSteamLaunchers" "$original_dir"
    fi

    # Check if EpicGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher" ]]; then
    # EpicGamesLauncher is installed
    original_dir="$HOME/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher"
    else
    # EpicGamesLauncher is not installed
    original_dir=""
    fi

    # Check if the user selected to move EpicGamesLauncher
    if [[ $move_options == *"EpicGamesLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the EpicGamesLauncher directory to the SD card
    mv "$original_dir" "$new_dir/EpicGamesLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/EpicGamesLauncher" "$original_dir"
    fi

    # Check if GogGalaxyLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher" ]]; then
    # GogGalaxyLauncher is installed
    original_dir="$HOME/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher"
    else
    # GogGalaxyLauncher is not installed
    original_dir=""
    fi

    # Check if the user selected to move GogGalaxyLauncher
    if [[ $move_options == *"GogGalaxyLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the GogGalaxyLauncher directory to the SD card
    mv "$original_dir" "$new_dir/GogGalaxyLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/GogGalaxyLauncher" "$original_dir"
    fi

    # Check if OriginLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/OriginLauncher" ]]; then
    # OriginLauncher is installed
    original_dir="$HOME/.local/share/Steam/steamapps/compatdata/OriginLauncher"
    else
    # OriginLauncher is not installed
    original_dir=""
    fi

    # Check if the user selected to move OriginLauncher
    if [[ $move_options == *"OriginLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the OriginLauncher directory to the SD card
    mv "$original_dir" "$new_dir/OriginLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/OriginLauncher" "$original_dir"
    fi

    # Check if UplayLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/UplayLauncher" ]]; then
    # UplayLauncher is installed
    original_dir="$HOME/.local/share/Steam/steamapps/compatdata/UplayLauncher"
    else
    # UplayLauncher is not installed
    original_dir=""
    fi

    # Check if the user selected to move UplayLauncher
    if [[ $move_options == *"UplayLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the UplayLauncher directory to the SD card
    mv "$original_dir" "$new_dir/UplayLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/UplayLauncher" "$original_dir"
    fi

    # Check if Battle.netLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/Battle.netLauncher" ]]; then
        # Battle.netLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/Battle.netLauncher"
    else
        # Battle.netLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move Battle.netLauncher
    if [[ $move_options == *"Battle.netLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the Battle.netLauncher directory to the SD card
        mv "$original_dir" "$new_dir/Battle.netLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/Battle.netLauncher" "$original_dir"
    fi

    # Check if TheEAappLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/TheEAappLauncher" ]]; then
        # TheEAappLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/TheEAappLauncher"
    else
        # TheEAappLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move TheEAappLauncher
    if [[ $move_options == *"TheEAappLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the TheEAappLauncher directory to the SD card
        mv "$original_dir" "$new_dir/TheEAappLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/TheEAappLauncher" "$original_dir"
    fi

    # Check if AmazonGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher" ]]; then
        # AmazonGamesLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher"
    else
        # AmazonGamesLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move AmazonGamesLauncher
    if [[ $move_options == *"AmazonGamesLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the AmazonGamesLauncher directory to the SD card
    mv "$original_dir" "$new_dir/AmazonGamesLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/AmazonGamesLauncher" "$original_dir"
    fi

    # Check if itchioLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/itchioLauncher" ]]; then
        # itchioLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/itchioLauncher"
    else
        # itchioLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move itchioLauncher
    if [[ $move_options == *"itchioLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the itchioLauncher directory to the SD card
        mv "$original_dir" "$new_dir/itchioLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/itchioLauncher" "$original_dir"
    fi

    # Check if LegacyGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher" ]]; then
        # LegacyGamesLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher"
    else
        # LegacyGamesLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move LegacyGamesLauncher
    if [[ $move_options == *"LegacyGamesLauncher"* ]] && [[ -n $original_dir ]]; then
    # Move the LegacyGamesLauncher directory to the SD card
    mv "$original_dir" "$new_dir/LegacyGamesLauncher"

    # Create a symbolic link to the new directory
    ln -s "$new_dir/LegacyGamesLauncher" "$original_dir"
    fi

    # Check if HumbleGamesLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher" ]]; then
        # HumbleGamesLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher"
    else
        # HumbleGamesLauncher is not installed
        original_dir=""
    fi

    # Check if the user selected to move HumbleGamesLauncher
    if [[ $move_options == *"HumbleGamesLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the HumbleGamesLauncher directory to the SD card
        mv "$original_dir" "$new_dir/HumbleGamesLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/HumbleGamesLauncher" "$original_dir"
    fi

    # Check if IndieGalaLauncher is installed
    if [[ -d "$HOME/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher" ]]; then
        # IndieGalaLauncher is installed
        original_dir="$HOME/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher"
    else
        # Indie Gala Launcher is not installed
        original_dir=""
    fi

    # Check if the user selected to move IndieGalaLauncher
    if [[ $move_options == *"IndieGalaLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the Indie GalaLauncher directory to the SD card
        mv "$original_dir" "$new_dir/IndieGalaLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/IndieGalaLauncher" "$original_dir"
    fi

    # Check if the user selected to move RockstarGamesLauncher
    if [[ $move_options == *"RockstarGamesLauncher"* ]] && [[ -n $original_dir ]]; then
        # Move the Rockstar Games Launcher directory to the SD card
        mv "$original_dir" "$new_dir/RockstarGamesLauncher"

        # Create a symbolic link to the new directory
        ln -s "$new_dir/RockstarGamesLauncher" "$original_dir"
    fi

    # Exit the script
    exit 1

fi


(



echo "0"
echo "# Detecting, Updating and Installing GE-Proton"

# check to make sure compatabilitytools.d exists and makes it if it doesnt
    if [ ! -d "$HOME/.steam/root/compatibilitytools.d" ]; then
    mkdir -p "$HOME/.steam/root/compatibilitytools.d"
fi






# Create NonSteamLaunchersInstallation subfolder in Downloads folder
mkdir -p ~/Downloads/NonSteamLaunchersInstallation

# Set the path to the Proton directory
proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

# Set the URLs to download GE-Proton from
ge_proton_url1=https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/GE-Proton.tar.gz
ge_proton_url2=https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton8-3/GE-Proton8-3.tar.gz





# Check if GE-Proton is installed
if [ -z "$proton_dir" ]; then
    # Download GE-Proton using the first URL
    echo "Downloading GE-Proton using the first URL"
    wget $ge_proton_url1 -O ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz

    # Check if the download succeeded
    if [ $? -ne 0 ]; then
        # Download GE-Proton using the second URL
        echo "Downloading GE-Proton using the second URL"
        wget $ge_proton_url2 -O ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz
    fi

    # Check if either download succeeded
    if [ $? -eq 0 ]; then
        # Install GE-Proton
        echo "Installing GE-Proton"
        tar -xvf ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz -C ~/.steam/root/compatibilitytools.d/
        proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
    else
        # Handle download failure
        echo "Failed to download GE-Proton"
    fi
else

# Check if installed version is the latest version
installed_version=$(basename $proton_dir | sed 's/GE-Proton-//')
    latest_version=$(curl -s https://api.github.com/repos/GloriousEggroll/proton-ge-custom/releases/latest | grep tag_name | cut -d '"' -f 4)
    if [ "$installed_version" != "$latest_version" ]; then
        # Download GE-Proton using the first URL
        echo "Downloading GE-Proton using the first URL"
        wget $ge_proton_url1 -O ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz

        # Check if the download succeeded
        if [ $? -ne 0 ]; then
            # Download GE-Proton using the second URL
            echo "Downloading GE-Proton using the second URL"
            wget $ge_proton_url2 -O ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz
        fi

        # Check if either download succeeded
        if [ $? -eq 0 ]; then
            # Install GE-Proton
            echo "Installing GE-Proton"
            tar -xvf ~/Downloads/NonSteamLaunchersInstallation/GE-Proton.tar.gz -C ~/.steam/root/compatibilitytools.d/
            proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
        else
            # Handle download failure
            echo "Failed to download GE-Proton"
        fi
    fi
fi




echo "10"
echo "# Setting files in their place"



# Set the appid for the non-Steam game
appid=NonSteamLaunchers

# Set the URL to download the MSI file from
msi_url=https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi

# Set the path to save the MSI file to
msi_file=~/Downloads/NonSteamLaunchersInstallation/EpicGamesLauncherInstaller.msi

# Set the URL to download the second file from
exe_url=https://webinstallers.gog-statics.com/download/GOG_Galaxy_2.0.exe

# Set the path to save the second file to
exe_file=~/Downloads/NonSteamLaunchersInstallation/GOG_Galaxy_2.0.exe

# Set the URL to download the third file from
ubi_url=https://ubi.li/4vxt9

# Set the path to save the third file to
ubi_file=~/Downloads/NonSteamLaunchersInstallation/UplayInstaller.exe

# Set the URL to download the fourth file from
origin_url=https://taskinoz.com/downloads/OriginSetup-10.5.119.52718.exe

# Set the path to save the fourth file to
origin_file=~/Downloads/NonSteamLaunchersInstallation/OriginSetup-10.5.119.52718.exe

# Set the URL to download the fifth file from
battle_url=https://www.battle.net/download/getInstallerForGame?os=win

# Set the path to save the fifth file to
battle_file=~/Downloads/NonSteamLaunchersInstallation/BattleNetInstaller.exe

# Set the URL to download the sixth file from
amazon_url=https://download.amazongames.com/AmazonGamesSetup.exe

# Set the path to save the sixth file to
amazon_file=~/Downloads/NonSteamLaunchersInstallation/AmazonGamesSetup.exe

# Set the URL to download the seventh file from
eaapp_url=https://origin-a.akamaihd.net/EA-Desktop-Client-Download/installer-releases/EAappInstaller.exe

# Set the path to save the seventh file to
eaapp_file=~/Downloads/NonSteamLaunchersInstallation/EAappInstaller.exe

# Set the URL to download the eighth file from
itchio_url=https://itch.io/app/download?platform=windows

# Set the path to save the eighth file to
itchio_file=~/Downloads/NonSteamLaunchersInstallation/itch-setup.exe

# Set the URL to download the ninth file from
legacygames_url=https://cdn.legacygames.com/LegacyGamesLauncher/legacy-games-launcher-setup-1.10.0-x64-full.exe

# Set the path to save the ninth file to
legacygames_file=~/Downloads/NonSteamLaunchersInstallation/legacy-games-launcher-setup-1.10.0-x64-full.exe

# Set the URL to download the tenth file from
humblegames_url=https://www.humblebundle.com/app/download

# Set the path to save the tenth file to
humblegames_file=~/Downloads/NonSteamLaunchersInstallation/Humble-App-Setup-1.1.8+411.exe

# Set the URL to download the eleventh file from
indiegala_url=https://content.indiegalacdn.com/common/IGClientSetup.exe

# Set the path to save the eleventh file to
indiegala_file=~/Downloads/NonSteamLaunchersInstallation/IGClientSetup.exe

# Set the URL to download the twelfth file from
rockstar_url=https://gamedownloads.rockstargames.com/public/installer/Rockstar-Games-Launcher.exe

# Set the path to save the twelfth file to
rockstar_file=~/Downloads/NonSteamLaunchersInstallation/Rockstar-Games-Launcher.exe




echo "20"
echo "# Creating files & folders"


# Create app id folder in compatdata folder if it doesn't exist and if the user selected to use a single app ID folder
if [ "$use_separate_appids" = false ] && [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
    mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
fi


# Change working directory to Proton's
cd $proton_dir

# Set the STEAM_RUNTIME environment variable
export STEAM_RUNTIME="$HOME/.steam/root/ubuntu12_32/steam-runtime/run.sh"


# Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

# Set the STEAM_COMPAT_DATA_PATH environment variable for the first file
export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid







wait
echo "30"
echo "# Downloading & Installing Epic Games...please wait..."

# Check if the user selected Epic Games Launcher
if [[ $options == *"Epic Games"* ]]; then
    # User selected Epic Games Launcher
    echo "User selected Epic Games"



    if [[ ! -f "$epic_games_launcher_path1" ]] && [[ ! -f "$epic_games_launcher_path2" ]]; then
        # Epic Games Launcher is not installed

        # Set the appid for the Epic Games Launcher
        if [ "$use_separate_appids" = true ]; then
        appid=EpicGamesLauncher
        else
        appid=NonSteamLaunchers
        fi


        # Create app id folder in compatdata folder if it doesn't exist
        if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
            mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
        fi

        # Change working directory to Proton's
        cd $proton_dir

        # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
        export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

        # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
        export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


        # Download MSI file
        if [ ! -f "$msi_file" ]; then
            echo "Downloading MSI file"
            wget $msi_url -O $msi_file
        fi

        # Run the MSI file using Proton with the /passive option
        echo "Running MSI file using Proton with the /passive option"
        "$STEAM_RUNTIME" "$proton_dir/proton" run MsiExec.exe /i "$msi_file" /qn


    fi
fi


# Wait for the MSI file to finish running
wait
echo "40"
echo "# Downloading & Installing Gog Galaxy...please wait..."


# Check if the user selected GOG Galaxy
if [[ $options == *"GOG Galaxy"* ]]; then
    # User selected GOG Galaxy
    echo "User selected GOG Galaxy"

    # Check if Gog Galaxy Launcher is already installed
    if [[ ! -f "$gog_galaxy_path1" ]] && [[ ! -f "$gog_galaxy_path2" ]]; then
        # Gog Galaxy Launcher is not installed

        # Set the appid for the Gog Galaxy 2.0
        if [ "$use_separate_appids" = true ]; then
            appid=GogGalaxyLauncher
        else
            appid=NonSteamLaunchers
        fi

        # Create app id folder in compatdata folder if it doesn't exist
        if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
            mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
        fi

        # Change working directory to Proton's
        cd $proton_dir

        # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
        export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

        # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
        export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid

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
        cd "$HOME/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/users/steamuser/Temp"

        # Find the GalaxyInstaller_XXXXX folder and copy it to C:\Downloads
        galaxy_installer_folder=$(find . -maxdepth 1 -type d -name "GalaxyInstaller_*" | head -n1)
        cp -r "$galaxy_installer_folder" ~/Downloads/NonSteamLaunchersInstallation/

        # Navigate to the C:\Downloads\GalaxyInstaller_XXXXX folder
        cd ~/Downloads/NonSteamLaunchersInstallation/"$(basename $galaxy_installer_folder)"

        # Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
        echo "Running GalaxySetup.exe with the /VERYSILENT and /NORESTART options"
        "$STEAM_RUNTIME" "$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART

        # Wait for the EXE file to finish running
        wait

    else
        # Gog Galaxy Launcher is already installed
        echo "Gog Galaxy Launcher is already installed"
    fi

fi



wait
echo "50"
echo "# Downloading & Installing Uplay ...please wait..."


# Check if user selected Uplay
if [[ $options == *"Uplay"* ]]; then
    # User selected Uplay
    echo "User selected Uplay"

    # Check if Uplay Launcher is installed
if [[ ! -f "$uplay_path1" ]] && [[ ! -f "$uplay_path2" ]]; then










    # Set the appid for the Ubisoft Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=UplayLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download UBI file
    if [ ! -f "$ubi_file" ]; then
        echo "Downloading UBI file"
        wget $ubi_url -O $ubi_file
    fi

  fi  # Run the UBI file using Proton with the /passive option
echo "Running UBI file using Proton with the /passive option"
"$STEAM_RUNTIME" "$proton_dir/proton" run "$ubi_file" /S
fi

# Wait for the UBI file to finish running
wait
echo "60"
echo "# Downloading & Installing Origin...please wait..."



# Check if user selected Origin
if [[ $options == *"Origin"* ]]; then
    # User selected Origin
    echo "User selected Origin"


    # Check if Origin Launcher is installed
    if [[ ! -f "$origin_path1" ]] && [[ ! -f "$origin_path2" ]]; then







    # Set the appid for the Origin Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=OriginLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download ORIGIN file
    if [ ! -f "$origin_file" ]; then
        echo "Downloading ORIGIN file"
        wget $origin_url -O $origin_file
    fi

    # Run the ORIGIN file using Proton with the /passive option
    echo "Running ORIGIN file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$origin_file" /SILENT

    # Edit local.xml
    sed -i 's|</Settings>|    <Setting value="true" key="MigrationDisabled" type="1"/>\n    <Setting key="UpdateURL" value="" type="10"/>\n    <Setting key="AutoPatchGlobal" value="false" type="1"/>\n    <Setting key="AutoUpdate" value="false" type="1"/>\n</Settings>|' "$HOME/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/ProgramData/Origin/local.xml"

    # Terminate any processes with the name Origin.exe
    pkill Origin.exe

    # Wait for the ORIGIN file to finish running
    wait
  fi
fi

wait
echo "70"
echo "# Downloading & Installing Battle.net...please wait..."

# Check if user selected Battle.net
if [[ $options == *"Battle.net"* ]]; then
    # User selected Battle.net
    echo "User selected Battle.net"

    # Check if Battlenet Launcher is installed
    if [[ ! -f "$battlenet_path1" ]] && [[ ! -f "$battlenet_path2" ]]; then



    # Set the appid for the Battlenet Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=Battle.netLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download BATTLE file
    if [ ! -f "$battle_file" ]; then
        echo "Downloading BATTLE file"
        wget $battle_url -O $battle_file
    fi

    # Run the BATTLE file using Proton with the /passive option
    echo "Running BATTLE file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net" &

    while true; do
    if pgrep -f "Battle.net.exe" > /dev/null; then
        pkill -f "Battle.net.exe"
        break
    fi
    sleep 1
done
    fi
fi



wait

echo "80"
echo "# Downloading & Installing Amazon Games...please wait..."

# Check if user selected Amazon Games
if [[ $options == *"Amazon Games"* ]]; then
    # User selected Amazon Games
    echo "User selected Amazon Games"

    # Check if Amazon Games Launcher is installed
    if [[ ! -f "$amazongames_path1" ]] && [[ ! -f "$amazongames_path2" ]]; then







    # Set the appid for the Amazon Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=AmazonGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Amazon Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download Amazon file
    if [ ! -f "$amazon_file" ]; then
        echo "Downloading Amazon file"
        wget $amazon_url -O $amazon_file
    fi


    # Run the Amazon file using Proton with the /passive option
    echo "Running Amazon file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$amazon_file" &


    while true; do
    if pgrep -f "Amazon Games.exe" > /dev/null; then
        pkill -f "Amazon Games.exe"
        break
    fi
    sleep 1
done
    fi
    # Wait for the Amazon file to finish running
    wait
fi





wait

echo "90"
echo "# Downloading & Installing EA App...please wait..."

# Check if user selected EA App
if [[ $options == *"EA App"* ]]; then
    # User selected EA App
    echo "User selected EA App"



    # Check if The EA App Launcher is installed
    if [[ ! -f "$eaapp_path1" ]] && [[ ! -f "$eaapp_path2" ]]; then







    # Set the appid for the EA App Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=TheEAappLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


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
fi

wait
echo "95"
echo "# Downloading & Installing itch.io...please wait..."

# Check if the user selected itchio Launcher
if [[ $options == *"itch.io"* ]]; then
    # User selected itchio Launcher
    echo "User selected itch.io"

    # Check if itchio Launcher is installed
    if [[ ! -f "$itchio_path1" ]] && [[ ! -f "$itchio_path2" ]]; then





    # Set the appid for the itchio Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=itchioLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download itchio file
    if [ ! -f "$itchio_file" ]; then
        echo "Downloading itchio file"
        wget $itchio_url -O $itchio_file
    fi

    # Run the itchio file using Proton with the /passive option
    echo "Running itchio file using Proton with the /passive option"
    "$STEAM_RUNTIME" "$proton_dir/proton" run "$itchio_file"
  fi
fi

wait
echo "98"
echo "# Downloading & Installing Legacy Games...please wait..."

# Check if user selected Legacy Games
if [[ $options == *"Legacy Games"* ]]; then
    # User selected Legacy Games
    echo "User selected Legacy Games"

    if [[ ! -f "$legacygames_path1" ]] && [[ ! -f "$legacygames_path2" ]]; then
        # Legacy Games Launcher is not installed





    # Set the appid for the Legacy Games Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=LegacyGamesLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download Legacy file
    if [ ! -f "$legacygames_file" ]; then
        echo "Downloading Legacy file"
        wget $legacygames_url -O $legacygames_file
    fi

      # Run the Legacy file using Proton with the /passive option
      echo "Running Legacy file using Proton with the /passive option"
      "$STEAM_RUNTIME" "$proton_dir/proton" run "$legacygames_file" /S
  fi
fi
# Wait for the Legacy file to finish running
wait


echo "99"
echo "# Downloading & Installing Humble Games Collection...please wait..."

# Check if the user selected Humble Games Launcher
if [[ $options == *"Humble Games Collection"* ]]; then
    # User selected Humble Games Launcher
    echo "User selected Humble Games Collection"



    if [[ ! -f "$humblegames_path1" ]] && [[ ! -f "$humblegames_path2" ]]; then
        # Humble Games Launcher is not installed

        # Set the appid for the Humble Games Launcher
        if [ "$use_separate_appids" = true ]; then
        appid=HumbleGamesLauncher
        else
        appid=NonSteamLaunchers
        fi


        # Create app id folder in compatdata folder if it doesn't exist
        if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
            mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
        fi

        # Change working directory to Proton's
        cd $proton_dir

        # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
        export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

        # Set the STEAM_COMPAT_DATA_PATH environment variable for Humble Games Launcher
        export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


        # Download exe file
        if [ ! -f "$humblegames_file" ]; then
            echo "Downloading MSI file"
            wget $humblegames_url -O $humblegames_file
        fi

        # Run the exe file using Proton with the /passive option
        echo "Running Exe file using Proton with the /passive option"
        "$STEAM_RUNTIME" "$proton_dir/proton" run "$humblegames_file" /S /D="C:\Program Files\Humble App"


    fi
fi


wait
echo "98"
echo "# Downloading & Installing Indie Gala...please wait..."

# Check if user selected indiegala
if [[ $options == *"IndieGala"* ]]; then
    # User selected indiegala
    echo "User selected IndieGala"

    if [[ ! -f "$indiegala_path1" ]] && [[ ! -f "$indiegala_path2" ]]; then
        # indiegala Launcher is not installed





    # Set the appid for the indiegala Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=IndieGalaLauncher
    else
        appid=NonSteamLaunchers
    fi

    # Create app id folder in compatdata folder if it doesn't exist
    if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
        mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
    fi

    # Change working directory to Proton's
    cd $proton_dir

    # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
    export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download indiegala file
    if [ ! -f "$indiegala_file" ]; then
        echo "Downloading indiegala file"
        wget $indiegala_url -O $indiegala_file
    fi

      # Run the indiegala file using Proton with the /passive option
      echo "Running IndieGala file using Proton with the /passive option"
      "$STEAM_RUNTIME" "$proton_dir/proton" run "$indiegala_file" /S
  fi
fi
# Wait for the Indie file to finish running
wait


echo "99"
echo "# Downloading & Installing Rockstar Games Launcher...please wait..."

# Check if user selected rockstar games launcher
if [[ $options == *"Rockstar Games Launcher"* ]]; then
    # User selected rockstar games
    echo "User selected Rockstar Games Launcher"

    if [[ ! -f "$rockstar_path1" ]] && [[ ! -f "$rockstar_path2" ]]; then
        # rockstar games Launcher is not installed

        # Set the appid for the indiegala Launcher
        if [ "$use_separate_appids" = true ]; then
            appid=RockstarGamesLauncher
        else
            appid=NonSteamLaunchers
        fi

        # Create app id folder in compatdata folder if it doesn't exist
        if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
            mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
        fi

        # Change working directory to Proton's
        cd $proton_dir

        # Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
        export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

        # Set the STEAM_COMPAT_DATA_PATH environment variable for Legacy Games Launcher
        export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid

        # Download rockstar games file
        if [ ! -f "$rockstar_file" ]; then
            echo "Downloading rockstar file"
            wget $rockstar_url -O $rockstar_file
        fi

          # Run the rockstar file using Proton with the /passive option
          echo "Running Rockstar Games Launcher file using Proton with the /passive option"
          "$STEAM_RUNTIME" "$proton_dir/proton" run "$rockstar_file"

    fi
fi
# Wait for the rockstar file to finish running
wait







# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf ~/Downloads/NonSteamLaunchersInstallation

echo "100"
echo "# Installation Complete - Steam will now restart. Your launchers will be in your library!...Food for thought...even Jedis use Force Compatability!"
) |
zenity --progress \
  --title="Update Status" \
  --text="Starting update...Please wait..." --width=450 --height=350\
  --percentage=0

if [ "$?" = -1 ] ; then
        zenity --error \
          --text="Update canceled."
fi

wait









#Checking Files For Shortcuts and Setting Directories For Shortcuts
if [[ -f "$epic_games_launcher_path1" ]]; then
    # Epic Games Launcher is installed at path 1
    epicshortcutdirectory="\"$epic_games_launcher_path1\""
    epiclaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$epic_games_launcher_path2" ]]; then
    # Epic Games Launcher is installed at path 2
    epicshortcutdirectory="\"$epic_games_launcher_path2\""
    epiclaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/EpicGamesLauncher/\" %command%"
fi
if [[ -f "$gog_galaxy_path1" ]]; then
    # Gog Galaxy Launcher is installed at path 1
    gogshortcutdirectory="\"$gog_galaxy_path1\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$gog_galaxy_path2" ]]; then
    # Gog Galaxy Launcher is installed at path 2
    gogshortcutdirectory="\"$gog_galaxy_path2\""
    goglaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/GogGalaxyLauncher/\" %command%"
fi
if [[ -f "$origin_path1" ]]; then
    # Origin Launcher is installed at path 1
    originshortcutdirectory="\"$origin_path1\""
    originlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$origin_path2" ]]; then
    # Origin Launcher is installed at path 2
    originshortcutdirectory="\"$origin_path2\""
    originlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/OriginLauncher/\" %command%"
fi
if [[ -f "$uplay_path1" ]]; then
    # Uplay Launcher is installed at path 1
    uplayshortcutdirectory="\"$uplay_path1\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$origin_path2" ]]; then
    # Uplay Launcher is installed at path 2
    uplayshortcutdirectory="\"$uplay_path2\""
    uplaylaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/UplayLauncher/\" %command%"
fi
if [[ -f "$battlenet_path1" ]]; then
    # Battlenet Launcher is installed at path 1
    battlenetshortcutdirectory="\"$battlenet_path1\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$battlenet_path2" ]]; then
    # Battlenet Launcher is installed at path 2
    battlenetshortcutdirectory="\"$battlenet_path2\""
    battlenetlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/Battle.netLauncher/\" %command%"
fi
if [[ -f "$eaapp_path1" ]]; then
    # EA App Launcher is installed at path 1
    eaappshortcutdirectory="\"$eaapp_path1\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$eaapp_path2" ]]; then
    # EA App Launcher is installed at path 2
    eaappshortcutdirectory="\"$eaapp_path2\""
    eaapplaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/TheEAappLauncher/\" %command%"
fi
if [[ -f "$amazongames_path1" ]]; then
    # Amazon Games Launcher is installed at path 1
    amazonshortcutdirectory="\"$amazongames_path1\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$amazongames_path2" ]]; then
    # Amazon Games Launcher is installed at path 2
    amazonshortcutdirectory="\"$amazongames_path2\""
    amazonlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/AmazonGamesLauncher/\" %command%"
fi
if [[ -f "$itchio_path1" ]]; then
    # itchio Launcher is installed at path 1
    itchioshortcutdirectory="\"$itchio_path1\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$itchio_path2" ]]; then
    # itchio Launcher is installed at path 2
    itchioshortcutdirectory="\"$itchio_path2\""
    itchiolaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/itchioLauncher/\" %command%"
fi
if [[ -f "$legacygames_path1" ]]; then
    # Legacy Games Launcher is installed at path 1
    legacyshortcutdirectory="\"$legacygames_path1\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$legacygames_path2" ]]; then
    # Legacy Games Launcher is installed at path 2
    legacyshortcutdirectory="\"$legacygames_path2\""
    legacylaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/LegacyGamesLauncher/\" %command%"
fi
if [[ -f "$humblegames_path1" ]]; then
    # Humble Games Launcher is installed at path 1
    humbleshortcutdirectory="\"$humblegames_path1\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$humblegames_path2" ]]; then
    # Humble Games Launcher is installed at path 2
    humbleshortcutdirectory="\"$humblegames_path2\""
    humblelaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/HumbleGamesLauncher/\" %command%"
fi
if [[ -f "$indiegala_path1" ]]; then
    # indiegala Launcher is installed at path 1
    indieshortcutdirectory="\"$indiegala_path1\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$indiegala_path2" ]]; then
    # indiegala Launcher is installed at path 2
    indieshortcutdirectory="\"$indiegala_path2\""
    indielaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/IndieGalaLauncher/\" %command%"
fi
if [[ -f "$rockstar_path1" ]]; then
    # rockstar Launcher is installed at path 1
    rockstarshortcutdirectory="\"$rockstar_path1\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/\" %command%"
elif [[ -f "$rockstar_path2" ]]; then
    # rockstar Launcher is installed at path 2
    rockstarshortcutdirectory="\"$rockstar_path2\""
    rockstarlaunchoptions="STEAM_COMPAT_DATA_PATH=\"/home/deck/.local/share/Steam/steamapps/compatdata/RockstarGamesLauncher/\" %command%"
fi










#VDF Library

# Set the download directory
download_dir=~/Downloads/NonSteamLaunchersInstallation

# Download the latest release of the vdf library from the Python Package Index
download_url="https://files.pythonhosted.org/packages/44/7f/74192f47d67c8bf3c47bf0d8487b3457614c2c98d58b6617721d217f3f79/vdf-3.4.tar.gz"

wget -P "$download_dir" "$download_url"

# Extract the downloaded tar.gz file
tar -xvf "$download_dir"/vdf-*.tar.gz -C "$download_dir"

#Setup Tools

# Download the latest release of setuptools from the Python Package Index
download_url="https://files.pythonhosted.org/packages/9b/be/13f54335c7dba713b0e97e11e7a41db3df4a85073d6c5a6e7f6468b22ee2/setuptools-60.2.0.tar.gz"

wget -P "$download_dir" "$download_url"

# Extract the downloaded tar.gz file
tar -xvf "$download_dir"/setuptools-*.tar.gz -C "$download_dir"

# Change to the extracted directory
cd "$download_dir"/setuptools-*/

# Add the installation directory to the PYTHONPATH environment variable
export PYTHONPATH="$download_dir/lib/python3.10/site-packages:$PYTHONPATH"

echo "$PYTHONPATH"

# Install setuptools
python setup.py install --prefix="$download_dir"

export PYTHONPATH="/usr/lib/python3.10/site-packages:$PYTHONPATH"

# Download extended-setup-tools from the provided URL
download_url="https://files.pythonhosted.org/packages/d2/a0/979ab67627f03da03eff3bc9d01c2969d89e33175764cdd5ec15a44efe50/extended-setup-tools-0.1.8.tar.gz"
wget -P "$download_dir" "$download_url"

# Extract the downloaded tar.gz file
tar -xvf "$download_dir"/extended-setup-tools-*.tar.gz -C "$download_dir"

# Change to the extracted directory
cd "$download_dir"/extended-setup-tools-*/

# Install extended-setup-tools
python setup.py install --prefix="$download_dir"

# Change to the extracted directory
cd "$download_dir"/vdf-*/

# Set the PYTHONPATH environment variable
export PYTHONPATH="$download_dir/lib/python3.10/site-packages:$PYTHONPATH"

# Install the vdf library
python setup.py install --prefix=~/Downloads/NonSteamLaunchersInstallation





# Initialize the userdata_folder variable
userdata_folder=""

# Initialize the most_recent variable
most_recent=0

# Loop through all the userdata folders
for USERDATA_FOLDER in ~/.steam/root/userdata/*
do
    # Check if the current userdata folder is not the "0" or "anonymous" folder
    if [[ "$USERDATA_FOLDER" != *"/0" ]] && [[ "$USERDATA_FOLDER" != *"/anonymous" ]]
    then
        # Get the access time of the current userdata folder
        access_time=$(stat -c %X "$USERDATA_FOLDER")

        # Check if the access time of the current userdata folder is more recent than the most recent access time
        if [[ $access_time -gt $most_recent ]]
        then
            # The access time of the current userdata folder is more recent
            # Set the userdata_folder variable
            userdata_folder="$USERDATA_FOLDER"

            # Update the most_recent variable
            most_recent=$access_time
        fi
    fi
done

# Check if the userdata folder was found
if [[ -n "$userdata_folder" ]]; then
    # The userdata folder was found
    echo "Current user's userdata folder found at: $userdata_folder"

    # Find the shortcuts.vdf file for the current user
    shortcuts_vdf_path=$(find "$userdata_folder" -type f -name shortcuts.vdf)

    # Check if shortcuts_vdf_path is not empty
    if [[ -n "$shortcuts_vdf_path" ]]; then
        # Create a backup of the shortcuts.vdf file
        cp "$shortcuts_vdf_path" "$shortcuts_vdf_path.bak"
    else
        # Find the config directory for the current user
        config_dir=$(find "$userdata_folder" -type d -name config)

        # Check if config_dir is not empty
        if [[ -n "$config_dir" ]]; then
            # Create a new shortcuts.vdf file at the expected location for the current user
            touch "$config_dir/shortcuts.vdf"
            shortcuts_vdf_path="$config_dir/shortcuts.vdf"
        else
            # Create a new config directory and a new shortcuts.vdf file at the expected location for the current user
            mkdir "$userdata_folder/config/"
            touch "$userdata_folder/config/shortcuts.vdf"
            config_dir="$userdata_folder/config/"
            shortcuts_vdf_path="$config_dir/shortcuts.vdf"
        fi
    fi

else
    # The userdata folder was not found
    echo "Current user's userdata folder not found"
fi














# Run the Python script to create a new entry for a Steam shortcut
python -c "
import vdf
import subprocess
import os


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
originshortcutdirectory = '$originshortcutdirectory'
uplayshortcutdirectory = '$uplayshortcutdirectory'
battlenetshortcutdirectory = '$battlenetshortcutdirectory'
eaappshortcutdirectory = '$eaappshortcutdirectory'
amazonshortcutdirectory = '$amazonshortcutdirectory'
itchioshortcutdirectory = '$itchioshortcutdirectory'
legacyshortcutdirectory = '$legacyshortcutdirectory'
humbleshortcutdirectory = '$humbleshortcutdirectory'
indieshortcutdirectory = '$indieshortcutdirectory'
rockstarshortcutdirectory = '$rockstarshortcutdirectory'

if epicshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Epic Games',
            'Exe': '$epicshortcutdirectory',
            'StartDir': '$epicshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$epiclaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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




if gogshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Gog Galaxy',
            'Exe': '$gogshortcutdirectory',
            'StartDir': '$gogshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$goglaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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








if uplayshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Ubisoft Connect',
            'Exe': '$uplayshortcutdirectory',
            'StartDir': '$uplayshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$uplaylaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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


if originshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Origin',
            'Exe': '$originshortcutdirectory',
            'StartDir': '$originshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$originlaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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


if battlenetshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Battle.net',
            'Exe': '$battlenetshortcutdirectory',
            'StartDir': '$battlenetshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$battlenetlaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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



if eaappshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'EA App',
            'Exe': '$eaappshortcutdirectory',
            'StartDir': '$eaappshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$eaapplaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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


if amazonshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Amazon Games',
            'Exe': '$amazonshortcutdirectory',
            'StartDir': '$amazonshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$amazonlaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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

if itchioshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'itch.io',
            'Exe': '$itchioshortcutdirectory',
            'StartDir': '$itchioshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$itchiolaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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


if legacyshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Legacy Games',
            'Exe': '$legacyshortcutdirectory',
            'StartDir': '$legacyshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$legacylaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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


if humbleshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Humble Games Collection',
            'Exe': '$humbleshortcutdirectory',
            'StartDir': '$humbleshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$humblelaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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



if indieshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'IndieGala',
            'Exe': '$indieshortcutdirectory',
            'StartDir': '$indieshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$indielaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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



if rockstarshortcutdirectory != '':
        # Create a new entry for the Steam shortcut
        new_entry = {
            'appid': '',
            'AppName': 'Rockstar Games Launcher',
            'Exe': '$rockstarshortcutdirectory',
            'StartDir': '$rockstarshortcutdirectory',
            'icon': '',
            'ShortcutPath': '',
            'LaunchOptions': '$rockstarlaunchoptions',
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
                entry.setdefault('AppName', '')
                entry.setdefault('Exe', '')
                if entry['AppName'] == new_entry['AppName'] and entry['Exe'] == new_entry['Exe']:
                    entry_exists = True
                    break
            if not entry_exists:
                shortcuts['shortcuts'].append(new_entry)
        elif type(shortcuts['shortcuts']) == dict:
            for key in shortcuts['shortcuts'].keys():
                shortcuts['shortcuts'][key].setdefault('AppName', '')
                shortcuts['shortcuts'][key].setdefault('Exe', '')
                if shortcuts['shortcuts'][key]['AppName'] == new_entry['AppName'] and shortcuts['shortcuts'][key]['Exe'] == new_entry['Exe']:
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












# Save the updated shortcuts dictionary to the shortcuts.vdf file
with open('$shortcuts_vdf_path', 'wb') as f:
    vdf.binary_dump(shortcuts, f)"







# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf ~/Downloads/NonSteamLaunchersInstallation


# Detach script from Steam process
nohup sh -c 'sleep 10; /usr/bin/steam' &

# Close all instances of Steam
killall steam

