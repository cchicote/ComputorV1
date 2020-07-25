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

    if expr[len(expr) - 2] in signs:
        print("WRONG FORMAT, CAN'T FINISH BY A SIGN")
        exit(1)

    for char in expr:
        
        # DIGIT
        if char.isdigit():
            if isPow is True and 'X' not in cell:
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

    if len(cell) > 0:
        cell = ''.join(cell)
        cells.append(cell)

    return cells

def eval_math_expr(cells):
    sorted_cells = {}
    sorted_cells['0'] = []
    sorted_cells['1'] = []
    sorted_cells['2'] = []
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
            sorted_cell = eval(''.join(sorted_cell))
            sorted_cells[degree] = sorted_cell
        except SyntaxError:
            pass
    print("Reduced form: ", end='')
    for degree, sorted_cell in sorted_cells.items():
        if sorted_cell:
            print("%s * X^%s" % (sorted_cell, degree), end=' ')
    print("= 0")

def main():
    try:
        while True: 
            math_expr = input('Your mathematical expression: ')
            expr = setup_and_apply_rules(math_expr)
            cells = parse_math_expr(expr)
            eval_math_expr(cells)
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
