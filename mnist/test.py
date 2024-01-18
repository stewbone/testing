import numpy as np
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import mnist


class NN:
	def __init__(self, *args):
		self.l = 784 #length of data vector
		self.n = 20 #number of nodes in hidden layer
		self.f = 10 #length of output layer
		self.hl = 3 #number of hidden layers	
		self.init_high = 0.5
		self.init_low = -0.5 #inital range of starting weights (look into changing)
		self.learn = 0.02 #learning rate
		
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
	
	def forwardProp(self, inp):
		activations = [np.array(inp)]
		zs = [[]]
		for i in range(len(self.weights)):
			z = self.weights[i] @ inp + self.bias[i] 
			zs.append(z)
			inp = np.array(list(map(self.act, z))) #input to next layer, or act(z)
			activations.append(inp)
		return activations, zs #returns list of activations

	def backwardProp(self, forward, label):
		lambdaWeights = []
		lambdaBias = []
		activations, zs = forward
		diff = activations[-1] - label #output - label

		dCdX = 2 * diff #derivative of cost function
		dXdZ = list(map(lambda n: n * (1 - n), activations[-1])) #derivative of activation function
		delta = np.array([dCdX[n] * dXdZ[n] for n in range(len(dCdX))]) #aka loss in the output layer

		##save the first set of changes (from right to left)
		delta.shape += (1,)
		activations[-2].shape += (1,)
		lambdaWeights = [delta @ np.transpose(activations[-2])] + lambdaWeights
		lambdaBias = [delta] + lambdaBias

		##we need to propogate this loss through the layers

		##start going backwards, so i starts at the second to last set of weights
		for i in range(2, len(self.weights) + 1): 

			##update delta
			dCdX = np.transpose(self.weights[-i + 1]) @ delta 
			dXdZ = list(map(lambda n: n * (1 - n), activations[-i])) #derivative of activation function
			delta = np.array([dCdX[n] * dXdZ[n] for n in range(len(dCdX))])

			activations[-i - 1].shape += (1,)
			lambdaWeights = [delta @ np.transpose(activations[-i - 1])] + lambdaWeights
			lambdaBias = [delta] + lambdaBias

		return lambdaWeights, lambdaBias

	def run_epoch(self, inp, label):
		lambdaWeights, lambdaBias = self.backwardProp(self.forwardProp(inp), label)
		self.weights = [np.add(self.weights[i], -self.learn * lambdaWeights[i]) for i in range(len(self.weights))]
		for bias in self.bias:
			bias.shape += (1,)
		self.bias = [np.add(self.bias[i], -self.learn * lambdaBias[i]) for i in range(len(self.bias))]

		for i in range(len(self.bias)):
			self.bias[i].shape = self.bias[i].shape[:-1]

	def run(self, data, labels):
		assert len(data) == len(labels)
		for i in range(len(data)):
			self.run_epoch(data[i], self.vectorizeLabel(labels[i]))
		for layer in self.weights:
			print(layer.shape)
	
	def test(self, data, labels):
		assert len(data) == len(labels)
		correct = 0
		for i in range(len(data)):
			activations, zs = self.forwardProp(data[i])
			if np.argmax(activations[-1]) == labels[i]:
				correct += 1
		return (correct / len(labels)) * 100
	
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
	data_train, label_train, data_test, label_test = mnist.load()
	data_train = [img / 255 for img in data_train]
	data_test = [img / 255 for img in data_test]

	nn = NN()
#	nn.forwardProp([0.1,0.5,1])	
#	nn.backwardProp(nn.forwardProp([num / 255 for num in data_train[0]]), nn.vectorizeLabel(label_train[0]))
#	nn.run([data_train[0]], [label_train[0]])
#	nn.run(data_train, label_train)

#	print("%f%%" % nn.test(data_test, label_test))

#	data = [[0.1,0.2,0.3,0.4,0.5]]
#	label = [[0,1]]	
#	nn.run(data, label)

#	clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(20,20,20), random_state=1)
#	clf.fit(data_train, label_train)
#	print(clf.score(data_test, label_test))
