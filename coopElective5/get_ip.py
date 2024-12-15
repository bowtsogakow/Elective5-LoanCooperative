import socket 

def get_local_ip():
    """
    Get the local IP address of the machine.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        s.connect(('10.254.254.254', 1))  # A public IP address, doesn't matter if it's unreachable
        ip = s.getsockname()[0]  # This gets the local IP address
    except Exception:
        ip = '127.0.0.1'  # Fallback to localhost if network is unavailable
    finally:
        s.close()
    return ip