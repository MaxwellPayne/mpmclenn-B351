import time
from copy import deepcopy

import randomPlay
from gamePlay import opponent, valid, validPos, printBoard, gameOver, score, newBoard, doMove

# validPos should short-circuit valid
def isValid(board, color, pos):
    x, y = pos[0], pos[1]
    return ( pos == 'pass' or validPos(x, y) ) and valid(board, color, (x, y))



def childBoard(board, movingColor, move):
    clone = deepcopy(board)
    doMove(clone, movingColor, move)
    return clone

def _surrounding(pos):
    """Returns up, down, left, right, diags"""
    x, y = pos[0], pos[1]
    neighbors = []
    for xMod in (-1, 0, 1):
        for yMod in (-1, 0, 1):
            neighbors.append((x + xMod, y +yMod))
    return neighbors

def children(board, myColor):
    """Yields all child nodes worth exploring"""
    opponentTiles = []
    opponentMarker = opponent(myColor)

    # define what tiles are on the board
    for x in range(8):
        for y in range(8):
            if board[x][y].upper() == opponentMarker:
                opponentTiles.append((x, y))

    alreadyYielded = set()

    for tile in opponentTiles:
        # for each opponent tile on board
        neighbors = filter(lambda pos: isValid(board, myColor, pos), _surrounding(tile))
        # only valid neighbors of this tile
        for move in neighbors:
            if move not in alreadyYielded:
                # yield each possible move only once
                alreadyYielded.add(move)
                yield move

def simpleHeuristic(board):
    value = 0
    for row in board:
        for elem in row:
            if elem == "W":
                value = value + 1
            elif elem == "B":
                value = value - 1
    return value

def alphabeta(board, color, depth, alpha, beta, moveMade, isMax):
    if depth == 0 or gameOver(board):
        #print 'bottomed out at %s' % str((simpleHeuristic(board), moveMade))
        return (simpleHeuristic(board), moveMade)
    if isMax:
        for movePos in children(board, color):
            childScore, childMove = alphabeta(childBoard(board, color, movePos), opponent(color), depth-1, alpha, beta, movePos, False)
            alpha = (childScore, movePos) if childScore > alpha[0] else alpha
            if beta[0] <= alpha[0]:
                break
        return alpha
    else:
        for movePos in children(board, color):
            childScore, childMove = alphabeta(childBoard(board, color, movePos), opponent(color), depth-1, alpha, beta, movePos, True)
            beta = (childScore, movePos) if childScore < beta[0] else beta
            if beta[0] <= alpha[0]:
                break
        return beta


def nextMove(boardState, color):
    printBoard(boardState)
    

    move = randomPlay.nextMove(boardState, color)
    TIMEOUT = float(2)
    start_time = time.time()

    DEPTH = 0
    #while time.time() - start_time < TIMEOUT:
    for depth in xrange(6):
        initAlpha, initBeta = ( float('-inf'), move ), ( float('inf'), move )
        move = alphabeta(boardState, color, depth, initAlpha, initBeta, move,  True)[1]
        
        
    print 'nextMove is %s' % str(move)
    return move

def _main():
    print _surrounding((1,2))

if __name__ == '__main__':
    _main()
