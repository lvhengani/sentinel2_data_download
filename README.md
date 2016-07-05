# Sentinel 2 data download tools
Tools for downloading sentinel 2 data. 
Using this tool, with a single click of a button, download a full sentinel 2 granule with metadata file of the scene.  

## Usage
When using this make sure that the saving directory save_l1c_dir is set to a valid path in the config.py file. 
To download using URL use the ```s2_file_downloader.py``` and to print usage information type: 


```
python s2_file_downloader.py -h

```

To run type.


```
python s2_file_downloader.py tile_info
-tile_info: is of the format '/utm_code/latitude_band/square/year/month/day/0/' or 'utm_codelatitude_bandsquare-year-month-day'  

```

## Example
Go to the site http://sentinel-pds.s3-website.eu-central-1.amazonaws.com/.
Scroll down to "Browse through data"
On the map, select the granule of interest. Once a granule is selected, you will see its ID in a format '36JUS-2016-07-03' for a tile on the North of Swaziland.
Copy the granule ID and give it as a commandline input as shown below. Please try to run without empty spaces.
```
python s2_file_downloader.py "/36/J/US/2016/7/3"
```
or
```
python s2_file_downloader.py "36JUS - 2016-07-03"
```
## Requirements
The script was written in python2.7 and only tested on an Ubuntu 14.04 system
In the configration (config.py) file, edit save_l1c_dir, to redirect the saved file elsewhere. Currently set to save in the Download folder.
  
 
