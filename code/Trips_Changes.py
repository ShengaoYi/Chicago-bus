# -*- coding: utf-8 -*-
'''
@Time    : 2023/7/3 18:25
@Author  : Ericyi
@File    : Trips_Changes.py

'''
import os
import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_monthly_actual_trips_average(folder_path, frequent_sch_routes):
    # Get file paths for the specified month in the folder
    file_names = os.listdir(folder_path)

    actual_trips_dict = {}
    n = 0
    # Read each file, calculate the sum and count for each route
    for file in file_names:
        date_string = file.split('.')[0]
        date_object = datetime.strptime(date_string, '%Y-%m-%d')

        # Get weekday
        weekday = date_object.weekday()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_string = weekdays[weekday]

        if weekday_string == 'tuesday' or weekday_string == 'wednesday' or weekday_string == 'thursday':
            n += 1
            df = pd.read_csv(os.path.join(folder_path, file))
            for _, row in df.iterrows():
                route_id = row['route_id']
                trips_count = row['trips']
                if route_id in frequent_sch_routes:
                    if route_id not in actual_trips_dict.keys():
                        actual_trips_dict[route_id] = trips_count
                    else:
                        actual_trips_dict[route_id] += trips_count

    # Calculate the average for each route
    for k in actual_trips_dict.keys():
        actual_trips_dict[k] = actual_trips_dict[k] / n

    return actual_trips_dict

def calculate_monthly_schedule_trips_average(GTFS_result_folder, frequent_sch_routes):
    # Calculate gap (TS_D - TO_D)
    file_names = os.listdir(GTFS_result_folder)

    sch_trips_dict = {}
    n = 0
    # Read each file, calculate the sum and count for each route
    for file in file_names:
        date_string = file.split('.')[0]
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        # Get weekday
        weekday = date_object.weekday()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_string = weekdays[weekday]

        if weekday_string == 'tuesday' or weekday_string == 'wednesday' or weekday_string == 'thursday':
            n += 1
            GTFS_result = pd.read_csv(os.path.join(GTFS_result_folder, file))

            for _, row in GTFS_result.iterrows():
                route_id = row['route_id']
                GTFS_trips_count = row['trips']

                if route_id in frequent_sch_routes:
                    if GTFS_trips_count:
                        if route_id not in sch_trips_dict.keys():
                            sch_trips_dict[route_id] = GTFS_trips_count
                        else:
                            sch_trips_dict[route_id] += GTFS_trips_count

    # Calculate the average ratio for each route
    for k in sch_trips_dict.keys():
        sch_trips_dict[k] = sch_trips_dict[k] / n

    return sch_trips_dict

def calculate_monthly_trips_gap(Bus_result_folder, GTFS_result_folder, frequent_sch_routes):
    # Calculate gap (TS_D - TO_D)
    file_names = os.listdir(Bus_result_folder)

    gap_dict = {}
    n = 0
    # Read each file, calculate the sum and count for each route
    for file in file_names:
        date_string = file.split('.')[0]
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        # Get weekday
        weekday = date_object.weekday()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_string = weekdays[weekday]

        if weekday_string == 'tuesday' or weekday_string == 'wednesday' or weekday_string == 'thursday':
            n += 1
            Bus_result = pd.read_csv(os.path.join(Bus_result_folder, file))
            GTFS_result = pd.read_csv(os.path.join(GTFS_result_folder, file))

            for _, row in Bus_result.iterrows():
                route_id = row['route_id']
                Bus_trips_count = row['trips']
                GTFS_trips_count = int(GTFS_result[GTFS_result['route_id'] == route_id]['trips'].values)

                if route_id in frequent_sch_routes:
                    if GTFS_trips_count:
                        if route_id not in gap_dict.keys():
                            gap_dict[route_id] = (GTFS_trips_count - Bus_trips_count) / GTFS_trips_count
                        else:
                            gap_dict[route_id] += (GTFS_trips_count - Bus_trips_count) / GTFS_trips_count

    # Calculate the average ratio for each route
    for k in gap_dict.keys():
        gap_dict[k] = gap_dict[k] / n

    return gap_dict

def calculate_monthly_ratio_average(Bus_result_folder, GTFS_result_folder, frequent_sch_routes):
    # Get file paths for the specified month in the folder
    file_names = os.listdir(Bus_result_folder)

    ratio_dict = {}
    n = 0
    # Read each file, calculate the sum and count for each route
    for file in file_names:
        date_string = file.split('.')[0]
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        # Get weekday
        weekday = date_object.weekday()
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        weekday_string = weekdays[weekday]

        if weekday_string == 'tuesday' or weekday_string == 'wednesday' or weekday_string == 'thursday':
            n += 1
            Bus_result = pd.read_csv(os.path.join(Bus_result_folder, file))
            GTFS_result = pd.read_csv(os.path.join(GTFS_result_folder, file))

            for _, row in Bus_result.iterrows():
                route_id = row['route_id']
                Bus_trips_count = row['trips']
                GTFS_trips_count = int(GTFS_result[GTFS_result['route_id'] == route_id]['trips'].values)

                if route_id in frequent_sch_routes:
                    if GTFS_trips_count:
                        if route_id not in ratio_dict.keys():
                            ratio_dict[route_id] = Bus_trips_count / GTFS_trips_count
                        else:
                            ratio_dict[route_id] += Bus_trips_count / GTFS_trips_count

    # Calculate the average ratio for each route
    for k in ratio_dict.keys():
        ratio_dict[k] = ratio_dict[k] / n

    return ratio_dict

# def calculate_schedule_cuts_score(Bus_dec_result_folder, GTFS_dec_result_folder, GTFS_feb_result_folder, frequent_sch_routes):
#     file_names = os.listdir(Bus_dec_result_folder)
#
#     ratio_dict = {}
#     n = 0
#     # Read each file, calculate the sum and count for each route
#     for file in file_names:
#         date_string = file.split('.')[0]
#         date_object = datetime.strptime(date_string, '%Y-%m-%d')
#         # Get weekday
#         weekday = date_object.weekday()
#         weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
#         weekday_string = weekdays[weekday]
#
#         if weekday_string == 'tuesday' or weekday_string == 'wednesday' or weekday_string == 'thursday':
#             n += 1
#             Bus_dec_result = pd.read_csv(os.path.join(Bus_dec_result_folder, file))
#             GTFS_result = pd.read_csv(os.path.join(GTFS_result_folder, file))

def calculate_trips_percentage_change(dec_dict, feb_dict):
    result_dict = {}
    for route_id, dec_value in dec_dict.items():
        if dec_value == 0:
            continue
        if route_id in feb_dict:
            feb_value = feb_dict[route_id]
            prc_change = (feb_value - dec_value) / dec_value * 100
            result_dict[route_id] = prc_change

    return result_dict


def save_dicts_to_csv(dec_dict, feb_dict, result_dict, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['route_id', 'trips_dec', 'trips_feb', 'prc_change'])

        for route_id in sorted(dec_dict.keys()):
            dec_value = dec_dict.get(route_id, 0)
            feb_value = feb_dict.get(route_id, 0)
            prc_change = result_dict.get(route_id, 0)
            writer.writerow([route_id, dec_value, feb_value, prc_change])


def plot_trips_routes(result_dict, dec_dict, feb_dict):
    # 根据 trips_dec 和 trips_feb 的值之和排序得到前十的路线
    # selected_routes = sorted(result_dict.items(), key=lambda x: dec_dict.get(x[0], 0) + feb_dict.get(x[0], 0), reverse=True)
    #
    # # 提取前十路线的数据
    # selected_route_ids = [route[0] for route in selected_routes]
    # print(selected_route_ids)
    selected_route_ids = [route for route in bottom_routes]
    trips_dec = [dec_dict.get(route_id, 0) for route_id in selected_route_ids]
    print(trips_dec)
    trips_feb = [feb_dict.get(route_id, 0) for route_id in selected_route_ids]
    print(trips_feb)
    trips_prc_change = [result_dict.get(route_id, 0) for route_id in selected_route_ids]
    print(trips_prc_change)
    abs_change = [feb_dict.get(route_id, 0) - dec_dict.get(route_id, 0) for route_id in selected_route_ids]
    print(abs_change)
    total_trips = [dec_dict.get(route_id, 0) + feb_dict.get(route_id, 0) for route_id in selected_route_ids]

    # 创建 DataFrame
    df = pd.DataFrame({
        'route_id': selected_route_ids,
        'trips_dec': trips_dec,
        'trips_feb': trips_feb,
        'prc_change': trips_prc_change,
        'total_trips': total_trips,
        'absolute_change': abs_change
    })

    # 绘制柱状图
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='route_id', y='prc_change', data=df)
    ax.set(xlabel='Route ID', ylabel='Percentage Change')
    ax.set_title('Bottom 10 Routes - Percentage Change')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # 显示数值标签和总行程数量
    for i, p in enumerate(ax.patches):
        ax.annotate(f"{format(p.get_height(), '.2f')}%, {format(abs_change[i], '.2f')} \n({format(total_trips[i], '.2f')})",
                    (p.get_x() + p.get_width() / 2, p.get_height() - 0.5), ha='center', va='center')

    plt.tight_layout()
    plt.show()

def plot_horizontal_trips(result_dict, dec_dict, feb_dict, dec_gap_trips_dict):
    # Create DataFrame
    df = pd.DataFrame({
        'route_id': result_dict.keys(),
        'trips_actual_dec': [dec_dict.get(route_id, 0) for route_id in result_dict.keys()],
        'trips_actual_feb': [feb_dict.get(route_id, 0) for route_id in result_dict.keys()],
        'prc_change': result_dict.values(),
        'dec_gap': [dec_gap_trips_dict.get(route_id, 0) * 100 for route_id in result_dict.keys()],
    })

    # Sort DataFrame by the December gap (TS - TO)
    df = df.sort_values(by='dec_gap', ascending=False)
    print(list(df['route_id']))
    # print(list(df['prc_change']))
    print(list(df['dec_gap']))

    # Create a horizontal barplot
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='prc_change', y='route_id', data=df)
    ax.set(xlabel='Actual Trips Percentage Change', ylabel='Route ID')
    ax.set_title('Routes Sorted by December Gap (TS - TO)')

    plt.tight_layout()
    plt.show()

def plot_sch_cut_score(dec_sch_trips_dict, feb_sch_trips_dict, dec_actual_trips_dict):

    sch_cut_score_dict = {route_id: (feb_sch_trips_dict[route_id] - dec_sch_trips_dict[route_id]) / (
                dec_sch_trips_dict[route_id] - dec_actual_trips_dict[route_id]) for route_id in
                          dec_actual_trips_dict.keys() if
                          (dec_sch_trips_dict[route_id] - dec_actual_trips_dict[route_id]) != 0}
    print(sch_cut_score_dict)
    result = []
    for route in ['81', '63', '152', '77', '67', '80', '82', '9', '55', '54B', '56', '62', '15', '21', '76', '47', '49', '95', '78', '71', '12', '52A', '34', '126', '65', '20', '66', '72', '73', '111', '146', '6', 'J14', '54', '112', '30', '60', '115', '36', '74', '119', '151', '28', '53', '70', '22', '29', '103', '8A', '92', '53A', '3', '24', '91', '147', '94', '79', '4', '52', '35', '57', '18', '87', '8', '50', '43', '59', '44', '75', '63W', '7', '93', '157', '49B', '155', '106', '172', '97']:
        result.append(sch_cut_score_dict[route])

    print(result)

    # Extract the values from the result_ratio_dict
    values = list(sch_cut_score_dict.values())
    selected_keys = [key for key, value in sch_cut_score_dict.items() if value < -50]
    print(selected_keys)

    # Create the bar chart using Seaborn
    sns.histplot(values, kde=False, edgecolor='black')

    # Set labels and title
    # plt.xticks(np.arange(-75, 5, 5))
    plt.xlabel('Intervals')
    plt.ylabel('Count')
    plt.title('Distribution of Values')

    # Show the plot
    plt.show()

def plot_ratio_routes(result_dict, dec_dict, feb_dict, frequent_sch_routes):
    print(dec_dict)
    # 根据 ratio_dec 和 ratio_feb 的值之和排序得到前十的路线
    sorted_routes = sorted(result_dict.items(), key=lambda x: dec_dict.get(x[0], 0) + feb_dict.get(x[0], 0), reverse=False)
    selected_routes = [route[0] for route in sorted_routes if route[0] in frequent_sch_routes][:10]
    print(selected_routes)

    # 提取前十路线的数据
    selected_route_ids = [route[0] for route in sorted_routes if route[0] in frequent_sch_routes]
    print(selected_route_ids)
    selected_route_ids = [route[0] for route in sorted_routes]

    ratio_dec = [dec_dict.get(route_id, 0) for route_id in selected_route_ids]
    # print(ratio_dec)
    ratio_feb = [feb_dict.get(route_id, 0) for route_id in selected_route_ids]
    # print(ratio_feb)
    ratio_prc_change = [result_dict.get(route_id, 0) for route_id in selected_route_ids]
    # print(ratio_prc_change)
    abs_change = [feb_dict.get(route_id, 0) - dec_dict.get(route_id, 0) for route_id in selected_route_ids]
    # print(abs_change)

    total_trips = [dec_dict.get(route_id, 0) + feb_dict.get(route_id, 0) for route_id in selected_route_ids]

    # 创建 DataFrame
    df = pd.DataFrame({
        'route_id': selected_route_ids,
        'trips_dec': ratio_dec,
        'trips_feb': ratio_feb,
        'prc_change': ratio_prc_change,
        'total_trips': total_trips
    })

    # 绘制柱状图
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='route_id', y='prc_change', data=df)
    ax.set(xlabel='Route ID', ylabel='Percentage Change')
    ax.set_title('Top 10% Routes - Percentage Change')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # 显示数值标签和总行程数量
    # for i, p in enumerate(ax.patches):
    #     ax.annotate(f"{format(p.get_height(), '.2f')}%\n({format(total_trips[i], '.2f')})",
    #                 (p.get_x() + p.get_width() / 2, p.get_height() + 0.3), ha='center', va='center')

    plt.tight_layout()
    plt.show()

# Define folder paths
dec_bus_result_folder = 'E:/MIT Summer Intern/data/CTA Bus/202212_result'
feb_bus_result_folder = 'E:/MIT Summer Intern/data/CTA Bus/202302_result'

dec_GTFS_result_folder = r'E:\MIT Summer Intern\data\GTFS data\gtfs202212_result'
feb_GTFS_result_folder = r'E:\MIT Summer Intern\data\GTFS data\gtfs202302_result'

frequent_sch_routes = ['103', '106', '111', '112', '115', '119', '12', '126', '146', '147', '15', '151', '152', '155', '157', '172', '18', '20', '21', '22', '24', '28', '29', '3', '30', '34', '35', '36', '4', '43', '44', '47', '49', '49B', '50', '52', '52A', '53', '53A', '54', '54B', '55', '56', '57', '59', '6', '60', '62', '63', '63W', '65', '66', '67', '7', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '8', '80', '81', '82', '85', '87', '8A', '9', '91', '92', '93', '94', '95', '97', 'J14']
garage_routes = ['12', '20', '37', '53', '54', '54B', '57', '65', '66', '70', '72', '73', '74', '120', '121', '125', '157']
top_routes = ['97', '172', '85', '106', '49B', '43', '157', '7', '75', '93']
bottom_routes = ['81', '9', '77', '63', '152', '56', '62', '67', '80', '82']

# Calculate the average trips number for each route in December
dec_actual_trips_dict = calculate_monthly_actual_trips_average(dec_bus_result_folder, frequent_sch_routes)
dec_sch_trips_dict = calculate_monthly_schedule_trips_average(dec_GTFS_result_folder, frequent_sch_routes)

dec_gap_trips_dict = calculate_monthly_trips_gap(dec_bus_result_folder, dec_GTFS_result_folder, frequent_sch_routes)

# Calculate the average for each route in February
feb_actual_trips_dict = calculate_monthly_actual_trips_average(feb_bus_result_folder, frequent_sch_routes)
feb_sch_trips_dict = calculate_monthly_schedule_trips_average(feb_GTFS_result_folder, frequent_sch_routes)

# fw = open(r'E:\MIT Summer Intern\data\total_result.csv', 'w', encoding='utf-8')
#
# fw.write('route_id,Dec_sch,Dec_actual,Feb_sch,Feb_actual\n')
#
# for route in frequent_sch_routes:
#     s = route + ',' + str(dec_sch_trips_dict[route]) + ',' + str(dec_actual_trips_dict[route]) + ',' + str(feb_sch_trips_dict[route]) + ',' + str(feb_actual_trips_dict[route]) + '\n'
#     fw.write(s)

# Calculate overall actual trips number percentage change
overall_trips_change = (sum(feb_actual_trips_dict.values()) - sum(dec_actual_trips_dict.values())) / sum(dec_actual_trips_dict.values()) * 100
# print(overall_trips_change)

# Calculate average actual trips number percentage change
result_actual_trips_dict = calculate_trips_percentage_change(dec_actual_trips_dict, feb_actual_trips_dict)
average_overall_trips_change = sum(result_actual_trips_dict.values()) / len(result_actual_trips_dict) * 100
# print(average_overall_trips_change)

# plot_trips_routes(result_actual_trips_dict, dec_actual_trips_dict, feb_actual_trips_dict)

plot_horizontal_trips(result_actual_trips_dict, dec_actual_trips_dict, feb_actual_trips_dict, dec_gap_trips_dict)

# Calculate and plot schedule cuts scores
plot_sch_cut_score(dec_sch_trips_dict, feb_sch_trips_dict, dec_actual_trips_dict)


# Save the result to a CSV file
# output_file = r'E:\MIT Summer Intern\data\CTA Bus\service_changes_dec_to_feb.csv'
# save_dicts_to_csv(dec_dict, feb_dict, result_dict, output_file)

# Calculate the average ratio for frequent route in December
# dec_ratio_dict = calculate_monthly_ratio_average(dec_bus_result_folder, dec_GTFS_result_folder, frequent_sch_routes)
#
# feb_ratio_dict = calculate_monthly_ratio_average(feb_bus_result_folder, feb_GTFS_result_folder, frequent_sch_routes)
#
# # Calculate the percentage change
# result_ratio_dict = calculate_trips_percentage_change(dec_ratio_dict, feb_ratio_dict)
# # print(result_ratio_dict)
# # overall_ratio_reduction = sum(result_ratio_dict.values()) / len(result_ratio_dict)
# # print(overall_ratio_reduction)
# plot_ratio_routes(result_ratio_dict, dec_ratio_dict, feb_ratio_dict, frequent_sch_routes)

# output_file = r'E:\MIT Summer Intern\data\CTA Bus\ratio_changes_dec_to_feb.csv'
# save_dicts_to_csv(dec_ratio_dict, feb_ratio_dict, result_ratio_dict, output_file)



