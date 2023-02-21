--[[
setup.lua -- Part of Chris1320/MacroKeyboard

This Lua script for LuaMacros will help you setup the configuration
file that will be used by the MacroKeyboard system.
]]--

local VERSION = {0, 0, 1}

local function splitStr(input_str, separator)
    --[[
        Split a string <input_str> into a table of strings, separated by <separator>.
        This function is based on `https://stackoverflow.com/a/7615129/15376542`.
    ]]--

    local result = {}
    local separator = separator or "%s"  -- Use default (any whitespaces) when separator is not supplied.

    -- Separate input_str into a list of substrings based on separator.
    for separated_str in string.gmatch(input_str, "([^" .. separator .. "]+)") do
        table.insert(result, separated_str)  -- Insert each substring into result.
    end

    return result
end

local function getMacropadPID(system_id)
    --[[
        Extract the PID of the keyboard from the SystemId string.

        @param system_id string The System ID of the keyboard.
        @return string The PID of the keyboard.
    ]]--

    local pid = splitStr(system_id, "&")
    return splitStr(pid[2], "&")[1]
end

print("========================================")
print("Script Version: v" .. table.concat(VERSION, "."))

-- ? Dump keyboard details to file.
print("Dumping keyboard details...")

local detected_keybs = {}  -- This table contains all detected keyboard details.
local devices = lmc_get_devices()

print("Detected Devices:")
for device_id, device_details in pairs(devices) do  -- Check each detected devices.
    detected_keybs[device_id] = {}  -- Create an entry for the device.
    print("Device #" .. device_id)
    print("[+] Hardware PID: " .. getMacropadPID(device_details["SystemId"]))
    detected_keybs[device_id]["PID"] = getMacropadPID(device_details["SystemId"])
    for dev_info_key, dev_info_value in pairs(device_details) do  -- Check each device detail.
        print("[+] " .. dev_info_key .. ": " .. dev_info_value)
        detected_keybs[device_id][dev_info_key] = dev_info_value
    end
    print()
end

for _, device in pairs(detected_keybs) do
    for key, value in pairs(device) do
        print(key .. ": " .. value)
    end
    print()
end
