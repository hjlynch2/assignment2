import copy

class InvalidLetters:

    rows = [set() for _ in xrange(9)]
    columns = [set() for _ in xrange(9)]
    smallGrids = [set() for _ in xrange(9)]

    def __init__(self, matrix, rows = None, columns = None, smallGrids = None):
        if rows == None:
            for curr_row in range(0,9):
                for curr_col in range(0,9):
                    curr_letter = matrix[curr_row][curr_col]
                    notBlank = not curr_letter == '_'
                    if notBlank:
                        self.rows[curr_row].add(curr_letter)
                    if curr_row/3 == 0 and curr_col/3 == 0 and notBlank: #3x3 grid 0
                        self.smallGrids[0].add(curr_letter)
                    elif curr_row/3 == 0 and curr_col/3 == 1 and notBlank: #3x3 grid 1
                        self.smallGrids[1].add(curr_letter)
                    elif curr_row/3 == 0 and curr_col/3 == 2 and notBlank: #3x3 grid 2
                        self.smallGrids[2].add(curr_letter)
                    elif curr_row/3 == 1 and curr_col/3 == 0 and notBlank: #3x3 grid 3
                        self.smallGrids[3].add(curr_letter)
                    elif curr_row/3 == 1 and curr_col/3 == 1 and notBlank: #3x3 grid 4
                        self.smallGrids[4].add(curr_letter)
                    elif curr_row/3 == 1 and curr_col/3 == 2 and notBlank: #3x3 grid 5
                        self.smallGrids[5].add(curr_letter)
                    elif curr_row/3 == 2 and curr_col/3 == 0 and notBlank: #3x3 grid 6
                        self.smallGrids[6].add(curr_letter)
                    elif curr_row/3 == 2 and curr_col/3 == 1 and notBlank: #3x3 grid 7
                        self.smallGrids[7].add(curr_letter)
                    elif curr_row/3 == 2 and curr_col/3 == 2 and notBlank: #3x3 grid 8
                        self.smallGrids[8].add(curr_letter)
            for curr_col in range(0,9):
                self.columns.append(set())
                for curr_row in range(0,9):
                    if not matrix[curr_row][curr_col] == '_':
                        self.columns[curr_col].add(matrix[curr_row][curr_col])
        else:
            self.rows = copy.deepcopy(rows)
            self.columns = copy.deepcopy(columns)
            self.smallGrids = copy.deepcopy(smallGrids)

    def get_grid_num(self, row, col):
        y = row / 3
        x = col / 3
        return y * 3 + x
