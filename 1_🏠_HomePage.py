# Import the streamlit library, which is used to create interactive web applications
import streamlit as st

# Define the main function that sets up the Streamlit app's page configuration and content
def main():
    # Customize the page configuration with a title and icon
    st.set_page_config(page_title = "Graph Generator and Line Coverage App", page_icon = "💻")

    # Create a title and introductory message on the main page
    st.title("Main Menu")
    st.write("Select a page from the sidebar")

# Check if the script is being run as the main program
if __name__ == "__main__":
    # Call the main function to start the Streamlit application
    main()
