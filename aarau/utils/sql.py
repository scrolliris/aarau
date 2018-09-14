import re


def format_sql(q):
    s = q.replace('\n', ' ')
    s = re.sub(r'[ ]{2,}', ' ', s)
    s = s.replace('( ', '(').replace(' )', ')')
    return s
