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
merged_data.loc[merged_data['Inc'] < 45500, 'income_level'] = 'low-income'

# 将收入高于等于$27,000的行设置为'high_income'
merged_data.loc[merged_data['Inc'] >= 45500, 'income_level'] = 'high-income'

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

routes = gpd.read_file(r'E:\MIT Summer Intern\data\route_result\Chicago_routes.shp')

routes = routes.to_crs('EPSG:3435')

# 投影多边形数据
tracts = tracts.to_crs('EPSG:3435')

# 计算每条路线经过低收入区域的线段长度
income_intersected = gpd.overlay(routes, tracts[tracts['income_level'] == 'low-income'], how='intersection')
income_intersected['income_length'] = income_intersected.length

minority_intersected = gpd.overlay(routes, tracts[tracts['minority'] == 'minority'], how='intersection')
minority_intersected['minority_length'] = minority_intersected.length

nocar_intersected = gpd.overlay(routes, tracts[tracts['non_car'] == 'non-car'], how='intersection')
nocar_intersected['nocar_length'] = nocar_intersected.length

# 计算每条路线的总长度
routes['total_length'] = routes.length

# 按路线分组计算低收入区域长度之和和总长度
income_grouped = income_intersected.groupby('route_id')['income_length'].sum().reset_index()
minority_grouped = minority_intersected.groupby('route_id')['minority_length'].sum().reset_index()
nocar_grouped = nocar_intersected.groupby('route_id')['nocar_length'].sum().reset_index()

total_lengths = routes.groupby('route_id')['total_length'].sum().reset_index()

# 合并数据，计算低收入区域占比
income_result = total_lengths.merge(income_grouped, on='route_id', how='left')
minority_result = total_lengths.merge(minority_grouped, on='route_id', how='left')
nocar_result = total_lengths.merge(nocar_grouped, on='route_id', how='left')

income_result['low_income_percentage'] = income_result['income_length'] / income_result['total_length'] * 100
minority_result['minority_percentage'] = minority_result['minority_length'] / minority_result['total_length'] * 100
nocar_result['nocar_percentage'] = nocar_result['nocar_length'] / nocar_result['total_length'] * 100

chicago_routes = routes.merge(income_result[['route_id', 'low_income_percentage']], on='route_id', how='left')
chicago_routes = chicago_routes.merge(minority_result[['route_id', 'minority_percentage']], on='route_id', how='left')
chicago_routes = chicago_routes.merge(nocar_result[['route_id', 'nocar_percentage']], on='route_id', how='left')


# 打印结果
print(chicago_routes)
chicago_routes = chicago_routes.to_crs('EPSG:4326')

output_file = r'E:\MIT Summer Intern\data\route_result\chicago_routes_result.geojson'
chicago_routes.to_file(output_file, driver='GeoJSON')

merged_data = merged_data.to_crs('EPSG:4326')
# 导出为 GeoJSON 文件
output_file = r'E:\MIT Summer Intern\data\Socioecon\chicago_tracts_merged.geojson'
merged_data.to_file(output_file, driver='GeoJSON')
