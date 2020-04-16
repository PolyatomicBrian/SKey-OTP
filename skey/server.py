#!/usr/bin/env python3

"""server.py
   Author: Brian Jopling, April 2020
   Usage: server.py [PORT]
   Sample: ./server.py
           ./server.py 40123
"""
import socket
import sys
import threading
from hashlib import md5       # Used for hash iterations of the otp.
from datetime import datetime # Used to timestamp logs.

''' GLOBALS '''

IS_DEBUG = True

OUT_SERVER_FILE = "server_password.txt"

PROGRAM_ARG_NUM = 0    # i.e. sys.argv[0]
PORT_ARG_NUM = 1       # i.e. sys.argv[1], optional port arg

DEFAULT_PORT = 40000
BUFF_SIZE = 1024

MSG_SERVER_SUCCESS = "Authentication Successful!\n"
MSG_SERVER_FAILURE = "Authentication Failure!\n"

''' CLASSES '''


class ClientConnectedThread(threading.Thread):
    """New thread for every connected client. Each thread
       handles an individual client's requests."""
    # Class vars:
    #   * client_ip - String
    #   * client_port - String
    #   * client_sock - Socket
    #   * lock - Mutex lock
    #   * file_service - Service for reading/writing to password file.
    def __init__(self, ip, port, sock, lock):
        """Initialize args to class variables."""
        threading.Thread.__init__(self)
        print_debug(datetime.now())
        self.client_ip = ip
        self.client_port = port
        self.client_sock = sock
        self.lock = lock
        self.file_service = FileService()

    def run(self):
        """Driver for individual thread. Handles client requests."""
        print_debug("Host %s:%s has connected!" % (self.client_ip, self.client_port))
        while True:
            try:
                # Get otp from client
                otp_recv = self.parse_client_request().decode('utf-8').rstrip('\r\n')
                print_debug("User sent over: %s" % otp_recv)
                self.lock.acquire()
                try:
                    serv_msg = self.authenticate_otp(otp_recv)
                    self.client_sock.send(serv_msg.encode())
                finally:
                    self.client_sock.close()
                    self.lock.release()
                    return
            except Exception as e:
                print_debug("Encountered error: " + str(e))

    def parse_client_request(self):
        try:
            msg_rec = self.client_sock.recv(BUFF_SIZE)
        except socket.error:
            print_debug("Connection error, unable to receive command.", 400)
        except:
            print_debug("An unknown error occurred, unable to receive command.", 400)
        return msg_rec

    def authenticate_otp(self, otp_recv):
        last_password = self.file_service.get_password_from_file()
        print_debug("Server's last stored password: %s" % last_password)
        hashed_user_password = self.do_hash(otp_recv)
        print_debug("Hashed user password is: %s" % hashed_user_password)
        if hashed_user_password == last_password:
            return self.successful_authentication(self.file_service, otp_recv)
        else:
            return self.failed_authentication()

    def do_hash(self, pword):
        hashed = md5(pword.encode()).hexdigest()  # MD5 hash of that random number.
        otp = hashed[12:20]  # Grab middle 8 chars of MD5 hash
        return otp

    def successful_authentication(self, file_service, new_password):
        print(MSG_SERVER_SUCCESS)
        file_service.update_password_in_file(new_password)
        return MSG_SERVER_SUCCESS

    def failed_authentication(self):
        print(MSG_SERVER_FAILURE)
        return MSG_SERVER_FAILURE


class FileService:
    def __init__(self):
        print_debug("Creating FileService...")
        print_debug("Successful init of FileService")

    def get_password_from_file(self):
        """Parses string literal from server password file."""
        try:
            sfile = open(OUT_SERVER_FILE, "r")
            last_pword = sfile.readline().rstrip('\n')
        except Exception:
            error_quit("Failed to read from file %s" % sfile.name, 500)
        return last_pword

    def update_password_in_file(self, new_password):
        """Updates password in server password file with last-used password."""
        try:
            sfile = open(OUT_SERVER_FILE, "w")
            sfile.write("%s\n" % new_password)
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


def handle_client_connections(server_port):
    """Driver that creates a socket and handles connections."""
    print_debug("Starting server.")
    try:
        lock = threading.Lock()
        # Create socket, connect to host and port.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', server_port))
        s.listen(1)
        print_debug("Server running.")
        while 1:
            try:
                conn, addr = s.accept()
                ip = addr[0]
                port = addr[1]
                client = ClientConnectedThread(ip, port, conn, lock)  # New thread.
                client.start()
            except Exception as e:
                print("Encountered error: " + str(e))
    except socket.error as e:
        print("Unable to connect due to " + str(e))


''' DEBUG '''


def print_debug(msg):
    """Prints if we are in debug mode."""
    if IS_DEBUG:
        print(msg)


''' MAIN '''


def main():
    """Main driver."""
    print_debug("Starting...")
    port = sys.argv[PORT_ARG_NUM] if len(sys.argv) == PORT_ARG_NUM + 1 else DEFAULT_PORT
    port = int(port)
    handle_client_connections(port)
    print_debug("Done!")


''' PROCESS '''


if __name__ == '__main__':
    main()
