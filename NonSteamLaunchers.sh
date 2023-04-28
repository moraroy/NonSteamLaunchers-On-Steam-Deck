#!/bin/bash
set -x
set -u

export WINEDEBUG=-all,err+all

# Display a list of options using zenity
options=$(zenity --list --text="Which installers do you want to download and install?" --checklist --column=":)" --column="The default is one App ID Installation" FALSE "Seperate App IDs" TRUE "Epic Games Launcher" TRUE "GOG Galaxy" TRUE "Uplay" TRUE "Origin" TRUE "Battle.net" FALSE "Amazon Games - broken" FALSE "EA App - broken" --width=400 --height=350)

# Check if the user selected both Origin and EA App
if [[ $options == *"Origin"* ]] && [[ $options == *"EA App"* ]]; then
    # User selected both Origin and EA App
    zenity --error --text="You cannot select both Origin and EA App at the same time." --width=200 --height=150
    exit 1
fi

# Check if the user selected to use separate app IDs
if [[ $options == *"Seperate App IDs"* ]]; then
    # User selected to use separate app IDs
    use_separate_appids=true
else
    # User did not select to use separate app IDs
    use_separate_appids=false
fi

(
echo "0"
echo "# Detecting and Installing GE-Proton"

# Create NonSteamLaunchersInstallation subfolder in Downloads folder
mkdir -p ~/Downloads/NonSteamLaunchersInstallation

# Set the path to the Proton directory
proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

# Set the URLs to download GE-Proton from
ge_proton_url1=https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/GE-Proton.tar.gz
ge_proton_url2=https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton7-55/GE-Proton7-55.tar.gz

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


echo "20"
echo "# Creating folders"


# Create app id folder in compatdata folder if it doesn't exist and if the user selected to use a single app ID folder
if [ "$use_separate_appids" = false ] && [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
    mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
fi


# Change working directory to Proton's
cd $proton_dir

# Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

# Set the STEAM_COMPAT_DATA_PATH environment variable for the first file
export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid

wait
echo "30"
echo "# Downloading/Installing Epic Games"

# Check if the user selected Epic Games Launcher
if [[ $options == *"Epic Games Launcher"* ]]; then
    # User selected Epic Games Launcher
    echo "User selected Epic Games Launcher"

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
"$proton_dir/proton" run MsiExec.exe /i "$msi_file" /qn
fi

# Wait for the MSI file to finish running
wait
echo "40"
echo "# Downloading/Installing Gog Galaxy"


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
    "$proton_dir/proton" run "$exe_file" &

    # Wait for 5 seconds to give the GalaxySetup.tmp process time to start
    sleep 90
echo "45"
echo "# Downloading/Installing Gog Galaxy"
    # Cancel & Exit the GOG Galaxy Setup Wizard
    pkill GalaxySetup.tmp

    # Navigate to %LocalAppData%\Temp
    cd "/home/deck/.local/share/Steam/steamapps/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/Temp"

    # Find the GalaxyInstaller_XXXXX folder and copy it to C:\Downloads
    galaxy_installer_folder=$(find . -maxdepth 1 -type d -name "GalaxyInstaller_*" | head -n1)
    cp -r "$galaxy_installer_folder" ~/Downloads/NonSteamLaunchersInstallation/

    # Navigate to the C:\Downloads\GalaxyInstaller_XXXXX folder
    cd ~/Downloads/NonSteamLaunchersInstallation/"$(basename $galaxy_installer_folder)"

    # Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
    echo "Running GalaxySetup.exe with the /VERYSILENT and /NORESTART options"
    "$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART

    # Wait for the EXE file to finish running
    wait
fi

wait
echo "50"
echo "# Downloading/Installing Uplay"


# Check if user selected Uplay
if [[ $options == *"Uplay"* ]]; then
    # User selected Uplay
    echo "User selected Uplay"

    # Set the appid for the Epic Games Launcher
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

    # Run the UBI file using Proton with the /passive option
echo "Running UBI file using Proton with the /passive option"
"$proton_dir/proton" run "$ubi_file" /S
fi

# Wait for the UBI file to finish running
wait
echo "60"
echo "# Downloading/Installing Origin"



# Check if user selected Origin
if [[ $options == *"Origin"* ]]; then
    # User selected Origin
    echo "User selected Origin"

    # Set the appid for the Epic Games Launcher
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
    "$proton_dir/proton" run "$origin_file" /SILENT

    # Edit local.xml
    sed -i 's|</Settings>|    <Setting value="true" key="MigrationDisabled" type="1"/>\n    <Setting key="UpdateURL" value="" type="10"/>\n    <Setting key="AutoPatchGlobal" value="false" type="1"/>\n    <Setting key="AutoUpdate" value="false" type="1"/>\n</Settings>|' "$HOME/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/ProgramData/Origin/local.xml"

    # Terminate any processes with the name Origin.exe
    pkill Origin.exe

    # Wait for the ORIGIN file to finish running
    wait
fi

wait
echo "70"
echo "# Downloading/Installing Battle.net"

# Check if user selected Battle.net
if [[ $options == *"Battle.net"* ]]; then
    # User selected Battle.net
    echo "User selected Battle.net"

    # Set the appid for the Epic Games Launcher
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
    "$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net" &

    sleep 90

    pkill Battle.net.exe
    pkill Battle.net Launcher.exe

fi

wait

echo "80"
echo "# Downloading/Installing Amazon Games"

# Check if user selected Amazon Games
if [[ $options == *"Amazon Games"* ]]; then
    # User selected Amazon Games
    echo "User selected Amazon Games"

    # Set the appid for the Epic Games Launcher
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

    # Set the STEAM_COMPAT_DATA_PATH environment variable for Epic Games Launcher
    export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid


    # Download Amazon file
    if [ ! -f "$amazon_file" ]; then
        echo "Downloading Amazon file"
        wget $amazon_url -O $amazon_file
    fi


    # Run the Amazon file using Proton with the /passive option
    echo "Running Amazon file using Proton with the /passive option"
    "$proton_dir/proton" run "$amazon_file" /qn

    # Wait for the Amazon file to finish running
    wait
fi

wait

echo "90"
echo "# Downloading/Installing EA App"

# Check if user selected EA App
if [[ $options == *"EA App"* ]]; then
    # User selected EA App
    echo "User selected EA App"


    # Set the appid for the EA App Launcher
    if [ "$use_separate_appids" = true ]; then
        appid=TheEAAPPLauncher
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
    "$proton_dir/proton" run "$eaapp_file"

    # Wait for the EA App file to finish running
    wait
fi

wait

# Delete NonSteamLaunchersInstallation subfolder in Downloads folder
rm -rf ~/Downloads/NonSteamLaunchersInstallation

echo "100"
echo "# Script is finished - you may close all windows"
) |
zenity --progress \
  --title="Update Status" \
  --text="Starting update..." --width=400 --height=350\
  --percentage=0

if [ "$?" = -1 ] ; then
        zenity --error \
          --text="Update canceled."
fi

exit
