#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SetTitleMatchMode, RegEx

configfile := "./config.txt"  ; The path of the configuration file
                              ; (Change this if you want to use a
                              ;       different configuration file)

; FIXME: How do I put a dictionary into config.txt? (DEV0004)
mode := 1 ; The default mode
max_modes := 4 ; How many "modes" do we have?
mode_names := {(1): "Application Shortcuts", (2): "OBS Studio", (3): "N/A", (4): "N/A"}

; Read configfile contents
FileRead, config, %configfile%

if ErrorLevel  ; If ErrorLevel is not equal to 0
{
    MsgBox, , "Configuration File Read Error", "Cannot read the configuration file."
    Exit, 1  ; TODO: The script still runs even after exiting. (DEV0001)
}

; Split config into an array
config := StrSplit(config, "`n")

keyfile := ""
obs_host := ""
obs_port := ""
obs_pass := ""

; Get values from config
For ckey, cvalue in config
{
    ; Check if line starts with a comment or nothing.
    ; Otherwise, continue to search for configuration data.
    stripped_cvalue := StrSplit(cvalue)
    For i, cvalue_char in stripped_cvalue
    {
        if (cvalue_char == "#") and (i == 1)  ; Ignore comments
        {
            Break
        }
        else
        {
            ; Search for config keys in cvalue
            keyfile_found := InStr(cvalue, "keyfile=", True)
            obs_host_found := InStr(cvalue, "obs_host=", True)
            obs_port_found := InStr(cvalue, "obs_port=", True)
            obs_pass_found := InStr(cvalue, "obs_pass=", True)
            if (keyfile_found == 1)
            {
                keyfile := StrSplit(cvalue, "=")[2]
            }
            else if (obs_host_found == 1)
            {
                obs_host := StrSplit(cvalue, "=")[2]
            }
            else if (obs_port_found == 1)
            {
                obs_port := StrSplit(cvalue, "=")[2]
            }
            else if (obs_pass_found == 1)
            {
                obs_pass := StrSplit(cvalue, "=")[2]
            }

            Break  ; Stop the second (by-character) loop.
        }
    }
}

if (obs_host == "" ) or ( obs_port == "") or (obs_pass == "") or (keyfile == "")
{
    MsgBox, , "Configuration File Read Error", "The configuration file lacks the neccessary data!"
    Exit, 2
}

; MsgBox,, "Configfile Values", Keyfile:%keyfile%`nobs_host:%obs_host%`nobs_port:%obs_port%`nobs_pass:%obs_pass%  ; For debugging only (DEV0005)

F24::

    ;Read the file key.txt and outputs the result in a variable named Output
    FileRead, Output, %keyfile%
    ;MsgBox,, "F24 Detected", "Detected input: %Output%"

;BTW these key codes are unicode
;https://en.wikipedia.org/wiki/List_of_Unicode_characters
;You can add more key codes if you want
;If you dont know the key code you can use Get_key_code.lua
;Here we attach a key code to each key.
;this is like saying. when i ask for 0 give me back 48 etc. each key is seperated by commas.

        ;List of main keys
        ;Number keys
Main_Keys := {"0": "48", "1": "49", "2": "50", "3": "51", "4": "52", "5": "53", "6": "54","7": "55", "8": "56", "9": "57"
        ;First row of letters
        , "q": "81", "w": "87", "e": "69", "r": "82", "t": "84", "y": "89", "u": "85", "i": "73", "o": "79", "p": "80", "å": "221"
        ;2nd row of letters
        , "a": "65", "s": "83", "d": "68", "f": "70", "g": "71", "h": "72", "j": "74", "k": "75", "i": "76", "æ": "192", "ø": "222"
        ;3rd row of letters
        , "z": "90", "x": "88", "c": "67", "v": "86", "b": "66", "n": "78", "m": "77"}

        ;list of Numpad keys
Numpad := {"numlock": "144", "/": "111", "*": "106", "-": "109"
            , "7": "103", "8": "104", "9": "105", "+": "107"
            , "4": "100", "5": "101", "6": "102"
            , "1": "97", "2": "98", "3": "99"
            ;0 on the number pad does not have the same key code as normal 0
            , "0": "96", "del": "46", "enter": "13", ".": "110", "backspace": "8"}

;F24 hotkey
f24::

    ;Read the file key.txt and outputs the result in a variable named Output
    FileRead, Output, %keyfile%

    ; Here are the current assignments for the hotkeys. Change them to your likings.
    ; Refer to AutoHotkey documentation for more information.
    ; https://www.autohotkey.com/docs/AutoHotkey.htm

    ; {NumLock}:         Change modes
    ;
    ; ########## [Mode 1: Application Shortcuts] ##########
    ;
    ; {Num/}             Play/Pause (Media Key)
    ; {Num*}             Mute (Media Key)
    ; {Num-}             Volume Down (Media Key)
    ; {Num+}             Volume Up (Media Key)
    ;
    ; {NumBackspace}     N/A
    ; {NumEnter}         Open "This PC" (Explorer)
    ; {Num.}             N/A
    ; {Num0}             Launch Firefox
    ;
    ; {Num1}             N/A
    ; {Num2}             N/A
    ; {Num3}             N/A
    ; {Num4}             N/A
    ; {Num5}             N/A
    ; {Num6}             N/A
    ;
    ; {Num7}             N/A
    ; {Num8}             N/A
    ; {Num9}             N/A
    ;
    ; ########## [Mode 2: OBS Mode] ##########
    ;
    ; {Num/}             N/A
    ; {Num*}             N/A
    ; {Num-}             N/A
    ; {Num+}             N/A
    ;
    ; {NumBackspace}     N/A
    ; {NumEnter}         N/A
    ; {Num.}             N/A
    ;
    ; {Num0}             N/A
    ;
    ; {Num1}             N/A
    ; {Num2}             N/A
    ; {Num3}             N/A
    ; {Num4}             N/A
    ; {Num5}             N/A
    ; {Num6}             N/A
    ; {Num7}             N/A
    ; {Num8}             N/A
    ; {Num9}             N/A
    ;
    ; ########## [Mode 3: N/A] ##########
    ;
    ; {Num/}             N/A
    ; {Num*}             N/A
    ; {Num-}             N/A
    ; {Num+}             N/A
    ;
    ; {NumBackspace}     N/A
    ; {NumEnter}         N/A
    ; {Num.}             N/A
    ; {Num0}             N/A
    ;
    ; {Num1}             N/A
    ; {Num2}             N/A
    ; {Num3}             N/A
    ; {Num4}             N/A
    ; {Num5}             N/A
    ; {Num6}             N/A
    ; {Num7}             N/A
    ; {Num8}             N/A
    ; {Num9}             N/A
    ;
    ; ########## [Mode 4: N/A] ##########
    ;
    ; {Num/}             N/A
    ; {Num*}             N/A
    ; {Num-}             N/A
    ; {Num+}             N/A
    ;
    ; {NumBackspace}     N/A
    ; {NumEnter}         N/A
    ; {Num.}             N/A
    ; {Num0}             N/A
    ;
    ; {Num1}             N/A
    ; {Num2}             N/A
    ; {Num3}             N/A
    ; {Num4}             N/A
    ; {Num5}             N/A
    ; {Num6}             N/A
    ; {Num7}             N/A
    ; {Num8}             N/A
    ; {Num9}             N/A
    ;

    if (Output == Numpad["numlock"]) {
        if (mode == max_modes)
            mode := 1

        else {
            mode++
        }

        Send, {NumLock} ; To restore the previous state of NumLock.
        notification := "Using mode #" . mode . " of " . max_modes . " modes (" . mode_names[mode] . ")"
        TrayTip, "Macropad Mode Change", %notification%, 17
        ; ? For troubleshooting only. Useless...
        ;MsgBox, , "Macropad Mode Change", %notification%, 3
        Return
    }

    else if (mode == 1) {
        if (Output == Numpad["/"]) {
            Send, {Media_Play_Pause}
            Return
        }

        else if (Output == Numpad["*"]) {
            Send, {Volume_Mute}
            Return
        }

        else if (Output == Numpad["-"]) {
            Send, {Volume_Down}
            Return
        }

        else if (Output == Numpad["+"]) {
            Send, {Volume_Up}
            Return
        }

        else if (Output == Numpad["backspace"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["enter"]) {
            Run, ::{20d04fe0-3aea-1069-a2d8-08002b30309d}
            Return
        }

        else if (Output == Numpad["."]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["0"]) {
            Run, firefox.exe
            Return
        }

        else if (Output == Numpad["1"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["2"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["3"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["4"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["5"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["6"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["7"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["8"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["9"]) {
            ; Command here
            Return
        }

        Return
    }

    else if (mode == 2) {
        if (Output == Numpad["/"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["*"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["-"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["+"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["backspace"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["enter"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["."]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["0"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["1"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["2"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["3"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["4"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["5"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["6"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["7"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["8"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["9"]) {
            ; Command here
            Return
        }

        Return
    }

    else if (mode == 3) {
        if (Output == Numpad["/"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["*"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["-"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["+"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["backspace"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["enter"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["."]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["0"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["1"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["2"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["3"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["4"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["5"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["6"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["7"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["8"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["9"]) {
            ; Command here
            Return
        }

        Return
    }

    else if (mode == 4) {
        if (Output == Numpad["/"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["*"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["-"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["+"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["backspace"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["enter"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["."]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["0"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["1"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["2"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["3"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["4"]) {
            ; Command here
            Return
        }

        else if (Output == Numpad["5"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["6"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["7"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["8"]) {
            ; Command here
            Return
        }
        else if (Output == Numpad["9"]) {
            ; Command here
            Return
        }

        Return
    }

;Return needs to be at the end of every hotkey
Return