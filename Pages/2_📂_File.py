import streamlit as st

def remove_comments(file_content):
    lines = file_content.splitlines()

    inside_single_line_comment = False
    inside_multiline_comment = False
    inside_block_comment = False
    modified_lines = []

    for line in lines:
        line_without_comments = ""

        i = 0
        while i < len(line):
            if inside_block_comment:
                if line[i:i + 2] == "*/":
                    inside_block_comment = False
                    i += 2
                else:
                    i += 1
            elif inside_multiline_comment:
                if line[i:i + 3] == "'''" or line[i:i + 3] == '"""':
                    inside_multiline_comment = False
                    i += 3
                else:
                    i += 1
            elif inside_single_line_comment:
                break
            else:
                if line[i:i + 2] == "/*":
                    inside_block_comment = True
                    i += 2
                elif line[i:i + 3] == "'''" or line[i:i + 3] == '"""':
                    inside_multiline_comment = True
                    i += 3
                elif line[i] == "#":
                    break
                else:
                    line_without_comments += line[i]
                    i += 1

        if not inside_single_line_comment and not inside_multiline_comment:
            modified_lines.append(line_without_comments)
    
    file_without_comments = "\n".join(modified_lines)
    lines = file_without_comments.splitlines()

    final_lines = []
    for line in lines:
        if line.strip():
            final_lines.append(line)
    
    return "\n".join(final_lines)

def process_and_save_file(file_content, output_file_path):
    modified_content = remove_comments(file_content)
    with open(output_file_path, 'w') as f:
        f.write(modified_content)
    return modified_content

def change_file_state():
    st.session_state.file = "uploaded"

# Graphic User Interface
def main():
    st.set_page_config(page_title = "File", page_icon = "📂")
    st.title("File Uploader")

    if "file" not in st.session_state:
        st.session_state.file = "not uploaded"
    
    # Lógica para leer el archivo fuente y procesarlo
    file = st.file_uploader("Upload your Python source code file.", on_change = change_file_state)

    if st.session_state.file == "uploaded":
        if file is not None:    
            # Leer el contenido del archivo
            file_content = file.getvalue().decode("utf-8")

            # Eliminar comentarios y guardar el archivo modificado
            modified_file_path = 'uploaded_file.py'
            clean_file = process_and_save_file(file_content, modified_file_path)

            if "file_content" not in st.session_state:
                st.session_state.file_content = clean_file

            st.success("You have successfully uploaded your file.")
        else:
            st.warning("You have not uploaded your file yet.")
    else:
        st.warning("You have not uploaded your file yet.")

# Execute application
if __name__ == "__main__":
    main()
