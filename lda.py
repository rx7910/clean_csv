import jieba
import pandas as pd
import pyLDAvis
import pymysql
import time
import pyLDAvis.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt

# pyLDAvis.enable_notebook()


stop_words = open('./stopwords/中文停用词库.txt', encoding='gb2312')
stop_words_content = stop_words.read()
stop_list = stop_words_content.splitlines()
stop_words.close()


def chinese_word_cut(mytext):
    return ' '.join(jieba.cut(mytext))


conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='Mi0ying2017', db='mooc_data', charset='utf8')
sql = 'select content from mooc_comment where course_id=268001'
# where course_id=268001
df = pd.read_sql(sql, con=conn)
conn.close()
df['content_cutted'] = df.content.apply(chinese_word_cut)

n_features = 1000
n_top_words = 20
n_samples = 0.7
data_set = df['content_cutted'].tolist()
data_samples = data_set[:int(len(data_set) * n_samples)]
test_samples = data_set[int(len(data_set) * n_samples):]

print('Extracting tf features for LDA...')
tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                max_features=n_features,
                                stop_words=stop_list,
                                max_df=0.5,
                                min_df=10)
t0 = time.time()
tf = tf_vectorizer.fit_transform(data_samples)
print('done in %0.3fs.' % (time.time() - t0))

print('Extracting tf features for LDA...')
t0 = time.time()
tf_test = tf_vectorizer.transform(test_samples)
print('done in %0.3fs.' % (time.time() - t0))

df_perplexity = pd.DataFrame(columns=['n_topics', 'train_perplexity', 'test_perplexity'])


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print('Topic #%d:' % topic_idx)
        print(' '.join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

for i in range(20, 101, 20):
    n_topics = i
    # print('Fitting LDA models with tf features,'
    #       'n_samples=%d, n_features=%d, n_topics=%d'
    #       %(n_samples, n_features, n_topics))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=100,
                                    learning_method='online',
                                    learning_offset=50,
                                    random_state=0)
    t0 = time.time()
    lda.fit(tf)

    train_gamma = lda.transform(tf)
    train_perplexity = lda.perplexity(tf, train_gamma)
    test_gamma = lda.transform(tf_test)
    test_perplexity = lda.perplexity(tf_test, test_gamma)

    df_perplexity = df_perplexity.append({'n_topics': n_topics,
                                          'train_perplexity': train_perplexity,
                                          'test_perplexity': test_perplexity},
                                         ignore_index=True)

    # print('sklearn perplexity: train=%0.3f, test=%0.3f'%(train_perplexity, test_perplexity))
    # print('done in %0.3fs.' % (time.time() - t0))

    tf_feature_names = tf_vectorizer.get_feature_names()

    print_top_words(lda, tf_feature_names, n_top_words)

    visualisation = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)

    #pyLDAvis.save_html(visualisation, 'LDA_Visualization_'+str(i)+'.html')

print(df_perplexity)


topic = df_perplexity['n_topics']
perplexity = df_perplexity['train_perplexity']


def graph_draw(topic, perplexity):
    x = topic
    y = perplexity
    plt.plot(x, y, color="red", linewidth=2)
    plt.xlabel("Number of Topic")
    plt.ylabel("Perplexity")
    plt.show()


graph_draw(topic, perplexity)




