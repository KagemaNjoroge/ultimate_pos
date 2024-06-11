import platform
import subprocess


def ping(host: str) -> bool:
    """
    Returns True if host responds to a ping request
    This function is used to detect the status of the eTIMS server
    """
    # remove the protocol from the host
    host = host.split("://")[-1]
    # remove port
    host = host.split(":")[0]

    param = "-n" if platform.system().lower() == "windows" else "-c"

    command = ["ping", param, "1", host]

    return subprocess.call(command) == 0
