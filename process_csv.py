import csv
import re

with open('./raw/imooc-20180222.csv') as f:

    with open('./target/out.csv', 'w') as w:

        w_csv = csv.writer(w)
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        w_csv.writerow(headers)

        filter_dist = 'js,java,python,javascript,go,c++,for,error,name,iphone,mark,if'

        for row in f_csv:
            if re.search(r"http", row[1]):
                # print(row)
                continue

            if re.search(r"^[’!\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~。，0-9a-zA-Z]+$", row[1]):
                continue

            if re.search(r"www", row[1]):
                # print(row)
                continue

            if re.search(r"\.com", row[1]):
                # print(row)
                continue

            if re.search(r"\.com", row[1]):
                # print(row)
                continue

            if re.search(r".*<.*>.*", row[1]):
                print(row)
                continue

            w_csv.writerow(row)

    w.close()

f.close()

# todo sort csv

with open('./target/out.csv') as f2:
    with open('./target/out_step_2.csv', 'w') as w2:
        f_csv2 = csv.reader(f2)
        w_csv2 = csv.writer(w2)
        headers = next(f_csv2)
        print(headers)
        w_csv2.writerow(headers)

        current_course_id = None
        next_course_id = None
        current_course_name = None
        cached_str = ''

        for row in f_csv2:
            if current_course_id == row[-2]:
                cached_str += row[1]
            else:
                w_csv2.writerow([current_course_id, current_course_name, cached_str])
                current_course_id = row[-2]
                current_course_name = row[-1]
                cached_str = row[1]

    w2.close()

f2.close()


