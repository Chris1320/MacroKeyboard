# MacroKeyboard

My setup for using a second keyboard as a macropad.

**NOTEs**:

- ~~This version is not (yet) working properly. `Main.ahk` cannot read `%keyfile%`.~~
- This version is experimental. `config.txt` is currently unused; Variables are hardcoded.

## How to Use

1. Plug your second keyboard (your macropad) to your system.
2. Edit `config.txt` to your needs. If you don't know the Keyboard ID of your second keyboard, run `get_key_codes.lua` in LuaMacros to automatically fill it in.
3. Edit `main.ahk` to your needs. (Refer to [AutoHotkey manual](https://www.autohotkey.com/docs/AutoHotkey.htm))
4. Edit `start-startup-cmds.py` to your needs. (if you want to use it)
5. Run `LuaMacros.exe -r 2nd_keyboard.lua`.
6. Run `AutoHotkey.exe main.ahk`.
7. Add to auto startup.

- **A**. Add a shortcut of `start-startup-cmds.py` to `C:\Users\***USERNAME***\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`.
- **B**. Add shortcuts of the two commands below to `C:\Users\***USERNAME***\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`.
  - `LuaMacros.exe -r 2nd_keyboard.lua`
  - `AutoHotkey.exe main.ahk`

## Requirements

Bare:

- LuaMacros
- AutoHotkey

Additional:

- Voicemeeter (Tested only on *Banana Edition*)
- OBS Studio (with OBS-Websocket plugin)

*This project is for advanced users (although some of you can use this without any coding skills) and **I am not responsible for any corruption of data or any other negative consequences this program may do.***

## Troubleshooting

- I am getting the error `The term '<command>' is not recognized as a name of a cmdlet, function, script file, or executable program.` in my terminal!
  - **Fix**: Make sure that **LuaMacros.exe** and **AutoHotkey.exe** are in PATH.
  - **Alternative Fix**: If you don't want to add the executables to PATH, use absolute paths. (e.g.: `D:\System\LuaMacros\LuaMacros.exe -r 2nd_keyboard.lua`)
- My macropad is acting like a normal keyboard.
  - **Notes**
    - Make sure LuaMacros and AutoHotkey are running.
    - Check if `config.txt` has the keyboard ID of your macropad.

## Credits

- This project is basically a modified fork of [Parrot023/Secondary_MACRO_keyboard](https://github.com/Parrot023/Secondary_MACRO_keyboard).
- Voicemeeter API wrapper in Python is from [chvolkmann/voicemeeter-remote-python](https://github.com/chvolkmann/voicemeeter-remote-python).
- OBS-Websocket Python API wrapper is from [Elektordi/obs-websocket-py](https://github.com/Elektordi/obs-websocket-py).
