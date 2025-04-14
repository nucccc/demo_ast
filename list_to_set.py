import ast

tree = ast.parse('elem = [elem for elem in [num for num in range(10)]]')

class MyNodeTransformer(ast.NodeTransformer):

	def visit_ListComp(self, node):
		self.generic_visit(node)
		return ast.SetComp(
            elt=node.elt,
            generators=node.generators
        )

tree = MyNodeTransformer().visit( tree )

print(ast.unparse(tree))
