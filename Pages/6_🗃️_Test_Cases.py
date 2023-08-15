import streamlit as st
import json
import re
import csv
from staticfg import CFGBuilder

# Function to generate and display the General CFG of the entire program
def generate_cfg_general(file_name):
    cfg = CFGBuilder().build_from_file(file_name, file_name)
    cfg.build_visual('source_CFG', 'png')

def add_line_counts(file_content):
    lines = file_content.splitlines()
    modified_lines = []
    line_count = 1

    for line in lines:
        if line.strip().startswith("def"):
            modified_lines.append(line)
            modified_lines.append(f"    global line_count")
            modified_lines.append(f"    line_count = {line_count}")
            modified_lines.append(f"    path_list.append(line_count)")
            line_count += 1
        elif line.strip() and re.match(r'^\s+', line):
            tabs = re.match(r'^\s+', line).group()  # Obtener los tabs iniciales de la línea
            num_spaces = len(tabs) * 4  # Calcular la cantidad de espacios equivalentes a los tabs
            spaces = " " * num_spaces  # Crear la cadena de espacios
            if line.strip().startswith("return") or line.strip().startswith("break") or line.strip().startswith("continue") or line.strip().startswith("pass") or line.strip().startswith("yield"):
                modified_lines.append(f"{spaces}line_count = {line_count}")
                modified_lines.append(f"{spaces}path_list.append(line_count)")
                modified_lines.append(f"{spaces}{line.strip()}")
                line_count += 1
            elif line.strip().startswith("if") or line.strip().startswith("elif") or line.strip().startswith("else") or line.strip().startswith("for") or line.strip().startswith("while"):
                modified_lines.append(f"{spaces}{line.strip()}")
                modified_lines.append(f"{spaces}    line_count = {line_count}")
                modified_lines.append(f"{spaces}    path_list.append(line_count)")
                line_count += 1
            else:
                modified_lines.append(f"{spaces}{line.strip()}")
                modified_lines.append(f"{spaces}line_count = {line_count}")
                modified_lines.append(f"{spaces}path_list.append(line_count)")
                line_count += 1
        else:
            modified_lines.append(line)

    return "\n".join(modified_lines), line_count

def numbers_file(file):
    lines = file.splitlines()
    line_count = 1
    numbered_lines = []

    for line in lines:
        if line.strip().startswith("def"):
            numbered_lines.append(line)
            numbered_lines.append(f"    {line_count}")
            line_count += 1
        elif line.strip() and re.match(r'^\s+', line):
            tabs = re.match(r'^\s+', line).group()  # Obtener los tabs iniciales de la línea
            num_spaces = len(tabs) * 4  # Calcular la cantidad de espacios equivalentes a los tabs
            spaces = " " * num_spaces  # Crear la cadena de espacios
            if line.strip().startswith("return") or line.strip().startswith("break") or line.strip().startswith("continue") or line.strip().startswith("pass"):
                numbered_lines.append(f"{spaces}{line_count}")
                numbered_lines.append(f"{spaces}{line.strip()}")
                line_count += 1
            elif line.strip().startswith("if") or line.strip().startswith("elif") or line.strip().startswith("else") or line.strip().startswith("for") or line.strip().startswith("while"):
                numbered_lines.append(f"{spaces}{line.strip()}")
                numbered_lines.append(f"{spaces}    {line_count}")
                line_count += 1
            else:
                numbered_lines.append(f"{spaces}{line.strip()}")
                numbered_lines.append(f"{spaces}{line_count}")
                line_count += 1
        else:
            numbered_lines.append(line)

    return "\n".join(numbered_lines)

def generate_test_calls(main_function_name, test_cases):
    calls = []
    for test_case_data in test_cases.values():
        args = ", ".join(json.dumps(arg) for arg in test_case_data.values() if arg != "result")
        call = f"{main_function_name}({args})"
        calls.append(call)
    return calls

def write_test_calls_to_file(file_name, calls):
    delimeter = f'''"//"'''

    with open(file_name, 'a') as file:
        file.write('\n# Test Calls\n')
        for i, call in enumerate(calls, 1):
            variable_name = f'x_{i}'
            file.write(f"{variable_name} = {call}\n")
            file.write(f"path_list.append({delimeter})\n")

def generate_save_results(calls):
    num_calls = len(calls)

    json_start = f'''
import json
results = {{
'''

    save_results = ""

    for i in range(1, num_calls + 1):
        variable_name = f'x_{i}'
        save_results += f'    "{variable_name}": {variable_name},\n'
    
    json_end = f'''
}}
# Escribir los resultados en un archivo JSON
with open("test_results.json", "w") as json_file:
    json.dump(results, json_file, indent=4)

# Escribir los paths de ejecucion en un archivo JSON
test_cases = []
current_test = []
for num in path_list:
    if num == "//":
        if current_test:
            test_cases.append(current_test)
        current_test = []
    else:
        current_test.append(num)

if current_test:
    test_cases.append(current_test)

with open('testcases_paths.json', 'w') as file:
    json.dump(test_cases, file)
'''

    save_results = json_start + save_results + json_end

    return save_results

def line_coverage(json_file_path, total_lines):
    with open(json_file_path) as json_file:
        data = json.load(json_file)

    coverages = []

    for testcase_path in data:
        unique_paths = set(testcase_path)
        coverage = (len(unique_paths) / (total_lines-1)) * 100
        coverages.append(coverage)

    with open('line_coverages.json', 'w') as output_file:
        json.dump(coverages, output_file, indent=4)

def combine_and_save_to_csv(test_cases_file, results_file, paths_file, coverage_file):
    with open(test_cases_file) as test_cases_json_file:
        test_cases_data = json.load(test_cases_json_file)

    with open(results_file) as results_json_file:
        results_data = json.load(results_json_file)

    with open(paths_file) as paths_json_file:
        paths_data = json.load(paths_json_file)

    with open(coverage_file) as coverage_json_file:
        coverage_data = json.load(coverage_json_file)

    with open('TestCases_Report.csv', mode='w', newline='') as csv_file:
        fieldnames = ['Test Case', 'Test Data', 'Result', 'Path', 'Coverage %']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        for test_case_key, test_case_data in test_cases_data.items():
            result_key = f'x_{test_case_key}'
            result = results_data.get(result_key, [])
            path = paths_data[int(test_case_key) - 1]  # Convertir la clave a entero y restar 1 para obtener el índice correcto en la lista
            coverage = coverage_data[int(test_case_key) - 1] if int(test_case_key) - 1 < len(coverage_data) else 0.0

            writer.writerow({
                'Test Case': test_case_key,
                'Test Data': test_case_data,
                'Result': result,
                'Path': path,
                'Coverage %': "{:.2f}%".format(coverage)
            })

# Graphic User Interface
def main():
    st.set_page_config(page_title="Test Cases Analysis", page_icon="🗃️")
    st.title("Execution and Analysis of Test Cases")

    with open("test_cases.json", "r") as test_cases_file:
        test_cases = json.load(test_cases_file)

    main_function_name = st.session_state.main_function
    calls = generate_test_calls(main_function_name, test_cases)
    
    numbered_file, total_lines = add_line_counts(st.session_state.file_content)
    with open('uploaded_file.py', 'w') as file:
        file.seek(0)
        file.write("path_list = []\n")
        file.write("line_count = 1\n")
        file.write(numbered_file)
        file.close()

    file_with_numbers = numbers_file(st.session_state.file_content)

    with open('numbers_graph.py', 'w') as n_file:
        n_file.write(file_with_numbers)
        n_file.close()

    # Execute the test cases and save the results
    if st.button("Execute Test Cases"):
        write_test_calls_to_file('uploaded_file.py',calls)

        # Generar el contenido de save_results con el número correcto de x_s
        save_results = generate_save_results(calls)

        # Agregar el contenido al archivo fuente
        with open('uploaded_file.py', 'a') as file:
            file.write(save_results)

        # Ejecutar el archivo fuente para obtener los resultados
        exec(open('uploaded_file.py').read(), globals())

        line_coverage('testcases_paths.json',total_lines)

        generate_cfg_general('numbers_graph.py')

        st.success("Test Cases have been successfully executed.")

        combine_and_save_to_csv('test_cases.json', 'test_results.json', 'testcases_paths.json', 'line_coverages.json')

# Execute application
if __name__ == "__main__":
    main()
