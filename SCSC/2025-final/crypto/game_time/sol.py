from pwn import *
import json
from dataclasses import dataclass, asdict
import random


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

import copy

def solve_puzzle(board):
    """Generates a sequence of moves to transform the board to the initial state."""
    board = copy.deepcopy(board)
    dim = len(board)

    def find_position(target: int) -> tuple:
        nonlocal board
        """Find the position (i, j) of the target value in the board."""

        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == target:
                    return (i, j)
        raise ValueError(f"Target {target} not found in board")

    moves = []
    def make_move(move):
        nonlocal board, moves
        moves.append(move)
        board = apply_move(board, move)
        return board

    def move_left(fr):
        i,j = fr
        if i == dim-1:
            make_move(Move(i-1,j-1, "cw"))
        else:
            make_move(Move(i,j-1, "ccw"))
    
    def move_up(fr):
        i,j = fr
        if j == dim-1:
            make_move(Move(i-1,j-1, "ccw"))
        else:
            make_move(Move(i-1,j, "cw"))

    def move_right(fr):
        i,j = fr
        if i == dim-1:
            make_move(Move(i-1,j, "ccw"))
        else:
            make_move(Move(i,j, "cw"))
    
    def move_down(fr):
        i,j = fr
        if j == dim-1:
            make_move(Move(i,j-1, "cw"))
        else:
            make_move(Move(i,j, "ccw"))

    def move_to(fr,to):
        while fr[0] < to[0]:
            move_down(fr)
            fr = (fr[0]+1, fr[1])
        while fr[1] < to[1]:
            move_right(fr)
            fr = (fr[0], fr[1]+1)
        while fr[0] > to[0]:
            move_up(fr)
            fr = (fr[0]-1, fr[1])
        while fr[1] > to[1]:
            move_left(fr)
            fr = (fr[0], fr[1]-1)
        
    for layer in range(dim-2):
        for col in range(layer,dim-2):
            target = layer * dim + col
            move_to(find_position(target),(layer,col))
        
        move_to(find_position(layer*dim+dim-1),(layer,dim-2))

        if find_position(layer*dim+dim-2) == (layer,dim-1):
            make_move(Move(layer,dim-2, "cw"))
            make_move(Move(layer+1,dim-2, "ccw"))
            make_move(Move(layer,dim-2, "ccw"))
        move_to(find_position(layer*dim+dim-2),(layer+1,dim-2))
        
        make_move(Move(layer,dim-2, "cw"))


        for row in range(layer,dim-2):
            target = row * dim + layer
            move_to(find_position(target),(row,layer))
        
        move_to(find_position((dim-1)*dim+layer),(dim-2,layer))

        if find_position((dim-2)*dim+layer) == (dim-1,layer):
            make_move(Move(dim-2,layer, "ccw"))
            make_move(Move(dim-2,layer+1, "cw"))
            make_move(Move(dim-2,layer, "cw"))
        move_to(find_position((dim-2)*dim+layer),(dim-2,layer+1))
        make_move(Move(dim-2,layer, "ccw"))
    return moves

def get_cycles(board):
    dim = len(board)
    seen = [0]*dim*dim
    ret = []
    flat = sum(board,[])
    for i in range(dim*dim):
        if seen[i]:
            continue
        x = i
        cyc = []
        while True:
            x = flat[x]
            if seen[x]:
                break
            cyc.append(x)
            seen[x] = True
        ret.append(cyc)
    return ret

def find_conjugating_move(x_board, y_board, dim):
    cycles_x = sorted(get_cycles(x_board),key=lambda x: len(x))
    cycles_y = sorted(get_cycles(y_board),key=lambda x: len(x))
    print(cycles_x)
    print(cycles_y)

    for offset in range(100):
        permutation = [0]*dim*dim
        for cyc_x, cyc_y in zip(cycles_x, cycles_y):
            for i in range(len(cyc_y)):
                permutation[cyc_x[i]] = cyc_y[(i+offset)%len(cyc_y)]

        board_S = [permutation[i:i+dim] for i in range(0,dim*dim,dim)]
        
        s_moves = solve_puzzle(board_S)
        s_moves = inverse_moves(s_moves)
        
        if board_S == apply_moves(init_state(dim), s_moves):
            break

    return s_moves

# Initialize process
r = process("./container/chall.py")

# Select option 3 (conjugancy problem)
r.recvuntil(b"3 - Check if the game is a good cryptographic group?")
r.sendline(b"3")

# Extract board X
r.recvuntil(b"X =\n")
x_board_data = r.recvuntil(b"\n\nY =", drop=True).decode().strip()
x_board_lines = x_board_data.split('\n')
x_board = []
for line in x_board_lines:
    row = [int(num.strip()) for num in line.split(',')]
    x_board.append(row)


# Extract board Y
y_board_data = r.recvuntil(b"\n\nGive", drop=True).decode().strip()
y_board_lines = y_board_data.split('\n')
y_board = []
for line in y_board_lines:
    row = [int(num.strip()) for num in line.split(',')]
    y_board.append(row)

dim = len(x_board)

print("Recived board X")
print_board(x_board)
print("Recived board Y")
print_board(y_board)

print("Solving conjugancy problem")
solution = find_conjugating_move(x_board, y_board, dim)

print("Found conjugating moves")

solution_json = json.dumps([asdict(m) for m in solution])

r.recvuntil(b"S*X*S^{-1} = Y")
print("sending...")
r.sendline(solution_json.encode())

# Receive output and flag
output = r.recvall().decode()
print(output)
