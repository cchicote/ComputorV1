#! python3.6.3
# test_regex.py

import logging
import re
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s -  %(levelname)s -  %(message)s')
#logging.disable(logging.CRITICAL)
logging.debug('Start of program')

def setup_and_apply_rules(string):
    rules = {}
    if not rules:
        rules = {
            ' ': '',
            'X+': 'X^1+',
            'X-': 'X^1-',
            'X/': 'X^1/',
            'X*': 'X^1*',
            '+X': '+1*X',
            '-X': '-1*X',
            '=X': '=1*X',
            '++': '+',
            '--': '+',
            '+-': '-',
            '-+': '-'
        }
        for key, value in rules.items():
            string = string.replace(key, value)
        return string

string = "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
string = "5 + 4 * X + X^2= X^2"

new_string = setup_and_apply_rules(string)
#patterns = re.findall("(=?((-?\d+|-?\d+\.\d+)\*X\^(\d+)))", new_string)

patterns = re.findall("(=?((-?\d+|-?\d+\.\d+)(?![\.])(\*?X(\^(\d+))?)?))", new_string)
print(patterns)

print(string)
print(new_string)

logging.debug('End of program')