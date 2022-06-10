import geopandas as gpd
import pandas as pd
import numpy as np

from shapely.wkt import loads 
from shapely.geometry import Point, Polygon


# ramdom tap points
start_point = [83.9159, 28.2905]
end_point = [84.0289, 28.1873]
x = np.linspace(start_point[0], end_point[0], 20)
y = np.linspace(start_point[1], end_point[1], 20)
point_list = []
for i in x:
    for j in y:
        point_list.append(Point(i, j))
point_df = pd.DataFrame({'geometry': point_list}).reset_index().rename(columns={'index': 'id'})
point_df['geometry'] = point_df['geometry'].astype(str)
point_df = gpd.GeoDataFrame(point_df, geometry=[loads(wkt) for wkt in point_df['geometry']])
point_df.to_file('random_point.gpkg', driver='GPKG')

# ramdom source points
source_index = np.random.randint(0, 400, 5)
tap_df = point_df[~point_df['id'].isin(source_index)]
sor_df = point_df[point_df['id'].isin(source_index)]
tap_df.to_file('goal_points.gpkg', driver='GPKG')
sor_df.to_file('start_points.gpkg', driver='GPKG')

# traget district
# district = gpd.read_file(r'./data/district/hermes_NPL_new_wgs_3.shp')
# tar_dis = district[district['LOCAL'] == 'Pokhara Lekhnath']
# tar_dis.to_file('pokhara_district.gpkg', driver='GPKG')
polygon_geom = Polygon(zip([83.9158999999999935, 83.9158999999999935, 84.0288999999999930, 84.0288999999999930], [28.1873000000000005, 28.3057000000000016, 28.3057000000000016, 28.1873000000000005]))
tar_dis = gpd.GeoDataFrame(index=[0], geometry=[polygon_geom])
tar_dis.to_file('target_district.gpkg', driver='GPKG')

# road info
road = gpd.read_file(r'./data/road/npl_rdsl_trans_25K_50K_sdn_wgs84.shp')
road_clipped = gpd.clip(road, tar_dis)
road_clipped.to_file('target_road.gpkg', driver='GPKG')