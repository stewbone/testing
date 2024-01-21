from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from collections import Counter
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd

if __name__ == "__main__":
	df = pd.read_pickle("dataset.pkl")
	df = df.dropna() #missing values mean no label

	#remove data with only one colony (9 pixels)
	for otu in df.Otu.unique():
		if df[df['Otu'] == otu].shape[0] == 9:
			df = df.drop(df[df.Otu == otu].index)
	
#	for otu in df.Otu.unique():
#		print("%s %d" % (otu, df[df['Otu'] == otu].shape[0]))

	##	separate into data and label (otu) 
	val = df.values
	data,label = val[:, 5:] , val[:, 2]

	## split into training and testing datasets
	dataTrain, dataTest, labelTrain, labelTest = train_test_split(
		data, label, test_size=0.2, random_state=101)

	## use SMOTE to balance training set, NOT testing
	le = LabelEncoder()
	labelTrain = le.fit_transform(labelTrain)
	labelTest = le.transform(labelTest)
	smote = SMOTE()
	dataTrain, labelTrain = smote.fit_resample(dataTrain, labelTrain)

	## use model (Random Forest)
	rf = svm.SVC()
	rf.fit(dataTrain, labelTrain)
	predict = rf.predict(dataTest)
	accuracy = accuracy_score(labelTest, predict)
	print("Accuracy:", accuracy)
