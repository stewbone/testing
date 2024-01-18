from tkinter import * 
from PIL import Image,ImageTk
import cv2
import numpy as np
import os
import sys
import importlib
import copy 
import math
import time
import threading
import imaging_picking_function as ipf

MAX_SAMPLES = 1600
MAX_LINES = 1700
MAX_BANDS = 462

RED_BAND = 189
GREEN_BAND = 121
BLUE_BAND = 53

class GUI(Canvas):
	def __init__(self, master, *args, **kwargs):
		Canvas.__init__(self, master, *args, **kwargs)

		self.master = master
		self.my_canvas = Canvas(self.master)

		self.cube = reduced_cube
		self.params = Params(DATA_CUBE_NAME)

		##initialize and make original image
		self.set_contours()
		if not os.path.isfile(DATA_CUBE_NAME + "/parameters.txt"):
			self.corners = find_edge(self.params) #TOP_LEFT_LINE, TOP_LEFT_SAMPLE, BOTTOM_RIGHT_LINE, BOTTOM_RIGHT_SAMPLE
		else:
			self.corners = [ None for i in range(4) ]
			self.corners[0] = int(self.params.LINE_START) + int(150 * self.params.LINE_MULT)
			self.corners[1] = int(self.params.SAMPLE_START) + int(150 * self.params.SAMPLE_MULT)
			self.corners[2] = int(1600 * float(self.params.LINE_MULT)) + self.corners[0]
			self.corners[3] = int(1000 * float(self.params.SAMPLE_MULT)) + self.corners[1]

		if self.params.VERT_FLIP_FLAG:
			self.cube = np.flip(self.cube, 0)
		if self.params.HORI_FLIP_FLAG:
			self.cube = np.flip(self.cube, 1) 

		imag = Image.fromarray(cv2.drawContours(np.copy(self.cube[self.corners[1]:self.corners[3], self.corners[0]:self.corners[2]]), self.contours, -1, (255,0,0), 1))
		self.my_canvas.configure(height=self.corners[3]-self.corners[1], width=self.corners[2]-self.corners[0])
		self.img = ImageTk.PhotoImage(image=imag) 
		self.image_container = self.my_canvas.create_image(0,0,anchor=NW,image=self.img)	
		self.my_canvas.grid(row=0, column=0, rowspan=6)

		self.l1 = Label(self.master, text="Line Multiplier = ")
		self.l2 = Label(self.master, text="Sample Multiplier = ")
		self.l3 = Label(self.master, text="Line Offset = ")
		self.l4 = Label(self.master, text="Sample Offset = ")
		self.l5 = Label(self.master, text="Rotation Angle (degrees) = ")

		self.l1.grid(row=0,column=1)	
		self.l2.grid(row=1,column=1)	
		self.l3.grid(row=2,column=1)	
		self.l4.grid(row=3,column=1)	
		self.l5.grid(row=4,column=1)

		self.t1 = StringVar()
		self.t2 = StringVar()
		self.t3 = StringVar()
		self.t4 = StringVar()
		self.i1 = Entry(self.master, textvariable = self.t1)
		self.i2 = Entry(self.master, textvariable = self.t2)
		self.i3 = Entry(self.master, textvariable = self.t3)
		self.i4 = Entry(self.master, textvariable = self.t4)

		self.i1.grid(row=0,column=2)
		self.i2.grid(row=1,column=2)
		self.i3.grid(row=2,column=2)
		self.i4.grid(row=3,column=2)

		self.convert_button = Button(self.master, text="Convert", command=self.convert)

		self.convert_button.grid(row=5, column=1)

		self.restore_button = Button(self.master, text="Reset to Stored Value", command=lambda: self.reset())
		self.restore_button.grid(row=5, column=2)

		self.c1 = IntVar()	
		self.check_vert_flip = Checkbutton(self.master, text = "Vertical Flip?", variable=self.c1, onvalue=1, offvalue=0)
		self.check_vert_flip.grid(row=2, column=3)

		self.c2 = IntVar()	
		self.check_hori_flip = Checkbutton(self.master, text = "Horizontal Flip?", variable=self.c2, onvalue=1, offvalue=0)
		self.check_hori_flip.grid(row=3, column=3)

		self.angle_scale = Scale(self.master, orient=HORIZONTAL, length=200, from_=-3.0, to=3, resolution=0.01, command=self.rotate_contours)
		self.angle_scale.grid(row=4, column=2, columnspan=2)

		self.save_button = Button(self.master, text="Save Values?", command=lambda: self.save_data())
		self.save_button.grid(row=5, column=3)

		self.restore()

	#update parameters class to user input
	def update_params(self):
		self.params.set(float(self.t1.get()), float(self.t2.get()), int(self.t3.get()), int(self.t4.get()), float(self.angle_scale.get()), self.c1.get(), self.c2.get())

	#save the data and print it to console
	def save_data(self):
		self.update_params()
		self.params.write()

	#build new image from updated parameters
	def new_image(self, cont):
		imag = Image.fromarray(cv2.drawContours(np.copy(self.cube[self.corners[1]:self.corners[3], self.corners[0]:self.corners[2]]), cont, -1, (255,0,0), 1))
		self.my_canvas.configure(height=self.corners[3]-self.corners[1], width=self.corners[2]-self.corners[0])
		self.img = ImageTk.PhotoImage(image=imag) 
		self.image_container = self.my_canvas.create_image(0,0,anchor=NW,image=self.img)	

	#update contours to new line/sample multipliers
	def set_contours(self):
		self.contours = [np.array(contour * [self.params.LINE_MULT, self.params.SAMPLE_MULT]).astype(np.int32) for contour in contours]
	
	#restore input boxes to values saved in parameters class
	def restore(self):
		self.i1.delete(0, END)
		self.i2.delete(0, END)
		self.i3.delete(0, END)
		self.i4.delete(0, END)

		self.i1.insert(END, self.params.LINE_MULT)
		self.i2.insert(END, self.params.SAMPLE_MULT)
		self.i3.insert(END, self.params.LINE_START)
		self.i4.insert(END, self.params.SAMPLE_START)
		
		self.angle_scale.set(self.params.ROT_ANGLE)

		if self.params.VERT_FLIP_FLAG:
			self.check_vert_flip.select()
		else:
			self.check_vert_flip.deselect()

		if self.params.HORI_FLIP_FLAG:
			self.check_hori_flip.select()
		else:
			self.check_hori_flip.deselect()

	#restore input boxes to values saved in parameters.txt
	def reset(self):
		self.params = Params(DATA_CUBE_NAME)
		self.restore()

	#rotate a point p around o by a degrees
	def rotate_point(self, o, p, a):
		ox, oy = o
		px, py = p

		sin = math.sin(math.radians(a))
		cos = math.cos(math.radians(a))

		return [int(ox + cos * (px - ox) - sin * (py - oy)), int(oy + sin * (px - ox) + cos * (py - oy))]

	#apply rotation to every point in contours list, using origin defined by line/sample multipliers
	def rotate_contours(self, val):
		o = [int(800 * self.params.LINE_MULT), int(500 * self.params.SAMPLE_MULT)]
		new_contours = [ np.array([ [ self.rotate_point(o,*point,float(val)) ] for point in contour ]).astype(np.int32) for contour in self.contours ]
		self.new_image(new_contours)

	#main conversion function, update parameters class and generate new image  
	def convert(self):
		if self.c1.get() != self.params.VERT_FLIP_FLAG:
			self.cube = np.flip(self.cube, 0)
		if self.c2.get() != self.params.HORI_FLIP_FLAG:
			self.cube = np.flip(self.cube, 1) 

		self.update_params()
		self.params.print()
   
		#update contours
		self.set_contours()
		
		self.angle_scale.set(0.0) #reset the angles scale for simplicity
		self.params.ROT_ANGLE = 0.0
		
		#update corners with newly inputted values
		self.corners[0] = int(self.params.LINE_START) + int(150 * self.params.LINE_MULT)
		self.corners[1] = int(self.params.SAMPLE_START) + int(150 * self.params.SAMPLE_MULT)
		self.corners[2] = int(1600 * float(self.params.LINE_MULT)) + self.corners[0]
		self.corners[3] = int(1000 * float(self.params.SAMPLE_MULT)) + self.corners[1]

		self.new_image(self.contours)

#run this fxn once per plate to estimate edge of plate, and set initial line/sample start parameters
def find_edge(params):
	MAX_SAMPLES, MAX_LINES, MAX_BANDS = np.shape(reduced_cube)
	TOP_LEFT_SAMPLE, TOP_LEFT_LINE, BOTTOM_RIGHT_SAMPLE, BOTTOM_RIGHT_LINE = np.zeros(4)
	BOTTOM_RIGHT_SAMPLE = MAX_SAMPLES - 1

	## thresholding to find the edge of the plate (might break if background of plate is changed)
	TOP_LEFT_LINE = 0
	MID_SAMPLE = int(MAX_SAMPLES / 2)
	MID_LINE = int(MAX_LINES / 2)
	while(reduced_cube[MID_SAMPLE][TOP_LEFT_LINE][0] > 31):
		TOP_LEFT_LINE = TOP_LEFT_LINE + 10
	  
	TOP_LEFT_SAMPLE = 0
	while(reduced_cube[TOP_LEFT_SAMPLE][MID_LINE][0] > 31):
		TOP_LEFT_SAMPLE = TOP_LEFT_SAMPLE + 10

	params.LINE_START = TOP_LEFT_LINE 
	params.SAMPLE_START = TOP_LEFT_SAMPLE
	TOP_LEFT_LINE = TOP_LEFT_LINE + int(150 * params.LINE_MULT) #where 150 is the CAMII crop length in both the x and y direction
	TOP_LEFT_SAMPLE = TOP_LEFT_SAMPLE + int(150 * params.SAMPLE_MULT)
	BOTTOM_RIGHT_LINE = int(1600 * params.LINE_MULT) + TOP_LEFT_LINE #1600x1000 is the resolution of CAMII image
	BOTTOM_RIGHT_SAMPLE = int(1000 * params.SAMPLE_MULT) + TOP_LEFT_SAMPLE

	return [TOP_LEFT_LINE, TOP_LEFT_SAMPLE, BOTTOM_RIGHT_LINE, BOTTOM_RIGHT_SAMPLE]

#also only run once to get initial contours
def CAMII_contour(configure_path, input_dir, output_dir):
	configure_pool = ipf.readConfigureFile(configure_path)
	ipf.modifyOSconfigure(configure_pool)
	total_image, image_label_list, image_trans_list, image_epi_list = ipf.readFileList(input_dir)

	globalOutput = ipf.globalOutputObject(total_image)
	threadPool_fun0 = []
	for i in range(total_image):
		tmpThread = threading.Thread(target = ipf.multi_fun0_detectColonySingleImage, args = (image_trans_list[i], image_epi_list[i], image_label_list[i], configure_pool, globalOutput, i))
		threadPool_fun0.append(tmpThread)
	for i in range(total_image):
		threadPool_fun0[i].start()
	for i in range(total_image):
		threadPool_fun0[i].join()

	for i in range(total_image):
		globalOutput.plateQC_flag[i] = True
		
	f = open(input_dir + "/image_processed.txt", "a")
	for e in image_label_list:
		f.writelines([e + os.linesep])
	f.close()

	ipf.modifyOutputObject_colonyDetection(globalOutput, total_image, configure_pool)

	if not os.path.isdir(output_dir):
		os.system("mkdir -p " + output_dir)

	ipf.saveOutputs_colonyDetection(globalOutput, total_image, configure_pool, output_dir)

def convert():
	return np.transpose(np.fromfile(DATA_CUBE_NAME + "/" + DATA_CUBE_NAME + ".bil", dtype=np.ushort).reshape((MAX_LINES, MAX_BANDS, MAX_SAMPLES)), (2, 0, 1))

def RGB(value):
	return (int) ((value * 255) / 8190)

#parameters class to keep parameters together and easy printing capability
class Params():
	def __init__(self, DATA_CUBE_NAME):
		self.DATA_CUBE_NAME = DATA_CUBE_NAME
		if os.path.isfile(DATA_CUBE_NAME + "/parameters.txt"):
			with open(DATA_CUBE_NAME + "/parameters.txt") as file:
				values = file.read()
				values = values.split(" ")
				self.set(float(values[0]), float(values[1]), int(values[2]), int(values[3]), float(values[4]), int(values[5]), int(values[6]))
		else:
			with open(DATA_CUBE_NAME + "/parameters.txt", "w") as file:
				file.write("%0.3f %0.3f %d %d %0.2f %d %d" % (0.731, 0.744, 255, 135, 0.0, 0, 0)) #empirically defined default values
				self.set(0.731, 0.744, 255, 135, 0.0, 0, 0)
	def set(self, *args): ##assume the all relevant variables are passsed
		self.LINE_MULT = args[0]
		self.SAMPLE_MULT = args[1]
		self.LINE_START = args[2]
		self.SAMPLE_START = args[3]
		self.ROT_ANGLE = args[4]
		self.VERT_FLIP_FLAG = args[5]
		self.HORI_FLIP_FLAG = args[6]
	def write(self):
		with open(self.DATA_CUBE_NAME + "/parameters.txt", "w") as file:
			file.write("%0.3f %0.3f %d %d %0.2f %d %d" % (self.LINE_MULT, self.SAMPLE_MULT, self.LINE_START, self.SAMPLE_START, self.ROT_ANGLE, self.VERT_FLIP_FLAG, self.HORI_FLIP_FLAG))
	def print(self):
		print("LINE_MULT: %0.3f" % self.LINE_MULT)
		print("SAMPLE_MULT: %0.3f" % self.SAMPLE_MULT)
		print("LINE_START: %d" % self.LINE_START)
		print("SAMPLE_START: %d" % self.SAMPLE_START)
		print("ROT_ANGLE: %0.2f" % self.ROT_ANGLE)
		print("VERT_FLIP_FLAG: %d" % self.VERT_FLIP_FLAG)
		print("HORI_FLIP_FLAG: %d" % self.HORI_FLIP_FLAG)
	
if __name__ == "__main__":
	DATA_CUBE_NAME = sys.argv[1]
	CAMII_contour("configure", DATA_CUBE_NAME + "/in", DATA_CUBE_NAME + "/out")
	contours = np.load("%s/out/%s_Contours_all.npy" % (DATA_CUBE_NAME, DATA_CUBE_NAME), allow_pickle=True)
	root = Tk()

	reduced_cube = convert()[:,:,(RED_BAND, GREEN_BAND, BLUE_BAND)]
	reduced_cube = np.array([[[RGB(val) for val in bands] for bands in row] for row in reduced_cube]).astype(np.uint8)
#	reduced_cube = np.load("reduced_cube.npy")
	app = GUI(root)	
	root.mainloop()
