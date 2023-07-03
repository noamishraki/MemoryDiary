from uuid import uuid4


def get_unique():
    return str(uuid4()).split("-")[-1]
