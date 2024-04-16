import streamlit as st
import yaml
import os

# Assuming your YAML content is saved in 'data.yaml' in the same directory as your script
yaml_file_path = 'data.yaml'

def load_yaml_content(filepath):
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)

def save_yaml_content(filepath, content):
    with open(filepath, 'w') as file:
        yaml.safe_dump(content, file)

def display_editor(content):
    return st.text_area("YAML Content", value=yaml.safe_dump(content), height=300)

def main():
    st.title("YAML Dashboard")

    if not os.path.exists(yaml_file_path):
        st.error(f"YAML file not found: {yaml_file_path}")
        st.stop()

    yaml_content = load_yaml_content(yaml_file_path)
    edited_content = display_editor(yaml_content)

    if st.button('Save Changes'):
        new_content = yaml.safe_load(edited_content)  # Convert edited string back to dictionary
        save_yaml_content(yaml_file_path, new_content)
        st.success("YAML content saved successfully.")

if __name__ == "__main__":
    main()
