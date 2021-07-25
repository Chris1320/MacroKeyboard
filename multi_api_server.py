
"""
multi_api_server.py

This script acts as a server that waits for
client command and execute API commands.
"""

import os
import pickle
import sys
import pickle
import socket
# import requests
import voicemeeter
import obswebsocket

from ConfigHandler import config_handler


class VoicemeeterAPI():
    """
    Handles Voicemeeter API calls.

    NOTE: This API wrapper hasn't been tested on Voicemeeter
          applications other than Voicemeeter Banana.
    """

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

    def _solo_input(self, channel: int, state: bool = None):
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


class OBSWebSocketAPI():
    """
    Handles OBS Studio's OBS-Websocket plugin API calls.
    """

    def __init__(self, obs_host: str = "127.0.0.1", obs_port: int = 4444, obs_pass: str = None):
        """
        The initialization method of OBSWebSocketAPI() class.

        :param str obs_host: The IP address of the machine that has OBS Studio running.
        :param int obs_port: The listening port of OBS-Websocket.
        :param str obs_pass: OBS-Websocket password. (if enabled)
        """

        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_pass = obs_pass

        self.client = obswebsocket.obsws(self.obs_host, self.obs_port, self.obs_pass)

    def connect(self):
        """
        Attempt to connect to OBS Studio.
        """

        self.client.connect()


class Main():

    def __init__(self, **kwargs):
        """
        The initialization method of Main() class.
        """

        voicemeeter_kind = 1 # ? Check `VoicemeeterAPI().kinds`

        self.VoicemeeterAPI = VoicemeeterAPI(voicemeeter_kind)

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

        self.responses = {
            0: b"Ok."
        }

        self._initialized = True

    def parse_data(self):
        """
        Parse the command-line arguments from the client.
        """

        pass

    def main(self):
        """
        The main method of Main() class. Starts the server.

        :returns int: Error code.
        """

        if not self._initialized: return 1

        self.VoicemeeterAPI.start_voicemeeter()  # Starts Voicemeeter application on system.

        # Start listening on <self.server>:<self.port>
        print(f"Starting to listen on `{self.api_server[0]}:{self.api_server[1]}`.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(self.api_server)
            server.listen(5)
            while True:
                client, address = server.accept()
                print(f"Accepted connection from `{address}`.")
                data = pickle.loads(client.recv(4096))
                print("Data:",data)  # DEV0005
                if "--shutdown" in data:
                    print("[i] Shutdown recieved. Now quitting.")
                    server.sendall(pickle.dumps(self.responses[0]))
                    return 0

                elif ("--help" in data) or "-h" in data:
                    # This is the help panel of the program.
                    # These are the commands available from the client,
                    # NOT for the server.
                    helpstring = f"""
{sys.argv[0]}

--help        -h        Show this help menu.
--shutdown              Shutdown the server.
"""
                    server.sendall(pickle.dumps(helpstring))

                else:
                    server.sendall(pickle.dumps(self.parse_data(data)))

                continue


if __name__ == "__main__":
    sys.exit(Main().main())
