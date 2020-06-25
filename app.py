from flask import Flask 
import sqlite3
import json
from flask import request
from DatabaseRepository import DatabaseRepository
from WorkCalendar import WorkCalendar
from PaymentPeriod import PaymentPeriod
from WorkDay import WorkDay
import io
import csv
from datetime import datetime

app = Flask(__name__)



def storeFileRecord(fileName):
    numToCheck = fileName.split("-")[2]
    app.logger.info(str(numToCheck))
    #check if file num exists in records.
    repo = DatabaseRepository()
    numList= repo.getAllRecordNum()
    for entry in numList:
             number = entry[0]
             app.logger.info(str(number))
             if numToCheck==number:
                 return False
    repo.insertReportNum(numToCheck)
    return True
             


def createDB():
    conn = None
    conn = sqlite3.connect('employees.db')
    createTables(conn)
    

def createTables(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS times_worked (
                [EmployeeId] int,
                [Date_] date,
                [HoursWorked] int,
                [JobGroup] varchar(5))
                ''' )
        c.execute('''CREATE TABLE IF NOT EXISTS time_report_record (
                [ID] int,
                [Date_] date) ''')
        conn.commit()
    except Error as e:
        print(e)

def generateJSON(workCalendarList):
    employeeReportList=[]
    #generate json for return
    for mWorkCalendar in workCalendarList:
        #elements contains the start, end and balance for each period
        workPeriodList = mWorkCalendar.getWorkPeriodList()
        for paymentPeriod in workPeriodList:
            startDate = paymentPeriod.getStartDate()
            endDate = paymentPeriod.getEndDate()
            balance = paymentPeriod.getBalance()

            payPeriod={}
            payPeriod['startDate']= paymentPeriod.getStartDate()
            payPeriod['endDate']= paymentPeriod.getEndDate()
            #populate list here
            reportObj = {}
            reportObj['employeeId']= mWorkCalendar.getEmployeeId()
            reportObj['amountPaid']= "$" + str(paymentPeriod.getBalance())
            reportObj['payPeriod']= payPeriod
            employeeReportList.append(reportObj)

    employeeReports={}
    employeeReports['employeeReports'] = employeeReportList

    jsonData = {}
    jsonData['payrollReport']=employeeReports
    return jsonData



def generateListUniqueId(entriesList):
    idList = []
    for entry in entriesList:
        mId = entry.getId()
        if mId not in idList:
            idList.append(mId)
    return idList



#create instance of db
createDB()

@app.route("/")
def main():
    return "hello world"

@app.route('/payroll', methods=['GET','POST'])
def getPayroll():
    entriesList = []
    #contains a list of lists which are individually unique in employee id.
    sortedByIdLists = []

    if request.method == 'GET':
         #get all entries from the db and parse into json.
        mRepository=DatabaseRepository()
        workDayList = mRepository.getAllWorkDays()
        app.logger.info(str(workDayList))
        for entry in workDayList:
            app.logger.info(str(entry))
            empId = entry[0]
            date = entry[1]
            hoursWorked = entry[2]

            jobGroup = entry[3]
            app.logger.info("type" + str(jobGroup))
            entriesList.append(WorkDay(empId, date,hoursWorked, jobGroup))

         #subset the list by employeeId in increasing order
        idList = generateListUniqueId(entriesList)
        app.logger.info(str(idList))
        workCalendarList = []
        for mId in idList:
            sublist = [x for x in entriesList if x.getId()==mId]
            app.logger.info("sublists:"+ str(sublist))
            sortedByIdLists.append(sublist)
        for commonIdWorkDayList in sortedByIdLists:
            workCalendar =WorkCalendar(commonIdWorkDayList[0].getId())
            for elem in commonIdWorkDayList:
                app.logger.info("workday" , elem.getDate())
                workCalendar.insertWorkDay(elem)
            workCalendarList.append(workCalendar)


        #arrange list of calendars to increasing employeeId
        sortedWorkCalendarList = sorted(workCalendarList,key=lambda workCalendar : workCalendar.getEmployeeId())
        #arrange workIntervals for each calendar to increasing start date.
        for workCalendar in sortedWorkCalendarList:
            workPeriodList = workCalendar.getWorkPeriodList()
            newWorkPeriodList= sorted(workPeriodList,key=lambda workPeriod :  datetime.strptime(workPeriod.getStartDate(), "%d-%m-%Y"))
            workCalendar.setWorkPeriodList(newWorkPeriodList)

        #format into json
        jsonDataString = generateJSON(sortedWorkCalendarList)
        jsonData = json.dumps(jsonDataString)
        #ready to send
        return jsonData





    if request.method == 'POST':
         #check if file has been uploaded previously.
         #parse csv file and save to db.
        f = request.files['data_file']
        if not f:
        	return "No file"

        fileName = f.filename
        #todo remove 
        #if storeFileRecord(fileName)==True:
             #this is a unique file. Insert.
        if True:
            stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream,delimiter=',')
            


            repo = DatabaseRepository()
            next(csv_input)
            for row in csv_input:
                app.logger.info("raw input" , str(row))
                
                date = row[0]
                hours = row[1]
                empId = row[2]
                app.logger.info("date split"+str(date))
                app.logger.info("hour split"+str(hours))
                jobGroup = row[3]
                data = (empId,date,hours,jobGroup)
                app.logger.info("data"+str(data))
                repo.insertWorkEntry(data)
                
            
            
            
            return "success!"
        #todo remove
        #else:
            #this file exists in the system throw.
           # return "This file is a duplicate"






if __name__ == '__main__':
    app.run(debug=True)