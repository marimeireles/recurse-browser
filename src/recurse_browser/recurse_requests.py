import socket
import ssl


def parse_url(url):
    scheme, url = url.split("://", 1)
    if "/" not in url:
        url = url + "/"
    host, path = url.split("/", 1)
    return (scheme, host, "/" + path)


def request(url):
    (scheme, host, path) = parse_url(url)
    assert scheme in ["http", "https"], "Unknown scheme {}".format(scheme)

    # default ports for http and https, respectively
    port = 80 if scheme == "http" else 443

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    # relevant configs. to connect via TCP
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
    s.connect((host, port))

    if scheme == "https":
        """
        TLS (Transport Layer Security)

        TLS is the successor to SSL and is currently the standard for secure network
        communication. It provides privacy and data integrity between two communicating
        applications and is used for web browsers and other applications that require
        data to be securely exchanged over a network.

        TLS ensures that:

          Encryption: Data transmitted over the network is encrypted, so that even if
          someone intercepts the packets, they can't read the actual data without the
          correct encryption keys.

          Authentication: The server (and optionally the client) must prove its
          identity using a digital certificate. This ensures that you're communicating
          with the legitimate server and not a malicious actor.

          Integrity: The data cannot be tampered with in transit without detection.
          This ensures that the data you send arrives at its destination in the same
          form as when it was sent.
        """

        # sets up rules and params. for how the SSL/TLS handshake should be conducted
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    # formatting is extremely important as the host and local machines counts with
    # specific formatting to conclude their handshakes
    s.send(
        ("GET {} HTTP/1.0\r\n".format(path) + "Host: {}\r\n\r\n".format(host)).encode(
            "utf8"
        )
    )
    response = s.makefile("r", encoding="utf8", newline="\r\n")

    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n":
            break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    # we need to treat these headers differently
    # ToDo: Add support for HTTP compression issue #1
    assert "transfer-encoding" not in headers
    assert "content-encoding" not in headers

    body = response.read()
    s.close()

    return headers, body


def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")


def load(url):
    headers, body = request(url)
    show(body)
