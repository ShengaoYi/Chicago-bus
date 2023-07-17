# -*- coding: utf-8 -*-
'''
@Time    : 2023/7/14 9:11
@Author  : Ericyi
@File    : Route_Classification.py

'''
import pandas as pd
import geopandas as gpd

def add_direction(result_file, trips_file):
    """
    Add direction column to total_result.csv based on the most frequent shape_id for each route_id.

    Args:
        result_file (str): Path to the total_result.csv file.
        trips_file (str): Path to the trips.txt file.
        output_file (str): Path to save the output CSV file.

    Returns:
        None
    """

    # Read trips.txt and total_result.csv
    gtfs_trips = pd.read_csv(trips_file)
    total_result = pd.read_csv(result_file)

    # Calculate the most frequent shape_id for each route_id
    route_shape_counts = gtfs_trips.groupby(['route_id', 'shape_id']).size().reset_index(name='count')
    max_count_indices = route_shape_counts.groupby('route_id')['count'].idxmax()
    most_frequent_shapes = route_shape_counts.loc[max_count_indices]
    route_shape_dict = dict(most_frequent_shapes[['route_id', 'shape_id']].values)

    # Retrieve direction for each route based on the most frequent shape_id
    direction_dict = {}
    for route_id, shape_id in route_shape_dict.items():
        direction = gtfs_trips[gtfs_trips['shape_id'] == shape_id]['direction'].iloc[0]
        direction_dict[route_id] = direction

    # Add direction column to total_result
    total_result['direction'] = total_result['route_id'].map(direction_dict)

    # Modify direction values to East-West or North-South
    total_result['direction'] = total_result['direction'].replace({'East': 'East-West', 'West': 'East-West',
                                                                   'North': 'North-South', 'South': 'North-South'})

    return total_result



def add_labels(total_result, shapefile_path):
    """
    Read total_result.csv, add label columns based on route_id and shapefile data, and save the updated CSV file.

    Args:
        result_file (str): Path to the original total_result.csv file.
        shapefile_path (str): Path to the shapefile containing route_id and coordinate data.
        output_file (str): Path to save the output CSV file.

    Returns:
        None
    """

    # Read shapefile
    shapefile = gpd.read_file(shapefile_path)

    # Merge total_result with shapefile based on route_id
    merged_data = total_result.merge(shapefile[['route_id', 'XCoord', 'YCoord']], on='route_id', how='left')

    # Add label columns based on coordinate values
    merged_data['South/North'] = 'North'
    merged_data.loc[merged_data['YCoord'] < 41.845451, 'South/North'] = 'South'

    merged_data['East/West'] = 'East'
    merged_data.loc[merged_data['XCoord'] < -87.665892, 'East/West'] = 'West'

    return merged_data

result_file = r'E:\MIT Summer Intern\data\total_result.csv'

output_file = r'E:\MIT Summer Intern\data\total_result_with_direction.csv'

trips_file = r'E:\MIT Summer Intern\data\GTFS data\gtfs202212\trips.txt'

center_shp = r'E:\MIT Summer Intern\data\route_result\Chicago_routes_center.shp'

total_result = add_direction(result_file, trips_file)
# total_result.to_csv(output_file, index=False)
merge_data = add_labels(total_result, center_shp)
print(merge_data)
# Save the result to a new CSV file
merge_data.to_csv(output_file, index=False)

