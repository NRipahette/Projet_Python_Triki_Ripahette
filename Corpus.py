from partie1_2 import Author
from Document import Document
import pickle
import datetime as dt
import re
import pandas as pd
from random import *
from nltk.corpus import stopwords
import math

# =============================================================================
# Suite du TD4 
# =============================================================================
class Corpus():
    
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
            
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))

    # 4.1
    def search(self,motCle):
        full_text = self.get_doc(1).get_text()
        phrases = full_text.split(". ")
        phrases_avec_motcle = []
        for phrase in phrases:
            if re.search(motCle, phrase, re.IGNORECASE):
                phrases_avec_motcle.append(phrase)
        # print(phrases_avec_motcle)
        return phrases_avec_motcle

    # 4.2
    def concorde(self,taille,motCle):
        for i in range(0,self.ndoc):
            full_text = self.get_doc(i).get_text()
            phrases = full_text.split(". ")
            df = {
                "contexte gauche": [],
                "motif trouvé": [],
                "contexte droit": []
            }
            for phrase in phrases:
                match = re.search(motCle, phrase, re.IGNORECASE)
                if match:
                    df["contexte gauche"].append("..."+phrase[match.start()-taille:match.start()])
                    df["motif trouvé"].append(motCle)
                    df["contexte droit"].append(phrase[match.end():match.start()+taille]+"...")
            df_concorde = pd.DataFrame(data=df)
            return df_concorde

    

    # 4.3
    def stats(self, n):

        vocabulaire = {}
        for i in range(0,self.ndoc):
            vocabulaire[i] = netoyer_texte(self.get_doc(i).get_text())
        # Découper en mots
        # vocabulaire=vocabulaire.split(" ")
        frequence_mot={}
        
        for i in vocabulaire: # Pour le doc i dans vocabulaire
            vocabulaire[i]=vocabulaire[i].split(" ")  
            for j in vocabulaire[i]:    
            # Si le mot est deja dans le dict => augmenter la frequence
                if j in frequence_mot:
                    frequence_mot[j]+=1
            # Si le mot n'existe pas dans le dict
                else:
                    frequence_mot[j]=1
            
            
        # return(frequence_mot)

        # Afficher les n mots les plus frequents
        df_frequence_mot = pd.DataFrame(data=frequence_mot, index=[0]).T
        top_n_mots = df_frequence_mot.sort_values(by=[0], ascending=False).iloc[:n]
        # print(df_frequence_mot)
        return top_n_mots, len(df_frequence_mot)        # Afficher le top n mots et le nombre de différents mots dans les corpus
    
    def evolution_temporelle(self, motCle=None):
        # Creer n périodes avec la date max et min
        def date_range(start, end, intv):
            from datetime import datetime
            start = datetime.strptime(start,"%Y%m%d")
            end = datetime.strptime(end,"%Y%m%d")
            diff = (end  - start ) / intv
            for i in range(intv):
                yield (start + diff * i).strftime("%Y%m%d")
            yield end.strftime("%Y%m%d")
    
    
        tbl = [[],[],[]] # tbl[0] => dates, tbl[1] => text, tbl[2] => top word count
        for i in range(0,self.ndoc):
            tbl[0].append(self.get_doc(i).get_date())
            tbl[1].append(self.get_doc(i).get_text())
            # tbl[1].append(1)
            tbl[2].append(0)
    
        earliest_date = min(tbl[0]).strftime('%Y%m%d')
        lastest_date = max(tbl[0]).strftime('%Y%m%d')
        # print(earliest_date, lastest_date)
        # date_list = [lastest_date - earliest_date for x in range(10)]
        periodes = list(date_range(earliest_date, lastest_date, 10))
    
        import matplotlib.pyplot as plt
    
        # Top mot du corpus
        # motCle = self.stats(2) #ToDo - Retrieve top word
        if motCle is None:
            motCle = "covid-19"
        # print(motCle)
       
        for i in range(0,self.ndoc):
            count = len(re.findall(motCle, tbl[1][i], re.IGNORECASE)) # Nombre de fois que motCle apparait dans le texte
            tbl[2][i] += count
        
        test_df = pd.DataFrame(tbl).T
        test_df[0] = pd.to_datetime(test_df[0]) # Dates to datetime
        test_df = test_df.sort_values(by=0)
            
    
        test_df = test_df.groupby(test_df[0].dt.strftime('%Y/%m'))[2].sum()
        return test_df

# 4.4
def nettoyer_texte(texte):
    text = str.lower(texte).replace('\n', ' ')
    text = text.replace('"', ' ')
    text = text.replace("'", ' ')
    text = text.replace(',', ' ')
    text = text.replace('.', ' ')
    text = text.replace(':', ' ')
    text = text.replace('!', ' ')
    text = text.replace('?', ' ')
    text = text.replace('(', ' ')
    text = text.replace(')', ' ')
    text = text.replace('{', ' ')
    text = text.replace('}', ' ')
    text = text.replace('=', ' ')
    text = text.replace('[', ' ')
    text = text.replace(']', ' ')
    text = text.replace('  ', ' ')
    return text

# =============================================================================
# Analyse fréquence et importance des mots ( méthode evolution_temporelle en fait partie aussi )
# =============================================================================


def tf_idf(CorpusA,CorpusB):  
    #On crée un sac de mot par corpus de textes.
    sacA=[]
    for i in range(0,CorpusA.ndoc):
        text = nettoyer_texte(CorpusA.get_doc(i).get_text())
        sacA.extend(text.split(" "))
    
    sacB=[]
    for i in range(0,CorpusB.ndoc):
        textb = nettoyer_texte(CorpusB.get_doc(i).get_text())
        sacB.extend(textb.split(" "))
        
    #On crée une liste des mots qui appartiennent aux corpus
    listeMots = set(sacA).union(set(sacB))
    
    #On compte le nombre d'occurences de chaque mot dans chaque corpus
    NbMotA = dict.fromkeys(listeMots,0)
    NbMotB = dict.fromkeys(listeMots,0)
    
    #On ne comptabilise pas les mots qui font parties des stopwrods comme "the" "and" "or" etc....
    for mot in sacA:
        if mot in stopwords.words('english'):
            pass
        else:
            NbMotA[mot] +=1
    for mot in sacB:
        if mot in stopwords.words('english'):
            pass
        else:
            NbMotB[mot] +=1
        
    #Calcul de la Fréquence du mot (TF)
    TFDitcA={}
    TFDitcB={}
    tailleSacA = len(sacA)
    tailleSacB = len(sacB)
    
    for mot,n in NbMotA.items():
        TFDitcA[mot] = n /float(tailleSacA)
    for mot,n in NbMotB.items():
        TFDitcB[mot] = n /float(tailleSacB)
        
    
    #Calcul IDF
    # nombre de textes dans lesquels un mot apparait / nombre de textes 
    dictIDF = dict.fromkeys(listeMots,0)
    for doc in range(0,CorpusA.ndoc):
        motsA=[]
        stopDict = dict.fromkeys(listeMots,0) # permet de savoir si le mot à déjà été vu dans le document
        text = nettoyer_texte(CorpusA.get_doc(doc).get_text())
        motsA.extend(text.split(" "))
        for mot in motsA:
            if stopDict[mot] == 0:
                dictIDF[mot] += 1
                stopDict[mot] = 1
    
    for doc in range(0,CorpusB.ndoc):
        motsB=[]
        stopDict = dict.fromkeys(listeMots,0) # permet de savoir si le mot à déjà été vu dans le document
        text = nettoyer_texte(CorpusB.get_doc(doc).get_text())
        motsB.extend(text.split(" "))
        for mot in motsB:
            if stopDict[mot] == 0:
                dictIDF[mot] += 1
                stopDict[mot] = 1
    
    for mot, n in dictIDF.items():
        dictIDF[mot] = math.log((CorpusA.ndoc + CorpusB.ndoc)/ float(n))

    #Calcul TF-IDF 
    tfidfA = {}
    tfidfB = {}
    
    for mot , score in TFDitcA.items():
        tfidfA[mot] = score * dictIDF[mot]
    for mot , score in TFDitcB.items():
        tfidfB[mot] = score * dictIDF[mot]
    
    return tfidfA, tfidfB


################################## Création du Corpus ##################################

import praw
import urllib.request
import xmltodict   

def CreateCorpus():
    corpus1 = Corpus("Corona") # Reddit
    corpus2 = Corpus("Corona") # Arxiv
    
    reddit = praw.Reddit(client_id='hT_2ncB8kj21TQ', client_secret='rr7v3WjOMJ2M65-c0FslWibf_54', user_agent='Algorithmique et programmation avancée')
    # Timestamps to test: Jue 1st 2020 => 1590969600; August 1st 2020 => 1596240000
    # time_filter – Can be one of: all, day, hour, month, week, year
    hot_posts = reddit.subreddit('Coronavirus').hot(limit=200) # .search(query, sort="new") #.hot(limit=100)
    for post in hot_posts:
        datet = dt.datetime.fromtimestamp(post.created)
        txt = post.title + ". "+ post.selftext
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document(datet,
                       post.title,
                       post.author_fullname,
                       txt,
                       post.url
                       )
        corpus1.add_doc(doc)
    
    url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=200'
    data =  urllib.request.urlopen(url).read().decode()
    docs = xmltodict.parse(data)['feed']['entry']
    
    for i in docs:
        datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            author = [aut['name'] for aut in i['author']][0]
        except:
            author = i['author']['name']
        txt = i['title']+ ". " + i['summary']
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document(datet,
                       i['title'],
                       author,
                       txt,
                       i['id']
                       )
        corpus2.add_doc(doc)
    return corpus1,corpus2

def comparer_corpus(corpus1, corpus2):
    print("Méthode de comparaison de corpus:")
    print("*****",corpus1, "*****")
    top_words, diff_words = corpus1.stats(5)
    print("Top 5 words | count:\n", top_words)
    print("Nombre total de mots différentes dans le corpus:", diff_words)

    print("*****",corpus2, "*****")
    top_words2, diff_words2 = corpus2.stats(5)
    print("Top 5 words | count:\n", top_words2)
    print("Nombre total de mots différentes dans le corpus:", diff_words2)

