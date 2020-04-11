#!/usr/bin/env python3

"""generate_list.py: Generates a list containing n iterations of a hashed password.
   Author: Brian Jopling, April 2020
   Usage: generate-list.py n
          n corresponds to the number of OTPs to be generated.
   Sample: ./generate-list.py 4
"""

import sys
from random import randrange  # Used for generating a seed.
from hashlib import md5       # Used for hash iterations of the seed.

''' GLOBALS '''

IS_DEBUG = True

OUT_FILE = "list-passwords.txt"

MAX_SEED = 1024  # Entropy of passwords based on this value.

# Program Arguments
REQUIRED_NUM_ARGS = 2  # Require prog name and num iters
MAXIMUM_NUM_ARGS = 2

PROGRAM_ARG_NUM = 0    # i.e. sys.argv[0]
NUM_ITERS_ARG_NUM = 1  # i.e. sys.argv[1]


''' CLASSES '''


class FileService:
    # Class vars:
    #   * file - File
    def __init__(self):
        print_debug("Creating FileService...")
        # Create file
        f = open(OUT_FILE, "w")
        self.file = f
        print_debug("Successful init of FileService")

    def write(self, list_passwords):
        """Writes passwords to output file."""
        self.file.write("%s" % str(list_passwords))

    def close_file(self):
        """Simply closes the file."""
        self.file.close()


''' FUNCTIONS '''


def usage():
    """Prints the usage/help message for this program."""
    program_name = sys.argv[PROGRAM_ARG_NUM]
    print("Usage:")
    print("%s NUM_ITERS" % program_name)
    print("  NUM_ITERS : Number of iterations to hash pass; positive integer.")


def error_quit(msg, code):
    """Prints out an error message, the program usage, and terminates with an
       error code of `code`."""
    print("[!] %s" % msg)
    usage()
    exit(code)


def validate_iters(num_iters):
    """Verifies that the provided argument for number of hash iterations is
       a valid int greater than 0."""
    try:
        num_iters = int(num_iters)
        if num_iters < 1:
            raise ValueError("Arg for num iterations must be a positive int!")
    except ValueError:
        error_quit("Arg for num iterations must be a positive int!", 400)
    except Exception:
        error_quit("Arg for num iterations must be a positive int!", 400)
    return num_iters


def parse_args():
    """Gets and returns provided arguments."""
    if len(sys.argv) < REQUIRED_NUM_ARGS or len(sys.argv) > MAXIMUM_NUM_ARGS:
        error_quit("Incorrect number of arguments!", 400)
    num_iters = sys.argv[NUM_ITERS_ARG_NUM]
    num_iters = validate_iters(num_iters)
    return num_iters


def generate_passwords(num_iters):
    """Returns list of OTPs based on the 8 middle characters of an MD5-hashed
       pseudorandom number."""
    list_passwords = []
    for i in range(0, num_iters):
        seed = randrange(MAX_SEED)  # Generate random number.
        hashed_seed = md5(b'%d' % seed).hexdigest()  # MD5 hash of that random number.
        otp = hashed_seed[12:20]    # Grab middle 8 chars of MD5 hash
        list_passwords.append(otp)
    return list_passwords


''' DEBUG '''


def print_debug(msg):
    """Prints if we are in debug mode."""
    if IS_DEBUG:
        print(msg)


''' MAIN '''


def main():
    """Main driver that parses args & creates objects."""
    print_debug("Starting...")
    print_debug("Args: %s" % str(sys.argv))
    num_iters = parse_args()
    print_debug("Received argument: %s" % num_iters)
    file_service = FileService()
    list_passwords = generate_passwords(num_iters)
    print_debug("Generated password list: %s" % str(list_passwords))
    file_service.write(list_passwords)
    file_service.close_file()
    print_debug("Done!")


''' PROCESS '''


if __name__ == '__main__':
    main()
