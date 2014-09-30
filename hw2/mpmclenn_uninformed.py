from Queue import PriorityQueue

from EightPuzzle import EightPuzzle


class AstarSolver(object):

    def __init__(self, nw, n, ne, w, c, e, sw, s, se, heuristic=lambda node: 0):
        self._puzzle = EightPuzzle(nw, n, ne, w, c, e, sw, s, se, sure_cost=0, h_cost=0)
        self._frontier = PriorityQueue()
        self._explored = {}
        # don't have a heuristic, so any application of heuristic will do nothing
        self._heuristic = heuristic

        self._frontier.put(self._puzzle)


    def solve(self):
        COUNTER = 0
        SEEN = set()
        SEEND = dict()
        SOLVED = EightPuzzle(*[1, 2, 3, 4, 5, 6, 7, 8, ' '])

        potential_wins = {}

        while not self._frontier.empty():
            node = self._frontier.get()
            
            if node.is_solved:
                print 'solve'
                return node
            
            
            #if node == SOLVED: raise Exception('huh node is sovled?')
            



            attempts = (node.right(), node.left(), node.up(), node.down())
            for attempt in attempts:
                if attempt:
                    """print
                    print attempt
                    print"""


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
                            raise Exception('hard way')

                    # never been here before
                    elif attempt not in self._explored:
                        #print 'adding the easy way'
                        self._explored[attempt] = attempt
                        self._frontier.put(attempt)
            
                    COUNTER += 1
                    SEEN.add(attempt)
                    SEEND[attempt] = None

            #print 'counter %d seen %d seend %d' % (COUNTER, len(SEEN), len(SEEND))

        raise Exception('fail')
                

def _main():
    from random import shuffle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
    shuffle(puzzle)
    
    puzzle = [3, 6, " ", 5, 7, 8, 2, 1, 4]

    s = AstarSolver(*puzzle)

    s.solve()

if __name__ == '__main__':
    _main()
