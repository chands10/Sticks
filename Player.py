class Player:
    def __init__(self):
        self.hands = [1, 1]
        
    def __str__(self):
        return str(self.hands)
        
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
        
            if self.hands[hand] == 0:
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
    