import pandas as pd
import numpy as np
from tmdbv3api import TMDb
import json
import requests
from tmdbv3api import Movie
import bs4 as bs
import urllib.request

tmdb_movie = Movie()
class Data_Fetchings_18:  # Fetching  the data
    def __init__(self):
        pass

    def get_genre(self, x):  # collecting all genre
        tmdb = TMDb()
        tmdb_movie = Movie()
        genres = []
        result = tmdb_movie.search(x)
        movie_id = result[0].id
        response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id, tmdb.api_key))
        data_json = response.json()
        if data_json['genres']:
            genre_str = " "
            for i in range(0, len(data_json['genres'])):
                genres.append(data_json['genres'][i]['name'])
            return genre_str.join(genres)
        else:
            np.NaN

    def get_director(self, x):  # collecting director name
        if "(director)" in x:
            return x.split('(director)')[0]
        elif "(directors)" in x:
            return x.split('(directors)')[0]
        else:
            return x.split('(director/screenplay)')[0]

    def get_actor1(self, x):  # collecting first actor name
        return ((x.split('screenplay);')[-1]).split(', ')[0])

    def get_actor2(self, x):  # collecting second actor name
        if len((x.split('screenplay);')[-1]).split(', ')) < 2:
            return np.NaN
        else:
            return ((x.split('screenplay);')[-1]).split(', ')[1])

    def get_actor3(self, x):
        if len((x.split('screenplay);')[-1]).split(', ')) < 3:
            return np.NaN
        else:
            return ((x.split('screenplay);')[-1]).split(', ')[2])

    def data_frame(self, link):
        df1 = pd.read_html(link, header=0)[2]
        df2 = pd.read_html(link, header=0)[3]
        df3 = pd.read_html(link, header=0)[4]
        df4 = pd.read_html(link, header=0)[5]
        df = pd.concat([df1, df2, df3, df4], axis=0)
        tmdb = TMDb()
        tmdb.api_key = '5492165c61b1a21c06eb3a3b578a6339'
        tmdb_movie = Movie()
        df['genre'] = df['Title'].apply(lambda x: self.get_genre(str(x)))
        df_1 = df[['Title', 'Cast and crew', 'genre']]
        df_1['director_name'] = df_1['Cast and crew'].apply(lambda x: self.get_director(x))
        df_1['actor_1_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor1(x))
        df_1['actor_2_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor2(x))
        df_1['actor_3_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor3(x))
        df_1 = df_1.rename(columns={'Title': 'movie_title'})
        new_df_2 = df_1[['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name', 'genre', 'movie_title']]
        new_df_2['actor_2_name'] = new_df_2['actor_2_name'].replace(np.nan, 'unknown')
        new_df_2['actor_3_name'] = new_df_2['actor_3_name'].replace(np.nan, 'unknown')
        new_df_2.movie_title = new_df_2.movie_title.str.lower()
        new_df_2['comb'] = new_df_2.actor_1_name + " " + new_df_2.actor_2_name + " " + new_df_2.actor_3_name + " " + new_df_2.director_name + " " + new_df_2.genre
        return new_df_2


class Data_Fetchings_20:

    def __init__(self):
        pass

    def get_genre(self,x):
        tmdb = TMDb()
        tmdb_movie = Movie()
        genres = []
        result = tmdb_movie.search(x)
        print(f'result = {result}')
        if not result:
            return np.NaN

        else: 
            movie_id = result[0].id
            print(f'movie_id  {movie_id}')
            response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
            print(f'response : {response}')
            data_json = response.json()
            print(f'data j_son = {data_json}')

            if data_json['genres']:
                print(f"data_json['genres'] = {data_json['genres']}")
                genre_str = " "
                for i in range(0,len(data_json['genres'])):
                    genres.append(data_json['genres'][i]['name'])
                return genre_str.join(genres)
            else:
                return np.NaN


    def get_director(x):
        if " (director)" in x:
            return x.split(" (director)")[0]
        elif " (directors)" in x:
            return x.split(" (directors)")[0]
        else:
            return x.split(" (director/screenplay)")[0]

    def get_actor1(x):
        return ((x.split("screenplay); ")[-1]).split(", ")[0])

    def get_actor2(x):
        if len((x.split("screenplay); ")[-1]).split(", ")) < 2:
            return np.NaN
        else:
            return ((x.split("screenplay); ")[-1]).split(", ")[1])

    def get_actor3(x):
        if len((x.split("screenplay); ")[-1]).split(", ")) < 3:
            return np.NaN
        else:
            return ((x.split("screenplay); ")[-1]).split(", ")[2])

    def collection(self,link):
        source = urllib.request.urlopen(link)
        soup = bs.BeautifulSoup(source, 'lxml')  # to get element from ul link
        tables = soup.find_all('table', class_='wikitable sortable')

        df1 = pd.read_html(str(tables[0]))[0]
        df2 = pd.read_html(str(tables[1]))[0]
        df3 = pd.read_html(str(tables[2]))[0]
        df4 = pd.read_html(str(tables[3]).replace("'1\"\'", '"1"'))[0]  # avoided "ValueEr
        df = pd.concat([df1, df2, df3, df4], axis=0)
        tmdb = TMDb()
        tmdb.api_key = '5492165c61b1a21c06eb3a3b578a6339'
        df_1 = df[['Title', 'Cast and crew']]
        df_1['genre'] = df_1['Title'].apply(lambda x: self.get_genre(str(x)))
        #df_1['director_name'] = df_1['Cast and crew'].apply(lambda x: self.get_director(x))
        df_1['actor_1_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor1(x))
        df_1['actor_2_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor2(x))
        df_1['actor_3_name'] = df_1['Cast and crew'].apply(lambda x: self.get_actor3(x))
        df_1 = df_1.rename(columns={'Title': 'movie_title'})
               
        new_df2 = df_1.loc[:,['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name', 'genres', 'movie_title']]

        new_df2['comb'] = df_1.actor_1_name + " " + df_1.actor_2_name + " " + df_1.actor_3_name + " " + ndf_1.director_name + " " + df_1.Genre

        return new_df2

