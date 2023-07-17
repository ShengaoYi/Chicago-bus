# -*- coding: utf-8 -*-
'''
@Time    : 2023/7/3 16:32
@Author  : Ericyi
@File    : Count_All_Trips_Daily.py

'''
import pandas as pd
import os
from datetime import datetime

def GTFS(stop_times_file, stop_file, trips_file, calendar_file, GTFS_dict, day, date):

    def merge_files(o_df, t_df, t_file_columns, field):
        # Select the desired columns from the stops DataFrame
        t_df = t_df[t_file_columns]

        # Merge the DataFrames based on stop_id
        merged_df = pd.merge(o_df, t_df, on=field, how='left')

        return merged_df

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

    # Select service_id based on date
    calendar_filtered = calendar_df[(calendar_df['start_date'] <= date) & (calendar_df['end_date'] >= date)]

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

    # Convert the time column to datetime type
    day_df['arrival_time'] = pd.to_datetime(day_df['arrival_time'], format='%H:%M:%S', errors='coerce')

    # Extract the hour component from arrival_time using apply()
    day_df['arrival_hour'] = day_df['arrival_time'].apply(lambda x: x.hour)

    all_routes = list(set(day_df['route_id']))

    for route in all_routes:
        target_hours = range(24)
        trip_counts = []
        for hour in target_hours:
            # Filter the data for the target hour
            target_df = day_df[day_df['arrival_hour'] == hour]
            # Filter the data for the specified route
            route_df = target_df[target_df['route_id'] == route]

            # Count the number of unique trips
            trip_count = len(route_df['trip_id'])

            trip_counts.append(trip_count)
        GTFS_dict[route] = sum(trip_counts[4:])

    return GTFS_dict

def Bus_Tracker(bus_tracker_file, date, Bus_Tracker_dict):

    def count_bus_tracker_trips(df, target_hour, route):
        # Just keep the first trip_id
        df = df.drop_duplicates('origtatripno', keep='first')

        # Filter by date and hour
        filtered_df = df[(df['data_hour'] == target_hour) & (df['rt'] == route)]

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

    all_routes = list(set(df['rt']))

    for route in all_routes:
        trip_counts = []
        for hour in target_hours:
            result = count_bus_tracker_trips(df, hour, route)
            trip_counts.append(result)
        Bus_Tracker_dict[route] = sum(trip_counts[4:])

    return Bus_Tracker_dict

start_date = 20230201

end_date = 20230228

for date in range(start_date, end_date + 1):
    date_string = str(date)[0:4] + '-' + str(date)[4:6] + '-' + str(date)[6:]
    date_object = datetime.strptime(date_string, '%Y-%m-%d')

    # Get weekday
    weekday = date_object.weekday()
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    weekday_string = weekdays[weekday]

    month = date_string.split('-')[1]
    Bus_path = ''
    GTFS_path = ''
    Bus_result_path = ''
    GTFS_result_path = ''

    if month == '12':
        GTFS_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202212'
        Bus_path = r'E:\MIT Summer Intern\data\CTA Bus\202212'
        Bus_result_path = r'E:\MIT Summer Intern\data\CTA Bus\202212_result'
        GTFS_result_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202212_result'
    if month == '02':
        GTFS_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202302'
        Bus_path = r'E:\MIT Summer Intern\data\CTA Bus\202302'
        Bus_result_path = r'E:\MIT Summer Intern\data\CTA Bus\202302_result'
        GTFS_result_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202302_result'
    if month == '03':
        GTFS_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202303'
        Bus_path = r'E:\MIT Summer Intern\data\CTA Bus\202303'
        Bus_result_path = r'E:\MIT Summer Intern\data\CTA Bus\202303_result'
        GTFS_result_path = r'E:\MIT Summer Intern\data\GTFS data\gtfs202303_result'

    # Bus_Tracker_dict = {}
    # bus_tracker_file = os.path.join(Bus_path, date_string + '.csv')
    # Bus_Tracker_dict = Bus_Tracker(bus_tracker_file, date_string, Bus_Tracker_dict)
    # Bus_Tracker_sorted = {k: Bus_Tracker_dict[k] for k in sorted(Bus_Tracker_dict.keys())}
    # print(date)
    #
    # Bus_result_file = os.path.join(Bus_result_path, date_string + '.csv')
    #
    # fw = open(Bus_result_file, 'w', encoding='utf-8')
    #
    # fw.write('route_id,trips\n')
    # for k, v in Bus_Tracker_sorted.items():
    #     s = k + ',' + str(v) + '\n'
    #     fw.write(s)
    # fw.close()


    stop_times_file = os.path.join(GTFS_path, 'stop_times.txt')
    stop_file = os.path.join(GTFS_path, 'stops.txt')
    trips_file = os.path.join(GTFS_path, 'trips.txt')
    calendar_file = os.path.join(GTFS_path, 'calendar.txt')

    GTFS_dict = {}

    GTFS_dict = GTFS(stop_times_file, stop_file, trips_file, calendar_file, GTFS_dict, weekday_string, date)
    GTFS_sorted = {k: GTFS_dict[k] for k in sorted(GTFS_dict.keys())}

    GTFS_result_file = os.path.join(GTFS_result_path, date_string + '.csv')

    fw = open(GTFS_result_file, 'w', encoding='utf-8')

    fw.write('route_id,trips\n')
    for k, v in GTFS_sorted.items():
        s = k + ',' + str(v) + '\n'
        fw.write(s)
    fw.close()






