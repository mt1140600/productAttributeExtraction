import csv
import math
import numpy as np

import operator
np.set_printoptions(threshold=np.nan)

def scalarProduct(vectorA, vectorB):
    modA = math.sqrt(sum(map(lambda x:x*x,vectorA)))
    modB = math.sqrt(sum(map(lambda x:x*x,vectorB)))
    dotProd = np.dot(vectorA, vectorB)
    if modA ==0 or modB ==0:
        return 0
    return (dotProd)/(modA*modB)

def getDocumentVector(document, all_words_list):
   wordArr = document.split(" ")
   n=len(all_words_list)
   if len(wordArr)==0:
       return np.zeros(n)
   wordList = {}
   temp = {}
   for word in wordArr:
       if word in temp:
           temp[word] = temp[word]+1
       else:
           temp[word] = 1
   mod = math.sqrt(sum(map(lambda x: x*x, temp.values())))
   docVector = []
   for word in all_words_list:
       if word in temp:
           wordList[word] = temp[word]
       else:
           wordList[word] = 0
       # print word
       # print wordList[word]

   for key in wordList:
       docVector.append(wordList[key])
   return np.array(docVector)/mod

def removeChars(word):
    chars = ["/", "(", ")", "&", "+", "-"]
    for char in chars:
        word = word.replace(char, "")
    word = word.lower()
    return word

def idf(word, corpus):
    docNum = len(corpus)
    df = 0.0
    for document in corpus:
        if word in document:
            df = df + 1
            # print df
    if df == 0 :
        return 0
    return (math.log(docNum/df, 2))

def combineTFIDF(tf, idf):
    return np.dot(tf, idf)


def getRelativeDocs(query, all_words_list):
    productsList = {}
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        for row in read:
            name = removeChars(row[0].lower())
            documentVector = getDocumentVector(name, all_words_list)
            queryVector = getDocumentVector(query, all_words_list)
            productsList[row[0]] = scalarProduct(documentVector, queryVector)
    return productsList


if __name__ == '__main__':
    corpus = []
    all_words_list = {}
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        docCount = 0
        for row in read:
            corpus.append(row[0].lower())
            docCount=docCount+1
            words = row[0].split()
            n = len(words)
            for word in words:
                word = removeChars(word)
                if word:
                    if word in all_words_list:
                        all_words_list[word] = all_words_list[word] + 1
                    else:
                        all_words_list[word] = 1

    m = len(all_words_list)
    all_words_list = sorted(all_words_list.iterkeys())
    # for key in all_words_list:
    #     print key
    # print len(all_words_list)
    # print (getDocumentVector('', all_words_list))
    # print idf('imported', corpus)
    # print len(all_words_list)
    # x = getRelativeDocs('back cover', all_words_list)
    # sorted_x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    # for i in range(len(sorted_x)):
    #     print str(sorted_x[i][0])+"  "+str(sorted_x[i][1])
