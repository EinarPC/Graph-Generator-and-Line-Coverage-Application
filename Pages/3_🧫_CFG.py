# Import necessary libraries
import streamlit as st
from staticfg import CFGBuilder
import ast

# Function to find the main function in the source code
def find_main_function(source_code):
    ast_tree = ast.parse(source_code)
    all_functions = set()
    called_functions = set()
    defined_classes = set()

    # Loop through the AST and store all functions in an array
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.FunctionDef):
            all_functions.add(node.name)
        elif isinstance(node, ast.ClassDef):
            defined_classes.add(node.name)

    # Loop through the AST again and find the functions that are called by other functions
    for node in ast.walk(ast_tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called_functions.add(node.func.id)

    # The main function will be the one that is in all_functions but is not in called_functions
    main_function = next(func for func in all_functions if func not in called_functions and func not in defined_classes)

    return main_function

# Function to generate and display the General CFG of the entire program
def generate_cfg_general(file_name):
    cfg = CFGBuilder().build_from_file(file_name, file_name)
    cfg.build_visual('source_CFG', 'png')
    st.write(f"General Control Flow Graph")
    st.image('source_CFG.png', use_column_width=True)

# Function to generate and display the CFGs for each function inside the program
def generate_cfg_method(file_name):
    # Parse the source file
    with open(file_name, 'r') as f:
        source_code = f.read()
    ast_tree = ast.parse(source_code)   # Built ast

    if "ast" not in st.session_state:
        st.session_state.ast = ast_tree # Add ast tree to dictionary session state

    # Generate CFG for each function
    ast_trees = []  # List to store method ASTs
    method_list = []  # List to store method names and function sources
    args_list = []  # List to store methods args
    indexes_list = [] # List to store methods indexes
    names_list = [] # List to store methods names
    main_f = find_main_function(source_code)
    main_fdef = next((node for node in ast.walk(ast_tree) if isinstance(node, ast.FunctionDef) and node.name == main_f), None)   # Find the FunctionDef object corresponding to the main function

    # Iterate over all nodes to filter Function Defs
    for node in ast_tree.body:
        if isinstance(node, ast.FunctionDef):
            # Get information about every method
            function_name = node.name
            names_list.append(function_name)
            function_source = ast.get_source_segment(source_code, node)
            function_ast_tree = build_ast_tree(node)
            ast_trees.append(function_ast_tree) # Add all function tress
            method_list.append((function_name, function_source))  # Add function name and source to list
            method_index = method_list.index((function_name, function_source)) + 1
            args = [arg.arg for arg in node.args.args]
            num_conditionals = count_conditionals(function_source)
            ast_tree = ast_trees[method_index - 1]
            ast_tree_str = print_ast_tree(ast_tree, indent=4)
            args_list.append(args)
            indexes_list.append(method_index)
    
            # Display method button
            if st.sidebar.button(f"{function_name}"):
                st.write(f"Control Flow Graph for {function_name} method:")
                cfg = CFGBuilder().build_from_src(function_name, function_source)
                cfg.build_visual(function_name, 'png')
                st.image(f'{function_name}.png', use_column_width=True)
            
                with st.expander(f"Click to see more information about the {function_name} method."):
                    st.write(f"ID: {method_index}")
                    st.write(f"Arguments of {function_name}: {', '.join(args)}")
                    st.write(f"Number of conditionals in {function_name}: {num_conditionals}")
                    st.write(f"AST for {function_name} method:")
                    st.code(ast_tree_str, language="python")
    
    # Update or add information to dictionary session state
    if "function_arguments" not in st.session_state:
        st.session_state.function_arguments = args_list
    if "method_index" not in st.session_state:
        st.session_state.method_indexes = indexes_list
    if "function_names" not in st.session_state:
        st.session_state.function_names = names_list
    if "main_function" not in st.session_state:
        st.session_state.main_function = main_f
    if "main_functiondef" not in st.session_state:
        st.session_state.main_functiondef = main_fdef

# Class to represent nodes in the AST
class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, level=0):
        indent = "  " * level
        st.code(f"{indent}{self.value}")
        for child in self.children:
            child.print_tree(level + 1)

# Function to build the AST of an individual method
def build_ast_tree(node):
    ast_node = ASTNode(node.__class__.__name__)
    for child_node in ast.iter_child_nodes(node):
        ast_child_node = build_ast_tree(child_node)
        ast_node.add_child(ast_child_node)
    return ast_node

# Function to print the AST tree as a string
def print_ast_tree(ast_node, indent=0):
    tree_str = ""
    indent_str = " " * indent

    if isinstance(ast_node, ASTNode):
        tree_str += f"{indent_str}{ast_node.value}\n"
        for child in ast_node.children:
            tree_str += print_ast_tree(child, indent + 2)
    elif isinstance(ast_node, list):
        for item in ast_node:
            tree_str += print_ast_tree(item, indent)
    else:
        tree_str += f"{indent_str}{ast_node}\n"

    return tree_str

# Visitor class to count the number of conditionals
class ConditionalCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0  # Initialize the counter to 0

    def visit_If(self, node):
        # Increment the counter when visiting an 'if' statement node
        self.count += 1
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_While(self, node):
        # Increment the counter when visiting a 'while' loop node
        self.count += 1
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_For(self, node):
        # Increment the counter when visiting a 'for' loop node
        self.count += 1
        self.generic_visit(node)  # Continue visiting child nodes

# Function to count the number of conditionals in a function
def count_conditionals(function_source):
    # Parse the function source code into an AST
    ast_tree = ast.parse(function_source)
    
    # Create an instance of the ConditionalCounter class
    conditional_counter = ConditionalCounter()
    
    # Visit the AST to count the number of conditionals
    conditional_counter.visit(ast_tree)
    
    # Return the count of conditionals
    return conditional_counter.count

# Graphic User Interface
def main():
    st.set_page_config(page_title = "CFGs", page_icon = "🧫")
    st.title("Control Flow Graph Generator")

    generate_cfg_general('uploaded_file.py')
    generate_cfg_method('uploaded_file.py')

# Execute application
if __name__ == "__main__":
    main()

