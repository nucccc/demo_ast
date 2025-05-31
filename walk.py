code = '''
def fibonacci(i: int) -> int:
    if i == 0 or i == 1:
        return 1
    else:
        return fibonacci(i-1) + fibonacci(i-2)

if __name__ == '__main__':
    for i in range(10):
        print(fibonacci(i))
'''

import ast
import time
from copy import copy
from termcolor import colored

color = 'red'

def get_node_code(node: ast.AST, codelines: list[str]) -> str:
    if node.lineno == node.end_lineno:
        return codelines[node.lineno][node.col_offset:node.end_col_offset]
    else:
        return '\n'.join([codelines[node.lineno][node.col_offset:]] + \
        codelines[node.lineno+1:node.end_lineno] + \
        [codelines[node.end_lineno][:node.end_col_offset]])

def colour_node_code(node: ast.AST, codelines: list[str]) -> str:

    codelines = copy(codelines)

    for codeline in codelines[:node.lineno]:
        print(codeline)
    
    print(codelines[node.lineno][:node.col_offset] + colored(get_node_code(node, codelines), color) + codelines[node.end_lineno][node.end_col_offset:])
    
    for codeline in codelines[node.end_lineno+1:]:
        print(codeline)


tree = ast.parse(code)

codelines = [''] + code.split('\n')

nodes = [node for node in ast.walk(tree) if hasattr(node, 'lineno')]
        
boh = None

i = 0

while boh != "q":
    if 0 <= i < len(nodes): 
        node = nodes[i]

    print('\n'*60)
    print(colored(f'node n° {i} line {node.lineno}: {type(node)}\n\n', color))
    colour_node_code(node, codelines)

    boh = input("")

    if boh == 'd':
        i += 1
        i = min(i, len(nodes))
    elif boh == 'a':
        i -= 1
        i = max(0, i)