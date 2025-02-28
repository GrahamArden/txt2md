import os
import time
import subprocess

def watch_folder(folder_to_watch, script_to_run, output_folder):
    already_seen = set(os.listdir(folder_to_watch))
    
    while True:
        time.sleep(1)
        current_files = set(os.listdir(folder_to_watch))
        new_files = current_files - already_seen
        
        for file in new_files:
            if file.endswith('.txt'):
                input_path = os.path.join(folder_to_watch, file)
                output_path = os.path.join(output_folder, file.replace('.txt', '.md'))
                subprocess.run(['python', script_to_run, input_path, output_path])
        
        already_seen = current_files

if __name__ == "__main__":
    watch_folder('Scribe', 'scribe2md.py', 'Markdown')