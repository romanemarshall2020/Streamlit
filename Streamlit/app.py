import streamlit as st
import os
from PIL import Image

def get_directory_structure(directory):
    structure = {}
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            structure[item] = "directory"
        else:
            structure[item] = "file"
    return structure

def display_directory(directory, current_path=""):
    structure = get_directory_structure(directory)
    for item, item_type in structure.items():
        full_path = os.path.join(current_path, item)
        if item_type == "directory":
            # with st.expander(f"📁 {item}", expanded=True):
            if st.button(f"{item}", key=f"dir_{full_path}"):
                st.session_state.selected_folder = os.path.join(directory, item)
                st.session_state.selected_file = full_path
        elif item_type == "file":
            
        else:
            if st.button(f"📄 {item}", key=f"file_{full_path}"):
                st.session_state.selected_file = full_path
                st.session_state.selected_folder = directory

def display_folder_contents(folder):
    st.write(f"Contents of: {folder}")
    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isdir(path):
            with st.expander(f"📁 {item}", expanded=False):
                if st.button(f"Open {item}", key=f"subdir_{path}"):
                    st.session_state.selected_folder = path
                    st.session_state.selected_file = path
        else:
            if st.button(f"📄 {item}", key=f"file_{path}"):
                st.session_state.selected_file = path

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            return file.read()
    except UnicodeDecodeError:
        # In case of an error, try another common encoding (ISO-8859-1)
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            return file.read()


def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def preview_file(file_path):
    """Try to preview the file depending on its type."""
    try:
        if file_path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            # Image file
            img = Image.open(file_path)
            st.image(img, caption="Image Preview", use_column_width=True)
        elif file_path.endswith('.pdf'):
            # PDF preview could be added, but for now, let’s notify the user
            st.write("PDF Preview not supported yet.")
        elif file_path.endswith('.txt'):
            # Show the file content for text files
            file_content = read_file(file_path)
            st.text_area("Text File Content", value=file_content, height=300)
        else:
            st.write(f"Cannot preview file type: {file_path}")
    except Exception as e:
        st.error(f"Error previewing file: {e}")

st.title("Interactive Directory Explorer with File Editor")

# Initialize session state variables
if 'root_directory' not in st.session_state:
    st.session_state.root_directory = ""
if 'selected_folder' not in st.session_state:
    st.session_state.selected_folder = ""
if 'selected_file' not in st.session_state:
    st.session_state.selected_file = None

root_directory = st.text_input("Enter root directory path:", value=st.session_state.root_directory)

if root_directory and os.path.isdir(root_directory):
    st.session_state.root_directory = root_directory
    
    # Create three columns
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.subheader("Directory Structure")
        display_directory(root_directory)
    
    with col2:
        st.subheader("Folder Contents")
        if st.session_state.selected_folder:
            display_folder_contents(st.session_state.selected_folder)
        else:
            st.write("Select a folder to view its contents")
    
    with col3:
        st.subheader("File Editor / Preview")
        if st.session_state.selected_file:
            # Preview or Edit file
            preview_file(st.session_state.selected_file)
            if st.button("Edit File"):
                file_content = read_file(st.session_state.selected_file)
                edited_content = st.text_area("Edit file content:", value=file_content, height=300)
                if st.button("Save Changes"):
                    write_file(st.session_state.selected_file, edited_content)
                    st.success("File saved successfully!")
        else:
            st.write("Select a file to preview or edit")
else:
    st.error("Please enter a valid directory path")


# TODO i must figure out the issue with file not opening if its the first thing selected when app runs