import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'cases_hr.csv'
covid_data = pd.read_csv(file_path)

# Display the first few rows
covid_data.head()


# Load the new GeoJSON file (WGS84 format)
geojson_wgs84_file_path = 'hr_wgs84.geojson'

# Read the GeoJSON file using GeoPandas
gdf_wgs84 = gpd.read_file(geojson_wgs84_file_path)
# gdf_wgs84.set_crs(epsg=4326, inplace=True)

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
merged_cases_population.head()



# Convert 'hruid' to string in both datasets for consistent data type
gdf_projected_alternative['hruid'] = gdf_projected_alternative['hruid'].astype(str)
merged_cases_population['hruid'] = merged_cases_population['hruid'].astype(str)

# Merge the recalculated infection rates with the geographical data
merged_geo_population = pd.merge(gdf_projected_alternative, merged_cases_population, on='hruid', how='left')

# Create a map for Ontario with the updated infection rates and health region boundaries
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
merged_geo_population.plot(column='infection_rate', ax=ax, legend=True,
                            legend_kwds={'label': "Infection Rate (cases per population)", 'orientation': "horizontal", 'shrink': 0.7},
                            cmap='YlOrRd', edgecolor='black', linewidth=0.5)

# Set title and remove axes
ax.set_title('COVID-19 Infection Rates by Health Region')
ax.set_axis_off()

# Saving the plot with high DPI
save_path = 'irs.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()




on_geo_population = merged_geo_population[merged_geo_population['region_x'] == 'ON']

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
on_geo_population.plot(column='infection_rate', ax=ax, legend=True,
                            legend_kwds={'label': "Infection Rate (cases per population)", 'orientation': "horizontal", 'shrink': 0.5},
                            cmap='YlOrRd', edgecolor='black', linewidth=0.5)


ax.set_title('COVID-19 Infection Rates by Health Region in ON')
ax.set_axis_off()

save_path = 'irs_ON.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()




mb_geo_population = merged_geo_population[merged_geo_population['region_x'] == 'MB']

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
mb_geo_population.plot(column='infection_rate', ax=ax, legend=True,
                            legend_kwds={'label': "Infection Rate (cases per population)", 'orientation': "horizontal", 'shrink': 0.5},
                            cmap='YlOrRd', edgecolor='black', linewidth=0.5)


ax.set_title('COVID-19 Infection Rates by Health Region in MB')
ax.set_axis_off()

save_path = 'irs_MB.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()




bc_geo_population = merged_geo_population[merged_geo_population['region_x'] == 'BC']

fig, ax = plt.subplots(1, 1, figsize=(10, 8))
bc_geo_population.plot(column='infection_rate', ax=ax, legend=True,
                            legend_kwds={'label': "Infection Rate (cases per population)", 'orientation': "horizontal", 'shrink': 0.5},
                            cmap='YlOrRd', edgecolor='black', linewidth=0.5)


ax.set_title('COVID-19 Infection Rates by Health Region in BC')
ax.set_axis_off()

save_path = 'irs_BC.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()