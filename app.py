import numpy as np


# -----------------------------
# Exercise 2: Game of Life step
# -----------------------------
def update_board(current_board):
    """
    Perform one update step of Conway's Game of Life.

    Rules:
    - Any live cell with <2 or >3 neighbors dies
    - Any live cell with 2 or 3 neighbors survives
    - Any dead cell with exactly 3 neighbors becomes alive
    """
    current_board = np.asarray(current_board, dtype=int)
    rows, cols = current_board.shape

    # Create a fresh board for the next state
    updated_board = np.zeros((rows, cols), dtype=int)

    for r in range(rows):
        for c in range(cols):

            # Get bounds safely (edges treated as dead)
            r0 = max(0, r - 1)
            r1 = min(rows, r + 2)
            c0 = max(0, c - 1)
            c1 = min(cols, c + 2)

            # Extract neighborhood
            neighborhood = current_board[r0:r1, c0:c1]

            # Count live neighbors (exclude self)
            live_neighbors = int(neighborhood.sum() - current_board[r, c])

            # Apply rules
            if current_board[r, c] == 1:
                if live_neighbors == 2 or live_neighbors == 3:
                    updated_board[r, c] = 1
            else:
                if live_neighbors == 3:
                    updated_board[r, c] = 1

    return updated_board


# --------------------------------------
# Bonus 3: Recursive Game of Life player
# --------------------------------------
def play_game_recursive(max_steps=25):
    """
    Generate a random 10x10 board and evolve it recursively.
    Stops if the board stabilizes or max_steps reached.
    """
    board = np.random.randint(2, size=(10, 10))

    def recurse(b, steps_left):
        next_b = update_board(b)

        # Stop conditions
        if steps_left <= 1:
            return next_b
        if np.array_equal(next_b, b):
            return next_b

        return recurse(next_b, steps_left - 1)

    return recurse(board, max_steps)


# -----------------------------
# Bonus 4: Knapsack (explained)
# -----------------------------
def knapsack(W, weights, values, full_table=False):
    """
    Solve the 0/1 Knapsack problem using dynamic programming.

    Builds a table where each entry [i][j] represents the maximum
    value achievable using the first i items with capacity j.
    """
    n = len(values)

    # Create DP table
    table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(W + 1):

            # Base case: no items or zero capacity
            if i == 0 or j == 0:
                table[i][j] = 0

            # If item fits, decide to take or leave it
            elif weights[i - 1] <= j:
                take = values[i - 1] + table[i - 1][j - weights[i - 1]]
                leave = table[i - 1][j]
                table[i][j] = max(take, leave)

            # If item doesn't fit, must leave it
            else:
                table[i][j] = table[i - 1][j]

    if full_table:
        return table

    return table[n][W]


# ----------------------------------------
# Optional Challenge: Return chosen items
# ----------------------------------------
def knapsack_with_items(W, weights, values, names=None):
    """
    Knapsack that also returns which items are chosen.
    """
    n = len(values)
    table = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Build table
    for i in range(1, n + 1):
        for j in range(W + 1):
            if weights[i - 1] <= j:
                take = values[i - 1] + table[i - 1][j - weights[i - 1]]
                leave = table[i - 1][j]
                table[i][j] = max(take, leave)
            else:
                table[i][j] = table[i - 1][j]

    # Backtrack to find chosen items
    chosen = []
    j = W

    for i in range(n, 0, -1):
        if table[i][j] != table[i - 1][j]:
            chosen.append(i - 1)
            j -= weights[i - 1]

    chosen.reverse()

    if names is not None:
        return table[n][W], [names[i] for i in chosen]

    return table[n][W], chosen
