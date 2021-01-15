# -*- coding: utf-8 -*-

import tkinter as tk
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Corpus
import collections


mot = "covid-19"

corpusR,corpusA = Corpus.CreateCorpus()

root= tk.Tk() 
font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 8}
matplotlib.rc('font', **font)

fig, axs = plt.subplots(2, 2, constrained_layout=True,figsize=(20,10))
fig.suptitle('Nombre de mentions du mot ' + str(mot) + ' et les mots les plus importants', fontsize=16)

# =============================================================================
# Fréquence d'apparition
# =============================================================================
# Graph de la fréquence d'apparition du mot choisis pour Reddit (juste les titres dans notre cas)
df_Reddit = corpusR.evolution_temporelle(mot)
axs[0,0].plot(df_Reddit)
axs[0,0].set_title('Reddit')
axs[0,0].set_xlabel('Mois)')
axs[0,0].set_ylabel('Mentions')

# Graph de la fréquence d'apparition du mot choisis pour Arxiv
df_Arxiv = corpusA.evolution_temporelle(mot)
axs[1,0].plot(df_Arxiv)
axs[1,0].set_xlabel('Mois')
axs[1,0].set_title('Arxiv')
axs[1,0].set_ylabel('Mentions')


# =============================================================================
# Partie TF-IDF
# =============================================================================
idfR,idfA = Corpus.tf_idf(corpusR,corpusA)
# Graphique des mots les plus "importants" pour Reddit 
CR = collections.Counter(idfR)
barR={}
for k, v in CR.most_common(10):
    barR[k] = v
axs[0,1].bar(list(barR.keys()), list(barR.values()), align='center')
axs[0,1].set_title('Importance Reddit')

# Graphique des mots les plus "importants" pour Arxiv
CA = collections.Counter(idfA)
barA={}
for k, v in CA.most_common(10):
    barA[k] = v
axs[1,1].bar(list(barA.keys()), list(barA.values()), align='center')
axs[1,1].set_title('Importance Reddit')

chart_type = FigureCanvasTkAgg(fig, root)
chart_type.get_tk_widget().pack()

root.mainloop()