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
        self.subsidiariesStatus = []

        self.taxValue = 60 #20
        self.subsidyValue = 50 #100
        self.governmentMoney = 0

    def startAuction(self, companyId):
        return None

    def isPersonHelped(self, bm):
        for subs in self.subsidiariesStatus:
            if subs[0] == bm.id:
                return True
        return False

    #TODO: improve
    def regulateSubsidiary(self,businessman):
        if not self.isPersonHelped(businessman):
            # if (businessman.capital < (self.avgCapital * 0.5)):
            if businessman.capital < 10000 and self.governmentMoney - self.subsidyValue > 0:
                businessman.subsidiaries += self.subsidyValue
                self.governmentMoney -= self.subsidyValue
                temp = [businessman.id, 0] # We put a pair instead of ID only because later on we will increment the counter to 3 days per subsidiary
                self.subsidiariesStatus.append(temp)
                print("Helping Businessman:" + str(businessman.id))
        else:
            for subs in self.subsidiariesStatus:
                if subs[0] == businessman.id:
                    self.subsidiariesStatus.remove(subs)
                    businessman.subsidiaries = 0
                    print("Removed Subsidiary from Businessman:" + str(businessman.id))

    def isCompanyTaxed(self, company):
        for tax in self.taxesStatus:
            if tax[0] == company.id:
                return True
        return False

    #TODO: improve
    def regulateTax(self,company):
        if not self.isCompanyTaxed(company):
            if company.companyValue > self.avgCompanyValue:
                company.taxes += self.taxValue
                self.governmentMoney += self.taxValue
                temp = [company.id, 0]
                self.taxesStatus.append(temp)
                print("Taxing Company:" + str(company.id))
        else:
            for tax in self.taxesStatus:
                if tax[0] == company.id:
                    self.taxesStatus.remove(tax)
                    company.taxes = 0
                    print("Removed Tax from Company:" + str(company.id))

    def regulate(self, averageCapital, averageCompany, businessmenList):
        self.avgCapital = averageCapital
        self.avgCompanyValue = averageCompany
        for bm in businessmenList:
            self.regulateSubsidiary(bm)
            for company in bm.companies:
                self.regulateTax(company)
