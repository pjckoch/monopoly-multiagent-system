class Government():
    """An intelligent agent that interacts with other agents in order to regulate the happiness."""

    def __init__(self):
        self.listOfTaxes = []
        self.listOfSubsidiaries = []
        self.happinessIndicator = 0

    def hello(self):
        print("Hellooooo")

    def changeTax(self, companyId):
        return self.listOfTaxes

    def changeSubsidiary(self, businessmanId):
        return self.listOfSubsidiaries

    def startAuction(self, companyId):
        return None
