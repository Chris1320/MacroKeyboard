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
    MsgBox,, "F24 Detected", "Detected input: %Output%"
