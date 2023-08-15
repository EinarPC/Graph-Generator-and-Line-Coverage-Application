# Import necessary libraries
import streamlit as st
import json
import math
import random

# Function to ask for a range of integers
def ask_range_integer(argument):
    key_min = f"{argument}_min"
    key_max = f"{argument}_max"
    min_value = st.number_input("Enter the minimum value (if a specific value, enter the same in both number inputs):", key=key_min)
    max_value = st.number_input("Enter the maximum value (if a specific value, enter the same in both number inputs):", key=key_max)
    min_value = int(min_value)
    max_value = int(max_value)
    return min_value, max_value

# Function to ask for a range of floating-point numbers
def ask_range_float(argument):
    key_min = f"{argument}_min"
    key_max = f"{argument}_max"
    min_value = st.number_input(f"Enter the minimum value (if a specific value, enter the same in both number inputs):", key=key_min)
    max_value = st.number_input(f"Enter the maximum value (if a specific value, enter the same in both number inputs):", key=key_max)
    return min_value, max_value

# Function to ask for a range of elements in a list
def ask_range_list(argument):
    key_n = f"{argument}_n"
    key_min = f"{argument}_min"
    key_max = f"{argument}_max"
    num_elements = st.number_input("Enter the number of elements in the list:", key = key_n)
    min_value = st.number_input("Enter the minimum value (if a specific value, enter the same in both number inputs):", key=key_min)
    max_value = st.number_input("Enter the maximum value (if a specific value, enter the same in both number inputs):", key=key_max)
    min_value = int(min_value)
    max_value = int(max_value)
    return min_value, max_value, num_elements

# Function to ask for different strings - Left for implementation
def ask_for_str(argument):
    n_str = st.number_input("Enter the number of the different strings you will input:")
    n_str = math.floor(n_str)
    start = 0
    step = 1
    x = range(start,n_str,step)
    diff_strs = []
    
    for n in x:
        key_str = f"{argument}_{n}_str"
        diff_str = st.text_input(f"Enter the string number {n+1}:", key = key_str)
        diff_strs.append(diff_str)

    return diff_strs

# Function to ask for a range based on the data type
def ask_range_data_type(data_type,argument):
    if data_type == 'int':
        return ask_range_integer(argument)
    elif data_type == 'list':
        return ask_range_list(argument)
    elif data_type == 'float':
        return ask_range_float(argument)
    elif data_type == 'str':    # Left for implementation
        return ask_for_str(argument)
    elif data_type == 'bool':   # Left for implementation
        return True, False

# Function to create a JSON file
def create_json_file(file_name, data_dict):
    # Save the generated numbers to a JSON file
    with open(file_name, 'w') as file:
        json.dump(data_dict, file, indent=4)

# Function to process test cases - Group them together
def process_test_cases(input_file, output_file):
    with open(input_file, "r") as json_file:
        data = json.load(json_file)

    test_cases_data = {}
    for var_name, var_values in data.items():
        for case_num, values in var_values.items():
            case_num = int(case_num)
            var_values = json.loads(values) if isinstance(values, str) else values
            test_cases_data.setdefault(case_num, {})[var_name] = var_values

    with open(output_file, "w") as json_file:
        json.dump(test_cases_data, json_file, indent=4)

# Function to generate a random list
def generate_random_list(min_value, max_value, num_elements, argument_name, data_dict):
    min_value = int(min_value)
    max_value = int(max_value)
    num_elements = int(num_elements)
    if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
        raise ValueError("Invalid range values")
    
    # Generate the list of random numbers
    random_list = [random.randint(min_value, max_value) for i in range(num_elements)]
    data_dict.setdefault(argument_name, {}).update({str(len(data_dict[argument_name])+1): str(random_list)})
    return data_dict

# Function to generate a random integer
def generate_random_int(min_value, max_value, argument_name, data_dict):
    if not isinstance(min_value, int) or not isinstance(max_value, int):
        raise ValueError("Invalid range values")
    
    # Generate the random integer number
    random_int = random.randint(min_value, max_value)
    data_dict.setdefault(argument_name, {}).update({str(len(data_dict[argument_name])+1): str(random_int)})
    return data_dict

# Function to generate a random floating-point number
def generate_random_float(min_value, max_value, argument_name, data_dict):
    if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
        raise ValueError("Invalid range values")
    
    # Generate the random float number
    random_float = random.uniform(min_value, max_value)
    data_dict.setdefault(argument_name, {}).update({str(len(data_dict[argument_name])+1): str(random_float)})
    return data_dict

# Function to load selected data types
def load_selected_types(file_types, function_arguments):
    selected_types = {}
    
    with open(file_types, 'r') as file:
        selected_types = json.load(file)

    method_type = selected_types.get(st.session_state.main_function, {})
    random_numbers_dict = {}  # Dictionary to store generated numbers

    with st.form(key="ranges_form"):
        test_cases_number = st.number_input("Specify number of Test Cases to generate:")
        test_cases_number = int(test_cases_number)

        st.write(f"Specify data ranges for arguments of the Main Function {st.session_state.main_function}:")
        for argument in function_arguments:
            data_type = method_type.get(argument)
            st.write(f"{argument} - {data_type}")

            if data_type == 'int':
                min_value, max_value = ask_range_data_type(data_type, argument)
                for i in range(test_cases_number):
                    random_numbers_dict = generate_random_int(min_value, max_value, argument, random_numbers_dict)
            elif data_type == 'float':
                min_value, max_value = ask_range_data_type(data_type, argument)
                for i in range(test_cases_number):
                    random_numbers_dict = generate_random_float(min_value, max_value, argument, random_numbers_dict)
            elif data_type == 'list':
                min_value, max_value, num_elements = ask_range_data_type(data_type, argument)
                for i in range(test_cases_number):
                    random_numbers_dict = generate_random_list(min_value, max_value, num_elements, argument, random_numbers_dict)
            elif data_type == 'str':
                st.warning("Left for future implementation")    # Left for future implementation

        submitted = st.form_submit_button("SAVE DATA RANGES")
        if submitted:
            st.success("Test Cases Generated Successfully")

            # Create JSON file
            create_json_file('random_numbers.json', random_numbers_dict)
            process_test_cases('random_numbers.json','test_cases.json')

# Graphic User Interface
def main():
    st.set_page_config(page_title = "Data Ranges", page_icon = "🎛️")
    st.title("Defining Data Ranges")

    load_selected_types('selected_types.json',st.session_state.main_arguments)

# Execute application
if __name__ == "__main__":
    main()
