# Sentinel 2 data download tools

This is utility for downloading Sentinel-2 data and pre-processing to level-2A. 
Using this tool to download a full Sentinel-2 scene and also process it with sen2cor.
This is a docker-based tool developed using [sentinesat](https://sentinelsat.readthedocs.io) and [sen2cor](http://step.esa.int/main/third-party-plugins-2/sen2cor/).

## Get the Repository

Clone the repository into your machine using the command below:

~~~
git clone https://github.com/lvhengani/sentinel2_data_download.git
~~~

## Configurartions

Create a `.env` file and write your own [scihub](http://scihub.copernicus.eu) username and password. Without the username and password you can`t download.
~~~
DHUS_USER=your_scihubusername
DHUS_PASSWORD=your_scihubpassword
~~~

Inside the `sentinel_data` directory there are subdirectories `level1c` and `level2c`, files are downloaded into the former and sen2cor pre-processed data is stored into the  later. 

## Build the Docker Image

First build the image using the command below:

~~~
./build
~~~

This may take time. To build the image make sure you have the latest version of Docker and Docker-compose installed in your machine.

## Usage

To search for a scene use and command below:

~~~
./search_scihub [-h] [--download] [--level2a_proc] [--clouds CLOUDS] tileid sdate edate
~~~

You can test using examples below:

### Example 1

Search a scene with tileid 34HCH, acquired between dates 2019-06-01 and 2019-06-27, with cloud cover percentage less than 20%, download it and process it to level-2A.

~~~
./search_scihub 34HCH 20190601 20190627 --download -level2a_proc --clouds 20
~~~

### Example 2

Search a scene with tileid 34JTT, acquired between dates 2018-09-01 and 2019-09-05, download it and process it to level-2A.

~~~
./search_scihub 36JTT 20180903 20180905 -d -l2a
~~~


# To Do List

- Use ubuntu base image instead of python.3.6 image &#x2611;
- Update to sen2cor 2.8 &#x2611;
- Include a sqlite database for registering all downloaded files and for controlling the process chain
