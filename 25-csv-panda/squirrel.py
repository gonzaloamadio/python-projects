import pandas

# DF
data = pandas.read_csv("squirrel_data_main.csv")

gray_squirrels = data[data["Primary Fur Color"] == "Gray"]
red_squirrels = data[data["Primary Fur Color"] == "Cinnamon"]
black_squirrels = data[data["Primary Fur Color"] == "Black"]

data_dict = {
    "Fur Color": ["Gray", "Cinnamon", "Black"],
    "Color": [len(gray_squirrels), len(red_squirrels), len(black_squirrels)]
}

df = pandas.DataFrame(data_dict)
df.to_csv("squirrel_color_count.csv")