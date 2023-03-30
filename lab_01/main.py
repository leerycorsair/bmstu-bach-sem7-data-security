import qrcode
from datetime import datetime
from license import check_license


def main():
    input_data = input("Enter text:")
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(input_data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    img.save("qrcode_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")


if __name__ == "__main__":
    try:
        if check_license():
            main()
        else:
            print("Incorrect license.")
    except:
        print("No license file.")
