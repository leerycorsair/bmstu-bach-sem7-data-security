
import numpy as np


class Rotor:
    def __init__(self) -> None:
        tmp = np.arange(255, -1, -1, dtype=np.uint8)
        np.random.shuffle(tmp)
        self.values = bytes(tmp)
        self.current_pos: int = 0

    def forward(self, data: int) -> int:
        return self.values[data]

    def back(self, data: int) -> int:
        return self.values.find(data)

    def rotate(self) -> bool:
        self.values = self.values[-1:-1] + self.values
        self.current_pos = (self.current_pos + 1) % 256
        return not self.current_pos
