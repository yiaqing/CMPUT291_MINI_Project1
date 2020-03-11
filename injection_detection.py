import re


# ********Search SQL Metadata********
def name_check(content):
    # Match user name to check if any illegal characters exists
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def pwd_check(content):
    # Match password to check if any illegal characters exists
    return re.fullmatch(r'^[A-Za-z0-9_]*$', content)


def email_check(content):
    # Match email to check if any illegal characters exists
    return re.fullmatch(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', content)


# ********General Check********
def search(string):
    # Search any SQL meta word
    # if exists, there is a SQL injection attempt
    if re.search(r"\b(and|exec|insert|select|drop|grant|alter|delete"
                 r"|update|count|chr|mid|master|truncate|char|declare|or)\b|(\*|;|\+|'|%)", string) is not None:
        return 1
