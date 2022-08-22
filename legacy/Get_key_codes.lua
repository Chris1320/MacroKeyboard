local string = require "string";
local io = require "io";  -- For file operations

clear();

-- Change the path here if you want to use a different configuration file.
local configfile = "./config.txt";

function splitStr(inputstr, sep) -- From `https://stackoverflow.com/a/7615129/15376542`
    if sep == nil then  -- If separator is nil then use whitespace.
        sep = "%s";
    end

    local result = {};

    for i in string.gmatch(inputstr, "([^"..sep.."]+)") do
        table.insert(result, i);
    end

    return result;
end

-- assign logical name to macro keyboard
-- you will be prompted to press a key on keyboard MACROS. This is the secondary keyboard
lmc_assign_keyboard('MACROS');

devices = lmc_get_devices();

print("Devices:");
-- id: The keyboard number (starts with 0)
-- data: Contains keyboard details
for id,data in pairs(devices) do
    print(id .. ':')
    -- info: key from <data>.
    -- value: value of <key> from <data>.
    for info,value in pairs(data) do
        if info == "Name" then  -- Check if this is the data of the macro keyboard.
            if value == "MACROS" then
                -- If this is the data of the macro keyboard, get SystemId.
                for k, v in pairs(data) do
                    if k == "SystemId" then
                        system_id = v;  -- Get the SystemID value of the keyboard
                        keyboard_id = splitStr(system_id, "&")
                        keyboard_id = splitStr(keyboard_id[2], "&")[1]
                        print("  Keyboard ID: " .. keyboard_id)
                        -- Read the configuration file first
                        local config = io.open(configfile, 'r');
                        local configdata = config:read("*all");
                        local configdata = splitStr(configdata, '\n');
                        local new_configdata = {};
                        for line, data in pairs(configdata) do
                            local dat = splitStr(data, '=');
                            if dat[1] == "keyboard_id" then
                                table.insert(new_configdata, "keyboard_id=" .. keyboard_id);

                            else
                                table.insert(new_configdata, data);
                            end
                        end
                        config:close();
                        local str_configdata = "";
                        -- Convert table to string
                        for k, v in pairs(new_configdata) do
                            str_configdata = str_configdata .. v .. '\n'
                        end
                        -- Write new configfile values to <configfile>.
                        local config = io.open(configfile, 'w');
                        config:write(str_configdata);
                        config:flush();  -- Save to file
                        config:close();
                    end
                end
            end
        end

        -- Print the device information
        print('  ' .. info .. ' = ' .. value)
    end
end

-- defines callback for device MACROS
lmc_set_handler('MACROS' ,function(button, direction)
    if (direction == 1) then return end  -- ignore down
    print("Button Pressed: " .. button) -- print button code
end)