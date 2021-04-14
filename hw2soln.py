# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 17:21:33 2021

@author: parke
"""

import io
import pandas as pd
import requests as r


url1 = 'http://drd.ba.ttu.edu/isqs3358/hw2/hr_data.csv'
url2 = 'http://drd.ba.ttu.edu/isqs3358/hw2/sales_data.csv'
filepath = 'Users/parke/OneDrive/Desktop/hw7/output_files'
file_out_1 = 'existing_title_aggregate.csv'
file_out_2 = 'updated_title_aggregate.csv'
file_out_3 = 'employee_raise.csv'

#pull hr
res = r.get(url1)
res.status_code
df_hr = pd.read_csv(io.StringIO(res.text), delimiter='|') 

#pull sales
res = r.get(url2)
res.status_code
df_sales = pd.read_csv(io.StringIO(res.text), delimiter='|')

#view dfs
df_hr.head()
df_sales.head()

#merge dfs
df_merge = df_hr.merge(df_sales, how='inner', left_on='EmpId', right_on='EmpId')
df_merge.head()

#get the averages
salary_avg = df_merge['Salary'].mean()
benefits_avg = df_merge['Benefits'].mean()
items_sold_avg = df_merge['ItemsSold'].mean()
sales_value_avg = df_merge['SalesValue'].mean()

#replace missing values with averages
df_merge['Salary'].fillna(salary_avg, inplace=True)
df_merge['Benefits'].fillna(benefits_avg, inplace=True)
df_merge['ItemsSold'].fillna(items_sold_avg, inplace=True)
df_merge['SalesValue'].fillna(sales_value_avg, inplace=True)

print('I felt it was best to replace these values with the averages for their respected column, because this fills the most accurate estimated values')

#replace titles
df_merge['Title'] = df_merge['Title'].replace(['Sales Associate 1'], 'Technician')
df_merge['Title'] = df_merge['Title'].replace(['Sales Associate 2'], 'Pinky')
df_merge['Title'] = df_merge['Title'].replace(['Sales Associate 3'], 'Brain')
df_merge['Title'] = df_merge['Title'].replace(['Sales Manager'], 'Yacko')

Metric3748 = df_merge['ItemsSold']/df_merge['SalesValue']

#add apples column
df_merge['Apples'] = 0

#set values to apples column based on title
df_merge['Apples'][df_merge['Title'] == 'Technician'] = 5
df_merge['Apples'][df_merge['Title'] == 'Pinky'] = 300
df_merge['Apples'][df_merge['Title'] == 'Brain'] = 17
df_merge['Apples'][df_merge['Title'] == 'Yacko'] = 51

Total_Compensation = df_merge['Salary']+ df_merge['Apples']

df_merge['employee_more_apples'] = 'No'
df_merge['employee_more_apples'][(df_merge['Title'] == 'Yacko') |
                                  (df_merge['Title'] == 'Brain') |
                                  (df_merge['Apples'] < 9)] = 'Yes'

# df_merge['tot_comp_avg'] = Total_Compensation.mean()
# df_merge['metric3748_avg'] = Metric3748.mean()

#average for total compensation and mertic by total ----------------------------------------------------------------
df_existing = df_merge[['Title', 'Total_Compensation', 'Metric3748']].groupby('Title').mean()

df_merge[['Title']].to_csv(filepath + file_out_1, sep ='|', index=True)
df_existing[['Total_Compensation', 'Metric3748']].to_csv(filepath + file_out_1, sep='|', index=True)

#compensation increase ----------------------------------------------------------------------------------------------
df_merge['Apples'][df_merge['employee_more_apples'] == 'Yes'] = (df_merge['Apples']*2.1)
df_merge['Apples'][df_merge['employee_more_apples'] == 'No'] = (df_merge['Apples']*0.7)
df_merge['Total_Compensation'] = df_merge['Salary'] + df_merge['Apples']

#total compensation -------------------------------------------------------------------------------------------------
df_updated = df_merge[['Title', 'Total_Compensation', 'Metric3748']].groupby('Title').mean()

df_merge[['Title']].to_csv(filepath + file_out_2, sep='|', index=True)
df_existing[['Total_Compensation', 'Metric3748']].to_csv(filepath + file_out_2, sep='|', index=True)

#employees that ger more apples -------------------------------------------------------------------------------------
df_merge[['EmpId', 'Title', 'Salary', 'Apples', 'Total_Compensation']].to_csv(filepath + file_out_3, sep='|', index=True)
