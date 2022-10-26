
from BaseReport import *

tfile = "Report-10-11-22.xlsx"

March14_flow = flowthrough(tfile)
March14_flow.printer()


March14_jobcap = Capital_Jobcostreport(tfile)
March14_jobcap.printer()




