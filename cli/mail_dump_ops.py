import aiohttp
import numpy as np
import pandas as pd
import asyncio
import os
import pickle

from cli.utils import get_mail_dump_path


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


class MailDumpOps:
    def __init__(self):
        self.df = pd.DataFrame(pd.read_pickle(get_mail_dump_path())).transpose()
        self.df['from_sender'] = np.nan
        self.df['from_sender'] = self.df.apply(MailDumpOps.get_from_sender, axis=1)
        # TODO: get un-subscribe link here

    @staticmethod
    def create_mail_dump(q: str, user_id, mail_client):
        print("Getting all your emails metadata, this might take a while based on the size of your inbox. "
              "Go grab a coffee :)")
        all_messages = mail_client.get_messages_for_q(q, user_id)
        print("Getting all your emails contents")
        messages_content = asyncio.run(get_all_emails(user_id, all_messages, mail_client))
        dump_mail_data(get_mail_dump_path(), messages_content, True)
        print("Collected all emails, run sanitize to clean up your inbox!")

    @staticmethod
    def get_from_sender(row):
        payload = row.payload
        if payload and isinstance(payload, dict):
            headers = payload.get('headers')
            filtered_from_sender = list(filter(lambda x: x['name'] == 'From', headers))
            if filtered_from_sender:
                return filtered_from_sender[0]['value']

    def get_top_senders(self):
        return list(self.df.from_sender.value_counts().index)

    def get_message_ids(self, sender: str):
        return list(self.df[self.df.from_sender == sender].id)
