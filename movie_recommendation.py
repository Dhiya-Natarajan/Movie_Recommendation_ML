import pandas as pd
import numpy as np
import streamlit as st
# this ensures even typo errors will display the desired movie
import difflib
# I am using (Text Freq index and Doc Freq Index) this converts textual data into numerics based on freq of occ
from sklearn.feature_extraction.text import TfidfVectorizer
# This is to find the similarity score among all the movies , this is used to recommend similar movies having the same liking
from sklearn.metrics.pairwise import cosine_similarity

def movie_inputs(movie_name,num_mov):
    # this gives a list of moives which are a close match

    close_match=difflib.get_close_matches(movie_name,df['title'])
    #close_match

    if not close_match:
        st.write('No match found')
        return

    match=close_match[0]
    matched_index = df[df['title'] == match].index[0]

    similarity_score_index = similarity_df.loc[matched_index]
    similarity_all_movies = list(enumerate(similarity_score_index))
    

    sorted_score = sorted(similarity_all_movies, key=lambda x: x[1], reverse=True)

    i = 1
    st.write("Because you watched ", movie_name, "\n")
    st.write("Here are some similar movies:\n")
    for interested in sorted_score:
        index = interested[0]
        if i<=num_mov and index!=matched_index: #this ensures that we are not displaying the same movie
            movie_title=df.iloc[index]['title']        
            st.write("No.",i," ",movie_title)
            i += 1

df=pd.read_csv('C:\\Users\\dhiya\\Downloads\\movies.csv')
# Feature Selection
select_fea = ['genres', 'keywords', 'tagline','cast', 'director']

# In case of missing values fill with empty string
for val in select_fea:
        df[val]=df[val].fillna('')
        
concat_fea = df['genres'] + ' ' + df['keywords'] + ' ' + df['tagline'] + ' ' + df['cast'] + ' ' + df['director']
# this ensures that all enteries in concat_fea is a string
concat_fea = concat_fea.astype(str)
   
v=TfidfVectorizer()
X_train_count=v.fit_transform(concat_fea.values)

similarity_score=cosine_similarity(X_train_count)

similarity_df=pd.DataFrame(similarity_score)

movie_name=st.text_input('Enter a movie name')

num_mov=st.number_input('Enter the number of movies you would like to see displayed according to your preference \n')

if movie_name and num_mov:
    movie_inputs(movie_name,num_mov)
