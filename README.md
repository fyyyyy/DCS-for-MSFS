# DCS-for-MSFS
Connecting the DCS Flight Model with Microsoft Flight Simulator.
See [on youtube](https://www.youtube.com/channel/UCZobogo5kNABPsUp_W4tU0Q)

This version currently is only for developers, normal users please wait for the .EXE installer.
Join the [DISCORD](https://discord.gg/j9WuCrsY8y)

# Installation

## MSFS
* Open a terminal / powershell window. Prefarably a shell that supports color (you can get one of those by going to the start menu and typing "cmd" or PowerShell) 
* Type `python` (or python3 depending on what is currently installed) and enter. If python is not installed, Microsoft Store will open. I recommend using [a different solution](https://stackoverflow.com/a/57421906) to install python 3
* At the Windows command prompt install Flask: `pip install -U Flask`
* Install [Python-SimConnect](https://github.com/odwdinc/Python-SimConnect): `pip install SimConnect`
* Start MSFS, span mid air 1000-5000 ft MSL with a similar aircraft that you fly in DCS. But it can also be a totally different aircraft, as it's flight physics are disabled in MSFS.
* Run `python DCS_MSFS_CONNECT.py` in the MSFS folder.
* IMPORTANT: Set MSFS General Options > Camera > HOME COCKPIT MODE > ON. Otherweise the camera will jitter on rolls
* Create a new joystick binding to unset all joystick controls. We dont want joystick controls to interfere with MSFS
* Preferably mute MSFS audio and listen to the sound from DCS

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
This is also ideal for comparing scenery between DCS and MSFS, for example Marinas below:
![grafik](https://user-images.githubusercontent.com/3744048/150657932-a38929c5-9a64-4694-91e6-93206b53697d.png)

We're working on a solution to allow takeoff and landing even when flying in different world locations in DCS vs MSFS

## VR
This was tested and works in VR. There is also no reason that it shouldn't as you are running regular MSFS in VR. DCS should be kept on 2D, so you need to bind your important buttons and controls to a HOTAS system. Interacting with VR cockpit buttons in MSFS does not yet have any effect on DCS

