# pylint: disable=I0011,C0103,C0413,W0104,W0106

#%%
import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('data_set/ml-1m/users.dat',
                      sep='::', header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('data_set/ml-1m/ratings.dat',
                        sep='::', header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('data_set/ml-1m/movies.dat',
                       sep='::', header=None, names=mnames)

#%%
users[:5]

#%%
ratings[:5]

#%%
movies[:5]

#%%
data = pd.merge(pd.merge(users, ratings), movies)
data[:5]

#%%
data.ix[0]

#%%
mean_ratings = data.pivot_table(
    'rating', index='title', columns='gender', aggfunc='mean')
mean_ratings[:5]

#%%
ratings_by_title = data.groupby('title').size()
ratings_by_title[:5]

#%% get the title of movies who get 250 ratings or above
active_titles = ratings_by_title.index[ratings_by_title >= 250]
active_titles

#%%
mean_ratings = mean_ratings.ix[active_titles]
mean_ratings[:5]

#%%
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
top_female_ratings[:5]

#%% those what females like much than males
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
sorted_by_diff[:5]

#%%
sorted_by_diff[::-1][:5]

#%% using STD to find the most controversial movies
rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]
rating_std_by_title.sort_values(ascending=False)[:5]
