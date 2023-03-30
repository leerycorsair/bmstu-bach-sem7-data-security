
import inout
from signature import Signature

OP_FOLDER = "./op_folder/"
DATA_FILENAME = "data.txt"
PUBLIC_KEY_FILENAME = "public_key.pk"
SIGNATURE_FILENAME = "signature.sig"


def main():
    try:
        data = inout.read_from_file(OP_FOLDER, DATA_FILENAME)
        sig_obj = Signature()

        public_key, sig = sig_obj.create(data)
        inout.write_to_file(public_key.export_key(),
                            OP_FOLDER, PUBLIC_KEY_FILENAME)
        inout.write_to_file(sig, OP_FOLDER, SIGNATURE_FILENAME)

        public_key = inout.read_from_file(OP_FOLDER, PUBLIC_KEY_FILENAME)
        sig = inout.read_from_file(OP_FOLDER, SIGNATURE_FILENAME)
        check = sig_obj.verify(data, public_key, sig)
        print(check)

    except BaseException as base_ex:
        print(base_ex)


if __name__ == "__main__":
    main()
