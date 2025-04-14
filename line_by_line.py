code = '''
def f():
    if True:
        for i in range(5):
            print(i)
        else:
            print('printed all the numbers')
        
        try:
            num = int('fourtytwo')
        except ValueError:
            print('naaaaa')
        else:
            print('unexpectedly')
        finally:
            print('anyways it\\'s an overrated movie')
    elif 5 < 4:
        print('never')
    else:
        print('never going to happen')
'''

import ast
from copy import copy
from typing import Iterator
from termcolor import colored

attrs_to_iter = [
    'body', 'handlers', 'orelse', 'finalbody'
]

def iter_bodies(node: ast.AST) -> Iterator[ast.AST]:
    yield node
    for attr in attrs_to_iter:
        if hasattr(node, attr):
            for subnode in getattr(node, attr):
                for elem in iter_bodies(subnode):
                    yield elem

def iter_stmts(node: ast.AST) -> list[ast.stmt]:
    stmts: list[ast.stmt] = [subnode for subnode in ast.walk(node) if isinstance(subnode, ast.stmt)]
    stmts.sort(key = lambda n: n.lineno)
    return stmts

color = 'cyan'

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

nodes = [node for node in iter_stmts(tree) if hasattr(node, 'lineno')]
        
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