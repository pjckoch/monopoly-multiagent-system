class Government():
    """An intelligent agent that interacts with other agents in order to regulate the happiness."""

    # Government Politics can be supportive, neutral or competitive

    def __init__(self):
        self.politics = "supportive"
        self.politicsSwitcher = {
            "supportive": 0.5,
            "neutral": 0,
            "competitive": -0.5,
        }
        self.avgCapital = 0

    def startAuction(self, companyId):
        return None

    def regulateSubsidiary(self,businessman):
        if (businessman.capital < (self.avgCapital * 0.5)):
            businessman.subsidiaries += 500 * self.politicsSwitcher.get("supportive", 0)
        if (businessman.capital > (self.avgCapital * 1.5)):
            businessman.subsidiaries = 0

    def regulateTax(self,company):
        return None

    def regulate(self, averageCapital, businessmenList):
        self.avgCapital = 0
        for bm in businessmenList:
            self.regulateSubsidiary(bm)
            for company in bm.companies:
                self.regulateTax(company)
