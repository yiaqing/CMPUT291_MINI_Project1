import re


# ********Search SQL Metadata********
def search(string):
    if re.search(r"\b(and|exec|insert|select|drop|grant|alter|delete"
                 r"|update|count|chr|mid|master|truncate|char|declare|or)\b|(\*|;|\+|'|%)", string) is not None:
        print("Injection")
        return 1
