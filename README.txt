SKey: Lamport's Scheme for OTPs
-------------------------------
Brian Jopling, April 2020

Description:

An implementation of RFC1760, aka the S/KEY One-Time Password System, with a
slightly modified algorithm for generating OTPs. Written in `python3`.


Usage:

1. Generate OTPs by running generate_list.py with a specified number of OTPs:

    `python3 generate_list.py 8`

    This will output two files:

    `client_passwords.txt`, which is a list of passwords that the client shall
    read from and update.

    `server_password.txt`, which contains a single OTP that the server shall
    read from and update.


2. Start the server for accepting OTPs from the client:

    `python3 server.py`

    By default, this will run on port 40000. Specifying an arg will change
    the port used, e.g. `python3 server.py 41234`.


3. Use the client to authenticate with the server by using an OTP from its list.

    `python3 client.py`

    By default, this will connect to localhost on port 40000. Specifying args
    will override this, e.g. `python3 client.py 10.0.0.1 41234`.

    On successful authentication, the client will display "Authentication
    Successful!"
    On a failed authentication, the client will display "Authentication
    Failure!"

    If the client has run out of OTPs, an error will be displayed, reading:
    `All passwords have been exhausted, please generate a new list of passwords!`
    This can be done by returning to step 1.


Algorithm for OTP Generation:

1. Generates a random integer, defaulting between 1 and 1024.
2. Hashes that random integer using MD5.
3. Grabs the middle 8 characters of that hash (from index 12 to 20).
4. This initial 8-character hash is used as the Server's starting OTP.
5. In a loop of n iterations (where n is specified by the user), the hash
   is hashed with MD5 again, and the middle 8 characters are taken again,
   getting the next hash.

