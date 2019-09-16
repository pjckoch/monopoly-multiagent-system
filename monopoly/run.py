from environment import Environment


if __name__	== "__main__":
	environment = Environment()
	# print businessmen id's
	print([bm.id for bm in environment.listOfPeople])
	# print companies id's
	print([company.id for company in environment.listOfCompanies])
