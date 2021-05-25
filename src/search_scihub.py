import os
import sys
import argparse
import datetime
import logging
from sentinelsat_wrapper import SentinelSatWrapper
from sen2cor_wrapper import Sen2Cor 
#from satellite_tasking import SentinelSatWrapper, Sen2Cor, Sentinel2Products

def search_scihub(sdate, edate, tileid, aoi, download, level2a_proc, cloudpcnt=20, resolution=20):
    "Search Scihub, download and convert to Leve-2A depending on options"
    # Search
    sentinel_data_path = "/var/sentinel2_data"
    username = os.getenv("DHUS_USER")
    password = os.getenv("DHUS_PASSWORD")
    level1c_path = os.path.join(sentinel_data_path, "level1c")
    level2a_path = os.path.join(sentinel_data_path, "level2a")
    unzipped_scenes = os.path.join(sentinel_data_path, "unzipped")
    products_path = os.path.join(sentinel_data_path, "products")

    logging.info("Search started")

    # search
    s2api = SentinelSatWrapper(username, password)

    if tileid is not None:
        results = s2api.search_by_tile(tileid, sdate, edate, cloudpcnt)
    elif aoi is not None:
        results = s2api.search_by_aoi(aoi, sdate, edate, cloudpcnt)
    else:
        logging.error("Either the aoi or tileid is required")
        exit()

    logging.debug(f"Search found products {results}")

    # Create the required paths
    logging.info("Check if downloads, unzipped and level2a paths exists")
    s2_paths = [level1c_path, level2a_path, unzipped_scenes, products_path]
    for ipath in s2_paths:
        if not os.path.exists(ipath):
            logging.info(f"Creating path {ipath}")
            os.makedirs(ipath)

    # Download
    for sceneid in results:
        relativeorbitnumber = results[sceneid]['relativeorbitnumber']
        scene_title = results[sceneid]["scene_title"]
        #orbit_flag = orbit == relativeorbitnumber

        if download:
            logging.info("Downloading products")
            s2api.download(sceneid, level1c_path)
            scene = "".join([scene_title, ".zip"])
            scene_path  = os.path.join(level1c_path, scene)
            scene_exists = os.path.exists(scene_path)
            logging.info("Downloading completed")

            if level2a_proc and scene_exists:
                logging.info("Converting products to level-2")
                delete_unzipped = True
                sen2cor = Sen2Cor(scene, resolution, delete_unzipped)
                sen2cor.convert_to_l2a()
                logging.info("Sen2Cor completed")

    # Generate products

    logging.info("Done!!")

def main(sdate, edate, tileid, aoi, download, level2a_proc, clouds=20, loglevel="DEBUG"):

    logging.basicConfig(stream=sys.stdout,
        format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d %(funcName)s() %(message)s',
        level=getattr(logging, loglevel))

    search_scihub(sdate, edate, tileid, aoi, download, level2a_proc, cloudpcnt=clouds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('sdate', help="The start date of the search in a form yyyymmdd, use date before scene acquisition")
    parser.add_argument('edate', help="The end date of the search in a form yyyymmdd, use date after scene acquisition")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tileid', '-t',help="The identity (ID) of the tile i.e 34HCH")
    group.add_argument('--aoi', '-aoi', help="The area of intersest in wkt format")
    parser.add_argument('--download', '-d', help="Download the scene", action="store_true")
    parser.add_argument('--level2a_proc', '-l2a', help="Process scene to level2A using sen2cor", action="store_true")
    parser.add_argument('--clouds', '-cld', help="Maximum percent of clouds cover", default=20)
    parser.add_argument('--loglevel', '-ll', help="Log level for this application", default="INFO")

    args = parser.parse_args()
    sdate = args.sdate
    edate = args.edate
    tileid = args.tileid
    aoi = args.aoi
    clouds = args.clouds
    download = args.download
    level2a_proc = args.level2a_proc
    loglevel = args.loglevel

    main(sdate, edate, tileid, aoi, download, level2a_proc, clouds=clouds, loglevel=loglevel.upper())
