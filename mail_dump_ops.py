import numpy as np
import pandas as pd


class MailDumpOps:
    def __init__(self):
        # TODO: Make this mail dump in home directory
        self.df = pd.DataFrame(pd.read_pickle("mail_dump")).transpose()
        self.df['from_sender'] = np.nan
        self.df['from_sender'] = self.df.apply(MailDumpOps.get_from_sender, axis=1)
        # TODO: get un-subscribe link here

    @staticmethod
    def get_from_sender(row):
        payload = row.payload
        headers = payload.get('headers')
        filtered_from_sender = list(filter(lambda x: x['name'] == 'From', headers))
        if filtered_from_sender:
            return filtered_from_sender[0]['value']

    def get_top_senders(self):
        return list(self.df.from_sender.value_counts().index)

    def get_message_ids(self, sender: str):
        return list(self.df[self.df.from_sender == sender].id)
