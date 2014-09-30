from Queue import PriorityQueue
from time import sleep

from EightPuzzle import EightPuzzle, MOVES_T



class AstarSolver(object):

    def __init__(self, nw, n, ne, w, c, e, sw, s, se, heuristic=lambda node: 0):
        self._start = EightPuzzle(nw, n, ne, w, c, e, sw, s, se, sure_cost=0, h_cost=0)
        self._frontier = PriorityQueue()
        self._explored = {}
        # don't have a heuristic, so any application of heuristic will do nothing
        self._heuristic = heuristic

        self._start.last_move = MOVES_T.nil
        self._frontier.put(self._start)


    def solve(self):
        COUNTER = 0
        SEEN = set()
        SEEND = dict()

        while not self._frontier.empty():
            node = self._frontier.get()
            
            if node.is_solved:
                # return the solution path
                return self.retrace(node, self._explored)
            
            # expand on the four directions
            attempts = (node.right(), node.left(), node.up(), node.down())
            for attempt, direction in zip(attempts, (MOVES_T.r, MOVES_T.l, MOVES_T.u, MOVES_T.d)):
                if attempt:
                    # be sure to note the direction that got us to attempt
                    attempt.last_move = direction


                    # add the heuristic function to the priority cost
                    heuristic_estimate = self._heuristic(attempt)
                    attempt.h_cost = heuristic_estimate
                    
                    old = self._explored[attempt] if attempt in self._explored else None
                    if old == attempt and attempt > old:
                        #print "found a worse way"
                        pass

                    # if there is not a better equal attempt already in explored
                    if old == attempt and (not attempt > old):
                        # if attempt has lower cost or (costs are equal and attempt has a smaller sure cost)
                        print '%s found an old atp %s oldp %s' % (attempt, attempt.sure_cost, old.sure_cost)
                        if attempt < old or attempt.sure_cost < old.sure_cost:
                            # forget the old and remember the new attempt
                            self._explored[attempt] = attempt
                            self._frontier.put(attempt)
                            del old
                            raise Exception('HAVENT YET SEEN THE REWRITE IN ACTION')

                    # never been here before
                    elif attempt not in self._explored:
                        # add to the explored and place on the frontier
                        self._explored[attempt] = attempt
                        self._frontier.put(attempt)
            
                    COUNTER += 1
                    SEEN.add(attempt)
                    SEEND[attempt] = None

        print 'FAILED'
        return False
    
    def retrace(self, state, explored):
        path = []
        # can't move anymore if the move was nil
        while state.last_move != MOVES_T.nil:
            # terminate if succesfully backtracked to start
            if state == self._start: break

            previous = state.backtrack()
            if previous not in explored:
                raise ValueError('explored does not contain a valid retrace path')

            # append the move taken by previous -> state
            # then backtrack from state to previous
            path.append(state.last_move)
            print state
            state = explored[previous]
        return tuple(reversed(path))

def _main():
    from random import shuffle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
    shuffle(puzzle)
    
    puzzle = [3, 6, " ", 5, 7, 8, 2, 1, 4]

    s = AstarSolver(*puzzle)

    s.solve()

if __name__ == '__main__':
    _main()
