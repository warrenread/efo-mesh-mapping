import sys

def newsflash(msg):
    """
    Sends a message to the standard error console; gets around posting info
    to console while redirecting standard output to a file (or whatever).
    """
    sys.stderr.write("%s\n" % (msg))
