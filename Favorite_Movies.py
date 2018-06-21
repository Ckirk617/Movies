#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 16:16:27 2018

@author: cmariekirk
"""

import tmdbsimple as tmdb
import config
import psycopg2

conn = psycopg2.connect(dbname='movies', user='postgres')
cur = conn.cursor()

tmdb.API_KEY = config.api_key


cur.execute("SELECT title,tmdb_id FROM favorite_movies ORDER BY title ASC;")
result = cur.fetchall()

tmdb_ids = []
for i in result:
    tmdb_ids.append(i[1])
"""Takes the title and tmdb_id from SQL database and stores the tmdb_id in a 
list for further use """

def update_budget():
    for movies in tmdb_ids:
        temp = movies
        identity = tmdb.Movies(temp)
        response = identity.info()
        budg = identity.budget
        SQL = "UPDATE favorite_movies SET budget = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (budg, temp))
        conn.commit()    

def update_releasedate():
    for movies in tmdb_ids:
        temp = movies
        identity = tmdb.Movies(temp)
        response = identity.info()
        rd = identity.release_date
        SQL = "UPDATE favorite_movies SET release_date = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (rd, temp))
        conn.commit() 

def update_runtime():
    for movies in tmdb_ids:
        temp = movies
        identity = tmdb.Movies(temp)
        response = identity.info()
        rt = identity.runtime
        SQL = "UPDATE favorite_movies SET runtime = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (rt, temp))
        conn.commit() 

def update_revenue():
    for movies in tmdb_ids:
        temp = movies
        identity = tmdb.Movies(temp)
        response = identity.info()
        rv = identity.revenue
        SQL = "UPDATE favorite_movies SET revenue = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (rv, temp))
        conn.commit() 

def get_genres():
    """Currently takes the global variable tmdb_ids which is a list of 
    ids of movies (will eventually) contain only the movies that do 
    not have defined genres and inserts the genres into the sql 
    database called favorite_movies"""
    for movies in tmdb_ids:
        temp = movies
        identity = tmdb.Movies(temp)
        response = identity.info()
        genres_string = ''
        for i in identity.genres:
            genres_string = genres_string + str(i['name']) + ' '
        genres_string = genres_string.rstrip()
        SQL = "UPDATE favorite_movies SET genre = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (genres_string, temp))
        conn.commit() 
        
        
def get_director():
    for i in tmdb_ids:
        identity = tmdb.Movies(i)
        response = identity.credits()
        name = '' 
        for d in identity.crew:
            if d['job'] == "Director":
                print("Adding director " + str(d['name']))
                name = str(d['name'])
        SQL = "UPDATE favorite_movies SET director = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (name, i))
        conn.commit() 
    

def get_writer():
    for i in tmdb_ids:
        identity = tmdb.Movies(i)
        response = identity.credits()
        writers = ''
        for d in identity.crew:
            if d['job'] == "Screenplay":
                writers = writers + str(d['name']) + '(Screenplay)' + " "
            elif d['job'] == "Writer":
                writers = writers + str(d['name']) + '(Writer)' + " "
        writers = writers.rstrip()
        SQL = "UPDATE favorite_movies SET screenwriters = %s WHERE tmdb_id = %s;"
        cur.execute(SQL, (writers, i))
        conn.commit()


    

def add_genres(db_id):
    genres_string = ''
    identity = tmdb.Movies(db_id)
    response = identity.info()
    for i in identity.genres:
        genres_string = genres_string + str(i['name']) + ' '
    genres_string = genres_string.rstrip()
    SQL = "UPDATE favorite_movies SET genre = %s WHERE tmdb_id = %s;"
    cur.execute(SQL, (genres_string, db_id))
    conn.commit() 
    
def add_director(db_id):
    identity = tmdb.Movies(db_id)
    response = identity.credits()
    name = ''
    for i in identity.crew:
        if i['job'] == "Director":
            name = str(i['name'])
            SQL = "UPDATE favorite_movies SET director = %s WHERE tmdb_id = %s;"
            cur.execute(SQL, (name,db_id))
            conn.commit() 

def add_writer(db_id):
    identity = tmdb.Movies(db_id)
    response = identity.credits()
    writers = ''
    for i in identity.crew:
        if i['job'] == "Screenplay":
            writers = writers + str(i['name']) + '(Screenplay)' + " "
        elif i['job'] == "Writer":
            writers = writers + str(i['name']) + '(Writer)' + " "
    writers = writers.rstrip()
    SQL = "UPDATE favorite_movies SET screenwriters = %s WHERE tmdb_id = %s;"
    cur.execute(SQL, (writers, db_id))
    conn.commit()
    

def search(movie):
    """ 
    Takes a string containing a movie name and returns
    a list of matching titles from tmdb including the 
    name, release date, and tmdb id
    """
    search = tmdb.Search()
    response = search.movie(query=movie)
    for s in search.results:
        print(s['title'],s['release_date'],s['id'])
        

def add_movie(tmdb_id):
    identity = tmdb.Movies(tmdb_id)
    response = identity.info()
    
    SQL = "INSERT INTO favorite_movies(title,release_date,revenue,tmdb_id,budget,runtime) VALUES(%s,%s,%s,%s,%s,%s);" 
    
    title = identity.original_title
    release_date = identity.release_date
    revenue = identity.revenue
    db_id = tmdb_id
    budget = identity.budget
    runtime = identity.runtime
    
    cur.execute(SQL,(title,release_date,revenue,db_id,budget,runtime))
    
    #Adds Genre
    add_genres(tmdb_id)
    
    #Adds Director
    add_director(tmdb_id)
    
    #Adds Writer
    add_writer(tmdb_id)
    
    print(str(title) + " " + "Successfully Addded!")




   