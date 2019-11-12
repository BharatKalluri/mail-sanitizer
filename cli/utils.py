import os

import yaml


def get_config_dir():
    home_dir = os.path.expanduser('~')
    return os.path.join(home_dir, ".config", "mail-sanitizer")


def get_config_file_path():
    return os.path.join(get_config_dir(), "config.yaml")


def get_mail_dump_path():
    return os.path.join(get_config_dir(), "mail_dump")


def create_config_path():
    if not os.path.exists(get_config_dir()):
        os.makedirs(get_config_dir())


def get_prop_from_config(prop_name: str):
    config_path = get_config_file_path()
    if not os.path.exists(config_path):
        print("config.yaml is mandatory at the mail sanitizer config")
        exit(1)
    with open(config_path) as raw_config:
        config = yaml.safe_load(raw_config)
        prop_val = config.get(prop_name)
        if not prop_val:
            print(f"{prop_name} is missing from config, please add")
        return prop_val
