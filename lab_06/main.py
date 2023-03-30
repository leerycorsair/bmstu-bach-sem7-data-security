import inout
from huffman import Huffman

OP_FOLDER = "./op_folder/"
INPUT_ARR = ["data.txt", "data.jpg",
             "data.rar"]


def main():
    try:
        for filename in INPUT_ARR:
            huff_obj = Huffman()

            input = inout.read_from_file(OP_FOLDER, filename)
            output = huff_obj.compress(input)
            inout.write_to_file(output, OP_FOLDER, "compressed_" + filename)

            input = inout.read_from_file(OP_FOLDER, "compressed_" + filename)
            output = huff_obj.decompress(input)
            inout.write_to_file(output, OP_FOLDER, "decompressed_" + filename)

    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
