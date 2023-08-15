import streamlit as st
import ast
import json

# Función para guardar los tipos seleccionados en el archivo JSON
def save_selected_types():
    with open('selected_types.json', 'w') as file:
        json.dump(st.session_state.selected_types, file, indent=4)
    return 'selected_types.json'

def select_data_types(main_function):
    data_types = ['int', 'float', 'str', 'bool', 'list', 'tuple', 'dict']
    file = ''

    if 'selected_types' not in st.session_state:
        st.session_state.selected_types = {}

    if main_function:
        # Obtener los argumentos de la "Función Principal" utilizando el AST
        main_function_args = None
        for node in ast.walk(st.session_state.ast):
            if isinstance(node, ast.FunctionDef) and node.name == main_function:
                main_function_args = [arg.arg for arg in node.args.args]
                break

        if main_function_args:
            # Obtener el diccionario de tipos de datos para la "Función Principal"
            main_function_selected_types = st.session_state.selected_types.get(main_function, {})

            # Mostrar el formulario para los select boxes y el botón
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
                    # Actualizar el diccionario de tipos de datos para la "Función Principal" en el estado persistente
                    st.session_state.selected_types[main_function] = main_function_selected_types

                    # Guardar los tipos seleccionados en el archivo JSON
                    file = save_selected_types()

        else:
            st.error("No se encontraron los argumentos de la 'Función Principal'.")
    else:
            st.error("No se encontró una 'Función Principal' en el código fuente.")

    # Verificar si hay tipos seleccionados para la "Función Principal"
    if main_function in st.session_state.selected_types:
        # Obtener los tipos de datos seleccionados para la "Función Principal"
        main_function_selected_types = st.session_state.selected_types[main_function]

        # Mostrar los tipos de datos seleccionados
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

    file_types, main_arguments = select_data_types(st.session_state.main_function)

    if "file_types" not in st.session_state:
        st.session_state.file_types = file_types
    if "main_arguments" not in st.session_state:
        st.session_state.main_arguments = main_arguments

# Execute application
if __name__ == "__main__":
    main()
