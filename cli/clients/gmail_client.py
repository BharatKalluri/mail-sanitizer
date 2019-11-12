import json
import os
import pickle

import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from cli.utils import get_config_dir

SCOPES = ['https://mail.google.com/']


class GmailClient:

    def __init__(self):
        self.token = None
        self.get_token()

    def get_token(self):
        creds = None
        token_pickle_path = os.path.join(get_config_dir(), 'token.pickle')
        creds_path = os.path.join(get_config_dir(), 'credentials.json')
        if not os.path.exists(creds_path):
            print("Please download your credentials.json and put it in the config folder")
            exit(1)
        if os.path.exists(token_pickle_path):
            with open(token_pickle_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_pickle_path, 'wb') as token:
                    pickle.dump(creds, token)
        self.token = creds.token

    def get_headers(self):
        return {
            'Authorization': 'Bearer {}'.format(self.token),
            'Accept': "application/json",
            'Content-Type': "application/json",
        }

    def get_messages_for_q(self, q, user_id):
        r = requests.get(
            f"https://www.googleapis.com/gmail/v1/users/{user_id}/messages",
            headers=self.get_headers(),
            params={"q": q}
        )
        response = r.json()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            r = requests.get(
                f"https://www.googleapis.com/gmail/v1/users/{user_id}/messages",
                headers=self.get_headers(),
                params={"pageToken": page_token}
            )
            response = r.json()
            messages.extend(response['messages'])
        return messages

    async def store_mail_resp(self, user_id, msg_id, map_to_store_in, client):
        g_url = f"https://www.googleapis.com/gmail/v1/users/{user_id}/messages/{msg_id}"
        async with client.get(g_url, headers=self.get_headers()) as response:
            response = await response.read()
            map_to_store_in[msg_id] = json.loads(response)

    def del_emails_with_id(self, msg_ids, user_id):
        msg_ids_str = ",".join(["\"" + mid + "\"" for mid in msg_ids])
        batch_del_url = f"https://www.googleapis.com/gmail/v1/users/" + user_id + "/messages/batchDelete"
        payload = "{\"ids\": [" + msg_ids_str + "]}"
        resp = requests.request("POST", batch_del_url, data=payload, headers=self.get_headers())
        if not resp.ok:
            print(resp.text)
            raise Exception("Deletion has failed")
