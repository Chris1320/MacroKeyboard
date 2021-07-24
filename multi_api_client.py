"""
multi_api_client.py

This script sends API calls to multi_api_server.py
"""

import os
import sys
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

        while i < len(sys.argv):
            arg = sys.argv[i]

            if arg.startswith("--config="):
                if os.path.exists(arg.partition("=")[2]):
                    self.configfile = arg.partition("=")[2]

                else:
                    print("[E] Defined configuration file doesn't exist.")
                    return 1

            i += 1

if __name__ == "__main__":
    sys.exit(Main().main())
