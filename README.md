# pseudo_network
This code is for creating pseudo network! You can get the geo info between start points and goal points.
We created both .py file and .ipynb file. You will utilize them depending on your tasks.
We prepared a simple task example to learn how to use our code. If you want to know how to use it, please follow below.


# task example
## dataset preparation
In this task, you use nepal raod information as pseudo network.
Download npl_rdsl_trans_25K_50K_sdn_wgs84.zip from https://data.humdata.org/dataset/nepal-road-network unser ./data/road dir.  
![画像](/assets/road.png)

## run data_collection.py or data_collection.ipynb
This task imput are  
- start points geo data
- goal points  geo data
- network geo data
In this file, you will get the target district road data, ramdom start points data, and random goal points data for the task.

### target district raod
We create target district mesh because road information is heavy to use directoly. 
By using the target district mesh, the road info is clipped. You can change the polygon info in the code.
![画像](/assets/tar_road.png)
![画像](/assets/tar_road_dis.png)

### random goal points
We create goal points information.  
![画像](/assets/goal_points.png)

### random start points
We change some goal points to start points. We will get the network info between start points and goal points.
![画像](/assets/start_points.png)


## run excute.py or excute.ipynb
you will get the string and poing geo info.  
![画像](/assets/pseudo_network.png)
