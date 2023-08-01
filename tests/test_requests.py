import test
from recurse_browser import recurse_requests
import pytest

# Start the patches for socket and SSL
_ = test.socket.patch().start()
_ = test.ssl.patch().start()


@pytest.mark.xfail(reason="Known bug, see issue #2")
def test_show():
    assert recurse_requests.show("<body>hello</body>") == "hello"
    assert recurse_requests.show("he<body>llo</body>") == "hello"
    assert recurse_requests.show("he<body>l</body>lo") == "hello"
    assert recurse_requests.show("he<body>l<div>l</div>o</body>") == "hello"
    assert recurse_requests.show("he<body>l</div>lo") == "hello"
    assert recurse_requests.show("he<body>l<div>l</body>o</div>") == "hello"


def test_request():
    url = "http://test.test/example1"
    test.socket.respond(
        url, b"HTTP/1.0 200 OK\r\n" + b"Header1: Value1\r\n\r\n" + b"Body text"
    )
    headers, body = recurse_requests.request(url)
    assert (
        test.socket.last_request(url)
        == b"GET /example1 HTTP/1.0\r\nHost: test.test\r\n\r\n"
    )
    assert body == "Body text"
    assert headers == {"header1": "Value1"}


def test_transfer_encoding():
    url = "http://test.test/te"
    test.socket.respond(
        url,
        b"HTTP/1.0 200 OK\r\n" + b"Transfer-Encoding: chunked\r\n\r\n" + b"0\r\n\r\n",
    )
    with pytest.raises(AssertionError):
        recurse_requests.request(url)


def test_content_encoding():
    url = "http://test.test/ce"
    test.socket.respond(
        url,
        b"HTTP/1.0 200 OK\r\n" + b"Content-Encoding: gzip\r\n\r\n" + b"\x00\r\n\r\n",
    )
    with pytest.raises(AssertionError):
        recurse_requests.request(url)


def test_ssl_support():
    url = "https://test.test/example2"
    test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\n")
    header, body = recurse_requests.request(url)
    assert body == ""

    url = "https://test.test:400/example3"
    test.socket.respond(url, b"HTTP/1.0 200 OK\r\n\r\nHi")
    header, body = recurse_requests.request(url)
    assert body == "Hi"

    with pytest.raises(KeyError):
        recurse_requests.request("http://test.test:401/example3")
