import time, threading
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

def alphabeta(board, color, depth, alpha, beta, moveMade, isMax, timeoutAt=None):
    # alphabeta failed to find a solution in time alotted
    if timeoutAt and time.time() > timeoutAt:
        raise threading.ThreadError('alphabeta timed out before finding a solution')

    if depth == 0 or gameOver(board):
        #print 'bottomed out at %s' % str((simpleHeuristic(board), moveMade))
        return (simpleHeuristic(board), moveMade)
    if isMax:
        for movePos in children(board, color):
            try:
                childScore, childMove = alphabeta(childBoard(board, color, movePos), opponent(color), depth-1, alpha, beta, movePos, False)
            except threading.ThreadError as e:
                raise e
            alpha = (childScore, movePos) if childScore > alpha[0] else alpha
            if beta[0] <= alpha[0]:
                break
        return alpha
    else:
        for movePos in children(board, color):
            try:
                childScore, childMove = alphabeta(childBoard(board, color, movePos), opponent(color), depth-1, alpha, beta, movePos, True)
            except threading.ThreadError as e:
                raise e
            beta = (childScore, movePos) if childScore < beta[0] else beta
            if beta[0] <= alpha[0]:
                break
        return beta
        
class NS:
    pass

def nextMove(boardState, color):
    decision, decisionLock = randomPlay.nextMove(boardState, color), threading.RLock()
    decidedDepth = NS()
    decidedDepth.depth = -1

    def distributedAlphaBeta(board, color, maxDepth, timeoutAt):
        def callback():
            #print 'thread going'
            randMove = randomPlay.nextMove(board, color)
            try:
                initAlpha, initBeta = ( float('-inf'), randMove ), ( float('inf'), randMove )
                best = alphabeta(board, color, maxDepth, initAlpha, initBeta, randMove, True, timeoutAt=timeoutAt)[1]
                with decisionLock as lock:
                    if maxDepth > decidedDepth.depth:
                        #print 'editing decision to %s' % str(best)
                        decision, decidedDepth.depth = best, maxDepth
            except threading.ThreadError as e:
                # timed out
                print 'timeout for depth %d' % maxDepth
                exit(3)
        return callback

    printBoard(boardState)
    
    
    ##move = randomPlay.nextMove(boardState, color)
    TIMEOUT = float(3)

    ##DEPTH = 0
    for depth in xrange(6):
        t = threading.Thread(target=distributedAlphaBeta(boardState, color, depth, time.time() + TIMEOUT))
        #initAlpha, initBeta = ( float('-inf'), move ), ( float('inf'), move )
        #move = alphabeta(boardState, color, depth, initAlpha, initBeta, move,  True)[1]
        t.setDaemon(True)
        t.start()

    t.join(TIMEOUT)
        
    print 'nextMove is %s' % str(decision)
    return decision

def _main():
    print _surrounding((1,2))

if __name__ == '__main__':
    _main()
