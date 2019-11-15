from typing import Optional

import aiohttp
import numpy as np
import pandas as pd
import asyncio
import os
import pickle

from mail_sanitizer.clients.gmail_client import GmailClient
from mail_sanitizer.utils import get_mail_dump_path, get_prop_from_config


def set_flatten(arr):
    flat_list = set()
    for sublist in arr:
        if sublist:
            for item in sublist:
                flat_list.add(item)
    return list(flat_list)


async def get_all_emails(user_id, messages, mail_client):
    all_messages_content = {}
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        await asyncio.gather(
            *(mail_client.store_mail_resp(user_id, msg['id'], all_messages_content, client) for msg in messages)
        )
    return all_messages_content


def dump_mail_data(file_name, obj, overwrite=False):
    if os.path.exists(file_name) and not overwrite:
        return
    dump = open(file_name, 'ab')
    pickle.dump(obj, dump)
    dump.close()


def _sanitize_un_sub_link(link):
    return str(link).strip().replace("\u003c", "").replace("\u003e", "")


def collect_emails():
    # Create a mail dump with everything in existence
    gmail_client = GmailClient()
    user_email = get_prop_from_config("email")
    print("Getting all your emails metadata")
    MailDumpOps.create_mail_dump("", user_email, gmail_client)


class MailDumpOps:
    def __init__(self):
        self.df = pd.DataFrame(pd.read_pickle(get_mail_dump_path())).transpose()
        self.df['from_sender'] = np.nan
        self.df['from_sender'] = self.df.apply(MailDumpOps.get_from_sender, axis=1)
        self.df['un_subscribe_links'] = self.df.apply(MailDumpOps.get_unsubscribe_links, axis=1)

    @staticmethod
    def does_dump_exist() -> bool:
        return os.path.exists(get_mail_dump_path())

    @staticmethod
    def create_mail_dump(q: str, user_id: str, mail_client):
        all_messages = mail_client.get_messages_for_q(q, user_id)
        print("Getting all your emails contents")
        messages_content = asyncio.run(get_all_emails(user_id, all_messages, mail_client))
        dump_mail_data(get_mail_dump_path(), messages_content, True)

    @staticmethod
    def get_from_sender(row) -> str:
        return MailDumpOps.get_header_val(row, 'From')

    @staticmethod
    def get_unsubscribe_links(row) -> Optional[list]:
        unsubscribe_links_raw = MailDumpOps.get_header_val(row, 'List-Unsubscribe')
        if unsubscribe_links_raw:
            unsubscribe_links = [_sanitize_un_sub_link(link) for link in unsubscribe_links_raw.split(",")]
            return unsubscribe_links

    @staticmethod
    def get_header_val(row, header_key: str):
        payload = row.payload
        if payload and isinstance(payload, dict):
            headers = payload.get('headers')
            filtered_from_sender = list(filter(lambda x: x['name'] == header_key, headers))
            if filtered_from_sender:
                return filtered_from_sender[0]['value']

    def get_top_senders(self) -> list:
        return list(self.df.from_sender.value_counts().index)

    def get_message_ids(self, sender: str) -> list:
        return list(self.df[self.df.from_sender == sender].id)

    def get_un_sub_link(self, sender: str) -> str:
        un_sub_links = set_flatten(list(self.df[self.df.from_sender == sender]['un_subscribe_links']))
        if un_sub_links:
            # TODO: Think what to do with mailto links
            filtered_un_sub_links = list(filter(lambda x: ((x is not None) and ('mailto' not in x)), un_sub_links))
            if filtered_un_sub_links and any(filtered_un_sub_links):
                return filtered_un_sub_links[0]
