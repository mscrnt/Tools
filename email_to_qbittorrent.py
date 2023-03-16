import base64
import re
import time
import qbittorrentapi
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery
from imapclient import IMAPClient
import os
import json
import pickle
from imapclient import IMAPClient, SEEN


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8090)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    with open('qb_credentials.json', 'r') as f:
        qb_credentials = json.load(f)

    return creds, qb_credentials


def process_emails():
    creds, qb_credentials = get_credentials()

    # Update these with your qBittorrent credentials and address
    qb_username = qb_credentials["qb_username"]
    qb_password = qb_credentials["qb_password"]
    qb_address = qb_credentials["qb_address"]

    gmail = googleapiclient.discovery.build('gmail', 'v1', credentials=creds)
    with IMAPClient("imap.gmail.com", use_uid=True, ssl=True) as client:
        client.login(qb_credentials["email"], qb_credentials["app_password"])
        client.select_folder("INBOX")

        # Search for emails marked as unseen
        messages = client.search(["UNSEEN"])
        for msg_id in messages:
            msg_data = client.fetch([msg_id], ["BODY[TEXT]"])
            msg_body = msg_data[msg_id][b"BODY[TEXT]"]
            magnet_links = re.findall(r'magnet:\?xt=urn:btih:[a-zA-Z0-9]+', msg_body.decode('utf-8'))
            for magnet_link in magnet_links:
                add_torrent(magnet_link, qb_username, qb_password, qb_address)  # Pass the qBittorrent credentials and address to the add_torrent function

            # Mark the email as read
            client.add_flags(msg_id, r'\Seen')


def add_torrent(magnet_link, qb_username, qb_password, qb_address):
    qbt_client = qbittorrentapi.Client(host=qb_address, username=qb_username, password=qb_password)

    try:
        qbt_client.auth_log_in()
        qbt_client.torrents_add(urls=magnet_link)
        print(f"Torrent added successfully: {magnet_link}")

    except qbittorrentapi.exceptions.LoginFailed as e:
        print(f"Failed to log in to qBittorrent Web API: {e}")

if __name__ == '__main__':
    print("Starting email_to_qbittorrent script...")
    while True:
        process_emails()
        time.sleep(60)  # Wait for 60 seconds before checking for new emails again
