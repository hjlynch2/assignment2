import grid_parser as parser
from invalidLetters import InvalidLetters

class Grid:

    matrix = []
    words = {}
    wordsList = []

    # pass arbitrary copying in grid values
    def __init__(self, num, matrix = None, invalid = None, words = None, wordsList = None):
        if not matrix is None:
            self.matrix = matrix
            self.invalid = invalid
            self.words = words
            self.wordsList = wordsList
        else:
            self.matrix = parser.convert_to_matrix(num)
            self.wordsList = parser.get_words(num)
            self.wordsList.sort(key=len,reverse=True)
            for word in self.wordsList: 
            	self.words[word] = list(word)
            self.invalid = InvalidLetters(self.matrix)
        