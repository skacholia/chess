import random
import chess
import chess.polyglot
import numpy as np
###MUST INSTALL numpy version 1.19.3######pip install numpy==1.19.3###
import time as t
#Chess AI V7
#MiniMax Agent
#December 6, 2020

class Player:
    
    def __init__(self, board, color, time):
        self.pawnTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

        self.knightTable = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,]

        self.bishopTable = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,]

        self.rookTable = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0]

        self.queenTable = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

        self.kingMiddleTable = [
        20, 30, 10,  0,  0, 10, 30, 20,
        20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30]

        self.kingEndTable = [
        -50,-40,-30,-20,-20,-30,-40,-50,
        -30,-20,-10,  0,  0,-10,-20,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 30, 40, 40, 30,-10,-30,
        -30,-10, 20, 30, 30, 20,-10,-30,
        -30,-30,  0,  0,  0,  0,-30,-30,
        -50,-30,-30,-30,-30,-30,-30,-50
        ]
        self.kingTable = self.kingMiddleTable
        self.start = t.time()
        self.color = color
        self.depth = 1
        self.quiesceDepth = 1
        self.nodes = 0
        self.quiesceNodes = 0
        self.moveTime = 1
        self.moveNumber = 1
        self.bookMoves = 0


    #Returns the best action for the player
    def move(self, board, time):
        try:
            #Selfmade opening book using https://rebel13.nl/download/polyglot.html
            #move = chess.polyglot.MemoryMappedReader("data/bookfish.bin").weighted_choice(board).move
            print(hi)
            self.bookMoves += 1
            return move
        except:
            self.start = t.time()      
            bestMove = random.choice(list(board.legal_moves))
            bestMoveScore, alpha, beta = float('-inf'), float('-inf'), float('inf')
            self.depth = 1
            previousBest = bestMove
            while t.time() - self.start <= self.moveTime:
                tempTime = t.time()
                bestMoveScore, alpha, beta = float('-inf'), float('-inf'), float('inf')
                
                #self.nodes = 0
                #self.quiesceNodes = 0
                #self.quiesceDepth = 1
                
                #If there are no queens, the game is set as End Game
                if len(board.pieces(chess.QUEEN, self.color)) == 0 and len(board.pieces(chess.QUEEN, not self.color)) == 0:
                    self.kingTable = self.kingEndTable

                for move in self.sortMoves(board, list(board.legal_moves)):
                    board.push(move)
                    score = -self.negamax(board, 1, -beta, -alpha)#Implementation of minimax
                    board.pop()
                    
                    if score == 123456789:
                        bestMove = previousBest
                        break
                    if score > alpha:
                        alpha = score
                    if score > bestMoveScore:
                        bestMoveScore = score
                        bestMove = move
                    
                    
                    self.kingTable = self.kingMiddleTable
                previousBest = bestMove
                print ("Color:",self.color,"|| Nodes:",self.nodes,"|| QuiesceNodes:",self.quiesceNodes,"|| Score:",bestMoveScore,"|| Move:",bestMove,"|| Time:",time,"|| Search Time:",t.time() - self.start,"|| Depth:",self.depth,"|| Quiesce Depth:",self.quiesceDepth)
                
                self.depth += 1
                time -= t.time() - tempTime
            #self.moveNumber += 1
            #self.moveTime = time/(50 - self.moveNumber)
            #print(self.moveTime)


            """nMoves = min(self.bookMoves, 10)
            factor = 2 - nMoves / 10
            target = time / (50 - self.moveNumber)
            self.moveTime = factor * target"""
            #print(self.bookMoves,self.moveTime)
            return bestMove


    def negamax(self, board, currentDepth, alpha, beta):
        #self.nodes += 1

        if t.time() - self.start >= self.moveTime:
            if board.turn == self.color:
                coeff = 1
            else:
                coeff = -1
            return coeff * 123456789
        
        if currentDepth == self.depth or len(list(board.legal_moves)) == 0 or board.is_game_over():
            #return self.quiesce(board, alpha, beta, 1) #last term is the max quiesce depth
            return self.quiesce(board, alpha, beta)#, 1

        
        #print(self.sortMoves(board, list(board.legal_moves)))
        for move in self.sortMoves(board, list(board.legal_moves)):
            board.push(move)
            score = -self.negamax(board, currentDepth + 1, -beta, -alpha)
            board.pop()
            
            #Alpha-Beta Pruning
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha


    #Fixes horizon problem issues
    def quiesce(self, board, alpha, beta):#currentDepth
        #self.nodes += 1
        #self.quiesceNodes += 1
        
        if t.time() - self.start >= self.moveTime:
            if board.turn == self.color:
                coeff = 1
            else:
                coeff = -1
            return coeff * 123456789

        """if self.quiesceDepth < currentDepth:
            self.quiesceDepth += 1"""

        stand_pat = self.evaluate(board)

        #Alpha-Beta Pruning in Quiescence
        #if depthLeft == 0:
            #return stand_pat
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        

        #Move Ordering yields an unecessary increase in time --- self.sortMoves(board, self.captureMoves(board))
        for move in self.captureMoves(board):
            board.push(move)
            score = -self.quiesce(board, -beta, -alpha)#, currentDepth + 1
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
            
        return alpha


    def evaluate(self, board):
        if board.turn == self.color:
            coeff = 1
        else:
            coeff = -1
        
        score = 0

        #Source for values: https://arxiv.org/pdf/2009.04374.pdf or https://en.wikipedia.org/wiki/Chess_strategy
        for (piece, value, table) in [(chess.PAWN, 100, self.pawnTable), 
                           (chess.BISHOP, 333, self.bishopTable),
                           (chess.QUEEN, 950, self.queenTable),
                           (chess.KING, 0, self.kingTable),
                           (chess.KNIGHT, 305, self.knightTable),
                           (chess.ROOK, 563, self.rookTable)]:
            score += (len(board.pieces(piece, self.color)) - len(board.pieces(piece, not self.color))) * value
            if board.turn:#if board.turn == chess.WHITE
                score += sum([table[i] for i in board.pieces(piece, chess.WHITE)]) - sum([table[i] for i in board.mirror().pieces(piece, chess.BLACK)])
            else:
                score += sum([table[i] for i in board.mirror().pieces(piece, chess.BLACK)]) - sum([table[i] for i in board.pieces(piece, chess.WHITE)])

        #Will guarantee that the current board state will return the highest score due to a checkmate
        if board.is_checkmate():
            score += 20000
        
        return coeff * score


    #Fully Functional move sorting:
    #   -If board.turn == self.color, moves are sorted by their evaluation in decending order
    #   -If board.turn != self.color, moves are sorted by their evaluation in ascending order
    def sortMoves(self, board, moves):
        sortedMoves = np.empty((0, 2))
        
        for move in moves:
            board.push(move)
            sortedMoves = np.append(sortedMoves, np.array([[move, self.miniEval(board)]]), axis = 0)
            board.pop()

        if board.turn == self.color:
            return sortedMoves[sortedMoves[:,1].argsort()[::-1]][:,0]
        else:
            return sortedMoves[sortedMoves[:,1].argsort()][:,0]
    

    #Returns Capture moves for the available moves for the current player on board
    def captureMoves(self, board):
        moves = []

        for move in list(board.legal_moves):
            if board.is_capture(move):
                moves.append(move)
        
        return moves


    #Quick evaluation function used for fast move sorting
    def miniEval(self, board):
        score = 0
        
        #Does not include (chess.KING, 0), for a faster evaluation loop
        for (piece, value) in [(chess.PAWN, 100),
                           (chess.BISHOP, 333),
                           (chess.QUEEN, 950),
                           (chess.KNIGHT, 305),
                           (chess.ROOK, 563)]:
            score += (len(board.pieces(piece, self.color)) - len(board.pieces(piece, not self.color))) * value
        
        if board.is_checkmate():
            score += 20000
        
        return score