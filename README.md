# Sentinel 2 data download tools

Tools for downloading Sentinel-2 data and pre-processing to level-2A. 
Using this tool to download a full Sentinel-2 granule and also process it with sen2cor.
This tool was built using [sentinesat](https://sentinelsat.readthedocs.io) and [sen2cor](http://step.esa.int/main/third-party-plugins-2/sen2cor/).  

## Get the Repository

~~~
git clone https://github.com/lvhengani/sentinel2_data_download.git
~~~

## Configurartions

Create a `.env` file and write your own scihub username and password. Without the username and password you can`t download.
~~~
SCIHUBUSERNAME=your_scihubusername
SCIHUBPASSWORD=your_scihubpassword
~~~

## Build the Docker Image

~~~
./build
~~~

## Usage

~~~
./search_scihub [sdate] [edate] [--download] [--level2a] [--orbit]
~~~

## Example

~~~
./search_scihub 34HCH 20190601 20190627 -d -l2a
~~~


# To Do List

- Use ubuntu base image instead of python.3.6 image &#x2611;
- Update to sen2cor 2.8 &#x2611;
- Include a sqlite database
