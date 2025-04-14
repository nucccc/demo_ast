import ast

code = '''
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    name: str
    psw_hash: str
    birthdate: datetime | None

class OtherClass:

    def __init__(self):
        self._counter = 0
'''

mod = ast.parse(code)

class OurNodeTransformer(ast.NodeTransformer):

    def visit_Module(self, node):
        node.body = [ast.ImportFrom(module='pydantic', names=[ast.alias(name='BaseModel')])] + node.body

        self.generic_visit(node)

        return node
        

    def visit_ClassDef(self, node):
        if 'dataclass' in [decorator.id for decorator in node.decorator_list]:
            node.decorator_list = [
                decorator
                for decorator in node.decorator_list
                if decorator.id != 'dataclass'
            ]
            node.bases = [ast.Name(id='BaseModel')]

        return node

ont = OurNodeTransformer()
ont.visit(mod)

print(ast.unparse(mod))