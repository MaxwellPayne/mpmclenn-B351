from mpmclenn_informed import AstarSolver
from EightPuzzle import EightPuzzle

class UniformCostSolver(AstarSolver):
    """UniformCostSolver is simply a subclass of AstarSolver that
   uses a null, uninformed heuristic"""
    def __init__(self, start_state, limit=float("inf"), goal_state=EightPuzzle(1, 2, 3, 4, 5, 6, 7, 8, ' ')):
        null_heuristic = lambda node, goal: 0
        super(UniformCostSolver, self).__init__(start_state, limit=limit, heuristic=null_heuristic, goal_state=goal_state)
        
