# with open("weather_data.csv") as data_file:
#     data = data_file.readlines()
#     print(data)
#     # ['day,temp,condition\n', 'Monday,12,Sunny\n', 'Tuesday,14,Rain\n', 
#     # 'Wednesday,15,Rain\n', 'Thursday,14,Cloudy\n', 'Friday,21,Sunny\n', 
#     # 'Saturday,22,Sunny\n', 'Sunday,24,Sunny']

# import csv

# with open('weather_data.csv') as f:
#     data = csv.reader(f)
#     # print(data) # <_csv.reader object at 0x1048444a0> -- iterable
#     for row in data:
#         print(row)
#         """
#         ['day', 'temp', 'condition']
#         ['Monday', '12', 'Sunny']
#         ['Tuesday', '14', 'Rain']
#         ['Wednesday', '15', 'Rain']
#         ['Thursday', '14', 'Cloudy']
#         ['Friday', '21', 'Sunny']
#         ['Saturday', '22', 'Sunny']
#         ['Sunday', '24', 'Sunny']
#         """
    
# What happen if we have much more complex data? --> PANDA
# Doc: https://pandas.pydata.org/docs/
# Api: https://pandas.pydata.org/docs/reference/index.html

import pandas

def print_separator():
    print("-----------------------------------")
    ############################################
    
data = pandas.read_csv("weather_data.csv")
print(data)
"""
         day  temp condition
0     Monday    12     Sunny
1    Tuesday    14      Rain
2  Wednesday    15      Rain
3   Thursday    14    Cloudy
4     Friday    21     Sunny
5   Saturday    22     Sunny
6     Sunday    24     Sunny
"""

############################################
print_separator()
print(type(data["temp"]))
# <class 'pandas.core.series.Series'>
print(data["temp"])
# Each column is called a Series
# Hole table: DataFrame
"""
0    12
1    14
2    15
3    14
4    21
5    22
6    24
Name: temp, dtype: int64
"""

############################################
print_separator()
data_list = data["temp"].to_list()  # this is a python list
print(data_list)  # [12, 14, 15, 14, 21, 22, 24]

############################################
print_separator()
print(data.to_dict())

############################################
print_separator()
print(data["temp"].all() == data.temp.all()) # True, means we can access series(columns) with dot notation

############################################
print_separator()
print("How do we access rows?")
# We have to make a filter with unique ID in the seria, and that will return a row
monday_row = data[data.day == "Monday"] # Get hole DF and then filter the column value
print(type(monday_row))
# <class 'pandas.core.frame.DataFrame'>
print(monday_row)
"""
      day  temp condition
0  Monday    12     Sunny
"""
print(data[data.temp == data.temp.max()])
"""
      day  temp condition
6  Sunday    24     Sunny
"""

############################################
print_separator()
# How do we create a DF from a dict

students_dict = {
    "students": ["Amy", "John"],
    "scores": [8,9]
}
data = pandas.DataFrame(students_dict)
print(data)
"""
  students  scores
0      Amy       8
1     John       9
"""
# Save it to a file
data.to_csv("students_data.csv")

############################################
print_separator()