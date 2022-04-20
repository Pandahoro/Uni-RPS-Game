class Game:
    def __init__(self, id):
        self.p1Went = False
        self.p2Went = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0
    
    def get_player_move(self, p):
        #p needs to be 1 or 0, eg player 1 or two
        return self.moves[p]

    def play(self, player, move): # update moves with move and set that the player went
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self): # sets self as ready
        return self.ready

    def bothWent(self): # checks both have went
        return self.p1Went and self.p2Went

    def winner(self): # takes moves and then decides the winner

        p1 = self.moves[0].upper()[0] # sets to uppercase
        p2 = self.moves[1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = 0
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "P" and p2 == "R":
            winner = 0
        elif p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1

        return winner # who won

    def resetWent(self): #reset if player went
        self.p1Went = False
        self.p2Went = False