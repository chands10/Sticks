from Player import *

class Game:
    def __init__(self, numHumans):
        self.players = [Player(), Player()]
        self.ais = [False, False]
        if numHumans <= 1:
            self.players[1] = AI(1)
            self.ais[1] = True
        if numHumans == 0:
            self.players[0] = AI(0)
            self.ais[0] = True
        
        self.turn = 0
        self.other = 1
        
    def makeMove(self):
        print()
        for i, player in enumerate(self.players):
            print("Player {}: {}".format(i + 1, player))
            
        if self.ais[self.turn]:
            move = self.players[self.turn].getOptimalMove(self.players[self.other])
            print(move)
        else:
            move = input("Player {} enter move: ".format(self.turn + 1))
        
        r = generateSuccessorState(self.players, self.turn, self.other, move)
        if r:
            print("Player {} wins!".format(self.turn + 1))
        
        self.turn, self.other = self.other, self.turn
        
        return r
        
if __name__ == "__main__":
    numHumans = int(input("Input number of humans (0 - 2): "))
    game = Game(numHumans)
    while True:
        try:
            finished = game.makeMove()
            if finished:
                break
        except Exception as e:
            print(e)
        