#! python3.6.3
# py_version.py

# "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"

# - -3 * X^2 + -4 * X^1 - -3 * X^0 + -12 * X^0 + 3 * X^2 + -4 * X^1 - -3 * X^0 = -12 * X^0

import logging
import re


class Cell:
    def __init__(self, value1, value2):
        self.num = value1
        self.pui = value2
        self.is_result = False


def setup_and_apply_rules(string):
    rules = {}
    if not rules:
        rules = {
            'x': 'X',
            'X+': 'X^1+',
            'X-': 'X^1-',
            'X/': 'X^1/',
            'X*': 'X^1*',
            'X=': 'X^1=',
            'X ': 'X^1',
            '+X': '+1*X',
            '-X': '-1*X',
            '=X': '=1*X',
            '++': '+',
            '--': '+',
            '+-': '-',
            '-+': '-'
        }
        """
        WE DELETE SPACES AND THEN ADD ONLY ONE AT THE END TO DETECT SINGLE X CHAR AT THE END OF FORMULA
        """
        string = string.replace(' ', '')
        string += ' '
        for key, value in rules.items():
            string = string.replace(key, value)
        return string


def parse_input(string):
    print("Before rules: ", string)
    new_string = setup_and_apply_rules(string)
    print("After rules: ", new_string)
    # patterns = re.findall("(=?((-?\d+|-?\d+\.\d+)\*X\^(\d+)))", new_string)
    patterns = re.findall("(=?((-?\d+|-?\d+\.\d+)(?![.])(\*?X(\^(-?\d+|-?\d+\.\d+)(?![.]))?)?))", new_string)
    print(patterns)
    """
    INIT CELLS
    """
    cells = []
    cells.append(Cell(float(0), int(0)))
    cells.append(Cell(float(0), int(1)))
    cells.append(Cell(float(0), int(2)))
    results = False
    for pattern in patterns:
        if results is False and '=' in pattern[0]:
            results = True
        if pattern[5] == '':
            new_pattern = (pattern[0], pattern[1], pattern[2], '*X^0', '^0', '0')
            pattern = new_pattern
        cell = Cell(float(pattern[2]), float(pattern[5]))
        doublon = False
        for existing_cell in cells:
            if results is True and existing_cell.pui == float(pattern[5]):
                existing_cell.num -= float(pattern[2])
                cell.num = 0.0
                cell.pui = 0
                cell.is_result = True
                cells.append(cell)
                doublon = True
                break
            elif existing_cell.pui == float(pattern[5]):
                doublon = True
                existing_cell.num += float(pattern[2])
                break
        if not doublon:
            cells.append(cell)
    zero = 0
    for cell in cells:
        if cell.num == 0 and cell.is_result is False:
            cells.remove(cell)
        if cell.num != 0:
            zero += 1
    if zero == 0:
        print("All real numbers are the solution")
        return cells, False
    return cells, True


def print_reduced(cells):
    reduced = ""
    for cell in cells:
        if not cell.is_result:
            if cells.index(cell) != 0 and cell.num > 0:
                reduced += "+ "
            elif cells.index(cell) != 0 and cell.num < 0:
                reduced += "- "
            elif cells.index(cell) == 0 and cell.num < 0:
                reduced += "-"
            if cell.num < 0:
                if cell.num.is_integer():
                    reduced += ("%s * X^%s " % (int(cell.num) * -1, cell.pui))
                else:
                    reduced += ("%s * X^%s " % (cell.num * -1, cell.pui))
            elif cell.num > 0:
                if cell.num.is_integer():
                    reduced += ("%s * X^%s " % (int(cell.num), cell.pui))
                else:
                    reduced += ("%s * X^%s " % (cell.num, cell.pui))
        else:
            if not ('=' in reduced):
                reduced += "= "
                if cell.num == 0:
                    reduced += "0"
                else:
                    reduced += ("%s * X^%s " % (cell.num, cell.pui))
    print(reduced)
    if ("X^1" not in reduced and "X^2" not in reduced):
        print("No solution")
        return False
    if "=" in reduced and "X" in reduced:
        print("Reduced form: ", end="")
        print(reduced)
        return True
    else:
        print("Error, bad format")
        return False


def print_degree(cells):
    max_degree = 0
    print("Polynomial degree: ", end="")
    for cell in cells:
        if cell.pui > max_degree:
            max_degree = cell.pui
    print(max_degree)
    return max_degree


def resolve_deg_two(cells):
    a = 1
    b = 0
    c = 0
    for cell in cells:
        if cell.is_result is False:
            if cell.pui == 2:
                a = cell.num
            elif cell.pui == 1:
                b = cell.num
            elif cell.pui == 0:
                c = cell.num
    delta = b * b - 4 * a * c
    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        x2 = (-b + delta ** 0.5) / (2 * a)
        x1 = (-b - delta ** 0.5) / (2 * a)
        if x1.is_integer() is False:
            print("{0:.6f}".format(x1))
        else:
            print(x1)
        if x2.is_integer() is False:
            print("{0:.6f}".format(x2))
        else:
            print(x2)
    elif delta == 0:
        print("Discriminant is equal to zero, the solution is:")
        x = (-b) / (2 * a)
        if x.is_integer() is False:
            print("{0:.6f}".format(x))
        else:
            print(x)
    else:
        print("Discriminant is strictly negative, there is no solution.")
        return False


def resolve_deg_one(cells):
    a = 1
    b = 0
    for cell in cells:
        if cell.is_result is False and cell.pui == 1:
            a = cell.num
        elif cell.is_result is False and cell.pui == 0:
            b = cell.num
    x = -b / a
    print("The solution is:")
    print(x)


def get_input():
    inp = input()
    ret = True
    if inp == "":
        return
    cells, ret = parse_input(inp)
    if ret is False:
        return
    ret = print_reduced(cells)
    if ret is False:
        return
    degree = print_degree(cells)
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
    elif degree == 2:
        resolve_deg_two(cells)
    else:
        resolve_deg_one(cells)


def start():
    while True:
        get_input()


def init():
    logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
    logging.info('Start of program')


if __name__ == '__main__':
    init()
    start()
    logging.info('End of program')
