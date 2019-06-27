import os
import datetime
import argparse
import sentinelsat_api as s2api
import sen2cor_wrapper as sen2cor 
import config

parser = argparse.ArgumentParser()
parser.add_argument('tileid', help="The identity (ID) of the tile i.e 34HCH")
parser.add_argument('sdate', help="The start date of the search in a form yyymmmdd, use date before scene acquisition")
parser.add_argument('edate', help="The end date of the search in a form yyymmmdd, use date after scene acquisition")
parser.add_argument('--download', '-d', help="Download the scene", action="store_true")
parser.add_argument('--level2a_proc', '-l2a', help="Process scene to level2A using sen2cor", action="store_true")
parser.add_argument('--clouds', '-cld', help="Maximum percent of clouds cover", default=config.cloudpcnt)
#parser.add_argument('--orbit', '-o', help="Relative orbit of the scene", default=None)

args = parser.parse_args()
tileid = args.tileid
sdate = args.sdate
edate = args.edate
download = args.download
level2a_proc = args.level2a_proc
#orbit = args.orbit

print(args)

# Search
username = config.scihub_username
password = config.scihub_password
cloudpcnt = config.cloudpcnt
level1c_path = config.level1c_path
unzipped_scenes = config.unzipped_scenes
resolution = config.resolution

# search
results = s2api.search(username, password, tileid, sdate, edate, cloudpcnt)
print(results)

# Download
for sceneid in results:
    print(sceneid, results[sceneid])
    relativeorbitnumber = results[sceneid]['relativeorbitnumber']
    scene_title = results[sceneid]["scene_title"]
    #orbit_flag = orbit == relativeorbitnumber

    if download:
        s2api.download(username, password, sceneid, level1c_path)
        scene_path  = os.path.join(level1c_path, scene)
        scene_exists = os.path.exists(scene_path)

        if level2a_proc and scene_exists:
            scene = "".join([scene_title, ".zip"])
            delete_unzipped = True                        
            sen2cor.sen2cor(scene, resolution, delete_unzipped)