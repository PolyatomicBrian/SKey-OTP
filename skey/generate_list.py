#!/usr/bin/env python3

"""generate_list.py: Generates a list containing n iterations of a hashed password.
   Author: Brian Jopling, April 2020."""
import sys

''' IMPORTS '''

''' GLOBALS '''

IS_DEBUG = True

# Program Arguments
REQUIRED_NUM_ARGS = 1
MAXIMUM_NUM_ARGS = 1

PROGRAM_ARG_NUM = 0    # i.e. sys.argv[0]
NUM_ITERS_ARG_NUM = 1  # i.e. sys.argv[1]

''' CLASSES '''

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
        # Is num_iters a valid value?
        if not isinstance(num_iters, int) or num_iters < 1:
            raise ValueError("Arg for num iterations must be a positive int!")
    except ValueError:
        error_quit("Arg for num iterations must be a positive int!", 400)
    except Exception:
        error_quit("Arg for num iterations must be a positive int!", 400)
    return int(num_iters)


def parse_args():
    """Gets and returns provided arguments."""
    if len(sys.argv) < REQUIRED_NUM_ARGS or len(sys.argv) > MAXIMUM_NUM_ARGS:
        error_quit("Incorrect number of arguments!", 400)
    num_iters = sys.argv[NUM_ITERS_ARG_NUM]
    num_iters = validate_iters(num_iters)
    return num_iters

''' DEBUG '''

def print_debug(msg):
    """Prints if we are in debug mode."""
    if IS_DEBUG:
        print(msg)


''' MAIN '''

def main():
    """Main driver that parses args & creates objects."""
    print_debug("Starting...")
    num_iters = parse_args()
    print_debug("Received argument: %s" % num_iters)


''' PROCESS '''

if __name__ == '__main__':
    main()
