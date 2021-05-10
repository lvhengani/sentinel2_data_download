#!/usr/bin/python
import os
import subprocess
import logging
import shutil
import argparse
import re
import config
import zipfile
import json
from datetime import date

"""
This script was generated for running in a docker container.
Author: L M Vhengani
Date: 2019-06-26
Purpose: Automatic processing of sen2cor version 2.5.5 on granules of interest.
Dependencies: It runs on Python 3
Inputs: It reads the s2granules.txt textfile with a list of granules of interest. The file must be in the same directory.
        On the commandline inputs include scene id (zipped) and the output spatial resolution of the output files. 
        The default output spatial resolution is 60, if not given as an input. 
Usage: python sen2cor_wrapper.py [scene] [-r] [-d]
"""

# Read granule information


def get_granule_info(granule):
    granule_info = dict()
    try:
        pattern = "(?P<sensor>.*)_(?P<class>.*)_(?P<category>.*)_(?P<level>.*)_(.*)_(.*)__(?P<cdate>.*)T(?P<ctime>.*)_(.*)_T(?P<granule>.*)_"
        m = re.match(pattern, granule, re.I)
        granule_info["sensor"] = m.group('sensor')
        granule_info["level"] = m.group('level')
        granule_info["acqdate"] = m.group('cdate')
        granule_info["acqtime"] = m.group('ctime')
        granule_info["utm_id"] = m.group('granule')
    except:
        pattern = "(?P<level>.*)_T(?P<granule>.*)_(.*)_"
        m = re.match(pattern, granule, re.I)
        granule_info["level"] = m.group('level')
        granule_info["utm_id"] = m.group('granule')

    return granule_info


def sen2cor(scene, resolution, delete_unzipped):
    level1c_path = config.level1c_path
    level2a_path = config.level2a_path
    unzipped_scenes = config.unzipped_scenes

    # Run sen2cor command
    run_sen2cor = "/Sen2Cor-02.09.00-Linux64/bin/L2A_Process"

    # Process each granule in a scene, which is a granule of interest
    zipped_scene_path = os.path.join(level1c_path, scene)
    unziped_scene = scene[:-3]+'SAFE'
    unziped_scene_path = os.path.join(unzipped_scenes, unziped_scene)

    # Unzip
    if os.path.exists(unziped_scene_path):
        shutil.rmtree(unziped_scene_path)

    with zipfile.ZipFile(zipped_scene_path, "r") as zip_ref:
        zip_ref.extractall(unzipped_scenes)

    # Run sen2cor, this depend on the mode
    if os.path.exists(unziped_scene_path):
        try:
            os.system('{} "{}" --resolution={} --output_dir={}'.format(run_sen2cor, unziped_scene_path,
                                                                       resolution, level2a_path))
            #print("Sen2Cor compeleted running {} at {}m spatial resolution".format(scene, resolution))
        except:
            print("Something went wrong while sen2cor was running %s" % scene)
    else:
        print("The unziped folder {} does not exists, check if unzip is working".format(
            unziped_scene))
        exit()

    # Assign all uniziped folderr to a user
    os.system("chown -R 1000 {}/*".format(level2a_path))

    if delete_unzipped:
        shutil.rmtree(unziped_scene_path)


if __name__ == "__main__":
    # Get user/ find commandline inputs
    description = """Atmospheric Corrections of Sentinel 2 granules"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'input_scene', help="The input scene which may have granules of interest without path")
    parser.add_argument(
        '-r', '--resolution', help="The output spatial resolution", default=config.resolution)
    parser.add_argument('-d', '--delete_unzipped',
                        help="Delete the unzipped level-1C scene", action="store_true")

    args = parser.parse_args()
    scene = args.input_scene
    resolution = args.resolution
    delete_unzipped = args.delete_unzipped

    sen2cor(scene, resolution, delete_unzipped)
