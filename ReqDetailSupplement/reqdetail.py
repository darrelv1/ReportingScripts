from BaseReport import Basereports
import pandas as pd 

#Preparing Reqdetail DataFrame 
reqdf = pd.read_excel("reqdetails0622.xlsx", header = 5)
reqdf = reqdf.rename(columns={"Site ":"Site"})
reqdf = reqdf.rename(columns={"Spend Category ":"Spend Category"})



Site_req = reqdf.groupby(['Site'])
Spend_req = reqdf.groupby(['Spend Category'])
Spend_req['Capital?'].value_counts().sort_values(ascending = False)

Company_Spend = reqdf.groupby(['Company', 'Spend Category'])
Company_Spend['Capital?'].value_counts().sort_values(ascending = False)


Spend_Company = reqdf.groupby(['Spend Category', 'Company'])
Spend_Company['Capital?'].value_counts().sort_values(ascending = False)

#Creation of Dataframe that will have multilevel index 
SpendbyCo = Spend_req['Company'].value_counts().sort_values(ascending= False)
#itertuples = tuple(iter.zip_longest(SpendbyCo.index.get_level_values(0), SpendbyCo.index.get_level_values(1)))

SpendbyCOdf = pd.DataFrame(SpendbyCo) 

#Capturing all the insuite-related
SpendbyCo[SpendbyCo.index.get_level_values(0).str.contains(r'([Ss]uite)')]







SpendbyCo[(SpendbyCo.index.get_level_values(1).str.contains(r'(HCN)'))]
SpendbyCo[SpendbyCo.index.get_level_values(0).str.contains(r'^[^iI]')]

reqdf_suite = reqdf[reqdf['Spend Category'].str.contains(r'([Ss]uite)', na=False)]
reqdf_suite['Memo'][reqdf_suite['Memo'].str.contains(r'(\d)', na=False)]

#Listing Tree of what has numbers 
[reqdf_suite['Memo'].str.contains(r'(\d*)')]
Suite_units = pd.DataFrame(reqdf_suite['Memo'].str.extract(r'(\d+)'))

reqdf_suite['Unit_Number'] = Suite_units

#Remove Columns
del(reqdf_suite['Unnamed: 11'])
del(reqdf_suite['Unnamed: 12'])

#Reading Asset Report and filtering out not in service lines and removing unecessary Columns
assetdf =pd.read_excel("asset0622.xlsx", header = 24)
assetdf = assetdf[assetdf['Asset Status'].str.contains(r'([I. ][Ss]ervice)')]
reqdf_suite_condensed = assetdf[['Worktags','Spend Category','Asset ID','Company','Asset Name','Description' ]]

#Suite Modified Dataframe with Suite Number Parsed
#reqdf_suite_condensed['Worktags'].str.extract(r'(Site: [\d][\d][\d][\d][\d][\s])')


#1. Extracting the site out of the worktags 
asset_site_list = pd.DataFrame(reqdf_suite_condensed['Worktags'].str.extract(r'(Site: [\d][\d][\d][\d][\d][\s])'))
reqdf_suite_condensed['Site'] = asset_site_list

#2. Asset Dataframe w/ Suite Number Parsed
assetdf_suite_condensed = reqdf_suite_condensed
assetdf_suite_condensed['Site'] = assetdf_suite_condensed['Site'].str.replace(r'(Site:[\s])',"ST", regex=True)


#Create the site columns for Asset Data frame 
def createSiteCol(dataframe):    
    df = dataframe

    #1. Extracting the site out of the worktags and appending the listing as series in the asset df
    asset_site_list = pd.DataFrame(df['Worktags'].str.extract(r'(Site: [\d][\d][\d][\d][\d][\s])'))
    df['Site'] = asset_site_list
    #2. Formatting the site col to start with "ST"
    df['Site'] = df['Site'].str.replace(r'(Site:[\s])',"ST", regex=True)
    return df



#3. Creation of the "Suite_Number" column from both of the coulmn source Description and Asset Name and assign them thier own columns in the main Asset Dataframe
assetSuiteNumber_Description = pd.DataFrame(assetdf_suite_condensed['Description'].str.extract(r'(\d+)'))
assetSuiteNumber_Name = pd.DataFrame(assetdf_suite_condensed['Asset Name'].str.extract(r'(\d+)'))
assetdf_suite_condensed['SuiteNumber_Description'] = assetSuiteNumber_Description
assetdf_suite_condensed['SuiteNumber_Name'] = assetSuiteNumber_Name



#The working Asset Dataframe now is "assetdf_suite_condensed"
#The working REQ Dataframe now is "reqdf_suite"






#the function that will be apply to every line in the reqdetail 
def assetMatch(lookupValue, site, masterIndex):
    if type(lookupValue) == str:
        unit_series = assetdf_suite_condensed['SuiteNumber_Name'].str.contains(lookupValue)
        indexList = iterIndex(unit_series)
        asset =  indexSiteMatch(indexList, site)
        req = reqdf_suite.loc[masterIndex,"Requisition #"]
        #print(f"{masterIndex} : [{asset}, {req}]")
        a = [masterIndex, req, asset]
        return  a

# The alternative        
def assetMatch_alternative(lookupValue, site, masterIndex):
    if type(lookupValue) == str:
        unit_series = assetdf_suite_condensed['SuiteNumber_Description'].str.contains(lookupValue)
        indexList = iterIndex(unit_series)
        asset =  indexSiteMatch(indexList, site)
        req = reqdf_suite.loc[masterIndex,"Requisition #"]
        #print(f"{masterIndex} : [{asset}, {req}]")
        a = [masterIndex, req, asset]
        return  a

    
#helper function --> returns a dictionary of (index , True) -- index of all  suite numbers that match up to the lookup value from assetMatch function 
def iterIndex(indexSeries):
    templist = {}
    for ind,val in indexSeries.items():
        
        if(val == True):
            templist[ind] = val
    return templist


#helper function --> Utilzing the dictionary, this function captures the it's exact match by site. when the site matches it returns the Asset ID from the asset df  
def indexSiteMatch(indexdict, site):
    site += " "
    for index, value in indexdict.items():
        #print("in the iterSiteMatch")
        indexSite = assetdf_suite_condensed.loc[index,'Site']
        if indexSite == site:
            assetID = assetdf_suite_condensed.loc[index, "Asset ID"]
            #print(assetID)
            return assetID

        
        
      #suite 109  , index 4, ST10011



#START HERE
def startingPoint(alternative = False):
    a = [reqdf_suite.index]
    dictItem = []

    for i in a[0]:
        lookupValue = reqdf_suite.loc[i,"Unit_Number"] 
        site = reqdf_suite.loc[i,"Site"]
        reqIndex = i
    
        #print(f"{type(lookupValue)} : {lookupValue}")
        
        if type(lookupValue) == float:
            print(type(str(lookupValue)))
            lookupValue = str(lookupValue)
        elif type(lookupValue) != str:
            print(type(lookupValue.to_string(index=False)))
            lookupValue = lookupValue.to_string(index=False)
        if alternative:
            item = assetMatch_alternative(lookupValue, site, i )
        else:
            item = assetMatch(lookupValue, site, i )
        print(item)
        if item != None:
            dictItem.append(item)
    
    grandresult = pd.DataFrame(dictItem)
    return grandresult

answer = startingPoint(True)
with pd.ExcelWriter("reqdetail_results.xlsx") as writer:
     answer.to_excel(writer )


"""
def lookup_asset(lookup_value, reference_dataframe, ):

        reference_dataframe


    return 
"""

#Opening Balance Asst Match 
#index filter of master  and IFRS 
master_filterIndex = assetDf["Asset ID"].str.contains(r'([mM]aster)')
ifrs_filterIndex = assetDf["Asset ID"].str.contains(r'([Ii][fF][rR][Ss])')
OB_filterIndex =  assetDf["Asset ID"].str.contains(r'([Oo]pening [Bb]alance)')