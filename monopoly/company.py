import numpy as np

class Company():
	"""Company Object."""

	def __init__(self):

		self.turnOver = 1000 * np.random.randn() + 10000		# sig * randn + mu
		self.fixedCost = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.variableCost = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.taxes = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.profitHistory = []
        self.frequency = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.necessity = 1000 * np.random.randn() + 10000		# sig * randn + mu
        self.companyValue = 1000 * np.random.randn() + 10000		# sig * randn + mu


# TODO - Initialize company atributes
