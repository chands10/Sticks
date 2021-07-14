from copy import deepcopy
from math import inf

class Player:
    def __init__(self):
        self.hands = [1, 1]
        
    def __str__(self):
        return str(self.hands)
    
    def evaluation(self, player2):
        return sum(player2.hands) - sum(self.hands)
    
    def getPossibleActions(self, player2):
        actions = []
        
        # splits
        points = sum(self.hands)
        for i in range(max(0, points - 5 + 1), min(points + 1, 5)):
            current = [i, points - i]
            if current != self.hands:
                actions.append("split {} {}".format(current[0], current[1]))
        
        # taps
        p1HandsAvailable = [i for i, hand in enumerate(self.hands) if hand != 0]
        p2HandsAvailable = [i for i, hand in enumerate(player2.hands) if hand != 0]
        
        for hand1 in p1HandsAvailable:
            for hand2 in p2HandsAvailable:
                actions.append("tap {} {}".format(hand1, hand2))
             
        return actions
        
    def split(self, new):
        if new == self.hands:
            raise Exception("No change")
        elif min(new) < 0 or max(new) >= 5:
            raise Exception("Hand out of bounds")
        elif sum(new) != sum(self.hands):
            raise Exception("Invalid split")
        
        self.hands = new[:]
    
    def tap(self, player2, hand1, hand2):
        for hand in [hand1, hand2]:
            if not 0 <= hand < len(self.hands):
                raise Exception("Invalid hand {}".format(hand))
        
        if self.hands[hand1] == 0 or player2.hands[hand2] == 0:
            raise Exception("Hand {} out".format(hand))
        
        return player2.receiveTap(hand2, self.hands[hand1])
    
    def receiveTap(self, hand, amount):
        if not 0 <= hand < len(self.hands):
            raise Exception("Invalid hand {}".format(hand))
        if self.hands[hand] == 0:
            raise Exception("Hand {} out".format(hand))
    
        self.hands[hand] += amount
        if self.hands[hand] >= 5:
            self.hands[hand] = 0
            
        return sum(self.hands) == 0
    
class AI(Player):
    def __init__(self, idx):
        super().__init__()
        self.idx = idx
        self.other = (idx + 1) % 2
        self.depth = 3
    
    def getOptimalMove(self, player2):
        def maxValue(players, depth):
            best = (-inf, "")
            
            moves = players[self.idx].getPossibleActions(players[self.other])
            for move in moves:
                newPlayers = deepcopy(players)
                if generateSuccessorState(newPlayers, self.idx, self.other, move): # AI wins at this point, no need to travel deeper
                    return (inf, move)
                best = max(best, value(newPlayers, depth + 0.5, move))
                
            if len(moves) == 0:
                best = (players[self.idx].evaluation(players[self.other]), None)
            
            return best
        
        def minValue(players, depth):
            best = inf
            
            moves = players[self.other].getPossibleActions(players[self.idx])
            for move in moves:
                newPlayers = deepcopy(players)
                if generateSuccessorState(newPlayers, self.other, self.idx, move): # opponent wins at this point, no need to travel deeper
                    return -inf
                
                best = min(best, value(newPlayers, depth + 0.5)[0])
                
            if len(moves) == 0:
                best = (players[self.idx].evaluation(players[self.other]), None)
            
            return best
        
        def value(players, depth, move=None):
            if depth == self.depth:
                return (players[self.idx].evaluation(players[self.other]), move)
            findMax = depth % 1 == 0
            if findMax:
                return maxValue(players, depth)
            else:
                return (minValue(players, depth), move)
                    
        
        players = [player2, player2]
        players[self.idx] = self
        
        move = value(players, 0)
        return move[1]
    
    
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
