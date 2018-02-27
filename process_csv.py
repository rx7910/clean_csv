# -*- coding:utf-8 -*-
import csv
import re

head = None

cached_dist = []

with open('./raw/imooc-20180222.csv') as f:

    with open('./target/out_step_1.csv', 'w') as w:

        w_csv = csv.writer(w)
        f_csv = csv.reader(f)
        headers = next(f_csv)
        head = headers
        # w_csv.writerow(headers)

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
                # print(row)
                continue

            w_csv.writerow(row)

    w.close()

f.close()

# 按照课程id、用户名进行排序

with open('./target/out_step_1.csv') as f2:
    with open('./target/out_step_2.csv', 'w') as w2:
        f_csv2 = csv.reader(f2)
        w_csv2 = csv.writer(w2)
        f_sorted = sorted(f_csv2, key=lambda x: (x[3], x[0]))
        for row in f_sorted:
            w_csv2.writerow(row)
    w2.close()
f2.close()

# 合并同一门课程下面的评论

with open('./target/out_step_2.csv') as f_combine:
    with open('./target/out_step_3.csv', 'w') as w_combine:
        f_csv_combine = csv.reader(f_combine)
        w_csv_combine = csv.writer(w_combine)

        print('headhadfalsdkjflaskdjfalskjdfalksdfjasdlf===============!!!!!!!!!!!!!!!', head)
        w_csv_combine.writerow(head)

        current_course_id = None
        next_course_id = None
        current_course_name = None
        cached_str = ''

        for row in f_csv_combine:
            if current_course_id == row[-2]:
                cached_str += row[1]
            else:
                w_csv_combine.writerow([current_course_id, current_course_name, cached_str])
                current_course_id = row[-2]
                current_course_name = row[-1]
                cached_str = row[1]

    w_combine.close()

f_combine.close()

