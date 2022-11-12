
from BaseReport import *
import pandas as pd

tfile = "Report-10-11-22.xlsx"
tfile1 = "project.xlsx"
tfile2 = "project2.xlsx"
tfile3 = "project3.xlsx"

#March14_flow = flowthrough(tfile)
#March14_flow.printer()


# March14_jobcap = Capital_Jobcostreport(tfile, False)
# March14_jobcap.printer("1")
# March14_jobcap.anaylsisReport()
# March14_jobcap = Capital_Jobcostreport(tfile1, False)
# March14_jobcap.printer("2")
# March14_jobcap.anaylsisReport()
# March14_jobcap = Capital_Jobcostreport(tfile2, False)
# March14_jobcap.printer("3")
# March14_jobcap.anaylsisReport()
# March14_jobcap = Capital_Jobcostreport(tfile3, False)
# March14_jobcap.printer("4")
# March14_jobcap.anaylsisReport()

ACCOUNTANT = input("Which Accountant")

df = pd.read_excel(r"Project Status Reports/09 Project Status Report.xlsx", sheet_name="Project List", header=3)
table = df[df["Responsible Accountant"] == ACCOUNTANT]
listing = table.loc[:, ["Project Number"]]

#For each project in listing there will be a temporary subset dataframe of the RFJL DF
#Then each one of those temporary subset dataframe will be ran pass through 


rfjl = pd.read_excel(r"Project Status Reports/RFJL11-11.xlsx", header=0)
rfjl = rfjl[rfjl["Project #"].notna()]

#Dict obj that will contain all ther error projects 

errorReport = {}
successReport = {}
successReportlist=pd.DataFrame();
def listingDf(prjNum):
    
    try:
        iterDF = rfjl[rfjl["Project #"].str.contains(prjNum)]
        tempOBJ = Capital_Jobcostreport(iterDF, True)
        #print(f"Report of: {prjNum}")
        fileName = prjNum 
        tempOBJ.printer(fileName)
        tempOBJ.anaylsisReport(fileName)
        entry = { "Project Number" : prjNum,
                "Accountant": ACCOUNTANT}
        print(successReportlist)
        successReportlist = successReportlist.append(entry, ignore_index=True)
        print(successReportlist)
       # print(f"TOTAL: {str(tempOBJ.total)} RAW TOTAL {str(tempOBJ.reportTotal)}")
       # successReportdf = pd.DataFrame(successReportlist)
        #print(successReportdf)
        
       
    except:
       # print(f"The Excemption was: {prjNum}: ")
       errorReport[prjNum] = "not Good"





#Iterating through each project number for the respective Accountant
listing['Project Number'].map(listingDf)

#listingDf("PRJ-2021-002302")

#print(rfjl)

successReportdf = pd.DataFrame(successReportlist)
print(successReportdf)