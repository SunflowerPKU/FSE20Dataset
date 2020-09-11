from nltk import word_tokenize
import collections
import math
import pandas as pd

from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    res = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))

    return " ".join(res)

f = open("idf_dic.txt", "r")
line = f.readline()
f.close()

idf = eval(line)
idf["<unk>"] = 0

def compute_tfidf(line):
    words = line.strip().split()
    counter = collections.Counter()
    for word in words:
        counter[word] += 1

    ret_dic = {}
    for item in counter:
        search_index = item
        if item not in idf:
            item = "<unk>"

        ret_dic[item] = (counter[item] / len(words)) * idf[item]

    return ret_dic


def compute_cos(dic_a, dic_b):
    dot = 0
    l_a = 0
    l_b = 0
    for item in dic_a:
        l_a += dic_a[item] * dic_a[item]

    for item in dic_b:
        l_b += dic_b[item] * dic_b[item]
        if item in dic_a:
            dot += dic_a[item] * dic_b[item]

    return dot / (math.sqrt(l_a) * math.sqrt(l_b))

def getkey(dic, num = 10):
    l = []
    for item in dic:
        l.append([dic[item], item])
    l = sorted(l)[::-1]
    key = []
    for i in range(min(len(l), num)):
        if l[i][1] == "<unk>":
            continue
        key.append(l[i][1])
    return key

if __name__ == "__main__":
    # how to use this two functions 
    
    f = open("train.txt")
    lines = f.readlines()
    evaledlines = []
    f.close()
    l = []

    for line in lines:
        evaledlines.append(eval(line))
        l.append(" ".join(word_tokenize(lemmatize_sentence(eval(line)[2].strip()))).lower())
    
    lines = l

    f = open("data.full.txt", "w")
    top = 10
    for i in range(0, len(lines)):
        dic_a = compute_tfidf(lines[i])
        evaledlines[i].append(getkey(dic_a))
        evaledlines[i].append(getkey(dic_a, 20))
        f.write(str(evaledlines[i]) + "\n")
        evaledlines[i][-1] = " ".join(evaledlines[i][-1])
        evaledlines[i][-2] = " ".join(evaledlines[i][-2])
    f.close()
    
    csv_list = pd.DataFrame(data=evaledlines)
    csv_list.to_csv('data.csv')
        #print (dic_a)
        #dic_b = compute_tfidf(lines[i + 1])
        #compute_cos(dic_a, dic_b)
        
