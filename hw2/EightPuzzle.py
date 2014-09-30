from itertools import chain

# enum for types of moves
class MOVES_T:
    nil = '\0'
    r = 'r'
    l = 'l'
    u = 'u'
    d = 'd'

class EightPuzzle(object):
    def __init__(self, nw, n, ne, w, c, e, sw, s, se, sure_cost=0, h_cost=float('inf')):

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

    @property
    def state(self):
        return self._state
    
    @property
    def priority(self):
        return self.sure_cost + self.h_cost

    def __hash__(self):
        return hash(''.join(map(str, self._state)))

    @property
    def is_solved(self):
        #print 'inside is_solved'
        SOLVED_STRING = '12345678 '
        return hash(self) == hash(SOLVED_STRING)

    def __str__(self):
        stringified = ''.join(map(str, self._state))
        #return '\n'.join([stringified[i:i+3] for i in range(0, 9, 3)])
        return stringified

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
            return isinstance(other, self.__class__) and self.state == other.state

    def __cmp__(self, other):
        return cmp(self.priority, other.priority if isinstance(other, self.__class__) else None)
    
    def _shifted(self, swap_index):
        from time import sleep

        new_state = list(self._state)
        """
        print 'new_state'
        print new_state[:3]
        print new_state[3:6]
        print new_state[6:]
        """

        temp = new_state[swap_index]
        new_state[swap_index] = ' '
        new_state[self._blank] = temp
        """
        print 'new_state now'
        print new_state[:3]
        print new_state[3:6]
        print new_state[6:]
        print
        """
        #sleep(1)
        
        #if new_state == [1, 2, 3, 4, 5, 6, 7, 8, ' ']: raise Exception('shifted error')
        #new_state = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
        return self.__class__(*new_state, sure_cost=self.sure_cost + 1)

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
