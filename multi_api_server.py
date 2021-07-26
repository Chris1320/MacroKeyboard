
"""
multi_api_server.py

This script acts as a server that waits for
client command and execute API commands.
"""

import os
import pickle
import sys
import time
import pickle
import socket
import hashlib
import subprocess
from pathlib import Path

import voicemeeter
import obswebsocket

from ConfigHandler import config_handler


class VoicemeeterAPI():
    """
    Handles Voicemeeter API calls.

    NOTE: This API wrapper hasn't been tested on Voicemeeter
          applications other than Voicemeeter Banana.
    """

    # * TODO: Support commands like from Macro.Buttons (DEV0004)
    #
    # Sample Command: Duck S4
    #
    # Strip(3).fadeto = (-20.0, 250);
    # Strip(3).EQGain2 = -12.0;
    #

    def __init__(self, kind_id: int):
        """
        The initialization method of Main() class.

        :param int kind_id: The kind of Voicemeeter to start. (See `self.kinds`)
        """

        self.kinds = ("basic", "banana", "potato")
        self.kind_id = kind_id

        self.remote = voicemeeter.remote(self.kinds[self.kind_id])
        self.remote.login()

    def start_voicemeeter(self):
        """
        Starts voicemeeter or if already running, put to foreground.

        :returns void:
        """

        voicemeeter.launch(self.kinds[self.kind_id])

        return None

    def restart(self):
        """
        Restarts voicemeeter audio engine.

        :returns void:
        """

        self.remote.restart()

        return None

    def _mute_input(self, channel: int, state: bool = None):
        """
        Sets the "mute" state of a strip.

        :param int channel: Strip number. (Index starts at 0)
        :param bool state: Set `True` to mute. (Optional)

        :returns void:
        """

        if state is None:
            state = not self.remote.inputs[channel].mute  # Invert value of mute.

        self.remote.inputs[channel].mute = state

        return None

    def _gain_input(self, channel: int, value: float, absolute: bool = True):
        """
        Sets the gain value of a strip.

        :param int channel: Strip number. (Index starts at 0)
        :param float value: Gain value from `-60.0` to `12.0`.
        :param bool absolute: If set to `True`, set the gain value to <value>.
                Otherwise, add <value> to current gain value.

        :returns void:
        """


        if absolute:
            # Check if value is valid first...
            if value < -60.0 or value > 12.0:
                raise ValueError("value must be `-60.0` or `12.0` only!")

            self.remote.inputs[channel].gain = value

        else:
            new_value = self.remote.inputs[channel].gain + value
            # Check if the sum is within acceptable range...
            if new_value < -60.0:
                self.remote.inputs[channel].gain = -60.0

            elif new_value > 12.0:
                self.remote.inputs[channel].gain = 12.0

            else:
                self.remote.inputs[channel].gain = new_value

        return None

    def _mute_output(self, channel: int, state: bool = None):
        """
        Sets the "mute" state of a bus.

        :param int channel: Bus number. (Index starts at 0)
        :param bool state: Set `True` to mute. (Optional)

        :returns void:
        """

        if state is None:
            state = not self.remote.outputs[channel].mute  # Invert value of variable.

        self.remote.outputs[channel].mute = state

        return None

    def _gain_output(self, channel: int, value: float, absolute: bool = True):
        """
        Sets the gain value of a bus.

        :param int channel: Bus number. (Index starts at 0)
        :param float value: Gain value from `-60.0` to `12.0`.
        :param bool absolute: If set to `True`, set the gain value to <value>.
                Otherwise, add <value> to current gain value.

        :returns void:
        """


        if absolute:
            # Check if value is valid first...
            if value < -60.0 or value > 12.0:
                raise ValueError("value must be `-60.0` or `12.0` only!")

            self.remote.outputs[channel].gain = value

        else:
            new_value = self.remote.outputs[channel].gain + value
            # Check if the sum is within acceptable range...
            if new_value < -60.0:
                self.remote.outputs[channel].gain = -60.0

            elif new_value > 12.0:
                self.remote.outputs[channel].gain = 12.0

            else:
                self.remote.outputs[channel].gain = new_value

        return None

    def mute(self, channel: str, index: int, state: bool = None):
        """
        Mute an input/output.

        :param str channel: Either "input" or "output".
        :param int index: Strip/Bus number. (Index starts at 1)
        :param bool state: Set `True` to mute. (Optional)

        :returns void:
        """

        if channel == "input":
            self._mute_input(index - 1, state)

        elif channel == "output":
            self._mute_output(index - 1, state)

        else:
            raise ValueError("Invalid channel value.")

    def solo(self, channel: int, state: bool = None):
        """
        Sets the "solo" state of a strip.

        :param int channel: Strip number. (Index starts at 0)
        :param bool state: Set `True` to activate solo mode. (Optional)

        :returns void:
        """

        if state is None:
            state = not self.remote.inputs[channel].solo  # Invert value of mute.

        self.remote.inputs[channel].solo = state

        return None

    def gain(self, channel: str, index: int, value: float, absolute: bool = True):
        """
        Adjust gain of an input/output.

        :param str channel: Either "input" or "output".
        :param int index: Strip/Bus number. (Index starts at 1)
        :param float value: The value of the gain slider.
        :param bool absolute: Set `True` to set the value instead of
                            adding to the current gain value. (Optional)

        :returns void:
        """

        if channel == "input":
            self._gain_input(index - 1, value, absolute)

        elif channel == "output":
            self._gain_output(index - 1, value, absolute)

        else:
            raise ValueError("Invalid channel value.")


class OBSWebSocketAPI():
    """
    Handles OBS Studio's OBS-Websocket plugin API calls.
    """

    def __init__(
        self,
        obs_host: str = "127.0.0.1",
        obs_port: int = 4444,
        obs_pass: str = None,
        obs_path: str = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
    ):
        """
        The initialization method of OBSWebSocketAPI() class.

        :param str obs_host: The IP address of the machine that has OBS Studio running.
        :param int obs_port: The listening port of OBS-Websocket.
        :param str obs_pass: OBS-Websocket password. (if enabled)
        """

        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_pass = obs_pass

        self.wdpath = Path(obs_path).parent
        self.exepath = obs_path
        self.cwd = os.getcwd()

        self.client = obswebsocket.obsws(self.obs_host, self.obs_port, self.obs_pass)
        self.connected = False

    def start_obs(self):
        """
        Start OBS Studio.

        :returns void:
        """

        # Check if self.wdpath exists first.
        # if os.path.isdir(self.wdpath) and self.wdpath != '.':
        # Start the file.
        # ! Not yet implemented (DEV0001)

        return None

    def connect(self):
        """
        Attempt to connect to OBS-Websocket.

        :returns tuple: Error code and the reason.
        """

        try:
            self.client.connect()

        except(obswebsocket.exceptions.ConnectionFailure) as e:
            self.connected = False
            return (1, e)

        except Exception as e:
            self.connected = False
            return (2, e)

        else:
            self.connected = True
            return (0, "OK.")

    def call(self, command: dict):
        """
        Make a call to OBS-Websocket.

        :param str dict: The command to send.

        :returns dict: Response from the server.
        """

        if self.connected:
            return self.client.send(command)

        else:
            return {
                "message-id": command["message-id"],
                "status": "error",
                "error": "Not yet connected."
            }

    def disconnect(self):
        """
        Disconnect from OBS-Websocket.
        """

        self.client.disconnect()
        self.connected = False


class Main():

    def __init__(self, **kwargs):
        """
        The initialization method of Main() class.
        """

        # Check if user is trying to use a custom config file.
        try:
            config_file = sys.argv[1]
            if not os.path.exists(config_file):
                print("ERROR: Defined configuration file path not found. Using default...")
                config_file = "./config.txt"

        except IndexError:
            config_file = "./config.txt"

        self.config = config_handler.Version1(config_file, False)

        self.obs_host = self.config.get("obs_host")
        self.obs_port = self.config.get("obs_port")
        self.obs_pass = self.config.get("obs_pass")
        self.api_server = (self.config.get("host"), self.config.get("port"))
        self.voicemeeter_kind = self.config.get("voicemeeter_kind")
        self.client_address_whitelist = self.config.get("whitelist").split(',')

        # Initialize Voicemeeter API.
        self.VoicemeeterAPI = VoicemeeterAPI(self.voicemeeter_kind)

        # Initialize OBS-Websocket API
        self.OBSWebSocketAPI = OBSWebSocketAPI(
            obs_host=self.obs_host,
            obs_port=self.obs_port,
            obs_pass=self.obs_pass
        )

        self.responses = {
            0: "OK.",
            1: "Blocked.",
            2: "Unknown command.",
            3: "Invalid parameter.",
            4: "Insufficient arguments."
        }

        self._initialized = True

    def parse_data(self, data: list):
        """
        Parse the command-line arguments from the client.

        :param list data: Data sent by the client.

        :returns list: The error code and command output. `[<errcode>, <output>]`
        """

        i = 1  # iterator

        # * The iterator starts with 1 because 0 is the filename.

        while i < len(data):
            if data[i].startswith("voicemeeter"):
                try:
                    command = data[i + 1]

                except(IndexError):
                    return [
                        0,
                        f"""
{data[0]} voicemeeter <commands> <parameters>

Commands: (All index starts at 1)

start                                                             Start Voicemeeter.
restart                                                           Restarts voicemeeter audio engine.
gain <input|output> <strip/bus index> <value> <absolute>          Set gain for a strip/bus.
                                            value:    value of the gain slider (-60.0 ~ 12.0)
                                            absolute: if false, add <value> to current value.
                                                      (Optional; defaults to `true`)
mute <input|output> <strip/bus index> <true|false>                Mute an input/output.
solo <strip index> <true|false>                                   Sets the "solo" state of a strip.
"""
                    ]

                else:
                    if command == "start":
                        self.VoicemeeterAPI.start_voicemeeter()  # Starts Voicemeeter application on system.
                        return [0, self.responses[0]]

                    elif command == "restart":
                        self.VoicemeeterAPI.restart()
                        return [0, self.responses[0]]

                    elif command == "gain":
                        try:  # <input|output>
                            if data[i + 2] == "input":
                                channel = "input"

                            elif data[i + 2] == "output":
                                channel = "output"

                            else:
                                return [3, self.responses[3]]

                        except(IndexError):
                            return [3, self.responses[3]]

                        try:  # <strip/bus index>
                            index = int(data[i + 3])

                        except(IndexError, TypeError):
                            return [3, self.responses[3]]

                        try:  # <value>
                            value = float(data[i + 4])

                        except(IndexError, TypeError):
                            return [3, self.responses[3]]

                        try:  # <absolute>
                            if data[i + 5] == "true":
                                absolute = True

                            elif data[i + 5] == "false":
                                absolute = False

                            else:
                                absolute = True

                        except(IndexError):
                            absolute = True

                        # Send the API call.
                        try:
                            self.VoicemeeterAPI.gain(channel, index, value, absolute)
                            return [0, self.responses[0]]

                        except IndexError:
                            return [3, self.responses[3]]

                    elif command == "mute":
                        # First, get the parameters.
                        try:  # <input|output>
                            if data[i + 2] == "input":
                                channel = "input"

                            elif data[i + 2] == "output":
                                channel = "output"

                            else:
                                return [3, self.responses[3]]

                        except IndexError:
                            return [3, self.responses[3]]

                        try:  # <strip/bus index>
                            index = int(data[i + 3])

                        except(TypeError, IndexError):
                            return [3, self.responses[3]]

                        try:  # <true|false>
                            if data[i + 4] == "true":
                                state = True

                            elif data[i + 4] == "false":
                                state = False

                            else:
                                return [3, self.responses[3]]

                        except IndexError:
                            return [3, self.responses[3]]

                        # Send the command to the API.
                        try:
                            self.VoicemeeterAPI.mute(channel, index, state)

                        # IndexError is raised when index (the variable)
                        # is out of range. (i.e, In Voicemeeter Banana,
                        # there are only 5 inputs.)
                        except IndexError:
                            return [3, self.responses[3]]

                        else:
                            return [0, self.responses[0]]

                    elif command == "solo":
                        try:  # <strip index>
                            index = int(data[i + 2])

                        except(TypeError, IndexError):
                            return [3, self.responses[3]]

                        try:  # <true|false>
                            if data[i + 3] == "true":
                                state = True

                            elif data[i + 3] == "false":
                                state = False

                            else:
                                return [3, self.responses[3]]

                        except IndexError:
                            return [3, self.responses[3]]

                        try:
                            # Send the command to API.
                            self.VoicemeeterAPI.solo(index - 1, state)

                        except IndexError:
                            return [3, self.responses[3]]

                        else:
                            return [0, self.responses[0]]

                    else:
                        return [2, self.responses[2]]

            elif data[i].startswith("obs"):
                try:
                    command = data[i + 1]

                except(IndexError):
                    return [
                        0,
                        f"""
{data[0]} obs <commands> <parameters>

Commands:

start                                 Start OBS Studio. (Not yet implemented)
connect                               Connect to OBS Studio.
disconnect                            Disconnect to OBS Studio.
command <command> <parameters>        * Send <command> with <parameters> parameters.

Examples:

<client> obs command StartRecording  # Starts recording.
<client> obs command SetCurrentScene --scene-name=scene1  # Switch to "scene1" scene.

* See `https://github.com/Palakis/obs-websocket/blob/4.x-current/docs/generated/protocol.md` for more information.
"""
                    ]

                else:
                    if command == "start":
                        self.OBSWebSocketAPI.start_obs()  # Starts OBS Studio
                        return [0, self.responses[0]]

                    elif command == "connect":
                        return self.OBSWebSocketAPI.connect()

                    elif command == "disconnect":
                        self.OBSWebSocketAPI.disconnect()
                        return [0, self.responses[0]]

                    elif command == "command":
                        try:
                            obs_request = {
                                "request-type": data[i + 2],
                                "message-id": hashlib.sha1(time.asctime().encode()).hexdigest().upper()
                            }

                        except(IndexError):
                            return [4, self.responses[4]]

                        _ = i + 2  # Iterator for the while loop below.
                        while _ < len(data):
                            if data[_] == obs_request["request-type"]:
                                pass  # Do nothing

                            elif data[_].startswith("--"):
                                obs_request[data[_].partition("--")[2].partition('=')[0]] = data[_].partition('=')[2]

                            _ += 1

                        response = self.OBSWebSocketAPI.call(obs_request)

                        return [0, response]

                    else:
                        return [2, self.responses[2]]

            else:
                return [2, self.responses[2]]

            i += 1  # Iterate

        return [4, self.responses[4]]

    def cleanup(self):
        """
        Do some housekeeping before shutting down.

        :returns void:
        """

        self.OBSWebSocketAPI.disconnect()

        return None

    def main(self):
        """
        The main method of Main() class. Starts the server.

        :returns int: Error code.
        """

        if not self._initialized: return 1

        print("[i] Starting...")

        obs_connect = self.OBSWebSocketAPI.connect()
        if obs_connect[0] != 0:
            print("[!] OBS-Websocket API:", obs_connect[1])

        # Start listening on <self.server>:<self.port>
        print(f"[Server] Starting to listen on `{self.api_server[0]}:{self.api_server[1]}`.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(self.api_server)
            server.listen(5)
            while True:
                client, address = server.accept()
                # Check the whitelist first.
                if address[0] not in self.client_address_whitelist:
                    print(f"[Server] Connection blocked from `{address[0]}:{address[1]}`.")
                    client.sendall(pickle.dumps([1, self.responses[1]]))
                    continue

                print(f"[Server] Accepted connection from `{address[0]}:{address[1]}`.")
                data = pickle.loads(client.recv(4096))
                print("    Data Recieved:",data)  # DEV0005
                if "--shutdown" in data:
                    print("[i] Shutdown recieved. Now quitting.")
                    client.sendall(pickle.dumps([0, self.responses[0]]))
                    # print("    Error Code: 0")
                    print("    Data Sent:", [0, self.responses[0]])
                    self.cleanup()
                    return 0

                elif ("--help" in data) or "-h" in data:
                    # This is the help panel of the program.
                    # These are the commands available from the client,
                    # NOT for the server.
                    helpstring = f"""
{sys.argv[0]} <switches|commands>

Switches:

--help        -h        Show this help menu.
--shutdown              Shutdown the server.

Commands:

obs                     Send a command to OBS-Websocket API.
voicemeeter             Send a command to Voicemeeter API.
"""
                    client.sendall(pickle.dumps([0, helpstring]))
                    # print("    Error Code: 0")
                    print("    Data Sent:", [0, helpstring])

                else:
                    result = self.parse_data(data)
                    client.sendall(pickle.dumps(result))
                    # print("    Error Code:", result[0])
                    print("    Data Sent:", result)

                print("[Server] Communication done.\n")
                continue


if __name__ == "__main__":
    sys.exit(Main().main())
