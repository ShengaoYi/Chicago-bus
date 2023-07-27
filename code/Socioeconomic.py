# -*- coding: utf-8 -*-
'''
@Time    : 2023/7/15 22:33
@Author  : Ericyi
@File    : Socioeconomic.py

'''
import pandas as pd
import numpy as np
import geopandas as gpd

inc = pd.read_csv(r'E:\MIT Summer Intern\data\Socioecon\inc.csv')

inc = inc.rename(columns={"B19013001": "Inc"})

race = pd.read_csv(r'E:\MIT Summer Intern\data\Socioecon\race.csv')

race['Prcwhite'] = np.array(race['B02001002']) * 100 / np.array(race['B02001001'])

race = race.rename(columns={"B02001001": "TotPop"})

car = pd.read_csv(r'E:\MIT Summer Intern\data\Socioecon\car.csv')

car['PrcNoCar'] = np.array(car['B08201002']) * 100 / np.array(car['B08201001'])

gdf_tracts = gpd.read_file(r"E:\MIT Summer Intern\data\Socioecon\chicago_tracts.shp")

# 将选定的列与 gdf_tracts 按照 geoid 进行字段连接
merged_data = gdf_tracts.merge(inc[['geoid', 'Inc']], on='geoid', how='left')
merged_data = merged_data.merge(race[['geoid', 'TotPop', 'Prcwhite']], on='geoid', how='left')
merged_data = merged_data.merge(car[['geoid', 'PrcNoCar']], on='geoid', how='left')

# 添加空的income_level列
merged_data['income_level'] = ''

# 将收入低于$27,000的行设置为'low_income'
merged_data.loc[merged_data['Inc'] < 65500, 'income_level'] = 'low-income'

# 将收入高于等于$27,000的行设置为'high_income'
merged_data.loc[merged_data['Inc'] >= 65500, 'income_level'] = 'high-income'

# 添加空的minority_route列
merged_data['minority'] = ''

# 将Prcwhite小于50的行设置为'minority'
merged_data.loc[merged_data['Prcwhite'] < 50, 'minority'] = 'minority'

# 将Prcwhite大于等于50的行设置为'non-minority'，可以根据需要进行修改
merged_data.loc[merged_data['Prcwhite'] >= 50, 'minority'] = 'non-minority'

# 添加空的non_car_route列
merged_data['non_car'] = ''

# 将PrcNoCar大于30的行设置为'non-car'
merged_data.loc[merged_data['PrcNoCar'] > 30, 'non_car'] = 'non-car'

# 将PrcNoCar小于等于30的行设置为'car'，可以根据需要进行修改
merged_data.loc[merged_data['PrcNoCar'] <= 30, 'non_car'] = 'car'

tracts = merged_data

routes = gpd.read_file(r'E:\MIT Summer Intern\data\route_result\Chicago_frequent_routes.geojson')

routes = routes.to_crs('EPSG:3435')

# 投影多边形数据
tracts = tracts.to_crs('EPSG:3435')

# 计算每条路线经过低收入区域的线段长度
low_income_intersected = gpd.overlay(routes, tracts[tracts['income_level'] == 'low-income'], how='intersection')
low_income_intersected['low_income_length'] = low_income_intersected.length

high_income_intersected = gpd.overlay(routes, tracts[tracts['income_level'] == 'high-income'], how='intersection')
high_income_intersected['high_income_length'] = high_income_intersected.length

minority_intersected = gpd.overlay(routes, tracts[tracts['minority'] == 'minority'], how='intersection')
minority_intersected['minority_length'] = minority_intersected.length

non_minority_intersected = gpd.overlay(routes, tracts[tracts['minority'] == 'non-minority'], how='intersection')
non_minority_intersected['non_minority_length'] = non_minority_intersected.length

nocar_intersected = gpd.overlay(routes, tracts[tracts['non_car'] == 'non-car'], how='intersection')
nocar_intersected['nocar_length'] = nocar_intersected.length

car_intersected = gpd.overlay(routes, tracts[tracts['non_car'] == 'car'], how='intersection')
car_intersected['car_length'] = car_intersected.length

# 计算每条路线的总长度
routes['total_length'] = routes.length

# Calculate the sum of lengths for low-income area segments and total length for each route
low_income_grouped = low_income_intersected.groupby('route_id')['low_income_length'].sum().reset_index()
high_income_grouped = high_income_intersected.groupby('route_id')['high_income_length'].sum().reset_index()
minority_grouped = minority_intersected.groupby('route_id')['minority_length'].sum().reset_index()
non_minority_grouped = non_minority_intersected.groupby('route_id')['non_minority_length'].sum().reset_index()
nocar_grouped = nocar_intersected.groupby('route_id')['nocar_length'].sum().reset_index()
car_grouped = car_intersected.groupby('route_id')['car_length'].sum().reset_index()

# Calculate the total income length for each route by summing 'low_income_length' and 'high_income_length'
income_lengths = low_income_grouped.merge(high_income_grouped, on='route_id', suffixes=('_low_income', '_high_income'))
income_lengths['total_income_length'] = income_lengths['low_income_length'] + income_lengths['high_income_length']

# Calculate the total minority length for each route by summing 'minority_length' and 'non_minority_length'
minority_lengths = minority_grouped.merge(non_minority_grouped, on='route_id', suffixes=('_minority', '_non_minority'))
minority_lengths['total_minority_length'] = minority_lengths['minority_length'] + minority_lengths['non_minority_length']

# Calculate the total car length for each route by summing 'nocar_length' and 'car_length'
car_lengths = nocar_grouped.merge(car_grouped, on='route_id', suffixes=('_nocar', '_car'))
car_lengths['total_car_length'] = car_lengths['nocar_length'] + car_lengths['car_length']

# Merge the calculated lengths with the routes DataFrame
chicago_routes = routes.merge(low_income_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(high_income_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(minority_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(non_minority_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(nocar_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(car_grouped, on='route_id', how='left')
chicago_routes = chicago_routes.merge(income_lengths[['route_id', 'total_income_length']], on='route_id', how='left')
chicago_routes = chicago_routes.merge(minority_lengths[['route_id', 'total_minority_length']], on='route_id', how='left')
chicago_routes = chicago_routes.merge(car_lengths[['route_id', 'total_car_length']], on='route_id', how='left')

# Calculate the percentage of low-income area length and other metrics
chicago_routes['low_income_percentage'] = chicago_routes['low_income_length'] / chicago_routes['total_income_length'] * 100
# chicago_routes['high_income_percentage'] = chicago_routes['high_income_length'] / chicago_routes['total_income_length'] * 100
chicago_routes['minority_percentage'] = chicago_routes['minority_length'] / chicago_routes['total_minority_length'] * 100
# chicago_routes['non_minority_percentage'] = chicago_routes['non_minority_length'] / chicago_routes['total_minority_length'] * 100
chicago_routes['nocar_percentage'] = chicago_routes['nocar_length'] / chicago_routes['total_car_length'] * 100
# chicago_routes['car_percentage'] = chicago_routes['car_length'] / chicago_routes['total_car_length'] * 100

chicago_routes = chicago_routes.to_crs('EPSG:4326')

output_file = r'E:\MIT Summer Intern\data\route_result\chicago_routes_result_latest.geojson'
chicago_routes.to_file(output_file, driver='GeoJSON')
#
# merged_data = merged_data.to_crs('EPSG:4326')
# # 导出为 GeoJSON 文件
# output_file = r'E:\MIT Summer Intern\data\Socioecon\chicago_tracts_merged.geojson'
# merged_data.to_file(output_file, driver='GeoJSON')
