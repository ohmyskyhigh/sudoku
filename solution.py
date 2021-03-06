assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'
import collections

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]


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


def common_elements(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result


boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = list(zip(rows, cols[::-1]))
diagonal2 = list(zip(rows, cols))
diagonal1 = [''.join(d) for d in diagonal1]
diagonal2 = [''.join(d) for d in diagonal2]
print(diagonal1)
print(diagonal2)
diagonal = [diagonal1, diagonal2]
unitlist = row_units + column_units + square_units + diagonal
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all the possible naked twins (length of 2)
    values2 = {loc: num for loc, num in values.items() if len(num) == 2}
    if len(values2) > 1:
        # the list of locations
        v = list(values2.values())
        #find the naked_twins values
        pair_value = [item for item, count in collections.Counter(v).items() if count > 1]
        #the possible naked_twins
        for i in pair_value:
            #find out the box with same value
            pair = [box for box, v in values2.items() if v == i]
            twins_dict = {}
            for e in pair:
                peer = [p for p in unitlist if e in p]
                twins_dict.update({e: peer})
            used = []
            for loc1, peer1 in twins_dict.items():
                #damp all the used boxes
                used.append(loc1)
                for loc2, peer2 in twins_dict.items():
                     if loc2 not in used:
                         #find the peer
                         del_list = common_elements(peer1, peer2)
                         if len(del_list) is not 0:
                             for box1 in del_list:
                                 for box2 in box1:
                                     new_num = [n for n in values[box2] if n not in i]
                                     if len(new_num) is not 0:
                                         value = ''.join(new_num)
                                         values = assign_value(values, box2, value)
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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """

    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            value = values[peer].replace(digit,'')
            values = assign_value(values, peer, value)
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)

    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    grid_dict = dict(zip(boxes, grid))
    grid_dict = {key: '123456789' if v == '.' else v for key, v in grid_dict.items()}
    grid_dict = search(grid_dict)

    return grid_dict

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
       print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
