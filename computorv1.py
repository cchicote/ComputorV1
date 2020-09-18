import re
import collections

signs = ['+', '-', '=', '*', '^', '.']

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
    if " ^" in string:
        raise CustomError("Bad format: space before ^ detected")
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
    
    if expr[-1].isspace():
        expr = expr[:-1]
    if expr[-1].isdigit() is False:
        raise CustomError("Equation must end by a digit")

    for char in expr:
        
        # Checking char
        if char.isdigit() is False and char != 'X' and char not in signs:
            if char == ' ':
                continue
            raise CustomError("Wrong char encountered: %s" % (char))

        # Handling the power
        if isPow is True:
            if char.isdigit() and '^' in cell and 'X' in cell:
                cell.append(char)
                continue
            elif char == 'X':
                cell.append(char)
                continue
            elif char == '^' and 'X' in cell:
                cell.append(char)
                continue
            elif (char == '+' or char == '-' or char == '=') and '^' in cell and 'X' in cell and cell[-1].isdigit():
                isPow = False
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

def replace_eval(cells):
    res = 0
    for cell in cells:
        res += float(cell)
    return res

def eval_math_expr(cells):
    sorted_cells = {}
    reduced_cells = {}
    first_cell = True
    for cell in cells:
        try:
            power = cell.split('^')[1]
        except IndexError:
            power = '0'
        splitted = cell.split('X')[0]
        if splitted == '':
            splitted = '+1'
        if '.' not in splitted and int(splitted[1:]) != 0:
            splitted = splitted[0] + splitted[1:].lstrip('0')
        if power in sorted_cells.keys():
            sorted_cells[power].append(splitted)
        else:
            sorted_cells[power] = [splitted]
    for degree, sorted_cell in sorted_cells.items():
        reduced_cells[degree] = replace_eval(sorted_cell)

    reduced_cells = collections.OrderedDict(sorted(reduced_cells.items(), reverse=True))
    print("Reduced form: ", end='')
    for degree, reduced_cell in reduced_cells.items():
        if reduced_cell:
            if first_cell is False:
                if reduced_cell > 0:
                    print("+ ", end='')
                elif reduced_cell < 0:
                    print("- ", end='')
                    reduced_cell = reduced_cell * -1
                if degree == '0':
                    print("%s" % (reduced_cell), end=' ')
                else:
                    print("%s * X^%s" % (reduced_cell, degree), end=' ')
            else:
                if degree == '0':
                    print("%s" % (reduced_cell), end=' ')
                else:
                    print("%s * X^%s" % (reduced_cell, degree), end=' ')
                first_cell = False
        elif not reduced_cell and first_cell is True and degree == '0':
            print("0", end=' ')
    print("= 0")
    max_deg = 0
    raiseError = False
    for degree, sorted_cell in reduced_cells.items():
        if int(degree) in range (0, 3) and int(degree) > max_deg and sorted_cell != 0:
            max_deg = int(degree)
        if int(degree) > 2 and sorted_cell != 0:
            raiseError = True
            break
    print("Polynomial degree: %s" % (max_deg))
    if raiseError:
        raise CustomError("The polynomial degree is strictly greater than 2, I can't solve.")
    return reduced_cells, max_deg

def mysqrt(number):
    iterations = 1000
    x = number
    for i in range(iterations):
        if x * x == number:
            return x
        x = (x + (number / x)) / 2
    return x

def resolve_deg_two(cells):
    try:
        a = cells['2']
    except KeyError:
        a = 0
    try:
        b = cells['1']
    except KeyError:
        b = 0
    try:
        c = cells['0']
    except KeyError:
        c = 0
    if a == 0:
        raise CustomError("Resolution of degree 2 should not be executed if a is equal to 0")
    delta = b * b - 4 * a * c
    if delta > 0:
        print("Discriminant is strictly positive, the two solutions are:")
        x2 = (-b + mysqrt(delta)) / (2 * a)
        x1 = (-b - mysqrt(delta)) / (2 * a)
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
        res_p2 = (mysqrt(abs(delta)) / (2 * a))
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
    # We add zero so we don't get a -0 as a solution in some cases like 0=2x
    x += 0
    if x.is_integer():
        print("The solution is: %s" % (x))
    else:
        print("The solution is: %s" % ("{0:.6f}".format(x)))

def main():
    try:
        while True: 
            try:
                math_expr = input('Your mathematical expression: ')
                expr = setup_and_apply_rules(math_expr)
                cells = parse_math_expr(expr)
                sorted_cells, degree = eval_math_expr(cells)
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
