
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 10:46:55 2020

@author: Mahin
"""
#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#uploading data
covid_states = pd.read_csv('covid_cases_states.csv')
covid_nyc = pd.read_csv('nyc_covid_cases_deaths.csv')
covid_NY= pd.read_csv('NYState_COVID_Testing.csv')
covid_counties= pd.read_csv('us-counties.csv')
fips= pd.read_csv('New_York_State_ZIP_Codes-County_FIPS_Cross-Reference.csv')
pop_counties = pd.read_csv('Annual_Population_Estimates_for_New_York_State_and_Counties__Beginning_1970.csv')
nyc_death= pd.read_csv('NYC_leading_cause_death.csv')



#standardising variable names
covid_states.columns = map(str.lower, covid_states.columns)
covid_states.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

covid_nyc.columns = map(str.lower, covid_nyc.columns)
covid_nyc.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

covid_counties.columns = map(str.lower, covid_counties.columns)
covid_counties.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

fips.columns = map(str.lower, fips.columns)
fips.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

pop_counties.columns = map(str.lower, pop_counties.columns)
pop_counties.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)

nyc_death.columns = map(str.lower, nyc_death.columns)
nyc_death.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)


#heat map of deaths by state

covid_states['death_max'] = covid_states.groupby(['fips'])['deaths'].transform(max)
covid_states = covid_states.drop_duplicates(subset='fips', keep="first")
heat_map_states = covid_states[['state','fips','death_max']]
heat_map_states= heat_map_states.rename(columns={"state": "NAME"})
#fipscode
#heat_map_states= heat_map_states.rename(columns={"fips": "STATEFP"})
# heat_map_states['STATEFP']= heat_map_states['STATEFP'].astype(str)
# heat_map_states['STATEFP'] = heat_map_states['STATEFP'].apply('="{}'.format)
heat_map_states.to_csv('heat_map_states.csv')

#covid deaths and cases in nyc


covid_nyc = pd.read_csv(r'C:\Users\Mahin\Documents\GitHub\APA_project\nyc_covid_cases_deaths.csv')
covid_nyc= covid_nyc.rename(columns={"DATE_OF_INTEREST": "date"})
covid_nyc= covid_nyc.rename(columns={"NEW_COVID_CASE_COUNT": "new_case"})
covid_nyc= covid_nyc.rename(columns={"HOSPITALIZED_CASE_COUNT": "hosp_case"})
covid_nyc= covid_nyc.rename(columns={"DEATH_COUNT": "death"})
covid_nyc.death.fillna('0', inplace=True)
covid_nyc.hosp_case.fillna('0', inplace=True)
covid_nyc['hosp_case']= covid_nyc['hosp_case'].astype(int)
covid_nyc['death']= covid_nyc['death'].astype(int)
covid_nyc['date'] = pd.to_datetime(covid_nyc['date'])
start_date = '2020-04-01'
april = (covid_nyc['date'] > start_date)
covid_nyc = covid_nyc.loc[april]
covid_nyc.sort_values(by=['date'])
covid_nyc=covid_nyc.drop(covid_nyc['date'].idxmax())
#covid_nyc.set_index('date')['death'].plot();

covid_nyc['date_str']= covid_nyc['date'].astype(str)

covid_nyc[['year','month', 'date_']] = covid_nyc.date_str.str.split("-",expand=True,)


fig, ax = plt.subplots()
ax2 = ax.twinx()
ax.bar(covid_nyc.date_, covid_nyc["hosp_case"], color=(190/255,190/255,190/255,0.7), label='hospital cases')
ax2.plot(covid_nyc.date_, covid_nyc["death"], color='maroon', label='death')
ax.set_xticklabels(covid_nyc.date_)
ax.legend(loc='best')
ax.set_xlabel("April 2020")
ax2.tick_params(axis='y', colors='maroon')
plt.savefig('covid_deaths_hospcases_nyc.png')

#covid cases ny state by county

covid_counties.loc[covid_counties['state']=='New York', 'ny'] = 1
droprows = covid_counties[covid_counties['ny'] != 1].index
covid_counties.drop(droprows, inplace=True)
covid_counties= covid_counties[['date','county', 'cases', 'deaths', 'fips']]
covid_counties= covid_counties.rename(columns={"fips": "county_fips"})

fips = fips.drop_duplicates(subset='county_fips', keep="first")
fips= fips[['county_name','county_fips']]

covid_counties = pd.merge(fips, #Our left-side dataframe; listing this dataset first defines it as the left-side dataframe
                covid_counties, #Our right-side dataframe; listing this dataset second defines it as the right-side datafrome 
                on = 'county_fips', #The column name for our right-side key; merge always mergers only two data sets. if more than that need to be merged they are done so in a cascade
                how = 'outer', #The type of merge we want to perform
                validate = "1:m", #A check to make sure that we have unique keys in our right-side dataframe (parcels)
                indicator = True #Creates a new _merge column that we can use to check our results
               )
drop= covid_counties[covid_counties['_merge'] != 'both'].index
covid_counties.drop(drop, inplace=True)
covid_counties= covid_counties[['date','county', 'cases', 'deaths', 'county_fips']]

pop_counties.loc[pop_counties['year']== 2019, 'keeprows'] = 1
droprows= pop_counties[pop_counties['keeprows'] != 1].index
pop_counties.drop(droprows, inplace=True)

pop_counties.loc[pop_counties['geography'].str.contains('New York State'), 'drop'] = 1
droprows_= pop_counties[pop_counties['drop'] == 1].index
pop_counties.drop(droprows_, inplace=True)

pop_counties= pop_counties.rename(columns={"fips_code": "county_fips"})

df_merged = pd.merge(pop_counties, #Our left-side dataframe; listing this dataset first defines it as the left-side dataframe
                covid_counties, #Our right-side dataframe; listing this dataset second defines it as the right-side datafrome 
                on = 'county_fips', #The column name for our right-side key; merge always mergers only two data sets. if more than that need to be merged they are done so in a cascade
                how = 'outer', #The type of merge we want to perform
                validate = "1:m", #A check to make sure that we have unique keys in our right-side dataframe (parcels)
                indicator = True #Creates a new _merge column that we can use to check our results
               )

drop= df_merged[df_merged['_merge'] != 'both'].index
df_merged.drop(drop, inplace=True)
df_merged['county'].value_counts()

df= df_merged.drop_duplicates(subset='county', keep="first")
df= df.sort_values(by=['population'], ascending=False)
df = df[:5]
df=df[['county_fips']]

df_merged=df_merged[['county_fips','geography', 'year','program_type','population', 'date', 'cases', 'deaths']]

df_final = pd.merge(df, #Our left-side dataframe; listing this dataset first defines it as the left-side dataframe
               df_merged, #Our right-side dataframe; listing this dataset second defines it as the right-side datafrome 
                on = 'county_fips', #The column name for our right-side key; merge always mergers only two data sets. if more than that need to be merged they are done so in a cascade
                how = 'outer', #The type of merge we want to perform
                validate = "1:m", #A check to make sure that we have unique keys in our right-side dataframe (parcels)
                indicator = True #Creates a new _merge column that we can use to check our results
               )

drop= df_final[df_final['_merge'] != 'both'].index
df_final.drop(drop, inplace=True)
df_final['case_percent'] = (df_final['cases']/df_final['population'] *100)

start_date_ = '2020-04-01'
april = (df_final['date'] > start_date_)
df_merged = df_final.loc[april]


df_final['date'].astype(str)
df_final.loc[df_final['date']== '2020-04-02', 'keep'] = 1
df_final.loc[df_final['date']== '2020-04-07', 'keep'] = 1
df_final.loc[df_final['date']== '2020-04-13', 'keep'] = 1

drop= df_final[df_final['keep'] != 1].index
df_final.drop(drop, inplace=True)

df_final_plot = df_final.pivot(index='date', columns='geography', values='case_percent')
df_final_plot.plot()



nyc_death.columns = map(str.lower, nyc_death.columns)
nyc_death.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
nyc_death.shape

covid_nyc.columns = map(str.lower, covid_nyc.columns)
covid_nyc.rename(columns=lambda x: x.replace(' ', '_'), inplace=True)
covid_nyc.shape


nyc_death = nyc_death.dropna(subset=['deaths'])
nyc_death.loc[nyc_death['leading_cause'].str.contains('All Other Causes'), 'drop'] = 1
nyc_death.loc[nyc_death['deaths']== '.', 'drop'] = 1
droprows_= nyc_death[nyc_death['drop'] == 1].index
nyc_death.drop(droprows_, inplace=True)

nyc_death['leading_cause'].value_counts()
nyc_death=nyc_death[['year','leading_cause', 'deaths']]
nyc_death['deaths']= nyc_death['deaths'].astype(int)
nyc_death= nyc_death.sort_values(by=['year', 'deaths'], ascending=False)

maxima = nyc_death.groupby('year')['deaths'].max()
nyc_death['max'] = nyc_death['year'].map(maxima)

nyc_death= nyc_death.drop_duplicates(subset='year', keep="first")
nyc_death=nyc_death[['year','leading_cause', 'deaths']]

nyc_death['time_frame'] ='Jan-Dec'
nyc_death.loc[nyc_death['leading_cause']== 'Diseases of Heart (I00-I09, I11, I13, I20-I51)', 'leading_cause']='Diseases of Heart'

covid_nyc['covid_deaths'] = covid_nyc['death_count'].sum() 
covid_nyc= covid_nyc.drop_duplicates(subset='covid_deaths', keep="last")

covid_nyc['year']= 2020
covid_nyc['leading_cause'] = "COVID"
covid_nyc= covid_nyc.rename(columns={"covid_deaths": "deaths"})

covid_nyc['deaths']= covid_nyc['deaths'].astype(int)
covid_nyc['time_frame'] ='Mar-Apr'
covid_nyc=covid_nyc[['year','time_frame','leading_cause', 'deaths']]
covid_nyc
covid_nyc['year']= covid_nyc['year'].astype(int)

nyc_deaths = nyc_death.append(covid_nyc, ignore_index = True)

nyc_deaths= nyc_deaths.sort_values(by=['year'], ascending=False)
nyc_deaths[['year','time_frame','leading_cause', 'deaths']]


plt.figure()
sns.regplot('leading_cause','deaths',data=nyc_deaths,ci=95)
plt.savefig('regplot.png')

fg = sns.catplot(y='year',x='deaths',data=nyc_deaths,kind='bar',orient='h')