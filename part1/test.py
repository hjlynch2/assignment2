from grid import Grid
from back_tracking import backTrack
from invalidLetters import InvalidLetters

test = Grid('2')
invalid = InvalidLetters(test.matrix)

matrix = []
words = test.words
for row in test.matrix:
    matrix.append(row)

results = backTrack(test)
nodesExpanded = results[0]
validGrid = results[1]
wordAssignments = results[2]
timeTaken = results[3]

print "\nValid Grid: "
for row in validGrid:
    print row

print "\nWord Assignment"
for word in wordAssignments:
	print word[0] + " - (" + word[1] + ", " + word[2] + ") - " + word[3] 

print "\nStats:"
print timeTaken
print "Nodes expanded: " + str(nodesExpanded)