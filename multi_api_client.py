"""
multi_api_client.py

This script sends API calls to multi_api_server.py
"""

import os
import sys
import pickle
import socket
# import requests

from ConfigHandler import config_handler

class Main():
    """
    The main class of multi_api_client.py.
    """

    def __init__(self):
        """
        The initialization method of Main() class.
        """

        self.configfile = "./config.txt"

    def main(self):
        """
        The main method of Main() class.
        """

        i = 1
        command = ""  # The command to be sent to the server.

        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg.startswith("--config="):
                if os.path.exists(arg.partition("=")[2]):
                    self.configfile = arg.partition("=")[2]

                else:
                    print("[E] Defined configuration file doesn't exist.")
                    return 1

            i += 1

        self.config = config_handler.Version1(self.configfile, False)  # Set config handler

        self.api_server = (self.config.get("host"), self.config.get("port"))

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.api_server)

        # Send the command to the server.
        self.client.send(pickle.dumps(sys.argv))
        self.client.close()  # Close the connection.


if __name__ == "__main__":
    sys.exit(Main().main())
