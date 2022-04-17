import json


def load_roots(filename):
    roots = []
    f = open(filename)
    contents = f.readlines()
    f.close()
    for line in contents:
        possibilities = [""]
        if len(line) < 3:
            continue
        root, definition = [part.strip() for part in line.split('>')]
        i = 0
        while i < len(root):
            if root[i] == '(':
                end = root.find(')', i+1)
                optional = root[i+1:end]
                new_poss = []
                for poss in possibilities:
                    new_poss.append(poss + optional)
                    new_poss.append(poss)
                possibilities = new_poss
                i = end + 1
            else:
                possibilities = [poss + root[i] for poss in possibilities]
                i += 1
        for poss in possibilities:
            roots.append((poss, definition))
    return roots


def find_affixes(word, affixes, roots):
    attributive_prefixes = [
        prefix for prefix in affixes['prefixes'] if prefix['argument'] == 'attributive']
    basic_prefixes = [prefix for prefix in affixes['prefixes']
                      if prefix['argument'] == 'basic']
    attributive_suffixes = [
        suffix for suffix in affixes['suffixes'] if suffix['argument'] == 'attributive']
    basic_suffixes = [suffix for suffix in affixes['suffixes']
                      if suffix['argument'] == 'basic']

    possibilities = [{
        'charleft': word,
        'meanings': []
    }]

    # print(possibilities)
    # print('finding attributive_prefixes')
    temp = possibilities.copy()
    for possibility in possibilities:
        word = possibility['charleft']
        for prefix in attributive_prefixes:
            if word.startswith(prefix['realization']):
                if prefix['realization'][-1] == 'o':
                    new_poss = {
                        'charleft': 'a' + word[len(prefix['realization']):],
                        'meanings': possibility['meanings'] + [prefix]
                    }
                    temp.append(new_poss)
                new_poss = {
                    'charleft': word[len(prefix['realization']):],
                    'meanings': possibility['meanings'] + [prefix]
                }
                temp.append(new_poss)
    possibilities = temp.copy()
    # print(possibilities)
    # print('finding basic_prefixes')
    for possibility in possibilities:
        word = possibility['charleft']
        for prefix in basic_prefixes:
            if word.startswith(prefix['realization']):
                new_poss = {
                    'charleft': word[len(prefix['realization']):],
                    'meanings': possibility['meanings'] + [prefix]
                }
                temp.append(new_poss)
    possibilities = temp.copy()
    # print(possibilities)
    # print('finding roots')
    for possibility in possibilities:
        word = possibility['charleft']
        for (root, meaning) in roots:
            if word.startswith(root):
                new_poss = {
                    'charleft': word[len(root):],
                    'meanings': possibility['meanings'] + [{
                        'realization': root,
                        'meaning': meaning
                    }]
                }
                temp.append(new_poss)
    possibilities = temp.copy()
    # print(possibilities)
    # print('finding basic_suffixes')
    for possibility in possibilities:
        word = possibility['charleft']
        for suffix in basic_suffixes:
            if word.startswith(suffix['realization']):
                new_poss = {
                    'charleft': word[len(suffix['realization']):],
                    'meanings': possibility['meanings'] + [suffix]
                }
                temp.append(new_poss)
    possibilities = temp.copy()
    # print(possibilities)
    # print('finding attributive_suffixes')
    for possibility in possibilities:
        word = possibility['charleft']
        for suffix in attributive_suffixes:
            if word.startswith(suffix['realization']):
                new_poss = {
                    'charleft': word[len(suffix['realization']):],
                    'meanings': possibility['meanings'] + [suffix]
                }
                temp.append(new_poss)
    possibilities = temp.copy()
    return possibilities


def print_legible(possibilities):
    for poss in possibilities:
        # print(poss)
        breakup = []
        meanings = []
        for meaning in poss['meanings']:
            breakup.append(meaning['realization'])
            meanings.append(meaning['meaning'])
        if len(poss['charleft']) > 0:
            breakup.append(poss['charleft'])
            meanings.append('<unmatched>')
        print(breakup)
        print(meanings)
        print()


def constrain_possibilities(possibilities):
    new_poss = []
    for poss in possibilities:
        if poss['charleft'] != '':
            continue
        new_poss.append(poss)
    return new_poss
