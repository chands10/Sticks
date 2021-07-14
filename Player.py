class Player:
    def __init__(self):
        self.hands = [1, 1]
        
    def __str__(self):
        return str(self.hands)
    
    def getPossibleActions(self, player2):
        actions = []
        
        # swaps
        points = sum(self.hands)
        for i in range(max(0, points - 5 + 1), min(points + 1, 5)):
            current = [i, points - i]
            if current != self.hands:
                actions.append("swap {} {}".format(current[0], current[1]))
        
        # taps
        p1HandsAvailable = [i for i, hand in enumerate(self.hands) if hand != 0]
        p2HandsAvailable = [i for i, hand in enumerate(player2.hands) if hand != 0]
        
        for hand1 in p1HandsAvailable:
            for hand2 in p2HandsAvailable:
                actions.append("tap {} {}".format(hand1, hand2))
             
        return actions
        
    def swap(self, new):
        if new == self.hands:
            raise Exception("No change")
        elif min(new) < 0 or max(new) >= 5:
            raise Exception("Hand out of bounds")
        elif sum(new) != sum(self.hands):
            raise Exception("Invalid swap")
        
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
    