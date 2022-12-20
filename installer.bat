@echo off
Color 02
Title requirements installer
Echo ============================
Echo    Requirements installer
Echo ============================
Echo Checking if nextcord or pycord is installed...
pip3 uninstall -r uninstall.txt
Echo started the module installer...
pip install -r requirements.txt
cls
Title             Done
Echo =================================
Echo Finnished installing Requirements
Echo =================================
Echo done
Echo Press any key to exit
Pause>nul
Exit