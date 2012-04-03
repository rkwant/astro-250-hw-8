import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import time
import csv
import urllib
import random

#list of names to be used
mfirstnames = []
ffirstnames = []
lastnames = []

def getNormal(mu, sigma):
	"""return a random number from a normal distribution with mean mu and variance sigma"""
	return int(np.random.normal(mu, sigma, 1)[0])
	
def getBinomial(n, p):
	"""return a random number from a binomial distribution with parameters n and p """
	return np.random.binomial(n, p, 1)[0]
	
def downloadNames():
	"""download lists of names from the US census """
	
	#urls
	mfirsturl = "http://www.census.gov/genealogy/names/dist.male.first"
	ffirsturl = "http://www.census.gov/genealogy/names/dist.female.first"
	lasturl = "http://www.census.gov/genealogy/names/dist.all.last"
	
	#download the files and store the names in lists for later use
	mfirstnamef = urllib.urlopen(mfirsturl)
	for line in mfirstnamef:
		mfirstnames.append(line.split()[0])
		
	ffirstnamef = urllib.urlopen(ffirsturl)
	for line in ffirstnamef:
		ffirstnames.append(line.split()[0])
		
	lastnamef = urllib.urlopen(lasturl)
	for line in lastnamef:
		lastnames.append(line.split()[0])
		
def getName(gender):
	"""return a name with a given gender.  0 for female, 1 for male """
	if gender == 1:
		return mfirstnames[np.random.randint(0, len(mfirstnames))]+" "+lastnames[np.random.randint(0, len(lastnames))]
	else:
		return ffirstnames[np.random.randint(0, len(ffirstnames))]+" "+lastnames[np.random.randint(0, len(lastnames))]	

class Timer:
	"""class that can be used to time processes """
	def __init__(self):
		self.start = 0 #when the timer was started
		self.end = 0 #when the timer was stopped
	
	#start the timer
	def __enter__(self):
		self.start = time.clock()
		
	#stop the timer and print the time
	def __exit__(self, *args):
		self.stop = time.clock()
		passed = self.stop - self.start
		#print passed

class Bear:
	"""Class that models a bear
	constructor takes parameters
	env: environment in which the bear lives
	name: name of bear
	mom
	dad
	sex: the probability that the bear will be male (where male is 1 and female is 0)
	mu: average age of the bear
	sigma: variance of bear's life
	
	attributes:
		env: environment
		name
		maximumAge: age at which bear dies
		sex
		mom
		dad
		kids (list)
		age
		matingAge:age at which the bear is sexually mature
		matingGap:minimum time between cubs
		yearsSinceCub:number of years since the bear has hada cub
	"""
	def __init__(self, env, name, mom, dad, sex=0.5, mu=35, sigma=5):
		self.env = env
		self.name = name
		self.maxAge = getNormal(mu, sigma)
		self.sex = getBinomial(1, sex)
		self.mom = mom
		self.dad = dad
		self.kids = []
		self.age = 0
		self.matingAge = 5
		self.matingGap = 5
		self.yearsSinceCub = self.matingGap
		self.children = []
		
	def __str__(self):
		return str(self.name)+"("+str(self.sex)+")"
				
	def addChild(self, child):
		"""add a child to the list of children """
		self.children.append(child)
	
	def getChildren(self):
		"""return a list of children"""
		return self.children
		
	def timeToDie(self):
		"""return true if it is time for the bear to die """
		return self.age > self.maxAge
	
	def matable(self):
		"""return true of the bear is old enough to mate and has not had a cub for matingGap years """
		return (self.age >= self.matingAge and self.yearsSinceCub > self.matingGap)
	
	def attemptMate(self, availableBears):
		"""attempt to mate each bear in available bears.  stop looking when one mating is successful"""
		if self.matable():
			for bear in availableBears:
				if bear.woo(self):
					#if wooing is successful, actually mate
					bear.mate(self)
					break
	
	def woo(self, other):
		"""check to see if another bear will mate with this bear """
		if self.mom == None or other.mom == None:
			return (self.matable() and not (other.sex == self.sex) and (abs(self.age-other.age) <= 10))
		else:
			return (self.matable() and not (other.sex == self.sex) and not (self.mom == other.mom and self.dad == other.dad) and (abs(self.age-other.age) <= 10))
	
	
	def mate(self, other):
		"""generate a child and update the environment and other bear """
		self.yearsSinceCub = 0
		self.env.generateChild(self, other)
		other.helpMate(self)
		
	def helpMate(self, other):
		"""reset the number of years since having a cub to zero """
		self.yearsSinceCub = 0
	
	def passTime(self):
		"""tell the bear that another year has passed """
		self.age += 1
		self.yearsSinceCub += 1
		if self.timeToDie():
			self.env.killBear(self)
		elif self.matable():
			self.env.auction(self)
		
class Env:
"""Class to contain a population of bears. parameters:	simLength: number of years in the simulation	sexPercent: the probability that a male cub will be born over a female cub """
	def __init__(self, simLength=150, sexPercent = 0.5):
		self.year = 0
		
		self.bears = set()
		self.deadBears = set()
		self.matable = []
		self.toKill = set()
		self.usedNames = set()
		
		self.bearCount = 0
		self.simLength = simLength
		self.sexPercent = sexPercent
		
		self.oneHundredCount = 0
		
		#initialize the population
		self.addBear(Bear(self, "Adam", None, None, sex=1))
		self.addBear(Bear(self, "Eve", None, None, sex=0))
		self.addBear(Bear(self, "Mary", None, None, sex=0))
		
	def addBear(self, bear):
		"""add a bear to the environment """
		self.bears.add(bear)
		self.bearCount+=1
		self.usedNames.add(bear.name)
		
	def getBears(self):
		"""reutnr the set of bears who are alive """
		return self.bears.copy()
		
	def getMates(self):
		"""return a list of bears that can mate """
		return self.matable
		
	def killBear(self, bear):
		"""kill a bear by moving it to set of bears to be killed"""
		self.toKill.add(bear)
		
	def generateChild(self, bear1, bear2):
		"""generate a child for two particular bears and update the environment """
		
		#generate a name
		testName = getName(0)
		while testName in self.usedNames:#loop until the name is unique
			testName = getName(0)
		
		#create the new bear and add it
		if bear1.sex == 0:
			bear = Bear(self, testName, bear1, bear2, sex = self.sexPercent)
			self.addBear(bear)
			bear1.addChild(bear)
			bear2.addChild(bear)
		else:
			bear = Bear(self, testName, bear2, bear1, sex = self.sexPercent)
			self.addBear(bear)
			bear1.addChild(bear)
			bear2.addChild(bear)
	
	def auction(self, bear):
		"""add a bear to the list of bears that can mate in a given year """
		self.matable.append(bear)
		
	def getRandomBear(self):
		"""return a random living bear """
		return random.sample(self.bears, 1)[0]
		
	def run(self):
		"""run the simulation
		returns a tuple with (total number of bears, number of alive bears, number of dead bears, number of bears alive during year 100)
		"""
		
		#loop through the number of years
		for i in range(0, self.simLength):
			
			self.matable = []#reset the list of bears that can mate
			self.toKill = set()#reset the bears to be killed
			
			with Timer():
				#tell each bear that time is passing
				for bear in self.bears:
					bear.passTime()
			
			with Timer():
				#kill bears that need to be killed
				for bear in self.toKill:
					self.bears.remove(bear)
					self.deadBears.add(bear)
			
			with Timer():
				#perform mating
				for j in range(0, len(self.matable)):
					bear = self.matable[j]
					bear.attemptMate(self.matable[j+1:])
			
			#record the number of bears alive if the year is 100
			if i == 100:
				self.oneHundredCount = len(self.bears)
			#print i,self.bearCount,len(self.bears),len(self.deadBears)
		return (self.bearCount,len(self.bears),len(self.deadBears), self.oneHundredCount)
	
	def showGraph(self):
		"""show a graph of all bears that are alive"""
		G = nx.Graph()
		for bear in self.bears:
			mom = bear.mom
			dad = bear.dad
			if dad!=None and mom != None:
				G.add_edges_from([(str(mom),str(mom)+"-"+str(dad)),(str(mom)+str(dad),str(dad)), (str(mom)+str(dad), str(bear))])
		nx.draw_spring(G)
		plt.show()
		
	def randBearGenealogy(self):
		"""show all direct older relatives of a random bear"""
		G = nx.Graph()
		bear = self.getRandomBear()
		self.helpGenes(G, bear.mom)
		self.helpGenes(G, bear.dad)
		nx.draw_spring(G)
		plt.show()
	
	def helpGenes(self, G, bear):
		"""helper method to help with the plotting"""
		for child in bear.getChildren():
			mom = child.mom
			dad = child.dad
			G.add_edges_from([(str(mom),str(mom)+"-"+str(dad)),(str(mom)+str(dad),str(dad)), (str(mom)+str(dad), str(child))])
		if (bear.mom != None and bear.dad != None):
			self.helpGenes(G,bear.mom)
			self.helpGenes(G,bear.dad)
			
				
				
				
#G=nx.Graph()				
#G.add_edges_from([("hello","world"),(1,3), (4, 5)])
#nx.draw(G)
#plt.show()				
				
def runSimulation(l):
	"""run l simulations and record the results in a text file"""
	with open("results.txt", "w") as f:
		for n in range(0, l):
			env = Env()
			res = env.run()
			f.write(str(res[0])+","+str(res[1])+","+str(res[2])+","+str(res[3]))
			f.write("\n")

def runGenderSimulation(l, increment):
	"""for each value of sexPercent from 0 to 0.5 in increments of increment, run l simulations and record the data"""
	with open("genderResults.txt", "w") as f:
		for i in decRange(0, 0.5, increment):
			print "sex percent is "+str(i)
			for n in range (0, l):
				print n,
				env = Env(sexPercent = i)
				res = env.run()
				f.write(str(i)+","+str(res[0])+","+str(res[1])+","+str(res[2])+","+str(res[3]))
				f.write("\n")
			print
			
def plotGenderData(fname):
	"""show a graph that shows the average number of bears alive for a given p(male)"""
	fileReader = csv.reader(open(fname, 'rb'), delimiter=',')
	bins = {}
	indices = []
	for row in fileReader:
		index = float(row[0])
		alive = int(row[2])
		if index not in bins:
			bins[index] = 0
		if index not in indices:
			indices.append(index)
		bins[index] += alive
	print bins
	
	values = []
	for index in indices:
		values.append(float(bins[index])/100)
	
	plt.plot(indices, values, 'ro')
			
def decRange(start, stop, inc):
	"""generator of a non integer list from start to stop with increments of inc"""
	current = start
	while current < stop:
		yield current
		current += inc
		
#download the names
downloadNames()