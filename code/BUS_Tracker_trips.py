# -*- coding: utf-8 -*-
'''
@Time    : 2023/6/12 21:57
@Author  : Ericyi
@File    : BUS_Tracker_trips.py

'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def count_unique_trips(df, target_hour, route):
    # Just keep the first trip_id
    df = df.drop_duplicates('origtatripno', keep='first')
    #
    df.to_csv(r'E:\MIT Summer Intern\data\CTA Bus\0531deduplicated.csv')
    #
    # df3 = df[df['rt'] == '85']
    # df3.to_csv(r'E:\MIT Summer Intern\data\CTA Bus\0531deduplicated85.csv')

    # 筛选特定日期和小时的数据
    filtered_df = df[(df['data_hour'] == target_hour) & (df['rt'] == route)]

    # 统计唯一行程数量
    unique_trip_count = len(filtered_df['origtatripno'].unique())

    return unique_trip_count

csv_file = r"E:\MIT Summer Intern\data\CTA Bus\2023-05-31.csv"
df = pd.read_csv(csv_file)

date = '2023-05-31'

df = df[df['data_date'] == date]

df['data_time'] = pd.to_datetime(df['data_time'])

# Sort by data_time
df.sort_values('data_time', inplace=True)

df['origtatripno'] = df['origtatripno'].astype(str)

df['rt'] = df['rt'].astype(str)

target_hours = range(24)
route = '54'

trip_counts = []
for hour in target_hours:
    result = count_unique_trips(df, hour, route)
    trip_counts.append(result)

print(sum(trip_counts[1:]))
data = pd.DataFrame({'Hour': target_hours, 'Trip Count': trip_counts})


plt.figure(figsize=(10, 6))
sns.barplot(x='Hour', y='Trip Count', data=data)

for index, row in data.iterrows():
    plt.text(row.name, row['Trip Count'], str(row['Trip Count']), ha='center')

plt.title(f'Route: {route} Number of Unique Trips per Hour From Bus Tracker, wednesday, Total trips: {sum(trip_counts)}')
plt.xlabel('Hour')
plt.ylabel('Trip Count')

plt.show()
