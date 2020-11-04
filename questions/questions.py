import nltk
import sys
import math
import os

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename)) as f:
            #print(type(f.read()))
            files[filename] = f.read().replace('\n', ' ')
    #print(files)        
    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = [
        word.lower() for word in
        nltk.word_tokenize(document)
        if word.isalpha()
    ]
    #print(words)
    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    numDocs = len(documents.keys())
    idfValues = dict()
    for document in documents.keys():
        wordList = documents[document]
        for word in wordList:
            if word in idfValues.keys():
                continue
            else:
                count = 0
                for doc in documents.keys():
                    if word in documents[doc]:
                        count = count + 1
                if count is 0:
                    continue
                else:
                    idfValues[word] = math.log(numDocs / count)
    # for temp in idfValues.keys():
    #     print(temp)
    #     print(idfValues[temp])
    #print(idfValues[0])
    #print(idfValues[1])
    #print(idfValues[2])
    return idfValues


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    topFiles = dict()
    for file in files: 
        sum = 0
        for word in query:
            idf = idfs[word]
            tf = files[file].count(word)
            sum = sum + (tf * idf)
        topFiles[file] = sum
    topFiles = sorted(topFiles.keys(), key=lambda x: topFiles[x], reverse=True)
    #print(topFiles[0:n])
    topFiles = list(topFiles)
    return topFiles[0:n+1]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    topSentences = dict()
    for sentence in sentences:
        mwm = 0
        words = sentences[sentence]
        numWords = len(words)
        qtd = 0
        for word in query:
            if word in words:
                qtd = qtd + words.count(word)
                mwm = mwm + idfs[word]
        qtd = qtd / numWords        
        topSentences[sentence] = [mwm, qtd]

    topSentences = sorted(topSentences.keys(), key=lambda x: topSentences[x], reverse=True)   
    topSentences = list(topSentences)

    return topSentences[0:n]

if __name__ == "__main__":
    main()
