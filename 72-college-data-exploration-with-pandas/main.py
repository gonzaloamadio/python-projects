"""
Use .head(), .tail(), .shape and .columns to explore your DataFrame and find out the number of rows and columns as well as the column names.

Look for NaN (not a number) values with .findna() and consider using .dropna() to clean up your DataFrame.

You can access entire columns of a DataFrame using the square bracket notation: df['column name'] or df[['column name 1', 'column name 2', 'column name 3']]

You can access individual cells in a DataFrame by chaining square brackets df['column name'][index] or using df['column name'].loc[index]

The largest and smallest values, as well as their positions, can be found with methods like .max(), .min(), .idxmax() and .idxmin()

You can sort the DataFrame with .sort_values() and add new columns with .insert()

To create an Excel Style Pivot Table by grouping entries that belong to a particular category use the .groupby() method
"""

import pandas as pd

df = pd.read_csv("salaries_by_college_major.csv")

print(df.head())

print(df.shape) # prints (num of rows, num of columns)
print(df.columns)
print("-----------------------------------")

"""
Before we can proceed with our analysis we should try and figure out if there are any missing or junk data
in our dataframe. That way we can avoid problems later on. In this case,
we're going to look for NaN (Not A Number) values in our dataframe.
NAN values are blank cells or cells that contain strings instead of numbers.
Use the .isna() method and see if you can spot if there's a problem somewhere
"""
print(df.isna())

print(df.tail())

print("-----------------------------------")
"""
We see that last row is trash, we do not want it in our DataFrame

There's two ways you can go about removing this row.
 1) The first way is to manually remove the row at index 50. 
 2) Simply use the .dropna() method from pandas. 
 
 Let's create a new dataframe without the last row and examine the last 5 rows to make sure we removed the last row:
"""

########## look for empty values ##########

clean_df = df.dropna()
print(clean_df.tail())
print("-----------------------------------")

########################################
########## min and max values ##########

# Find College Major with Highest Starting Salaries
starting_salary = clean_df['Starting Median Salary']
max_salary = starting_salary.max()
print("Max salary is {}".format(max_salary))
print("")

# Info for max salary
row_with_max_salary = clean_df[starting_salary == max_salary]
print(row_with_max_salary)
print(type(row_with_max_salary)) # <class 'pandas.core.frame.DataFrame'>
print("")
row = row_with_max_salary["Undergraduate Major"]
print(row)
print(type(row)) # <class 'pandas.core.series.Series'>
"""
43    Physician Assistant
Name: Undergraduate Major, dtype: object
<class 'pandas.core.series.Series'>
"""
########################################
########## access a cell value ##########

# Doing the same other way: 
# .idxmax() method will give us index for the row with the largest value.
id_row_with_max_salary = starting_salary.idxmax()
# Find the cell for: Column/Serie Undergraduate Major, and row id_row_with_max_salary
print("")
print(clean_df['Undergraduate Major'].loc[id_row_with_max_salary])
print(clean_df['Undergraduate Major'][id_row_with_max_salary]) # same as row above
print(type(clean_df['Undergraduate Major'].loc[id_row_with_max_salary]))  # str

# If you don't specify a particular column you can use the .loc property to retrieve an entire row:
print("-----------------------------------")
print(clean_df.loc[43])
print(type(clean_df.loc[43]))  # <class 'pandas.core.series.Series'>

print("-----------------------------------")
row_43 = clean_df.loc[43]
print(row_43['Undergraduate Major'])


print("-----------------------------------")
# ### What college major has the highest mid-career salary? 
# How much do graduates with this major earn? (Mid-career is defined as having 10+ years of experience).
print(f"Mid career max salary {clean_df['Mid-Career Median Salary'].max()}")
print(f"Index for the max mid career salary: {clean_df['Mid-Career Median Salary'].idxmax()}")
career_with_max_salary = clean_df['Undergraduate Major'][clean_df['Mid-Career Median Salary'].idxmax()]
print(career_with_max_salary)

# ### The Lowest Starting and Mid-Career Salary
print(clean_df['Starting Median Salary'].min())
print(clean_df['Undergraduate Major'].loc[clean_df['Starting Median Salary'].idxmin()])
print(clean_df.loc[clean_df['Mid-Career Median Salary'].idxmin()])

###########################################################################
########## arythmethic and create a new column with those values ##########

print("-----------------------------------")
# ### Lowest Risk Majors
# A low-risk major is a degree where there is a small difference between the lowest and highest salaries.
# In other words, if the difference between the 10th percentile and the 90th percentile earnings 
# of your major is small, then you can be more certain about your salary after you graduate.

# How would we calculate the difference between the earnings of the 10th and 90th percentile?
# Well, Pandas allows us to do simple arithmetic with entire columns, so all we need to do
# is take the difference between the two columns:

salary_diff = clean_df['Mid-Career 90th Percentile Salary'] - clean_df['Mid-Career 10th Percentile Salary']
#same 
salary_diff_2 = clean_df['Mid-Career 90th Percentile Salary'].subtract(clean_df['Mid-Career 10th Percentile Salary'])
print(type(salary_diff)) # <class 'pandas.core.series.Series'>
# print(salary_diff) # 0     109800.0, 1      96700.0, 2     113700.0

# The output of this computation will be another Pandas dataframe column.
# We can add this to our existing dataframe with the .insert() method.
# First arg is the position of where to insert. 1 means in the second column
clean_df.insert(1, 'Salary Diff', salary_diff)
print(clean_df.head())
"""
     Undergraduate Major  Salary Diff  Starting Median Salary   . . .
0             Accounting     109800.0                 46000.0   . . . 
1  Aerospace Engineering      96700.0                 57700.0   . . . 
2            Agriculture     113700.0                 42600.0   . . . 
3           Anthropology     104200.0                 36800.0   . . .
4           Architecture      85400.0                 41600.0   . . . 
"""

###########################################
########## Sort values ####################

print("-----------------------------------")
# ### Sorting by the Lowest Spread
low_risk = clean_df.sort_values('Salary Diff')
print(type(low_risk)) # <class 'pandas.core.frame.DataFrame'>
df_top_5_less_risk_jobs = low_risk[['Undergraduate Major', 'Salary Diff']].head()
print(df_top_5_less_risk_jobs)

print("-----------------------------------")
# Find the degrees with the highest potential? Find the top 5 degrees with the highest values in the 90th percentile. 
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary')
print(highest_potential.tail())
# same
highest_potential = clean_df.sort_values('Mid-Career 90th Percentile Salary', ascending=False)
highest_potential[['Undergraduate Major', 'Mid-Career 90th Percentile Salary']].head()
# Find the degrees with the greatest spread in salaries.
low_risk.tail()
# Same
highest_spread = clean_df.sort_values('Salary Diff', ascending=False)
highest_spread[['Undergraduate Major', 'Salary Diff']].head()


########################################
########## Group values ################
print("-----------------------------------")

grouped_by_category = clean_df.groupby('Group')
print(type(grouped_by_category))  # <class 'pandas.core.groupby.generic.DataFrameGroupBy'>
print("")

num_of_jobs_in_each_category = clean_df.groupby('Group').count()
print(num_of_jobs_in_each_category['Undergraduate Major'])

print("")
pd.options.display.float_format = '{:,.2f}'.format 
just_num_columns = clean_df.drop(columns=["Undergraduate Major"])
print(just_num_columns.groupby('Group').mean())