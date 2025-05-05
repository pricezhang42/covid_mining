import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the new GeoJSON file (WGS84 format)
geojson_wgs84_file_path = 'hr_wgs84.geojson'

# Read the GeoJSON file using GeoPandas
gdf_wgs84 = gpd.read_file(geojson_wgs84_file_path)
# gdf_wgs84.set_crs(epsg=4326, inplace=True)

# Display the first few rows to confirm successful loading and to understand its structure
gdf_wgs84.head()

# Alternative projection - using a widely recognized North American Albers Equal Area projection
albers_projection_alternative = "EPSG:5070"  # North American Albers Equal Area

# Attempt to reproject the GeoDataFrame
try:
    gdf_projected_alternative = gdf_wgs84.to_crs(albers_projection_alternative)

except Exception as e:
    print(e)



# Create a basic map of health regions in Canada
fig, ax = plt.subplots(1, 1, figsize=(15, 10))
gdf_projected_alternative.plot(ax=ax, edgecolor='black', color='lightgrey')

# Set title and remove axes
ax.set_title('Health Regions in Canada')
ax.set_axis_off()

plt.show()
