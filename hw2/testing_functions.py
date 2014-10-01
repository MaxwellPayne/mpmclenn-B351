import csv

from EightPuzzle import *
from mpmclenn_uninformed import *
from mpmclenn_informed import *

def makeState(nw, n, ne, w, c, e, sw, s, se):
    states = map(lambda t: ' ' if t == "blank" else t, (nw, n, ne, w, c, e, sw, s, se))
    return EightPuzzle(*states)

def outputTimes(solution_len, time_elapsed, outfile_name='output.txt'):
    # write "(solution_len, time_elapsed)" to outfile for a given trial
    with open(outfile_name, 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([solution_len, time_elapsed])

def testUninformedSearch(initialState, goalState, limit, timeit=False):
    searcher = UniformCostSolver(initialState, goal_state=goalState, limit=limit)
    if timeit:
        # time the solution if specified
        solution, time_elapsed = searcher.time_solution()
        outputTimes(len(solution), time_elapsed, outfile_name='uninformed.csv')
        return solution
    else:
        return searcher.solve()

def testInformedSearch(initialState, goalState, limit, timeit=False, heur_names=('hamming', 'sample')):

    def sample_heuristic(current_node, goal_node):
        # Calculates how far each tile is from its goal state, and sums those distances
        current, goal = current_node.matrix, goal_node.matrix
        sum = 0
        for i in range(0, len(goal)):
            for j in range(0, len(goal)):
                tile = goal[i][j]
                for k in range(0, len(current)):
                    for l in range(0, len(current)):
                        if current[k][l] == tile:
                            sum += (k - i) * (k - i) + (j - l) * (j - l)
        return sum


    def hamming_distance(current_node, goal_node):
        # number of tiles not in their goal state position
        dist = 0
        for current_tile, goal_tile in zip(current_node.state, goal_node.state):
            if current_tile != goal_tile:
                dist += 1
        
        return dist

    function_mapping = {'hamming': hamming_distance, 'sample': sample_heuristic}
    # decide which heuristics to use based on the specifications passed
    heuristics = (lambda c, g: 0,) if not heur_names else tuple((function_mapping[name] for name in heur_names))
    # use both hamming and sample heuristic by default

    searcher = AstarSolver(initialState, goal_state=goalState, limit=limit, heuristic=heuristics)

    if timeit:
        # time the solution if specified
        solution, time_elapsed = searcher.time_solution()
        outfile_name = 'uninformed' if not heur_names else 'informed_' + '_'.join(sorted((name for name in heur_names)))
        outfile_name += '.csv'
        outputTimes(len(solution), time_elapsed, outfile_name=outfile_name)
        return solution
    else:
        return searcher.solve()

