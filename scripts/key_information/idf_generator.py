from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
import numpy as np
import collections
import math

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

f = open("stop_words.txt", "r")
lines = f.readlines()
f.close()
stop_words = []
for line in lines:
    stop_words.append(line.strip())


f = open("train.txt", "r")
lines = f.readlines()#eval(f.readlines())[1].strip()
f.close()
corpus = []#lines
#for i in range(len(lines)):
#    lines[i] = lemmatize_sentence(lines[i])

for line in lines:
    c = ""
    words = word_tokenize(lemmatize_sentence(eval(line)[2].strip()).lower())    
    nwords = []
    for w in words:
        if w not in stop_words:
            nwords.append(w)
    #print (words)
    corpus.append(" ".join(nwords))

dic = collections.Counter()
lines = corpus
for line in lines:
    words = line.strip().split()
    #print (words)
    used = collections.Counter()
    for word in words:
        if word not in ['{', '}', '[', ']', '(', ')', '.', ':', '"', "'", '', ' ', '', '。', '：', '，', '）', '（', '！', '?', '”', '“', "’", "‘", "；"] and used[word] < 1:
            dic[word] += 1
            used[word] += 1

D = len(lines)
print_dic = {}
#print_dic["<unk>"] = math.log((D + 1) / 1 + 1, 2)
for item in dic:
    print_dic[item] = math.log((D + 1) / (dic[item] + 1) + 1, 2)

f = open("idf_dic.txt", "w")
f.write(str(print_dic))
f.close()

