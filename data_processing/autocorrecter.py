from autocorrect import spell
import re


fileName = 'gazette'
inputFile = open(fileName + '.txt', 'r')
words = inputFile.read().split()
outputFile = open(fileName + 'SpellChecked.txt', 'w')
revisionFile = open(fileName + 'RevisedWords.txt', 'w')


revisions = 0

for word in words:
    word = re.sub('[^A-Za-z0-9]+', '', word)
    revision = spell(word)
    if revision == word:
        outputFile.write(word + " ")
    else:
        outputFile.write(revision + " ")
        revisions += 1
        revisionFile.write(revision + " " + word + " \n")



inputFile.close()
outputFile.close()
revisionFile.close()
print(revisions)
