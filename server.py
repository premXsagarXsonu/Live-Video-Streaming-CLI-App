# In this video server is receiving video from clients.
#importing the libraries

import socket,pickle, struct
import imutils
import threading
import cv2
import os
import hashlib
import json

from termcolor import colored
from pyfiglet import Figlet

f = Figlet(font='standard')
print(colored(f.renderText('Send is Live'),'green'))

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
print(host_name)
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 9999
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

HashTable = {}
ThreadCount = 0

with open('users.txt') as f_in:
    HashTable = json.load(f_in)

def init():
    global ThreadCount
    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(
            target=threaded_client,
            args=(address,client_socket)  
        )
        client_handler.start()
        ThreadCount += 1
        print('Connection Request: ' + str(ThreadCount))

def show_client(addr,client_socket):
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket: # if a client socket exists
			data = b""
			payload_size = struct.calcsize("Q")
			while True:
				while len(data) < payload_size:
					packet = client_socket.recv(4*1024) # 4K
					if not packet: break
					data+=packet
				packed_msg_size = data[:payload_size]
				data = data[payload_size:]
				msg_size = struct.unpack("Q",packed_msg_size)[0]
				
				while len(data) < msg_size:
					data += client_socket.recv(4*1024)
				frame_data = data[:msg_size]
				data  = data[msg_size:]
				frame = pickle.loads(frame_data)
				cv2.imshow(f"FROM {addr}",frame)
				key = cv2.waitKey(1) & 0xFF
				if key  == ord('q'):
					break
			client_socket.close()
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		pass


# Function : For each client 
def threaded_client(addr,client_socket):
    client_socket.send(str.encode('Enter User Name : ')) # Request Username
    name = client_socket.recv(2048)
    client_socket.send(str.encode('Enter Password : ')) # Request Password
    password = client_socket.recv(2048)
    password = password.decode()
    name = name.decode()
    password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# REGISTERATION PHASE   
# If new user,  regiter in Hashtable Dictionary  
    if name not in HashTable:
        HashTable[name]=password

        with open('users.txt', 'w') as json_file:
            json.dump(HashTable, json_file)

        client_socket.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        show_client(addr,client_socket)
        client_socket.close()
    else:
# If already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            client_socket.send(str.encode('Connection Successful')) # Response Code for Connected Client 
            print('Connected : ',name)
            show_client(addr,client_socket)
        else:
            # client_socket.send(str.encode('Login Failed')) # Response code for login failed
            client_socket.send(str.encode("Login Failed")) # Response code for login failed
            print('Connection denied : ',name)
            client_socket.close()
    while True:
        break
    

init()