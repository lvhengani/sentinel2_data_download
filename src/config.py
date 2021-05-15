import os

# Scihub authentication 
scihub_username = os.getenv("DHUS_USER")
scihub_password = os.getenv("DHUS_PASSWORD")

# paths and logfiles
loglife = os.path.join("/var/logs","sentinel_download_log.log")
level1c_path = os.path.join("/var/sentinel_data", 'level1c')
level2a_path = os.path.join("/var/sentinel_data", 'level2a')
unzipped_scenes = os.path.join("/var/sentinel_data", "unzipped")

# default resolution when running sen2cor
resolution = 20 # 10, 60

# maximum cloud threshold when searching for scenes
cloudpcnt = 20 # min 0 and max 100

# API endpoint
endpoint = 'https://apihub.copernicus.eu/apihub'