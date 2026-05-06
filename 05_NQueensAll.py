def is_safe(board, row, col):
    """ Check if it's safe to place a queen at board[row][col] """
    n = len(board)
    
    # Check column
    for i in range(row):
        if board[i][col] == 1:
            return False
    
    # Check upper diagonal on left side
    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1
    
    # Check upper diagonal on right side
    i, j = row, col
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1
    
    return True

def solve_queens(board, row, solutions):
    """ Recursively solve the 8-Queens Problem using backtracking """
    n = len(board)
    
    # Base case: If all queens are placed, add the solution to the list
    if row >= n:
        solutions.append([row[:] for row in board])
        return
    
    for col in range(n):
        if is_safe(board, row, col):
            board[row][col] = 1  # Place the queen
            solve_queens(board, row + 1, solutions)
            board[row][col] = 0  # Backtrack

def print_board(board):
    """ Print the board configuration """
    n = len(board)
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print()
    print()

def print_all_solutions():
    """ Solve the 8-Queens Problem and print all distinct solutions """
    n = 8  # Size of the chessboard (8x8)
    board = [[0] * n for _ in range(n)]  # Initialize empty board
    solutions = []
    
    solve_queens(board, 0, solutions)
    
    # Print all solutions found
    num_solutions = len(solutions)
    if num_solutions == 0:
        print("No solutions found.")
    else:
        print(f"Total solutions found: {num_solutions}")
        for idx, solution in enumerate(solutions, start=1):
            print(f"Solution {idx}:")
            print_board(solution)

# Call the function to print all solutions to the 8-Queens Problem
print_all_solutions()
