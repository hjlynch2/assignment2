import time
from grid import Grid
import copy
from invalidLetters import InvalidLetters
from Queue import PriorityQueue

def backTrack(wordGrid):
    start = time.time()

    assignmentStack = []
    grid = wordGrid.matrix
    initialWords = wordGrid.wordsList
    invalid = wordGrid.invalid

    assignmentStack.append(wordGrid)

    nodesExpanded = 0

    while not len(assignmentStack) == 0:
        word_grid = assignmentStack.pop()
        grid = word_grid.matrix
        words = word_grid.words
        wordsList = word_grid.wordsList
        invalid = word_grid.invalid

        if len(wordsList) == 0 and assignmentComplete(invalid):
            wordDict = getWordPlacement(grid, initialWords)
            return (nodesExpanded, grid, wordDict, time.time() - start)

        currWord = wordsList[0]
        toAdd = PriorityQueue()

        for col in range(0,9):
            for row in range(0,9):
                downValid = checkValidPlacement(grid, invalid, currWord, True, row, col)
                acrossValid = checkValidPlacement(grid, invalid, currWord, False, row, col)
                if acrossValid or downValid:
                    # copy of words list with curr word deleted
                    deletedWord = deleteWord(currWord, words, wordsList)
                    newWords = deletedWord[0]
                    newWordsList = deletedWord[1]
                    if downValid: # add into the grid, update word lists, and push onto the stack
                        restrictionsAdded = calculateRestrictions(invalid, currWord, row, col, True)
                        newGrid = placeWord(grid, invalid, currWord, row, col, True)
                        newMatrix = newGrid[0]
                        newInvalid = newGrid[1]
                        newWordGrid = Grid(0,newMatrix,newInvalid,newWords,newWordsList)
                        nodesExpanded = nodesExpanded + 1
                        toAdd.put((restrictionsAdded, newWordGrid))
                    if acrossValid:
                        restrictionsAdded = calculateRestrictions(invalid, currWord, row, col, True)
                        newGrid = placeWord(grid, invalid, currWord, row, col, False)
                        newMatrix = newGrid[0]
                        newInvalid = newGrid[1]
                        newWordGrid = Grid(0,newMatrix,newInvalid,newWords,newWordsList)
                        nodesExpanded = nodesExpanded + 1
                        toAdd.put((restrictionsAdded, newWordGrid))

        while not toAdd.empty():
            popped = toAdd.get()
            assignmentStack.append(popped[1])

def printGrid(grid):
    for row in grid:
        print ''.join(row)

def deleteWord(word, words, wordsList):
    wordsCopy = copy.deepcopy(words)
    wordsListCopy = copy.deepcopy(wordsList)
    wordsListCopy.remove(word)
    del wordsCopy[word]
    return (wordsCopy, wordsListCopy)

def placeWord(grid, invalid, word, start_row, start_col, down):
    gridCopy = copy.deepcopy(grid)
    invalidCopy = InvalidLetters(grid, invalid.rows, invalid.columns, invalid.smallGrids)
    if down:
        letterIt = 0
        for row in range(start_row, start_row + len(word)):
            currLetter = word[letterIt]
            gridNum = invalidCopy.get_grid_num(row, start_col)
            gridCopy[row][start_col] = currLetter
            invalidCopy.rows[row].add(currLetter)
            invalidCopy.columns[start_col].add(currLetter)
            invalidCopy.smallGrids[gridNum].add(currLetter)
            letterIt = letterIt + 1
    else:
        letterIt = 0
        for col in range(start_col, start_col + len(word)):
            currLetter = word[letterIt]
            gridNum = invalid.get_grid_num(start_row, col)
            gridCopy[start_row][col] = word[letterIt]
            invalidCopy.rows[start_row].add(currLetter)
            invalidCopy.columns[col].add(currLetter)
            invalidCopy.smallGrids[gridNum].add(currLetter)
            letterIt = letterIt + 1
    return (gridCopy, invalidCopy)


def calculateRestrictions(invalid, currWord, row, col, down):
    restrictions = 0
    if down:
        for letter in currWord:
            gridNum = invalid.get_grid_num(row, col)
            if not letter in invalid.rows[row]:
                restrictions = restrictions + 1
                continue
            if not letter in invalid.columns[col]:
                restrictions = restrictions + 1
                continue
            if not letter in invalid.smallGrids[gridNum]:
                restrictions = restrictions + 1
                continue
            row = row + 1
    else:
        for letter in currWord:
            gridNum = invalid.get_grid_num(row, col)
            if not letter in invalid.rows[row]:
                restrictions = restrictions + 1
                continue
            if not letter in invalid.columns[col]:
                restrictions = restrictions + 1
                continue
            if not letter in invalid.smallGrids[gridNum]:
                restrictions = restrictions + 1
                continue
            col = col + 1
    return restrictions

# checks if the current assignment is complete
def assignmentComplete(invalid):
    for row in range(0,9):
        if not len(invalid.rows[row]) == 9:
            return False
    for col in range(0,9):
        if not len(invalid.columns[col]) == 9:
            return False
    return True

# checks if the current assignment is complete
def getNumFilled(invalid):
    totalFilled = 0
    for row in invalid.rows:
        totalFilled += len(row)
    for col in invalid.columns:
        totalFilled += len(col)
    totalFilled /= 2
    return totalFilled

def checkValidPlacement(matrix, invalid, word, down, start_row, start_col):
    letters = list(word)

    #if word is oriented down, should follow same pattern as below
    if down:
        if len(word) + start_row > 9:
            return False

        #check rows
        letterIt = 0
        for row in range(start_row,start_row + len(word)):
            curr_space = matrix[row][start_col]
            curr_letter = letters[letterIt]
            if curr_letter in invalid.rows[row] and not curr_space == curr_letter:
                return False
            if not curr_space == '_' and not curr_space == curr_letter:
                return False
            gridNum = invalid.get_grid_num(row, start_col)
            if curr_letter in invalid.smallGrids[gridNum] and not curr_space == curr_letter:
                return False
            letterIt += 1

        #check columns
        row = start_row
        for curr_letter in letters:
            if curr_letter in invalid.columns[start_col] and not curr_letter == matrix[row][start_col]:
                return False
            row += 1

    else: #if word is oriented across
        if len(word) + start_col > 9:
            return False

        #check columns
        letterIt = 0
        for col in range(start_col,start_col + len(word)):
            curr_space = matrix[start_row][col]
            curr_letter = letters[letterIt]
            if curr_letter in invalid.columns[col] and not curr_space == curr_letter:
                return False
            if not curr_space == '_' and not curr_space == curr_letter:
                return False
            gridNum = invalid.get_grid_num(start_row, col)
            if curr_letter in invalid.smallGrids[gridNum] and not curr_space == curr_letter:
                return False
            letterIt += 1

        #check row
        col = start_col
        for curr_letter in letters:
            if curr_letter in invalid.rows[start_row] and not curr_letter == matrix[start_row][col]:
                return False
            col += 1

    return True

def getWordPlacement(grid, wordsList):
    wordDict = {}
    wordAssignments = []
    for word in wordsList:
        letterIt = 0
        start_row = -1
        start_col = -1
        wordFound = False
        for row in range(0,9):
            for col in range(0,9):
                if not grid[row][col] == word[letterIt]:
                    letterIt = 0
                    start_row = -1
                    start_col = -1
                    continue
                if grid[row][col] == word[letterIt]:
                    if letterIt == 0:
                        start_row = row
                        start_col = col
                    letterIt = letterIt + 1
                if letterIt >= len(word):
                    wordFound = True
                    wordDict[word] = (start_row, start_col, "across")
                    break
            if wordFound:
                break
                letterIt = 0
        if wordFound:
            continue
        start_row = -1
        start_col = -1
        wordFound = False
        for col in range(0,9):
            for row in range(0,9):
                if not grid[row][col] == word[letterIt]:
                    letterIt = 0
                    start_row = -1
                    start_col = -1
                if grid[row][col] == word[letterIt]:
                    if letterIt == 0:
                        start_row = row
                        start_col = col
                    letterIt = letterIt + 1
                if letterIt >= len(word):
                    wordFound = True
                    wordDict[word] = (start_row, start_col, "across")
                    break
            if wordFound:
                break
    for word in wordsList:
        row = str(wordDict[word][0])
        col = str(wordDict[word][1])
        orientation = str(wordDict[word][2])
        wordAssignments.append((word, row, col, orientation))
    return wordAssignments