import os

'''
A configuration file used by sentinel 2 download tools
'''
save_l1c_dir= os.path.expanduser("~/Downloads")

granules={'34':['HBH','HBJ','HBK','HCK','HCJ','HCH','HCG','HDJ','HDH','HDG','HEJ','HEH'],'35':['JML','JPL','JMM','JNM'],'36':['JUS','JUT','KUU']}

bands=['B01.jp2','B02.jp2','B03.jp2','B04.jp2','B05.jp2','B06.jp2','B07.jp2',
       'B08.jp2','B8A.jp2','B09.jp2','B10.jp2','B11.jp2','B12.jp2','productInfo.json','tileInfo.json']

loglife = os.path.join(save_l1c_dir,'log')
