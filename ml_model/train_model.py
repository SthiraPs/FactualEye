import numpy as np
import praw, nltk, itertools
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import time

# Reddit API configuration
reddit = praw.Reddit(client_id='-YIIZ6y7MIPbb6dUYUw9IQ',
                     client_secret='IzetkMNd9H9o7g_RMz0bKlVOXSj6ZQ',
                     user_agent='MyRedditApp/1.0 by Sithira')

subreddit = reddit.subreddit('drama')

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word for word in tokens if word not in stopwords.words('english') + ['machine', 'learning', 'neural']]
    return tokens

titles = [submission.title for submission in subreddit.top(limit=10)]
processed_titles = [preprocess_text(title) for title in titles]
all_title_words = list(itertools.chain(*processed_titles))

comments = []
# for submission in subreddit.top(limit=3):
#     submission.comments.replace_more(limit=None)
#     top_comments = submission.comments.list()[:10]
#     for comment in top_comments:
#         comments.append(comment.body)

processed_comments = [preprocess_text(comment) for comment in comments]
all_comment_words = list(itertools.chain(*processed_comments))

all_words = all_title_words + all_comment_words

# Bigram and Trigram extraction
bigram_finder = BigramCollocationFinder.from_words(all_words)
bigram_freq = bigram_finder.ngram_fd

trigram_finder = TrigramCollocationFinder.from_words(all_words)
trigram_freq = trigram_finder.ngram_fd

bigram_strings = [' '.join(bigram) for bigram in bigram_freq.keys() if not any(word in bigram for word in stopwords.words('english'))]
trigram_strings = [' '.join(trigram) for trigram in trigram_freq.keys() if not any(word in trigram for word in stopwords.words('english'))]

bigram_string_freq = Counter(bigram_strings)
trigram_string_freq = Counter(trigram_strings)

N = 20
word_freq = Counter(all_words)
top_bigrams = bigram_string_freq.most_common(N)
top_trigrams = trigram_string_freq.most_common(N)

# Visualization
def plot_top_words(top_words, title, color='skyblue'):
    words, counts = zip(*top_words)
    plt.figure(figsize=(12, 8))
    plt.barh(words, counts, color=color)
    plt.xlabel('Counts')
    plt.ylabel('Words/Phrases')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.show()

plot_top_words(word_freq.most_common(20), 'Top 20 Words in MachineLearning Subreddit Titles')
plot_top_words(top_bigrams, 'Top {} Bigrams in MachineLearning Subreddit Titles'.format(N))
plot_top_words(top_trigrams, 'Top {} Trigrams in MachineLearning Subreddit Titles'.format(N), color='lightgreen')

# Advanced: TF-IDF for phrases (you'll need scikit-learn for this)
vectorizer = TfidfVectorizer(ngram_range=(2,3), stop_words='english', max_features=20)
tfidf_matrix = vectorizer.fit_transform(titles)
tfidf_scores = np.sum(tfidf_matrix, axis=0)
tfidf_scores = np.asarray(tfidf_scores).ravel()
tfidf_ranking = np.argsort(tfidf_scores)[::-1]
top_phrases = [(feature, tfidf_scores[idx]) for idx, feature in enumerate(vectorizer.get_feature_names()) if idx in tfidf_ranking]
plot_top_words(top_phrases, 'Top Phrases by TF-IDF in MachineLearning Subreddit Titles', color='pink')