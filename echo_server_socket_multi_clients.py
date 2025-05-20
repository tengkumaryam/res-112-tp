#!/usr/bin/env python3

"""A server module for the socket echo.
"""

import argparse
import socket
import signal
import os
import sys

#################################################
## Parsing command line arguments
parser = argparse.ArgumentParser(description='Echo Server')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    metavar="[1024-49151]", 
                    help='the port number to bind to')

options = parser.parse_args()

if options.port > 49151 or options.port < 1024:
    print("Invalid port: the port number has to be between 1024 and 49151")
    exit(1)


#################################################
## Global variables
host = ''  # address to bind to. '' means all available interfaces
s = None   # variable to store your socket


#################################################
## Handling of Ctrl+C
def close_connection(sig, frame):
    print('Ctrl+C Pressed. Closing the socket...')
    if s:
        # close the socket
        s.close()
    sys.exit(0)

# Register this handler for Ctrl+C (SIGINT) event
signal.signal(signal.SIGINT, close_connection)




#################################################
## The main program

# socket creation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Allow reusing of adress
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind with a local address and port
s.bind((host, options.port))

# make it a server socket
s.listen(3)
print("Server listening on port", options.port)

while True:
    # wait for a connection
    conn, address = s.accept()
    print("Connection accepted")
    child = os.fork()
    if child == 0:
        s.close()
        while True:
            # receive the data
            data = conn.recv(1024)
            if not data:
                break
            print("Received: " + data.decode('utf-8'))
        print("Connection broken!")
        # we close the connection
        conn.close()
        os._exit(0)
    else:
        conn.close()
s.close()