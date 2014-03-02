"""
This module just contains the code to call the command-line program 'rsync'
from inside python.
"""
import subprocess


def rsync_logs(target_username, target_ip, target_path):
    """
    This function sends the contents of the PATH specified to the TARGET path
    via rsync.

    RSync is a program which synchronized directories in 2 different places.
    When invoked, it compares the 2 paths and only sends files which are
    necessary for them to stay synchronized. It doesn't send all of the files.
    It sends files over SSH (Secure Shell).
    """
    # This is how you call a command line code inside python. The below line
    # calls:
    #     rsync -rave "ssh -l <TARGET-USERNAME>" --delete <SOURCE> <TARGET>
    #
    try:
        subprocess.call(["rsync", "-rave", "ssh -l " + target_username,
                         "--delete", target_path, target_ip])
    except:
        return False
    return True

