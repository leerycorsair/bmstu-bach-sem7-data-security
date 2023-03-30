class Node:
    def __init__(self, byte: int, freq: int):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other: "Node"):
        return self.freq < other.freq

    def __eq__(self, other: "Node"):
        if (other == None):
            return False
        return self.freq == other.freq