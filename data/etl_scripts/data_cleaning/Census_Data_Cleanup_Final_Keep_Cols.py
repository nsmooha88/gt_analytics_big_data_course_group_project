# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 09:34:13 2020

@author: Amelia.Bell
"""

# =============================================================================
# After doing initial data exploration and reviewing of column names, this brings
# in the final data source with which we will work
#
# Data is brought in and then geography columns and columns not requiring further 
# adjustments are used to build initial dataframe of cleaned data. The remaining
# columns are then converted into percentages via calculations and added to the
# dataframe. Any calculation errors are then cleaned and inital data is written
# to a pickle file to be added to full amenities data later for visualization.
# Column names are then converted from "code" names to short names that provide
# enough information, but are abbreviated. Rows with high number of null values
# are then removed.
# Outlier treatment and subsequent truncation is then applied, and any nulls are
# replaced with the mean. The columns are then evaluated for skewness and Box-Cox
# is applied as necessary. The data is then standardized.
# A final profile report is created, and data is written to a pickle file. This
# final data will later be combined with amenities data and used for clustering.
# 
# Data Sources: Census data was gathered and pickled by another team member
# Column names were reviewed manually in excel and short names were developed
# =============================================================================

import pyodbc
import pandas.io.sql as pdq
import pandas as pd
import numpy as np
import pandas_profiling as pp
from pandas_profiling import ProfileReport
import pickle as pkl
from colorama import Fore,Style
import os
from scipy import stats
from sklearn.preprocessing import StandardScaler

#Check working directory, if needed, change working directory
if os.getcwd() == 'D:\\CSE 6242':
    print (Fore.GREEN + 'Working Directory is already set correctly!' + Style.RESET_ALL)
else:
    os.chdir('D:\\CSE 6242')
    print (Fore.GREEN + 'Working Directory is now set correctly!' + Style.RESET_ALL)

#Read in initial census data pickle files and make list of columns for raw census data
d1 = pd.read_pickle('2018_5yr_cendatagov_ESTIMATES_v4.pkl')
d2 = pd.read_pickle('2018_5yr_cendatagov_ESTIMATES_DD_v4.pkl')
d3 = pd.read_pickle('2018_5yr_cendatagov_GAZ_v4.pkl')

col_list = d1.columns.tolist()

#Cleaned dataframe build from initial columns that are geography indicators, summary indicators, or already percentages
d1_cleaned = d1[['GEOID','GEO_ID','NAME','S0101_C01_036E','S0101_C01_035E','S0101_C01_032E', 'S1501_C01_059E', 'S1701_C03_001E', 'S2301_C02_021E','S2301_C04_021E', 'S1101_C01_004E', 'S1101_C01_016E', 'S1101_C01_017E','S1101_C01_019E']]

#This is race and housing units per population - transforming into percentages
d1_cleaned['DP05_0037E'] = d1['DP05_0037E']/d1['DP05_0033E']
d1_cleaned['DP05_0038E'] = d1['DP05_0038E']/d1['DP05_0033E']
# d1_cleaned['DP05_0039E'] = d1['DP05_0039E']/d1['DP05_0033E']
d1_cleaned['DP05_0044E'] = d1['DP05_0044E']/d1['DP05_0033E']
d1_cleaned['DP05_0052E'] = d1['DP05_0052E']/d1['DP05_0033E']
d1_cleaned['DP05_0057E'] = d1['DP05_0057E']/d1['DP05_0033E']
d1_cleaned['DP05_0071E'] = d1['DP05_0071E']/d1['DP05_0070E']
d1_cleaned['DP05_0086E'] = d1['DP05_0086E']/d1['DP05_0001E']

#Education Levels Pop 25+ - transform into percentages
d1_cleaned['S1501_C01_009E'] = d1['S1501_C01_009E']/d1['S1501_C01_006E']
d1_cleaned['S1501_C01_015E'] = d1['S1501_C01_015E']/d1['S1501_C01_006E']

#Civilian Employment Pop 16+ - transform into percentages
d1_cleaned['S2405_C02_001E'] = d1['S2405_C02_001E']/d1['S2405_C01_001E']
d1_cleaned['S2405_C03_001E'] = d1['S2405_C03_001E']/d1['S2405_C01_001E']
d1_cleaned['S2405_C04_001E'] = d1['S2405_C04_001E']/d1['S2405_C01_001E']
d1_cleaned['S2405_C05_001E'] = d1['S2405_C05_001E']/d1['S2405_C01_001E']
d1_cleaned['S2405_C06_001E'] = d1['S2405_C06_001E']/d1['S2405_C01_001E']

#Create new list of columns in initial cleaned dataframe
cleaned_col_list = d1_cleaned.columns.tolist()

#Replace any calculation errors (that divided by 0) with 0
d1_cleaned.replace([np.inf, -np.inf], 0, inplace=True)

#Write initial cleaned data into pickle file to be used later for visualization
d1_cleaned.to_pickle('Cleaned_Data.pkl')

#Pulling in file that maps final coded column names to a short name with enough details
clean_short = pd.read_excel("Cleaned_Col_Dict.xlsx")
clean_short.set_index('code',inplace=True)
clean_short_dict = clean_short.to_dict("dict")
clean_short_dict = clean_short_dict.get("Short Names")

d1_cleaned_new = d1_cleaned.rename(columns=clean_short_dict)

#Add a column that counts the number of nulls for each row - after reviewing with team, found 646 rows had more than 100 
#null values and rows were determined to negligble w.r.t value add, so chose to remove
d1_cleaned_new['Null_Cnt'] = d1_cleaned_new.isnull().sum(axis=1)
# d1_cleaned_new.hist(column='Null_Cnt')
d1_cleaned_new_v1 = d1_cleaned_new[d1_cleaned_new['Null_Cnt'] < 100]

#Beginning of Null Replacement and outlier treatment
#Create list of final columns to be used for looping - without 3 columns that map to geography
cleaned_col_list_fin = d1_cleaned_new_v1.columns.tolist()
cleaned_col_list_fin = cleaned_col_list_fin[3:]

#Truncate to 3 standard deviations
for i in cleaned_col_list_fin:
    mean = d1_cleaned_new_v1[i].mean()
    std_dev = d1_cleaned_new_v1[i].std()
    d1_cleaned_new_v1.loc[d1_cleaned_new_v1[i] < (mean - (3*std_dev)), i] = (mean - (3*std_dev))
    d1_cleaned_new_v1.loc[d1_cleaned_new_v1[i] > (mean + (3*std_dev)), i] = (mean + (3*std_dev))

#Replace Null values with mean    
for i in cleaned_col_list_fin:    
    d1_cleaned_new_v1[i] = d1_cleaned_new_v1[i].fillna(value = d1_cleaned_new_v1[i].mean())

#Beginning of data transformation and standardization
#Create a list to store columns where data is skewed
skew_col_list = list()

#Calculate skewness of data in each column and add to list if skewed
for i in cleaned_col_list_fin:
    skewness = d1_cleaned_new_v1[i].skew()
    if skewness > 1.2 or skewness < -1:
        skew_col_list.append(i)

# Remove Null Count column from list
skew_col_list = skew_col_list[:-1]

#Replace 0 with min non-zero
for j in skew_col_list:
    val_list = d1_cleaned_new_v1[j].unique()
    d1_cleaned_new_v1[j] = np.where(d1_cleaned_new_v1[j] == 0, val_list[1], d1_cleaned_new_v1[j])

#Perform Box-Cox on skewed columns
for j in skew_col_list:
    # print(j)
    d1_cleaned_new_v1[j] = stats.boxcox(d1_cleaned_new_v1[j])[0]

#Standardize Data
scaler = StandardScaler()
d1_cleanded_new_v2 = d1_cleaned_new_v1.copy()

df =  scaler.fit_transform(d1_cleanded_new_v2[cleaned_col_list_fin])
scaled_df = pd.DataFrame(df, columns=cleaned_col_list_fin)
d1_cleanded_new_v2 = pd.concat([d1_cleaned_new_v1[['GEOID', 'GEO_ID', 'NAME']], scaled_df], axis=1)

#Create profile of final dataset to do final review
d1_profile = d1_cleaned_new_v2.profile_report(minimal=True)
d1_profile.to_file(output_file = "Census_Data_Profile_v4_Prelim_Cleaned_v4.html")

#Write data to pickle file - will be used to add to amenities data and clustering
#d1_cleaned_new.to_pickle("Cleaned_Census_wHigh_Nulls.pkl")
d1_cleanded_new_v2.to_pickle("Cleaned_Census_wo_HighNulls_fin.pkl")

