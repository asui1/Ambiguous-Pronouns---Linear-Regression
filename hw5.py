import math, csv
from bs4 import BeautifulSoup
from urllib import request
from nltk.corpus import brown, reuters, words, stopwords, treebank
from nltk import *
import pathlib
from nltk.corpus import conll2000
import nltk
import sys
import re

def is_match(first, second):
    if " " in first or " " in second:
        return False
    if len(first) != len(second):
        return False
    if "*" in first or "*" in second:
        match = 0
        for i in range(len(first)):
            if first[i] == second[i]:
                match += 1
        if match >= len(first)-1:
            return True
    else:
        if first == second:
            return True
    return False

def find_ord(text, word):
    length = len(word)
    index = []
    for i in range(len(text)-length):
        cur_word = text[i: i+length]
        if is_match(cur_word, word):
            index.append(i)
    return index

def get_nth(text, word, wanted_pos, occur):
    count = 1
    for i in occur:
        if i == wanted_pos or i == wanted_pos +1 or i == wanted_pos - 1:
            return count
        count += 1
    return len(occur)


def chunk_text(text):
    sents = text.split(".")
    if "" in sents:
        sents.remove("")
    chunks = []
    for sent in sents:
        token = nltk.word_tokenize(sent)
        tagged_token = pos_tag(token)
        tree = ne_chunk(tagged_token, binary=True)
        chunks.append(tree)
    return chunks

def get_vars(text, info, Ppos, Pos, boo):
    if boo == "TRUE":
        var = [0, 0, len(info[1]), Ppos, Pos, 1]
    else:
        var = [0, 0, len(info[1]), Ppos, Pos, 0]
    sent_count = 0
    para_count = 0
    word_count = 0
    for i in range(len(chunk)):
        sent_count = 0
        for j in range(len(chunk[i])):
            if type(chunk[i][j]) is nltk.tree.Tree:
                sent_count += 1
                para_count += 1
                
                for k in chunk[i][j]:
                    if (is_match(k[0], info[0][0])):
                        word_count += 1
                        if word_count <= info[2]:
                            var[0] = para_count
                            var[1] = sent_count
            else:
                if chunk[i][j][1][0:2] == 'NN':
                    sent_count += 1
                    para_count += 1
                    if (is_match(chunk[i][j][0], info[0][0])):
                        word_count += 1
                        if word_count <= info[2]:
                            var[0] = para_count
                            var[1] = sent_count
                    
                

    return var    


tsv_file = open("gap-development.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
count = 0
data = []
for row in read_tsv:
    if count == 0:
        count +=1
        continue
#    num = row[0], text = row[1], pronoun row[2] pos row[3]
    prep = row[2].split(" ")
    Ppos = int(row[3])
    perA = row[4].split(" ")
    Apos = int(row[5])
    Aans = row[6]
    perB = row[7].split(" ")
    Bpos = int(row[8])
    Bans = row[9]
    Pord = find_ord(row[1], prep[0])
    Aord = find_ord(row[1], perA[0])
    Bord = find_ord(row[1], perB[0])
    target = [prep, Pord, get_nth(row[1], prep[0], Ppos, Pord)]
    first = [perA, Aord, get_nth(row[1], perA[0], Apos, Aord)]
    second = [perB, Bord, get_nth(row[1], perB[0], Bpos, Bord)]
    chunk = chunk_text(row[1])
    Avar = get_vars(row[1], first, Ppos, Apos, Aans)
    Bvar = get_vars(row[1], second, Ppos, Bpos, Bans)
    Avar.append(row[0])
    Bvar.append(row[0])
    data.append(Avar)
    data.append(Bvar)

    count+=1


tsv_file.close()


tsv_file = open("gap-test.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
count = 0
for row in read_tsv:
    if count == 0:
        count +=1
        continue
#    num = row[0], text = row[1], pronoun row[2] pos row[3]
    prep = row[2].split(" ")
    Ppos = int(row[3])
    perA = row[4].split(" ")
    Apos = int(row[5])
    Aans = row[6]
    perB = row[7].split(" ")
    Bpos = int(row[8])
    Bans = row[9]
    Pord = find_ord(row[1], prep[0])
    Aord = find_ord(row[1], perA[0])
    Bord = find_ord(row[1], perB[0])
    target = [prep, Pord, get_nth(row[1], prep[0], Ppos, Pord)]
    first = [perA, Aord, get_nth(row[1], perA[0], Apos, Aord)]
    second = [perB, Bord, get_nth(row[1], perB[0], Bpos, Bord)]
    chunk = chunk_text(row[1])
    Avar = get_vars(row[1], first, Ppos, Apos, Aans)
    Bvar = get_vars(row[1], second, Ppos, Bpos, Bans)
    Avar.append(row[0])
    Bvar.append(row[0])
    data.append(Avar)
    data.append(Bvar)

    count+=1


tsv_file.close()

tsv_file = open("gap-validation.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")
count = 0
for row in read_tsv:
    if count == 0:
        count +=1
        continue
#    num = row[0], text = row[1], pronoun row[2] pos row[3]
    prep = row[2].split(" ")
    Ppos = int(row[3])
    perA = row[4].split(" ")
    Apos = int(row[5])
    Aans = row[6]
    perB = row[7].split(" ")
    Bpos = int(row[8])
    Bans = row[9]
    Pord = find_ord(row[1], prep[0])
    Aord = find_ord(row[1], perA[0])
    Bord = find_ord(row[1], perB[0])
    target = [prep, Pord, get_nth(row[1], prep[0], Ppos, Pord)]
    first = [perA, Aord, get_nth(row[1], perA[0], Apos, Aord)]
    second = [perB, Bord, get_nth(row[1], perB[0], Bpos, Bord)]
    chunk = chunk_text(row[1])
    Avar = get_vars(row[1], first, Ppos, Apos, Aans)
    Bvar = get_vars(row[1], second, Ppos, Bpos, Bans)
    Avar.append(row[0])
    Bvar.append(row[0])
    data.append(Avar)
    data.append(Bvar)

    count+=1


tsv_file.close()


print(len(data))
g = open('snippet.csv', 'w', newline = '')
wr = csv.writer(g)


for i in data:
    wr.writerow([i[0], i[1], i[2], i[3], i[4], i[5], i[6]])

g.close()


