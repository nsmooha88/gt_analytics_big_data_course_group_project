# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 19:57:39 2020

@author: Amelia.Bell
"""
# =============================================================================
# This code is run after the Census data is cleaned, transformed, and standardized.
# The final Census and amenities data are first pulled in and the amenities data
# is profiled for initial observations. Upon seeing all data columns are skewed,
# the data is then prepared and transformed via Box-Cox. It is then standardized
# and re-profiled. Upon reviewing second profile, final columns to keep are 
# determined for clustering. The data is then combined with Census data to be used
# in the clustering exercise. 
# The cleaned Census data, prior to being transformed and standardized is then
# brought in and joined with the initial amenities data. This dataset will be used
# as part of the visualization.
#
# Data Sources: Census data was developed via Census_Data_Cleanup_Final_Keep_Cols.py
# Amenities data was provided via pickle file developed by other team members
# =============================================================================

# import pyodbc
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

#Final Census data and initial amenities data    
d1_cleaned_new_v2 = pd.read_pickle("Cleaned_Census_wo_HighNulls_fin.pkl")
df_amenitie = pd.read_pickle("amenities_features.pkl")
df_amenities = df_amenitie.copy()

#Create initial data profile of amenities data to review 
amenities_profile = df_amenities.profile_report(minimal=True)
amenities_profile.to_file(output_file = "Amenities_Features_Profile.html")

amenities_col_list = df_amenities.columns.to_list()
amenities_col_list = amenities_col_list[3:]

#Replace 0 with next lowest value - preparation for applying Box-Cox
for i in amenities_col_list:
    val_list = df_amenities[i].unique()
    df_amenities[i] = np.where(df_amenities[i] == 0, val_list[1], df_amenities[i])
    # df_amenities[i] = df_amenities[i] + 1
    
#Perform Box-Cox on skewed columns
for j in amenities_col_list:
    # print(j)
    df_amenities[j] = stats.boxcox(df_amenities[j])[0]
    
#Standardize Data - exclude "GEOID" then add back to standardized data
scaler = StandardScaler()
df_amenities_v1 = df_amenities.copy()

df = scaler.fit_transform(df_amenities_v1[amenities_col_list])
scaled_df = pd.DataFrame(df, columns=amenities_col_list)

df_amenities_v1 = pd.concat([df_amenities_v1[['GEOID']], scaled_df], axis=1)

#Data Profile after completing transformation and standardization
amenities_profile = df_amenities.profile_report(minimal=True)
amenities_profile.to_file(output_file = "Amenities_Features_Profile_v1.html")


#Reduce amenities data to only include columns needed for clustering - determined through reviewing profile
df_amenities_final = df_amenities_v1[['GEOID','WT_N_GROCERY_DIST_25','WT_N_GYMS_DIST_25','WT_N_HARDWARE_DIST_25',
                                      'WT_N_PARKS_DIST_25','WT_N_MEDICAL_DIST_25']]

#Merge Amenities and Census Data to be used for Clustering
df_final = pd.merge(d1_cleaned_new_v2,df_amenities_final ,on = 'GEOID', how="left" )
df_final.drop(columns=['Null_Cnt'], inplace=True)

#Pickle File for Clustering
df_final.to_pickle("Final_Clustering_Input_Data.pkl")

#Bring in Cleaned Census data - prior to transformation and standardization
df_clean_census = pd.read_pickle('Cleaned_Data.pkl')

#Convert column names from codes to abbreviated descriptions
clean_short = pd.read_excel("Cleaned_Col_Dict.xlsx")
clean_short.set_index('code',inplace=True)
clean_short_dict = clean_short.to_dict("dict")
clean_short_dict = clean_short_dict.get("Short Names")

df_cleaned_census = df_clean_census.rename(columns=clean_short_dict)

#Merge original amenities data and Cleaned Census data to create final dataset to be used as part of visualization
df_cleaned_final = pd.merge(df_cleaned_census,df_amenitie ,on = 'GEOID', how="left" )

#Pickle File for Visualization
df_cleaned_final.to_pickle("Final_Visualization_Input_Data.pkl")
