class Player:
    def __init__(self, player_side):
        # creating player vars
        self.side = player_side
        self.stone_count = sum(self.side)
        self.legal_moves = self.get_legal_moves()


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
            self.update_vars()
            return self.is_game_over()
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
        self.update_vars()
        return self.is_game_over()
    
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
    
    def is_game_over(self):
        # lose if you only have one stone in any tile left
        max_stones = max(self.side)
        if max_stones <= 1:
            return False #Lost
        else:
            return True #Keep playing

    def get_legal_moves(self):
        # this function returns a board of the legal moves for a player. 1 = legal move, 0 = no legal move
        # Used to help AI navigate
        legal_moves_side = []
        for args in self.side:
            if args > 1:
                legal_moves_side.append(1)
            else:
                legal_moves_side.append(0)
        return legal_moves_side
    
    def update_vars(self):
        # function used to update the vars before each move
        self.set_legal_moves()
        self.set_stone_count()

    def set_legal_moves(self):
        self.legal_moves = self.get_legal_moves()
    
    def set_stone_count(self):
        self.stone_count = sum(self.side)


class Board:
    def __init__(self):
        # creating player with given side so AI can input different boards
        front = [0, 0, 0, 0, 2, 2, 2, 2]
        back = [2, 2, 2, 2, 2, 2, 2, 2]
        # players need different sides due to pointer
        p1_side = front + back
        p2_side = front + back
        self.p1 = Player(p1_side)
        self.p2 = Player(p2_side)
    
    def show_board(self):
        self.p1.show_side_top()
        print()
        self.p2.show_side_bott()