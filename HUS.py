class Player:
    def __init__(self):
        self.front = [0, 0, 0, 0, 2, 2, 2, 2]
        self.back = [2, 2, 2, 2, 2, 2, 2, 2]
        self.side = self.front + self.back
        self.stones = sum(self.side)


    def show_side_bott(self):
        print(self.side[:8])
        # reverse to look nicer in console
        ree = self.side[8:16]
        ree.reverse()
        print(ree)

    def show_side_top(self):
        print(self.side[8:16])
        ree = self.side[:8]
        ree.reverse()
        print(ree)

    # use st as start tile
    def move(self, opp, st, start_stones):
        # set stones to numb of stones in starting tile
        stones = self.side[st]
        stones = stones + start_stones
        if stones == 1: # if there is only one stone the move is does nothing
            return self.game_end()
        self.side[st] = 0 # empty the tile
        st = (st + 1) % len(self.side) # if we go abve the board size we loop around
        while stones != 0: # loop as long as we have stones
            if stones > 1:
                # put one stone in the tile
                self.side[st] += 1
                stones -= 1
                st = (st + 1) % len(self.side) # move one tile
            elif stones == 1:
                # put one stone in the tile and start moving again from the same tile
                self.side[st] += 1
                stones -= 1
                
                # if the tile wasnt empty keep moving
                if self.side[st] > 1:
                    stones = stones + self.take(opp, st)
                    self.move(opp, st, stones)
                break
        return self.game_end()
    
    def take(self, opp, p_tile):
        snack = 0
        if p_tile <= 7:
            opp_tile = 7-p_tile
            # Check if first row opponent tile is empty
            if opp.side[opp_tile] != 0:
                snack = opp.side[opp_tile]
                opp.side[opp_tile] = 0
                # Check if secund row opponent tile is empty
                if opp.side[15-opp_tile] != 0:
                    snack = snack + opp.side[15-opp_tile]
                    opp.side[15-opp_tile] = 0
        return snack
    
    def game_end(self):
        # lose if you only have one stone in any tile left
        max_stones = max(self.side)
        if max_stones <= 1:
            return False #Lost
        else:
            return True #Keep playing



class Board:
    def __init__(self):
        self.p1 = Player()
        self.p2 = Player()
    
    def show_board(self):
        self.p1.show_side_top()
        print()
        self.p2.show_side_bott()

    def play(self):
        p_turn = True # True -> Player 1s turn
        while True:
            if p_turn:
                print("Player 1.Which tile do u move?")
                arg = int(input())
                if self.p1.move(self.p2, arg, 0):
                    p_turn = False
                else: 
                    print("Player 1 lost")
                    break
            else:
                print("Player 2. Which tile do u move?")
                arg = int(input())
                if self.p2.move(self.p1, arg, 0):
                    p_turn = True
                else:
                    print("Player 2 lost")
                    break
            self.show_board()



board = Board()
board.show_board()
board.play()