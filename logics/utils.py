from uuid import uuid4


def get_unique():
    """
    Generate a unique string using UUID version 4.

    Returns:
        str: A unique string generated using UUID version 4.

    """
    return str(uuid4()).split("-")[-1]
