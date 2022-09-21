from unicodedata import category
import pandas as pd

df = pd.read_excel('generators/dimensions_generator/product_dimension.xls')

list_df = list(df)

for i in list_df:
    column_values = df[i].tolist()
    break

new_list = [] 

for elem in column_values:
    new_list.append(elem.replace('/Categories/', ''))

new_list1 = [] 

for elem in new_list:
    new_list1.append(elem.replace('/Products/', ''))

words_dict = {}
for i in range(1,9):
    words_dict["category_" + str(i)] = []

for elem in new_list1:
    words = elem.split('/')
    for i in range(1,9) :
        if (len(words) >= i): words_dict['category_' + str(i)].append(words[i-1])


print(words_dict['category_1'])

for key, value in words_dict.items():
    with open('dimensions/Product.' + key, "w") as f:
        value = list(set(value))
        for elem in value:
            f.write(elem + '\n')