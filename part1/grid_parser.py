def convert_to_matrix(num):
    file = open('./grids/grid' + num + '.txt')
    lines = file.readlines()
    res = [] # Res is a 2D array representing the maze
    for line in lines:
        to_add = " ".join(line.splitlines())
        res.append(list(to_add))
    return res

def get_words(num):
    file = open('./wordBanks/bank' + num + '.txt')
    lines = file.readlines()
    words = []
    for line in lines:
        words.append(line.strip().upper())
    return words
