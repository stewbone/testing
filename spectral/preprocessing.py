from wavelength import WAVELENGTHS
from pathlib import Path
import numpy as np
import csv
import os
import sys

outdirName = "hyper_colonies_Processed"
indirName = "hyper_colonies"
colonies = os.listdir("./" + indirName)
varianceThreshold = 0.003

Path(outdirName).mkdir(exist_ok=True)

for colony in colonies:
	with open(indirName + "/" + colony, "r") as file:
		reader = csv.reader(file)
		data = [ [int(num) for num in row] for row in reader]

	## NORMALIZATION
		for i in range(len(data)):
			tot = np.sum([float(num) for num in data[i][2:]])
			data[i] = [data[i][0], data[i][1]] + [(float(num) / tot) * 1000 for num in data[i][2:]] 
	
	## OUTLIER REMOVAL
		# average variance per wavelength
		variance = [None for _ in range(len(WAVELENGTHS))]
		rotateData = list(zip(*data))
		average = [np.average(wavelength) for wavelength in rotateData[2:]]
		for i in range(len(average)):
			variance[i] = np.average([pow(num - average[i], 2) for num in rotateData[i + 2]])
	
	##SAVE DATA
		if np.average(variance) > varianceThreshold:
			with open("%s/%s" % (outdirName, colony), "w") as file:
				writer = csv.writer(file)
				writer.writerows(data)
