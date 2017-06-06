import csv

def getDocumentVector(document, totalWords, all_words_list):
    wordArr = document.split(" ")
    wordList = {}
    docVector = []
    for word in all_words_list:
        if word in wordArr:
            if word in wordList:
                wordList[word] = wordList[word] + 1
            else:
                wordList[word] = 1
        else:
            wordList[word] = 0
    for key in wordList:
        docVector.append(wordList[key])
    return docVector


def removeChars(word):
    chars = ["/", "(", ")", "&", "+", "-"]
    for char in chars:
        word = word.replace(char, "")
    word = word.lower()
    return word


if __name__ == '__main__':

    all_words_list = {}
    with open('products.csv') as ifile:
        read = csv.reader(ifile)
        for row in read:
            row[0] = row[0].replace("/", "")
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
    for key in all_words_list:
        print key
    print len(all_words_list)
    print getDocumentVector('Aqua Asus', m, all_words_list)