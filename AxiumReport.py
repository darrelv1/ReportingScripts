import pandas as pd
from datetime import datetime


class Reporting:
    #Job Cost RFJL

    

    date = datetime.today().strftime("%m-%d-%y")

    file = "Report-" + date +".xlsx"

    jobcostdf = pd.read_excel(file)
    jobcostdfRAW = jobcostdf
   
    #removal of what is the best way to become what we can do and what we can do


    #Creation of Disposaldf off the Slicing of Disposal
    disposaldf = jobcostdf.loc[:,:][jobcostdf.Source == "Asset Disposal"]

    #Removal of Disposal off the main JBdf 
    jobcostdf = jobcostdf.loc[:,:][jobcostdf.Source != "Asset Disposal"]

    #Subsets df extracting a triple criteria for transfer 
    transferdf = jobcostdf[(~jobcostdf['Worktags'].str.contains('fund') & ~jobcostdf['Worktags'].str.contains('Fund') ) & ((jobcostdf['Line Memo'].str.contains('Tsfr', na = False)) | (jobcostdf['Journal Memo'].str.contains('Tsfr', na = False)) | ((jobcostdf.Source == 'Asset Assign Accounting')))]

    #Set deletes all duplicates
    source =  set()
    for i in jobcostdf.Source:
        source.add(i)
    
    #what is the best way to bec


  #Additiondf utlizing the not (bitwise operator)
   # Additiondf = jobcostdf[((~jobcostdf['Line Memo'].str.contains('Tsfr', na = False)) | (~jobcostdf['Journal Memo'].str.contains('Tsfr', na = False))) & ((jobcostdf.Source != 'Asset Assign Accounting') & (jobcostdf['Worktags'].str.contains("Fund", na =False)))]
    #Additiondf = jobcostdf[((~jobcostdf['Line Memo'].str.contains('Tsfr', na = False)) & (~jobcostdf['Journal Memo'].str.contains('Tsfr', na = False))) & ((jobcostdf.Source != 'Asset Assign Accounting'))]
    
    #Additiondf =  jobcostdf[(jobcostdf.Source.isin(source) & ~jobcostdf['Line Memo'].str.contains('Tsfr', na = False) & ~jobcostdf['Line Memo'].str.contains('Trsfr', na = False)  & ~jobcostdf['Journal Memo'].str.contains('Tsfr', na = False) & ~jobcostdf['Journal Memo'].str.contains('Trsfr', na = False))]

    #Additiondf = Additiondf[Additiondf['Worktags'].str.contains('Fund', na = False)  & Additiondf['Source'] != "Asset Assign Accounting "]

    ##transferdf = pd.concat([transferdf1,transferdf2],axis=0)
    

    Additiondf =  jobcostdf[(jobcostdf.Source.isin(source) & (jobcostdf['Worktags'].str.contains('fund') | jobcostdf['Worktags'].str.contains('Fund') | ~jobcostdf['Line Memo'].str.contains('Tsfr', na = False) & ~jobcostdf['Line Memo'].str.contains('Trsfr', na = False)  & ~jobcostdf['Journal Memo'].str.contains('Tsfr', na = False) & ~jobcostdf['Journal Memo'].str.contains('Trsfr', na = False)))]
    Additiondf = Additiondf[ (Additiondf['Worktags'].str.contains('fund') | Additiondf['Worktags'].str.contains('Fund')) | ~Additiondf['Source'].str.contains("Asset Assign Accounting")]

    #Creating Stats
    Total_Jb = sum(jobcostdf['Ledger Debit Amount']-jobcostdf['Ledger Credit Amount'])
    Total_Add = sum(Additiondf['Ledger Debit Amount']-Additiondf['Ledger Credit Amount'])
    Total_trans = sum(transferdf['Ledger Debit Amount']-transferdf['Ledger Credit Amount'])
    Total_dis = sum(disposaldf['Ledger Debit Amount']-disposaldf['Ledger Credit Amount'])

    #Creating a container
    reports_list= [jobcostdfRAW, disposaldf, jobcostdf, transferdf, Additiondf]
    reports_str= ["jobcostdfRAW","disposaldf", "jobcostdf", "transferdf" , "Additiondf" ]
    reportname_list = []

    dictionaryholder = {}
    index = 0 
    for k in reports_str:
        dictionaryholder[k] = reports_list[index]
        index += 1 




        

    statdict = {"Total Job Cost": Total_Jb, "Total Addition": Total_Add, "Total Transfers": Total_trans }

    ##dictionaryholder = {k : v  for k in reports_str for v in reports_list}

    stringlink = "output/JobCostRFJL_"+date+".xlsx"

    # Specify the ExcelWriter Object:
    
    with pd.ExcelWriter(stringlink) as writer:
        jobcostdfRAW.to_excel(writer, sheet_name="Job_Cost_RAW")
        Additiondf.to_excel(writer, sheet_name="Additions")
        disposaldf.to_excel(writer, sheet_name="Disposal")
        transferdf.to_excel(writer, sheet_name="Transfers")

        for i in dictionaryholder.keys():
            
            temp = dictionaryholder[i]
            if temp.empty:
                        continue

            temp = temp.pivot_table(index = "Source", aggfunc= sum)
            
            temp = temp.iloc[:,6:8]
            total = temp["Ledger Debit Amount"] - temp["Ledger Credit Amount"]
            temp = pd.concat([temp, total], axis =1)



            name = i + " PivotTable"
            totalname = i + "Total"
            print(f"{name}: {temp}")
            temp.to_excel(writer,sheet_name= name)



        
