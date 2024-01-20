from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from wavelength import WAVELENGTHS
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler
from PIL import Image,ImageTk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import tkinter
import sys
import os
import csv
import cv2

class GUI(Canvas):
	def __init__(self, master):
		self.master = master
		self.master.bind('<Destroy>', lambda e: self.master.quit())
		self.master.columnconfigure(0, weight=1)
		self.master.columnconfigure(1, weight=1)
		self.master.columnconfigure(2, weight=1)
		self.master.columnconfigure(3, weight=8)
		self.master.columnconfigure(4, weight=2)
		for i in range(4,9):
			self.master.rowconfigure(i, weight=1)
#		self.master.rowconfigure(0, weight=1)	
#		self.master.rowconfigure(1, weight=1)
#		self.master.rowconfigure(2, weight=100)
		
		with open("completeCollated.csv") as file:
			reader = csv.reader(file)
			self.header = next(reader)
			self.metaData = [row for row in reader]
		self.colonies = {}
		for column in self.header:
			self.colonies[column] = {"All" : []}
		for row in self.metaData:
			for i in range(len(row)):
				if row[i] in self.colonies[self.header[i]].keys():
					self.colonies[self.header[i]][row[i]].append("%s_%s.csv" % (row[3], row[4]))
				else:
					self.colonies[self.header[i]][row[i]] = ["%s_%s.csv" % (row[3], row[4])]
		self.comboVar = [ StringVar() for _ in range(len(self.header)) ]
		self.pathDir = "./hyper_colonies_process"

		self.listBox = Listbox(self.master, exportselection=False)
		self.listBox.bind('<<ListboxSelect>>', self.individual)
		self.browseButton = Button(self.master, text="select folder", command=self.browseDir)
		self.filterButton = Button(self.master, text="filter", command=self.filter)
		self.compareButton = Button(self.master, text="compare", command= lambda: self.compare())
		self.clearButton = Button(self.master, text="clear", command= lambda: self.clearPlot())

		self.boxList = []
		self.plotDict = {}
		self.checkVar = IntVar(value=0)
		self.checkButton = ttk.Checkbutton(self.master, text="Retain Mode", variable=self.checkVar)
		self.infoText = StringVar()
		self.infoLabel = Label(self.master, textvariable=self.infoText)

		self.figure = Figure()
		self.ax = self.figure.add_subplot()
		self.title = ""
		self.plot()
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=False)
		self.toolbar.update()
	
		self.imageCanvas = Canvas(self.master)
		self.image_container = self.imageCanvas.create_image(0,0,anchor=NW)
		self.preImage = Image.fromarray(np.zeros((20,20)))
		self.imageCanvas.bind('<Configure>', self.resizeImage)
	
		self.browseButton.grid(row=0, column=0, padx=5, pady=5, sticky="s")
		self.filterButton.grid(row=0, column=1, padx=5, pady=5, sticky="s")	
		self.clearButton.grid(row=0, column=2, padx=5, pady=5, sticky="s")
		self.imageCanvas.grid(row=0, column=4, rowspan=5, padx=5, pady=5, sticky="nsew")
		self.infoLabel.grid(row=5, column=4, rowspan=5, sticky="nsew")
		self.compareButton.grid(row=1, column=0, sticky="s")
		self.checkButton.grid(row=1, column=1, sticky = "s")	
		self.listBox.grid(row=2, column=0, columnspan=3, rowspan=8, sticky="ns", padx=5, pady=5)
		self.canvas.get_tk_widget().grid(row=0, column=3, rowspan=9, sticky="nsew")
		self.toolbar.grid(column=0, row=9, columnspan=5, sticky="nsew")
	
	def grid_canvas(self):
		self.canvas.get_tk_widget().grid(row=0, column=3, rowspan=9, sticky="nsew")
		
	def sortBox(self):
		self.boxList.sort(key = lambda x : (x.split("_")[0], int(x.split("_")[1].split(".")[0])))
		
	def filter(self):	
		def updateListBox():
			vals = [item.get() for item in self.comboVar]
			lists = []
			for i in range(len(vals)):
				if vals[i] != "" and vals[i] != "All":
					lists.append(self.colonies[self.header[i]][vals[i]])	
			self.boxList = list(set.intersection(*map(set, lists)))
			self.boxList = [item for item in self.boxList if item in self.dirList]	
			self.sortBox()
			self.fileDir = StringVar(value=self.boxList)
			self.listBox.configure(listvariable=self.fileDir)
			for i in range(0, self.listBox.size(), 2):
				self.listBox.itemconfigure(i, background='#f0f0ff')	
			self.top.destroy()
				
		self.top = Toplevel(self.master)
		self.top.wait_visibility()
		self.top.grab_set()
		self.top.geometry('250x150')
	
		genusCombo = ttk.Combobox(self.top, textvariable=self.comboVar[9], state="readonly")
		genusCombo['values'] = list(self.colonies[self.header[9]].keys())
		genusCombo.current(genusCombo['values'].index(self.comboVar[9].get()) if self.comboVar[9].get() != "" else 0)
		genusCombo.grid(row=0, column=1, padx=5, pady=10)

		otuCombo = ttk.Combobox(self.top, textvariable=self.comboVar[10], state="readonly")
		otuCombo['values'] = sorted(list(self.colonies[self.header[10]].keys()), key = lambda x: int(x[3:]) if len(x) > 3 else 0)
		otuCombo.current(otuCombo['values'].index(self.comboVar[10].get()) if self.comboVar[10].get() != "" else 0)
		otuCombo.grid(row=1, column=1, padx=5, pady=10)

		plateCombo = ttk.Combobox(self.top, textvariable=self.comboVar[3], state="readonly")
		plateCombo['values'] = list(self.colonies[self.header[3]].keys())
		plateCombo.current(plateCombo['values'].index(self.comboVar[3].get()) if self.comboVar[3].get() != "" else 0)
		plateCombo.grid(row=2, column=1, padx=5, pady=10)

		genusLabel = Label(self.top, text="Genus: ")
		genusLabel.grid(row=0, column=0, padx=5, pady=10)
		
		otuLabel = Label(self.top, text="Otu: ")
		otuLabel.grid(row=1, column=0, padx=5, pady=10)

		plateLabel = Label(self.top, text="Plate: ")
		plateLabel.grid(row=2, column=0, padx=5, pady=10)

		filterButton = Button(self.top, text="Filter", command= lambda : updateListBox())
		filterButton.grid(row=3, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
	
	def setLabel(self, event):
		idx = self.listBox.curselection()
		name = self.listDir[idx[0]][:-4]

	def browseDir(self):
		self.pathDir = filedialog.askdirectory(initialdir=self.pathDir)
		self.dirList = os.listdir(self.pathDir)
		self.boxList = self.dirList
		self.sortBox()
		self.fileDir = StringVar(value=self.boxList)
		self.listBox.configure(listvariable=self.fileDir)
		for i in range(0, self.listBox.size(), 2):
			self.listBox.itemconfigure(i, background='#f0f0ff')	
	
	def plot(self):
		if len(self.plotDict.keys()) == 1:
			key = list(self.plotDict.keys())[0]
			self.ax.clear()
			self.ax.set_title(key)
		
			lines = self.plotDict[key][0]
			labels = self.plotDict[key][1]
			for i in range(len(lines)):	
				if len(labels) > 0:
					self.ax.plot(WAVELENGTHS, lines[i], label=labels[i])
				else:
					self.ax.plot(WAVELENGTHS, lines[i])
			if len(labels) > 0:
				self.ax.legend()
		elif len(self.plotDict.keys()) != 0:
			self.infoText.set("")
			self.ax.clear()
			titles = list(self.plotDict.keys())
			color = [None for i in range(len(titles))]
			for i in range(len(titles)):
				lines = self.plotDict[titles[i]][0]
				for line in lines:
					if color[i] == None:
						artist = self.ax.plot(WAVELENGTHS, line, label=titles[i])	
						color[i] = artist[0].get_c()	
					else:
						self.ax.plot(WAVELENGTHS, line, color=color[i])
			self.ax.legend()
		self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)	
		self.canvas.draw()
		self.toolbar = NavigationToolbar2Tk(self.canvas, self.master, pack_toolbar=False)
		self.canvas.get_tk_widget().grid(row=0, column=3, rowspan=9, sticky="nsew")
		self.toolbar.grid(column=0, row=9, columnspan=5, sticky="nsew")

	def resizeImage(self, event):
		newPreImage = self.preImage.resize((event.width, event.height), Image.Resampling.BOX)
		self.newImage = ImageTk.PhotoImage(newPreImage)	
		self.imageCanvas.itemconfigure(self.image_container, image=self.newImage)
		self.imageCanvas.grid(row=0, column=4, rowspan=5, padx=5, pady=5, sticky="nsew")
	
	def individual(self, event):
		idx = self.listBox.curselection()
		name = self.boxList[idx[0]]
		lines = []
		if os.path.isfile(self.pathDir + "/" + name):
			with open(self.pathDir + "/" + name) as file:
				self.ax.clear()
				reader = csv.reader(file)
				dataFull = [row for row in reader]
				data = [row[2:] for row in dataFull]
				for row in data:
					lines.append([float(num) for num in row])
				variance = [None for _ in range(len(WAVELENGTHS))]
				rotateData = list(zip(*data))
				average = [np.average([float(num) for num in wavelength]) for wavelength in rotateData]
				for i in range(len(average)):
					variance[i] = np.average([pow(float(num) - average[i], 2) for num in rotateData[i]])
		self.infoText.set("")
		for row in self.metaData:	
			if "%s_%s" % (row[3], row[4]) == name[:-4]:
				for i in range(len(self.header)):
					self.infoText.set(self.infoText.get() + "%s: %s\n" % (self.header[i], row[i]))
				self.infoText.set(self.infoText.get() + "Average Variance: %0.10f" % np.average(variance))
				break
		if self.checkVar.get() == 0:
			self.plotDict = {}
		self.plotDict[name] = [lines,[]]
		self.plot()

		plateName = name[:8]
		colonyNum = int(name[9:-4]) - 1

		plate = cv2.imread("ax/plates/" + plateName + ".jpg")
		plate = np.flip(plate, 2)
		for row in dataFull:
			plate[int(row[0]), int(row[1])] = [0, 255, 0]
		subPlate = plate[int(dataFull[0][0]) - 10 : int(dataFull[0][0]) + 10, int(dataFull[0][1]) - 10 : int(dataFull[0][1]) + 10]
		self.preImage = Image.fromarray(subPlate.astype(np.uint8))
		newPreImage = self.preImage.resize((self.imageCanvas.winfo_reqheight(), self.imageCanvas.winfo_reqwidth()), Image.Resampling.BOX)
		self.newImage = ImageTk.PhotoImage(image=newPreImage)
		self.imageCanvas.itemconfig(self.image_container, image = self.newImage)
		self.imageCanvas.grid(row=0, column=4, rowspan=5, padx=5, pady=5, sticky="nsew")
		cv2.imwrite("test.jpg", subPlate)

	def compare(self):
		lines = []
		labels = []
		title = "Genus= %s, Otu= %s, Plate= %s" % (self.comboVar[9].get(), self.comboVar[10].get(), self.comboVar[3].get())
		for colony in self.boxList:
			with open(self.pathDir + "/" + colony) as file:
				reader = csv.reader(file)
				data = [row[2:] for row in reader]
			lines.append([np.average([float(num) for num in wavelength]) for wavelength in zip(*data)])
			labels.append(colony[:-4])
		if self.checkVar.get() == 0:
			self.plotDict = {}
		self.plotDict[title] = [lines, labels]
		self.plot()
		
	def clearPlot(self):
		self.ax.clear()
		self.infoText.set("")
		self.plotDict = {}
		self.plot()

if __name__ == "__main__":
	root = Tk()
	app = GUI(root)
	root.mainloop()
