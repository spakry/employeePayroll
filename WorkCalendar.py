import calendar 
from PaymentPeriod import PaymentPeriod


class WorkCalendar:
    #an instance of a 'work calendar' which contains instances of work days embedded in the calendar. 
    #keeps track of the hours worked in each unique pay period. 
    #new instance for each unique employee.
    

   

    def __init__(self, employeeId):
        self.employeeId = employeeId
        self.workPeriodList=[]

    def getPeriodFromStartDate(self, startDayToCheck):
        for period in self.workPeriodList:
            if period.getStartDate()==startDayToCheck:
                return period
        return None
        
    def getEmployeeId(self):
        return self.employeeId

    def getWorkPeriodList(self):
        return self.workPeriodList

    def setWorkPeriodList(self,newWorkPeriodList):
        self.workPeriodList=newWorkPeriodList

    def insertWorkDay(self,workDay):
        #determine the period the workday belongs in.
        date = workDay.getDate()
  

        month = date.split("-")[1]
        year = date.split("-")[0]
        day = date.split("-")[2]
        
        if (0<int(day)<16):
            #corresponds to the first interval
            startDay = str(1)+ "-" + month + "-" + year 
            endDay = str(15)+ "-" + month + "-" + year 
        else:
            #second interval
            lastDayOfMonth = calendar.monthrange(int(year),int(month))[1]
            startDay = str(16)+ "-" + month + "-" + year 
            endDay = str(lastDayOfMonth) + "-" + month + "-" + year 
        result=self.getPeriodFromStartDate(startDay)
        if result==None:
            #the time interval bucket does not exist. create and place inside
            mPeriod = PaymentPeriod(startDay,endDay)
            mPeriod.addWorkDay(workDay)
            self.workPeriodList.append(mPeriod)
        else:
            #interval bucket exists. place inside.
            mPeriod = self.getPeriodFromStartDate(startDay)
            mPeriod.addWorkDay(workDay)
            
            





