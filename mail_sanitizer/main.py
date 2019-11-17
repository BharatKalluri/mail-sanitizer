from mail_sanitizer.clients.gmail_client import GmailClient
from mail_sanitizer.mail_dump_ops import MailDumpOps, collect_emails
import click

from mail_sanitizer.utils import create_config_path, get_prop_from_config

create_config_path()


@click.group()
def cli():
    pass


@cli.command()
def sanitize():
    collect_emails()
    user_email = get_prop_from_config("email")
    mail_client = GmailClient()
    mail_dump_ops = MailDumpOps()
    top_senders = mail_dump_ops.get_top_senders()
    for sender in top_senders:
        emails_ids = mail_dump_ops.get_message_ids(sender)
        un_sub_links = mail_dump_ops.get_un_sub_link(sender)
        print(f"You have {len(emails_ids)} messages from {sender}, Delete? (y/n) ", end="")
        should_del = str(input())
        if should_del and should_del[0] == 'y':
            mail_client.del_emails_with_id(emails_ids, user_email)
        if un_sub_links:
            print(f"Unsubscribe link: {un_sub_links}")


def main():
    cli()


if __name__ == "__main__":
    cli()
