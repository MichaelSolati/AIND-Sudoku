def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [
    cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI')
    for cs in ('123', '456', '789')
]
diagonal_units = [[rows[i] + cols[i]
               for i in range(9)], [rows[::-1][i] + cols[i] for i in range(9)]]
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)

assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # Go through all coordinates that are potential 'twins'
    for box in [box for box in boxes if len(values[box]) == 2]:
        # Find potential 'twins' from peers
        possible = [peer for peer in peers[box] if values[box] == values[peer]]
        # Ensure only one pair 'twin' from peers exist
        if (len(possible) == 1):
            # Intersection of peers (using sets to avoid duplicates)
            boxSet = set(peers[box]) & set(peers[possible[0]])
            # Remove the two digits in a the naked twins from all common peers
            for point in boxSet:
                for remove in values[box]:
                    assign_value(values, point, values[point].replace(remove, ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    # Create a dictionary from boxes (the grid coordinates) and the grid input (turned into a list)
    dictionary = dict(zip(boxes, list(grid)))
    #Iterate through all points that have a value of '.'
    for coord in [point for point in dictionary if dictionary[point] == '.']:
        # Replace the '.' with '123456789' (possible solutions)
        dictionary[coord] = '123456789'
    return dictionary


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    colCount = 0
    rowCount = 0
    message = ' '
    for row in 'ABCDEFGHI':
        for col in '123456789':
            colCount += 1
            message += values[row + col] + ' '
            if (colCount % 3 == 0 and colCount % 9 != 0):
                message += '| '
        print(message)
        rowCount += 1
        if (rowCount % 3 == 0 and rowCount % 9 != 0):
            print('-------+-------+-------')
        colCount = 0
        message = ' '


def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    # Iterate through every point/box with only one value for that box
    for point in [box for box in boxes if len(values[box]) == 1]:
        # Iterate through that boxes peers
        for peer in peers[point]:
            # Remove the value of the box from its peers
            assign_value(values, peer, values[peer].replace(values[point], '')) 
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            # Create a list of all the boxes in the unit in question that contain the digit in question
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # This box is the only choice for this digit
                assign_value(values, dplaces[0], digit)
    return values


def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Args:
        A sudoku in dictionary form.
    Returns:
        The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        eliminate(values)
        # Your code here: Use the Only Choice Strategy
        only_choice(values)
        # Apply Naked Twins Strategy
        naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len(
            [box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    Args:
        A sudoku in dictionary form.
    Returns:
        The solved sudoku if solvable or False if not solvable.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
    if len([elem for elem in values if len(values[elem]) != 1]) == 0:
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        clone = values.copy()
        clone[s] = value
        clone = search(clone)
        if clone:
            return clone

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Convert string grid to dictionary grid
    answer = grid_values(grid)
    # Search for a solution
    answer = search(answer)
    return answer


if __name__ == '__main__':
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
