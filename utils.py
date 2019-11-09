import os


def get_config_dir():
    home_dir = os.path.expanduser('~')
    return os.path.join(home_dir, ".mail_sanitizer")


def get_mail_dump_path():
    return os.path.join(get_config_dir(), "mail_dump")
