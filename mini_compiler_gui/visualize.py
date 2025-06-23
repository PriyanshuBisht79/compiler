from graphviz import Digraph
import os

def generate_ast_image(node, filename="C:/Users/Admin/Desktop/mini_compiler_gui/assets/ast"):
    dot = Digraph()
    counter = [0]

    def add_nodes(n, parent=None):
        node_id = str(counter[0])
        counter[0] += 1
        label = f"{n.type}\\n{n.value}" if n.value is not None else n.type
        dot.node(node_id, label)

        if parent is not None:
            dot.edge(parent, node_id)

        for child in n.children:
            add_nodes(child, node_id)

    add_nodes(node)
    dot.render(filename, format='png', cleanup=True)
