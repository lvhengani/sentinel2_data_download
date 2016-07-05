#!/usr/bin/python
import argparse
import os
import shutil
import json
import urllib2
import datetime
import config
'''
This script download sentinel 2 granule.
The word tile is used but in sentinel 2 reference this should be a granule and a tile has several granules.
Written by L M Vhengani
Date: 2016-03-22
Usage:
To run the script: 'python sentinel2_file_downloder.py 34/H/BH/2015/12/18/0/'
To print a help of the script: 'python sentinel2_file_downloder.py -h' or 'python sentinel2_file_downloder.py --help'
Make sure that the save_dir variable is set to the correct folder.
Future improvements include givign the string in a format 34HCJ-2016-02-06 for data to be downloaded.
'''

def process_tile_input_url(input_url_string):
    input_url_string=input_url_string.strip()
    
    if input_url_string.startswith('/'):
        input_url_string=input_url_string[1:]

    if input_url_string.endswith('/0/'):
        input_url_string=input_url_string[:-3]

    if input_url_string.endswith('/0'):
        input_url_string=input_url_string[:-2]

    if input_url_string.endswith('/'):
        input_url_string=input_url_string[:-1]        
         
    utm_num,utm_grid,granule,year,month,day=input_url_string.split('/')
    url_string = "{}/{}/{}/{}/{}/{}/0/".format(utm_num,utm_grid,granule,int(year),int(month),int(day))
    return utm_num,utm_grid,granule,year,month,day,url_string

def process_tile_id2_url(tile_id_string):
    tile_id_string=tile_id_string.strip()
    utm_gr,year,month,day = tile_id_string.split('-')
    utm_num=utm_gr[0:2].strip()
    utm_grid=utm_gr[2].strip()
    granule = utm_gr[3:].strip()
    url_string = "{}/{}/{}/{}/{}/{}/0/".format(utm_num,utm_grid,granule,int(year),int(month),int(day))
    return utm_num,utm_grid,granule,year,month,day,url_string

def process_tile_id_input(input_string):
    if '-' in input_string:
        utm_num,utm_grid,granule,year,month,day,url_string =process_tile_id2_url(input_string)
    elif '/' in input_string:
        utm_num,utm_grid,granule,year,month,day,url_string =process_tile_input_url(input_string)
    else:
        return None
    return utm_num,utm_grid,granule,year,month,day,url_string

def test_data_vailability(url,bands):
    for band in bands:
        ifile=os.path.join(url,band)
        try:
            urllib2.urlopen(ifile).code
        except urllib2.HTTPError,e:
            #print ifile, e.code
            print url, e.code
            return False
    return True

def get_s2_data(save_dir,tile_utm_zone,tile_id,formated_date,bands,url):

    os.system('cd {}'.format(save_dir))

    for band in bands:
        out_filename='S2_T{}{}_{}_{}'.format(tile_utm_zone,tile_id,formated_date,band)
        #print out_filename
        if band.endswith('.jp2'):
            t = 'wget {} --output-document={} -q'.format(os.path.join(url,band),os.path.join(save_dir,out_filename))
        else:
            t = 'wget {} -P {} -q'.format(os.path.join(url,band),save_dir)
        #print t
        os.system(t)

def get_tile_metadata(save_dir,productinfo_json_file):
    if os.path.exists(productinfo_json_file):    
        metadata_url = read_metadata(productinfo_json_file)
        get_metadata_str = 'wget {} -P {} -q'.format(metadata_url,save_dir)
        os.system(get_metadata_str)

def read_metadata(productinfo_json_file):
    ## get metadata
    base_url='http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com'
    # read the jason file
    
    with open(productinfo_json_file) as product_info:
        data=json.load(product_info)
    tile_path = data["path"]
    metadata_url = "{}/{}/{}".format(base_url,tile_path,'metadata.xml')
    return metadata_url 

parser=argparse.ArgumentParser()
parser.add_argument('tile_info',help='Enter sentinel 2 granule information in a format "34HCH-2016-02-06" or "/34/H/CH/2016/2/6/0/"')
parser.add_argument('-f','--force', default=False, action='store_true')

args=parser.parse_args()
tile_info_input=args.tile_info
force_download = args.force

utm_num,utm_grid,granule,year,month,day,tile_info=process_tile_id_input(tile_info_input)

formated_date = datetime.date(int(year),int(month),int(day)).strftime('%Y%m%d')

fld_name = '{}{}{}/S2_T{}{}{}_{}_L1C'.format(utm_num,utm_grid,granule,utm_num,utm_grid,granule,formated_date)

save_dir = os.path.join(config.save_l1c_dir,fld_name)    

# if the directroy exist do not download, except if its forced.
if os.path.exists(save_dir) and force_download:
    shutil.rmtree(save_dir)
try:
    os.makedirs(save_dir)
except:
    print 'data exist in the directory'
    exit()

base_url='http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/tiles'
url = os.path.join(base_url,tile_info)

bands = config.bands

wget_true = test_data_vailability(url,bands) # This will be true if all the bands are available

tile_utm_zone='{}{}'.format(utm_num,utm_grid)


if wget_true:
    print 'Getting level_1C sentinel 2 data from:\n{}'.format(url)        
    get_s2_data(save_dir,tile_utm_zone,granule,formated_date,bands,url)    
    productinfo_json_file = os.path.join(save_dir,'productInfo.json')
    get_tile_metadata(save_dir,productinfo_json_file)

else:
    print "There is an exception, with one or more of the files to download"
    shutil.rmtree(save_dir) # Do not leave an empty directory,delete it


