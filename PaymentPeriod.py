class PaymentPeriod:
    

    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.balance=0

    def addWorkDay(self, workDay):
        rate = 0
        jobGroup = workDay.getJobGroup().lower()
        if jobGroup=="a":
            rate = 20
        if jobGroup=="b":
            rate = 30
        self.balance = self.balance + workDay.getHoursWorked()*rate

    def getBalance(self):
        return self.balance

    def getStartDate(self):
        return self.startDate

    def getEndDate(self):
        return self.endDate



