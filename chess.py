class Board():
    def __init__(self):
        #self.board = [ ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        #               ['p', 'p', 'p', '-', 'p', 'p', 'p', 'p'],
        #               ['-', '-', '-', '-', '-', '-', '-', '-'],
        #               ['-', '-', '-', '-', '-', '-', '-', '-'],
        #               ['-', '-', 'R', '-', '-', '-', '-', '-'],
        #               ['-', '-', '-', 'p', '-', '-', '-', '-'],
        #               ['P', 'P', 'P', '-', '-', 'P', 'P', 'P'],
        #               ['-', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'] ]

        self.board = [ ['-', '-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-', '-'],
                       ['B', '-', '-', 'k', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-', '-'],
                       ['r', '-', '-', '-', '-', '-', '-', '-'],
                       ['-', '-', '-', '-', '-', '-', '-', 'K'] ]
        
        self.whiteToMove = True

def kingsPosition(board, whiteToMove):
    king = 'K' if whiteToMove else 'k'
    for array in board:
        if king in array:
            kingSquare = [board.index(array), array.index(king)]
    return kingSquare

def attackedSquares(moves):
    attackingMoves = []
    for m in range(len(moves)):
        attackingMoves.append(moves[m][1])
    return attackingMoves

def pieceMoves(board, whiteToMove):
    allMoves = []
    
    if whiteToMove:
        ownPieces = ['K', 'Q', 'R', 'B', 'N', 'P']
        capturablePieces = ['k', 'q', 'r', 'b', 'n', 'p']
    else:
        ownPieces = ['k', 'q', 'r', 'b', 'n', 'p']
        capturablePieces = ['K', 'Q', 'R', 'B', 'N', 'P']

    for i in range(8):
        for j in range(8):
            if board[i][j] == ownPieces[0]:
                allMoves = allMoves + kingMoves(board, capturablePieces, i, j)
            if board[i][j] == ownPieces[1]:
                allMoves = allMoves + queenMoves(board, capturablePieces, i, j)
            if board[i][j] == ownPieces[2]:
                allMoves = allMoves + rookMoves(board, capturablePieces, i, j)
            if board[i][j] == ownPieces[3]:
                allMoves = allMoves + bishopMoves(board, capturablePieces, i, j)
            if board[i][j] == ownPieces[4]:
                allMoves = allMoves + knightMoves(board, capturablePieces, i, j)
            if board[i][j] == ownPieces[5]:
                allMoves = allMoves + pawnMoves(board, capturablePieces, i, j)
    return allMoves

def legalMoves(board, whiteToMove):
    legalMoves = []

    #Find all whites moves:
    allMoves = pieceMoves(board, whiteToMove)
    for move in allMoves:
        hypotheticalBoard = [x[:] for x in board]
        #Make a hypothetical white move:
        updateBoard(hypotheticalBoard, move[0], move[1])

        #Blacks turn. Find all blacks moves:
        whiteToMove = not whiteToMove
        hypotheticalMoves = pieceMoves(hypotheticalBoard, whiteToMove)
        
        #Whites turn: Check if King is in check.
        whiteToMove = not whiteToMove
        kingSquare = kingsPosition(hypotheticalBoard, whiteToMove)
        attackingMoves = attackedSquares(hypotheticalMoves)
        if kingSquare not in attackingMoves:
            legalMoves.append(move)

    print(legalMoves)
    return legalMoves 

def kingMoves(board, capturablePieces, i, j):
    kingMoves = []
    for k, l in zip([0, 0, 1, -1, 1, 1, -1, -1], [1, -1, 0, 0, 1, -1, 1, -1]):
        if all(x >= 0 and x <= 7 for x in [i + k, j + l]):
            if board[i + k][j + l] in ['-'] + capturablePieces:
                kingMoves.append([[i, j], [i + k, j + l]])
    return kingMoves 

def queenMoves(board, capturablePieces, i, j):
    queenMoves = rookMoves(board, capturablePieces, i, j) + bishopMoves(board, capturablePieces, i, j)
    return queenMoves 

def rookMoves(board, capturablePieces, i, j):
    rookMoves = []
    for k, l in zip([0, 0, 1, -1], [1, -1, 0, 0]):
        for m in range(1, 8):
            try:
                if all(x >= 0 for x in [i + (k * m), j + (l * m)]):
                    if board[i + (k * m)][j + (l * m)] == '-':
                        rookMoves.append([[i, j], [i + (k * m), j + (l * m)]])
                    elif board[i + (k * m)][j + (l * m)] in capturablePieces:
                         rookMoves.append([[i, j], [i + (k * m), j + (l * m)]])
                         break
                    else:
                        break
            except IndexError:
                break
    return rookMoves 

def bishopMoves(board, capturablePieces, i, j):
    bishopMoves = []
    for k, l in zip([1, 1, -1, -1], [1, -1, 1, -1]):
        for m in range(1, 8):
            try:
                if all(x >= 0 for x in [i + (k * m), j + (l * m)]):
                    if board[i + (k * m)][j + (l * m)] == '-':
                        bishopMoves.append([[i, j], [i + (k * m), j + (l * m)]])
                    elif board[i + (k * m)][j + (l * m)] in capturablePieces:
                         bishopMoves.append([[i, j], [i + (k * m), j + (l * m)]])
                         break
                    else:
                        break
            except IndexError:
                break
    return bishopMoves 

def knightMoves(board, capturablePieces, i, j):
    knightMoves = []
    for k, l in zip([1, 1, 2, 2, -1, -1, -2, -2], [2, -2, 1, -1, 2, -2, 1, -1]):
        try:
            if all(x >= 0 for x in [i + k, j + l]):
                if board[i + k][j + l] in ['-'] + capturablePieces: 
                    knightMoves.append([[i, j], [i + k, j + l]])
        except IndexError:
            pass
    return knightMoves

def pawnMoves(board, capturablePieces, i, j):
    pawnMoves = []
    
    if board[i][j].isupper():
        up, lastRank = -1, 0
    else:
        up, lastRank = 1, 7

    if  i + up >= lastRank:
        #Moving without capturing
        if board[i + up][j] == '-':
            pawnMoves.append([[i, j], [i + up, j]])
            if i == 6 and board[i + (2 * up)][j] == '-':
                pawnMoves.append([[i, j], [i + (2 * up), j]])

        #Capture eastside.
        if j in range(7) and board[i + up][j + 1] in capturablePieces:
            pawnMoves.append([[i, j], [i - 1, j + 1]])
        
        #Capture westside.
        if j in range(1,8) and board[i + up][j - 1] in capturablePieces:
            pawnMoves.append([[i, j], [i - 1, j - 1]])

    return pawnMoves

def updateBoard(board, fromSq, toSq):
    movedPiece = board[fromSq[0]][fromSq[1]]
    board[fromSq[0]][fromSq[1]] = '-'
    board[toSq[0]][toSq[1]] = movedPiece 

def chessToArray(chessSq): 

    fileToArray = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }

    rankToArray = {
        "8": 0,
        "7": 1,
        "6": 2,
        "5": 3,
        "4": 4,
        "3": 5,
        "2": 6,
        "1": 7
    }

    return fileToArray[chessSq[0]], rankToArray[chessSq[1]]