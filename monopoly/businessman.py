import numpy as np

class Businessman():
	"""An intelligent agent that interacts with other agents with the objective to maximize his capital."""

	def __init__(self):

		self.capital = 1000 * np.random.randn() + 10000		# sig * randn + mu
		self.happiness = 10 * np.random.randn() + 50		# sig * randn + mu
		self.isAlive = True
		self.subsidiaries = 0
		self.companies = []
