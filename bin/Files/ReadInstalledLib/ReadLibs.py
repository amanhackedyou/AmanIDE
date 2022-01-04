import re
import os
import subprocess as sp


def getInstalledMods():
	binFls = os.listdir("/usr/lib/")
	pythonDirName = "/usr/lib/"
	for flnm in binFls:
		if(re.match("python3..", flnm)):
			pythonDirName = pythonDirName+flnm
			break

	moduleName = os.listdir(pythonDirName)
	modFormate = ""
	for module in moduleName:
		module = module.replace(".py", "")
		modFormate += module+"|"

	modFormate+="Aman"
	return modFormate

if __name__ == "__main__":
	print(getInstalledMods())

