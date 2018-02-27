import chardet
import csv

with open('./target/out_10.csv') as f:
    f_csv = csv.reader(f)
    print(chardet.detect(f_csv))
f.close()