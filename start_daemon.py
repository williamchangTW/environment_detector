# Automation to check environment
import subprocess, os

def startDAEMON():
	path = os.getcwd()
	subprocess.Popen(args=["gnome-terminal", "--command=python3 " + path + "./environment_detector/envir_daemon.py"], shell=False)

