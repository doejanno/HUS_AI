import HUS
import time
import pytorch_ai
import torch
import bot1

def main():
    board = HUS.Board()
    player1 = pytorch_ai.DQN()
    player2 = pytorch_ai.DQN()
    
    # Load trained models
    player1.load_state_dict(torch.load("trained_player1.pth"))
    player2.load_state_dict(torch.load("trained_player2.pth"))
    
    player1.eval()
    player2.eval()
    
    p_turn = True

    board.show_board()
    while True:
        if p_turn:
        	if board.p1.is_game_over():
        		print("Game Over, P2 Wins")
        		return
        	else:	
		        #print("Player 1 Turn. Input move")
		        board_state = board.get_board()
		        legal_moves = board.p1.legal_moves
		        inp = player1.get_move(board_state, legal_moves, epsilon=0)  # No exploration during gameplay
		        
		        #print("Player 1 plays tile " + str(inp))
		        if not board.p1.move(board.p2, inp, 0):
		            print("Player 1 lost")
		            break
		        p_turn = False
        else:
        	if board.p2.is_game_over():
        		print("Game Over, P1 Wins")
        		return
        	else:
		        #print("Player 2 Turn. Input move")
		        #board_state = board.get_board()
		        #legal_moves = board.p2.legal_moves
		        #inp = player2.get_move(board_state, legal_moves, epsilon=0)  # No exploration during gameplay
		        inp = bot1.calcMove(board.p2.side.copy(),board.p1.side.copy())
		        #print("Player 2 plays tile " + str(inp))
		        if not board.p2.move(board.p1, inp, 0):
		            print("Player 2 lost")
		            break
		        p_turn = True
		        
        board.show_board()
        time.sleep(1)

if __name__ == "__main__":
    main()

