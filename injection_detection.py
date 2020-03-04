import re


# ********Search SQL Metadata********
def name_check(content):
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def pwd_check(content):
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def email_check(content):
    return re.fullmatch(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', content)
