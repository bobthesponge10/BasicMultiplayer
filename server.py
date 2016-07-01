import socket
import time
connections = []
s = socket.socket()
host = input("Ip to use: ")
print(host)
port = 10000
s.bind((host, port))

done1 = False
done2 = False

x = "200".encode()
y = "200".encode()

x1 = "400".encode()
y1 = "400".encode()

s.listen(5)

while not done1:
    c, addr = s.accept()
    print('Got connection from', addr)
    connections.append(c)
    if len(connections) == 2:
        done1 = True
    for i in connections:
        i.send("0".encode())
print(connections)

for i in connections:
    i.send("1".encode())
    print(i)

time.sleep(5)

connections[0].send(x)
connections[0].recv(1024)
connections[0].send(y)
connections[0].recv(1024)
connections[1].send(x1)
connections[1].recv(1024)
connections[1].send(y1)
connections[1].recv(1024)

print("test")

while not done2:

        connections[1].send(x)
        x1 = connections[1].recv(1024)
        connections[1].send(y)
        y1 = connections[1].recv(1024)
        print("First")
        connections[0].send(x1)
        x = connections[0].recv(1024)
        connections[0].send(y1)
        y = connections[0].recv(1024)
        print(x, y, x1, y1)
for i in connections:
    i.close()
