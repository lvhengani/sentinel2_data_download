import os
from collections import OrderedDict
from sentinelsat import SentinelAPI

"""
This is a wrapper to the sentinelsat api.
"""

def download(username, password, scene_id, directory_path, url=None):
    """A function for downloading scenes from Scihub with an API"""
    # connect to the API
    if url is None:
        api = SentinelAPI(username, password, api_url='https://apihub.copernicus.eu/apihub')
    else:
        api = SentinelAPI(username, password, api_url=url)
        
    api.download(scene_id, directory_path, True)


def search(username, password, tile_name, date1, date2, cloudpcnt, url=None):
    """A function for searching the Scihub API"""
    results = {}
    # connect to the API
    if url is None:
        api = SentinelAPI(username, password, api_url='https://apihub.copernicus.eu/apihub')
    else:
        api = SentinelAPI(username, password, api_url=url)

    # search by tileid, date and other SciHub query keywords   
    products = api.query(tileid=tile_name,
                         date = (date1, date2),
                         platformname='Sentinel-2',
                         producttype = 'S2MSI1C',
                         cloudcoverpercentage=(0, cloudpcnt))


    for iproduct in products:
        iproduct_metadata = api.get_product_odata(iproduct, full=True)
        scene_id = iproduct.strip()
        results[scene_id] = {'scene_title':iproduct_metadata['title'],
                             'ingestiondate':iproduct_metadata['Ingestion Date'],
                             'acquisitiondate':iproduct_metadata['Sensing start'],
                             'relativeorbitnumber':iproduct_metadata['Relative orbit (start)'],
                             'tileid': iproduct_metadata['Tile Identifier'],
                             'footprint':iproduct_metadata['footprint']
                             }
    
    return results

def test_scihub_connection(username, password, url=None):
    """Test connection"""
    # connect to the API
    if url is None:
        api = SentinelAPI(username, password, api_url='https://apihub.copernicus.eu/apihub')
    else:
        api = SentinelAPI(username, password, api_url=url)

    print(api.api_url)
    #print(dir(api))
    #print(api.dhus_version)

    
if __name__ == "__main__":
    test_scihub_connection(os.getenv("DHUS_USER"), os.getenv("DHUS_PASSWORD"))