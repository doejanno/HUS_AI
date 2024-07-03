import HUS
import pytorch_ai
import torch
import random

MAX_MOVES = 50

def train_dqn(num_episodes, batch_size=32, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
    board = HUS.Board()
    player1 = pytorch_ai.DQN()
    player2 = pytorch_ai.DQN()
    replay_buffer = pytorch_ai.ReplayBuffer(10000)

    epsilon = epsilon_start

    for episode in range(num_episodes):
        board = HUS.Board()  # Reset the board
        state = board.get_board()
        done = 0
        total_reward = 0
        moves = 0

        while not done and moves < MAX_MOVES:
            # Player 1's turn
            #print("Player 1 turn")
            #print("Board state:", state)
            #print("Legal moves:", board.p1.legal_moves)
            if board.p1.is_game_over():
                print("Game over")
                done = True
                reward = -1
            else:	   	
                action1 = player1.get_move(state, board.p1.legal_moves, epsilon) 
                board.p1.move(board.p2, action1, 0)
                reward = 0


            next_state = board.get_board()
            replay_buffer.push(state, action1, reward, next_state, done)
            state = next_state
            total_reward += reward

            if not done and moves < MAX_MOVES:
                # Player 2's turn
                #print("Player 2 turn")
                #print("Board state:", state)
                #print("Legal moves:", board.p2.legal_moves)
                if board.p2.is_game_over():
                    print("Game over")
                done = True
                reward = -1
            else:	   	
                action2 = player2.get_move(state, board.p2.legal_moves, epsilon) 
                board.p2.move(board.p1, action2, 0)
                reward = 0

            next_state = board.get_board()
            replay_buffer.push(state, action2, reward, next_state, done)
            state = next_state
            total_reward += reward

            moves += 1  # Increment the moves counter

    # Train both players
    loss1 = player1.update(replay_buffer, batch_size, gamma)
    loss2 = player2.update(replay_buffer, batch_size, gamma)

    epsilon = max(epsilon_end, epsilon * epsilon_decay)

    print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {epsilon:.2f}")

    return player1, player2

if __name__ == "__main__":
    trained_player1, trained_player2 = train_dqn(1000)
    torch.save(trained_player1.state_dict(), "trained_player1.pth")
    torch.save(trained_player2.state_dict(), "trained_player2.pth")

