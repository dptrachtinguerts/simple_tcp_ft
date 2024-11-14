import socket 
import PIL
import PIL.Image
import struct
import cv2

if __name__ == '__main__': 
	# Defining Socket 
	host = ''
	port = 9200

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.bind((host, port)) 
	sock.listen(1)
	conn, _ = sock.accept() 

	packet_size = 1024

	while True:
		value = conn.recv(2)
		file_size = struct.unpack('!Q', value)[0]

		print("file size: ", file_size)

		with open("./output.png", 'wb') as img_file:
			received_bytes = 0
			while received_bytes < file_size:
				bytes_to_receive = packet_size if ((file_size - received_bytes)//packet_size != 0) else (file_size - received_bytes)
				data = conn.recv(bytes_to_receive)
				# assert(len(data) == bytes_to_receive)
				img_file.write(data)

			img_file.close()

		img = cv2.imread("./output.png")
		cv2.imshow("screen capture", img)
		key = cv2.waitKey(10)
		cv2.destroyAllWindows()

		if key == ord("q"):
			break