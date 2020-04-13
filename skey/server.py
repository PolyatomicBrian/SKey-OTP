#!/usr/bin/env python3

"""server.py
   Author: Brian Jopling, April 2020
   Usage: server.py
   Sample: ./server.py
"""

import sys
from hashlib import md5       # Used for hash iterations of the otp.

''' GLOBALS '''

IS_DEBUG = True

OUT_SERVER_FILE = "server_password.txt"

PROGRAM_ARG_NUM = 0    # i.e. sys.argv[0]

''' CLASSES '''


class FileService:
    def __init__(self):
        print_debug("Creating FileService...")
        print_debug("Successful init of FileService")

    def get_password_from_file(self):
        """Parses string literal from server password file."""
        try:
            sfile = open(OUT_SERVER_FILE, "r")
            last_pword = sfile.readline()
        except Exception:
            error_quit("Failed to read from file %s" % sfile.name, 403)
        return last_pword

    def update_password_in_file(self, new_password):
        """Updates password in server password file with last-used password."""
        try:
            sfile = open(OUT_SERVER_FILE, "w")
            sfile.write("%s" % new_password)
        finally:
            sfile.close()


''' FUNCTIONS '''


def usage():
    """Prints the usage/help message for this program."""
    program_name = sys.argv[PROGRAM_ARG_NUM]
    print("\nUsage:")
    print("\t%s" % program_name)
    print("\tFile \"%s\" must exist and be populated with the next password it expects." % OUT_SERVER_FILE)


def error_quit(msg, code):
    """Prints out an error message, the program usage, and terminates with an
       error code of `code`."""
    print("\n[!] %s" % msg)
    usage()
    sys.exit(code)


def get_next_password(file_service):
    try:
        if not file_service.get_list_from_file():
            print_debug("List of passwords is empty")
            error_quit("All passwords have been exhausted, please generate a new list of passwords!", 200)
        pword = file_service.get_list_from_file()[0]
    except Exception:
        error_quit("Failed to read first password", 500)
    return pword


def do_hash(pword):
    hashed = md5(pword.encode()).hexdigest()  # MD5 hash of that random number.
    otp = hashed[12:20]  # Grab middle 8 chars of MD5 hash
    return otp


def successful_authentication(file_service, new_password):
    print("Authentication successful!")
    file_service.update_password_in_file(new_password)


''' DEBUG '''


def print_debug(msg):
    """Prints if we are in debug mode."""
    if IS_DEBUG:
        print(msg)


''' MAIN '''


def main():
    """Main driver that parses args & creates objects."""
    print_debug("Starting...")
    file_service = FileService()

    print("Enter your OTP: ")
    user_password = str(sys.stdin.readlines()[0].rstrip('\n'))
    print_debug("User submitted: %s" % user_password)

    last_password = file_service.get_password_from_file()

    print_debug("Server stored last password: %s" % last_password)

    hashed_user_password = do_hash(user_password)
    print_debug("Hashed user password is: %s" % hashed_user_password)

    if hashed_user_password == last_password:
        successful_authentication(file_service, user_password)
    else:
        print("Failed to Authenticate.")
    print_debug("Done!")


''' PROCESS '''


if __name__ == '__main__':
    main()
