import HUS
import pytorch_ai
import torch
import random

MAX_MOVES = 1000

def train_dqn(num_episodes, batch_size=128, gamma=0.99, epsilon_start=1.0, epsilon_end=0.05, epsilon_decay=0.99999):
    board = HUS.Board()
    player1 = pytorch_ai.DQN()
    player2 = pytorch_ai.DQN()
    replay_buffer = pytorch_ai.ReplayBuffer(1000000)

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
                reward = -100
            else:
                p1_initial_stones = board.p1.stone_count
                p2_initial_stones = board.p2.stone_count	   	
                action1 = player1.get_move(state, board.p1.legal_moves, epsilon) 
                board.p1.move(board.p2, action1, 0)
                print(f"Player 1 stones: {board.p1.stone_count}")
                print(f"Player 2 stones: {board.p2.stone_count}")
                reward = (board.p1.stone_count - p1_initial_stones) + (p2_initial_stones - board.p2.stone_count)


                next_state = board.get_board()
                replay_buffer.push(state, action1, reward, next_state, done)
                state = next_state
                total_reward += reward
                if board.p1.is_game_over():
                    print("Game over")
                    done = True
                    reward = -100

            if not done and moves < MAX_MOVES:
                # Player 2's turn
                #print("Player 2 turn")
                #print("Board state:", state)
                #print("Legal moves:", board.p2.legal_moves)
                if board.p2.is_game_over():
                    print("Game over")
                    done = True
                    reward = -100  # Reward based on stone difference
            else:	   	
                p1_initial_stones = board.p1.stone_count
                p2_initial_stones = board.p2.stone_count
                action2 = player2.get_move(state, board.p2.legal_moves, epsilon) 
                board.p2.move(board.p1, action2, 0)
                reward = (board.p1.stone_count - p1_initial_stones) + (p2_initial_stones - board.p2.stone_count)
                print(f"Player 1 stones: {board.p1.stone_count}")
                print(f"Player 2 stones: {board.p2.stone_count}")

                next_state = board.get_board()
                replay_buffer.push(state, action2, -reward, next_state, done)
                state = next_state
                total_reward -= reward
                if board.p1.is_game_over():
                    print("Game over")
                    done = True
                    reward = -100

            moves += 1  # Increment the moves counter

        # Train both players
        loss1 = player1.update(replay_buffer, batch_size, gamma)
        loss2 = player2.update(replay_buffer, batch_size, gamma)

        epsilon = max(epsilon_end, epsilon * epsilon_decay)
        if episode % 100 == 0:
            print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {epsilon:.2f}")

    return player1, player2

if __name__ == "__main__":
    trained_player1, trained_player2 = train_dqn(10000)
    torch.save(trained_player1.state_dict(), "trained_player1.pth")
    torch.save(trained_player2.state_dict(), "trained_player2.pth")

