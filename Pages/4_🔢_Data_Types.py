# Import necessary libraries
import streamlit as st
import ast
import json

# Function to save the selected data types to a JSON file
def save_selected_types():
    with open('selected_types.json', 'w') as file:
        json.dump(st.session_state.selected_types, file, indent=4)
    return 'selected_types.json'

# Function to select data types for the main function arguments
def select_data_types(main_function):
    data_types = ['int', 'float', 'str', 'bool', 'list', 'tuple', 'dict']
    file = ''

    if 'selected_types' not in st.session_state:
        st.session_state.selected_types = {}

    if main_function:
        # Get the arguments of the "Main Function" using the AST
        main_function_args = None
        for node in ast.walk(st.session_state.ast):
            if isinstance(node, ast.FunctionDef) and node.name == main_function:
                main_function_args = [arg.arg for arg in node.args.args]
                break

        if main_function_args:
            # Get the dictionary of data types for the "Main Function"
            main_function_selected_types = st.session_state.selected_types.get(main_function, {})

            # Show the form for the select boxes and the button
            with st.form(key="main_function_form"):
                st.write(f"Select data types for arguments of the Main Function {main_function}:")
                for argument in main_function_args:
                    select_key = f"{main_function}_{argument}_datatype"
                    st.write(f"Select data type for Argument {argument}:")
                    selected_type = st.selectbox("Choose data type", data_types, key=select_key,
                                                label_visibility='collapsed',
                                                index=data_types.index(main_function_selected_types.get(argument, 'int')))
                    main_function_selected_types[argument] = selected_type

                st.write("______")
                submitted = st.form_submit_button("SAVE DATA TYPES")

                if submitted:
                    # Update the data type dictionary for the "Main Function" in the persistent state
                    st.session_state.selected_types[main_function] = main_function_selected_types

                    # Save the selected types to the JSON file
                    file = save_selected_types()

        else:
            st.error("'Main Function' arguments not found.")
    else:
            st.error("No 'Main Function' was found in the source code.")

    # Check if there are types selected for the "Main Function"
    if main_function in st.session_state.selected_types:
        # Get the data types selected for the "Main Function"
        main_function_selected_types = st.session_state.selected_types[main_function]

        # Show the selected data types
        st.success(f"Data Types of {main_function} selected successfully")
        with st.expander("See selected data types."):
            for argument, data_type in main_function_selected_types.items():
                st.write(f"Argument {argument}: {data_type}")

    if file is not None:
        return file, main_function_args

# Graphic User Interface
def main():
    st.set_page_config(page_title = "Data Types", page_icon = "🔢")
    st.title("Defining Data Types")

    # Call the function to select data types and get file_types and main_arguments
    file_types, main_arguments = select_data_types(st.session_state.main_function)

    # Set session state variables if not set
    if "file_types" not in st.session_state:
        st.session_state.file_types = file_types
    if "main_arguments" not in st.session_state:
        st.session_state.main_arguments = main_arguments

# Execute application
if __name__ == "__main__":
    main()
