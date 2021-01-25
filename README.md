# Dublin Buses Delay Prediction 
 Final Project of the Data Mangment and Gathering Lab 094290
 **Ben Filiarsky & Itzik Koyfman**
<p align='center'>
<img src=https://user-images.githubusercontent.com/74211354/105638890-fb00f900-5e7d-11eb-9042-6d9230babc37.jpg width=75% height=400px alt='Dublin Buses'></img>
</p>

## Overview
The app provides the city of Dublin a tool to assess the quality of ML models that predict the delay of a bus to its destination (the upcoming station). We use the delay as a proxy for the actual arrival time of the buses. Moreover, the tool can be used to provide routes between a source station and destination station, which is useful both for civilians and the city, which can use it as an route IR system.

## Technologies

* Processing framework - Apache Spark™.
<img src=https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Apache_Spark_logo.svg/1200px-Apache_Spark_logo.svg.png width=5% height=5% align='center' style="padding-bottom:6px" alt='Docker'></img>
* Data warehouse - Elasticsearch cluster.
<img src=https://www.elastic.co/static-res/images/elastic-logo-200.png width=4% height=4% align='center' padding-left=2% alt='Docker'></img>
* Docker - running Elasticsearch and Kibana on Ubuntu VMs.
<img src=https://pbs.twimg.com/profile_images/1273307847103635465/lfVWBmiW_400x400.png width=5% height=5% align='center' padding-left=2% alt='Docker'></img>

## Requirments

### Web App
* The app currently does not have a public domain.
* In order to run the app, Pyhton 3.7+ is required, please install the neccesary packages using 

    ```pip install -r requirement.txt```
* Run the app using ```python app.py```

### Processing Framework
* Processing is executed in the Databricks enviroment and requires Spark 2.4.5 (Pyspark).
* Run docker on your VM using the code and the configuration file (docker-compose.yml).

    ```sudo /opt/anaconda3/bin/docker-compose up -d```

## Usage

### Delay predictions assesmnet
A kibana dashboard depicting the average delay predicted by our model and comparing it to the real average delay in different regions of Dublin. It is possible to filter the following parameters:
* Time interval of the data. (using the kibana interface)
* Bus station ID. (Bus station filter)
* Bus Line ID. (Bus line filter)

### Route planning
Use this section in order to find shortest routes (both in distance and in number of lines) from source station to destination station. Choose source and destination, see their location on the Dublin map and see direct route (if exists) and shortest routes in L1 distance. Moreover, you will see the predicted delay of the line, based on a random initializtion of parameters and using a trained linear regression model.

<p align='center'>
 <img src=https://user-images.githubusercontent.com/74211354/105734001-d454c800-5f3a-11eb-8750-1021996d0039.png width=75% height=75% alt='Upload Data' href=''></img>
<p>

### Uploading Data
Can be found on the sidebar under 'Upload Data'. Use the buttons to upload stream/batch data to the databricks enviroment and Elasticsearch cluster.
<p align='center'>
 <img src=https://user-images.githubusercontent.com/74211354/105732945-ad49c680-5f39-11eb-966d-cd0efa322c93.png width=50% height=50% alt='Upload Data' href=''></img>
<p>
 
**Note!** the following schema will be enforced.

``` ['_id', 'delay', 'congestion', 'lineId', 'vehicleId', 'timestamp', 'areaId', 'areaId1', 'areaId2','areaId3', 'gridID', 'actualDelay', 'longitude', 'latitude', 'currentHour', 'dateTypeEnum', 'angle','ellapsedTime', 'vehicleSpeed', 'distanceCovered', 'journeyPatternId', 'direction', 'busStop','poiId', 'poiId2', 'systemTimestamp', 'calendar', 'filteredActualDelay', 'atStop', 'dateType', 'justStopped', 'justLeftStop', 'probability', 'anomaly', 'loc'] ```
