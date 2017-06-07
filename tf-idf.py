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
    return (dotProd)

def removeChars(word):
    chars = ["/", "(", ")", "&", "+", "-"]
    for char in chars:
        word = word.replace(char, " ")
    word = word.lower()
    return word


def getDocumentVector(document, all_words_list, idf_list):
   document = document.lower()
   document = removeChars(document)
   wordArr = document.split()
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
   # maxValue = max(temp.iteritems(), key = operator.itemgetter(1))[0]
   # print temp[maxValue]
   # for key in temp:
   #     temp[key] = 1.0+math.log(temp[key],2)
   docVector = []
   for word in all_words_list:
       if word in temp:
           wordList[word] = temp[word]*idf_list[word]
       else:
           # flag = ''
           # for key in temp:
           #     try:
           #         n = word.index(key)
           #         flag = key
           #     except:
           #         n=-1
           # if not n==-1:
           #     wordList[word] = temp[flag]*idf_list[word]
           # else:
           wordList[word] = 0

   for key in wordList:
       docVector.append(wordList[key])
   return np.array(docVector)


def idf(word, corpus):
    docNum = len(corpus)
    df = 0.0
    for document in corpus:
        if word in document:
            df = df + 1
    if df == 0 :
        return 0
    return (math.log(docNum/df, 2))


def getRelativeDocs(query, all_words_list, idf_list):
    productsList = {}
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        for row in read:
            name = removeChars(row[0].lower())
            documentVector = getDocumentVector(name, all_words_list, idf_list)
            queryVector = getDocumentVector(query, all_words_list, idf_list)
            productsList[row[0]] = scalarProduct(documentVector, queryVector)
    return productsList


if __name__ == '__main__':
    corpus = []
    all_words_list = {}
    idf_list = {}
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        for row in read:
            corpus.append(removeChars(row[0].lower()))
            row[0] = removeChars(row[0])
            words = row[0].split()
            n = len(words)
            for word in words:
                if word:
                    if word in all_words_list:
                        all_words_list[word] = all_words_list[word] + 1
                    else:
                        all_words_list[word] = 1
        for word in all_words_list:
            idf_list[word] = idf(word, corpus)
    m = len(all_words_list)
    all_words_list = sorted(all_words_list.iterkeys())

    # print all_words_list
    x = getRelativeDocs('sr 374', all_words_list, idf_list)
    x =  sorted(x.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(50):
        print str(x[i][0])+"   "+str(x[i][1])