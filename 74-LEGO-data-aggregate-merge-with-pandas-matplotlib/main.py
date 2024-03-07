"""
Today we're going to be diving deep into a dataset all about LEGO, which will help us answer a whole bunch of
  interesting questions about the history of the company, their product offering, and which LEGO set rules them all:
What is the most enormous LEGO set ever created and how many parts did it have?
In which year were the first LEGO sets released and how many sets did the company sell when it first launched?
Which LEGO theme has the most sets? Is it Harry Potter, Ninjago, Friends or something else?
When did the LEGO company really take-off based on its product offering? How many themes and sets did it release every year?
Did LEGO sets grow in size and complexity over time? Do older LEGO sets tend to have more or fewer parts than newer sets?

--- What you'll learn today
How to combine a Notebook with HTML Markup.
Apply Python List slicing techniques to Pandas DataFrames.
How to aggregate data using the .agg() function.
How to create scatter plots, bar charts, and line charts with two axes in Matplotlib.
Understand database schemas that are organised by primary and foreign keys.
How to merge DataFrames that share a common key

NOTE: If you want to see plots, uncomment plot and scatter lines
"""

import pandas as pd
import matplotlib.pyplot as plt

colors = pd.read_csv("data/colors.csv")

"""
   id            name     rgb is_trans
0  -1         Unknown  0033B2        f
1   0           Black  05131D        f
...
"""

##### How many colors do we have? #####
len_of_colors_df = len(colors)
print(f"There are {len_of_colors_df} different colors")
# Same. Unique count for each column
un = colors.nunique() # <class 'pandas.core.series.Series'>
"""
id          135
name        135
rgb         124
is_trans      2
"""
print(f"There are {un.id} different colors")
# Same. Count number of names
num_of_colours = colors['name'].nunique()

##### How many are transparent and how many opaque? #####
transparency_count = colors.groupby(['is_trans']).count()
"""
is_trans  id  name  rgb
f         107   107  107
t          28    28   28
"""
transparency_count_dict = transparency_count.id.to_dict()
print(f"There are {transparency_count_dict['f']} opaque colours and {transparency_count_dict['t']} transparent")
print(f"There are {transparency_count.id.f} opaque colours and {transparency_count.id.t} transparent")
# Same. value_counts: Return a Series containing counts of unique values.
is_trans_count = colors.is_trans.value_counts()
print(is_trans_count)
"""
is_trans
f    107
t     28
Name: count, dtype: int64
"""

############################################################
############################################################
############################################################
print("-----------------------------------------------------")

sets = pd.read_csv("data/sets.csv")
print(sets.head())
"""
  set_num                        name  year  theme_id  num_parts
0   001-1                       Gears  1965         1         43
1  0011-2           Town Mini-Figures  1978        84         12
2  0011-3  Castle 2 for 1 Bonus Offer  1987       199          0
3  0012-1          Space Mini-Figures  1979       143         12
4  0013-1          Space Mini-Figures  1979       143         12
"""
min_year = sets.year.min() # 1949
min_year_2 = sets.sort_values('year').year.values[0]
min_year_3 = sets.loc[sets.year.idxmin()].year  # this may not be just one value in case of not unique values?
min_year_4 = sets.loc[sets.year.idxmin(), "year"]
print(min_year, min_year_2, min_year_3, min_year_4)

print("\n--- All LEGOs in the first year")
all_legos_first_year = sets[sets.year == min_year]
print(all_legos_first_year)

print("\n--- LEGO with more parts")
sets.sort_values("num_parts", ascending=False).head()

############################################################
################# Sets by year, and plot result ############
############################################################

print("\n--- Sets by year")
sets_by_year = sets.groupby("year")
sets_by_year_count = sets_by_year.count()
print(sets_by_year_count.set_num)
#plt.plot(sets_by_year_count.index, sets_by_year_count.set_num)
# Take out last value, because 2021 year info is wrong
#plt.plot(sets_by_year_count.index[:-1], sets_by_year_count.set_num[:-1])
#plt.title("Sets released by year")
# This is needed so we can see when we ran in bash, and image does not close automatically
plt.show(block=True)

############################################################
############# Aggregate functions ##########################
############################################################

# We want to calculate the number of different themes by calendar year
# This means we have to group the data by year and then count the number of unique theme_ids for that year

# Agg takes a dict as an arg. And we specify wich operation to apply to each column
# In our case, we just want to calculate the number of unique entries in the theme_id column
# by using our old friend, the .nunique() method.

# Number of themes by year
print("\n--- Themes by year")
themes_by_year = sets.groupby("year").agg({'theme_id': pd.Series.nunique})

# Rename column
themes_by_year.rename(columns={"theme_id":"themes_count"}, inplace=True)
print(themes_by_year)
#plt.plot(themes_by_year.index[:-1], themes_by_year.themes_count[:-1])
#plt.title("Themes released by year")
#plt.show(block=True)

############# Plot both in same graph ######################

"""
The problem is that they have very different scale in the Y axis
The theme number ranges between 0 and 90, while the number of sets ranges between 0 and 900.
So what can we do?

We need to be able to configure and plot our data on two separate axes on the same chart.
This involves getting hold of an axis object from Matplotlib.
"""
ax1 = plt.gca()   # get current axis
ax2 = ax1.twinx() # By using the .twinx() method allows ax1 and ax2 to share the same x-axis

#ax1.plot(sets_by_year_count.index[:-1], sets_by_year_count.set_num[:-1], color='g')
#ax2.plot(themes_by_year.index[:-1], themes_by_year.themes_count[:-1], 'b')
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of sets", color="green")
ax2.set_ylabel("Number of themes", color="blue")
plt.title("Themes and Sets released by year")
#plt.show(block=True)

############# Average ######################

# Has the year as the index and contains the average number of parts per LEGO set in that year
print("\n--- Avergate parts per set in each year")
parts_per_set = sets.groupby("year").agg({'num_parts': pd.Series.mean})
print(parts_per_set)

# Scatter plot: simply uses dots to represent the values of each data point.
#plt.scatter(themes_by_year.index[:-1], themes_by_year.themes_count[:-1])
#plt.title("Themes released by year")
#plt.show(block=True)


##############################################################
### Relational Database Schemas: Primary and Foreign Keys ####
##############################################################

# Number of Sets per LEGO Theme
# But we have no idea which theme is, we just see the id
print("\n--- set_theme_count")
set_theme_count = sets.theme_id.value_counts()
print(set_theme_count)
"""
theme_id
158    753
501    656
      ...
414      1
Name: count, Length: 571, dtype: int64
"""

"""
The themes.csv file has the actual theme names.
How is this table linked to the others tables? Well,
the sets .csv has theme_ids which match the id column in the themes.csv.

This means that the theme_id is the foreign key inside the sets.csv.
Many different sets can be part of the same theme.
But inside the themes.csv, each theme_id, which is just called id is unique.
This uniqueness makes the id column the primary key inside the themes.csv.
To see this in action, explore the themes.csv.
"""

print("\n--- Themes structure")
themes = pd.read_csv("data/themes.csv")
print(themes.head())
"""
   id            name  parent_id
0   1         Technic        NaN
1   2  Arctic Technic        1.0
2   3     Competition        1.0
"""

print("\n--- Star wars themes")
print(themes[themes.name == "Star Wars"])
"""
      id       name  parent_id
17    18  Star Wars        1.0
150  158  Star Wars        NaN
174  209  Star Wars      207.0
211  261  Star Wars      258.0
"""

print("\n--- Sets with star wars themes")
sw_theme_ids = themes[themes.name == "Star Wars"].id.values  # array([ 18, 158, 209, 261])
print(sets[sets.theme_id.isin(sw_theme_ids)])
"""
           set_num                                               name  year  theme_id  num_parts
850        11912-1                Star Wars: Build Your Own Adventure  2016       158         73
855        11920-1  Parts for Star Wars Build Your Own Adventure: ...  2019       158         70
1717       20006-1                            Clone Turbo Tank - Mini  2008       158         64
1728       20007-1                     Republic Attack Cruiser - Mini  2009       158         84
1738       20009-1                                AT-TE Walker - Mini  2009       158         94
...            ...                                                ...   ...       ...        ...
15686         VP-4            Star Wars Co-Pack of 7101 7111 and 7171  2000       158          0
15689         VP-8                 Star Wars Co-Pack of 7130 and 7150  2000       158          0
15707      XWING-1                                Mini X-Wing Fighter  2019       158         60
15708      XWING-2                                  X-Wing Trench Run  2019       158         52
15709  YODACHRON-1                    Yoda Chronicles Promotional Set  2013       158        413
"""

##############################################################
############### Merge DataFrames #############################
##############################################################

"""
The .merge() method to combine two separate DataFrames into one.
The merge method works on columns with the same name in both DataFrames
"""

# Convert series into DF
set_theme_count = pd.DataFrame({
  "id": set_theme_count.index,
  "set_count": set_theme_count.values
})
"""
    id    set_count
 0  158    753   
 1 . . .
"""

"""
To .merge() two DataFrame along a particular column, we need to provide our two DataFrames
and then the column name on which to merge. This is why we set on='id'.
Both our set_theme_count and our themes DataFrames have a column with this name.
"""
print("\n--- Merged themes info")
# Order matters, merge will be in the order of id "id" of the first arg of merge
# so if set_theme_count is ordered some way, it will respect that order
# in this case, set_count descending
merged_df = pd.merge(set_theme_count, themes , on='id')
print(merged_df[:3])

##### Plot

plt.figure(figsize=(14,8))
plt.xticks(fontsize=14, rotation=45)
plt.yticks(fontsize=14)
plt.ylabel('Nr of sets', fontsize=14)
plt.xlabel('Theme', fontsize=14)
plt.bar(merged_df.name[:10], merged_df.set_count[:10])


"""
In this lesson we looked at how to:

  combine the groupby() and count() functions to aggregate data

  use the .value_counts() function

  slice DataFrames using the square bracket notation e.g., df[:-2] or df[:10]

  use the .agg() function to run an operation on a particular column

  rename() columns of DataFrames

  create a line chart with two separate axes to visualise data that have different scales.

  create a scatter plot in Matplotlib

  work with tables in a relational database by using primary and foreign keys

  .merge() DataFrames along a particular column

  create a bar chart with Matplotlib  
"""