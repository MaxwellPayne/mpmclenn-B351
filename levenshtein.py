import numpy

class Levenshtein():
    def __init__(self, horizWord, vertWord):
        self._rows, self._cols = len(vertWord) + 1, len(horizWord) + 1
        self._horizWord, self._vertWord = horizWord, vertWord
        # word1 is vertical, word2 is horizontal
        self._bottomRight = (self._rows - 1, self._cols - 1)
        self.isSolved, self._matrix = None, None
        self._initMatrix()

    def _initMatrix(self):
        self._matrix = numpy.zeros([self._rows, self._cols], dtype=int)
        for x in xrange(self._cols):
            # set all the horizWord to their index
            self._matrix[0][x] = x
        for y in xrange(self._rows):
            # set all the vertWord to their index 
            self._matrix[y][0] = y
        self.isSolved = False

    def __str__(self):
        return self._matrix.__str__()

    def _setCellVal(self, index):
        x, y = index
        mat = self._matrix
        if x == 0:
            val = y
        elif self._horizWord[x - 1] == self._vertWord[y - 1]:
            # letters match, return top left cost
            val = mat[y - 1][x - 1]
        else:
            val = min(mat[y - 1][x - 1], mat[y - 1][x], mat[y][x - 1]) + 1
            # min of (upper left, upper, left) + 1
        mat[y][x] = val

    def _fillMatrix(self):
        from itertools import izip, cycle, chain, repeat

        # iterate column by column and compute the cells
        for x, y in izip(chain.from_iterable((repeat(x, self._rows - 1) for x in xrange(1, self._cols))), cycle(xrange(1, self._rows))):
            # set the cell val based on the previously computed cell vals/character match
            self._setCellVal((x, y))

    def distance(self):
        # return the Levenshtein Distance
        if not self.isSolved:
            self._fillMatrix()
        return self._matrix[self._bottomRight]

def _main():
    x = LevMatrix("SATURDAY", "SUNDAY")
    print x.distance()
    #print x

if __name__ == '__main__':
    _main()
