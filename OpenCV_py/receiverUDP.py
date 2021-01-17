
import socket
import numpy
from cv2 import cv2 as cv

UDP_IP = "127.0.0.1"        # receiver ip
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

s = [b'\xff' * 46080 for x in range(20)]

fourcc = cv.VideoWriter_fourcc(*'DIVX')
out = cv.VideoWriter('datas/videos/receiver_out.avi', fourcc, 25.0, (640, 480))

while True:
    picture = b''

    data, addr = sock.recvfrom(46081)
    s[data[0]] = data[1:46081]

    if data[0] == 19:
        for i in range(20):
            picture += s[i]

        frame = numpy.fromstring(picture, dtype=numpy.uint8)
        frame = frame.reshape(480, 640, 3)
        cv.imshow("frame", frame)
        out.write(frame)

        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break
