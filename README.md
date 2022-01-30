# IoTBenchmarkTool
Benchmarking tool for IoT environments

IoTDB-benchmark is a tool for benchmarking the edge device. It is capable of monitoring the resources through different load.
Measurements such as CPU, Memory, DiskI/O and Network.
Also, we take advantage of EMU-IoT-Gateway to generate the data from the Camera (simulating the real sensors).


Main Features:
-Easy to use: IoTDB-benchmark is a tool combined multiple testing functions so users 
do not need to switch different tools.
-Testing report and result: Supporting storing testing information and results
for further query or analysis.
Visualize results: Integration with Grafana to visualize the results.

We recommend using Linux or Raspbian systems.

Prerequisites of IoTBenchmarkTool
To use the tool, you need to have:

Linux 20
Raspberry PI 4

Installation requirements on Rpi:

-Docker
-Docker-compose

Instruction:
1.VM side:
Running the docker-compose file on the VM side to send the camera data to the Raspberry Pi.
- sudo docker-compose up
If you want to scale the number of cameras to try different load use:
-sudo docker-compose up --scale app=2
If you want to scale more than 200 sensors add this:
sudo COMPOSE_HTTP_TIMEOUT=3000 docker-compose up --scale app=200


2. Edge side:
2.1: Instalation Requirements:
-Install python
-Install docker 
-Install the Mosquitto in the container 
-Install the Telegraf in the container 
change the telegraf.conf:
# Configuration for sending metrics to InfluxDB
urls = ["IP of the Influxdb VM:Port"] --recommend 8086
database = "DBname"
skip_database_creation = true
## HTTP Basic Auth
  username = "telegraf"
  password = "telegraf"

2.2:Run docker-compose.yml file
-sudo docker-compose up

2.3:Monitoring
 -Change monitoring.py based on what you the changes on telegraf.conf

client = InfluxDBClient('Influxdb IP', Influxdb port, 'telegraf', 'telegraf', 'DBname')

 -Then run the monitoring.py on the edge to collect the measurements such as CPU, Memory, DiskI/O and Network
3.DB side
-Install influxdb
-you can connect the Influxdb to Grafana for visualizaton or convert the measurements to csv file

Note: after a set of experiments you have to reset the systems and dockers to remove the loads.
-sudo docker-compose down
-sudo service docker restart





