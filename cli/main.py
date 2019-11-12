from cli.clients.gmail_client import GmailClient
from cli.mail_dump_ops import MailDumpOps
import click

from cli.utils import create_config_path, get_prop_from_config

create_config_path()


@click.group()
def cli():
    pass


@cli.command()
def sanitize():
    user_email = get_prop_from_config("email")
    mail_client = GmailClient()
    mail_dump_ops = MailDumpOps()
    top_senders = mail_dump_ops.get_top_senders()
    for sender in top_senders:
        emails_ids = mail_dump_ops.get_message_ids(sender)
        print(f"You have {len(emails_ids)} messages from {sender}, "
              f"do you want to delete all messages from these senders? (y/n) ", end="")
        should_del = str(input())
        if should_del and should_del[0] == 'y':
            mail_client.del_emails_with_id(emails_ids, user_email)
            print(f"Deleted {len(emails_ids)} emails!")


@cli.command()
def collect():
    # Create a mail dump with everything in existence
    gmail_client = GmailClient()
    user_email = get_prop_from_config("email")
    MailDumpOps.create_mail_dump("", user_email, gmail_client)


def main():
    cli()


if __name__ == "__main__":
    cli()
