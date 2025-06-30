# Minecraft Mod Updater

This project provides tools for retargeting Minecraft mod JARs to a different
game version. You can use either the simple Tkinter GUI or a web interface
served with Flask and React.

## Usage
1. Run `python3 mod_updater_gui.py`.
2. Select the JAR file you want to update.
3. Enter the target Minecraft version along with your Modrinth project ID, CurseForge mod ID and API key.
4. The tool checks both sites for an existing build and, if none is found, writes a new JAR next to the original named `modname}{version.jar`.

The Tkinter app relies on the `requests` package which is generally available
with Python 3. If missing, install it with `pip install requests`.

## React Web Interface
1. Install the server dependencies with `pip install flask requests`.
2. Run `python3 server.py`.
3. Visit [http://localhost:5000](http://localhost:5000) to access the React
   frontend and update your JAR.
