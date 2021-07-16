from copy import deepcopy
from math import inf

# Human Player
class Player:
    # initial state is one finger out on each hand
    def __init__(self):
        self.hands = [1, 1] # [left hand, right hand]
        
    # return the current number of fingers out on each hand
    def __str__(self):
        return str(self.hands)
    
    # return all the possible moves the current player has (used to help the AI)
    # takes as input the opponent to view their current position
    def getPossibleMoves(self, opponent):
        moves = []
        
        # splits
        points = sum(self.hands)
        # cannot have more than four fingers up in one hand
        for i in range(max(0, points - 5 + 1), min(points + 1, 5)):
            current = [i, points - i]
            if current != self.hands: # cannot have same hands after split
                moves.append("split {} {}".format(current[0], current[1]))
        
        # taps
        p1HandsAvailable = [i for i, hand in enumerate(self.hands) if hand != 0]
        p2HandsAvailable = [i for i, hand in enumerate(opponent.hands) if hand != 0]
        
        for hand1 in p1HandsAvailable:
            for hand2 in p2HandsAvailable:
                moves.append("tap {} {}".format(hand1, hand2))
             
        return moves
        
    # split hands to position in new
    # position cannot be the same as it was prior
    # position must have at most four fingers on one hand
    # position must have the same sum as it was prior
    def split(self, new):
        if new == self.hands:
            raise Exception("No change")
        elif min(new) < 0 or max(new) >= 5:
            raise Exception("Hand out of bounds")
        elif sum(new) != sum(self.hands):
            raise Exception("Invalid split")
        
        self.hands = new[:]
    
    # tap opponent's hand2 with your hand1
    # hand1 and hand2 must be active
    # return True if the game is won
    # else return False
    def tap(self, opponent, hand1, hand2):
        for hand in [hand1, hand2]:
            if not 0 <= hand < len(self.hands):
                raise Exception("Invalid hand {}".format(hand))
        
        if self.hands[hand1] == 0 or opponent.hands[hand2] == 0:
            raise Exception("Hand {} out".format(hand))
        
        return opponent.receiveTap(hand2, self.hands[hand1])
    
    # add amount to hand
    # ensure that the hand being tapped is still active
    # return True if both hands are out, else return False
    def receiveTap(self, hand, amount):
        if not 0 <= hand < len(self.hands):
            raise Exception("Invalid hand {}".format(hand))
        if self.hands[hand] == 0:
            raise Exception("Hand {} out".format(hand))
    
        self.hands[hand] += amount
        if self.hands[hand] >= 5: # hand is no longer active
            self.hands[hand] = 0
            
        return sum(self.hands) == 0
    
# AI Player, extends Human Player
class AI(Player):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx # index in the players list
        self.other = (idx + 1) % 2 # either 0 or 1, opposite of idx
        self.depth = 8 # depth of Minimax search
    
    # score of current state
    # prefers opponent to have more fingers out and AI to have less fingers out
    def evaluation(self, opponent):
        return sum(opponent.hands) - sum(self.hands)
    
    # find the optimal move to perform using minimax search with alpha beta pruning, given the opponent's current state
    def getOptimalMove(self, opponent):
        # find the optimal move for the AI (the max player) given the current state of the players list, the current depth, and alpha/beta
        # returns (max value, optimal move)
        def maxValue(players, depth, alpha, beta):
            best = (-inf, None)
            
            moves = players[self.idx].getPossibleMoves(players[self.other])
            for move in moves:
                # create a copy of players that will be updated in generateSuccessorState
                newPlayers = deepcopy(players)
                if generateSuccessorState(newPlayers, self.idx, self.other, move): # AI wins at this point, no need to travel deeper
                    return (inf, move)
                
                score = value(newPlayers, depth + 1, move, alpha, beta)
                alpha = max(alpha, score[0])
                
                if score[0] > best[0]: # only update best if new score is explicitly greater than the current to ensure alpha beta pruning works as intended
                    best = score
                
                if alpha >= beta:
                    break
                
            if len(moves) == 0: # should always be a move possible
                best = (players[self.idx].evaluation(players[self.other]), None)
            
            return best
        
        # find the optimal move for the opponent (the min player) given the current state of the players list, the current depth, and alpha/beta
        # returns min value (move does not matter for opponent)
        def minValue(players, depth, alpha, beta):
            best = inf
            
            moves = players[self.other].getPossibleMoves(players[self.idx])
            for move in moves:
                newPlayers = deepcopy(players)
                # create a copy of players that will be updated in generateSuccessorState
                if generateSuccessorState(newPlayers, self.other, self.idx, move): # opponent wins at this point, no need to travel deeper
                    return -inf
                
                score = value(newPlayers, depth + 1, None, alpha, beta)[0]
                beta = min(beta, score)
                best = min(best, score)
                
                if alpha >= beta:
                    break                
                
            if len(moves) == 0: # should always be a move possible
                best = (players[self.idx].evaluation(players[self.other]), None)
            
            return best
        
        # find value of current state/move
        def value(players, depth, move=None, alpha=-inf, beta=inf):
            if depth == self.depth: # return evaluation function
                return (players[self.idx].evaluation(players[self.other]), move)
            
            findMax = (depth % 2 == 0) # at max level of tree
            if findMax:
                return maxValue(players, depth, alpha, beta)
            else:
                # add optimal move for max player to return value
                return (minValue(players, depth, alpha, beta), move)
                    
        # create players list
        players = [opponent, opponent]
        players[self.idx] = self
        
        move = value(players, 0) # initial depth is 0
        return move[1] # return optimal move
    

# perform a move given the players list, the index of the current turn, the index of the opponent (other), and the move performed
# return True if player wins after move, else return False    
def generateSuccessorState(players, turn, other, move):
    move = move.split()
    
    if len(move) != 3:
        raise Exception("Invalid move")
    
    move[1] = int(move[1])
    move[2] = int(move[2])
    
    if move[0] == "split":
        players[turn].split(move[1:])
    elif move[0] == "tap":
        finished = players[turn].tap(players[other], move[1], move[2])
        if finished:
            return True
    else:
        raise Exception("Invalid move")
    
    return False
