# Import the streamlit library, which is used to create interactive web applications
import streamlit as st

# Define a function to remove comments from the provided file content
def remove_comments(file_content):
    # Split the file content into lines
    lines = file_content.splitlines()

    # Initialize variables to track comment types and modified lines
    inside_single_line_comment = False
    inside_multiline_comment = False
    inside_block_comment = False
    modified_lines = []

    # Loop through each line in the file
    for line in lines:
        line_without_comments = ""

        i = 0
        while i < len(line):
            if inside_block_comment:
                # Check for the end of a block comment
                if line[i:i + 2] == "*/":
                    inside_block_comment = False
                    i += 2
                else:
                    i += 1
            # Check for the end of a multiline string
            elif inside_multiline_comment:
                if line[i:i + 3] == "'''" or line[i:i + 3] == '"""':
                    inside_multiline_comment = False
                    i += 3
                else:
                    i += 1
            # Check for the start of a single-line comment
            elif inside_single_line_comment:
                break
            else:
                # Check for the start of a block comment
                if line[i:i + 2] == "/*":
                    inside_block_comment = True
                    i += 2
                # Check for the start of a multiline string
                elif line[i:i + 3] == "'''" or line[i:i + 3] == '"""':
                    inside_multiline_comment = True
                    i += 3
                # Check for the start of a single-line comment
                elif line[i] == "#":
                    break
                else:
                    line_without_comments += line[i]
                    i += 1

        # Add the line without comments to the modified_lines list
        if not inside_single_line_comment and not inside_multiline_comment:
            modified_lines.append(line_without_comments)
    
    # Join the modified lines to create the file content without comments
    file_without_comments = "\n".join(modified_lines)
    
    # Split the file content without comments into lines
    lines = file_without_comments.splitlines()

    # Initialize a list to store final non-empty lines
    final_lines = []
    for line in lines:
        # Add non-empty lines to the final_lines list
        if line.strip():
            final_lines.append(line)
    
    # Join the final non-empty lines to create the modified content
    return "\n".join(final_lines)

# Define a function to process and save the modified file content
def process_and_save_file(file_content, output_file_path):
    modified_content = remove_comments(file_content)
    with open(output_file_path, 'w') as f:
        f.write(modified_content)
    return modified_content

# Define a function to change the session state when a file is uploaded
def change_file_state():
    st.session_state.file = "uploaded"

# Define the main function to create the Streamlit app
def main():
    # Customize the page configuration with a title and icon
    st.set_page_config(page_title="File", page_icon="📂")
    st.title("File Uploader")

    # Check if the "file" key exists in the session state, initialize if not
    if "file" not in st.session_state:
        st.session_state.file = "not uploaded"
    
    # Logic to read the uploaded file, process it, and provide feedback
    file = st.file_uploader("Upload your Python source code file.", on_change=change_file_state)

    if st.session_state.file == "uploaded":
        if file is not None:    
            # Read the content of the uploaded file
            file_content = file.getvalue().decode("utf-8")

            # Process the file content to remove comments and save the modified file
            modified_file_path = 'uploaded_file.py'
            clean_file = process_and_save_file(file_content, modified_file_path)

            # Store the clean file content in session state if not already stored
            if "file_content" not in st.session_state:
                st.session_state.file_content = clean_file

            # Display success message after successful upload
            st.success("You have successfully uploaded your file.")
        else:
            # Display a warning message if no file is uploaded
            st.warning("You have not uploaded your file yet.")
    else:
        # Display a warning message if the file upload state is not "uploaded"
        st.warning("You have not uploaded your file yet.")

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Call the main function to start the Streamlit application
    main()
