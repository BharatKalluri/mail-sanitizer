from clients.gmail_client import GmailClient
from create_mail_dump import create_mail_dump
from mail_dump_ops import MailDumpOps
import click


@click.group()
def cli():
    pass


@cli.command()
def sanitize():
    gmail_client = GmailClient()
    mail_dump_ops = MailDumpOps()
    top_senders = mail_dump_ops.get_top_senders()
    for sender in top_senders:
        emails_ids = mail_dump_ops.get_message_ids(sender)
        print(f"You have {len(emails_ids)} messages from {sender}, "
              f"do you want to delete all messages from these senders? (y/n)")
        should_del = str(input())
        if should_del[0] == 'y':
            # TODO: Get email from config
            gmail_client.del_emails_with_id(emails_ids, "kalluribharat@gmail.com")
            print(f"Deleted {len(emails_ids)} emails!")


@cli.command()
def collect():
    # Create a mail dump with everything in existence
    # TODO: Get email from config
    create_mail_dump("", "kalluribharat@gmail.com")


if __name__ == "__main__":
    cli()
