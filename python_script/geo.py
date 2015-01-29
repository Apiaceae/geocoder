import os
from geopy import geocoders
from osgeo import ogr, osr

def geocode(address):
    g = geocoders.Google()
    place, (lat, lng) = g.geocode(address)
    print '%s: %.5f, %.5f' % (place, lat, lng)
    return place, lat, lng

def parse_file(filepath, output_shape):
    # create the shapefile
    drv = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(output_shape):
        drv.DeleteDataSource(output_shape)
    ds = drv.CreateDataSource(output_shape)
    # spatial reference
    sr = osr.SpatialReference()
    sr.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    lyr = ds.CreateLayer(output_shape, sr, ogr.wkbPoint)
    # fields
    featDefn = lyr.GetLayerDefn()
    fld_id = ogr.FieldDefn('id', ogr.OFTInteger)
    fld_address = ogr.FieldDefn('ADDRESS', ogr.OFTString)
    fld_address.SetWidth(255)
    lyr.CreateField(fld_id)
    lyr.CreateField(fld_address)
    print 'Shapefile %s created...' % ds.name
    # read text addresses file
    i = 0
    f = open(filepath, 'r')
    for address in f:
        try:
            print 'Geocoding %s' % address
            place, lat, lng = geocode(address)
            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint(0, lng, lat)
            feat = ogr.Feature(lyr.GetLayerDefn())
            feat.SetGeometry(point)
            feat.SetField('id', i)
            feat.SetField('ADDRESS', address)
            lyr.CreateFeature(feat)
            feat.Destroy()
            i = i + 1
        except:
            print 'Error, skipping address...'

parse_file('addresses_to_geocode', 'my_output')