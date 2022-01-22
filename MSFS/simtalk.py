from utils import *
f18Height = 6.07
TO_FEET = 3.28084

# set aircraft mechanical surfaces and actors - less frequently updated
def setMechanics(mechanics, aircraftType):
    Rudder = - mechanics['RudderLeft'] - mechanics['RudderRight']

    # setting this on a HELI will throw SimConnect errors
    if (aircraftType=='FIXEDWING'):
        # 0= gear up .. 1= gear down
        set_datapoint("GEAR_CENTER_POSITION", None, mechanics["Gear"])
        set_datapoint("GEAR_RIGHT_POSITION", None, mechanics["Gear"])
        set_datapoint("GEAR_LEFT_POSITION", None, mechanics["Gear"])
        trigger_event("SET_TAIL_HOOK_HANDLE", mechanics["Hook"])

    Fuel = 1
    set_datapoint("FUEL_TANK_CENTER_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_CENTER2_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_CENTER3_LEVEL", None, Fuel)

    set_datapoint("FUEL_TANK_EXTERNAL1_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_EXTERNAL2_LEVEL", None, Fuel)
    
    set_datapoint("FUEL_TANK_LEFT_MAIN_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_LEFT_TIP_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_LEFT_AUX_LEVEL", None, Fuel)

    set_datapoint("FUEL_TANK_RIGHT_MAIN_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_RIGHT_TIP_LEVEL", None, Fuel)
    set_datapoint("FUEL_TANK_RIGHT_AUX_LEVEL", None, Fuel)

    trigger_event("THROTTLE1_SET", mechanics["LeftThrottle"] * 16383)
    trigger_event("THROTTLE2_SET", mechanics["RightThrottle"] * 16383)

    #for simplicity we set inner and outer flaps to same value
    set_datapoint("LEADING_EDGE_FLAPS_RIGHT_PERCENT", None, mechanics["Flaps"])
    set_datapoint("LEADING_EDGE_FLAPS_LEFT_PERCENT", None, mechanics["Flaps"])
    set_datapoint("TRAILING_EDGE_FLAPS_RIGHT_PERCENT", None, mechanics["Flaps"])
    set_datapoint("TRAILING_EDGE_FLAPS_LEFT_PERCENT", None, mechanics["Flaps"])

    # some weird shit with the F-18 ? AileronLeft is static at 0.67
    Aileron = mechanics["AileronLeft"] + mechanics["AileronRight"]
    if Aileron < 0: Aileron *= 3

    set_datapoint("ELEVATOR_POSITION", None, mechanics["ElevatorLeft"])
    #set_datapoint("ELEVATOR_POSITION", 2, ElevatorRight * 16000)
    #set_datapoint("ELEVON_DEFLECTION", None, ElevatorLeft * 5)
    set_datapoint("RUDDER_POSITION", None, Rudder)
    set_datapoint("AILERON_POSITION", None, Aileron)
    #set_datapoint("AILERON_RIGHT_DEFLECTION", None, AileronRight * 16000)
    set_datapoint("SPOILERS_HANDLE_POSITION", None, mechanics["SpeedBrakes"])


def parseRow(row, dic, start):
    fields = row.split(",")

    i = start
    for k, v in dic.items():
        dic[k] = float(fields[i])
        #print(k, dic[k])
        i += 1




def initialSettings(telemetrics, Offsets, setDcsPosition):
    #MsAltAboveGnd = get_datapoint("PLANE_ALT_ABOVE_GROUND")
    #Ms_GndAlt = get_datapoint("GROUND_ALTITUDE") # ground height AMSL in m
    #Ms_Alt = get_datapoint("PLANE_ALTITUDE") # center of plane, in feet
    #print(Ms_GndAlt, Ms_GndAlt * TO_FEET, Ms_Alt, Ms_Alt - Ms_GndAlt * TO_FEET, Ms_Elevation)
    print("DCS Map started at Lat: %.4f, Lng: %.4f" % (telemetrics["Lat"], telemetrics["Lng"]))

    # command line argument
    if setDcsPosition:
        Offsets["Lat"] = 0
        Offsets["Lng"] = 0
        Offsets["Alt"] = f18Height
        Offsets["Hdg"] = 0
        Offsets["StartLat"] = 0
        Offsets["StartLng"] = 0

        # Plane could be stuck in ground from last crash. Keep aircraft on runway when DCS on ground
        Ms_GndAlt = get_datapoint("GROUND_ALTITUDE") or 0 # ground height AMSL in m
        print(Ms_GndAlt, "Ms_GndAlt")
        Ms_Elevation = f18Height + (Ms_GndAlt * TO_FEET) # equals Ms_Alt
        if Ms_Elevation > 1 and telemetrics["AltGnd"] < f18Height + 1:
            set_datapoint("PLANE_ALTITUDE", None, Ms_Elevation)
        print("Setting MSFS aircraft to DCS world coordinates and altitude", setDcsPosition)

    # Keep MSFS world position
    else:
        Offsets["StartLat"] = get_datapoint("PLANE_LATITUDE")
        Offsets["StartLng"] = get_datapoint("PLANE_LONGITUDE")
        if not (Offsets["StartLat"] and Offsets["StartLng"]):
            raise("MSFS coordinates not readable. Crashed?")
        Offsets["Lat"] = Offsets["StartLat"] - telemetrics["Lat"]
        Offsets["Lng"] = Offsets["StartLng"] - telemetrics["Lng"]
        Offsets["Alt"] = 0 #StartAlt - telemetrics["Alt"] + f18Height
        MagneticHdg = get_datapoint("PLANE_HEADING_DEGREES_MAGNETIC")
        Offsets["Hdg"] = 0 #MagneticHdg - telemetrics["Hdg"]
        TrueHdg = get_datapoint("PLANE_HEADING_DEGREES_TRUE")
        Offsets["Declination"] = TrueHdg - MagneticHdg
        print("Keeping MSFS aircraft coordinates, altitude and heading at ", Offsets["StartLat"], Offsets["StartLng"])



# set aircraft position, rotation - frequently updated
def setTelemetrics(telemetrics, Offsets, setDcsPosition):
    set_datapoint("PLANE_PITCH_DEGREES", None, telemetrics["Pit"])

    # MSFS F18 seems to be showing TRUE HDG in HUD
    NewHdg =  telemetrics["Hdg"] + Offsets["Hdg"]
    set_datapoint("PLANE_HEADING_DEGREES_TRUE", None, NewHdg)
    set_datapoint("PLANE_BANK_DEGREES", None, telemetrics["Bnk"])
    
    
    #Check if DCS aircraft is airborne
    Airborne = telemetrics["AltGnd"] > f18Height + 3
    NewAlt = telemetrics["Alt"] + Offsets["Alt"]
    
    # Dont change MS aircraft altitude during rolling takeoff / landing
    # And don't set MS aircraft alt lower than Elevation
    if  not setDcsPosition or Airborne:
        #print(telemetrics["AltGnd"], NewAlt, Ms_Elevation)
        set_datapoint("PLANE_ALTITUDE", None, NewAlt )
        #set_datapoint("INDICATED_ALTITUDE", None, NewAlt )
    #else:
        #print(telemetrics["AltGnd"], NewAlt, Ms_Elevation)
        #Offsets["Alt"] += .3
        #set_datapoint("PLANE_ALTITUDE", None, Ms_Alt )

    x = telemetrics["Lat"] + Offsets["Lat"]
    y = telemetrics["Lng"] + Offsets["Lng"]

    if setDcsPosition:
        set_datapoint("PLANE_LATITUDE", None, x)
        set_datapoint("PLANE_LONGITUDE", None, y)
    else: 
        #p = rotate_point(Offsets["StartLat"], Offsets["StartLng"], Offsets["Hdg"], x, y)
        #print(p, math.degrees(telemetrics["Hdg"]), math.degrees(Offsets["Hdg"]))
        set_datapoint("PLANE_LATITUDE", None, x)
        set_datapoint("PLANE_LONGITUDE", None, y)
    
  

    set_datapoint("AIRSPEED_TRUE", None, telemetrics["TAS"])
        # set_datapoint("ROTATION_VELOCITY_BODY_X", None, 0)
        # set_datapoint("ROTATION_VELOCITY_BODY_Y", None, 0)
        # set_datapoint("ROTATION_VELOCITY_BODY_Z", None, 0)
        # set_datapoint("VELOCITY_BODY_X", None, 0)
        # set_datapoint("VELOCITY_BODY_Y", None, 0)
        # set_datapoint("VELOCITY_BODY_Z", None, 0)