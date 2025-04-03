#! /usr/bin/env python3
import random
from dataclasses import dataclass, asdict
import json
from secrets import flag

@dataclass
class Move:
    x : int
    y : int
    direction : str

def random_move(dim):
    return Move(
        random.randint(0,dim-2),
        random.randint(0,dim-2),
        random.choice(["ccw","cw"])
    )

def random_moves(dim, n_moves):
    return [random_move(dim) for i in range(n_moves)]

def init_state(dim):
    return [[i*dim+j for j in range(dim)] for i in range(dim)]

def apply_move(b, move):
    dim = len(b)
    x = move.x
    y = move.y

    assert x < dim-1
    assert y < dim-1



    if move.direction == "cw":
        b[x][y], b[x+1][y], b[x+1][y+1], b[x][y+1] = b[x+1][y], b[x+1][y+1], b[x][y+1], b[x][y]
    else:
        b[x][y], b[x+1][y], b[x+1][y+1], b[x][y+1] = b[x][y+1], b[x][y], b[x+1][y], b[x+1][y+1]
        
    return b

def apply_moves(board, moves):
    for move in moves:
        board = apply_move(board, move)
    return board

def print_board(board):
    print("\n".join(",".join(f"{x:>2}" for x in row) for row in board))

def print_move_sequence(dim, moves):
    board = init_state(dim)
    apply_moves(board, moves)
    print_board(board)

def inverse_moves(moves):
    return [Move(m.x,m.y,"ccw" if m.direction == "cw" else "cw") for m in moves[::-1]]

def moves_to_dicts(moves):
    return [asdict(m) for m in moves]

def main():
    print("""
I have a game for you!
    """)

    print("""
Do you want to:
    1 - See an example
    2 - Play the game
    3 - Check if the game is a good cryptographic group?
    """)

    choice = input()
    if choice == '1':
        dim = 4
        example_board = init_state(dim)
        example_moves = random_moves(dim, 1)

        print("Let's show an example")
        print("Starting board:")
        print_board(example_board)
        print()
        print("Making move:")
        print(json.dumps(moves_to_dicts(example_moves)[0]))
        print()
        print("Resulting board:")
        print_board(apply_moves(example_board,example_moves))
    elif choice == '2':
        print("Let's play!")
        dim = 6
        board = init_state(dim)
        board = apply_moves(board, random_moves(dim, 100))
        while True:
            print_board(board)
            print("Make your moves:")
            moves = input()
            moves = [Move(**move) for move in json.loads(moves)]
            board = apply_moves(board, moves)
    elif choice == '3':
        print("I think this would be a good group for non-commutative cryptography. Can you solve the conjugancy search problem in this group?")
        dim = 50
        a = random_moves(dim, random.randint(100000,200000))
        x = random_moves(dim, random.randint(100000,200000))
        board_x = apply_moves(init_state(dim), x)
        board_y = apply_moves(init_state(dim), a + x + inverse_moves(a))
        print("Here's a random conjugancy problem:")
        print("X =")
        print_board(board_x)
        print()
        print("Y =")
        print_board(board_y)
        print()
        print("Give a list of moves S such that S*X*S^{-1} = Y")
        S = [Move(**move) for move in json.loads(input())]
        board = apply_moves(init_state(dim), S + x + inverse_moves(S))
        if board == board_y:
            print("Correct!")
            print("Here's a flag:")
            print(flag)
        else:
            print("Incorrect!")
        
    else:
        print("Invalid choice, exiting")



if __name__=="__main__":
    main()