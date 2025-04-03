from flask import Flask, request, render_template, jsonify
import random
import copy
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Use a secure key in production

def generate_base_sudoku():
    """Generate a valid base Sudoku grid to shuffle."""
    base_grid = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 4, 5, 6, 7, 8, 9, 1],
        [5, 6, 7, 8, 9, 1, 2, 3, 4],
        [8, 9, 1, 2, 3, 4, 5, 6, 7],
        [3, 4, 5, 6, 7, 8, 9, 1, 2],
        [6, 7, 8, 9, 1, 2, 3, 4, 5],
        [9, 1, 2, 3, 4, 5, 6, 7, 8]
    ]
    return base_grid

def shuffle_sudoku(grid):
    """Randomly shuffle the rows and columns within each 3x3 block."""
    def shuffle_rows(grid):
        rows = [grid[i:i+3] for i in range(0, 9, 3)]
        for block in rows:
            random.shuffle(block)
        return [row for block in rows for row in block]

    def transpose(grid):
        return [list(row) for row in zip(*grid)]

    grid = shuffle_rows(grid)
    grid = transpose(grid)
    grid = shuffle_rows(grid)
    grid = transpose(grid)
    return grid

def remove_numbers(grid, num_holes=40):
    """Remove numbers from the grid to create a puzzle."""
    puzzle = copy.deepcopy(grid)
    for _ in range(num_holes):
        row, col = random.randint(0, 8), random.randint(0, 8)
        while puzzle[row][col] == 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
        puzzle[row][col] = 0
    return puzzle

def generate_sudoku():
    """Generate a random solvable Sudoku puzzle."""
    base_grid = generate_base_sudoku()
    shuffled_grid = shuffle_sudoku(base_grid)
    puzzle = remove_numbers(shuffled_grid)
    return puzzle, shuffled_grid  # Return the puzzle and the solution

@app.route('/')
def index():
    puzzle, solution = generate_sudoku()
    # Send the puzzle and solution as JSON in the rendered page for client-side handling
    return render_template('index.html', puzzle=json.dumps(puzzle), solution=json.dumps(solution))

@app.route('/check_solution', methods=['POST'])
def check_solution():
    # Accept any solution without validation (intended vulnerability)
    data = request.json
    completed = data.get('completed', 0) + 1
    if completed == 200:
        return jsonify({"status": "success", "flag": "SSM{sud0_sud0ku_m4s73r}"})
    new_puzzle, new_solution = generate_sudoku()
    return jsonify({"status": "correct", "completed": completed, "new_puzzle": new_puzzle, "new_solution": new_solution})

if __name__ == '__main__':
    app.run(debug=True)
