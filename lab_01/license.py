

from sys import platform
import subprocess
import hashlib


def run(cmd):
    completed = subprocess.run(
        ["powershell", "-Command", cmd], capture_output=True)
    return completed


def get_system_info():
    system_info = ""
    if platform == "win32":
        command = "Get-CimInstance -ClassName Win32_BIOS | Select-Object -Property SerialNumber"
        bios_serial_number = run(command).stdout.decode(
            "utf-8").split("------------")[1].strip()
        command = "Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object -Property SerialNumber"
        os_serial_number = run(command).stdout.decode(
            "utf-8").split("------------")[1].strip()
        system_info = bios_serial_number + os_serial_number
        system_info = hashlib.sha256(system_info.encode('utf-8')).hexdigest()
    return system_info


def check_license():
    with open("license.key", "r") as lic_file:
        return lic_file.readline() == get_system_info()


def write_license():
    with open("license.key", "w") as licence_file:
        licence_file.write(str(get_system_info()))


if __name__ == "__main__":
    write_license()
