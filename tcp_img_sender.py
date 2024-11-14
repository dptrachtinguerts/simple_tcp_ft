import socket
import PIL 
import struct
import time
import os

import PIL.ImageGrab

# Creating Client Socket 
if __name__ == '__main__': 
	# host = '10.1.1.140'
	host = '127.0.0.1'
	port = 24375

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.connect((host, port)) 
	file_name = "./tmp_img.png"

	while True: 
		try: 
			img = PIL.ImageGrab.grab()
			img.save(file_name)

			size = os.stat(file_name).st_size
			sock.send(struct.pack('!Q', size))

			bytes_sent = 0
			with open(file_name, "rb") as img_file:
				data = img_file.read(1024 if ((size - bytes_sent)//1024 != 0) else (size - bytes_sent))
				while data != b'': 
					bytes_sent += sock.send(data)
					data = img_file.read(1024 if ((size - bytes_sent)//1024 != 0) else (size - bytes_sent))

				img_file.close()

		except IOError: 
			print('could not fetch image') 