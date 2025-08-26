def p(grid, rng=range):
    rows, cols = len(grid), len(grid[0])

    # Get all nonzero positions and their values
    nonzero_cells = [
        (row, col, grid[row][col])
        for row in rng(rows)
        for col in rng(cols)
        if grid[row][col] != 0
    ]
    nonzero_cells.sort()

    # Only proceed if exactly two nonzero cells
    if len(nonzero_cells) == 2:
        cell_a, cell_b = nonzero_cells

        # Case 1: Same row
        if cell_a[0] == cell_b[0]:
            row_index = cell_a[0]
            col_a, val_a = cell_a[1], cell_a[2]
            col_b, val_b = cell_b[1], cell_b[2]
            dist = abs(col_b - col_a)

            # Fill the two columns for all rows
            for r in rng(rows):
                grid[r][col_a] = val_a
                grid[r][col_b] = val_b

            # Extend the pattern horizontally
            if dist:
                current_col = max(col_a, col_b) + dist
                toggle = 0
                values = [val_a, val_b]
                if col_b < col_a:
                    values.reverse()
                while current_col < cols:
                    for r in rng(rows):
                        grid[r][current_col] = values[toggle % 2]
                    current_col += dist
                    toggle += 1

        # Case 2: Same column
        elif cell_a[1] == cell_b[1]:
            col_index = cell_a[1]
            row_a, val_a = cell_a[0], cell_a[2]
            row_b, val_b = cell_b[0], cell_b[2]
            dist = abs(row_b - row_a)

            # Fill the two rows for all columns
            for c in rng(cols):
                grid[row_a][c] = val_a
                grid[row_b][c] = val_b

            # Extend the pattern vertically
            if dist:
                current_row = row_b + dist
                toggle = 0
                values = [val_a, val_b]
                while current_row < rows:
                    for c in rng(cols):
                        grid[current_row][c] = values[toggle % 2]
                    current_row += dist
                    toggle += 1

        # Case 3: First nonzero at top row, second at bottom row
        elif cell_a[0] == 0 and cell_b[0] == rows - 1:
            row_a, col_a, val_a = cell_a
            row_b, col_b, val_b = cell_b
            dist = abs(col_b - col_a)

            # Fill two columns
            for r in rng(rows):
                grid[r][col_a] = val_a
                grid[r][col_b] = val_b

            # Extend horizontally
            if dist:
                current_col = col_b + dist
                toggle = 0
                values = [val_a, val_b]
                while current_col < cols:
                    for r in rng(rows):
                        grid[r][current_col] = values[toggle % 2]
                    current_col += dist
                    toggle += 1

        # Case 4: One nonzero in leftmost column, one in rightmost column
        elif (cell_a[1] == 0 and cell_b[1] == cols - 1) or (cell_b[1] == 0 and cell_a[1] == cols - 1):
            if cell_a[1] == 0:
                row_a, col_a, val_a = cell_a
                row_b, col_b, val_b = cell_b
            else:
                row_a, col_a, val_a = cell_b
                row_b, col_b, val_b = cell_a

            dist = abs(row_b - row_a)

            # Fill the two rows
            for c in rng(cols):
                grid[row_a][c] = val_a
                grid[row_b][c] = val_b

            # Extend vertically
            if dist:
                current_row = max(row_a, row_b) + dist
                toggle = 0
                values = [val_a, val_b]
                if row_b < row_a:
                    values.reverse()
                while current_row < rows:
                    for c in rng(cols):
                        grid[current_row][c] = values[toggle % 2]
                    current_row += dist
                    toggle += 1

    return grid
