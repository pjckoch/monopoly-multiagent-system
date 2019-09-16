import numpy as np
from company import Company

class Businessman():
	"""An intelligent agent that interacts with other agents with the objective to maximize his capital."""

	def __init__(self, businessmanId):
		self.id = businessmanId
		self.capital = 1000 * np.random.randn() + 10000		# sig * randn + mu
		self.happiness = 10 * np.random.randn() + 50		# sig * randn + mu
		self.isAlive = True
		self.subsidiaries = 500000 * 1 / (self.capital + 1000)
		self.companies = []
		

	def negotiate(self):


	def suicide(self):


	def declareBancrupcy(self):


	def invest(self):