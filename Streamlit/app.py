# import streamlit as st
# import os

# def display_file_structure(path):
#     for root, dirs, files in os.walk(path):
#         level = root.replace(path, '').count(os.sep)
#         indent = ' ' * 4 * level
#         st.write(f'{indent}{os.path.basename(root)}/')
#         sub_indent = ' ' * 4 * (level + 1)
#         for file in files:
#             st.write(f'{sub_indent}{file}')

# # Usage
# st.title("File Structure Viewer")
# root_path = st.text_input("Enter the root path:")
# if root_path:
#     display_file_structure(root_path)

import streamlit as st
import os

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
            if st.button(f"📁 {item}", key=f"dir_{full_path}"):
                st.session_state.selected_folder = os.path.join(directory, item)
                st.session_state.selected_file = None
        else:
            if st.button(f"📄 {item}", key=f"file_{full_path}"):
                st.session_state.selected_file = full_path
                st.session_state.selected_folder = directory
def display_folder_contents(folder):
    st.write(f"Contents of: {folder}")
    for item in os.listdir(folder):
        path = os.path.join(folder, item)
        if os.path.isdir(path):
            if st.button(f"📁 {item}", key=f"subdir_{path}"):
                st.session_state.selected_folder = path
                st.session_state.selected_file = path
        else:
            if st.button(f"📄 {item}", key=f"file_{path}"):
                st.session_state.selected_file = path

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)


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
        st.subheader("File Editor")
        if st.session_state.selected_file:
            file_content = read_file(st.session_state.selected_file)
            edited_content = st.text_area("Edit file content:", value=file_content, height=300)
            if st.button("Save Changes"):
                write_file(st.session_state.selected_file, edited_content)
                st.success("File saved successfully!")
        else:
            st.write("Select a file to edit")
else:
    st.error("Please enter a valid directory path")
