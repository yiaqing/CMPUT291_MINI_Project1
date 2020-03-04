import re


# ********Search SQL Metadata********
def name_check(content):
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def pwd_check(content):
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def email_check(content):
    return re.fullmatch(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', content)


# ********General Chcek********
def search(string):
    if re.search(r"\b(and|exec|insert|select|drop|grant|alter|delete"
                 r"|update|count|chr|mid|master|truncate|char|declare|or)\b|(\*|;|\+|'|%)", string) is not None:
        return 1
