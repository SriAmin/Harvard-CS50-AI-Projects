# Harvard-CS50-AI-Projects
These are the project files submitted for Harvard's CS50 Introduction to Artificial Intelligence.
All these resources and projects is thanks to Harvard University for providing this free online course. The following is a link to the webpage of their free online course and projects.
https://cs50.harvard.edu/ai/2020/

## Degrees
This uses breadth-first search to find the shortest link between two actors within the database. Similar to [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon)

To execute it type the following in a bash terminal

```bash
python3 degrees.py large
```
You can either use large or small, small is a smaller dataset meaning it'll won't take as long to return a link.

## Tic-Tac-Toe
Uses minimax algorithm to create an AI that will play against you in a game of tic tac toe, trying to find the best possible move. It doesn't always win but it does push back.

```bash
python3 runner.py
```

## Knights
Solves the classic Knights and Knaves logic puzzles using proportional logic, with a given set of problems.

```bash
python3 puzzle.py
```

## Minesweeper
A simulator of the game MineSweeper but allows the player to let the AI make the best move using proportional logic and knowledge representation of the game board.

```bash
python3 runner.py
```

## PageRank
An AI that uses the random surfer and interative algorithm to rank webpages by important similar to how Google ranks their pages, but with a much small dataset

```bash
python3 pagerank.py corpus0
```
Corpus is the dataset of webpages, their are 3 corpus (corpus0 - corpus2)

## Heredity
An AI that determines the likelihood that a person has a genetic trait using probability distribution

```bash
python3 heredity.py data/family0.csv
```
Currently there is family0.csv, family1.csv, and family2.csv in the data folder

## Crossword
An AI that uses constraint statification along with node consistency and arch consistency to generate a complete crossword puzzle with a given structure and dateset of words to place in the puzzle.

```bash
python3 generate.py data/structure1.txt data/words1.txt output.png
```
Currently there is structure0.txt, structure1.txt, structure2.txt along with words0.txt, words1.txt, words2.txt. An image of the puzzle will be named as output.png

## Shopping
Uses machine learning to determine if online shoppers will complete their purchase or leave it

```bash
python3 shopping.py shopping.csv
```

## Nim
Uses reinforcement learning through playing 1000 games to play against the player in a classic game of [Nim](https://en.wikipedia.org/wiki/Nim). Through it's learning algorithm it wins almost every game against the player.

```bash
python3 play.py
```

## Parser
Program that will parse english sentences and extract noun phrases displaying them to the user using context-free grammer formalism.

```bash
python3 parser.py
```

## Questions
An AI that uses the python package td-idf to rank pages of information based on frequency and will return answers to question submitted by the users on the CLI.

```bash
python3 questions.py corpus
```
