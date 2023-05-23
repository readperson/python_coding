import uuid


def p_uid():
    return str(uuid.uuid4()).replace("-", "").upper()


if __name__ == '__main__':
    print(p_uid())
