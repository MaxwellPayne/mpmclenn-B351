import collections
import time
from Queue import PriorityQueue

from EightPuzzle import EightPuzzle, MOVES_T

class AstarSolver(object):
    def __init__(self, start_state, limit=float("inf"), heuristic=lambda node, goal: 0, goal_state=EightPuzzle(1, 2, 3, 4, 5, 6, 7, 8, ' ')):
        self._start = start_state
        self.goal = goal_state
        self.limit = limit

        if isinstance(heuristic, collections.Iterable):
            # if multiple heuristics given, chain them together and sum the results
            self.heuristic = lambda node, goal: reduce(lambda cost, heur_func: cost + heur_func(node, goal), heuristic, 0)
        else:
            # else there is only one heuristic, just use it
            self.heuristic = heuristic

        self._start.last_move = MOVES_T.nil


    def solve(self):
        """return a list of the best path from start to goal, False if failure"""
        frontier, explored = PriorityQueue(), dict()
        frontier.put(self._start)
        COUNTER = 0

        while not frontier.empty():
            node = frontier.get()
            
            if node == self.goal:
                # TERMINATE SUCCESS! - return the solution path
                return self.retrace(node, explored)
            
            # expand on the four directions
            attempts = (node.right(), node.left(), node.up(), node.down())
            for attempt, direction in zip(attempts, (MOVES_T.r, MOVES_T.l, MOVES_T.u, MOVES_T.d)):
                if attempt: # is not None, would be None if that direction was not legal

                    if COUNTER > self.limit:
                        # limit expansion to self.limit
                        return False
                    
                    # be sure to note the direction that got us to attempt
                    attempt.last_move = direction

                    # add the heuristic function to the priority cost
                    heuristic_estimate = self.heuristic(attempt, self.goal)
                    attempt.h_cost = heuristic_estimate
                    
                    old = explored[attempt] if attempt in explored else None
                    
                    # if there is not a better, equivalent node already in explored
                    if old == attempt and (not attempt > old):
                        
                        # if attempt has lower cost or (costs are equal and attempt has a smaller sure cost)
                        if attempt < old or attempt.sure_cost < old.sure_cost:
                            # forget the old and remember the new attempt
                            explored[attempt] = attempt
                            frontier.put(attempt)
                            del old
                            
                    elif attempt not in explored:
                        # never been here before
                        explored[attempt] = attempt
                        frontier.put(attempt)
                
                # increment the counter for every attempted move
                COUNTER += 1

        # TERMINATE FAILURE
        return False
    
    def retrace(self, state, explored):
        """Retraces the path from state back to start"""
        path, states = [], []
        # can't move anymore if the move was nil
        while state.last_move != MOVES_T.nil:
            states.append(state)
            # terminate if succesfully backtracked to start
            if state == self._start: break

            previous = state.backtrack()
            if previous not in explored:
                raise ValueError('explored does not contain a valid retrace path')

            # append the move taken by previous -> state
            # then backtrack from state to previous
            path.append(state.last_move)
            state = explored[previous]
        return ( tuple(reversed(path)), '\n'.join(reversed(map(str, states))) )

    def time_solution(self):
        """Solve the puzzle, but also return the time elapsed"""
        start = time.time()
        solution = self.solve()
        end = time.time()
        return (solution, end - start)

def _main():
    from random import shuffle
    puzzle = [1, 2, 3, 4, 5, 6, 7, 8, ' ']
    shuffle(puzzle)

    puzzle = (2, 6, 5, 4, " ", 3, 7, 1, 8)

    s = AstarSolver(EightPuzzle(*puzzle))

    print s.solve()

if __name__ == '__main__':
    _main()
