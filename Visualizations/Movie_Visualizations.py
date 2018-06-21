#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 12:39:23 2018

@author: cmariekirk
"""
import Movies_CLASS
import config
import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import datetime

""" 
The code below first creates an empty numpy array of shape - length of the database contents, number of 
desired columns. Here that means a 28 row array with 4 columns. At first these are set as placeholder values 
to later be updated to reflect the contents of favorite_movies.

Next we import the data using psycopg2. Because the array is specified to contain only integers,
at first we only import the integer values from the database i.e., budget, revenue and tmdb_id 
but cannot import release_date because it is of the format datetime. """ # CAN USE PANDAS TO RESOLVE

"""
To import the datetime values we execute another psycopg2 statement to select those values
from our database and store them into a variable called dbyears. We then take the values stored
in this list and extract the only the year value and store that in our primary data numpy array.
"""
conn = psycopg2.connect(dbname='movies', user='postgres')
cur = conn.cursor()



def collect_favorite_movies():
    favorite_movies=np.ones((28,4),dtype=int) #create an 28x4 numpy array of ones 
    
    cur.execute("SELECT budget,revenue,tmdb_id FROM favorite_movies;")
    conn.commit()
    results = cur.fetchall()

    counter = 0 #updates the numpy array to reflect the contents of favorite_movies
    for i in results:
        for num in range(3):
            favorite_movies[counter,num] = i[num]
        counter += 1

    #need to convert first two columns to millions ie /ie6

    cur.execute("SELECT release_date FROM favorite_movies;")
    conn.commit()
    dbyears = cur.fetchall()
    
    counter = 0
    for i in dbyears:
        favorite_movies[counter,3] = i[0].year
        counter += 1


def collect_my_ratings():

    """ 
    
    Np array that captures identical info as above for movies rated 8
    """

    rating_eight=np.ones((45,4),dtype=int)
    
    cur.execute("SELECT budget,revenue,tmdb_id FROM my_ratings WHERE rating=8;")
    conn.commit()
    rating_eight_results = cur.fetchall()
    
    counter = 0 #updates the numpy array to reflect the contents of favorite_movies
    for i in rating_eight_results:
        for num in range(3):
            rating_eight[counter,num] = i[num]
        counter += 1
    
    cur.execute("SELECT release_date FROM my_ratings WHERE rating=8;")
    conn.commit()
    dbyears_eight = cur.fetchall()
    
    counter = 0
    for i in dbyears_eight:
        rating_eight[counter,3] = i[0].year
        counter += 1



"""" 

Visualizations Below:

"""
    
l1 = np.arange(5)
l2 = np.arange(10)

plt.figure(1)
plt.subplot(121)
plt.text(2,2,'test text')
plt.annotate('local max', xy=(4, 4), xytext=(2, 4),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )
plt.plot(l1,l1,'b-')
plt.subplot(122)
plt.plot(l2,l2,'go')




def plot_budg_vs_year():
    plt.figure(1)
    plt.scatter(data[:,3],data[:,1]) 
    plt.figure(2)
    plt.scatter(rating_eight[:,3],rating_eight[:,1]) 
    plt.ylabel('budget in millions USD')
    plt.xlabel('release date of movie')
    #need to correct the axes
    plt.show()
    
