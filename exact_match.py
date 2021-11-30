from Levenshtein import distance as ldist
import numpy as np
import sys

def first_match(gold, word):
  length = min((len(gold), len(word)))
  idx = 0
  while(idx < length and gold[idx] == word[idx]):
    idx += 1
  return idx

def mid_match(gold, word):
  i = 0
  best = 0
  while(i < len(word)):
    while(i < len(word) and word[i] != gold[0]):
      i += 1
    j = i
    while(j < len(word) and j-i < len(gold) and word[j] == gold[j-i]):
      j += 1
    best = max(best, j-i)
    i += 1
  return best

def edit_dist(gold, word):
  return ldist(gold, word)

def declutter(word):
  result = ''
  for char in word:
    if char == '~':
      result += 'e'
    elif char == 'q':
      result += 'o'
    elif char == "'":
      pass
    elif char == '3':
      result += 'a'
    elif char == '2':
      result += 'o'
    elif char == ':':
      pass
    elif char == 't':
      result += 'd'
    else:
      result += char
  return result

def stem(word):
  word = declutter(word)
  original = word
  if len(word) < 3:
    return word
  # number prefix
  if word[:2] == 'de':
    word = word[2:]
  if len(word) < 3:
    return word
  # noun prefix
  if word[0] == 'o' or word[0] == 'a':
    word = word[1:]
  elif word[:2] == 'ga':
    word = word[2:]
  elif word[:2] == 'ag' or word[:2] == 'go' or word[:2] == 'ho':
    word = word[2:]
  elif word[:2] == 'ha' or word[:2] == 'ek' or word[:2] == 'go':
    word = word[2:]
  elif len(word) > 3 and word[:3] == 'ago':
    word = word[3:]
  elif len(word) > 3 and word[:3] == 'gae' or word[:3] == 'hadi':
    word = word[3:]
  if len(word) < 3:
    return word
  # pluralizer suffix:
  if len(word) > 5 and word[-5:] == 'shooh':
    return word[:-5]
  elif len(word) > 3 and word[-3:] == 'sho':
    return word[:-3]
  if len(word) < 3:
    return word
  # noun suffix
  if word[-1] == 'a' or word[-1] == 'e':
    word = word[:-1]
  elif len(word) > 4 and word[-4:] == 'ageh' or word[-4:] == 'egeh':
    word = word[:-4]
  elif len(word) > 3 and word[-3:] == 'ago':
    word = word[:-3]
  elif word[-2:] == 'go':
    word = word[:-2]
  elif len(word) > 4 and word[-4:] == 'akah':
    word = word[:-4]
  elif len(word) > 7 and word[-7:] == 'akdagye':
    word = word[:-7]
  elif len(word) > 5 and word[-5:] == 'gowah':
    word = word[:-5]
  if len(original) - len(word) > 1:
    return word
  word = original
  if len(word) < 3:
    return word
  # verb aspect-mode categories
  if len(word) > 4 and word[-4:] == 'gehe':
    word = word[:-4]
  elif word[-1] == 'k':
    word = word[:-1]
  elif len(word) > 3 and word[-3:] == 'hne':
    word = word[:-3]
  elif len(word) > 3 and word[-3:] == 'hek' or word[-3:] == 'hok':
    word = word[:-3]
  if len(word) < 3:
    return word
  # aspect suffixes
  if len(word) > 3 and word[-3:] == 'ahs':
    word = word[:-3]
  elif word[-1] == 's' or word[-1] == 'h' or word[-1] == 'o':
    word = word[:-1]
  elif word[-2:] == 'oh':
    word = word[:-2]
  if len(word) < 3:
    return word
  # agent pronominal prefixes
  if len(word) > 4 and word[:4] in ['akni','agwa','gadi','hadi']:
    word = word[4:]
  elif len(word) > 3 and word[:3] in ['agy','agw','gen','hen','gao','gae','kni','dwa','sni','swa']:
    word = word[3:]
  elif word[:2] in ['gy', 'dw', 'sw', 'ga', 'ha']:
    word = word[2:]
  elif word[0] in ['g','s','j','w','h','o','k','e']:
    word = word[1:]
  if len(word) < 3:
    return word
  # patient pronominal prefixes
  if len(word) > 4 and word[:4] in ['okni','ogwa','hodi','godi']:
    word = word[4:]
  elif len(word) > 3 and word[:3] in ['ogy','ogw','hon','gon','odi','swa','sni']:
    word = word[3:]
  elif word[:2] in ['ag','sw','on','ak','sa','ho','go']:
    word = word[2:]
  elif word[0] in ['s','j']:
    word = word[1:]
  if len(word) < 3:
    return word
  # modal prefixes
  if word[:2] == 'sa':
    word = word[2:]
  elif word[0] == 'a' or word[0] == 'e':
    word = word[1:]
  


  return word
  
def edit_stemmer(gold, word):
  gstem = stem(gold)
  wstem = stem(word)
  return mid_match(gstem, declutter(word))
  # return edit_dist(gstem, wstem)

def score_weighted(related, predicted):
  score = 0
  inc = max(0.2, 1 / (len(related) - 1))
  for w in predicted:
    if w in related:
      score += inc
  return min(1, score)

def score_one(related, predicted):
  for w in predicted:
    if w in related:
      return 1
  return 0

# exact_math.py input.txt dictionary.txt match_func v/s
arguments = sys.argv
if len(arguments) == 1:
  filename = arguments[0]
  input_name = 'hand_words.txt'
  dict_name = 'hand_dict.txt'
  fn_name = first_exact
  verbose = False
elif len(arguments) == 5:
  filename, input_name, dict_name, fn_name, verbose = arguments
  if verbose == 'v':
    verbose = True
  else:
    verbose = False
else:
  print("Wrong number of arguments")

wordbank = open(input_name, 'r')

fn_dict = { 'first_match' : (first_match, -1),
            'mid_match' : (mid_match, -1),
            'edit_dist' : (edit_dist, 1),
            'edit_stem' : (edit_stemmer, 1)
          }
match_fn, rank_mult = fn_dict[fn_name]

sum_one = 0
sum_weighted = 0
num_inputs = 0
for ln in wordbank.readlines():
  num_inputs += 1
  line = ln.split(' ')
  word = line[0]
  rankings = []
  dictionary = open('hand_dict.txt', 'r')
  for dln in dictionary.readlines():
    dline = dln.split(' ')
    dw = dline[0]
    # rankings.append((dw, match_fn(declutter(word), declutter(dw))))
    rankings.append((dw, match_fn(word, dw)))
  dictionary.close()
  rankings.sort(key = lambda x : rank_mult * x[1])
  matches = []
  for word, score in rankings:
    if not word in matches:
      matches.append(word)
  sum_one += score_one(line[1:], matches[:10])
  sum_weighted += score_weighted(line[1:], matches[:10])
  if not verbose:
    print(line[0], ':', score_weighted(line[1:], matches[:10]))
  else:
    print(line[0], ':', score_weighted(line[1:], matches[:10]), matches[:10])
print('Average weighted score:  ', sum_weighted / num_inputs)
print('Average one-found score: ', sum_one / num_inputs)
