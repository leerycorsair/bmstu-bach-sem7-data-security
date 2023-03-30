
from .rotor import Rotor
from .reflector import Reflector

ROTORS_AMOUNT: int = 3


class Enigma():
    def __init__(self) -> None:
        self.rotors: list[Rotor] = [Rotor() for _ in range(ROTORS_AMOUNT)]
        self.reflector = Reflector()

    def _cipherbyte(self, data: int) -> int:
        for rotor in self.rotors:
            data = rotor.forward(data)

        data = self.reflector.reflect(data)

        for rotor in reversed(self.rotors):
            data = rotor.back(data)

        for rotor in self.rotors:
            if rotor.rotate():
                break

        return data

    def cipher(self, data: bytearray) -> bytearray:
        result: bytearray = bytearray()
        for byte in data:
            result.append(self._cipherbyte(byte)) 
        return result
