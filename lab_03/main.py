import inout
from des import DES

OP_FOLDER = "./op_folder/"
INPUT_ARR = ["data.txt", "data.jpg",
             "data.rar"]
DES_SETTINGS_FILENAME = "./settings.json"


def main():
    try:
        for filename in INPUT_ARR:
            des_obj = DES(DES_SETTINGS_FILENAME)

            input = inout.read_from_file(OP_FOLDER, filename)
            output = des_obj.encode(input)
            inout.write_to_file(output, OP_FOLDER, "encoded_" + filename)

            input = inout.read_from_file(OP_FOLDER, "encoded_" + filename)
            output = des_obj.decode(input)
            inout.write_to_file(output, OP_FOLDER, "decoded_" + filename)
            
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
