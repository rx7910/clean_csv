import csv

# with open('./target/out.csv') as f:
#
#     f_csv = csv.reader(f)
#
#     for row in f_csv:
#         print(row[1])
#
# f.close()


import pandas as pd

df = pd.read_csv('./target/out_10.csv',encoding='utf-8')
print(df.columns.values)