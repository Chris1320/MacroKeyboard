local string = require "string";
local io = require "io";  -- For file operations

-- minimizes the luamacros window
lmc.minimizeToTray = true
lmc_minimize()

-- Change the path here if you want to use a different configuration file.
local configfile = "D:/Scripts/MacroKeyboard/config.txt";

print("Reading configuration file `" .. configfile .. "`...")

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

local kbID = nil;
local keyfile = nil;

-- Read config file.
local config = io.open(configfile, 'r'):read("*all");
local config = splitStr(config, '\n');  -- Convert config file to a table.

for line, value in pairs(config) do
    -- Parse config data
    if string.find(value, "keyboard_id=") ~= nil then
        kbID = splitStr(value, '=')[2];

    elseif string.find(value, "keyfile=") ~= nil then
        keyfile = splitStr(value, '=')[2];
    end
end

print("Keyboard ID: " .. kbID)
print("Keyfile:     " .. keyfile)

-- clear() -- clears the luamacros terminal

lmc_device_set_name('MACROS',kbID); -- asigns a logical name to our secondary keyboard
lmc_print_devices() -- prints all devices, you should se a device named MACROS

print("\nWaiting for input...\n====================")

-- function to write the key codes to <keyfile>.
write_to_file = function (key)
    print("Button: " .. key)
    print("====================")
    local file = io.open(keyfile, "w")
    file:write(key)
    file:flush() -- flush = save
    file:close()
    lmc_send_keys('{F24}')  -- Triggers the F24 key to tell autohotkey to read the key.txt file
end

-- define callback device MACROS 
lmc_set_handler('MACROS' ,function(button, direction)
    if (direction == 1) then return end  -- ignore down
    write_to_file(button) -- executes function write_to_file with argument button (button = the ascii code of that key)
    end
)
