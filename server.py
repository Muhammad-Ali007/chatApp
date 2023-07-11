# adding shebangs incase the file is run as an executable
#!/usr/bin/env python3
#!/bin/python3

# importing all the required libraries
import os
import threading, socket, sys

# choosing the localHost as the server. we can also choose an ip address for communication over broader perspective.
host = '127.0.0.1'
try:
    port = int(sys.argv[1])
except Exception:
    print('[!] Usage: python3 server.py <port_number_currently_not_in_use>')
    sys.exit(1)

# initialising the socket for the connection with clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# binding to host and port specified
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message):
    # this function will broadcast messages to all the users connected
    for client in clients:
        client.send(message)

def write_file(path, content):
	with open(path, 'w') as file:
		file.write(content)
		return '[+] Upload successful ...'

def handle(client):
    # this function will send and receive messages in the chat
    index = clients.index(client)
    name = names[index]
    while True:
        try:
            # recieving messages (limited buffer to 4096 bytes) from client and then broadcasting it to all the users
            message = client.recv(4096)
            decoded_message = message.decode('utf-8').split()
            if decoded_message[0].lower() == 'exit':
                 break
            elif decoded_message[0] == 'upload':
                file_content = ''
                for x in decoded_message[2:]:
                    file_content += x + ' '
                file_content = file_content.strip()
                if not os.path.exists(f'{name}'):
                    os.mkdir(f'{name}')
                    write_file(f'{name}/{decoded_message[1]}', file_content)
                else:
                    write_file(f'{name}/{decoded_message[1]}', file_content)
            else:
                broadcast(message)
        except:
            # removing clients from the list who have left
            clients.remove(client)
            client.close()
            broadcast('[*] {} left due to a problem in network connection.'.format(name).encode('utf-8'))
            names.remove(name)
            break

    clients.remove(client)
    client.close()
    names.remove(name)
    broadcast('[*] {} left.'.format(name).encode('utf-8'))

def receive():
    # this function will handle multiple clients connecting and leaving the server
    print('[+] Server is up and running. Awaiting connections...\n')
    while True:
        # this loop will keep accepting messages from the users
        client, address = server.accept()
        print("[*] Connected with {}".format(str(address)))
        client.send('name'.encode('utf-8'))
        name = client.recv(4096).decode('utf-8')
        names.append(name)
        print("[*] Name >> {}\n".format(name))
        client.send('[+] Welcome to the server!\n[*] Command to upload files to the server is: upload <file>\n[*] You can only upload one file at a time and the program will quit after file upload.\n[*] File will be stored in the server in a directory under your name.\n[*] You can exit from the chat anytime by typing "exit"\n\n'.encode('utf-8'))
        broadcast("[*] {} joined!".format(name).encode('utf-8'))
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client,)) # comma is added to prevent a small error
        thread.start()

# invoking the receive function that will start the server hereon
receive()
