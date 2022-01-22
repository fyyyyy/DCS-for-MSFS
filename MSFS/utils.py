import math
import sys

from SimConnect import *
this = sys.modules[__name__]


def initSimConnect():
    # SIMCONNECTION RELATED STARTUPS
    print('\n       Connecting to MSFS SimConnect...')

    # Create simconnection
    try:
        this.sm = SimConnect()
    except Exception as e:
        print(bcolors.FAIL, 'Error: MSFS not running on this machine or pyton SimConnect not installed?\n%s' %
              e, bcolors.ENDC, file=sys.stderr)
        exit()

    print(bcolors.OKGREEN,"""
                        |
    ____________________|____________________
                   \  |   |  /
                    `.--=--.'
                     /`-_-'\\
                   O'       `O

            MSFS SimConnect connected !
                Disabling MSFS input
    """, bcolors.ENDC)

    this.ae = AircraftEvents(this.sm)
    this.aq = AircraftRequests(this.sm, _time=3)

    set_datapoint("USER_INPUT_ENABLED", None, False)

    # Disable MSFS simulation while connecting to DCS
    set_datapoint("SIM_DISABLED", None, True)


def get_datapoint(datapoint_name, index=None):
    # This function actually does the work of getting the datapoint

	if index is not None and ':index' in datapoint_name:
		dp = this.aq.find(datapoint_name)
		if dp is not None:
			dp.setIndex(int(index))

	return this.aq.get(datapoint_name)


def set_datapoint(datapoint_name, index=None, value_to_use=None):
	# This function actually does the work of setting the datapoint

	if index is not None and ':index' in datapoint_name:
		clas = this.aq.find(datapoint_name)
		if clas is not None:
			clas.setIndex(int(index))

	sent = False
	if value_to_use is None:
		sent = this.aq.set(datapoint_name, 0)
	else:
		sent = this.aq.set(datapoint_name, value_to_use)

	if sent is True:
		status = "success"
	else:
		status = "Error with sending request: %s" % (datapoint_name)
		print(bcolors.FAIL, status, bcolors.ENDC)
	return status


EVENTCACHE = {}


def trigger_event(event_name, value_to_use=None):
    # This function actually does the work of triggering the event
    
    try:
        EVENT_TO_TRIGGER = EVENTCACHE[event_name]
    except:
        EVENT_TO_TRIGGER = EVENTCACHE[event_name] = this.ae.find(event_name)

    if EVENT_TO_TRIGGER is not None:
        if value_to_use is None:
            EVENT_TO_TRIGGER()
        else:
            EVENT_TO_TRIGGER(int(value_to_use))

        status = "success"
    else:
        status = "Error: %s is not an Event" % (event_name)
        print(bcolors.FAIL, status, bcolors.ENDC)
    return status


def disableAircraftPhysics(bool):
    trigger_event("FREEZE_ALTITUDE_SET", bool)
    trigger_event("FREEZE_ATTITUDE_SET", bool)
    trigger_event("FREEZE_LATITUDE_LONGITUDE_SET", bool)

def rotate_point(cx, cy, rad, px, py):
    s = math.sin(rad)
    c = math.cos(rad)

    # translate point back to origin:
    px -= cx
    py -= cy

    # rotate point
    xnew = px * c - py * s
    ynew = px * s + py * c

    # translate point back:
    px = xnew + cx
    py = ynew + cy
    return [px, py]

def printDcsLogo(ip, port):
    print(bcolors.OKBLUE, """
                  |     |
                  |  _  |
    _____________/|_( )_|\_____________
       o   +|+   [ ( o ) ]   +|+
                *[_]---[_]*
            
DCS started on IP {0} port {1}
""".format(ip, port), bcolors.ENDC)


# this doesnt work yet, we want to add more aircraft via simconnect
# from ctypes import *

# initPos = SIMCONNECT_DATA_INITPOSITION(
#     get_datapoint("PLANE_LATITUDE"),
#     get_datapoint("PLANE_LONGITUDE"),
#     Alt,
#     0,
#     Hdg,
#     0,
#     0,
#     -1
# )

# this.sm.dll.AICreateNonATCAircraft(
#     this.sm.hSimConnect,
#     123.412,
#     32123.2,
#     initPos,
#     "REQUEST0"
# )

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    DEBUG = '\033[90m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_debug(name, o):
    print(bcolors.DEBUG, "DEBUG ", name, end=" ", flush=True)

    if type(o) == dict:
        for k, v in o.items():
            print(bcolors.DEBUG, k, bcolors.HEADER, v, " ", end=" ", flush=True)
    else: print(bcolors.HEADER, o)

    print(bcolors.ENDC) # flush