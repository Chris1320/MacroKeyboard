--[[
setup.lua -- Part of Chris1320/MacroKeyboard

This Lua script for LuaMacros will help you setup the configuration
file that will be used by the MacroKeyboard system.
]]--

Name = "MacroKeyboard"
Version = {0, 0, 4}
Title = Name .. " v" .. table.concat(Version, ".")

--[[
    CONFIGURATION

    The table below contains configuration data of the script.
]]--
local config = {
    -- Script Configuration
    debug = false,

    -- filesystem paths
    configfile_path = "./default.conf",  -- The path of the configuration file to use.

    -- Keyboard Configuration
    target_keyboard_name = "MACROS"  -- The name to assign to the macropad.
}

local function debugPrint(message)
    --[[
        Print <message> if <debug> is true.

        :param str message: The message to print.

        :returns nil:
    ]]--

    if config["debug"] then
        print(message)

    end
end

local function optionalPrint(message, enable)
    --[[
        Print <message> only if <enable> is true.

        :param string message: The message to print.
        :param bool enable: It true, print the message.

        :returns nil:
    ]]--

    if enable then
        print(message)

    end
end

local function splitStr(input_str, separator)
    --[[
        Split a string <input_str> into a table of strings, separated by <separator>.
        This function is based on `https://stackoverflow.com/a/7615129/15376542`.

        :param str input_str: The string to split.
        :param str separator: The separator to use.

        :returns table: A table of strings.
    ]]--

    local result = {}
    local separator = separator or "%s"  -- Use default (any whitespaces) when separator is not supplied.

    -- Separate input_str into a list of substrings based on separator.
    for separated_str in string.gmatch(input_str, "([^" .. separator .. "]+)") do
        table.insert(result, separated_str)  -- Insert each substring into result.

    end

    return result

end

local ConfigHandler = {
    --[[
        This table contains functions that will be used to handle the configuration file.

        TODO: Currently, the functions can only handle strings.
    ]]--

    get = function(configpath, key)
        --[[
            Get the <key> from <configpath> configuration file.

            :param str configpath: The path to the configuration file.
            :param str key: The key to find in the configuration file.

            :returns str: The value of the key.
        ]]--

        local file = io.open(configpath, "r")
        if not file then
            return nil

        else
            local contents = splitStr(file:read("*all"), '\n')
            file:close()  -- We're done reading the file. Close it.
            for _, line in ipairs(contents) do
                local k = nil
                local v = nil
                -- See the comment to the same logic in ConfigHandler.set() for
                -- the explanation to this atrocity.
                for _, l in pairs(splitStr(line, '=')) do
                    -- Each line `l` can be the key or value of the splitted line.
                    -- _ is the index (not needed)
                    if not k then  -- If k is nil, then l is the key.
                        k = l

                    else
                        v = l  -- If the key is already set, set l as the value.
                        break  -- Break loop because we now have k and v.

                    end
                end
                if k == key then
                    return v

                end
            end
        end
    end,
    set = function(configpath, key, value)
        --[[
            Set the <key> to <value> in <configpath> configuration file.

            :param str configpath: The pathto the configuration file.
            :param str key: The key to add/modify.
            :param str value: The new value of the key.

            :returns int: 0 if successful, otherwise non-zero.
        ]]--

        local file = io.open(configpath, "r")  -- Read its contents first.
        local new_contents = {}
        local value_changed = false
        if file then  -- Skip reading file if file does not exist.
            local contents = splitStr(file:read("*a"), '\n')
            file:close()  -- Close the file.
            for _, line in pairs(contents) do
                local k = nil
                local v = nil
                -- ? I have no idea why we need the for loop below instead of just
                -- ? unpacking the table using the following:
                -- local k, v = splitStr(line, '=')

                for _, l in pairs(splitStr(line, '=')) do
                    -- Each line `l` can be the key or value of the splitted line.
                    -- _ is the index (not needed)
                    if not k then  -- If k is nil, then l is the key.
                        k = l

                    else
                        v = l  -- If the key is already set, set l as the value.
                        break  -- Break loop because we now have k and v.

                    end
                end
                if k == key then  -- Change the value of key if it already exists in the table.
                    v = value
                    value_changed = true

                end
                new_contents[k] = v  -- Add the key/value pair to the new table.

            end
        end

        if not value_changed then  -- Add a new entry if the key does not yet exist in the table.
            new_contents[key] = value

        end

        local file = io.open(configpath, "w")  -- Write the new contents to the file.
        if not file then
            return 2  -- Failed to open the configuration file.

        else
            local new_file_content = ""  -- Create a new string to be written to file.
            for k, v in pairs(new_contents) do
                new_file_content = new_file_content .. k .. "=" .. v .. "\n"

            end

            file:write(new_file_content)
            file:close()
            return 0

        end
    end
}

local function assignMacroKeyboardName()
    --[[
        Assign logical name to macro keyboard.
        The user will be prompted to press a key on the keyboard that will be used as the macropad.

        :returns nil:
    ]]--

    lmc_assign_keyboard(config["target_keyboard_name"]) -- Assign the keyboard name to the macropad.

end

local function getMacropadPID(system_id)
    --[[
        Extract the PID of the keyboard from the SystemId string.

        :param str system_id: The System ID of the keyboard.

        :returns string: The PID of the keyboard.
    ]]--

    local pid = splitStr(system_id, "&")
    return splitStr(pid[2], "&")[1]

end

local function getMacropadDetails(print_details)
    --[[
        Get (and optionally print) the details of the new macropad.

        :param bool print_details: If true, print the details of the device.

        :returns table: The macropad details.
    ]]--

    local print_details = print_details or false  -- Set false as default value.
    local macropad_details = {}  -- Return this table containing device details.

    local devices = lmc_get_devices() -- Get all device information.
    optionalPrint("Detected Devices:", print_details)

    for device_id, device_details in pairs(devices) do  -- Check each detected devices.
        for device_details_key, device_details_value in pairs(device_details) do  -- Check each device detail.
            if device_details_key == "Name" then  -- Only get the name of the keyboard.
                if device_details_value == config["target_keyboard_name"] then
                    -- print all details of the keyboard.
                    optionalPrint("Device #" .. device_id, print_details)
                    for key, value in pairs(device_details) do
                        optionalPrint("[+] " .. key .. ": " .. value, print_details)
                        macropad_details[key] = value
                    end

                    optionalPrint("[+] Hardware PID: " .. getMacropadPID(device_details["SystemId"]), print_details)
                    macropad_details["PID"] = getMacropadPID(device_details["SystemId"])
                    return macropad_details

                end
            end
        end
    end
end

function Main()
    --[[
        The main function of the script.

        :returns int: The exit code of the script.
    ]]--

    clear()  -- Clear the logs.
    if config["debug"] == true then
        lmc_log_all() -- enable debug mode.

    end

    print(Title)
    print()
    assignMacroKeyboardName()
    local macropad_details = getMacropadDetails(true)
    print()
    print("[i] Writing configuration to " .. config["configfile_path"] .. "...")
    debugPrint("Writing `Keyboard.SystemId` exit code: " .. ConfigHandler.set(config["configfile_path"], "Keyboard.SystemId", macropad_details["SystemId"]))  -- Not actually used yet
    debugPrint("Writing `Keyboard.PID` exit code: " .. ConfigHandler.set(config["configfile_path"], "Keyboard.PID", macropad_details["PID"]))
    debugPrint("Writing `Keyboard.Name` exit code: " .. ConfigHandler.set(config["configfile_path"], "Keyboard.Name", macropad_details["Name"]))  -- Not actually used yet
    debugPrint("Writing `Keyboard.Handle` exit code: " .. ConfigHandler.set(config["configfile_path"], "Keyboard.Handle", macropad_details["Handle"]))  -- Not actually used yet
    print("[i] Writing configuration to " .. config["configfile_path"] .. "... Done!")

    return 0

end

return Main()
