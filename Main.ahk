#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
#InstallKeybdHook ;Makes the script monitor keystrokes for hotkeys not supported by default windows registry, improves responsiveness
#UseHook On ;Forces script to use keyboard hook for all hotkeys
#SingleInstance force ;Makes sure you don't accidentally have multiple versions of this script running at one time
#KeyHistory 200 ;how many events the key history will record, useful for debugging
#MenuMaskKey vk07 ;Menu masking may unintentionally send additional keystrokes when using Alt as a modifier, this prevents that
#WinActivateForce ;prevent taskbar flashing.
#Persistent

SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SendMode Input ;Sets the default method any commands will be sent. Overwritten by ControlSend commands but good to have to prevent issues when tinkering in the future
SetTitleMatchMode, RegEx
SetKeyDelay, -1, 50
; DetectHiddenWindows, On  ; This makes ControlSend not work in OBS Studio mode.

if not A_IsAdmin
{
   Run *RunAs "%A_ScriptFullPath%"  ; Requires v1.0.92.01+
   ExitApp
}

configfile := "./config.txt"  ; The path of the configuration file
                              ; (Change this if you want to use a
                              ;       different configuration file)

; FIXME: How do I put a dictionary into config.txt? (DEV0004)

mode := 1 ; The default mode
max_modes := 2 ; How many "modes" do we have?
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
            if (keyfile_found == 1)
            {
                keyfile := StrSplit(cvalue, "=")[2]
            }

            Break  ; Stop the second (by-character) loop.
        }
    }
}

if (keyfile == "")
{
    MsgBox, , "Configuration File Read Error", "The configuration file lacks the neccessary data!"
    Exit, 2
}

; MsgBox,, "Configfile Values", Keyfile:%keyfile%  ; For debugging only (DEV0005)

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
F24::

    ;Read the file key.txt and outputs the result in a variable named Output
    FileRead, Output, D:/Scripts/MacroKeyboard/key.txt

    ; Here are the current assignments for the hotkeys. Change them to your likings.
    ; Refer to AutoHotkey documentation for more information.
    ; https://www.autohotkey.com/docs/AutoHotkey.htm

    ; {NumLock}:         Change modes
    ;
    ; ########## [Mode 1: Application Shortcuts] ##########
    ;
    ; {Num/}             Previous (Media Key)
    ; {Num*}             Next (Media Key)
    ; {Num-}             Volume Down (Media Key)
    ; {Num+}             Volume Up (Media Key)
    ;
    ; {NumBackspace}     Reload Voicemeeter Settings
    ; {NumEnter}         Duck S4 (Voicemeeter)
    ; {Num.}             Play/Pause (Media Key)
    ; {Num0}             Toggle Microphone (Toggle Voicemeeter)
    ;
    ; {Num1}             Firefox
    ; {Num2}             Open "This PC" (Explorer)
    ; {Num3}             Obsidian
    ; {Num4}             MusicBee
    ; {Num5}             OBS Studio
    ; {Num6}             Turn off Monitor
    ;
    ; {Num7}             Mute A1 (Voicemeeter)
    ; {Num8}             Mute A2 (Voicemeeter)
    ; {Num9}             Mute A3 (Voicemeeter)
    ;
    ; ########## [Mode 2: OBS Mode] ##########
    ;
    ; {Num/}             N/A
    ; {Num*}             Toggle AFK Mode (OBS Studio)
    ; {Num-}             Volume Down (Media Key)
    ; {Num+}             Volume Up (Media Key)
    ;
    ; {NumBackspace}     Pause/Resume Recording (OBS Studio)
    ; {NumEnter}         Start/Stop Recording (OBS Studio)
    ; {Num.}             Start/Stop Virtual Camera (OBS Studio)
    ; {Num0}             Toggle Microphone (Voicemeeter)
    ;
    ; {Num1}             Go to Scene 1 (OBS Studio)
    ; {Num2}             Go to Scene 2 (OBS Studio)
    ; {Num3}             Go to Scene 3 (OBS Studio)
    ; {Num4}             Go to Scene 4 (OBS Studio)
    ; {Num5}             Go to Scene 5 (OBS Studio)
    ; {Num6}             Go to Scene 6 (OBS Studio)
    ; {Num7}             Go to Scene 7 (OBS Studio)
    ; {Num8}             Go to Scene 8 (OBS Studio)
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
            Send, {Media_Prev}
            Return
        }

        else if (Output == Numpad["*"]) {
            Send, {Media_Next}
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
            Send, ^{Numpad9}
            Return
        }

        else if (Output == Numpad["enter"]) {
            Send, !{Numpad9}
            Return
        }

        else if (Output == Numpad["."]) {
            Send, {Media_Play_Pause}
            Return
        }

        else if (Output == Numpad["0"]) {
            Send, !{Numpad7}
            Return
        }

        else if (Output == Numpad["1"]) {
            Send, ^{F19}
            Return
        }

        else if (Output == Numpad["2"]) {
            ; Opens "This PC" folder (From `https://www.autohotkey.com/docs/commands/Run.htm`)
            Run, ::{20d04fe0-3aea-1069-a2d8-08002b30309d}
            Return
        }

        else if (Output == Numpad["3"]) {
            Send, ^{F20}
            Return
        }

        else if (Output == Numpad["4"]) {
            Send, ^{F21}
            Return
        }

        else if (Output == Numpad["5"]) {
            Send, ^{F22}
            Return
        }

        else if (Output == Numpad["6"]) {
            Sleep 100 ; if you use this with a hotkey, not sleeping will make it so your keyboard input wakes up the monitor immediately
            SendMessage 0x112, 0xF170, 2,,Program Manager ; send the monitor into standby (off) mode
            Return
        }

        else if (Output == Numpad["7"]) {
            Send, ^{F1}
            Return
        }

        else if (Output == Numpad["8"]) {
            Send, ^{F2}
            Return
        }

        else if (Output == Numpad["9"]) {
            Send, ^{F3}
            Return
        }

        Return
    }

    else if (mode == 2) {
        if (WinExist("ahk_exe obs64.exe")) {
            ;if (WinActive("ahk_exe obs64.exe")) {  ; For debugging purposes only
            ;    MsgBox, , OBS Studio, Active, 3
            ;} else {
            ;    MsgBox, , OBS Studio, Inactive, 3
            ;}

            if (Output == Numpad["/"]) {
                Return
            }

            else if (Output == Numpad["*"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, ^{F13}
                }

                else {
                    ControlSend, , ^{F13}, ahk_exe obs64.exe
                }
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
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, ^{F14}
                }

                else {
                    ControlSend, , ^{F14}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["enter"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, ^{F15}
                }

                else {
                    ControlSend, , ^{F15}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["."]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, ^{F16}
                }

                else {
                    ControlSend, , ^{F16}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["0"]) {
                Send, !{Numpad7}
                Return
            }

            else if (Output == Numpad["1"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F13}
                }

                else {
                    ControlSend, , !{F13}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["2"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F14}
                }

                else {
                    ControlSend, , !{F14}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["3"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F15}
                }

                else {
                    ControlSend, , !{F15}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["4"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F16}
                }

                else {
                    ControlSend, , !{F16}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["5"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F17}
                }

                else {
                    ControlSend, , !{F17}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["6"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F18}
                }

                else {
                    ControlSend, , !{F18}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["7"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F19}
                }

                else {
                    ControlSend, , !{F19}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["8"]) {
                if (WinActive("ahk_exe obs64.exe")) {
                    Send, !{F20}
                }

                else {
                    ControlSend, , !{F20}, ahk_exe obs64.exe
                }
                Return
            }

            else if (Output == Numpad["9"]) {
                Return
            }
        }

        else
        {
            MsgBox, , Macropad Warning, OBS Studio is not started. Please start it first., 3
            Return
        }

        Return
    }

    else if (mode == 3) {
        if (Output == Numpad["enter"])
            MsgBox, , "Macropad", "This mode is not configured yet.", 3

        Return
    }

    else if (mode == 4) {
        if (Output == Numpad["enter"])
            MsgBox, , "Macropad", "This mode is not configured yet.", 3

        Return
    }

;Return needs to be at the end of every hotkey
Return