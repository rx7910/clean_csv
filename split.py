import csv

with open('./target/out_step_2.csv') as f:
        f_csv = csv.reader(f)

        with open('./target/out_10_comment.csv', 'w') as w:
            w_csv = csv.writer(w)
            for row in f_csv:
                if row[-2] == '10':
                    w_csv.writerow(row[1])
        w.close()

f.close()
