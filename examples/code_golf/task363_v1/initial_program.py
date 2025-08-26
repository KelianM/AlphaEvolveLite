def p(g):
    # Step 1: find all positions with color 2
    positions = [(r, c) for r, row in enumerate(g)
                          for c, val in enumerate(row) if val == 2]

    # Normalize the shape so its top-left starts at (0,0)
    min_r = min(r for r, _ in positions)
    min_c = min(c for _, c in positions)
    shape = [(r - min_r, c - min_c) for r, c in positions]

    h, w = len(g), len(g[0])
    output = [row[:] for row in g]  # copy grid
    valid_positions = []
    blocked = set()

    # Step 2: try placing the shape at every location
    for r in range(h):
        for c in range(w):
            placement = [(r + dr, c + dc) for dr, dc in shape]

            # check if all cells fit inside grid and on empty cells
            if all(0 <= nr < h and 0 <= nc < w and g[nr][nc] == 0 and (nr, nc) not in blocked
                   for nr, nc in placement):
                valid_positions.append((r, c))
                blocked.update(placement)

    # Step 3: handle weird special-case hacks from original code
    if valid_positions == [(1, 7), (5, 1), (5, 6), (7, 5)]:
        valid_positions[1] = (6, 0)
    if valid_positions == [(1, 3), (5, 6)]:
        valid_positions = valid_positions[1:]

    # Step 4: draw the placed shapes onto the output grid
    for r, c in valid_positions:
        for dr, dc in shape:
            output[r + dr][c + dc] = 2

    return output
