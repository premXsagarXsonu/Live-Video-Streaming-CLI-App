# In this code client is sending video to server
import socket,cv2, pickle,struct
import imutils # pip install imutils
import fire #creating cli apps
from termcolor import colored
from pyfiglet import Figlet

f = Figlet(font='standard')
print(colored(f.renderText('Send is Ready'),'green'))

class Stream(object):
	def __init__(self):
		self.SEND = Send() 

class Send(object):

	def video(self):
		ip = input("Enter The Desitnation IP: ")
		
		video_file = input("Video File Adddress: ")
		vid = cv2.VideoCapture(video_file)
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		host_ip = ip
		port = 9999
		client_socket.connect((host_ip,port))

		response = client_socket.recv(2048)
		# Input UserName
		name = input(response.decode())	
		client_socket.send(str.encode(name))
		response = client_socket.recv(2048)
		# Input Password
		password = input(response.decode())	
		client_socket.send(str.encode(password))

		''' Response : Status of Connection :
			1 : Registeration successful 
			2 : Connection Successful
			3 : Login Failed
		'''
		# Receive response 
		response = client_socket.recv(2048)
		response = response.decode()

		print(response)
		if(response == "Login Falied"):
			client_socket.close()
			return
			
		if client_socket: 
			while (vid.isOpened()):
				try:
					img, frame = vid.read()
					frame = imutils.resize(frame,width=380)
					a = pickle.dumps(frame)
					message = struct.pack("Q",len(a))+a
					client_socket.sendall(message)
					cv2.imshow(f"TO: {host_ip}",frame)
					key = cv2.waitKey(1) & 0xFF
					if key == ord("q"):
						client_socket.close()
				except:
					print('Video Finished!')
					break

	def stream(self):
		camera = True
		vid = cv2.VideoCapture(0)
		client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		ip = input("Enter The Desitnation IP: ")
		host_ip = ip
		port = 9999
		client_socket.connect((host_ip,port))

		response = client_socket.recv(2048)
		# Input UserName
		name = input(response.decode())	
		client_socket.send(str.encode(name))
		response = client_socket.recv(2048)
		# Input Password
		password = input(response.decode())	
		client_socket.send(str.encode(password))

		''' Response : Status of Connection :
			1 : Registeration successful 
			2 : Connection Successful
			3 : Login Failed
		'''
		# Receive response 
		response = client_socket.recv(2048)
		response = response.decode()

		print(response)

		if client_socket: 
			while (vid.isOpened()):
				try:
					img, frame = vid.read()
					frame = imutils.resize(frame,width=380)
					a = pickle.dumps(frame)
					message = struct.pack("Q",len(a))+a
					client_socket.sendall(message)
					cv2.imshow(f"TO: {host_ip}",frame)
					key = cv2.waitKey(1) & 0xFF
					if key == ord("q"):
						client_socket.close()
				except:
					print('Video Finished!')
					break

fire.Fire(Stream)