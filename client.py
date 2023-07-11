# adding shebangs incase the file is run as an executable
#!/usr/bin/env python3
#!/bin/python3

# importing all the required libraries
import socket, threading, sys

# setting up the name of the user
try:
    name = sys.argv[1]
except Exception:
    print('[!] Usage: python3 client.py <name> <hostname_to_connect_to> <port_number>')
    sys.exit()

# setting up the hostname to connect to
try:
    hostname = sys.argv[2]
except Exception:
    print('[!] Usage: python3 client.py <name> <hostname_to_connect_to> <port_number>')
    sys.exit()

# setting up the port number of the server
try:
    port = int(sys.argv[3])
except Exception:
    print('[!] Usage: python3 client.py <name> <hostname_to_connect_to> <port_number>')
    sys.exit()

# initialising the socket for the connection with the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding the client to server on specified address and port
client.connect((hostname, port))

def read_file(path):
    # this fuction will read the contents of a file and then return them
    with open(path, 'r') as file:
    	data = file.read()
    return data

def receive():
    # this function will receive messages
    while True:
        try:
            # recieving messages (limited buffer to 4096 bytes)
            message = client.recv(4096).decode('utf-8')
            if message == 'name':
                client.send(name.encode('utf-8'))
            else:
                print(message)
        except:                                                 
            # if IP address or port number is given other than on which the server is serving, then error will be raised.
            print("[*] The connection with the server has been closed.")
            client.close()
            break

def write():
    # this function will write messages to the screen for connected clients
    while True:
        command = input('')
        split_command = command.split()
        if command.lower() == 'exit':
            client.send(command.encode('utf-8'))
            break
        elif split_command[0] == 'upload':
            path = split_command[1]
            fille_name = path.split('/')[-1]
            content = read_file(split_command[1])
            final_command = f'{split_command[0]} {fille_name} {content}'
            client.send(final_command.encode('utf-8'))
        else:
            message = f'{name} >> ' 
            message = message + command
            client.send(message.encode('utf-8'))

    client.close()

# initialising thread for receiving messages
receive_thread = threading.Thread(target=receive)
receive_thread.start()
# initialising thread for sending  messages 
write_thread = threading.Thread(target=write)
write_thread.start()
