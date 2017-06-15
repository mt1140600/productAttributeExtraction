import csv
import math
import numpy as np
import operator
import enchant
np.set_printoptions(threshold=np.nan)
from pymongo import MongoClient
import psycopg2
import pickle

corpus = []
all_words_list = {}
idf_list = {}

def scalarProduct(vectorA, vectorB):
    modA = math.sqrt(sum(map(lambda x:x*x,vectorA)))
    modB = math.sqrt(sum(map(lambda x:x*x,vectorB)))
    dotProd = np.dot(vectorA, vectorB)
    if modA ==0 or modB ==0:
        return 0
    return (dotProd)


def editDistDP(str1, str2):
    m = len(str1)
    n = len(str2)
    dp = [[0 for x in range(n+1)] for y in range(m+1)]
    for i in range(m+1):
        for j in range(n+1):
            if (i == 0):
                dp[i][j] = j
            elif (j == 0):
                dp[i][j] = i
            elif (str1[i-1] == str2[j-1]):
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j], dp[i-1][j-1])

    return dp[m][n]

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
   docVector = []
   for word in all_words_list:
       if word in temp:
           wordList[word] = temp[word]*idf_list[word]
       else:
           wordList[word] = 0
       all_words_list[word] = wordList[word]

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
    queryVector = getDocumentVector(query, all_words_list, idf_list)
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        for row in read:
            name = removeChars(row[0].lower())
            documentVector = getDocumentVector(name, all_words_list, idf_list)
            productsList[row[0]] = scalarProduct(documentVector, queryVector)
    return productsList


def sortDict(dictionary):
    dictionary = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    temp = {}
    n = len(dictionary)
    for i in range(n):
        temp[dictionary[i][0]] = dictionary[i][1]
    return temp


def spellCheck(queryWord, dict):
    queryWord = queryWord.lower()
    suggestions = dict.suggest(queryWord)
    suggestions = map(lambda x : x.lower(), suggestions)
    suggestions = sorted(suggestions)
    print suggestions
    optDist = 5
    ind = 0
    if len(suggestions)==0:
        return queryWord
    elif len(suggestions)>1:
        for i in range(len(suggestions)):
            dist = editDistDP(queryWord, suggestions[i])
            if (dist<optDist):
                optDist = dist
                ind = i
                # print optDist
    return suggestions[ind]


def queryCorrector(query, dict):
    query = removeChars(query)
    wordArr = query.split()
    str = ""
    for i in range(len(wordArr)):
        wordArr[i] = spellCheck(wordArr[i], dict)
        str = str + wordArr[i]+" "
    return str

def save_model(file_name, model_list):
    with open(file_name, 'wb') as fid:
        pickle.dump(model_list, fid)


def load_model(file_name):
    with open(file_name, 'rb') as fid:
        model = pickle.load(fid)
    return model


def convertUrlToAttribute(url):
    if 'product/' in url:
        newUrl = url.split('product/')[1]
        return ['product',newUrl]
    elif 'cart/' in url:
        newUrl = url.split('cart/')[1]
        return ['cart', newUrl]


def issubseq(str1, str2):
    m = len(str1)
    n = len(str2)
    i=0
    for j in range(n):
        if str1[i]==str2[j]:
            i = i+1
            if i==m:
                return True
    return False

if __name__ == '__main__':
    # con = psycopg2.connect("dbname='prokure' user='postgres'")
    # cur = con.cursor()
    # cur.execute("SELECT * FROM all_data")
    # rows = cur.fetchall()
    # popularity = {}
    # client = MongoClient('10.240.0.9')
    # db = client.prokure2
    # pincodedetails = db.productfinals
    # productsMap = {}
    #
    # for row in pincodedetails.find():
    #     productsMap[row['product_id'].__str__()] = row['name']
    #     productsMap[row['_id']] = row['name']
    # for row in rows:
    #     details = convertUrlToAttribute(row[3])
    #     if details:
    #         if details[1] in productsMap:
    #             if productsMap[details[1]] in popularity:
    #                 if details[0]=='cart':
    #                     popularity[productsMap[details[1]]] = popularity[productsMap[details[1]]]+5
    #                 else:
    #                     popularity[productsMap[details[1]]] = popularity[productsMap[details[1]]] + 2
    #             else:
    #                 if details[0] == 'cart':
    #                     popularity[productsMap[details[1]]] = 5
    #                 else:
    #                     popularity[productsMap[details[1]]] = 2
    #
    #         else:
    #             if details[1] in popularity:
    #                 if details[0]=='cart':
    #                     popularity[details[1]] = popularity[details[1]]+5
    #                 else:
    #                     popularity[details[1]] = popularity[details[1]] + 2
    #             else:
    #                 if details[0] == 'cart':
    #                     popularity[details[1]] = 5
    #                 else:
    #                     popularity[details[1]] = 2


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
    # print all_words_list
    all_words_list = sortDict(all_words_list)
    # newlist = sorted(newlist.items(), key=operator.itemgetter(1), reverse=True)
    # all_words_list = sorted(all_words_list.iterkeys())
    # print all_words_list
    pwl = enchant.request_pwl_dict("big.txt")
    print('enter query')
    a = raw_input()
    a = queryCorrector(a, pwl)
    print type(a)
    print a
    x = getRelativeDocs(a, all_words_list, idf_list)
    # x = sorted(x.items(), key=operator.itemgetter(1), reverse=True)[:30]
    # newList = {}
    # for i in range(30):
    #     print str(x[i][0])+' '+str(x[i][1])
        # newList[x[i][0]] = popularity[x[i][0]]
    # newList = sorted(newList.items(), key=operator.itemgetter(1), reverse=True)
    # for i in range(30):
    #     flag = True
    #     arr = a.split()
    #     for word in arr:
    #         flag = flag and issubseq(word, newList[i][0].lower())
    #     if flag:
    #         print newList[i][0]

