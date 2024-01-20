from wavelength import WAVELENGTHS
from pathlib import Path
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
import csv
import os
import sys
import pandas as pd
import pickle

indirName = "hyper_colonies"
colonies = os.listdir("./" + indirName)
varianceThreshold = 0.003

path = Path("dataset_raw.pkl")

if (path.is_file()):
	df = pd.read_pickle("dataset_raw.pkl")	
else:
	dataset = []
	removed = len(colonies)
	for colony in colonies:
		with open(indirName + "/" + colony, "r") as file:
			reader = csv.reader(file)
			data = [ [int(num) for num in row] for row in reader]
	
		## NORMALIZATION
		# with more uniform lighting this step is probably not needed. 
		
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
			if np.average(variance) < varianceThreshold:
				for pixel in data:
					dataset.append([colony] + pixel)
				removed -= 1
	print("Removed %d out of %d colonies due to outlier removal" % (removed, len(colonies)))
	df = pd.DataFrame(dataset, columns=["colonyID", "x", "y"] + WAVELENGTHS)
	df.to_pickle("dataset_raw.pkl")

## STANDARDIZATION
x = df.loc[:, WAVELENGTHS]
x = StandardScaler().fit_transform(x)

## DIMENSIONALITY REDUCTION
pca = PCA(n_components=9) #9 components looks to be good enough
principalComponents = pca.fit_transform(x)
df = df.loc[:, ["colonyID", "x", "y"]].join(pd.DataFrame(x, columns=WAVELENGTHS))
df.to_pickle("dataset.pkl")
