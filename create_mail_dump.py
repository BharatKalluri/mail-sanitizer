import asyncio
import json
import os
import pickle

import aiohttp
import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://mail.google.com/']


def get_token():
    creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
    return creds.token


TOKEN = get_token()
AUTH_HEADERS = {'Authorization': 'Bearer %s' % TOKEN}


def get_messages_for_q(query):
    r = requests.get(
        "https://www.googleapis.com/gmail/v1/users/kalluribharat@gmail.com/messages",
        headers=AUTH_HEADERS,
        params={"q": query}
    )
    response = r.json()
    messages = []
    if 'messages' in response:
        messages.extend(response['messages'])

    while 'nextPageToken' in response:
        page_token = response['nextPageToken']
        r = requests.get(
            f"https://www.googleapis.com/gmail/v1/users/kalluribharat@gmail.com/messages",
            headers=AUTH_HEADERS,
            params={"pageToken": page_token}
        )
        response = r.json()
        messages.extend(response['messages'])

    return messages


async def store_mail_resp(msg_id, map_to_store_in, client):
    g_url = f"https://www.googleapis.com/gmail/v1/users/kalluribharat@gmail.com/messages/{msg_id}"
    async with client.get(g_url, headers=AUTH_HEADERS) as response:
        response = await response.read()
        map_to_store_in[msg_id] = json.loads(response)


async def get_all_emails(messages):
    all_messages_content = {}
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        print("Getting email")
        await asyncio.gather(
            *(store_mail_resp(msg['id'], all_messages_content, client) for msg in messages)
        )
    return all_messages_content


def dump_mail_data(file_name, obj, overwrite=False):
    if os.path.exists(file_name) and not overwrite:
        return
    dump = open(file_name, 'ab')
    pickle.dump(obj, dump)
    dump.close()


def create_mail_dump(q: str):
    all_messages = get_messages_for_q(q)
    messages_content = asyncio.run(get_all_emails(all_messages))
    dump_mail_data('mail_dump', messages_content, True)
    print("Dump created")


# Create a mail dump with everything in existence
create_mail_dump("")
