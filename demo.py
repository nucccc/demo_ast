import ast

from pathlib import Path
from typing import Iterator

import polars as pl
import seaborn as sns
from matplotlib import pyplot as plt


root = Path('../../repos/pydantic/pydantic')

def iter_pyfiles(dir: Path) -> Iterator[Path]:
    for elem in dir.iterdir():
        if elem.is_dir():
            for pyfile in iter_pyfiles(elem):
                yield pyfile
        elif elem.is_file() and elem.name.endswith('.py'):
            yield elem


class MC(ast.NodeVisitor):

    def __init__(self):
        self.func_names: list[str] = list()
        self.func_data: list[dict] = list()
        self.list_comp_data: list[dict] = list()

    def set_file(self, path: Path, code: str):
        self.path = path
        self.code = code

    def visit_FunctionDef(self, node):
        self.func_names.append(node.name)

        doc_str = ast.get_docstring(node)

        self.func_data.append({
            'name': node.name,
            'line_no': node.lineno,
            'n_lines': node.end_lineno - node.lineno,
            'n_chars': len(ast.get_source_segment(self.code, node)),
            'n_args': len(node.args.args),
            'path': str(self.path),
            'doc_str': doc_str
        })

        self.generic_visit(node)

    def visit_ListComp(self, node):

        self.list_comp_data.append({
            'line_no': node.lineno,
            'len': node.end_col_offset - node.col_offset,
            'path': self.path,
            'n_lines': node.end_lineno - node.lineno,
        })
        
        self.generic_visit(node)

    def visit_Import(self, node):

        if node.lineno > 100:
            pass #print(f'{ast.get_source_segment(self.code, node)}\t\t\t {self.path}:{node.lineno}')

        self.generic_visit(node)

    def visit_ImportFrom(self, node):

        if node.lineno > 100:
            pass #print(f'{ast.get_source_segment(self.code, node)}\t\t\t {self.path}:{node.lineno}')

        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        for subnode in node.body:
            if isinstance(subnode, ast.FunctionDef) and subnode.name == '__call__':
                pass# print(f'In {self.path}:{node.lineno} class {node.name} is defined as a callable')
        
        # checking if there are dataclasses
        if 'dataclass' in {decorator.id for decorator in node.decorator_list if hasattr(decorator, 'id')}:
            print(f'In {self.path}:{node.lineno} class {node.name} is a dataclass')

mc = MC()

for pyfile in iter_pyfiles(root):
    code = pyfile.read_text()

    ast_mod = ast.parse(code)    

    mc.set_file(pyfile, code)
    mc.visit(ast_mod)

df = pl.DataFrame(mc.func_data)

df.write_csv('funcs.csv')

lcdf = pl.DataFrame(mc.list_comp_data)

plt.plot(df['n_lines'], df['n_chars'], 'o')
plt.show()

sns.histplot(df['n_lines'])
plt.title('Distribution of number of codelines')
plt.xlabel('Number of codelines')
plt.show()