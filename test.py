import numpy as np
import matplotlib.pyplot as plt
import mnist


class NN:
	def __init__(self, *args):
		self.n = 16 #number of nodes in hidden layer
		self.l = 784 #length of data vector
		self.f = 10 #length of output layer
		self.init_high = 0.5
		self.init_low = -0.5 #inital range of starting weights (look into changing)
		self.hl = 1 #number of hidden layers	
		
		if len(args) > 0:
			self.hl = args[0]

		## initialize for just one hidden layer
		self.weights = []
		self.bias = []
		self.weights.append(np.random.uniform(self.init_low, self.init_high, (self.n, self.l))) #weights for input to first hidden layer
		self.weights.append(np.random.uniform(self.init_low, self.init_high, (self.f, self.n))) #weights for first hidden layer to output layer

		## additional hidden layers
		for i in range(self.hl - 1):	
			self.weights.insert(1, np.random.uniform(self.init_low, self.init_high, (self.n, self.n)))

		## initialize bias
		self.bias = [np.zeros(layer.shape[0]) for layer in self.weights]
	
	def act(self, z): #activation function
		return 1/(1 + np.exp(-z)) #sigmoid
	
	def cost(self, data, label): #cost function sum of square differences
		return sum([pow(data[i], 2) for i in range(len(data))]) - 2*data[label] + 1
	
	def forwardProp(self, data):
		activations = [data]
		for i in range(len(self.weights)):
			data = list(map(self.act, self.weights[i] @ data + self.bias[i]))
			activations.append(data)
		return activations #returns list of activations

	def backwardProp(self, activations, label):
		diff = activations[-1] - label	
		return diff
	
	def vectorizeLabel(self, label):
		n = np.zeros(self.f)
		n[label] = 1.0
		return n
	
	def printLayerSize(self):
		for layer in self.weights:
			print(layer.shape)
			
if __name__ == "__main__":
	np.random.seed(10)

	## load the dataset
	data_train, label_train, data_test, data_test = mnist.load()

	nn = NN()
	print(nn.backwardProp(nn.forwardProp([num / 255 for num in data_train[0]]), nn.vectorizeLabel(label_train[0])))
