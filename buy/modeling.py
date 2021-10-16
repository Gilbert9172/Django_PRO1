# import numpy as np 
# import pandas as pd
# import json


# meta = pd.read_csv('movies_metadata.csv')
# meta = meta[['id', 'original_title', 'original_language', 'genres']]
# meta = meta.rename(columns={'id':'movieId'})
# meta = meta[meta['original_language'] == 'en']

# ratings = pd.read_csv('ratings_small.csv')
# ratings = ratings[['userId', 'movieId', 'rating']]

# meta.movieId = pd.to_numeric(meta.movieId, errors='coerce')
# ratings.movieId = pd.to_numeric(ratings.movieId, errors='coerce')

# def parse_genres(genres_str):
#     genres = json.loads(genres_str.replace('\'', '"'))
    
#     genres_list = []
#     for g in genres:
#         genres_list.append(g['name'])

#     return genres_list

# meta['genres'] = meta['genres'].apply(parse_genres)

# data = pd.merge(ratings, meta, on='movieId', how='inner')

# matrix = data.pivot_table(index='userId', columns='original_title', values='rating')

# GENRE_WEIGHT = 0.1

# def pearsonR(s1, s2):
#     s1_c = s1 - s1.mean()
#     s2_c = s2 - s2.mean()
#     return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

# def recommend(input_movie, matrix, n, similar_genre=True):
#     input_genres = meta[meta['original_title'] == input_movie]['genres'].iloc(0)[0]

#     result = []
#     for title in matrix.columns:
#         if title == input_movie:
#             continue

#         cor = pearsonR(matrix[input_movie], matrix[title])
        
#         if similar_genre and len(input_genres) > 0:
#             temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0]

#             same_count = np.sum(np.isin(input_genres, temp_genres))
#             cor += (GENRE_WEIGHT * same_count)
        
#         if np.isnan(cor):
#             continue
#         else:
#             result.append((title, '{:.2f}'.format(cor), temp_genres))
            
#     result.sort(key=lambda r: r[1], reverse=True)

#     return result[:n]
# search_list = pd.read_csv('search_list.csv')
# search_list = search_list.set_index('Title')

import pandas as pd 
import numpy as np 
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity


df1=pd.read_csv('tmdb_5000_credits.csv')
df2=pd.read_csv('tmdb_5000_movies.csv')

df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')
# tfidf = TfidfVectorizer(stop_words='english')

# df2['overview'] = df2['overview'].fillna('')

# tfidf_matrix = tfidf.fit_transform(df2['overview'])

# cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()


features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        if len(names) > 3:
            names = names[:3]
        return names

    return []

df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)


def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''

features = ['cast', 'keywords', 'director', 'genres']

for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
df2['soup'] = df2.apply(create_soup, axis=1)



count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['title'])


def get_recommendations(title, cosine_sim=cosine_sim2):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]
    movie_indices = [i[0] for i in sim_scores]
    return df2['title'].iloc[movie_indices]

overviews = df2.set_index('title')