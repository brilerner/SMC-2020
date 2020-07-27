Road Network

Roads are segmented into so-called Links, which are sections of the road with similar properties, e.g. speed limit, paving type, number of lanes, etc. Each Link is a LineString, which consists of one or multiple line segments, and it has a unique LINKID.

The road network is provided in two different formats:

- As GeoJSON format (can be read using json library)

- As ESRI shapefile (can be read using GDAL library, imported in QGIS/ArcGIS, etc)
