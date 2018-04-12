import sys

def newsflash(msg=None):
    """
    Sends a message to the standard error console; gets around posting info
    to console while redirecting standard output to a file (or whatever).
    """
    if msg is None:
        msg = ""
    sys.stderr.write("%s\n" % (msg))
