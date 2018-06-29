from autocorrect import spell
import re
import sys

corrections = {}

def load_dictionary():
    dictionary = open("dictionary.txt", 'r')
    for line in dictionary:
        pair = line.split()
        corrections[pair[0]] = pair[1]


def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=str, default=None, nargs="+", help="files to process, no extension as .txt assumed")

    args = parser.parse_args(args=args)

    for fileName in args.files:
        inputFile = open(fileName + '.txt', 'r')
        outputFile = open(fileName + 'Revised.txt', 'w')
        revisedLog = open(fileName + 'RevisedLog.txt', 'w')

        revisedLog.write("revised   word\n")
        revisions = 0

        cache = ""
        carryOver = False

        for line in inputFile:
            for word in line.split():
                if carryOver:
                    carryOver = False
                    word = cache + word
                    cache = ""

                if word[-1] == "-":
                    carryOver = True
                    cache = word[:-1]
                    continue

                word = (re.sub('[^A-Za-z0-9]+', '', word)).lower()
                revision = spell_check(word)
                if revision == word:
                    outputFile.write(word + " ")
                else:
                    outputFile.write(revision.upper() + " ")
                    revisions += 1
                    revisedLog.write(revision + " " + word + " \n")
            outputFile.write("\n")

        inputFile.close()
        outputFile.close()
        revisedLog.close()
        print(revisions)

def spell_check(word):
    if word in corrections:
        return corrections[word]
    return spell(word)


if __name__ == '__main__':
    load_dictionary()
    sys.exit(main())
