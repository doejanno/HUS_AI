import HUS
import pytorch_ai
import time


def main():
    board =  HUS.Board()
    player1 = pytorch_ai.DQN()
    player2 = pytorch_ai.DQN()
    p_turn = True

    board.show_board()
    while True:
        if p_turn:
            print("Player 1 Turn. Imput move")
            # inp = player1.rdm()
            inp = player1.forward(board.get_board())
            print("Player 1 plays tile " + str(inp))
            if board.p1.move(board.p2, inp, 0):
                p_turn = False
            else: 
                print("Player 1 lost")
                break
        else:
            print("Player 2. Which tile do u move?")
            # inp = player2.rdm()
            inp = player1.forward(board.get_board())
            print("Player 2 plays tile " + str(inp))
            if board.p2.move(board.p1, inp, 0):
                p_turn = True
            else:
                print("Player 2 lost")
                break
        board.show_board()
        time.sleep(1)

if __name__ == "__main__":
    main()
