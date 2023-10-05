# Assumptions:
# Time in column "C" is "Time In"

import pandas as pd
from datetime import datetime, timedelta

# Define the input file path
file = 'Assignment_Timecard.xlsx - Sheet1.csv'

# Load the data from the CSV file into a DataFrame
df = pd.read_csv(file)

#  Rename "Time" column to "Time In", for better understanding 
df.rename(columns={'Time': 'Time In'}, inplace=True)

# Convert time columns to datetime objects
df['Time In'] = pd.to_datetime(df['Time In'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Sort the DataFrame by "Employee Name" and "Time In" in asending order
df.sort_values(by=['Employee Name', 'Time In'], inplace=True)

# Define the criteria for analysis
consecutive_days = 7
min_time_between_shifts = timedelta(hours=1)
max_time_between_shifts = timedelta(hours=10)
max_shift_duration = timedelta(hours=14)

# Initialize variables to track employee shifts
current_employee = None
current_shift_start = None
previous_shift_end = None

# Initialize sets to store unique answers
qa = set()
qb = set()
qc = set()

for index, row in df.iterrows():
  if (row['Time Out'] - row['Time In']) > max_shift_duration:
    qc.add((current_employee,row['Position ID']))

  if current_employee is None or current_employee != row['Employee Name']:
        current_employee = row['Employee Name']
        previous_shift_end = row['Time Out']
        consecutive_count = 1
  else:
        if row['Time In'] - previous_shift_end > min_time_between_shifts and row['Time In'] - previous_shift_end < max_time_between_shifts:
            qb.add((current_employee,row['Position ID']))

        # handling null values
        if(pd.notna(row['Time In']) and pd.notna(previous_shift_end)):
            if (row['Time In'].date() - previous_shift_end.date()) > timedelta(days=1):
                consecutive_count = 1
            elif (row['Time In'].date() - previous_shift_end.date()) == timedelta(days=1):
                consecutive_count += 1
            if (pd.notna(row['Time Out']) and (row['Time Out'].date() - row['Time In'].date()) == timedelta(days=1)):
                consecutive_count +=1
        if(consecutive_count == 7):
            qa.add((current_employee,row['Position ID']))

        previous_shift_end = row['Time Out']

print('Emp who has worked for 7 consecutive days :')
j = 0
for i in qa:
  j+=1
  print(j,' : ',i)
print()

print('Emp  who have less than 10 hours of time between shifts but greater than 1 hour :')
j = 0
for i in qb:
  j+=1
  print(j,' : ',i)
print()

print('Emp who has worked for more than 14 hours in a single shift :')
j = 0
for i in qc:
  j+=1
  print(j,' : ',i) 