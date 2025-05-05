import matplotlib.pyplot as plt
import pandas as pd

# Load the datasets
cases_file_path = 'cases_can.csv'
hospitalizations_file_path = 'hospitalizations_can.csv'

# Reading the data
cases_data = pd.read_csv(cases_file_path)
hospitalizations_data = pd.read_csv(hospitalizations_file_path)

# Displaying the first few rows of each dataset for inspection
cases_data.head(), hospitalizations_data.head()
# Selecting relevant columns
cases_daily = cases_data[['date', 'value_daily']].copy()
hospitalizations_daily = hospitalizations_data[['date', 'value_daily']].copy()

# Renaming columns for clarity
cases_daily.rename(columns={'value_daily': 'daily_cases'}, inplace=True)
hospitalizations_daily.rename(columns={'value_daily': 'daily_hospitalizations'}, inplace=True)

# Merging the datasets on the date column
combined_data = pd.merge(cases_daily, hospitalizations_daily, on='date', how='outer')

# Sorting by date
combined_data['date'] = pd.to_datetime(combined_data['date'])
combined_data.sort_values(by='date', inplace=True)





fig, ax1 = plt.subplots(figsize=(15, 11))

# Plotting daily cases
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Daily Cases', color=color)
ax1.plot(combined_data['date'], combined_data['daily_cases'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Creating a second y-axis for hospitalizations
ax2 = ax1.twinx() 
color = 'tab:red'
ax2.set_ylabel('Daily Hospitalizations', color=color)
ax2.plot(combined_data['date'], combined_data['daily_hospitalizations'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Adding title and grid
plt.title('Daily COVID-19 Cases and Hospitalizations in Canada')
plt.grid(True)

fig.tight_layout()  # to ensure the right y-label is not clipped

# Saving the plot with high DPI
save_path = 'hos_case.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()






# Creating a column for shifted (lagged) cases
combined_data['daily_cases_4d_lag'] = combined_data['daily_cases'].shift(4)

fig, ax1 = plt.subplots(figsize=(15, 11))
font_size = 22
# Plotting daily cases
color = 'tab:blue'
ax1.set_xlabel('Date', fontsize=font_size)
ax1.set_ylabel('Daily Cases', color=color, fontsize=font_size)
ax1.plot(combined_data['date'], combined_data['daily_cases'], color=color)
ax1.tick_params(axis='y', labelcolor=color, labelsize=font_size-2)
ax1.tick_params(axis='x', labelsize=font_size-2)

# Creating a second y-axis for hospitalizations
ax2 = ax1.twinx() 
color = 'tab:red'
ax2.set_ylabel('Daily Hospitalizations', color=color, fontsize=font_size)
ax2.plot(combined_data['date'], combined_data['daily_hospitalizations'], color=color)
ax2.tick_params(axis='y', labelcolor=color, labelsize=font_size-2)

# Adding title and grid
plt.title('Daily COVID-19 Cases and Hospitalizations in Canada', fontsize=font_size+4)
plt.grid(True)

fig.tight_layout()  # to ensure the right y-label is not clipped

# Saving the plot with high DPI
save_path = 'hos_case.png'
plt.savefig(save_path, dpi=300)  # Saving with high DPI for better resolution

plt.show()
