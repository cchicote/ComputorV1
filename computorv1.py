import re

# Regexp digit surrounded by - + = / * 
# [^\^][\/+-=](\d+)[\/+-=](?!\*)

signs = ['+', '-', '=', '*', '/']

class CustomError(Exception):
    pass

def check_for_spaces_between_numbers(string):
    splitted = string.split()
    isNum = False
    for split in splitted:
        if isNum is True and split[0] not in signs:
            raise CustomError("Bad format (check spacing)")
        if split[len(split) - 1].isdigit():
            isNum = True
        else:
            isNum = False

def setup_and_apply_rules(string):
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
    check_for_spaces_between_numbers(string)
    string = string.replace(' ', '')
    string += ' '
    for key, value in rules.items():
        string = string.replace(key, value)
    return string

def parse_math_expr(expr):
    isNum = False
    isPow = False
    equalIsPassed = False
    sign = '+'
    cells = []
    cell = []
    
    # DEBUG
    # print("Expr: [%s]" % (expr))
    if expr[len(expr) - 2].isdigit() is False:
        raise CustomError("Equation must end by a digit")

    for char in expr:
        
        # Handling the power
        if isPow is True:
            if char.isdigit():
                if int(char) >= 0 and int(char) <= 2 and 'X' in cell and '^' in cell:
                    cell.append(char)
                    isPow = False
                    continue
                elif int(char) > 2 or int(char) < 0:
                    raise CustomError("The polynomial degree is strictly greater than 2, I can't solve.")
            elif char == 'X':
                cell.append(char)
                continue
            elif char == '^' and 'X' in cell:
                cell.append(char)
                continue
            elif 'X' not in cell or '^' not in cell:
                raise CustomError("Bad format with the power")
            else:
                raise CustomError("Bad format with the degree")

        # DIGIT
        if char.isdigit():
            if isNum is False:
                if len(cell) > 0:
                    cell = ''.join(cell)
                    cells.append(cell)
                cell = []
                if equalIsPassed is True:
                    if sign is '+':
                        cell.append('-')
                    elif sign is '-':
                        cell.append('+')
                else:
                    cell.append(sign)
                cell.append(char)
                isNum = True
            else:
                cell.append(char)

        # MINUS
        elif char == '-':
            isPow = False
            if isNum is True:
                sign = '+'
                if len(cell) > 0:
                    cell = ''.join(cell)
                    cells.append(cell)
                    cell = []
                isNum = False
            if sign == '' or sign == '+':
                sign = '-'
            else:
                sign = '+'

        # PLUS
        elif char == '+':
            isPow = False
            if isNum is True:
                sign = '+'
                if len(cell) > 0:
                    cell = ''.join(cell)
                    cells.append(cell)
                    cell = []
                isNum = False
            if sign == '' or sign == '+':
                sign = '+'
            else:
                sign = '-'

        # DOT
        elif char == '.':
            if len(cell) == 0 or isNum is False:
                raise CustomError("Bad format for decimal")
            else:
                cell.append(char)

        # TIMES
        elif char == '*':
            if isPow is True:
                raise CustomError("Misplaced * sign")
            isPow = True
        
        # X
        elif char == 'X':
            if char in cell:
                raise CustomError("Misplaced X")
            isPow = True
            cell.append(char)

        # EQUAL
        elif char == '=':
            if equalIsPassed is True:
                raise CustomError("There cannot be two = signs")
            if len(cell) > 0:
                cell = ''.join(cell)
                cells.append(cell)
                cell = []
            sign = '+'
            equalIsPassed = True
            isNum = False
            isPow = False

    if len(cell) > 0:
        cell = ''.join(cell)
        cells.append(cell)

    if equalIsPassed is False:
        print("We presume that your equation is equal to zero")

    return cells

def eval_math_expr(cells):
    sorted_cells = {}
    sorted_cells['2'] = []
    sorted_cells['1'] = []
    sorted_cells['0'] = []
    reduced_cells = {}
    first_cell = True
    for cell in cells:
        if "X^1" in cell:
            sorted_cells['1'].append(cell.split('X')[0])
        elif "X^2" in cell:
            sorted_cells['2'].append(cell.split('X')[0])
        else:
            sorted_cells['0'].append(cell.split('X')[0])
    print(sorted_cells)
    for degree, sorted_cell in sorted_cells.items():
        try:
            reduced_cells[degree] = eval(''.join(sorted_cell))
        except SyntaxError:
            # Throws a syntax error if eval an empty string
            # If the cell contains only an X for example, its len should be 1
            # And the value of X is equal to 1 * X
            # Otherwise it's a 0 
            if len(sorted_cell):
                reduced_cells[degree] = 1
            else:
                reduced_cells[degree] = 0
            continue
    print("Reduced form: ", end='')
    for degree, reduced_cell in reduced_cells.items():
        if reduced_cell:
            if first_cell is False:
                if reduced_cell > 0:
                    print("+ ", end='')
                elif reduced_cell < 0:
                    print("- ", end='')
                if degree == '0':
                    print("%s" % (reduced_cell), end=' ')
                elif degree == '1':
                    print("%s * X" % (reduced_cell), end=' ')
                else:
                    print("%s * X^%s" % (reduced_cell, degree), end=' ')
            else:
                if degree == '0':
                    print("%s" % (reduced_cell), end=' ')
                elif degree == '1':
                    print("%s * X" % (reduced_cell), end=' ')
                else:
                    print("%s * X^%s" % (reduced_cell, degree), end=' ')
                first_cell = False
    print("= 0")
    return reduced_cells

def resolve_deg_two(cells):
    a = cells['2']
    b = cells['1']
    c = cells['0']
    if a == 0:
        raise CustomError("Resolution of degree 2 should not be executed if a is equal to 0")
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
        print("Discriminant is strictly negative, the two complex solutions are:")
        res_p1 = -b / (2 * a)
        res_p2 = ((delta ** 0.5) / (2 * a)).imag
        print("%s + i * %s" % ("{0:.6f}".format(res_p1), "{0:.6f}".format(res_p2)))
        print("%s - i * %s" % ("{0:.6f}".format(res_p1), "{0:.6f}".format(res_p2)))

def resolve_deg_one(cells):
    a = 1
    b = 0
    for degree, cell in cells.items():
        if degree == '1':
            a = cell
        elif degree == '0':
            b = cell
    x = -b / a
    print("The solution is: %s" % ("{0:.6f}".format(x)))

def print_degree(cells):
    if cells['2'] != 0:
        print("Polynomial degree: 2")
        return 2
    elif cells['1'] != 0:
        print("Polynomial degree: 1")
        return 1
    else:
        print("Polynomial degree: 0")
        return 0

def main():
    try:
        while True: 
            try:
                math_expr = input('Your mathematical expression: ')
                expr = setup_and_apply_rules(math_expr)
                cells = parse_math_expr(expr)
                sorted_cells = eval_math_expr(cells)
                degree = print_degree(sorted_cells)
                if degree == 0:
                    if sorted_cells['0'] == 0:
                        print("All real numbers are the solution")
                    else:
                        print("There is no solution.")
                elif degree == 2:
                    resolve_deg_two(sorted_cells)
                elif degree == 1:
                    resolve_deg_one(sorted_cells)
            except CustomError as message:
                print("ERROR: [%s]" % (message))
                
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
