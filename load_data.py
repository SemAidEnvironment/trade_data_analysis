import pandas as pd
import os
import json

#load data:
# Get the HS codes for the selected group
with open('product_names.json') as file:
    commodity_groups = json.load(file)
groups = list(commodity_groups.keys())
### load 2024 trade data;
# Path to the directory containing the Excel files
directory_path_volumes = "data/volumes"
directory_path_values = "data/values"

# Read all files in the directory
def gather_data(directory_path):
    all_files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
    #initialize countries and data lists
    all_hs_data = {}
    EU_COUNTRIES = []
    # Directory for Pickle files
    commodity_groups={}
    list_hs_codes=[]
    # Extract data from each file and determine EU countries
    for file in all_files:
        file_path = os.path.join(directory_path, file)
        xls = pd.ExcelFile(file_path)
        #get commodity group name for name of excel file
        commodity = file.split(" ")[2]
        for sheet_name in xls.sheet_names:
            if sheet_name != "Info":
                df = pd.read_excel(xls, sheet_name=sheet_name,index_col=0,header=9)
                df = df[~df.index.duplicated(keep='first')]
                hs_code = sheet_name
                #df.to_pickle(f"data/cache/{hs_code}.pkl")
                all_hs_data[hs_code] = df
                #add hs code to the correct commodity group
                list_hs_codes.append(hs_code)
        commodity_groups[commodity]=list_hs_codes
        list_hs_codes=[]

    return all_hs_data,commodity_groups

all_hs_data_volumes,commodity_groups = gather_data(directory_path_volumes)
all_hs_data_values,commodity_groups = gather_data(directory_path_values)


##### create list with total non-eu imports per hs code and per commodity group
EU = "European Union - 27 countries (AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK)"
eu_countries = all_hs_data_values[next(iter(all_hs_data_values))].columns
extra_eu="Extra-EU"



def gather_data_transposed(directory_path):
    ### transposed df's############### (for exporting info)
    all_hs_data_transposed = {}
    # Extract data from each file and determine EU countries
    all_files = [f for f in os.listdir(directory_path) if f.endswith('.xlsx')]
    for file in all_files:
        file_path = os.path.join(directory_path, file)
        xls = pd.ExcelFile(file_path)
        # get commodity group name for name of excel file
        for sheet_name in xls.sheet_names:
            if sheet_name != "Info":
                df = pd.read_excel(xls, sheet_name=sheet_name, index_col=0, header=9)
                df = df[~df.index.duplicated(keep='first')]
                df =df.T
                hs_code = sheet_name
                #df.to_pickle(f"data/cache/{hs_code}.pkl")
                all_hs_data_transposed[hs_code] = df

    return all_hs_data_transposed

all_hs_data_transposed_volumes = gather_data_transposed(directory_path_volumes)
all_hs_data_transposed_values = gather_data_transposed(directory_path_values)