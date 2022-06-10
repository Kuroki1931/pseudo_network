import geopandas as gpd
import networkx as nx
import fiona
import pandas as pd
import numpy as np

from shapely.wkt import loads 
from shapely.geometry import Point
from scipy.spatial import cKDTree


def _ckdnearest(gdA, gdB):
    nA = np.array(list(gdA.geometry.apply(lambda x: (x.x, x.y))))
    nB = np.array(list(gdB.geometry.apply(lambda x: (x.x, x.y))))
    btree = cKDTree(nB)
    dist, idx = btree.query(nA, k=1)
    gdB_nearest = gdB.iloc[idx].drop(columns="geometry").reset_index(drop=True)
    gdf = pd.concat(
        [
            gdA.reset_index(drop=True),
            gdB_nearest,
            pd.Series(dist, name='dist')
        ], 
        axis=1)
    return gdf

# get vertices - get start and end point of road
def get_vertices(output=False):
    point_unique_list = []
    road_unique_list = []
    geopoint_list = []
    road_length_list = []
    start_id = 0
    with fiona.open('target_road.gpkg') as lines:
        for line in lines:
            # raod start point
            geopoint_list.append(str(Point(line['geometry']['coordinates'][0])))
            point_unique_list.append(start_id)
            start_id += 1
            road_unique_list.append(int(line['id'])-1)
            road_length_list.append(line['properties']['LENGTH'])
            # road end point
            geopoint_list.append(str(Point(line['geometry']['coordinates'][-1])))
            point_unique_list.append(start_id)
            start_id += 1
            road_unique_list.append(int(line['id'])-1)
            road_length_list.append(line['properties']['LENGTH'])

    df = pd.DataFrame({'net_id': point_unique_list, 'index': road_unique_list, 'geometry': geopoint_list, 'length': road_length_list})
    df = gpd.GeoDataFrame(df, geometry=[loads(wkt) for wkt in df['geometry']])
    if output:
        df.to_file('vertices.gpkg', driver='GPKG')
    return df

# get overlapping points (intersection points)
def get_intersection(df):
    df['X'] = df['geometry'].x
    df['Y'] = df['geometry'].y
    df = pd.DataFrame(df.groupby(['X', 'Y']).agg({'net_id': (lambda x: list(x.value_counts().index))}))
    intersection_list = df['net_id'].values
    return intersection_list

# select a representative point
def select_rep_point(df, inter_list, output=False):
    rep_point_list = []
    for i in inter_list:
        # take first point if it has some points
        rep_point_list.append(i[0])
    df = df.set_index('net_id').iloc[rep_point_list, :].reset_index()
    df = df[['net_id', 'index', 'geometry']]
    if output:
        df.to_file('rep_vertices.gpkg', driver='GPKG')
    return df

# get length between points
def get_length(df, inter_list):
    dic = {}
    for i in inter_list:
        for v in i:
            dic[v] = i[0]
    df['net_id'] = df['net_id'].apply(lambda x: dic[x])
    len_df = df[['net_id', 'index']]
    len_df = len_df.groupby('index').apply(lambda x: x['net_id'].reset_index(drop=True)).reset_index().rename(columns={0: 'start_id', 1: 'end_id'})
    df = df.drop_duplicates(subset=['index'])
    len_df = pd.merge(len_df, df[['index', 'length']], on='index', how='left')
    return len_df

# get adjacency matrix
def get_ad_matrix(df):
    node_num = df.shape[0] * 2
    INF = 10**5 - 1
    W = [[INF] * node_num for _ in range(node_num)]
    for i in range(df.shape[0]):
        W[df.loc[i, 'start_id']][df.loc[i, 'end_id']] = df.loc[1, 'length']
        W[df.loc[i, 'end_id']][df.loc[i, 'start_id']] = df.loc[1, 'length']
    return W

# get nearest points
def get_neareset_points(df):
    start_df = gpd.read_file('start_points.gpkg').rename(columns={'id': 'start_id'})
    goal_df = gpd.read_file('goal_points.gpkg').rename(columns={'id': 'goal_id'})
    start_nearest_points = _ckdnearest(start_df, df)[['start_id', 'net_id']]
    goal_nearest_points = _ckdnearest(goal_df, df)
    # remove points too far from road
    goal_nearest_points = goal_nearest_points[goal_nearest_points['dist']<0.003]
    goal_nearest_points = goal_nearest_points[['goal_id', 'net_id']].reset_index(drop=True)
    return start_nearest_points, goal_nearest_points