from itertools import chain

class EightPuzzle(object):
    def __init__(self, nw, n, ne, w, c, e, sw, s, se, sure_cost=float('inf'), h_cost=float('inf')):

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
        SOLVED_STRING = '12345678 '
        return hash(self) == SOLVED_STRING

    def __str__(self):
        stringified = ''.join(map(str, self._state))
        return '\n'.join([stringified[i:i+3] for i in range(0, 9, 3)])

    def __eq__(self, other):
        return self.state == other.state

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)
    
    def _shifted(self, swap_index):
        new_state = list(self._state)

        temp = new_state[swap_index]
        new_state[swap_index] = " "
        new_state[self._blank] = temp
        return self.__class__(*new_state, sure_cost=self.priority + 1)

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

