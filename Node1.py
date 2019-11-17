import socket
import threading
from multiprocessing.pool import ThreadPool




def deal_with_customer(client_socket, addr):

    print('Connection created with :', addr[0], ':', addr[1])
    print('Waiting request from the client.')

    price = client_socket.recv(1024).decode()

    info_customer = client_socket.recv(1024).decode()
    name = info_customer.split(", ")[0]
    bank_account = info_customer.split(", ")[1]

    pool = ThreadPool(processes=1)

    if (len(str(bank_account)) == 18):
        async_thread1_result = pool.apply_async(call_node2, (name, bank_account))
        async_thread2_result = pool.apply_async(call_node3, (name, bank_account))

        print("Node1 called other two nodes.")

        if(async_thread1_result.get() == 'OK'):
            if(async_thread1_result.get() == 'OK'):
                client_socket.send("OK".encode())
            else:
                client_socket.send(async_thread2_result.get())
        else:
            client_socket.send(async_thread2_result.get())
    else:
        print("Wrong bank account number")
        client_socket.send("Wrong bank account number".encode())



def call_node2(name, bankaccount):
    sock_for_N2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N2.connect(("localhost", 8002))
    print("Node 2 connected")

    sock_for_N2.send()
    return sock_for_N2.recv(1024).decode()




def call_node3(name, bankaccount):
    sock_for_N3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N3.connect(("localhost", 8003))
    print("Node 3 connected")

    sock_for_N3.send(bytes(bankaccount, "utf-8"))
    return sock_for_N3.recv(1024).decode()






socket_for_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_for_clients.bind(("localhost", 8001))
socket_for_clients.listen()


while True:
    print('Waiting connction from a client.')
    client_socket, addr = socket_for_clients.accept()
    threading.Thread(target=deal_with_customer, args=(client_socket, addr)).start()



