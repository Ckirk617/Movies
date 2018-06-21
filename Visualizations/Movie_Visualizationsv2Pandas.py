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
from sqlalchemy import create_engine
import pandas as pd


def create_df(table_name):
    engine = create_engine('postgresql://cmariekirk:14BostonSt@localhost:5432/movies')
    conn = engine.connect()
    
    tableName = table_name
    df = pd.read_sql_table(tableName, engine)
    
    return df


data = create_df('favorite_movies')

rated = create_df('my_ratings')



data['year'] = df['release_date'].dt.year # creates a new column containing the release years of the movies
data['convbudget'] = (data['budget']/1e6)
data['convrevenue'] =(data['revenue']/1e6)

def plot_budg_vs_year():
    plt.figure(1)
    plt.scatter(data['year'],data['convbudget'])
    plt.xlabel('release date of movie')
    plt.ylabel('budget in million USD')
    #need to correct the axes
    plt.show()    
    
    

print(data.corr())
print()
print(rated.corr())

def plot_budg_vs_revenue():   
    pos = np.arange(len(data['convbudget'])) #the x values
    width = 0.4
    fig, ax = plt.subplots(figsize=(60,15))
    plt.bar(pos,data['convbudget'],width,alpha=1,color='r',label=None)
    plt.bar([p + width for p in pos],data['convrevenue'],width,alpha=1,color='b',label=None)
    ax.set_xticks([p + 0.2 for p in pos])
    ax.set_xticklabels(data['title'])
    ax.set_ylabel('USD in Millions')
    ax.set_xlabel('Movie Title')
    ax.set_title('Budget vs. Revenue of my Favorite Movies')
    plt.legend(['Budget', 'Revenue'], loc='upper left')
    plt.grid()
    plt.savefig('budgetvrevnue.pdf')


plot_budg_vs_revenue()