import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

df = pd.read_csv('./target/out_10.csv', encoding='utf-8')


def chinese_word_cut(mytext):
    return ' '.join(jieba.cut(mytext))

df[5] = df[1].apply(chinese_word_cut)
print(df[5].head())

n_features = 1000

tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                max_features=n_features,
                                stop_words='english',
                                max_df=0.5,
                                min_df=10)
tf = tf_vectorizer.fit_transform(df.content_cutted)

n_topics = 5
lda = LatentDirichletAllocation(n_topics, max_iter=50,
                                learning_method='online',
                                learning_offset=50,
                                random_state=0)
lda.fit(tf)

