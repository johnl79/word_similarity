#! /usr/local/bin/python

import pandas as pd

A = pd.read_csv('name_similarity_all.csv')
A.index = A.pop("Account Name")

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
