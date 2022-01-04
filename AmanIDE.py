#!/usr/bin/python3
print("Loading...")
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re
import os
import sys
import subprocess
from tkinter import *
from tkinter.ttk import *
from collections import deque
import tkinter.filedialog as tkfile
import tkinter.font as tkFont
import tkinter.messagebox as tmsg
sys.path.append("/usr/bin/AmanIDE/bin/Files/ReadInstalledLib/")
# AMAN CREATED MODULES
from ReadLibs import *

# IMPORTENT VARIABLE
presentFilePath = None
isFileSaved = True
stack = deque(maxlen = 10)
stackcursor = 0
Indent = 0
bgClr = "#1e1e1e"
#bgClr="#000000"


# IMPORTENT DATASET
morePack = "sys"
builtInPack = getInstalledMods()+"|"+morePack

# Function for set the root title
def setTitle():
	global isFileSaved
	currentTitle = root.title()
	if (isFileSaved == False):
		if (currentTitle[-1] == "*"):
			pass
		else:
			root.title(currentTitle+"*")
	else:
		isFileSaved=False
		if (currentTitle[-1] == "*"):
			newTitle = currentTitle.replace("*", "")
			root.title(newTitle)

def newFile():
	global presentFilePath
	global isFileSaved
	if (isFileSaved != True):
		saveTheFile = tmsg.askyesno("Save the file.", "Do you want to save this file?")
		if (saveTheFile == True):
			saveFile()
			text.delete("1.0", END)
			isFileSaved = True
			presentFilePath = None
			root.title("AmanIDE - Untitled")
	else:
		text.delete("1.0", END)
		isFileSaved = True
		presentFilePath = None
		root.title("AmanIDE - Untitled")
			

def writeRecentFile(fileName):
	with open("/usr/bin/AmanIDE/bin/resentFile.aman", "w") as f:
		f.write(fileName)

def openRecentFile():
	global isFileSaved
	global presentFilePath
	with open("/usr/bin/AmanIDE/bin/resentFile.aman", "r") as r:
		presentFilePath = r.read()
		isFileSaved = True
		with open(presentFilePath, "r") as f:
			text.delete("1.0", END)
			text.insert("1.0", f.read())
			baseName = os.path.basename(presentFilePath)
			root.title(f"AmanIDE - {baseName}")

def openFile():
	global presentFilePath
	if (isFileSaved == False):
		if (presentFilePath != None):
			saveFile()
	fileName = tkfile.askopenfilename(filetypes=[("Python File", ".py"), ("All Files", "*.*")])
	if len(fileName)!=0:
		writeRecentFile(fileName)
		fileBaseName = os.path.basename(fileName)
		root.title(f"AmanIDE - {fileBaseName}")
		presentFilePath=fileName
		
		with open(presentFilePath) as f:
			openFileContent = f.read()
			text.delete("1.0", END)
			text.insert("1.0", openFileContent)
	else:
		tmsg.showerror("File Not Selected...", "Please select an file.")
		
	


def saveAsFile():
	global isFileSaved
	global presentFilePath
	saveFileName = tkfile.asksaveasfilename()
	if (len(saveFileName) != 0):
		writeRecentFile(saveFileName)
		codeForSave = text.get("1.0", END)
		with open(saveFileName, "w+") as f:
			f.write(codeForSave)
			presentFilePath = saveFileName
			isFileSaved = True
			fileBaseName = os.path.basename(presentFilePath)
		root.title(f"AmanIDE - {fileBaseName}")
		setTitle()
		tmsg.showinfo("Saved!", "File saved Successfully.")
	else:
		tmsg.showerror("File Not Saved!", "There are some issues for save the file.")
	
	
def saveFile():
	global presentFilePath
	global isFileSaved
	codeForSave = text.get("1.0", END)
	if (presentFilePath != None):
		isFileSaved = True
		with open(presentFilePath, "w") as f:
			f.write(codeForSave)
			isFileSaved = True
			setTitle()
	else:
		saveAsFile()
	
# Function for RUN the file
def runFile():
	if (presentFilePath != None):
		saveFile()
		command = f"python3 '{presentFilePath}'"
		#exc = os.getoutput(command)
		#tmsg.showerror("Python Output", exc)
		
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		output, err = process.communicate()
		OutPut.delete("1.0", END)
		OutPut.insert("1.0", output)
		OutPut.insert(END, err)
		
	else:
		tmsg.showerror("Running Error.", "Please Save the file before Run.")

#Function for exit the program
def exitProg():
	exitStatus = tmsg.askyesno("EXIT...", "Do you want to exit?")
	if (exitStatus == True):
		if (isFileSaved != True):
			save = tmsg.askyesno("Save the file...", "File is unsaved, Do you want to save the file?")
			if (save == True):
				saveFile()
		exit()
	else:
		pass
		
	



# Function for about
def about():
	tmsg.showinfo("About...", "This is an IDE made by\nAman Programmer.")
	
	
# Function for Contact
def Contact():
	tmsg.showinfo("Contact Us...", "Aman Programmer's personal email id\n ay12121230@gmail.com")

#Other Function
def writeFile(fileName, data):
	with open(fileName, "a") as f:
		f.write("\n\n"+data)

# SELECT ALL THE TEXT FROM CODE
def select_all():
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, "1.0")
    text.see(INSERT)
    return 'break'





def getAftPoint(val, act, aval):
	val = str(val)
	pd = "F"
	bp = ""
	ap = ""
	for i in val:
		if (i == "."):
			pd = "T"
			continue
		if (pd == "F"):
			bp += i
		else:
			ap += i
			
	if(act == "Sub"):
		ap = int(ap)-aval
	elif(act == "Add"):
		ap = int(ap)+aval
	final = f"{bp}.{ap}"
	
	return final



def duplicatAble(eve):
	curStr = text.index(INSERT)
	curFlt = float(curStr)
	char = eve.char
	keyName = eve.keysym
	if (char == "'"):
		text.insert(INSERT, "'")
		text.mark_set(INSERT, curStr)
	elif(char == '"'):
		text.insert(INSERT, '"')
		text.mark_set(INSERT, curStr)
	elif (char == "("):
		text.insert(INSERT, ')')
		text.mark_set(INSERT, curStr)
	elif (char == "["):
		text.insert(INSERT, ']')
		text.mark_set(INSERT, curStr)
	elif (char == "{"):
		text.insert(INSERT, '{\n\t\n}')
		text.mark_set(INSERT, float(curStr)+1.1)
		return "D"
	else:
		if(keyName == "BackSpace"):
			ind = float(text.index(INSERT))
			ad = getAftPoint(ind, "Sub", 1)
			g = text.get(ad, INSERT)
			if (g == "("):
				v = getAftPoint(ind, "Add", 1)
				h = text.get(INSERT, v)
				if (h == ")"):
					text.delete(ad, v)
					return "D"

			if (g == "'"):
				v = getAftPoint(ind, "Add", 1)
				h = text.get(INSERT, v)
				if (h == "'"):
					text.delete(ad, v)
					return "D"

			if (g == '"'):
				v = getAftPoint(ind, "Add", 1)
				h = text.get(INSERT, v)
				if (h == '"'):
					text.delete(ad, v)
					return "D"

			if (g == "["):
				v = getAftPoint(ind, "Add", 1)
				h = text.get(INSERT, v)
				if (h == "]"):
					text.delete(ad, v)
					return "D"

			if (g == "{"):
				v = getAftPoint(ind, "Add", 1)
				h = text.get(INSERT, v)
				if (h == "}"):
					text.delete(ad, v)
					return "D"
	


def inputing(eve):
	isFileSaved = False
	setTitle()
	if (duplicatAble(eve) == "D"):
		return "break"




root = Tk()
root.title("AmanIDE")
root.geometry("900x580")
#root.resizable(width=False, height=False)
#root.iconphoto(False, PhotoImage(file="/usr/bin/AmanIDE/icon.ico"))
#root.iconbitmap(r"icon.ico")


mainMenu = Menu(root, bg="white", font="bold 9")
filesMenu = Menu(mainMenu, bg="white", font="bold 9", tearoff=0)
filesMenu.add_command(label="New", command=newFile)
filesMenu.add_command(label="Open", command=openFile)
filesMenu.add_command(label="Save", command=saveFile)
filesMenu.add_command(label="Save As", command=saveAsFile)
filesMenu.add_separator()
filesMenu.add_command(label="Exit", command=lambda: exitProg())

mainMenu.add_cascade(label="Files", menu=filesMenu)


runMenu = Menu(mainMenu, bg="white", font="bold 9", tearoff=0)
runMenu.add_command(label="Run", command=runFile)

mainMenu.add_cascade(label="Run", menu=runMenu)


aboutMenu = Menu(mainMenu, bg="white", font="bold 9", tearoff=0)
aboutMenu.add_command(label="About", command=about)
aboutMenu.add_command(label="Contact Us", command=Contact)

mainMenu.add_cascade(label="About", menu=aboutMenu)




root.config(menu=mainMenu)


scrBar = Scrollbar(root)
scrBar.pack(side=RIGHT, fill=Y)

text = Text(root, bg=bgClr, fg="#FFFFFF", insertbackground="red")
text.pack(fill=BOTH, expand=YES)
text.config(yscrollcommand=scrBar.set)
scrBar.config(command=text.yview)
text.bind("<Key>", inputing)

cdg = ic.ColorDelegator()
cdg.prog = re.compile(fr'\b(?P<MYGROUP>{builtInPack})\b|' + ic.make_pat(), re.S)

cdg.idprog = re.compile(r'\s+(\w+)', re.S)

cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': bgClr}

# These five lines are optional. If omitted, default colours are used.
cdg.tagdefs['COMMENT'] = {'foreground': '#7F7F7F', 'background': bgClr}
cdg.tagdefs['KEYWORD'] = {'foreground': '#FF002D', 'background': bgClr}
cdg.tagdefs['BUILTIN'] = {'foreground': '#FF002D', 'background': bgClr}
cdg.tagdefs['STRING'] = {'foreground': '#00F2FF', 'background': bgClr}
cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': bgClr}

ip.Percolator(text).insertfilter(cdg)


OutPut = Text(root, bg="black", fg="#00F2FF", insertbackground="red", font=("ut Mono", 8))
OutPut.pack(fill=X)
OutPut.insert("1.0", "# Output will be show here...")


# Small Controll
root.bind("<Control-s>", lambda event: saveFile())
root.bind("<Control-o>", lambda event: openFile())
root.bind("<Control-r>", lambda event: runFile())
root.bind("<Control-a>", lambda event: select_all())
root.bind("<Control-q>", lambda event: cqExit())

#Caps Controll
root.bind("<Control-S>", lambda event: saveFile())
root.bind("<Control-O>", lambda event: openFile())
root.bind("<Control-R>", lambda event: runFile())
root.bind("<Control-A>", lambda event: select_all())
root.bind("<Alt-F4>", lambda event: exitProg())

font = tkFont.Font(font=text["font"])
tab_size = font.measure("    ")
text.config(tabs=tab_size)


# OPEN THE RECENT FILE
openRecentFile()
print("Running...")
root.mainloop()













