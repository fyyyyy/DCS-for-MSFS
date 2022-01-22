import socket
import threading
import sys
import time
import re

from simtalk import *
from utils import *

aircraftType = 'HELI'
aircraftName = bcolors.FAIL + "UNKNOWN. Restart DCS Mission" + bcolors.ENDC
pilotName = bcolors.FAIL + "UNKNOWN. Restart DCS Mission" + bcolors.ENDC

setDcsPosition = False
DEBUG = True

try:
    # command line arg supplied ?
    setDcsPosition = sys.argv[1] == 'DCS'
    print("Set MSFS to DCS world location", setDcsPosition)
except:
    print("Not setting MSFS to DCS world location (arg false)")
    setDcsPosition = False


initSimConnect()

# Create a UDP socket SERVER
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#  Listening for local and remote connections
host = "0.0.0.0"
port = 31339

sock.bind((host, port))

# DCS connection status
try:
    myIp = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    print("Enter this ip address in 'DCS/Scripts/Dcs For Msfs/config.lua' on the DCS computer:", bcolors.BOLD, myIp, bcolors.ENDC)
except:
    print("Not connected to a network?")

print('\nWaiting for DCS on %s port %s. (Press Ctrl + C to stop)' % (myIp or host, port))
    

def parseData(t):

    Offsets = {
        "Lat": None,
        "Lng": None,
        "Alt": None,
        "Hdg": None,
        "StartLat": None,
        "StartLng": None,
        "Declination": 0
    }
    telemetrics = {
        "Hdg": 0,
        "Bnk": 0,
        "Pit": 0,
        "AltGnd": 0,
        "Alt": 0,
        "Lat": 0,
        "Lng": 0,
        "TAS": 0,
    }
    mechanics = { 
        "Gear": 0,
        "Flaps": 0,
        "RefuelingBoom": 0,
        "SpeedBrakes": 0,
        "Hook": 0,
        "LeftThrottle": 0,
        "RightThrottle": 0,
        "ElevatorLeft": 0,
        "ElevatorRight": 0,
        "RudderLeft": 0,
        "RudderRight": 0,
        "AileronLeft": 0,
        "AileronRight": 0,
    }

    while getattr(t, "do_run", True):
        try:
            set_datapoint("SIM_DISABLED", None, False)
            disableAircraftPhysics(True)

            #receiving data from Export.lua ?
            data, addr = sock.recvfrom(256)
            if not data: return

            stringdata = data.decode('utf-8')
            if stringdata == "EXIT_DCS":
                print ("DCS is exiting.\nWaiting for new connection... (Press Ctrl + C to stop)")
                raise ConnectionError("DCS quit")

            rows = stringdata.split("\n")
            #print('rows', rows)

            # Telemetry data
            if rows[1]:
                parseRow(rows[1], telemetrics, 1)

                # First Iteration ? Setup offset positions for DCS VS MSFS world coordinates
                if getattr(t, "first_run", True):
                    t.first_run = False
                    print("\nDCS Aircraft: %s. Pilot: %s" % (aircraftName, pilotName))
                    initialSettings(telemetrics, Offsets, setDcsPosition)
                    if DEBUG:
                        print_debug("OFFSETS:", Offsets)
                else:
                    setTelemetrics(telemetrics, Offsets, setDcsPosition)

            # Mechanical data
            if rows[2]:
                parseRow(rows[2], mechanics, 0)
                setMechanics(mechanics, aircraftType)

        except Exception as e:
            print(bcolors.WARNING, '\nPausing due to Error: %s' % e, bcolors.ENDC, file=sys.stderr)
            t.do_run = False
            if DEBUG:
                print_debug("TELE:", telemetrics)
                print_debug("MECH:", mechanics)


# Ensures the connection is still active. Not sure we still need a thread since its no longer a TCP IP connection
def keepalive(data, ip):
    printDcsLogo(ip, port)

    set_datapoint("SIM_DISABLED", None, True)
    t = threading.currentThread()

    parseData(t)

    # Disconnected ?
    t.do_run = False
    print(bcolors.OKCYAN, "\nDCS disconnected ! Reconnecting... (Press Ctrl + C to stop)\n", bcolors.ENDC)


runningThread = 0
data = addr = 0

try:
    while True:
        # allow keyboard interrupt by setting timeout to 2 seconds
        sock.settimeout(2)
        try:
            if data == 0 or runningThread.do_run == False:
                data, addr = sock.recvfrom(256)
                stringData = data.decode('utf-8')

                if re.match("Hello_DCS", stringData):
                    fields = stringData.split(",")
                    aircraftName = fields[1]
                    pilotName = fields[2]
                    
                    if (aircraftName == 'UH-1H'): aircraftType = 'HELI'
                    if (aircraftName == 'FA-18C_hornet'): aircraftType = 'FIXEDWING'
                    print (bcolors.OKBLUE, "\nHello", pilotName, "Aircraft:", aircraftName, "Type:", aircraftType, "! DCS is loading...", bcolors.ENDC)
                    data = addr = 0
                elif stringData == "EXIT_DCS":
                    print ("DCS is exiting.\nWaiting for new connection... (Press Ctrl + C to stop)")
                    data = addr = 0

            # Data is good. Start thread unless already running
            if data != 0 and addr != 0 and (runningThread == 0 or runningThread.do_run == False):
                runningThread = threading.Thread(target=keepalive, args=(data, addr[0]))
                runningThread.do_run = True
                runningThread.first_run = True
                runningThread.start()
        except:
            # Waiting...
            print('.', end=" ", flush=True)
        time.sleep(1)

except KeyboardInterrupt:
    if sock:
        sock.close()
    print(bcolors.WARNING, ' INTERRUPTED!', bcolors.ENDC)
