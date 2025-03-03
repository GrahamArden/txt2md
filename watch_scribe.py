#!/usr/bin/env python3
"""
watch_scribe.py

This script watches a specified folder for new `.txt` files and converts them to `.md` files
using a specified script. The converted files are saved in an output folder.

It also queries an email address, downloads the emails, looks for a link in the email that says
'Download text file', and then downloads the linked file to the folder 'Scribe'.

Usage:
    python watch_scribe.py
"""

import os
import time
import subprocess
import imaplib
import email
from email.header import decode_header
import requests

def download_emails(imap_server, email_user, email_pass, folder_to_save):
    """
    Downloads emails and looks for a link that says 'Download text file', then downloads the linked file.

    Args:
        imap_server (str): The IMAP server address.
        email_user (str): The email address to query.
        email_pass (str): The password for the email address.
        folder_to_save (str): The folder to save the downloaded files.
    """
    # Connect to the server
    mail = imaplib.IMAP4_SSL(imap_server)
    # Login to the account
    mail.login(email_user, email_pass)
    # Select the mailbox you want to check
    mail.select("inbox")

    # Search for all emails
    status, messages = mail.search(None, "ALL")
    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email
                msg = email.message_from_bytes(response_part[1])
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                # Check if the email has the link
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True).decode()
                            if 'Download text file' in body:
                                # Extract the link
                                start = body.find('href="') + len('href="')
                                end = body.find('"', start)
                                link = body[start:end]
                                # Download the file
                                response = requests.get(link)
                                filename = os.path.join(folder_to_save, time.strftime("%Y%m%d-%H%M%S") + ".txt")
                                with open(filename, "wb") as f:
                                    f.write(response.content)
    # Logout and close the connection
    mail.logout()

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
    # Email configuration
    IMAP_SERVER = 'imap.example.com'
    EMAIL_USER = 'your_email@example.com'
    EMAIL_PASS = 'your_password'
    
    # Download emails and save the files to 'Scribe' folder
    download_emails(IMAP_SERVER, EMAIL_USER, EMAIL_PASS, 'Scribe')
    
    # Watch the 'Scribe' folder, run 'scribe2md.py', and save output to 'Markdown' folder
    watch_folder('Scribe', 'scribe2md.py', 'Markdown')