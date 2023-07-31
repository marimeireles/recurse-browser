from recurse_browser import recurse_requests

if __name__ == "__main__":
    import sys
    recurse_requests.load(sys.argv[1])