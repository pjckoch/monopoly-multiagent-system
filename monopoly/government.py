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
        self.avgCompanyValue = 0
        self.taxesStatus = []

    def startAuction(self, companyId):
        return None

    def regulateSubsidiary(self,businessman):
        if (businessman.capital < (self.avgCapital * 0.5)):
            businessman.subsidiaries += 500 * self.politicsSwitcher.get("supportive", 0)
        if (businessman.capital > (self.avgCapital * 1.5)):
            businessman.subsidiaries = 0

    def isCompanyTaxed(self, company):
        for tax in self.taxesStatus:
            if tax[0] == company.id:
                return True
        return False

    #TODO: improve tomorrow
    def regulateTax(self,company):
        if not self.isCompanyTaxed(company):
            if company.companyValue > self.avgCompanyValue:
                company.taxes += 20
                temp = [company.id, 0]
                self.taxesStatus.append(temp)
                print("Taxing Company:" + str(company.id))
        else:
            for tax in self.taxesStatus:
                if tax[0] == company.id:
                    self.taxesStatus.remove(tax)
                    print("Removed Tax from Company:" + str(company.id))

    def regulate(self, averageCapital, averageCompany, businessmenList):
        self.avgCapital = averageCapital
        self.avgCompanyValue = averageCompany
        for bm in businessmenList:
            self.regulateSubsidiary(bm)
            for company in bm.companies:
                self.regulateTax(company)
