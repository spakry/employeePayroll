
import yaml
from datetime import date
import sqlite3

class DatabaseRepository:

    def __init__(self):
        self.conn = sqlite3.connect('employees.db') 
        self.employeeIdIndex = 0
        self.dateIndex = 1
        self.hoursWorkedIndex = 2
        self.jobGroupIndex = 3 

    def getAllWorkDays(self):
        cur = self.conn.cursor()
        result = cur.execute('''SELECT * FROM times_worked''')
        workDayList = cur.fetchall()      
        return workDayList
       


    def getAllRecordNum(self):
        cur = self.conn.cursor()
        result = cur.execute('''SELECT * FROM time_report_record''')
        reportNumList = cur.fetchall()
        return reportNumList
        

    def insertReportNum(self,idNum):
        todayDate = date.today() 
        cur = self.conn.cursor()
        result = cur.execute('''INSERT INTO time_report_record(ID,Date_) VALUES (?,?) ''',(idNum,todayDate))
        self.conn.commit()
        
    def insertWorkEntry(self,data):
        cur = self.conn.cursor()
        result = cur.execute('''INSERT INTO times_worked(EmployeeId,Date_ ,HoursWorked,JobGroup) VALUES (?,?,?,?) ''',data)
        self.conn.commit()




