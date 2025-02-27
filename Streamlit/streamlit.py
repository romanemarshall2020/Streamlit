import streamlit as st
from streamlit_modal import Modal
import os
import ast

class FileExplorerEditor:
    def __init__(self):
        """Initialize session state variables."""
        if "current_path" not in st.session_state:
            st.session_state.current_path = os.getcwd()
        if "selected_file" not in st.session_state:
            st.session_state.selected_file = None
        if "file_content" not in st.session_state:
            st.session_state.file_content = ""
        if "unsaved_changes" not in st.session_state:
            st.session_state.unsaved_changes = False
        # IMPORTANT: Start with navigation not confirmed
        if "confirm_navigation" not in st.session_state:
            st.session_state.confirm_navigation = False
        # Flag to control modal display
        if "show_modal" not in st.session_state:
            st.session_state.show_modal = False

    def list_dir_contents(self, directory):
        """List directories and files in the given path."""
        try:
            items = sorted(os.listdir(directory))
            dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
            files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
            return dirs, files
        except Exception as e:
            st.error(f"Error accessing directory: {e}")
            return [], []

    def navigate_back(self):
        """Navigate up one directory level."""
        parent_dir = os.path.dirname(st.session_state.current_path)
        if parent_dir != st.session_state.current_path:
            st.session_state.current_path = parent_dir
            st.session_state.selected_file = None
            # Reset flags
            st.session_state.confirm_navigation = False
            st.session_state.show_modal = False
            st.rerun()

    def unsaved_changes_handle(self):
        """
        Render the modal asking if the user wants to navigate back despite unsaved changes.
        This function should be called every render if the modal flag is active.
        """
        # If the flag is set, open the modal
        # Render modal content if open


    def select_folder(self, folder_path):
        """Set the selected folder as the current path."""
        st.session_state.current_path = folder_path
        st.session_state.selected_file = None
        st.rerun()

    def select_file(self, file_path):
        """Load file content into session state."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                st.session_state.file_content = f.read()
            st.session_state.selected_file = file_path
            st.rerun()
        except Exception as e:
            st.error(f"Error reading file: {e}")

    def is_valid_python_code(self, code):
        """Check if Python code has valid syntax."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)

    def save_file(self, new_content):
        """Save file changes, with syntax validation for Python files."""
        try:
            if st.session_state.selected_file.endswith(".py"):
                is_valid, error_msg = self.is_valid_python_code(new_content)
                if not is_valid:
                    st.error(f"Syntax Error: {error_msg}")
                    return

            with open(st.session_state.selected_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            st.session_state.unsaved_changes = False
            st.success("File saved successfully!")

        except Exception as e:
            st.error(f"Error saving file: {e}")

    def render(self):
        """Render the Streamlit UI."""
        st.title("📂 File Explorer with Editor")

        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader("📁 File Explorer")

            # Navigate up button
            if os.path.dirname(st.session_state.current_path) != st.session_state.current_path:
                if st.button("🔙 Go Back"):
                    # If there are unsaved changes, set the flag to show modal
                    if st.session_state.unsaved_changes:
                        modal = Modal("Confirm Navigation", key="modal_key")
                        if st.button("Modal"):
                            modal.open()
                            st.session_state.show_modal = True

                        if st.session_state.show_modal:
                            with modal.container():
                                st.warning(
                                    "You have unsaved changes to the current file, are you sure you want to go back without saving?")
                                col1, col2 = st.columns(2)
                                with col1:
                                    if st.button("Yes, Go Back"):
                                        st.warning("Please save or revert your changes.")
                                        st.session_state.confirm_navigation = True  # Reset confirmation
                                        st.session_state.show_modal = False
                                        modal.close()
                                with col2:
                                    if st.button("Cancel"):
                                        st.session_state.confirm_navigation = False  # Cancel confirmation
                                        st.session_state.show_modal = False
                                        modal.close()

                    else:
                        self.navigate_back()

                    # If the modal flag is active, render the modal (it will block further actions until resolved)
                    if st.session_state.confirm_navigation:
                        self.unsaved_changes_handle()
                        # Do not process further until modal decision is made
                        return

            # Display current directory
            st.write(f"**Current Directory:** `{st.session_state.current_path}`")

            # List directory contents
            dirs, files = self.list_dir_contents(st.session_state.current_path)

            # Display folders as buttons
            for folder in dirs:
                folder_path = os.path.join(st.session_state.current_path, folder)
                if st.button(f"📂 {folder}", key=f"folder_{folder_path}"):
                    self.select_folder(folder_path)

            # Display files as buttons
            for file in files:
                file_path = os.path.join(st.session_state.current_path, file)
                if st.button(f"📄 {file}", key=f"file_{file_path}"):
                    self.select_file(file_path)

        with col2:
            st.subheader("📝 File Editor")

            if st.session_state.selected_file:
                st.write(f"**Editing:** `{st.session_state.selected_file}`")
                new_content = st.text_area("Edit file:", st.session_state.file_content, height=400)

                if new_content != st.session_state.file_content:
                    st.session_state.unsaved_changes = True
                else:
                    st.session_state.unsaved_changes = False

                if st.button("💾 Save Changes"):
                    self.save_file(new_content)
            else:
                st.info("Select a file to edit.")

# Run the app
if __name__ == "__main__":
    app = FileExplorerEditor()
    app.render()