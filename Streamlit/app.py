import streamlit as st
import os

def display_file_structure(path):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * level
        st.write(f'{indent}{os.path.basename(root)}/')
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            st.write(f'{sub_indent}{file}')

# Usage
st.title("File Structure Viewer")
root_path = st.text_input("Enter the root path:")
if root_path:
    display_file_structure(root_path)