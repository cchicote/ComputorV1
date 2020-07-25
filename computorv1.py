import re

# Regexp digit surrounded by - + = / * 
# [^\^][\/+-=](\d+)[\/+-=](?!\*)

signs = ['+', '-', '=', '*', '/', '.']

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

def parse_math_expr(expr):
    isNum = False
    isPow = False
    equalIsPassed = False
    sign = '+'
    cells = []
    cell = []
    
    print("Expr: [%s]" % (expr))
    if expr[len(expr) - 2] in signs:
        print("WRONG FORMAT, CAN'T FINISH BY A SIGN")
        exit(1)

    for char in expr:
        
        print(char)
        # DIGIT
        if char.isdigit():
            if isPow is True and 'X' not in cell:
                print("CELL: [%s] [%s]" % (char, cell))
                print("CAN'T MULTIPLY NUMBERS")
                exit(1)
                #cell.append('*')
                #isPow = False
            if isPow is True and int(char) > 2:
                print("DEGREE TOO HIGH, CAN'T SOLVE")
                exit(1)
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
                print("WRONG FORMAT 1")
                exit(1)
            else:
                cell.append(char)

        # TIMES
        elif char == '*':
            if isPow is True:
                print("ERROR DOUBLE POWER")
                exit(1)
            isPow = True
        
        # X
        elif char == 'X':
            if char in cell:
                print("DOUBLE X")
                exit(1)
            isPow = True
            cell.append(char)
        
        # POW
        elif char == '^':
            if isPow is False:
                print("ERROR NOT POWER YET FOR ^")
                exit(1)
            cell.append(char)

        # EQUAL
        elif char == '=':
            if equalIsPassed is True:
                print("CAN'T BE TWO EQUAL SIGNS")
                exit(1)
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

    return cells

def eval_math_expr(cells):
    sorted_cells = {}
    sorted_cells['0'] = []
    sorted_cells['1'] = []
    sorted_cells['2'] = []
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
            reduced_cells[degree] = 0
            pass
    print("Reduced form: ", end='')
    for degree, reduced_cell in reduced_cells.items():
        if reduced_cell:
            if first_cell is False:
                if reduced_cell > 0:
                    print("+ %s * X^%s" % (reduced_cell, degree), end=' ')
                elif reduced_cell < 0:
                    print("- %s * X^%s" % (reduced_cell * -1, degree), end=' ')
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
        print("GROS PROBLEME, ON NE DEVRAIT PAS LANCER DEG_TWO SI A = 0")
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

def resolve_deg_one(cells):
    a = 1
    b = 0
    for degree, cell in cells.items():
        if degree == '1':
            a = cell
        elif degree == '0':
            b = cell
    x = -b / a
    print("The solution is: %s" % (x))

def print_degree(cells):
    if cells['2'] != 0:
        print("Polynomial degree: 2")
    elif cells['1'] != 0:
        print("Polynomial degree: 1")
    elif cells['0'] != 0:
        print("Polynomial degree: 0")

def main():
    try:
        while True: 
            math_expr = input('Your mathematical expression: ')
            expr = setup_and_apply_rules(math_expr)
            cells = parse_math_expr(expr)
            sorted_cells = eval_math_expr(cells)
            print_degree(sorted_cells)
            if sorted_cells['2'] != 0:
                resolve_deg_two(sorted_cells)
            else:
                resolve_deg_one(sorted_cells)
                
    except KeyboardInterrupt:
        pass

"""
def main():
    try:
        while True:
            math_expr = input('Your mathematical expression: ')
            print("Before trimming: ", math_expr)
            trimmed = setup_and_apply_rules(math_expr)
            print("After trimming: ", trimmed)
            splitted = re.findall(r'[X0-9\.]+|[^X0-9\.]+', trimmed)
            print("After splitting: ", splitted)
    except KeyboardInterrupt:
        pass
"""

if __name__ == "__main__":
    main()
