#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:05:16 2018

@author: cmariekirk
"""


import tmdbsimple as tmdb
import config
import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(dbname='movies', user='postgres')
cur = conn.cursor()

tmdb.API_KEY = config.api_key

class Movies(object):
      
    def __init__(self):
        self.id = None
        self.title  = None
        
    def __str__(self):
        return "Movie located at table: " + str(self.table)

   
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
        
    def add_movie(tmdb_id,rating=None):
        identity = tmdb.Movies(tmdb_id)
        response = identity.info()
        
        SQL = "INSERT INTO my_ratings (title,release_date,revenue,tmdb_id,budget,runtime,rating) VALUES(%s,%s,%s,%s,%s,%s,%s);"  
        title = identity.original_title
        release_date = identity.release_date
        revenue = identity.revenue
        db_id = tmdb_id
        budget = identity.budget
        runtime = identity.runtime
        rate = rating
        
        cur.execute(SQL,(title,release_date,revenue,db_id,budget,runtime,rate))
        
        def add_genres(tmdb_id):
            genres_string = ''
            identity = tmdb.Movies(tmdb_id)
            response = identity.info()
            for i in identity.genres:
                genres_string = genres_string + str(i['name']) + ' '
            genres_string = genres_string.rstrip()
            SQL = "UPDATE my_ratings SET genre = %s WHERE tmdb_id = %s;"
            cur.execute(SQL, (genres_string, tmdb_id))
            conn.commit() 
            
        def add_director(tmdb_id):
            identity = tmdb.Movies(tmdb_id)
            response = identity.credits()
            name = ''
            for i in identity.crew:
                if i['job'] == "Director":
                    name = str(i['name'])
                    SQL = "UPDATE my_ratings SET director = %s WHERE tmdb_id = %s;"
                    cur.execute(SQL, (name,db_id))
                    conn.commit() 
    
        def add_writer(tmdb_id):
            identity = tmdb.Movies(tmdb_id)
            response = identity.credits()
            writers = ''
            for i in identity.crew:
                if i['job'] == "Screenplay":
                    writers = writers + str(i['name']) + '(Screenplay)' + " "
                elif i['job'] == "Writer":
                    writers = writers + str(i['name']) + '(Writer)' + " "
            writers = writers.rstrip()
            SQL = "UPDATE my_ratings SET screenwriters = %s WHERE tmdb_id = %s;"
            cur.execute(SQL, (writers, tmdb_id))
            conn.commit()
            
            #Adds Genre
        add_genres(tmdb_id)
        
        #Adds Director
        add_director(tmdb_id)
        
        #Adds Writer
        add_writer(tmdb_id)
        
        print(str(title) + " " + "Successfully Addded!")

    
    def title(self):
            identity = tmdb.Movies(self.id)
            response = identity.info()
            print("Title is " + str(identity.title))
    
    def director(self):
            identity = tmdb.Movies(self.id)
            response = identity.credits()
            name = '' 
            for i in identity.crew:
                if i['job'] == "Director":
                    name = str(i['name'])
            print("Director was" + name)
     
    def writer(self):
            identity = tmdb.Movies(self.id)
            response = identity.credits()
            writers = '' 
            for i in identity.crew:
                if i['job'] == "Screenplay":
                    writers = writers + str(i['name']) + '(Screenplay)' + " "
                elif i['job'] == "Writer":
                    writers = writers + str(i['name']) + '(Writer)' + " "
            writers = writers.rstrip()
            print("Writer(s) was/were: " + writers)
            
    def budget(self):
        identity = tmdb.Movies(self.id)
        response = identity.info()
        print("Budget was " + str(identity.budget))

    def releasedate(self):
        identity = tmdb.Movies(self.id)
        response = identity.info()
        print("Release Date was " + str(identity.release_date))

    def runtime(self):
        identity = tmdb.Movies(self.id)
        response = identity.info()
        print("Runtime was " + str(identity.runtime) + " minutes long")

    def revenue(self):
        identity = tmdb.Movies(self.id)
        response = identity.info()
        print("Revenue was $" + str(identity.revenue))
        #want to modify to convert budget into millions
        
    def genres(self):
        identity = tmdb.Movies(self.id)
        response = identity.info()
        genres_string = ''
        for i in identity.genres:
            genres_string = genres_string + str(i['name']) + ' '
        genres_string = genres_string.rstrip()
        print("Genre(s): " + genres_string)

class Rate(Movies):
    
    def __init__(self):
        self.rating = None
        self.id = None
    
    def get_all_ratings():
        SQL = "SELECT title,rating FROM my_ratings ORDER BY rating DESC;"
        cur.execute(SQL)
        results = cur.fetchall()
        for i in results:
            print(i[0] + ": " + str(i[1]))
    
    def add_rating(movie,new_rating):
        title = movie
        if new_rating > 10:
            print("Error - rating cannot be greater than 10")
        elif new_rating <1:
            print("Error - rating cannot be less than 0")
        else:
            rating = int(new_rating)
        SQL = "UPDATE my_ratings SET rating = %s WHERE title = %s;"
        cur.execute(SQL,(rating,title))
        conn.commit()
        print("Rating succesfully updated")
    
    def rate(self,new_rating):
        title = self.id
        if new_rating > 10:
            return "Error - rating cannot be greater than 10"
        elif new_rating <1:
            return "Error - rating cannot be less than 0"
        else:
            rating = int(new_rating)
        SQL = "UPDATE my_ratings SET rating = %s WHERE tmdb_id = %s;"
        cur.execute(SQL,(rating,title))
        conn.commit()
        print("Rating succesfully updated")

