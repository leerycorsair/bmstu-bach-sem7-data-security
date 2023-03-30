
import numpy as np


class Reflector:
    def __init__(self) -> None:
        self.values: bytes = bytes(np.arange(255, -1, -1, dtype=np.uint8))

    def reflect(self, data: int) -> int:
        return self.values[data]
