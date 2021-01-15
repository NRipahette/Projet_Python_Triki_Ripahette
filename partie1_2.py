#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 08/05/2020

@author: julien and antoine
"""

################################## Déclaration des classes ##################################

import datetime as dt
import re

import pickle
# import Corpus
# import Document  

class Author():
    def __init__(self,name):
        self.name = name
        self.production = {}
        self.ndoc = 0
        
    def add(self, doc):     
        self.production[self.ndoc] = doc
        self.ndoc += 1

    def __str__(self):
        return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)
    def __repr__(self):
        return self.name

import praw

import urllib.request
import xmltodict   



################################## Création du Corpus ##################################

# corpus = Corpus("Corona")


# reddit = praw.Reddit(client_id='hT_2ncB8kj21TQ', client_secret='rr7v3WjOMJ2M65-c0FslWibf_54', user_agent='Algorithmique et programmation avancée')
# hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)
# for post in hot_posts:
#     datet = dt.datetime.fromtimestamp(post.created)
#     txt = post.title + ". "+ post.selftext
#     txt = txt.replace('\n', ' ')
#     txt = txt.replace('\r', ' ')
#     doc = Document(datet,
#                    post.title,
#                    post.author_fullname,
#                    txt,
#                    post.url)
#     corpus.add_doc(doc)

# url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
# data =  urllib.request.urlopen(url).read().decode()
# docs = xmltodict.parse(data)['feed']['entry']

# for i in docs:
#     datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
#     try:
#         author = [aut['name'] for aut in i['author']][0]
#     except:
#         author = i['author']['name']
#     txt = i['title']+ ". " + i['summary']
#     txt = txt.replace('\n', ' ')
#     txt = txt.replace('\r', ' ')
#     doc = Document(datet,
#                    i['title'],
#                    author,
#                    txt,
#                    i['id']
#                    )
#     corpus.add_doc(doc)

# print("Création du corpus, %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))

# print()

# print("Corpus trié par titre (4 premiers)")
# res = corpus.sort_title(4)
# print(res)
    
# print()

# print("Corpus trié par date (4 premiers)")
# res = corpus.sort_date(4)
# print(res)

# print()

# print("Enregistrement du corpus sur le disque...")
# corpus.save("Corona.crp")
# corpus.searh("test")