import socket


def find_free_port():
    """
    Finds a free port on the local machine

        :return: A free port on the local machine
        :rtype: int
    """

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))  # Bind to any available IP address and port 0

    # Get the assigned port
    _, port = sock.getsockname()

    # Close the socket
    sock.close()

    return port
