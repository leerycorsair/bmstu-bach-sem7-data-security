

def read_from_file(path: str, filename: str) -> bytes:
    file = open(path + filename, 'rb')
    data = file.read()
    file.close()
    return data


def write_to_file(data: bytes, path: str, filename: str) -> None:
    file = open(path + filename, 'wb')
    file.write(data)
    file.close()
