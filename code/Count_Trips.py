# -*- coding: utf-8 -*-
'''
@Time    : 2023/6/24 20:27
@Author  : Ericyi
@File    : Count_Trips.py

'''
import pandas as pd
import os
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def GTFS(stop_times_file, stop_file, trips_file, calendar_file, route, day, date):

    def merge_files(o_df, t_df, t_file_columns, field):
        # Select the desired columns from the stops DataFrame
        t_df = t_df[t_file_columns]

        # Merge the DataFrames based on stop_id
        merged_df = pd.merge(o_df, t_df, on=field, how='left')

        return merged_df

    def count_GTFS_trips(data, target_hour, route):
        # Convert the time column to datetime type
        data['arrival_time'] = pd.to_datetime(data['arrival_time'], format='%H:%M:%S', errors='coerce')

        # Extract the hour component from arrival_time using apply()
        data['arrival_hour'] = data['arrival_time'].apply(lambda x: x.hour)

        # Filter the data for the target hour
        target_df = data[data['arrival_hour'] == target_hour]

        # Filter the data for the specified route
        route_df = target_df[target_df['route_id'] == route]

        # Count the number of unique trips
        trip_count = len(route_df['trip_id'])

        return trip_count

    # Read the GTFS data files
    stop_times_df = pd.read_csv(stop_times_file)
    stop_times_df['trip_id'] = stop_times_df['trip_id'].astype(str)

    stops_df = pd.read_csv(stop_file)

    trips_df = pd.read_csv(trips_file)
    trips_df['trip_id'] = trips_df['trip_id'].astype(str)
    trips_df['route_id'] = trips_df['route_id'].astype(str)
    trips_df['service_id'] = trips_df['service_id'].astype(str)

    calendar_df = pd.read_csv(calendar_file)
    calendar_df['service_id'] = calendar_df['service_id'].astype(str)

    stops_columns = ['stop_id', 'stop_lat', 'stop_lon']
    df = merge_files(stop_times_df, stops_df, stops_columns, 'stop_id')

    trips_columns = ['trip_id', 'route_id', 'service_id']

    df = merge_files(df, trips_df, trips_columns, 'trip_id')

    # Filter the calendar data based on start_date and end_date
    start_date = 20230530
    end_date = 20230603

    # Select service_id based on date
    calendar_filtered = calendar_df[(calendar_df['start_date'] <= date) & (calendar_df['end_date'] >= date)]

    # Get the days of the week to analyze
    days_of_week = ['tuesday', 'wednesday', 'thursday', 'friday']

    # Get the service IDs for the specific day
    service_ids = calendar_filtered[calendar_filtered[day] == 1]['service_id']

    service_ids = service_ids.astype(str)
    df['service_id'] = df['service_id'].astype(str)
    df['stop_sequence'] = df['stop_sequence'].astype(str)

    # Filter the DataFrame for the selected service IDs
    day_df = df[df['service_id'].isin(service_ids)]

    # To avoid duplication, filter the stop_sequence==1
    day_df = day_df[(day_df['stop_sequence'] == '1')]

    day_df['arrival_time'] = pd.to_datetime(day_df['arrival_time'])

    target_hours = range(24)
    trip_counts = []
    for hour in target_hours:
        result = count_GTFS_trips(day_df, hour, route)
        trip_counts.append(result)
        # print(f"Route: {route} Number of trips for {day} at hour {hour}: {result}")

    return sum(trip_counts[1:])

def Bus_Tracker(bus_tracker_file, date, route):

    def count_bus_tracker_trips(df, target_hour, route):
        # Just keep the first trip_id
        df = df.drop_duplicates('origtatripno', keep='first')

        # df.to_csv(r'E:\MIT Summer Intern\data\CTA Bus\0531deduplicated.csv')
        #
        # df3 = df[df['rt'] == '85']
        # df3.to_csv(r'E:\MIT Summer Intern\data\CTA Bus\0531deduplicated85.csv')

        # 筛选特定日期和小时的数据
        filtered_df = df[(df['data_hour'] == target_hour) & (df['rt'] == route)]

        # 统计唯一行程数量
        unique_trip_count = len(filtered_df['origtatripno'].unique())

        return unique_trip_count

    df = pd.read_csv(bus_tracker_file)

    df = df[df['data_date'] == date]

    df['data_time'] = pd.to_datetime(df['data_time'])

    # Sort by data_time
    df.sort_values('data_time', inplace=True)

    df['origtatripno'] = df['origtatripno'].astype(str)

    df['rt'] = df['rt'].astype(str)

    target_hours = range(24)

    trip_counts = []
    for hour in target_hours:
        result = count_bus_tracker_trips(df, hour, route)
        trip_counts.append(result)

    return sum(trip_counts[1:])

GTFS_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202302'
Bus_path = r'E:\MIT Summer Intern\data\CTA Bus'

stop_times_file = os.path.join(GTFS_path, 'stop_times.txt')
stop_file = os.path.join(GTFS_path, 'stops.txt')
trips_file = os.path.join(GTFS_path, 'trips.txt')
calendar_file = os.path.join(GTFS_path, 'calendar.txt')

top_routes = ['85', '97', '111A', '68', '81W']
bottom_routes = ['2', '125', '34', '108', '134']

Dec_dates = ['2022-12-13', '2022-12-14', '2022-12-15']
Feb_dates = ['2023-02-14', '2023-02-15', '2023-02-16']
Mar_dates = ['2023-03-14', '2023-03-15', '2023-03-16']
days_of_week = ['tuesday', 'wednesday', 'thursday']


fig, ax = plt.subplots(figsize=(12, 8))

# 创建一个空的DataFrame来保存数据
data = pd.DataFrame(columns=['Route', 'Day of Week', 'Ratio'])

for i, date in enumerate(Mar_dates):
    ratios = []
    for j, route in enumerate(top_routes):
        bus_tracker_file = os.path.join(Bus_path, date + '.csv')
        Bus_Tracker_trips = Bus_Tracker(bus_tracker_file, date, route)

        GTFS_date = int(date.replace('-', ''))
        GTFS_trips = GTFS(stop_times_file, stop_file, trips_file, calendar_file, route, days_of_week[i], GTFS_date)

        ratio = Bus_Tracker_trips / GTFS_trips
        ratios.append(ratio)

        data = data.append({'Route': route, 'Day of Week': days_of_week[i], 'Ratio': ratio}, ignore_index=True)


# 使用Seaborn绘制柱状图
sns.barplot(x='Route', y='Ratio', hue='Day of Week', data=data, ax=ax)

font_prop = FontProperties(size=12)  # 设置字体大小
for p in ax.patches:
    ax.annotate(f'{p.get_height():.3f}', (p.get_x() + p.get_width() / 2, p.get_height()), ha='center', va='bottom',
                fontproperties=font_prop)

# 设置图形标题和标签
ax.set_title('Ratio of Top 10 Routes in Mar', fontsize=16)  # 设置标题字体大小
ax.set_xlabel('Route', fontsize=14)  # 设置横坐标标签字体大小
ax.set_ylabel('Ratio', fontsize=14)  # 设置纵坐标标签字体大小

# 显示图例
ax.legend(title='Day of Week', fontsize=12)  # 设置图例字体大小

# 调整布局，避免横坐标标签重叠
plt.tight_layout()
# 显示图例
ax.legend(title='Day of Week')

# 调整布局，避免横坐标标签重叠
plt.tight_layout()

# 显示图形
plt.show()
