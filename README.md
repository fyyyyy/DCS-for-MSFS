# DCS-for-MSFS
Connecting DCS Flight Model with Microsoft Flight Simulator.
See [on youtube](https://www.youtube.com/channel/UCZobogo5kNABPsUp_W4tU0Q)

This is only for experienced developers, normal users please wait for the EXE installer.

# Installation

## MSFS
* Open a terminal / powershell. Prefarably a shell that supports color (you can get one of those by going to the start menu and typing "cmd" or PowerShell) 
* Type `python` and enter. If python is not installed, Microsoft Store will open. I recommend using another solution to install python 3
* At the Windows command prompt install Flask: `pip install -U Flask`
* Install [Python-SimConnect](https://github.com/odwdinc/Python-SimConnect): `pip install SimConnect`
* Start MSFS, span mid air 1000-5000 ft MSL
* Run `python DCS_MSFS_CONNECT.py` in the MSFS folder.
* Create a new joystick binding to unset all joystick controls. We dont want joystick controls to interfere with MSFS

![grafik](https://user-images.githubusercontent.com/3744048/150621920-9eb15a86-a0af-455a-a90a-6f6c51e3e4ac.png)


## DCS
* Add the line in DCS/Export.lua to your DCS/Scripts/Export.lua or copy the file if it doesn't exist
* Copy the entire `DCS For MSFS` folder into `DCS/Scripts/DCS For MSFS`
* If you run DCS on a different machine, it must be connected via Wifi or LAN to the same network. Enter the IP address you see when running the python script in the `DCS/Scripts/Dcs For Msfs/config.lua` file.
* If you run DCS on the same machine (not recommended) make sure you set it to LOWEST graphics and resolution. If you have a laptop, set DCS to be rendered with the * INTERNAL graphics card if available.
* With the python script running and already connected to SimConnect, start a DCS mission 1000-5000ft MSL. If you want to save render frames in DCS, go to F10 ingame map this will save about 30-50% CPU and GPU

![grafik](https://user-images.githubusercontent.com/3744048/150621954-1e6c6d76-51f6-4c3e-ba64-5a26ade57e83.png)


## Tested Aircraft
Tested aircraft combos are
1. DCS F-18 -> MSFS default F-18 ( The SuperWarrior F-18 Mod has some collision issues)
2. DCS UH-1 -> MSFS UH-1 Gunship [freeware](https://fr.flightsim.to/file/24313/uh-1c-huey-gunship)

External control surfaces, gear, speedbrakes if available are synchronised. Some cockpit instruments work correctly, some don't.
If you want to interact with complex systems in the cockpit, do it inside DCS not MSFS. Most of the cockpit controls in MSFS are not yet synched to DCS.

## Takeoff and Landing
Landing / Takeoff is not possible unless you run `python DCS_MSFS_CONNECT.py DCS` which sets MSFS world position to the same location as DCS.
Working on a solution...
