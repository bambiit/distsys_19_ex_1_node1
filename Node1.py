import socket
from _thread import *


def deal_with_customer(client_socket, addr):

    print('Connection created with :', addr[0], ':', addr[1])
    print('Waiting request from the client.')
    data = client_socket.recv(1024)


    if (data.decode() == "Payment Request"):
        start_new_thread(call_node1())
        start_new_thread(call_node2())




def call_node1():
    sock_for_N2.send("something")
    sock_for_N2.recv(1024)


def call_node2():
    sock_for_N3.send("something")
    sock_for_N3.recv(1024)


socket_for_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_for_clients.bind(("localhost", 8000))
socket_for_clients.listen()

sock_for_N2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_for_N2.connect(("localhost", 8001))

sock_for_N3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_for_N3.connect(("localhost", 8002))


while True:
    print('Waiting connction from a client.')
    client_socket, addr = socket_for_clients.accept()

    start_new_thread(deal_with_customer(client_socket, addr))


