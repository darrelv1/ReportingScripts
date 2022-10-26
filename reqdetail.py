from email.mime import base
from BaseReport import Basereports
import pandas as pd

#Preparing/cleaning Reqdetail DataFrame 
reqdf = pd.read_excel("reqdetails0622.xlsx", header = 5)
reqdf = reqdf.rename(columns={"Site ":"Site"})
reqdf = reqdf.rename(columns={"Spend Category ":"Spend Category"})# Clean up ofRemove Columns
del(reqdf['Unnamed: 11'])
del(reqdf['Unnamed: 12'])


#Preparing/Cleaning Asset Dataframe
assetdf =pd.read_excel("asset0622.xlsx", header = 24)


def analyzeDetails():
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
    






def produceSuiteReq(baseDF):

    # Dataframe for In-Suite related requisitons/POs
    reqdf_suite = baseDF[baseDF['Spend Category'].str.contains(r'([Ss]uite)', na=False)]
    reqdf_suite['Memo'][reqdf_suite['Memo'].str.contains(r'(\d)', na=False)]

    #New Dataframe that extracts the suite #'s off the column
    [reqdf_suite['Memo'].str.contains(r'(\d*)')]
    Suite_units = pd.DataFrame(reqdf_suite['Memo'].str.extract(r'(\d+)'))

    #Appending the extracted suite # on to it's own columns to the suite dataframe
    reqdf_suite['Unit_Number'] = Suite_units

    return reqdf_suite


def produceSuiteAsset(baseDF):

    #Reading Asset Report and filtering out not in service lines and removing unecessary Columns
    assetdf = baseDF[baseDF['Asset Status'].str.contains(r'([I. ][Ss]ervice)')]
    assetdf = assetdf[['Worktags','Spend Category','Asset ID','Company','Asset Name','Description' ]]


    #Suite Modified Dataframe with Suite Number Parsed
    #1. Extracting the site out of the worktags 
    asset_site_list = pd.DataFrame(assetdf['Worktags'].str.extract(r'(Site: [\d][\d][\d][\d][\d][\s])'))
    assetdf['Site'] = asset_site_list

    #2. Asset Dataframe w/ Suite Number Parsed
    assetdf['Site'] = assetdf['Site'].str.replace(r'(Site:[\s])',"ST", regex=True)

    #3. Creation of the "Suite_Number" column from both of the coulmn source Description and Asset Name and assign them thier own columns in the main Asset Dataframe
    assetSuiteNumber_Description = pd.DataFrame(assetdf['Description'].str.extract(r'(\d+)'))
    assetSuiteNumber_Name = pd.DataFrame(assetdf['Asset Name'].str.extract(r'(\d+)'))
    assetdf['SuiteNumber_Description'] = assetSuiteNumber_Description
    assetdf['SuiteNumber_Name'] = assetSuiteNumber_Name

    return assetdf



#The working Asset Dataframe now is "assetdf_suite_condensed"
#The working REQ Dataframe now is "reqdf_suite"

    
    return assetdf


#Create the site columns for Asset Data frame 
def createSiteCol(dataframe):    
    df = dataframe

    #1. Extracting the site out of the worktags and appending the listing as series in the asset df
    asset_site_list = pd.DataFrame(df['Worktags'].str.extract(r'(Site: [\d][\d][\d][\d][\d][\s])'))
    df['Site'] = asset_site_list
    #2. Formatting the site col to start with "ST"
    df['Site'] = df['Site'].str.replace(r'(Site:[\s])',"ST", regex=True)
    return df





reqdf_suite = produceSuiteReq(reqdf)
assetdf_suite = produceSuiteAsset(assetdf)

#the function that will be apply to every line in the reqdetail 
def assetMatch(lookupValue, site, masterIndex):
    if type(lookupValue) == str:
        unit_series = assetdf_suite['SuiteNumber_Name'].str.contains(lookupValue)
        indexList = iterIndex(unit_series)
        asset =  indexSiteMatch(indexList, site)
        req = reqdf_suite.loc[masterIndex,"Requisition #"]
        #print(f"{masterIndex} : [{asset}, {req}]")
        a = [masterIndex, req, asset]
        return  a

# The alternative        
def assetMatch_alternative(lookupValue, site, masterIndex):
    if type(lookupValue) == str:
        unit_series = assetdf_suite['SuiteNumber_Description'].str.contains(lookupValue)
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
        indexSite = assetdf_suite.loc[index,'Site']
        if indexSite == site:
            assetID = assetdf_suite.loc[index, "Asset ID"]
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

# Asset Opening Balance Names
# PPE




#Opening Balance Asst Match 
#index filter of master  and IFRS 
master_filterIndex = assetDf["Asset ID"].str.contains(r'([mM]aster)')
ifrs_filterIndex = assetDf["Asset ID"].str.contains(r'([Ii][fF][rR][Ss])')
OB_filterIndex =  assetDf["Asset ID"].str.contains(r'([Oo]pening [Bb]alance)')

#CHECK THIS OUT 
https://www.youtube.com/watch?v=uM4_SY4mXj4&list=PLiC1doDIe9rC_BfKW51I258aPIIt3onCP&index=23&ab_channel=DataDaft
https://www.youtube.com/watch?v=smPLY_5gVv4&ab_channel=DataDaft
#removing duplicated for the spend Cateogories from ASset DF 

obTable = {}

a = assetdf['Spend Category']
a = a.drop_duplicates()

def openBal_filter(sC):
    if sC.__contains__("FF&E"):
        obTable[sC] = "Amenity Spaces FF&E (Capital)"
    elif sC.__contains__("Electical"):
        obTable[sC] = "HVAC Systems (Capital)"
    elif sC.__contains__("Kitchen (Capital)") | sC.__contains__("Dining Room (Capital)"):
        obTable[sC] = "Amenity Spaces (Capital)"
    else:
        obTable[sC] = sC
    return obTable[sC]


#CHECK THIS OUT 
https://www.youtube.com/watch?v=uM4_SY4mXj4&list=PLiC1doDIe9rC_BfKW51I258aPIIt3onCP&index=23&ab_channel=DataDaft
https://www.youtube.com/watch?v=smPLY_5gVv4&ab_channel=DataDaft

a.apply(openBal_filter)