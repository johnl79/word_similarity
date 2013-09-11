#! /usr/local/bin/python

import pandas as pd
import pylev
import sys

#Truncate to n chars
TRUNC = 5

# Do not consider length in lev (Truncate both to the len of the smaller)
NO_LEN = 1

# Return the similarity between string s1 and s2. Currently runs on a
# levenshtein basis with options for string truncation and consideration of
# length differences.
def similarity(s1, s2):
  # Length considerations on/off
  if NO_LEN == 1:
    trunc_len = min(len(s1), len(s2), TRUNC)
  else:
    trunc_len = TRUNC

  # Truncate
  s1 = s1[:trunc_len]
  s2 = s2[:trunc_len]

  # Return the levenshtein distance between the two modified strings
  return pylev.levenshtein(s1, s2)


def cmp_func(x):
  def cmp(n):
    return similarity(x, n)
  return cmp

def compute_similarity(items):
  distances = pd.DataFrame(index=items, columns=items)
  for n in items:
    callthis = cmp_func(n)
    distances.ix[n] = list(items.map(callthis))
  return distances

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

if __name__ == "__main__":
  while TRUNC < 18:
    lead_df = pd.read_csv('input/lead_list.csv')
    names = lead_df['Account Name']
    names = names.fillna('NONE')

    # Limit size for testing
    #names = names.head(int(sys.argv[1]))

    A = compute_similarity(names)
    A.save("output/" + str(TRUNC) + "sim.pd")
    TRUNC = TRUNC + 3

