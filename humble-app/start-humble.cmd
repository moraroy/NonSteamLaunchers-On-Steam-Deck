@echo off

cd /d "C:\Program Files\Humble App\"
set /p Url=<"C:\.auth"

if defined Url (
    start "" "Humble App.exe" "%Url%"
) else (
    start "" "Humble App.exe" "%*"
)

exit