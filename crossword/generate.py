import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain in self.domains.keys():
            removeWord = []
            for word in self.domains[domain]:
                if domain.length != len(word):
                    removeWord.append(word)
            for word in removeWord:
                self.domains[domain].remove(word)            

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]

        if overlap is None:
            return False
        else:
            i = overlap[0]
            j = overlap[1]
            removeWords = []

            for wordX in self.domains[x]: 
                for wordY in self.domains[y]:
                    if wordX[i] == wordY[j]:
                        break
                else:
                    removeWords.append(wordX)
                    #self.domains[x].remove(wordX)
                    revised = True

            for word in removeWords:
                self.domains[x].remove(word)    

            return revised            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = []
            for x in self.domains.keys():
                for y in self.domains.keys():
                    if x != y:
                        queue.append((x, y))
        else:
            queue = []
            for arc in arcs:
                queue.append(arc)

        while queue != None:
            arc = self.dequeue(queue)
            if (arc is not None):
                x = arc[0]
                y = arc[1]
                if self.revise(x, y):
                    if (len(self.domains[x]) == 0):
                        return False
                    for z in self.crossword.neighbors(x):
                        if z != y:
                            queue.append((z, x))
            else:
                break                
        return True                
    
    def dequeue(self, queue):
        for x, y in queue:
            queue.remove((x, y))
            return (x, y)

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for domain in self.domains.keys():
            if domain not in assignment.keys():
                return False
            else:
                if assignment[domain] is None:
                    return False    
        return True        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = []
        for key, val in assignment.items():
            if (val in values):
                return False
            else:
                values.append(val)
            
            if (key.length != len(val)):
                return False

            neighbourCells = self.crossword.neighbors(key)
            for neighbor in neighbourCells:
                overlap = self.crossword.overlaps[key, neighbor]
                if neighbor in assignment:
                    if assignment[neighbor][overlap[1]] != val[overlap[0]]:
                        return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = {}
        variables = self.domains[var]
        neighbors = self.crossword.neighbors(var)
        for variable in variables:
            if variable in assignment:
                continue
            else:
                count = 0
                for neighbor in neighbors:
                    if variable in self.domains[neighbor]:
                        count = count + 1
                values[variable] = count      
        return sorted(values, key=lambda key: values[key])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        degree = 0
        value = 10000
        for i in self.domains.keys():
            if i in assignment:
                continue
            else:
                if value > len(self.domains[i]):
                    value = len(self.domains[i])
                    variable = i
                    if self.crossword.neighbors(i) is None:
                        degree = 0
                    else:
                        degree = len(self.crossword.neighbors(i))
                elif value == len(self.domains[i]):
                    if self.crossword.neighbors(i) is not None:
                        if degree < len(self.crossword.neighbors(i)):
                            value = len(self.domains[i])
                            variable = i
                            degree = len(self.crossword.neighbors(i))
                        else:
                            variable = i
                            value = len(self.domains[i])
                            degree = 0    
        return variable        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
        return None            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
