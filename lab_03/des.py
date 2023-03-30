import json


class DES:
    def __init__(self, settings_filename: str) -> None:
        settings_file = open(settings_filename, "r")
        settings = json.load(settings_file)
        settings_file.close()

        self.key = settings["key"]
        self.initial_permutation = settings["initial_permutation"]
        self.expansion = settings["expansion"]
        self.sboxes = settings["sboxes"]
        self.each_round_permutation = settings["each_round_permutation"]
        self.final_permutation = settings["final_permutation"]

    def _add_padding(self, string: str) -> str:
        padding = 8 - (len(string) % 8)
        if padding == 0:
            padding = 8
        string += [padding] * padding
        return string

    def _remove_padding(self, string: str) -> str:
        padding = string[-1]
        return string[:-padding]

    def _n_split(self, list: list, n: int) -> list[list]:
        return [list[i: i + n] for i in range(0, len(list), n)]

    def _xor(self, list_1: list, list_2: list):
        return [element_1 ^ element_2 for element_1, element_2 in zip(list_1, list_2)]

    def _bin_value(self, val: int, bit_size: int) -> str:
        bin_val = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
        while len(bin_val) < bit_size:
            bin_val = "0" + bin_val
        return bin_val

    def _string_to_bit_array(self, input: str) -> list[int]:
        bit_array = []
        for letter in input:
            bin_val = self._bin_value(letter, 8)
            bin_val_arr = [int(x) for x in list(bin_val)]
            bit_array += bin_val_arr
        return bit_array

    def _byte_array_to_bit_array(self, array: list[int]) -> list[int]:
        bit_array = []
        for byte in array:
            bit_str = str.zfill(bin(byte)[2:], 8)
            for bit in bit_str:
                bit_array.append(int(bit))
        return bit_array

    def _bit_array_to_byte_array(self, array: list[int]) -> list[int]:
        byte_chunks = self._n_split(array, 8)
        bytes_list = []
        for byte in byte_chunks:
            bits_list = []
            for bit in byte:
                bits_list += str(bit)
            bytes_list.append(int(''.join(bits_list), 2))
        return bytes_list

    def _expand(self, array: list, table: list) -> list:
        return [array[element - 1] for element in table]

    def _left_shift(self, list_1: list, list_2: list, n: int) -> list:
        return list_1[n:] + list_1[:n], list_2[n:] + list_2[:n]

    def _permute(self, array: list, table: list) -> list:
        return [array[element - 1] for element in table]

    def _generate_keys(self) -> list:
        keys = []
        key = self._string_to_bit_array(self.key["value"])
        key = self._permute(key, self.key["permutation_1"])
        left_block, right_block = self._n_split(key, 28)

        for i in range(16):
            left_block, right_block = self._left_shift(
                left_block, right_block, self.key["shift"][i])
            tmp = left_block + right_block
            keys.append(self._permute(tmp, self.key["permutation_2"]))
        return keys

    def _sbox_substitute(self, bit_array: list[int]) -> list[int]:
        blocks = self._n_split(bit_array, 6)
        result = []

        for i in range(len(blocks)):
            block = blocks[i]
            row = int(str(block[0]) + str(block[5]), 2)
            column = int(''.join([str(x) for x in block[1:-1]]), 2)
            sbox_value = self.sboxes[i][row][column]
            bin_val = self._bin_value(sbox_value, 4)
            result += [int(bit) for bit in bin_val]
        return result

    def _DES(self, input: list[int], decode: bool = False) -> list[int]:
        keys = self._generate_keys()

        input_8byte_blocks = self._n_split(input, 8)
        result = []

        for block in input_8byte_blocks:
            block = self._byte_array_to_bit_array(block)
            block = self._permute(block, self.initial_permutation)
            left_block, right_block = self._n_split(block, 32)

            tmp = None
            for i in range(16):
                expanded_right_block = self._expand(
                    right_block, self.expansion)

                if not decode:
                    tmp = self._xor(keys[i], expanded_right_block)
                else:
                    tmp = self._xor(keys[15 - i], expanded_right_block)

                tmp = self._sbox_substitute(tmp)
                tmp = self._permute(tmp, self.each_round_permutation)
                tmp = self._xor(left_block, tmp)

                left_block = right_block
                right_block = tmp

            result += self._permute(right_block + left_block,
                                    self.final_permutation)

        output = self._bit_array_to_byte_array(result)
        return output

    def encode(self, input: list[int]) -> list[int]:
        input = self._add_padding(input)
        output = self._DES(input)
        return output

    def decode(self, input: list[int]) -> list[int]:
        output = self._DES(input, decode=True)
        output = self._remove_padding(output)
        return output
