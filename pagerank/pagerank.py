import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    keys = {}

    for i in corpus.keys():
        keys[i] = (1 - damping_factor) / len(corpus.keys())

    pageLinks = corpus[page]
    numLinks = len(pageLinks)

    if numLinks == 0:
        for i in keys.keys():
            keys[i] = keys[i] + (damping_factor / len(corpus.keys()))
            return keys

    for i in keys:
        keys[i] = keys[i] + float((damping_factor / numLinks))
    return keys   


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    randPage = random.randint(0, len(corpus.keys()) - 1)
    firstPage = list(corpus.keys())[randPage]
    keys = {}
    for i in corpus.keys():
        keys[i] = 0
    for i in range(0, n):
        keys[firstPage] = keys[firstPage] + 1 
        randInt = random.random()
        chances = transition_model(corpus, firstPage, damping_factor)
        for chance in chances.keys():
            if randInt > chances[chance]:
                randInt = randInt - chances[chance]
            else:
                firstPage = chance
                break

    normalize = sum(keys.values())
    for i in keys.keys():
        keys[i] = keys[i] / normalize            
    return keys


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    keys = {}
    for i in corpus.keys():
        keys[i] = 1 / len(corpus.keys())

    condition = True
    while condition:
        tempKeys = {}
        condition = False

        for i in keys.keys():
            temp = keys[i]

            tempKeys[i] = (1 - damping_factor / len(corpus.keys()))

            for page, link in corpus.items():
                if i in link:
                    tempKeys[i] = tempKeys[i] + (damping_factor * (keys[page] / len(link)))

            if (temp-tempKeys[i] > 0.001):
                condition = True 

        for i in keys.keys():
            keys[i] = tempKeys[i]            
    return keys

if __name__ == "__main__":
    main()
