# pseudo_network
This code is for creating a pseudo network! You can get the geo info between start points and goal points.
We created both .py file and .ipynb file. You will utilize them depending on your tasks.
We prepared a simple task example to learn how to use our code. If you want to know how to use it, please follow below.


# task example
## dataset preparation
In this task, you use Nepal raod information as the pseudo network.
Download npl_rdsl_trans_25K_50K_sdn_wgs84.zip from https://data.humdata.org/dataset/nepal-road-network unser ./data/road dir.  
![画像](/assets/road.png)

## run data_collection.py or data_collection.ipynb
This task input are  
- start points geo data
- goal points  geo data
- network geo data  
In this file, you will get the target district road data, random start points data, and random goal points data for the task.

### target district raod
The road information is heavy to use directory, so the target district mesh is required first.
By using the target district mesh, the road info is clipped.
![画像](/assets/tar_road.png)
![画像](/assets/tar_road_dis.png)

### random goal points
You will get the goal points info.  
![画像](/assets/goal_points.png)

### random start points
Some goal points are changed to start points.  
![画像](/assets/start_points.png)


## run run.py or run.ipynb
you will get the shortest string geo data between goal points and starts points.  
This task removes goal points that are too far from the road.
![画像](/assets/pseudo_network.png)

# License
MIT
