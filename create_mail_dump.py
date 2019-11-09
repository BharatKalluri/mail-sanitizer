import asyncio
import os
import pickle

import aiohttp

from clients.gmail_client import GmailClient
from utils import get_mail_dump_path

gmail_client = GmailClient()


async def get_all_emails(messages):
    all_messages_content = {}
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        await asyncio.gather(
            *(gmail_client.store_mail_resp(msg['id'], all_messages_content, client) for msg in messages)
        )
    return all_messages_content


def dump_mail_data(file_name, obj, overwrite=False):
    if os.path.exists(file_name) and not overwrite:
        return
    dump = open(file_name, 'ab')
    pickle.dump(obj, dump)
    dump.close()


def create_mail_dump(q: str, user_id):
    print("Getting all your emails metadata")
    all_messages = gmail_client.get_messages_for_q(q, user_id)
    print("Getting all your emails contents")
    messages_content = asyncio.run(get_all_emails(all_messages))
    print("Creating a dump with the data we have now")
    dump_mail_data(get_mail_dump_path(), messages_content, True)
    print("Dump created")


# Create a mail dump with everything in existence
if __name__ == "__main__":
    create_mail_dump("", "kalluribharat@gmail.com")
