local log_file = nil
local TO_FEET = 3.28084

-- load Network, Config
dofile(lfs.writedir()..[[Scripts\Dcs For Msfs\config.lua]])


function LuaExportStart()
    if Config.writeLog then log_file = io.open(Config.filename, "w") end
    if Config.writeLog then log_file:write("start") end

	package.path  = package.path..";"..lfs.currentdir().."/LuaSocket/?.lua"
	package.cpath = package.cpath..";"..lfs.currentdir().."/LuaSocket/?.dll"

	socket = require("socket")
    MySocket = socket.udp()
    MySocket:setpeername(Network.ip, Network.port)

    local own = LoGetSelfData()
    local pilotName = LoGetPilotName()

   socket.try(MySocket:send(
        table.concat({"Hello_DCS", own.Name, pilotName}, ",")
    ))
end

function LuaExportAfterNextFrame()
    if Config.writeLog then 
        local data = GetTelemetry(false)
        log_file:write(data)
    end
end

function LuaExportStop()
    if Config.writeLog then
        log_file:write(string.format("EXIT_DCS"))
        if log_file then
            log_file:close()
            log_file = nil
        end
    end

    if MySocket then 
		socket.try(MySocket:send("EXIT_DCS"))
		MySocket:close()
	end
end

function LuaExportActivityNextEvent(t)
    local tNext = t

    -- interval in milliseconds
    ms = Config.interval

    -- send less frequent data every "Config.rare" milliseconds
    local rarelyUpdate = (tNext * 1000) % Config.rare < ms

    local telemetry, mechanics = GetTelemetry(rarelyUpdate)
    socket.try(MySocket:send(telemetry .. mechanics))

    tNext = tNext + (ms / 1000)
    return tNext
end

function GetTelemetry(rarelyUpdate)
    local mechanicsSerial = ''

    --local time = LoGetModelTime()
    --local AoA = LoGetAngleOfAttack()

    -- On marrinas map, true north magnetic declination is 1° E. For other maps change this param 
    -- local MagneticDeclination = math.rad(1) -- positive = East, negative = West
    local TAS = LoGetTrueAirSpeed()
    local own = LoGetSelfData()
    local mech = LoGetMechInfo()
    local altGnd = LoGetAltitudeAboveGroundLevel()

    local telemetry = {}
    telemetry[#telemetry+1] = "\n" 
    telemetry[#telemetry+1] = string.format( "%.4f", own.Heading ) -- seems to be TRUE NORTH 
    telemetry[#telemetry+1] = string.format( "%.5f", - own.Bank )
    telemetry[#telemetry+1] = string.format( "%.3f", - own.Pitch )
    telemetry[#telemetry+1] = string.format( "%.4f", altGnd * TO_FEET )
    telemetry[#telemetry+1] = string.format( "%.4f", own.LatLongAlt.Alt * TO_FEET )
    telemetry[#telemetry+1] = string.format( "%.10f", own.LatLongAlt.Lat )
    telemetry[#telemetry+1] = string.format( "%.10f", own.LatLongAlt.Long )
    telemetry[#telemetry+1] = string.format( "%.4f", TAS / 0.539957 ) --to knots because of DCS error
    telemetry[#telemetry+1] = "\n" 
    telemetrySerial = table.concat(telemetry, ",")

    -- less frequent updates
    if rarelyUpdate then
            
        local MainPanel = GetDevice(0)
        
        -- F-18 specific, does NOT work in external view
        -- See DCS World\Mods\aircraft\FA-18C\Cockpit\Scripts\mainpanel_init.lua
        -- 104 = Left Engine Throttle
        local F18_leftThrottle = MainPanel:get_argument_value(104)
        -- 105 = Right Engine Throttle
        local F18_rightThrottle = MainPanel:get_argument_value(105)
        -- 293 = Hook retracted
        local F18_hook = 1 - MainPanel:get_argument_value(293)

        local mechanics = {}
        mechanics[#mechanics+1] = string.format( "%.2f", mech.gear.value )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.flaps.value )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.refuelingboom.value )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.speedbrakes.value )
        mechanics[#mechanics+1] = string.format( "%.2f", F18_hook )
        mechanics[#mechanics+1] = string.format( "%.2f", F18_leftThrottle )
        mechanics[#mechanics+1] = string.format( "%.2f", F18_rightThrottle )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.elevator.left )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.elevator.right )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.rudder.left )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.rudder.right )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.eleron.left )
        mechanics[#mechanics+1] = string.format( "%.2f", mech.controlsurfaces.eleron.right )
        mechanics[#mechanics+1] = "\n" 
        mechanicsSerial = table.concat(mechanics, ",")
    end

    return  telemetrySerial, mechanicsSerial
end