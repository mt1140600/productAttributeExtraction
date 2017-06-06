
def getVector(document):
    wordArr = document.split(" ")
    wordList = {}
    for word in wordArr:
        if word in wordList:
            wordList[word] = wordList[word] + 1
        else:
            wordList[word] = 1
    n = len(wordList)
    print n
    return wordList

getVector('hey rghav dude dude jbkrj')