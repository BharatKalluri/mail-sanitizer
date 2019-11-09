from clients.gmail_client import GmailClient
from mail_dump_ops import MailDumpOps

gmail_client = GmailClient()


if __name__ == "__main__":
    # TODO: Have a proper cli tool here
    mail_dump_ops = MailDumpOps()
    top_senders = mail_dump_ops.get_top_senders()
    for sender in top_senders:
        emails_ids = mail_dump_ops.get_message_ids(sender)
        print(f"You have {len(emails_ids)} messages from {sender}, "
              f"do you want to delete all messages from these senders?")
        # TODO: Formalize this further
        should_del = str(input())
        if should_del[0] == 'y':
            print(f"Deleting {len(emails_ids)} emails")
            gmail_client.del_emails_with_id(emails_ids, "kalluribharat@gmail.com")
