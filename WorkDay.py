class WorkDay: 
#this class represents a working day of an employee. 

    def __init__(self, empId, date,hoursWorked, jobGroup):
        self.empId = empId
        self.date = date
        self.hoursWorked = hoursWorked
        self.jobGroup = jobGroup

    def getDate(self):
        return self.date

    def getHoursWorked(self):
        return self.hoursWorked

    def getJobGroup(self):
        return self.jobGroup

    def getId(self):
        return self.empId

    