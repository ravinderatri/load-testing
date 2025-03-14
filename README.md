# Load-Testing Tool

This is a Python-based API load-testing tool with a GUI built using Tkinter. It allows users to send multiple concurrent requests to APIs and log results.

---

## **Installation Instructions**

### **1. Requirements**
- Python 3.8 or later
- pip (Python package manager)
- Windows, macOS, or Linux system

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

## **Building Executables for Windows, macOS, and Linux**

### **Windows (NSIS Installer & Standalone EXE)**

#### **Option 1: Generate Standalone EXE**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=Load-Testing ui.py
```
The generated EXE will be inside the `dist/` folder.

#### **Option 2: Create an NSIS Installer**
1. Install **NSIS** from [nsis.sourceforge.io](https://nsis.sourceforge.io)
2. Create an `installer.nsi` file:

```nsis
OutFile "Load-Testing-Installer.exe"
InstallDir "$PROGRAMFILES\Load-Testing"
Section "Install"
    SetOutPath "$INSTDIR"
    File "dist/Load-Testing.exe"
    CreateShortcut "$SMPROGRAMS\Load-Testing.lnk" "$INSTDIR\Load-Testing.exe"
    CreateShortcut "$DESKTOP\Load-Testing.lnk" "$INSTDIR\Load-Testing.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\Load-Testing.exe"
    Delete "$SMPROGRAMS\Load-Testing.lnk"
    Delete "$DESKTOP\Load-Testing.lnk"
    RMDir "$INSTDIR"
SectionEnd
```
3. Compile the installer:
```bash
makensis installer.nsi
```
The installer EXE will be generated.

---

### **macOS (Create .app and .dmg)**

#### **Option 1: Generate .app**
```bash
pip install py2app
python setup.py py2app
```
The generated `.app` file will be inside the `dist/` folder.

#### **Option 2: Create a .dmg Installer**
```bash
npm install -g create-dmg
create-dmg "dist/Load-Testing.app" "dist/" --overwrite --dmg-title="Load-Testing Installer"
```
A `.dmg` file will be created.

---

### **Linux (Generate Standalone Executable)**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=Load-Testing ui.py
```
The generated executable