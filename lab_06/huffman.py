from node import Node
import heapq

class Huffman():
    def __init__(self) -> None:
        self.heap = []
        self.codes = {}
        self.frequency = {}

    def _make_freq(self, byte_array: list[int]) -> None:
        for byte in byte_array:
            if not byte in self.frequency:
                self.frequency[byte] = 0
            self.frequency[byte] += 1

    def _make_heap(self) -> None:
        for key in self.frequency:
            node = Node(key, self.frequency[key])
            heapq.heappush(self.heap, node)

    def _merge_nodes(self) -> None:
        while (len(self.heap) > 1):
            node_1 = heapq.heappop(self.heap)
            node_2 = heapq.heappop(self.heap)
            merged_node = Node(None, node_1.freq + node_2.freq)
            merged_node.left = node_1
            merged_node.right = node_2
            heapq.heappush(self.heap, merged_node)

    def _make_code_helper(self, root: Node, current_code: Node) -> None:
        if (root == None):
            return

        if (root.byte != None):
            self.codes[root.byte] = current_code
            return

        self._make_code_helper(root.left, current_code + "0")
        self._make_code_helper(root.right, current_code + "1")

    def _make_codes(self):
        root = self.heap[0]
        current_code = ""
        self._make_code_helper(root, current_code)

    def _encode_byte_array(self, input: list[int]) -> str:
        output = ""
        for byte in input:
            output += self.codes[byte]
        return output

    def _add_padding(self, string) -> str:
        padding = 8 - (len(string) % 8)
        string += "0" * padding
        padding_info = "{0:08b}".format(padding)
        return padding_info + string

    def _remove_padding(self, string: str) -> str:
        padding_info = string[:8]
        padding = int(padding_info, 2)
        return string[8:-padding]

    def _decode_string(self, string: str):
        output = []
        root = self.heap[0]
        current_node = root
        for symbol in string:
            if (symbol == "0"):
                current_node = current_node.left
            elif (symbol == "1"):
                current_node = current_node.right
            if (current_node.byte != None):
                output.append(current_node.byte)
                current_node = root
        return output

    def _string_to_byte_array(self, string: str) -> list[int]:
        byte_array = []
        for i in range(0, len(string), 8):
            byte = string[i: i+8]
            byte_array.append(int(byte, 2))
        return byte_array

    def _byte_array_to_string(self, byte_array: list[int]) -> str:
        string = ""
        for byte in byte_array:
            string += str.zfill(bin(byte)[2:], 8)
        return string

    def compress(self, input: list[int]) -> list[int]:
        self._make_freq(input)
        self._make_heap()
        self._merge_nodes()
        self._make_codes()
        output = self._encode_byte_array(input)
        output = self._add_padding(output)
        output = self._string_to_byte_array(output)
        return output

    def decompress(self, input: list[int]) -> list[int]:
        output = self._byte_array_to_string(input)
        output = self._remove_padding(output)
        output = self._decode_string(output)
        return output
