from collections import OrderedDict
import numpy as np
import nltk
from nltk.corpus import stopwords as sw
import math

def tokenize(inputstr, onlyalpha = True, stopwords = False, stemmer = True):
	inputstr = inputstr.lower()
	tokens = nltk.word_tokenize(inputstr)

	if(onlyalpha):
		tokens = [i for i in tokens if i.isalpha()]

	if(not stopwords):
		stpwrds = set(sw.words('english'))
		tokens = [i for i in tokens if i not in stpwrds]

	if(stemmer):
		stmr = nltk.stem.porter.PorterStemmer()
		tokens = [stmr.stem(i) for i in tokens]

	return tokens

def cosine_similarity(A, B):
	multi = (A.dot(B))
	x = math.sqrt(A.dot(A))
	y = math.sqrt(B.dot(B))
	result = multi / (x * y)
	return result

class Vocabulary:
	def __init__(self):
		self.vector = OrderedDict()
		self.entry = []

	def add(self, token):
		if token not in self.vector and not token.isspace() and token != '':
			self.vector[token] = len(self.vector)
			self.entry.append(token)

	def addall(self, tokens):
		for token in tokens:
			self.add(token)

	def has(self, token):
		return token in self.vector

	def index(self, token):
		return self.vector[token]

	def size(self):
		return len(self.vector)

	# get ith word in the vector
	def at(self, i):
		return self.entry[i]

	# word2vec = str -> numpy.array
	# get one-hot encoded vector of a word
	def word2vec(self, word):
		v = [0 for i in range(self.size())]
		if word in self.vector:
			v[self.index(word)] = 1
		else:
			raise ValueError("Word \'" + word + "\' Not Found")
		return np.array(v)

	# doc2vec = list -> numpy.array
	# get word count vector of the given tokens
	def doc2vec(self, tokens):
		v = [0 for i in range(self.size())]
		for token in tokens:
			if token in self.vector:
				v[self.index(token)] += 1
		return np.array(v)

	def save(self, filename):
		f = open(filename, 'w', encoding = 'utf-8')
		for word in self.vector:
			f.write(word + '\n')
		f.close()

	def load(self, filename):
		f = open(filename, 'r', encoding = 'utf-8')
		lines = f.readlines()
		bow = [i[:-1] for i in lines]
		self.addall(bow)
		f.close()
	
	def __str__(self):
		s = "Vocabulary("
		for word in self.vector:
			s += (str(self.vector[word]) + ": " + word + ", ")
		if self.size() != 0:
			s = s[:-2]
		s += ")"
		return s

