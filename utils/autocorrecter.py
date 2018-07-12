import re
import sys
import os
from autocorrect import spell

corrections = {}
revisions = 0

def load_dictionary(dir):
    dictionary = open(dir, 'r')
    for line in dictionary:
        pair = line.split()
        corrections[pair[0]] = pair[1]

def arguments(args):
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-f", dest="files", type=str, default=None, help="files to process .txt assumed")
    parser.add_argument("-d", dest="dictionary", type=str, default="/dictionary.txt", help="filepath of dictionary")
    parser.add_argument("--dir", dest="data_dir", type=str, default="/data", help="filepath of data directory")
    args = parser.parse_args(args=args)
    return args

def main(args=None):
    process_files(arguments(args))

def process_files(args):
    # assign all parsed arguments
    files = None
    dict_dir = args.dictionary
    data_dir = args.data_dir

    if not files:
        files = []
        for file in os.listdir(data_dir):
            if file.endswith(".txt"):
                files.append(file)

    # load dictionary
    load_dictionary(dict_dir)

    # set up directories for data storage
    revised_dir = data_dir + "/revised"
    revised_log_dir = data_dir + "/log"

    # create revised txt file directory
    if not os.path.exists(revised_dir):
        os.makedirs(revised_dir)

    # create revised log txt file directory
    if not os.path.exists(revised_log_dir):
        os.makedirs(revised_log_dir)

    # helper function to write to appropriate files
    def write(word, revision, outputFile, revisedLog):
        global revisions
        if word != revision:
            outputFile.write(revision.upper() + " ")
            revisedLog.write(revision + " " + word + "\n")
            revisions += 1
        else:
            outputFile.write(word + " ")

    # process all text data in files
    for fileName in files:
        fileName = fileName[:-4]
        inputFile = open(data_dir + "/" + fileName + '.txt', 'r')
        outputFile = open(revised_dir + "/" + fileName + 'Revised.txt', 'w')
        revisedLog = open(revised_log_dir + "/" + fileName + 'Log.txt', 'w')

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
    sys.exit(main())
