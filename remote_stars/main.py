import numpy as np
import matplotlib.pyplot as plt
import socket

host = "84.237.21.36"
port = 5152

def recvall(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return
        data.extend(packet)
    return data

def square(im1, y, x):
    return im1[y-1:y+2, x-1:x+2].flatten()   
#flatten() возвращает копию массива, свернутого в одномерный

def find_pos(data):
    pos1, pos2 = None, None
    for y in range(1, data.shape[0] - 1):
        for x in range(1, data.shape[1] - 1):
            v = data[y, x]
            if v < 3: continue
            if any([n > v for n in square(data, y, x)]): 
                continue
            if pos1 is None: 
                pos1 = (x, y)
            elif pos2 is None: 
                pos2 = (x, y)
            else: break 
    return pos1, pos2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))

    for _ in range(10):
        sock.send(b"get")
        bts = recvall(sock, 40002)  # Получаем данные изображения
        im1 = np.frombuffer(bts[2:40002], dtype=np.uint8).reshape((200, 200))

        pos1, pos2 = find_pos(im1)

        distance = np.linalg.norm(np.array(pos1) - np.array(pos2))

        sock.send(f"{distance:.1f}".encode())  # Отправляем результат на сервер
        beat = sock.recv(20)  # Получаем информацию от сервера
        print(beat) 

