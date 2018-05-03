import pandas as pd
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Mi0ying2017', db='mooc_data', charset='utf8')
sqlcmd = 'select commentor_id, course_id, content, mark, modify_timestamp from mooc_comment'
df = pd.read_sql(sqlcmd, conn)
commentor_id_list = df['commentor_id']
course_id_list = df['course_id']


def transforId(id_before):
    id_before = list(set(id_before))
    id_before.sort()
    transfor_dic = {'id_before': id_before}
    transfor_df = pd.DataFrame(transfor_dic)
    transfor_df['id_after'] = transfor_df.index + 1
    return transfor_df

new_commentor_id_df = transforId(commentor_id_list)
new_course_id_df = transforId(course_id_list)

df2 = pd.merge(df, new_commentor_id_df, left_on='commentor_id', right_on='id_before')
df2.rename(columns={'id_after': 'commentor_id_new'}, inplace=True)

df3 = pd.merge(df2, new_course_id_df, left_on='course_idÅ', right_on='id_before')
df3.rename(columns={'id_after': 'course_id_new'}, inplace=True)

df_new = pd.DataFrame(df3, columns=['commentor_id_new', 'course_id_new', 'content', 'mark', 'modify_timestamp'])
df_new.to_csv('./course_marks.csv', sep=';', header=True)