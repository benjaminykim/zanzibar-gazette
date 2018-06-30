from autocorrect import spell
import re
import sys

corrections = {}
revisions = 0

def load_dictionary():
    dictionary = open("dictionary.txt", 'r')
    for line in dictionary:
        pair = line.split()
        corrections[pair[0]] = pair[1]

def arguments(args):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", type=str, default=None, nargs="+", help="files to process, no extension as .txt assumed")
    args = parser.parse_args(args=args)
    return args

def main(args=None):
    process_files(arguments(args))

def process_files(args):
    def write(word, revision, outputFile, revisedLog):
        global revisions
        if word != revision:
            outputFile.write(revision.upper() + " ")
            revisedLog.write(revision + " " + word + "\n")
            revisions += 1
        else:
            outputFile.write(word + " ")

    for fileName in args.files:
        inputFile = open(fileName + '.txt', 'r')
        outputFile = open(fileName + 'Revised.txt', 'w')
        revisedLog = open(fileName + 'RevisedLog.txt', 'w')

        revisedLog.write("revised   word\n")
        cache = ""
        carryOver = False

        for line in inputFile:
            words = line.split()
            for word in words:

                word = (re.sub('[^A-Za-z0-9\-]+', '', word)).lower()
                """
                    this checks to see if there is a carry over. If not, then check if carryovers or
                    hyphened dual words exist ("well-stocked" is a hyphened dual word).
                """
                if carryOver:
                    carryOver = False
                    word = cache + word
                    cache = ""
                else:
                    """
                    the following block of code checks if there is a hyphen after
                    the word in check. If there is, the word can either be a broken
                    single word or a hyphened dual word. Hyphened dual words that are split
                    by a line break are considered to be single words due to fringe cases
                    """
                    if word == "":
                        continue
                    if "-" in word:
                        # there is a hyphen in the word
                        if word[0] == "-":
                            continue
                        elif word[-1] == "-" and word == words[-1]:
                            carryOver = True
                            cache = word[:-1]
                            continue
                        else:
                            dualWord = word.split("-")
                            firstWord = dualWord[0]
                            secondWord = dualWord[1]
                            if len(firstWord) > 2 and len(secondWord) > 2:
                                word = spell_check(firstWord) + "-" + spell_check(secondWord)
                            else:
                                continue

                revision = spell_check(word)
                write(word, revision, outputFile, revisedLog)

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
