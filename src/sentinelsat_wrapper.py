import os
from collections import OrderedDict
import logging
from sentinelsat import SentinelAPI

class SentinelSatWrapper:
    def __init__(self, username, password, url='https://apihub.copernicus.eu/apihub'):
        self.username = username
        self.password = password
        self.url = url
        self.api = SentinelAPI(username, password, api_url=self.url)
        logging.info(f"Search data from {self.url}")

    def filter_metadata_info(self, products):
        results = {}
        for iproduct in products:
            iproduct_metadata = self.api.get_product_odata(iproduct, full=True)
            scene_id = iproduct.strip()
            
            results[scene_id] = {'scene_title':iproduct_metadata['title'],
                                'ingestiondate':iproduct_metadata['Ingestion Date'],
                                'acquisitiondate':iproduct_metadata['Sensing start'],
                                'relativeorbitnumber':iproduct_metadata['Relative orbit (start)'],
                                'tileid': iproduct_metadata['Tile Identifier'],
                                'footprint':iproduct_metadata['footprint']
                                }
    
        return results

    def search_by_tile(self, tile_name, date1, date2, cloudpcnt):
        """search by tileid, date and other SciHub query keywords"""
        logging.info(f"Search data by tileid {tile_name}")
        products = self.api.query(tileid=tile_name,
                                  date=(date1, date2),
                                  platformname='Sentinel-2',
                                  producttype='S2MSI1C',
                                  cloudcoverpercentage=(0, cloudpcnt))
        
        results = self.filter_metadata_info(products)
        return results

    def search_by_aoi(self, wkt_footprint, date1, date2, cloudpcnt):
        "search data by wkt footprint and other SciHub query keywords"
        products = self.api.query(wkt_footprint,
                                  date=(date1, date2),
                                  platformname='Sentinel-2',
                                  producttype='S2MSI1C',
                                  cloudcoverpercentage=(0, cloudpcnt))
        
        results = self.filter_metadata_info(products)
        
        return results

    def download(self, scene_id, directory_path):
        self.api.download(scene_id, directory_path, True)

if __name__ == "__main__":
    s2 = SentinelSatWrapper(os.getenv('DHUS_USER'), os.getenv('DHUS_PASSWORD'))
    results = s2.search_by_tile('34HCH', '20210401', '20210430', 20) 
    #wkt = 'POLYGON((18.84897620825523 -33.42037795506848,20.029650964642173 -33.43523769197612,20.018355218855746 -34.42538216019411,18.82395539904375 -34.409960850871684,18.84897620825523 -33.42037795506848))'
    #results = s2.search_by_aoi(wkt, '20210401', '20210430', 20)
    print(results)