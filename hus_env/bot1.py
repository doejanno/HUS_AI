#Random moves
import random
def calcMove(activeBoard, passiveBoard):
    if max(activeBoard) < 2:
        return 0
    while 1:
        i = random.randint(0,15)
        if activeBoard[i] > 1:
            return i