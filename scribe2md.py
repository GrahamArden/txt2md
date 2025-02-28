# %%
"""
This script converts text files from a Kindle Scribe to markdown files.
Usage:
    python3 kindle2md.py
The script will prompt the user to select an input text file and an output markdown file using file dialogs.
Functions:
    - The script reads the content of the selected input text file.
    - It processes the content by:
        - Replacing '◦' with '- '.
        - Replacing lines containing 'concise summary of' with 'Summary'.
        - Ensuring lines starting with '-' are followed by a space.
        - Removing lines starting with '...'.
        - Removing lines starting with 'Page'.
        - Adding '### ' at the beginning of lines that do not start with '- '.
    - It prints the updated content.
    - It writes the updated content to the selected output markdown file.
Dependencies:
    - tkinter: For file dialogs to select input and output files.
    - re: For regular expression operations on the content.
Note:
    - If file selection is cancelled, the script prints a message and exits.
"""
import tkinter as tk
from tkinter import filedialog
import re

# Prompt the user to select an input text file and an output markdown file
# Hide the root window

root = tk.Tk()
root.withdraw()  # Hide the root window

input_file = filedialog.askopenfilename(title="Select the input text file", filetypes=[("Text files", "*.txt")])
output_file = filedialog.asksaveasfilename(title="Save as", defaultextension=".md", filetypes=[("Markdown files", "*.md")])

if not input_file or not output_file:
    print("File selection cancelled.")
    exit()

# Now you can use input_file and output_file for further processing
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read()




updated_content = content.replace('◦', '- ')
updated_content = re.sub(r'^.*concise summary of.*$', 'Summary', updated_content, flags=re.MULTILINE)
updated_content = re.sub(r'^-(?! )', '- ', updated_content, flags=re.MULTILINE)
updated_content = re.sub(r'^\.{3}', '', updated_content, flags=re.MULTILINE)
updated_content = re.sub(r'^Page.*', '', updated_content, flags=re.MULTILINE)
updated_content = re.sub(r'^(?!- )', '### ', updated_content, flags=re.MULTILINE)
print(updated_content)


# Write the updated content to the output file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(updated_content)



