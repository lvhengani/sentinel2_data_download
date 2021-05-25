import ee

ee.Authenticate()
ee.Initialize()

dem = ee.Image('USGS/SRTMGL1_003')

xy = ee.Geometry.Point([86.9250, 27.9881])

elev = dem.sample(xy, 30).first().get('elevation').getInfo()

#url = dem.updateMask(dem.gt(0)).getThumbURL({'min': 0, 'max': 4000, 'dimensions': 512,
#                'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']})

data = dem.gt(0)

print(dir(data))