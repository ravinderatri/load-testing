# Define Installer Name
Outfile "Load-Testing-Installer.exe"

# Set Installation Directory
InstallDir "$PROGRAMFILES\Load-Testing"

# Request admin rights for installation
RequestExecutionLevel admin

# Default Install Section
Section "Install"

    # Create Installation Directory
    SetOutPath "$INSTDIR"

    # Copy EXE File
    File "dist\Load-Testing.exe"

    # Create Start Menu Shortcut
    CreateShortcut "$SMPROGRAMS\Load-Testing.lnk" "$INSTDIR\Load-Testing.exe"

    # Create Desktop Shortcut
    CreateShortcut "$DESKTOP\Load-Testing.lnk" "$INSTDIR\Load-Testing.exe"

    # Write Uninstaller to Installation Directory
    WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

# Uninstall Section
Section "Uninstall"

    # Remove Installed Files
    Delete "$INSTDIR\Load-Testing.exe"
    Delete "$INSTDIR\Uninstall.exe"

    # Remove Shortcuts
    Delete "$SMPROGRAMS\Load-Testing.lnk"
    Delete "$DESKTOP\Load-Testing.lnk"

    # Remove Installation Directory
    RMDir "$INSTDIR"

SectionEnd
