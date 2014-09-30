import collections
import time
from Queue import PriorityQueue

from EightPuzzle import EightPuzzle, MOVES_T

class AstarSolver(object):
    def __init__(self, start_state, limit=float("inf"), heuristic=lambda node, goal: 0, goal_state=EightPuzzle(1, 2, 3, 4, 5, 6, 7, 8, ' ')):
        self._start = start_state
        self.goal = goal_state
        self.limit = limit

        #self._frontier = PriorityQueue()
        #self._explored = {}

        if isinstance(heuristic, collections.Iterable):
            # if multiple heuristics given, chain them together and sum the results
            self.heuristic = lambda node, goal: reduce(lambda cost, heur_func: cost + heur_func(node, goal), heuristic, 0)
        else:
            # else there is only one heuristic, just use it
            self.heuristic = heuristic

        self._start.last_move = MOVES_T.nil


    def solve(self):
        COUNTER = 0
        SEEN = set()
        SEEND = dict()

        frontier, explored = PriorityQueue(), dict()
        frontier.put(self._start)

        while not frontier.empty():
            node = frontier.get()
            
            if node == self.goal:
                # return the solution path
                return self.retrace(node, explored)
            
            # expand on the four directions
            attempts = (node.right(), node.left(), node.up(), node.down())
            for attempt, direction in zip(attempts, (MOVES_T.r, MOVES_T.l, MOVES_T.u, MOVES_T.d)):
                if attempt:
                    # limit expansion to self.limit
                    if COUNTER > self.limit:
                        return False
                    
                    # be sure to note the direction that got us to attempt
                    attempt.last_move = direction


                    # add the heuristic function to the priority cost
                    heuristic_estimate = self.heuristic(attempt, self.goal)
                    attempt.h_cost = heuristic_estimate
                    
                    old = explored[attempt] if attempt in explored else None
                    if old == attempt and attempt > old:
                        #print "found a worse way"
                        pass

                    # if there is not a better equal attempt already in explored
                    if old == attempt and (not attempt > old):
                        # if attempt has lower cost or (costs are equal and attempt has a smaller sure cost)
                        #print '%s found an old atp %s oldp %s' % (attempt, attempt.sure_cost, old.sure_cost)
                        if attempt < old or attempt.sure_cost < old.sure_cost:
                            # forget the old and remember the new attempt
                            explored[attempt] = attempt
                            frontier.put(attempt)
                            del old
                            #raise Exception('HAVENT YET SEEN THE REWRITE IN ACTION')
                            #print 'THE REWRITE IS HAPPENING'
                            #time.sleep(0.5)
                            
                    # never been here before
                    elif attempt not in explored:
                        # add to the explored and place on the frontier
                        explored[attempt] = attempt
                        frontier.put(attempt)
            
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

    def time_solution(self):
        start = time.time()
        solution = self.solve()
        end = time.time()
        return (solution, end - start)

def _main():
    from random import shuffle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
    shuffle(puzzle)
    
    puzzle = [3, 6, " ", 5, 7, 8, 2, 1, 4]

    s = AstarSolver(EightPuzzle(*puzzle))

    s.solve()

if __name__ == '__main__':
    _main()
