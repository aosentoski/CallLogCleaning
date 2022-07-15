#!/usr/bin/env python
# coding: utf-8

# # Automatic Call Log Cleaning

# In[68]:


# Importing numpy and pandas
import numpy as np
import pandas as pd


# In[ ]:


# Getting Call File
CSV = input("What File Would You Like to Read In?\n")


# In[ ]:


# Reading in Call Data and creating data frame
df = pd.read_csv(CSV)


# In[ ]:


# removing all outbound calls
df = df.drop(df[df['Initial Direction'] == 'outbound'].index).reset_index(drop=True)


# In[ ]:


# Fixes answered/missed call data
df['Missed'].mask(df['Answered'] == 1, 0, inplace=True)


# In[ ]:


# Adds calls during shift times
def addTimes(df, date, StartTime, EndTime):
    
    Start = str(date) + ' ' + str(StartTime)
    End = str(date) + ' ' + str(EndTime)
    NewDay = str(date) + str(' 00:00:01')
    
    df['Time'] = df['Date/Time (earliest)'].apply(pd.to_datetime)
    
    df1 = pd.DataFrame()
    df1 = df.loc[df['Time'].between(Start,End)]
    
    return df1


# In[ ]:


# Getting Shift Data
CSV2 = input("What Shifts Would You Like to Cross Reference?\n")


# In[ ]:


# Reading in shifts and creating data frame
Shifts_df = pd.read_csv(CSV2)
Shifts_df['Date'] = Shifts_df['Date'].apply(pd.to_datetime)


# In[ ]:


# Combining all calls for shifts worked
calls_df = pd.DataFrame()
for i,row in Shifts_df.iterrows():
    df2 = addTimes(df, row['Date'], row['Start'], row['End'])
    if len(df2.columns) != 0:
        calls_df = pd.concat([calls_df, df2])
calls_df = calls_df.reset_index(drop=True)


# In[ ]:


# Printing and downloading cleaned data
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    calls_df.to_csv('cleaned call data.csv')


# In[ ]:


# Outputting Stats
AllTotAnswered = sum(df['Answered'])
AllTotMissed = sum(df['Missed'])
TotAnswered = sum(calls_df['Answered'])
TotMissed = sum(calls_df['Missed'])
if AllTotAnswered == 0:
    AllMissPercent = 0
else:
    AllMissPercent = round(AllTotMissed/AllTotAnswered,2) * 100
if TotAnswered == 0:
    MissPercent = 0
else:
    MissPercent = round(TotMissed/TotAnswered,2) * 100


print('Total Calls Answered')
print(AllTotAnswered)
print('Total Calls Missed')
print(AllTotMissed)
print('All Time Missed Call Percentage')
print(AllMissPercent, '%')

print('\n')

print('Total calls Answered on Shift: ') 
print(TotAnswered)
print('Total calls Answered on Shift: ') 
print(TotMissed)
print('HQ Missed Call Percentage: ') 
print(MissPercent,'%')

