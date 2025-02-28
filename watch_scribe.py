#!/usr/bin/env python3
"""
watch_scribe.py

This script watches a specified folder for new `.txt` files and converts them to `.md` files
using a specified script. The converted files are saved in an output folder.

Usage:
    python watch_scribe.py
"""

import os
import time
import subprocess

def watch_folder(folder_to_watch, script_to_run, output_folder):
    """
    Watches a folder for new .txt files and runs a script to convert them to .md files.

    Args:
        folder_to_watch (str): The folder to watch for new .txt files.
        script_to_run (str): The script to run for converting .txt files to .md files.
        output_folder (str): The folder to save the converted .md files.
    """
    # Keep track of files that have already been seen
    already_seen = set(os.listdir(folder_to_watch))
    
    while True:
        # Wait for 1 second before checking the folder again
        time.sleep(1)
        # Get the current list of files in the folder
        current_files = set(os.listdir(folder_to_watch))
        # Determine the new files that have been added
        new_files = current_files - already_seen
        
        for file in new_files:
            if file.endswith('.txt'):
                input_path = os.path.join(folder_to_watch, file)
                output_path = os.path.join(output_folder, file.replace('.txt', '.md'))
                # Run the script to convert the .txt file to a .md file
                subprocess.run(['python', script_to_run, input_path, output_path])
        
        # Update the set of already seen files
        already_seen = current_files

if __name__ == "__main__":
    # Watch the 'Scribe' folder, run 'scribe2md.py', and save output to 'Markdown' folder
    watch_folder('Scribe', 'scribe2md.py', 'Markdown')