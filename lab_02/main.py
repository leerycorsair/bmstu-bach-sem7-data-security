

from copy import deepcopy

from enigma.enigma import Enigma


def main():
    try:
        file_name = input("FileName:")
        in_file = open(file_name, "rb")
        data = bytearray(in_file.read())
        in_file.close()

        enigma1 = Enigma()
        enigma2 = deepcopy(enigma1)

        c_name = file_name.split(".")
        c_name = c_name[0]+"_ciphered."+c_name[1]
        ciphered = enigma1.cipher(data)
        c_file = open(c_name, "wb")
        c_file.write(ciphered)
        c_file.close()

        d_name = file_name.split(".")
        d_name = d_name[0]+"_deciphered."+d_name[1]
        deciphered = enigma2.cipher(ciphered)
        d_file = open(d_name, "wb")
        d_file.write(deciphered)
        d_file.close()
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")


if __name__ == "__main__":
    main()
