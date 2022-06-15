import os

import geopandas as gpd
import numpy as np
import pandas as pd
from absl import app
from absl import flags
from shapely.wkt import loads 
from shapely.geometry import Point, Polygon


FLAGS = flags.FLAGS
flags.DEFINE_string('basedir', '../..', 'basedir.')
flags.DEFINE_integer('points_longitude', 10, 'number of points in longitude direction')
flags.DEFINE_integer('points_latitude', 10, 'number of points in latitude direction')
flags.DEFINE_integer('source_points', 5, 'number of source points')


def main(unused_argv):
    output_dir = os.path.join(FLAGS.basedir, 'data')
    os.makedirs(output_dir, exist_ok=True)
    input_dir = os.path.join(FLAGS.basedir, 'data')
    # tap create area (latitude, longitude)
    start_point = [83.9159, 28.2905]
    end_point = [84.0289, 28.1873]
    # target district area
    polygon_geom = Polygon(zip([83.9158999999999935, 83.9158999999999935, 84.0288999999999930, 84.0288999999999930], [28.1873000000000005, 28.3057000000000016, 28.3057000000000016, 28.1873000000000005]))

    # ramdom tap points
    x = np.linspace(start_point[0], end_point[0], FLAGS.points_longitude)
    y = np.linspace(start_point[1], end_point[1], FLAGS.points_latitude)
    point_list = []
    for i in x:
        for j in y:
            point_list.append(Point(i, j))
    point_df = pd.DataFrame({'geometry': point_list}).reset_index().rename(columns={'index': 'id'})
    point_df['geometry'] = point_df['geometry'].astype(str)
    point_df = gpd.GeoDataFrame(point_df, geometry=[loads(wkt) for wkt in point_df['geometry']])
    point_df.to_file(f'{output_dir}/random_point.gpkg', driver='GPKG')

    # ramdom source points
    source_index = np.random.randint(0, FLAGS.points_longitude*FLAGS.points_latitude, FLAGS.source_points)
    tap_df = point_df[~point_df['id'].isin(source_index)]
    sor_df = point_df[point_df['id'].isin(source_index)]
    tap_df.to_file(f'{output_dir}/goal_points.gpkg', driver='GPKG')
    sor_df.to_file(f'{output_dir}/start_points.gpkg', driver='GPKG')

    # traget district
    tar_dis = gpd.GeoDataFrame(index=[0], geometry=[polygon_geom])
    tar_dis.to_file(f'{output_dir}/target_district.gpkg', driver='GPKG')

    # road info
    road = gpd.read_file(f'{input_dir}/road/npl_rdsl_trans_25K_50K_sdn_wgs84.shp')
    road_clipped = gpd.clip(road, tar_dis)
    road_clipped.to_file(f'{output_dir}/target_road.gpkg', driver='GPKG')


if __name__ == '__main__':
    app.run(main)