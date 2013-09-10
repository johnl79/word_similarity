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

def compute_similarity(names):
  dists = pd.DataFrame(index=names, columns=names)
  for n in names:
    callthis = lev_func(n)
    dists.ix[n] = list(names.map(callthis))

  dists.to_csv("./name_similarity.csv")

def aggregate_matches(A):
  results = []
  while(len(A.columns)):
    first_col = A.pop(A.columns[0])
    G = first_col[ first_col == 0 ]
    match_list = list(G.index)
    num_match = len(G)
    this_name = G.name
    result = (this_name, num_match, match_list)
    print result
    results.append(result)
    for m in match_list:
      try:
        A.pop(m)
      except KeyError:
        pass
  results = pd.DataFrame(results, columns=["Name", "No. Matches", "Matches"])
  results.to_csv("./matches.csv")


