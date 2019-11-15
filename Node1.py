import socket
import _thread
import time


def deal_with_customer(client_socket, addr):

    print('Connection created with :', addr[0], ':', addr[1])
    print('Waiting request from the client.')

    price = client_socket.recv(1024)
    info_customer = data.decode().split()
    


    if (data.decode() == "Payment Request"):
        _thread.start_new_thread(call_node2())
        _thread.start_new_thread(call_node3())

        ##something for synchronization


        if (OK):
            client_socket.send(something)
        elif (not OK):
            client_socket.send(something)




def call_node2():
    sock_for_N2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N2.connect(("localhost", 8001))

    sock_for_N2.send("something_to_Node2")
    sock_for_N2.recv(1024)



def call_node3():
    sock_for_N3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N3.connect(("localhost", 8002))

    sock_for_N3.send("something_to_Node3")
    sock_for_N3.recv(1024)






socket_for_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_for_clients.bind(("localhost", 8000))
socket_for_clients.listen()


while True:
    print('Waiting connction from a client.')
    client_socket, addr = socket_for_clients.accept()
    _thread.start_new_thread(deal_with_customer, (client_socket, addr))


