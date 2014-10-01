8-Puzzle Solver
===============

Description
-----------
*EightPuzzle.py* contains a class for an 8-puzzle board state. *mpmclenn_informed.py* contains a **AstarSolver**, a class that solves the 8-puzzle given one or more heuristics. *mpmclenn_uninformed.py* contains **UniformCostSolver**, a class that solves the 8-puzzle without uxcsing any heuristics.


Testing
-------

Run `python sample_problems.py > output.txt` to execute the given tests and output their contents to a file. By default, *sample_problems.py* composes both the Hamming Priority heuristic and the sample Manhattan heuristic given by this project's specification when conducting informed search. You can specify `--use-heuristic` {hamming, sample} option to change which heuristic A\* uses. *sample_problems.py* also accpts the `-t` flag, which times the execution of each search and writes the results to the corresponding .csv file.

The utility funcitons `makeState`, `testUninformedSearch`, and `testInformedSearch` are located in *testing_functions.py*. They are used by *sample_problems.py* and can be used to design other tests.
