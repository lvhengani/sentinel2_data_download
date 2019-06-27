import os

# Scihub authentication 
scihub_username = os.environ["SCIHUBUSERNAME"]
scihub_password = os.environ["SCIHUBPASSWORD"]

# paths and logfiles
loglife = os.path.join("/var/logs","sentinel_download_log.log")
level1c_path = os.path.join("/var/sentinel_data", 'level1c')
level2a_path = os.path.join("/var/sentinel_data", 'level2a')
unzipped_scenes = os.path.join("/var/sentinel_data", "unzipped")

# default resolution when running sen2cor
resolution = 20

# maximum cloud threshod when searching for scenes
cloudpcnt = 20