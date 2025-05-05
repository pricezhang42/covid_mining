import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and display the first few rows of the first file
file_path_health_regions = 'Health Region with Peer Group - Copy.csv'
health_regions_data = pd.read_csv(file_path_health_regions)
health_regions_data.head()

# Load and display the first few rows of the second file
file_path_infection_rates = 'infection_rate_hr.csv'
infection_rates_data = pd.read_csv(file_path_infection_rates)
infection_rates_data.head()

# Merge the datasets on health region ID (assuming 'Health Region ID' corresponds to 'hruid')
merged_data = pd.merge(health_regions_data, infection_rates_data, left_on='Health Region ID', right_on='hruid')

# Display the first few rows of the merged dataset
merged_data.head()





# Setting up the plot
plt.figure(figsize=(12, 8))

# Scatter plot with infection rate on the x-axis and health region ID on the y-axis
# Different colors for different peer groups
sns.scatterplot(data=merged_data, x='infection_rate', y='region_x', hue='Peer Group', style='Peer Group')

# Adding labels and title
plt.xlabel('Infection Rate')
plt.ylabel('Province')
plt.title('Infection Rate by Health Region and Peer Group')
plt.grid(False)
plt.legend(title='Peer Group')


save_path = 'peer.png'
plt.savefig(save_path, dpi=300)
# Show the plot
plt.show()
