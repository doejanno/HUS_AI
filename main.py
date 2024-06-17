import HUS

def play(self):
        p_turn = True # True -> Player ones turn
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


def main():
    board =  HUS.Board()
    p_turn = True

    board.show_board()
    while True:
        if p_turn:
            print("Player 1 Turn. Imput move")
            inp = int(input())
            if board.p1.move(board.p2, inp, 0):
                p_turn = False
            else: 
                print("Player 1 lost")
                break
        else:
            print("Player 2. Which tile do u move?")
            arg = int(input())
            if board.p2.move(board.p1, arg, 0):
                p_turn = True
            else:
                print("Player 2 lost")
                break
        board.show_board()

if __name__ == "__main__":
    main()
