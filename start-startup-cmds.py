#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

I combined ConfigHandler and start-startup-cmds to keep it as a single file.

============================== ConfigHandler License ==============================

MIT License
Copyright (c) 2020 Chris1320

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import time
import subprocess

def info(msg):
	"""
	Print <msg> with format.

	:param str msg: The message to print.

	:returns void:
	"""

	print(f"    * {msg}")

class Process(object):
	"""
	Use for starting a process.
	"""

	def __init__(self, name: str, proc_name: str, path: str, use_subprocess: bool, restartable: bool):
		"""
		The initialization method of Process() class.

		:param str name:            The name of the process (For printing in STDOUT)
		:param str proc_name:       The process name (For checking process in tasklist)
		:param str path:            The path of the file to run if <proc_name> is not in tasklist output.
		:param bool use_subprocess: Use `subprocess.getoutput()` command instead of `os.startfile()` command.
		:param bool restartable:    If true, it can be restarted by the script.
		"""

		self.name = name
		self.proc_name = proc_name
		self.path = path
		self.use_subprocess = use_subprocess
		self.type = "process"
		self.restartable = restartable

	def start(self, force_restart: bool):
		"""
		Start the process by calling <self.path>.

		:param bool force_restart: Kill <self.proc_name> processes using `taskkill`.

		:returns int: The error code.
		"""

		info(f"Checking {self.name}...")
		if self.process_exists():
			if force_restart and self.restartable:
				info(f"Killing {self.proc_name} processes for restart...")
				subprocess.getoutput(f"taskkill /IM {self.proc_name} /F")

			else:
				info(f"{self.name} is already running...")
				return 0  # Return 0 if process already exists.

		try:
			if self.use_subprocess:
				subprocess.Popen(self.path)  # ! DEV0001: Needs Tuple if use_subprocess is True.
				# ? In other words, how to use this by entering a string parameter?

			else:
				os.startfile(self.path)

		except FileNotFoundError:
			info(f"Cannot find `{self.path}`...")
			return 11  # Return 11 if it cannot find <self.path>.

		else:
			info(f"{self.name} has started...")
			return 0  # Return 0 if <self.path> is executed successfully.

	def process_exists(self):
		"""
		Check if <self.proc_name> is already running.

		:returns bool: True if process exists, return True.
		"""

		call = 'TASKLIST', '/FI', 'imagename eq %s' % self.proc_name
		# use built-in check_output right away
		output = subprocess.check_output(call).decode()
		# check in last line for process name
		last_line = output.strip().split('\r\n')[-1]
		# because Fail message could be translated
		return last_line.lower().startswith(self.proc_name.lower())

class Service(object):

	def __init__(self, name: str, serv_name: str, nssm: bool, restartable: bool):
		"""
		The initialization method of Process() class.

		:param str name: The name of the service (For use with info())
		:param str serv_name: The service name (For use as argument to sc/nssm)
		:param bool nssm: If true, use NSSM. Otherwise, use SC.
		:param bool restartable: If true, it can be restarted by the script.
		"""

		self.name = name
		self.serv_name = serv_name
		self.nssm = nssm
		self.type = "service"
		self.restartable = restartable

	def start(self, force_restart: bool):
		"""
		Start the process by calling <self.path>.

		:param bool force_restart: If True, it will restart the service instead of skipping it.
		"""

		if self.nssm:
			if subprocess.getoutput(f"nssm status {self.serv_name}") == "SERVICE_RUNNING":
				if force_restart and self.restartable:
					subprocess.getoutput(f"nssm restart {self.serv_name}")
					while True:
						if subprocess.getoutput(f"nssm status {self.serv_name}") == "SERVICE_RUNNING":
							info(f"{self.name} has been restarted...")
							break

				else:
					if force_restart:
						info("Service is already running. (Service not restartable)")

					else:
						info("Service is already running.")

			else:
				subprocess.getoutput(f"nssm start {self.serv_name}")
				while True:
					if subprocess.getoutput(f"nssm status {self.serv_name}") == "SERVICE_RUNNING":
						info(f"{self.name} has been started...")
						break

		else:
			if force_restart and self.restartable:
				subprocess.getoutput(f"sc stop {self.serv_name}")  # ! DEV0001: Script cannot detect when access is denied.
				# time.sleep(5)  # We'll use this if the while loop fails.

				info("Waiting for service to completely stop...")
				while True:
					if "STOPPED" in subprocess.getoutput(f"sc query {self.serv_name}").split('\n')[3]:
						info("Service has been stopped.")
						break

			if "An instance of the service is already running." in subprocess.getoutput(f"sc start {self.serv_name}"):
				if force_restart and not self.restartable:
					info("Service is already running. (Service not restartable)")

				else:
					info("Service is already running.")

			else:
				info("Starting service...")
				while True:
					if "RUNNING" in subprocess.getoutput(f"sc query {self.serv_name}").split('\n')[3]:
						info(f"{self.name} has been started...")
						break

		return 0

print("Starting startup commands...")

class Main():

	def __init__(self):
		# self.name = sys.argv[0][::-1].partition(os.sep)[0][::-1][::-1].partition('.')[2][::-1]  # Get the filename but not the file extension.
		# self.configpath = f"D:/Scripts/{self.name}.conf"  # This is hardcoded; This is where the configuration file is located.

		self.cmds = [
			Service(
				name = "NetLimiter 4",
				serv_name = "NLSvc",
				nssm = False,
				restartable = False
			),
			Process(
				name = "NetLimiter 4",
				proc_name = "NLClientApp.exe",
				path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/NetLimiter 4/NetLimiter 4 64 bit.lnk",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "Graphic Tablet Driver",
				proc_name = "TabletDriver.exe",
				path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/PenTabletDriver/PenTabletDriver.lnk",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "MSI Afterburner",
				proc_name = "MSIAfterburner.exe",
				path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/MSI Afterburner.lnk",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "Rainmeter",
				proc_name = "Rainmeter.exe",
				path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Rainmeter.lnk",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "SuperF4",
				proc_name = "SuperF4.exe",
				path = "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/SuperF4.lnk",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "Voicemeeter Banana",
				proc_name = "voicemeeterpro.exe",
				path = "C:/Users/Chris3120/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/VB Audio/Voicemeeter/Voicemeeter Banana.lnk",
				use_subprocess = False,
				restartable = False
			),
			Service(
				name = "Ombi",
				serv_name = "Ombi",
				nssm = True,
				restartable = True
			),
			Service(
				name = "Jellyfin Server",
				serv_name = "JellyfinServer",
				nssm = False,
				restartable = True
			),
			Process(
				name = "Jellyfin Server Tray",
				proc_name = "Jellyfin.Windows.Tray.exe",
				path = "C:/Program Files/Jellyfin/Server/Jellyfin.Windows.Tray.exe",
				use_subprocess = False,
				restartable = False
			),
			Process(
				name = "LuaMacros",
				proc_name = "LuaMacros.exe",
				path = ("D:\System\LuaMacros\LuaMacros.exe", "-r", "D:\\Scripts\\MacroKeyboard\\2nd_keyboard.lua"),
				use_subprocess = True,
				restartable = True
			),
			Process(
				name = "AutoHotkey",
				proc_name = "AutoHotkey.exe",
				path = "D:\Scripts\MacroKeyboard\Main.ahk",
				use_subprocess = False,
				restartable = True
			)
		]

	def main(self):
		"""
		:returns int: The number of "faulty" cmds.
		"""

		faulty = 0

		force_restart = False  # Set default value of <force_restart> variable.

		try:  # Check if switch is present from command.
			if sys.argv[1].startswith(("-r", "--restart")):  # If these are present in command, change value of <force_restart> to True.
				force_restart = True

		except IndexError:
			# If there are no  other arguments from command, never mind it.
			pass

		print()
		print("Active Switches:")
		if force_restart:
			print("[X] Restart (-r/--restart)")

		else:
			print("[ ] Restart (-r/--restart)")

		print()
		print()
		print()

		for item in self.cmds:  # Run the classes from <self.cmds>.
			if item.type == "process":
				print("[i] Starting {0} process.".format(item.name))

			else:
				print("[i] Starting/Restarting {0} service.".format(item.name))

			if item.start(force_restart) != 0:
				faulty += 1

		print("[!] Done! ({0}/{1} faulty cmds)".format(faulty, len(self.cmds)))
		countdown = 5
		while countdown != 0:
			try:
				print(f"Exiting in {countdown}s...")
				time.sleep(1)
				countdown -= 1

			except(KeyboardInterrupt, EOFError):
				break

		return faulty

if __name__ == "__main__":
	sys.exit(Main().main())
