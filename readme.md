# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 23:46:18 2020

@author: Mahin
"""

### Summary

This project analyzes covid cases and deaths in the US, specifically NY state.

### Input Data

All of the data is obtained online and has not been manually manipulated. 
Each step of the cleaning process is in the script.


                                ###input files
    #datasets
ny times ny state covid data ('covid_cases_states.csv')
cdc nyc covid data ('nyc_covid_cases_deaths.csv')
ny state covid testing data('NYState_COVID_Testing.csv')
ny times county level covid data ('us-counties.csv')
ny state fips code ('New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv')
ny state and county population data ('Annual_Population_Estimates_for_New_York_State_and_Counties__Beginning_1970.csv')
nyc leading cause death data('NYC_leading_cause_death.csv')
    #shapefiles
censes shape files US states ('cb_2018_us_state_500k.zip')

                                ###output files
heat_map_states heatmap (heat_map_states.qgz)

                                ###qgis project
The py script takes ny times ny state covid dataset, creates a max death variable for each state
and saves is as heat_map csv file.

The qgis project uses censes shape files for US states and joins the csv created created earlier
to generate a heatmap of max deaths by covid till mid April '20'


                                ### py file
                                
##heatmap                                
The py script takes ny times ny state covid dataset, creates a max death variable for each state
and saves is as heat_map csv file. This file is then used in qgis to create a heat map when joined
on statename with census tracts shape file.

##covid deaths and cases in NYC
This part uses nyc covid cases, keep only april deaths and cases and maps cases as bars and deaths as
a line graph.

##covid cases in ny state by county
Here county level data for covid is used, only NY state is kept for analyses. The purpose of this analyses 
was to correlate population density with cases and deaths. The ny times
data for state and county is missing some major counties and fips code. The top 3 counties for largest population in NY
state are missing from the data. To resolve this problem, I merged county level data
with fips code data on fips code. Now that I have fips code for all counties,
I merged county level data with population data to get population numbers for each
county affected by covid. After keeping the only ones that merge, I keep the top 5 with the largest 
population numbers. For analyses purposes, I created variable for percent cases for each county
The graph looks at specifically 3 dates of April(5 days apart)

##leading causes of death and covid in NYC
Here the purpose of analysis was to counter people's argument of understating covid because "people 
die from other diseases too" I analyse the leading cause of death for the past years in NYC and comparing this 
year's covid numbers. Using the data for deaths in NYC, I keep the ones with maximun deaths by year and leading 
cause of death. For all years, the leading cause has been heart disease but the numbers fluctuate. The graph shows how the numbers
for covid outnumber heart disease for all years. The numbers for covid are just through March to April.
 
