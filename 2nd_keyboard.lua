local string = require "string";
local io = require "io";  -- For file operations

-- Change the path here if you want to use a different configuration file.
local configfile = "./config.txt";

function split_str(inputstr, sep) -- From `https://stackoverflow.com/a/7615129/15376542`
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
local config = split_str(config, '\n');  -- Convert config file to a table.

for line, value in pairs(config) do
    -- Parse config data
    if string.find(value, "keyboard_id=") ~= nil then
        kbID = split_str(value, '=')[2];

    elseif string.find(value, "keyfile=") ~= nil then
        keyfile = split_str(value, '=')[2];
    end
end

print("Keyboard ID: " .. kbID)
print("Keyfile:     " .. keyfile)

print("Waiting...")
