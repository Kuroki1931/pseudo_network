# pseudo_network
This code is for creating pseudo network!
We created both .py file and .ipynb file. You will utilize them depents on your tasks.
We prepared a simple task to learn how to use our code. If you want to know how to use it, please follow below.


# task example
## dataset preparation
In this task, we use nepal raod information as pseudo network.
download npl_rdsl_trans_25K_50K_sdn_wgs84.zip from https://data.humdata.org/dataset/nepal-road-network unser ./data/road dir.


## excute data_collection.py or data_collection.ipynb
In this file, you will get random target district road, goal points, and random start points.

### target district
We create target district because road information is heavyto use directoly. 

### random goal points
We create goal points information.  
![画像](/assets/goal_points.png)

### random start points
We change some goal points to start points. We will get the network info between start points and goal points.
![画像](/assets/start_points.png)


## run excute.py or excute.ipynb
