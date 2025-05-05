import pandas as pd
import matplotlib.pyplot as plt

# Load the provided CSV file
file_path = 'cases_pt.csv'
data = pd.read_csv(file_path, parse_dates=['date'], dayfirst=False)

# Display the first few rows of the dataframe to understand its structure
data.head()

# Grouping the data by date and summing the values to get total cumulative cases and total daily new cases for each date
grouped_data = data.groupby('date').agg({'value': 'sum', 'value_daily': 'sum'}).reset_index()

# Display the aggregated data
grouped_data.head()

# Identifying and removing the data points where the cumulative cases drop
cleaned_data = grouped_data.copy()

# Finding the point where the cumulative cases drop
drop_point = cleaned_data['value'].idxmax()  # This should be the highest point before the drop

# Keeping only the data up to the drop point
cleaned_data = cleaned_data.iloc[:drop_point + 1]

import matplotlib.dates as mdates

# Re-plotting the graph with adjusted x-axis tick frequency

# Creating the figure
plt.figure(figsize=(15, 11))

# Plotting the data
plt.plot(cleaned_data['date'], cleaned_data['value'], label='Cumulative Cases', color='blue')
font_size = 22
# Setting the x-axis ticks to be monthly (or another suitable frequency)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# Adding labels and title
plt.title('COVID-19 Cumulative Cases in Canada', fontsize=font_size+4)
plt.xlabel('Date', fontsize=font_size)
plt.ylabel('Cumulative Cases', fontsize=font_size)
plt.xticks(fontsize=font_size, rotation=45)
plt.yticks(fontsize=font_size)
plt.grid(visible=True)

# Showing the plot
plt.tight_layout()
save_path = 'case_cul_CA.png'
plt.savefig(save_path, dpi=300)
plt.show()



# Graph for Daily New Cases
plt.figure(figsize=(15, 11))
plt.plot(cleaned_data['date'], cleaned_data['value_daily'], label='Daily New Cases', color='red', alpha=0.7)

# Setting the x-axis ticks to be monthly (or another suitable frequency)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=4))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

plt.title('COVID-19 Daily New Cases in Canada', fontsize=font_size+4)
plt.xlabel('Date', fontsize=font_size)
plt.ylabel('Daily New Cases', fontsize=font_size)
plt.xticks(rotation=45, fontsize=font_size)
plt.yticks(fontsize=font_size)
plt.grid(visible=True)
plt.tight_layout()

save_path = 'case_new_CA.png'
plt.savefig(save_path, dpi=300)

plt.show()

