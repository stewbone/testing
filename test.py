import numpy as np
import matplotlib.pyplot as plt
import mnist

np.random.seed(10)
## load the dataset
data_train, label_train, data_test, data_test = mnist.load()

data = [i for i in range(10)]

class NN:
	def __init__(self, *args):
		self.n = 5 #number of nodes in hidden layer
		self.l = 10 #length of data vector
		self.f = 10 #length of output layer
		self.reps = 3 #number of repetitions of NN
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
	
	def forwardProp(self, data):
		history = []
		for i in range(len(self.weights)):
			data = list(map(self.act, self.weights[i] @ data + self.bias[i]))
			history.append(data)
		return history
	
	def printLayerSize(self):
		for layer in self.weights:
			print(layer.shape)
			
if __name__ == "__main__":
	data = [1 for i in range(10)]
	nn = NN()
#	print("Data: ")
#	print(data)
#	print("Weights of Input to Hidden Layer: ")
#	print(nn.weights[0])
#	print("Weights of Hidden to Output Layer: ")
#	print(nn.weights[1])
#	print("Hidden Layer: ")
#	hidden = nn.weights[0] @ data
#	print(hidden)
#	print("Output Layer: ")
#	output = nn.weights[1] @ hidden
#	print(output)
