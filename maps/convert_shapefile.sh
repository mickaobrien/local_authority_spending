ogr2ogr -f GeoJSON -t_srs EPSG:29902 local_authorities.geo.json Census2011_Admin_Counties_generalised20m.shp
topojson --id-property COUNTYNAME -p name=COUNTYNAME -p name -o local_authorities.topo.json local_authorities.geo.json
