from mail_sanitizer.clients.gmail_client import GmailClient
from mail_sanitizer.mail_dump_ops import MailDumpOps
import click

from mail_sanitizer.utils import create_config_path, get_prop_from_config

create_config_path()


@click.group()
def cli():
    pass


@cli.command()
def sanitize():
    if not MailDumpOps.does_dump_exist():
        print("Please run mail-sanitizer collect before you run sanitize")
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
            print(f"Deleted {len(emails_ids)} emails!")
        # TODO: Better format mail_sanitizer and educate people about how mailto for un sub works
        if un_sub_links:
            print(f"Unsubscribe links: {un_sub_links}")


@cli.command()
def collect():
    if MailDumpOps.does_dump_exist():
        print("Mails are already collected, do you want to overwrite? (y/n)")
        decision = str(input())
        if decision and decision.lower()[0] == 'n':
            exit(0)
    # Create a mail dump with everything in existence
    gmail_client = GmailClient()
    user_email = get_prop_from_config("email")
    print("Getting all your emails metadata, this might take a while based on the size of your inbox. "
          "Go grab a coffee :)")
    MailDumpOps.create_mail_dump("", user_email, gmail_client)
    print("Collected all emails, run sanitize to clean up your inbox!")


def main():
    cli()


if __name__ == "__main__":
    cli()
