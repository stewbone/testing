import struct
import sys
import numpy as np
import os
import time
import cv2
import imaging_picking_function as ipf
import time
import threading
import copy
import importlib
import math
import pickle

par = importlib.import_module("0_setParams")

MAX_SAMPLES = 1600
MAX_LINES = 1700
MAX_BANDS = 462

GREEN_BAND = 121
RED_BAND = 189
BLUE_BAND = 53

#convert hyperspectral units into RGB friendly units (8190 is unit max)
def RGB(value):
	return (int) ((value * 255) / 8190)

#rotate a point p around a point o by an angle of a degrees
def rotate_point(o, p, a):
	ox, oy = o
	px, py = p

	sin = math.sin(math.radians(a))
	cos = math.cos(math.radians(a))

	return [int(ox + cos * (px - ox) - sin * (py - oy)), int(oy + sin * (px - ox) + cos * (py - oy))]

#apple rotation to every point in contours list around an origin determined by line/sample multipliers
def rotate_contours(contours, params):
	o = [int(800 * params.LINE_MULT), int(500 * params.SAMPLE_MULT)]
	return [ np.array([ [ rotate_point(o,*point,float(params.ROT_ANGLE)) ] for point in contour ]).astype(np.int32) for contour in contours ]

#convert .bil file to a numpy array with shape (samples, lines, bands)
def step1_convert():
	return np.transpose(np.fromfile(DATA_CUBE_NAME + "/" + DATA_CUBE_NAME + ".bil", dtype=np.ushort).reshape((MAX_LINES, MAX_BANDS, MAX_SAMPLES)), (2, 0, 1))

#apply parameters to cube, flipping if necessary, then cropping by corners
def step2_apply(cube, params):
	if params.VERT_FLIP_FLAG:
		cube = np.flip(cube, 0)
	if params.HORI_FLIP_FLAG:
		cube = np.flip(cube, 1) 
	
	corners = [None for _ in range(4)]
	corners[0] = int(params.LINE_START) + int(150 * params.LINE_MULT)
	corners[1] = int(params.SAMPLE_START) + int(150 * params.SAMPLE_MULT)
	corners[2] = int(1600 * float(params.LINE_MULT)) + corners[0]
	corners[3] = int(1000 * float(params.SAMPLE_MULT)) + corners[1]
	return cube[corners[1]:corners[3], corners[0]:corners[2]]	

#build the final directory, with .npy files of cropped cube, updated contours file, and images for manual checking
def step3_build(cube, params):
	contours_normal = np.load(DATA_CUBE_NAME + "/out/" + DATA_CUBE_NAME + "_Contours_all.npy", allow_pickle=True)
	image = cv2.imread(DATA_CUBE_NAME + "/out/" + DATA_CUBE_NAME + "_Image_colony_trans.jpg", cv2.IMREAD_GRAYSCALE) #x is samples, y is lines
	contours_hyper = copy.deepcopy(contours_normal)
	MAX_SAMPLES, MAX_LINES, MAX_BANDS = np.shape(cube)
	drawn_HSimage = np.zeros((MAX_SAMPLES, MAX_LINES, 3))

	#convert the normal contours to hyperspectral scale, then rotate them by parameter 	
	for i in range(len(contours_normal)):
		for j in range(len(contours_normal[i])):
			contours_hyper[i][j][0][0] = int(contours_normal[i][j][0][0] * params.LINE_MULT)
			contours_hyper[i][j][0][1] = int(contours_normal[i][j][0][1] * params.SAMPLE_MULT)
	contours_hyper = rotate_contours(contours_hyper, params)

	#build image file 
	for i in range(len(cube)):
		for j in range(len(cube[i])):
			drawn_HSimage[i][j] = (RGB(cube[i][j][BLUE_BAND]), RGB(cube[i][j][GREEN_BAND]), RGB(cube[i][j][RED_BAND]))

	HSimage = copy.deepcopy(drawn_HSimage)
	drawn_HSimage = cv2.drawContours(drawn_HSimage, contours_hyper, -1, (0,0,255))
	drawn_Nimage = cv2.drawContours(image, contours_normal, -1, (0,0,255))

	return (contours_hyper, drawn_HSimage, drawn_Nimage, HSimage)

def main():
	params = par.Params(DATA_CUBE_NAME)
	full_cube = step1_convert()
	cropped_cube = step2_apply(full_cube, params)	

	with open(DATA_CUBE_NAME + "/" + DATA_CUBE_NAME + "_cropped.pkl", "wb") as f:
		pickle.dump(cropped_cube, f)

	contours_hyper, drawn_HSimage, drawn_Nimage, HSimage = step3_build(cropped_cube, params)
	with open(DATA_CUBE_NAME + "/hyper_contours.pkl", "wb") as f:
		pickle.dump(contours_hyper, f)

	cv2.imwrite(DATA_CUBE_NAME + "/drawn_HSimage.jpg", drawn_HSimage)
	cv2.imwrite(DATA_CUBE_NAME + "/HSimage.jpg", HSimage)
	cv2.imwrite(DATA_CUBE_NAME + "/drawn_Nimage.jpg", drawn_Nimage)

if __name__ == "__main__":
	DATA_CUBE_NAME = sys.argv[1]
	main()
