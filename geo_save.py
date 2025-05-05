import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset to examine its contents
file_path = 'cases_hr.csv'
covid_data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
covid_data.head()


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

    # Calculate the area for each health region (in square meters)
    gdf_projected_alternative['area_sqm'] = gdf_projected_alternative['geometry'].area

    # Display the first few rows with the new area column
    area_data = gdf_projected_alternative[['region', 'hruid', 'name_canonical', 'area_sqm']].head()
except Exception as e:
    area_data = str(e)

print(area_data)







# Aggregate the total COVID-19 cases for each health region
total_cases_per_hr = covid_data.groupby('sub_region_1')['value_daily'].sum().reset_index()

# Rename the columns for clarity and for merging
total_cases_per_hr.columns = ['hruid', 'total_cases']

# Display the first few rows of the aggregated total cases
print(total_cases_per_hr.head())




# Load the population data
population_file_path = 'hr.csv'
population_data = pd.read_csv(population_file_path)

# Display the first few rows of the population data
population_data.head()



# Convert 'hruid' to string in the population data for consistent data type
population_data['hruid'] = population_data['hruid'].astype(str)
total_cases_per_hr['hruid'] = total_cases_per_hr['hruid'].astype(str)

# Merge the total cases data with the population data
merged_cases_population = pd.merge(total_cases_per_hr, population_data, on='hruid', how='left')

# Recalculate the infection rate (cases per population)
merged_cases_population['infection_rate'] = merged_cases_population['total_cases'] / merged_cases_population['pop']

# Display the first few rows of the merged data with the recalculated infection rate
print(merged_cases_population.head())



# Convert 'hruid' to string in both datasets for consistent data type
gdf_projected_alternative['hruid'] = gdf_projected_alternative['hruid'].astype(str)
merged_cases_population['hruid'] = merged_cases_population['hruid'].astype(str)

# Merge the recalculated infection rates with the geographical data
merged_geo_population = pd.merge(gdf_projected_alternative, merged_cases_population, on='hruid', how='left')

# Filter the data for only Ontario regions
print(merged_geo_population.head())

merged_geo_population['pop_density'] = merged_geo_population['pop'] / merged_geo_population['area_sqm']
test_data = merged_geo_population[['region_x', 'hruid', 'pop_density', 'infection_rate']].head()

print(test_data)


merged_geo_population = merged_geo_population[merged_geo_population['region_x'] == 'QC']


print(type(merged_geo_population))


fig, ax1 = plt.subplots(figsize=(15, 12))
font_size = 22
# Plotting daily cases
color = 'tab:blue'
ax1.set_xlabel('Population Density(population per sqm)', fontsize=font_size)
ax1.set_ylabel('Infection Rate(cases per population)', fontsize=font_size)
ax1.scatter(merged_geo_population['pop_density'], merged_geo_population['infection_rate'], color=color, s=100)
ax1.tick_params(axis='both', labelsize=font_size-2)

# Adding title and grid
plt.title('COVID-19 Infection Rates and Population Density of Health Regions in QC', fontsize=font_size+3)
plt.grid(True)

fig.tight_layout()  # to ensure the right y-label is not clipped

save_path = 'ir_pd_QC.png'
plt.savefig(save_path, dpi=300)

plt.show()




