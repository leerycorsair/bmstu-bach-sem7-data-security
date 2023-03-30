

def read_from_file(path: str, filename: str) -> list[int]:
    file = open(path + filename, 'rb')
    byte_array = []
    while True:
        byte = file.read(1)
        if byte == b"":
            break
        byte_array.append(int.from_bytes(byte, byteorder="big", signed=False))
    file.close()
    return byte_array


def write_to_file(data: list[int], path: str, filename: str) -> None:
    file = open(path + filename, 'wb')
    for byte in data:
        file.write(byte.to_bytes(1, byteorder='big', signed=False))
    file.close()
