#! /usr/local/bin/python

import pandas as pd
import pylev
import sys

# Look at the first [LIM] chars for comparison
LIM = 5

def levenshtein(x1, x2):
  x1 = x1[:LIM]
  x2 = x2[:LIM]
  return pylev.levenshtein(x1, x2)

def lev_func(x):
  def lev(n):
    #return pylev.levenshtein(x, n)
    return levenshtein(x, n)
  return lev

lead_df = pd.read_csv('lead_list.csv')
names = lead_df['Account Name']
names = names.fillna('NONE')
names = names.head(int(sys.argv[1]))

#names = pd.Series(['foot', 'found', 'foos', 'fall', 'mall'])

dists = pd.DataFrame(index=names, columns=names)
for n in names:
  callthis = lev_func(n)
  dists.ix[n] = list(names.map(callthis))

dists.to_csv("./name_similarity.csv")

