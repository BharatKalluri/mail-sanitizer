import os


def get_config_dir():
    home_dir = os.path.expanduser('~')
    return os.path.join(home_dir, ".config", "mail-sanitizer")


def get_mail_dump_path():
    return os.path.join(get_config_dir(), "mail_dump")


def create_config_path():
    if not os.path.exists(get_config_dir()):
        os.makedirs(get_config_dir())
