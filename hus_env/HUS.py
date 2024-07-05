import sys


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
        print(f"Starting move from pit {st} with {self.side[st] + start_stones} stones")
        stones = self.side[st] + start_stones
        self.side[st] = 0
        SC = 0
        while stones > 0:
            st = (st + 1) % len(self.side)
            self.side[st] += 1
            stones -= 1
            SC += 1
            print(f"Dropped stone in pit {st}, {stones} stones left")
            if stones == 0 and self.side[st] > 1:
                print(f"Last stone in non-empty pit {st}, continuing with {self.side[st]} stones")
                stones = self.side[st]
                self.side[st] = 0
                stones += self.take(opp, st)
                print(f"Sowing Cycle: {SC}")
                print(f"Boardstate during move:{self.side}")
                if SC > 3000:
                	print("SC-Limit reached")
                	sys.exit(0)
        print(f"Move ended. Final board state: {self.side}")
        self.update_vars()
        opp.update_vars()
        return not self.is_game_over()		


    def take(self, opp, p_tile):
        print(f"Attempting to take from opponent. Landing pit: {p_tile}")
        snack = 0
        if p_tile <= 7:
            opp_tile = 7 - p_tile
            if opp.side[opp_tile] != 0:
                snack = opp.side[opp_tile]
                opp.side[opp_tile] = 0
                print(f"Took {snack} stones from opponent's pit {opp_tile}")
                if opp.side[15 - opp_tile] != 0:
                    snack += opp.side[15 - opp_tile]
                    opp.side[15 - opp_tile] = 0
                    print(f"Took additional {opp.side[15 - opp_tile]} stones from opponent's pit {15 - opp_tile}")
        opp.update_vars()
        print(f"Total stones taken: {snack}")
        return snack

    def is_game_over(self):
        # lose if you only have one stone in any tile left
            max_stones = max(self.side)
            for stones in self.side:
                if stones > 1:
                    return False
            return True

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
        #print(sum(self.side))


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


    def get_board(self):
        return self.p1.side + self.p2.side
