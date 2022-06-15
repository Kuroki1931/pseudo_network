import os

import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import tqdm
from absl import app
from absl import flags

import func


FLAGS = flags.FLAGS
flags.DEFINE_string('basedir', '../..', 'basedir.')


def main(unused_argv):
    output_dir = os.path.join(FLAGS.basedir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    input_dir = os.path.join(FLAGS.basedir, 'data')

    vertices = func.get_vertices(input_dir)
    intersection_list = func.get_intersection(vertices)
    rep_vertices = func.select_rep_point(vertices, intersection_list)
    len_df = func.get_length(vertices, intersection_list)
    df_matrix = func.get_ad_matrix(len_df)
    start_df = gpd.read_file(f'{input_dir}/start_points.gpkg').rename(columns={'id': 'start_id'})
    goal_df = gpd.read_file(f'{input_dir}/goal_points.gpkg').rename(columns={'id': 'goal_id'})
    start_nearest_points, goal_nearest_points = func.get_neareset_points(rep_vertices, start_df, goal_df)
    data = np.array(df_matrix)
    G=nx.from_numpy_matrix(data)

    # extract nearest start points
    goal_id_list = []
    nearest_len_list = []
    nearest_point_list = []
    start_id_list = []
    for i in tqdm.tqdm(range(goal_nearest_points.shape[0])):
        goal_id_list.append(goal_nearest_points.loc[i, 'net_id'])
        goal_id = goal_nearest_points.loc[i, 'net_id']
        len_list = []
        point_list = []
        start_ids_list = []
        for j in range(start_nearest_points.shape[0]):
            start_ids_list.append(start_nearest_points.loc[j, 'net_id'])
            start_id = start_nearest_points.loc[j, 'net_id']
            nearest_point = nx.shortest_path(G, source=goal_id, target=start_id, weight='weight')
            nearest_len = nx.shortest_path_length(G, source=goal_id, target=start_id, weight='weight')
            len_list.append(nearest_len)
            point_list.append(nearest_point)
        min_len_index = len_list.index(min(len_list))
        nearest_len_list.append(len_list[min_len_index])
        nearest_point_list.append(point_list[min_len_index])
        start_id_list.append(start_ids_list[min_len_index])
    output = pd.DataFrame({'goal_id': goal_id_list, 'start_id': start_id_list, 'length': nearest_len_list, 'point_list': nearest_point_list})
    output = output[output['length']!=10**5 - 1].reset_index(drop=True)
    output.to_csv(f'{input_dir}/network.csv')


    # extract point and string geo data
    os.makedirs(output_dir, exist_ok=True)
    road = gpd.read_file(f'{input_dir}/target_road.gpkg').reset_index()
    set_list = []
    for i in range(len_df.shape[0]):
        b = {len_df.loc[i, 'start_id'], len_df.loc[i, 'end_id']}
        set_list.append(b)
    for i in range(output.shape[0]):
        # point
        point_list = output.loc[i, 'point_list']
        goal_id = output.loc[i, 'goal_id']
        nearest_point_info = rep_vertices.set_index('net_id').loc[point_list, :].reset_index()[['net_id', 'index', 'geometry']]
        nearest_point_info.to_file(f'{input_dir}/unite_point{goal_id}.gpkg', driver='GPKG')
        
        # string
        index_list = []
        for j in range(len(point_list)-1):
            a = {point_list[j], point_list[j+1]}
            for k in range(len(set_list)):
                if set_list[k] == a:
                    index_list.append(k) 
        road_index_list = len_df.loc[index_list, 'index'].values
        road_info = road[road['index'].isin(road_index_list)][['index', 'LENGTH', 'geometry']]
        try:
            road_info.to_file(f'{input_dir}/road_info{goal_id}.gpkg', driver='GPKG')
        except:
            nearest_point_info.to_file(f'{input_dir}/road_info{goal_id}.gpkg', driver='GPKG')


if __name__ == '__main__':
    app.run(main)

