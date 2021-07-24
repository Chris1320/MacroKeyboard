
-- Keyboard id for 2nd keyboard
-- If you dont know the id of you secondary keyboard you can use Get_keycode.lua
-- Which you will also find in this repository
local kbID = 'PID_FF0F';
-- The filepath where to write the keys
local keyfile = "D:\\Scripts\\MacroKeyboard\\key.txt";

-- minimizes the luamacros window
lmc.minimizeToTray = true
lmc_minimize()
clear() -- clears the luamacros terminal

lmc_device_set_name('MACROS',kbID); -- asigns a logical name to our secondary keyboard

lmc_print_devices() -- prints all devices, you should se a device named MACROS

-- function to write the key codes to file: key.txt
write_to_file = function (key)
    print("Button: " .. key)
    print("====================")
    local file = io.open(keyfile, "w")
    file:write(key)
    file:flush() -- flush = save
    file:close()
    lmc_send_keys('{F24}')  -- Triggers the F24 key to tell autohotkey to read the key.txt file
end

print("Waiting...")
print()
print("====================")
-- define callback device MACROS 
lmc_set_handler('MACROS' ,function(button, direction)

  if (direction == 1) then return end  -- ignore down
  write_to_file(button) -- executes function write_to_file with argument button (button = the ascii code of that key)

end)
