from itertools import chain

# enum for types of moves
class MOVES_T:
    nil = '\0'
    r = 'r'
    l = 'l'
    u = 'u'
    d = 'd'

class EightPuzzle(object):
    def __init__(self, nw, n, ne, w, c, e, sw, s, se, sure_cost=0, h_cost=0):

        values = tuple((nw, n, ne, w, c, e, sw, s, se))
        if set(values) != set((1, 2, 3, 4, 5, 6, 7, 8, " ")):
            raise ValueError("Must provide all tiles of an 8 puzzle")

        self._state = values
        self.sure_cost, self.h_cost = sure_cost, h_cost

        self._blank = -1
        # track the location of the blank
        for i, val in enumerate(values):
            if val == " ":
                self._blank = i
                break

        self.last_move = MOVES_T.nil
        # matrix-shaped representation of the state
        self._matrix = (self._state[:3], self._state[3:6], self._state[6:])

    @property
    def state(self):
        return self._state

    @property
    def matrix(self):
        return self._matrix
    
    @property
    def priority(self):
        # priority is the sum of known path and heuristic cost
        return self.sure_cost + self.h_cost

    def __hash__(self):
        return hash(''.join(map(str, self._state)))

    def __str__(self):
        return '\n'.join(map(lambda row: ', '.join(map(str, row)), self.matrix)) + '\n\n'

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        # two boards are equal if their states are the same
        return isinstance(other, self.__class__) and self.state == other.state

    def __cmp__(self, other):
        # EightPuzzle1 is < EightPuzzle2 if it has a lower priority
        return cmp(self.priority, other.priority if isinstance(other, self.__class__) else None)
    
    def _shifted(self, swap_index):
        # return a new instance with blank swapped at swap_index
        new_state = list(self._state)

        temp = new_state[swap_index]
        new_state[swap_index] = ' '
        new_state[self._blank] = temp

        return self.__class__(*new_state, sure_cost=self.sure_cost + 1)

    """right, left, up, and down return a new EightPuzzle with the blank
    shifted in their direction if the blank can be shifted that direction,
    otherwise they return None"""
    def right(self):
        if self._blank % 3 == 2:
            return None
        return self._shifted(self._blank + 1)

    def left(self):
        if self._blank % 3 == 0:
            return None
        return self._shifted(self._blank - 1)

    def up(self):
        if self._blank < 3:
            return None
        return self._shifted(self._blank - 3)

    def down(self):
        if self._blank > 5:
            return None
        return self._shifted(self._blank + 3)

    def backtrack(self):
        # return a new instance one move
        # before the current state
        mv = self.last_move
        if mv == MOVES_T.r:
            return self.left()
        elif mv == MOVES_T.l:
            return self.right()
        elif mv == MOVES_T.u:
            return self.down()
        elif mv == MOVES_T.d:
            return self.up()
        elif mv == MOVES_T.nil:
            return self


