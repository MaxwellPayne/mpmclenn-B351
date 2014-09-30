from Queue import PriorityQueue

from EightPuzzle import EightPuzzle


class AstarSolver(object):

    def __init__(self, nw, n, ne, w, c, e, sw, s, se, heuristic=lambda node: 0):
        self._puzzle = EightPuzzle(nw, n, ne, w, c, e, sw, s, se)
        self._frontier = PriorityQueue()
        self._explored = {}
        # don't have a heuristic, so any application of heuristic will do nothing
        self._heuristic = heuristic

        for node in (self._puzzle.right(), self._puzzle.left(), self._puzzle.up(), self._puzzle.right()):
            print '\nnode is \n%s' % str(node)
            if node:
                self._frontier.put(node)


    def solve(self):
        COUNTER = 0
        SEEN = set()
        SEEND = dict()
        from time import sleep

        while not self._frontier.empty():
            node = self._frontier.get()
            
            attempts = (node.right(), node.left(), node.up(), node.down())
            for attempt in attempts:
                if attempt:
                    
                    # add the heuristic function to the priority cost
                    heuristic_estimate = self._heuristic(attempt)
                    attempt.h_cost = heuristic_estimate
                    
                    old = self._explored[attempt] if attempt in self._explored else None
                    # if there is not a better equal attempt already in explored
                    if old and (not attempt > old):
                        # if attempt has lower cost or (costs are equal and attempt has a smaller sure cost)
                        if attempt.priority < old.priority or attempt.sure_cost < old.sure_cost:
                            # forget the old and remember the new attempt
                            self._explored[attempt] = attempt
                            self._frontier.put(attempt)
                            del old

                    # never been here before
                    elif attempt not in self._explored:
                        self._frontier.put(attempt)
            
            COUNTER += 1
            SEEN.add(attempt)
            SEEND[attempt] = None

            print 'counter %d seen %d seend %d' % (COUNTER, len(SEEN), len(SEEND))
        try:
            return self._explored['12345678 ']
        except KeyError:
            raise Exception('frontier is empty idk what to do')
                

def _main():
    from random import shuffle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
    #shuffle(puzzle)
    s = AstarSolver(*puzzle)

    s.solve()

if __name__ == '__main__':
    _main()
