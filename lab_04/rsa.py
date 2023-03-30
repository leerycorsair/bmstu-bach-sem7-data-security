import json
from random import choice, randrange


class RSA:
    def __init__(self, settings_filename: str, generate: bool = True) -> None:
        settings_file = open(settings_filename, "r")
        settings = json.load(settings_file)
        settings_file.close()

        if generate:
            key_length_tmp = int(settings["key_length"])
            self._key_length = self._adjust_key_length(key_length_tmp)
            self._generate_keys()
        else:
            self._keyLength = int(settings["default"]["key_length"])
            self._n = int(settings["default"]["n"])
            self._d = int(settings["default"]["d"])
            self._e = int(settings["default"]["e"])

    def _adjust_key_length(self, key_length: int) -> int:
        r = key_length % 8
        if (r >= 4):
            return key_length + (8 - r)
        else:
            return key_length - r

    def _gcd(self, num_1: int, num_2: int) -> int:
        if num_2 == 0:
            return num_1
        else:
            return self._gcd(num_2, num_1 % num_2)

    def _gcd_extended(self, num_1: int, num_2: int, u_1: int = 1, v_1: int = 0, u_2: int = 0, v_2: int = 1) -> tuple[int, int, int]:
        if (num_2 == 0):
            return num_1, 1, 0

        q = num_1 // num_2
        r = num_1 % num_2

        u_1_, v_1_ = u_2, v_2
        u_2_, v_2_ = u_1 - q * u_2, v_1 - q * v_2
        return (num_2, u_2, v_2) if (r == 0) else self._gcd_extended(num_2, r, u_1_, v_1_, u_2_, v_2_)

    def _prime_eratosthenes(self, bottom: int, top: int) -> list[int]:
        non_prime_list = []
        prime_list = []
        for i in range(2, top + 1):
            if i not in non_prime_list:
                prime_list.append(i)
                for j in range(i*i, top + 1, i):
                    non_prime_list.append(j)
        return [num for num in prime_list if num >= bottom]

    def _coprime_euclid(self, phi: int) -> int:
        e = randrange(1, phi)
        while self._gcd(e, phi) != 1:
            e = randrange(1, phi)
        return e

    def _mod_inverse_extended_euclid(self, e: int, phi: int) -> int:
        _, _, v = self._gcd_extended(phi, e)

        return v % phi

    def _generate_keys(self) -> None:
        length = int(self._key_length / 2)
        top = 2**(length) - 1
        bottom = 2**(length - 1) + 1

        prime_list = self._prime_eratosthenes(bottom, top)
        p = choice(prime_list)
        prime_list.remove(p)
        q = choice(prime_list)

        self._n = p * q

        phi = (p - 1) * (q - 1)

        self._e = self._coprime_euclid(phi)
        self._d = self._mod_inverse_extended_euclid(self._e, phi)

    def _num_array_to_byte_array(self, num_array: list[int], bytes_in_num: int) -> list[int]:
        byte_array = []
        for num in num_array:
            for _ in range(bytes_in_num):
                byte_array.append(num % 256)
                num //= 256
        return byte_array

    def _byte_array_to_num_array(self, byte_array: list[int], bytes_in_num: int) -> list[int]:
        num_array = []
        for i in range(0, len(byte_array) - bytes_in_num + 1, bytes_in_num):
            num = 0
            for j in range(bytes_in_num - 1, -1, -1):
                num = num * 256 + byte_array[i + j]
            num_array.append(num)
        return num_array

    def _RSA(self, input: list[int], decode: bool = False) -> list[int]:
        if not decode:
            output = [pow(byte, self._e, self._n) for byte in input]
        else:
            output = [pow(byte, self._d, self._n) for byte in input]

        return output

    def encode(self, input: list[int]) -> list[int]:
        output = self._RSA(input)
        output = self._num_array_to_byte_array(output, int(self._key_length/8))
        return output

    def decode(self, input: list[int]) -> list[int]:
        output = self._byte_array_to_num_array(input, int(self._key_length/8))
        output = self._RSA(output, decode=True)
        return output
