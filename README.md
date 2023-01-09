# Predicting the Presence of E. coli in Tap Water Using Machine Learning in Nepal

# pseudo_network
This code is for creating a pseudo network! You can get the geo info between start points and goal points.  
We created both .py file and .ipynb file. You will utilize them depending on your tasks.  
We prepared a simple task example to learn how to use our code. If you want to know how to use it, please follow below.  


# task example
## dataset preparation
In this task example, you will use Nepal raod information as the pseudo network.  
Download npl_rdsl_trans_25K_50K_sdn_wgs84.zip from https://data.humdata.org/dataset/nepal-road-network and put it under ./data/road.  
![画像](/assets/road.png)

## execute data_collection.py
### setting
1. Set the norht west latitude and longitude coordinates as start_point, and the source east one as end_point.  
2. If you just want random goal points, set source_points as 0.  
3. In this file, you will get the target district road data, random start points data, and random goal points data for the task.

### target district raod
Acoording to the stat_point and end_point you set, a target_district road will be clipped from the whole road information.
By using the target district mesh, the road info is clipped.
![画像](/assets/tar_road.png)
![画像](/assets/tar_road_dis.png)

### random goal points
You will get the goal points info.  
![画像](/assets/goal_points.png)

### random start points
Some goal points are changed to start points.  
![画像](/assets/start_points.png)


## execute run.py
1. If you want to use your own start points, you will change start_points.gpkg to yours.  
2. you will get the shortest string geo data between goal points and starts points.  

![画像](/assets/pseudo_network.png)
