"""
- Google's search interest ranges between 0 and 100.
Numbers represent search interest relative to the highest point on the chart for the given region and time.
A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular.
A score of 0 means there was not enough data for this term.

Basically, the actual search volume of a term is not publicly available. Google only offers a scaled number.
Each data point is divided by the total searches of the geography and time range it represents to compare 
relative popularity.

- Here are the Google Trends Search Parameters that I used to generate the .csv data:
"Tesla", Worldwide, Web Search
"Bitcoin", Worldwide, News Search
"Unemployment Benefits", United States, Web Search


##### Things learned here: #####

How to use .describe() to quickly see some descriptive statistics at a glance.
How to use .resample() to make a time-series data comparable to another by changing the periodicity.
How to work with matplotlib.dates Locators to better style a timeline (e.g., an axis on a chart).
How to find the number of NaN values with .isna().values.sum()
How to change the resolution of a chart using the figure's dpi
How to create dashed '--' and dotted '-.' lines using linestyles
How to use different kinds of markers (e.g., 'o' or '^') on charts.
Fine-tuning the styling of Matplotlib charts by using limits, labels, linewidth and colours (both in the form of named colours and HEX codes).
Using .grid() to help visually identify seasonality in a time series.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df_tesla = pd.read_csv('TESLA Search Trend vs Price.csv')

# monthly search volume from Google Trends.
df_btc_search = pd.read_csv('Bitcoin Search Trend.csv')
# day-by-day closing price and the trade volume of Bitcoin across 2204 rows. 
df_btc_price = pd.read_csv('Daily Bitcoin Price.csv')

df_unemployment = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')


print(df_tesla.shape)  # (124,3)

# .describe(). 
# If you use df_tesla.describe(), you get a whole bunch of descriptive statistics
print(df_tesla.describe())
"""
       TSLA_WEB_SEARCH  TSLA_USD_CLOSE
count       124.000000      124.000000
mean          8.725806       50.962145
std           5.870332       65.908389
min           2.000000        3.896000
25%           3.750000        7.352500
50%           8.000000       44.653000
75%          12.000000       58.991999
max          31.000000      498.320007
"""


### Remove missing values
df_tesla.isna()
"""
     MONTH  TSLA_WEB_SEARCH  TSLA_USD_CLOSE
0    False            False           False
1    False            False           False
...
"""
df_tesla.isna().values  # convert to list
"""
array([[False, False, False],
       [False, False, False],
       [False, False, False
       ...
"""

print(f'Missing values for Tesla?: {df_tesla.isna().values.any()}') # check if any() of the list is True, i.e is NaN
print(f'Missing values for U/E?: {df_unemployment.isna().values.any()}')
print(f'Missing values for BTC Search?: {df_btc_search.isna().values.any()}')
print(f'Number of missing values: {df_btc_price.isna().values.sum()}')
# Remove NaN values
# df_btc_price = df_btc_price.dropna()
df_btc_price.dropna(inplace=True)  # same as above



######## Convert string to datetimes

# All the date data in our columns are in the form of strings.
# To convert this into a Datetime object we're going to use the Pandas .to_datetime() function

print(type(df_tesla.MONTH[0])) # str
df_tesla.MONTH = pd.to_datetime(df_tesla.MONTH)
df_btc_search.MONTH = pd.to_datetime(df_btc_search.MONTH)
df_unemployment.MONTH = pd.to_datetime(df_unemployment.MONTH)
df_btc_price.DATE = pd.to_datetime(df_btc_price.DATE)
print(type(df_tesla.MONTH[0])) # <class 'pandas._libs.tslibs.timestamps.Timestamp'>, dtype: datetime64[ns]


##########################################################################
######### Resampling Time Series Data (convert daily data to monthly data)

# Next, we have to think about how to make our Bitcoin price and our Bitcoin search volume comparable.
# Our Bitcoin price is daily data, but our Bitcoin Search Popularity is monthly data.

# To convert our daily data into monthly data, we're going to use the .resample() function.
# The only things we need to specify is which column to use (i.e., our DATE column) and what
# kind of sample frequency we want (i.e., the "rule"). We want a monthly frequency, so we use 'ME'. 
# If you ever need to resample a time series to a different frequency, 
# you can find a list of different options here: 
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects 
# (for example 'Y' for yearly or 'T' for minute).

# resample() is a time-based groupby, followed by a reduction method on each of its groups

# Resample: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
# https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#resampling
# Convenience method for frequency conversion and resampling of time series.
# The object must have a datetime-like index (DatetimeIndex, PeriodIndex, or TimedeltaIndex),
# or the caller must pass the label of a datetime-like series/index to the on/level keyword parameter.


# Group data by month, and get last price of the month
df_btc_monthly = df_btc_price.resample('ME', on='DATE').last()
# Group data by month, and get average price of the month
df_btc_monthly_mean = df_btc_price.resample('ME', on='DATE').mean()

# Now we have data for each month.. same amount of rows as search data

####################################################################################
######################## Plot Tesla info ############################################


# # Create locators for ticks on the time axis, i.e. a mark for each year and month
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y') # how we see dates in the date labels at the bottom

# # Register date converters to avoid warning messages
# from pandas.plotting import register_matplotlib_converters
# register_matplotlib_converters()

# Plot the Tesla stock price against the Tesla search volume using a line chart and two different axes. 
# Label one axis 'TSLA Stock Price' and the other 'Search Trend'.
# Increase the figure size (e.g., to 14 by 8). 
# 2. Increase the font sizes for the labels and the ticks on the x-axis to 14. 
# 3. Rotate the text on the x-axis by 45 degrees. 
# 4. Make the lines on the chart thicker. 
# 5. Add a title that reads 'Tesla Web Search vs Price'
# 6. Keep the chart looking sharp by changing the dots-per-inch or [DPI value](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.figure.html). 
# 7. Set minimum and maximum values for the y and x axis. Hint: check out methods like [set_xlim()](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.axes.Axes.set_xlim.html). 
# 8. Finally use [plt.show()](https://matplotlib.org/3.2.1/api/_as_gen/matplotlib.pyplot.show.html) to display the chart below the cell instead of relying on the automatic notebook output.

plt.figure(figsize=(10,6), dpi=120) # increases size and resolution
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# format the ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# Also, increase fontsize and linewidth for larger charts
ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# Set the minimum and maximum values on the axes
ax1.set_ylim([0, 600])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

ax1.plot(df_tesla.MONTH, df_tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(df_tesla.MONTH, df_tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

# Displays chart explicitly
plt.show(block=True)



########################################################################
######################### Plot BTC info ################################
########################################################################

# Modify the chart title to read 'Bitcoin News Search vs Resampled Price'
# Change the y-axis label to 'BTC Price'
# Change the y- and x-axis limits to improve the appearance
# Investigate the linestyles to make the BTC closing price a dashed line
# Investigate the marker types to make the search datapoints little circles
# Were big increases in searches for Bitcoin accompanied by big increases in the price?


plt.figure(figsize=(14,8), dpi=120)
 
plt.title('Bitcoin News Search vs Resampled Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.set_ylabel('BTC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)
 
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
 
ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([df_btc_monthly.index.min(), df_btc_monthly.index.max()])

# Show the grid lines as dark grey lines
ax1.grid(color='grey', linestyle='--')
 
# Experiment with the linestyle and markers
ax1.plot(df_btc_monthly.index, df_btc_monthly.CLOSE, 
         color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(df_btc_monthly.index, df_btc_search.BTC_NEWS_SEARCH, 
         color='skyblue', linewidth=3, marker='o')
 
plt.show()