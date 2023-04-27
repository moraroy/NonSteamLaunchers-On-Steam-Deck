#!/bin/bash
set -x

# Create NonSteamGameInstallation subfolder in Downloads folder
mkdir -p ~/Downloads/NonSteamGameInstallation

# Check if all necessary files and folders are in place
if [ -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ] && [ -f "$msi_file" ] && [ -f "$exe_file" ] && [ -f "$ubi_file" ] && [ -f "$origin_file" ] && [ -f "$battle_file" ]; then
    echo "All files and folders are in place. No updates needed."
    exit 0
fi

# Set the path to the Proton directory
proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)

# Set the URLs to download GE-Proton from
ge_proton_url1=https://github.com/GloriousEggroll/proton-ge-custom/releases/latest/download/GE-Proton.tar.gz
ge_proton_url2=https://github.com/GloriousEggroll/proton-ge-custom/releases/download/GE-Proton7-55/GE-Proton7-55.tar.gz

# Check if GE-Proton is installed
if [ -z "$proton_dir" ]; then
    # Download GE-Proton using the first URL
    wget $ge_proton_url1 -O ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz

    # Check if the download succeeded
    if [ $? -ne 0 ]; then
        # Download GE-Proton using the second URL
        wget $ge_proton_url2 -O ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz
    fi

    # Check if either download succeeded
    if [ $? -eq 0 ]; then
        # Install GE-Proton
        tar -xvf ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz -C ~/.steam/root/compatibilitytools.d/
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
        wget $ge_proton_url1 -O ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz

        # Check if the download succeeded
        if [ $? -ne 0 ]; then
            # Download GE-Proton using the second URL
            wget $ge_proton_url2 -O ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz
        fi

        # Check if either download succeeded
        if [ $? -eq 0 ]; then
            # Install GE-Proton
            tar -xvf ~/Downloads/NonSteamGameInstallation/GE-Proton.tar.gz -C ~/.steam/root/compatibilitytools.d/
            proton_dir=$(find ~/.steam/root/compatibilitytools.d -maxdepth 1 -type d -name "GE-Proton*" | sort -V | tail -n1)
        else
            # Handle download failure
            echo "Failed to download GE-Proton"
        fi
    fi
fi

# Set the appid for the non-Steam game
appid=NonSteamLaunchers

# Set the URL to download the MSI file from
msi_url=https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi

# Set the path to save the MSI file to
msi_file=~/Downloads/NonSteamGameInstallation/EpicGamesLauncherInstaller.msi

# Set the URL to download the second file from
exe_url=https://webinstallers.gog-statics.com/download/GOG_Galaxy_2.0.exe

# Set the path to save the second file to
exe_file=~/Downloads/NonSteamGameInstallation/GOG_Galaxy_2.0.exe

# Set the URL to download the third file from
ubi_url=https://ubi.li/4vxt9

# Set the path to save the third file to
ubi_file=~/Downloads/NonSteamGameInstallation/UplayInstaller.exe

# Set the URL to download the fourth file from
origin_url=https://taskinoz.com/downloads/OriginSetup-10.5.119.52718.exe

# Set the path to save the fourth file to
origin_file=~/Downloads/NonSteamGameInstallation/OriginSetup-10.5.119.52718.exe

# Set the URL to download the fifth file from
battle_url=https://www.battle.net/download/getInstallerForGame?os=win

# Set the path to save the fifth file to
battle_file=~/Downloads/NonSteamGameInstallation/BattleNetInstaller.exe


# Download all files sequentially (if URLs and paths are set)
if [ ! -f "$msi_file" ]; then
    wget $msi_url -O $msi_file
fi
if [ ! -f "$exe_file" ]; then
    wget $exe_url -O $exe_file
fi
if [ ! -f "$ubi_file" ]; then
    wget $ubi_url -O $ubi_file
fi
if [ ! -f "$origin_file" ]; then
    wget $origin_url -O $origin_file
fi

if [ ! -f "$battle_file" ]; then
    wget $battle_url -O $battle_file
fi

# Create app id folder in compatdata folder if it doesn't exist
if [ ! -d "$HOME/.local/share/Steam/steamapps/compatdata/$appid" ]; then
    mkdir -p "$HOME/.local/share/Steam/steamapps/compatdata/$appid"
fi

# Change working directory to Proton's
cd $proton_dir

# Set the STEAM_COMPAT_CLIENT_INSTALL_PATH environment variable
export STEAM_COMPAT_CLIENT_INSTALL_PATH="~/.local/share/Steam"

# Set the STEAM_COMPAT_DATA_PATH environment variable for the first file
export STEAM_COMPAT_DATA_PATH=~/.local/share/Steam/steamapps/compatdata/$appid

# Run the MSI file using Proton with the /passive option
"$proton_dir/proton" run MsiExec.exe /i "$msi_file" /qn

# Wait for the first file to finish running before running the second file
wait

# Run the second file using Proton with the /passive option
"$proton_dir/proton" run "$ubi_file" /S

# Wait for the second file to finish running before running the third file
wait

# Run the third file using Proton with the /passive option
"$proton_dir/proton" run "$origin_file" /SILENT

# Edit local.xml
sed -i 's|</Settings>|    <Setting value="true" key="MigrationDisabled" type="1"/>\n    <Setting key="UpdateURL" value="" type="10"/>\n    <Setting key="AutoPatchGlobal" value="false" type="1"/>\n    <Setting key="AutoUpdate" value="false" type="1"/>\n</Settings>|' "$HOME/.local/share/Steam/steamapps/compatdata/$appid/pfx/drive_c/ProgramData/Origin/local.xml"

# Terminate any processes with the name Origin.exe
pkill Origin.exe

# Wait for the third file to finish running before running the fourth file
wait

# Run the fourth file using Proton without the /passive option
"$proton_dir/proton" run "$exe_file" &

# Wait for 5 seconds to give the GalaxySetup.tmp process time to start
sleep 90

# Cancel & Exit the GOG Galaxy Setup Wizard
pkill GalaxySetup.tmp

# Navigate to %LocalAppData%\Temp
cd "/home/deck/Desktop/compatdata/NonSteamLaunchers/pfx/drive_c/users/steamuser/Temp"

# Find the GalaxyInstaller_XXXXX folder and copy it to C:\Downloads
galaxy_installer_folder=$(find . -maxdepth 1 -type d -name "GalaxyInstaller_*" | head -n1)
cp -r "$galaxy_installer_folder" ~/Downloads/NonSteamGameInstallation/

# Navigate to the C:\Downloads\GalaxyInstaller_XXXXX folder
cd ~/Downloads/NonSteamGameInstallation/"$(basename $galaxy_installer_folder)"

# Run GalaxySetup.exe with the /VERYSILENT and /NORESTART options
"$proton_dir/proton" run GalaxySetup.exe /VERYSILENT /NORESTART

# Wait for the fourth file to finish running before running the fifth file
wait

# Run the fifth file using Proton with the /passive option
"$proton_dir/proton" run "$battle_file" Battle.net-Setup.exe --lang=enUS --installpath="C:\Program Files (x86)\Battle.net" &

sleep 90

pkill Battle.net.exe

# Delete NonSteamGameInstallation subfolder in Downloads folder
rm -rf ~/Downloads/NonSteamGameInstallation

echo "Script is fininshed"
exit

