
from BaseReport import *

tfile = "Report-10-11-22.xlsx"
tfile1 = "project.xlsx"
tfile2 = "project2.xlsx"
tfile3 = "project3.xlsx"

#March14_flow = flowthrough(tfile)
#March14_flow.printer()


March14_jobcap = Capital_Jobcostreport(tfile)
March14_jobcap.printer()
March14_jobcap.anaylsisReport()
March14_jobcap = Capital_Jobcostreport(tfile1)
March14_jobcap.printer()
March14_jobcap.anaylsisReport()
March14_jobcap = Capital_Jobcostreport(tfile2)
March14_jobcap.printer()
March14_jobcap.anaylsisReport()
# March14_jobcap = Capital_Jobcostreport(tfile3)
# March14_jobcap.printer()
# March14_jobcap.anaylsisReport()





