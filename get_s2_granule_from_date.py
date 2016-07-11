#!usr/bin/python
import argparse
import os
import shutil
import json
import urllib2
import datetime

"""
This utility will get all sentinel data from a given day to today or to specific end date.
The user is supposed to give the from date and tile info in a for 34HCH, 34HEH and so forth.
Usage: python get_s2_granule.py [-h] [--start_date START_DATE] [--end_date END_DATE] granule
This utility depends on the python s2_file_downloader_v2.py utility.
Wriiten by: L M Vhengani
Date: 31 March 2016
"""


def convert_input2date(input_date):
    in_year,in_month,in_day = input_date.split('-')
    input_date =datetime.date(int(in_year),int(in_month),int(in_day))
    return input_date
    
parser=argparse.ArgumentParser()
parser.add_argument('granule',help='Enter sentinel 2 granule information in a format "34HCH"')
parser.add_argument('--start_date', help='Enter date to start searching for sentinel 2 granule')
parser.add_argument('--end_date',default=datetime.date.today(),
                    help='Enter date to stop searching for sentinel 2 granule,if not entered current date will be used')


args=parser.parse_args()
granule=args.granule
start_date = args.start_date
end_date = args.end_date

formated_start_date=convert_input2date(start_date)

if end_date!=datetime.date.today():
    formated_end_date= convert_input2date(end_date)
else:
    formated_end_date = datetime.date.today()
    

while formated_start_date<=formated_end_date:
    tile_input_info='{} - {}'.format(granule,formated_start_date)
    get_date_str='python s2_file_downloader.py "{}"'.format(tile_input_info)
    #print get_date_str
    os.system(get_date_str)
    formated_start_date=formated_start_date+datetime.timedelta(days=1)
    
