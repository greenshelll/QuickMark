def print_points_as_dots(coordinates):
    # Find the minimum and maximum coordinates
    min_x = min(coord[0] for coord in coordinates)
    max_x = max(coord[0] for coord in coordinates)
    min_y = min(coord[1] for coord in coordinates)
    max_y = max(coord[1] for coord in coordinates)

    # Create a grid
    grid = [[' ' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

    # Mark the points on the grid
    for x, y in coordinates:
        grid[y - min_y][x - min_x] = '@'

    # Print the grid
    for row in grid:
        print(''.join(row))

# Example usage:
coordinates =  [[100,100],[200,200]]
print_points_as_dots(coordinates)