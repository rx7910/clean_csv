import csv

# with open('./target/out.csv') as f:
#
#     f_csv = csv.reader(f)
#
#     for row in f_csv:
#         print(row[1])
#
# f.close()


with open('./target/out_step_2.csv') as f:

    f_csv = csv.reader(f)

    for row in f_csv:
        print(row[0])

f.close()
