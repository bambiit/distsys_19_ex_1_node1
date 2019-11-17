import socket
import threading

from threading import Thread

## class for getting return values of functions each thread runs
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)
    ##by running this join function, return value of the target function can be obtained.
    def join(self, *args):
        Thread.join(self, *args)
        return self._return



def deal_with_customer(client_socket, addr):


    print('Connection created with :', addr[0], ':', addr[1])
    print('Waiting request from the client.')

    price = client_socket.recv(1024).decode()

    info_customer = client_socket.recv(1024).decode()
    name = info_customer.split(", ")[0]
    bank_account = info_customer.split(", ")[1]


    if (len(str(bank_account)) == 18):

        thread1 = ThreadWithReturnValue(target=call_node2, args=(name, bank_account, price, ))
        thread2 = ThreadWithReturnValue(target=call_node3, args=(bank_account,))

        thread1.start()
        thread2.start()

        result1 = thread1.join()
        result2 = thread2.join()

        if (result1 == 'OK'):
            if (result2 == 'OK'):
                print("Payment succeeded and send the result to the cleint <" + addr[0] + ':' + addr[1] + ">")
                client_socket.send("OK".encode())
            else:
                print("The client couldn't succeed to pay with this reason : " + result2)
                client_socket.send(str(result2).encode())
        else:
            print("The client couldn't succeed to pay with this reason : " + result1)
            client_socket.send(str(result1).encode())


    else:
        print("The client couldn't succeed to pay with this reason : WRONG BANK ACCOUNT NUMBER")
        client_socket.send("WRONG BANK ACCOUNT NUMBER".encode())



def call_node2(name, bankaccount, amount):
    sock_for_N2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N2.connect(("localhost", 8002))
    print("Node 2 connected")
    sock_for_N2.send(str(name+", "+bankaccount+", "+amount).encode())
    print("Info sent to Node 2")
    
    return sock_for_N2.recv(1024).decode()




def call_node3(bankaccount):
    sock_for_N3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_for_N3.connect(("localhost", 8003))
    print("Node 3 connected")
    sock_for_N3.send(bytes(bankaccount, "utf-8"))
    print("Info sent to Node 3")

    return sock_for_N3.recv(1024).decode()






socket_for_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_for_clients.bind(("localhost", 8001))
socket_for_clients.listen()


while True:
    print('Waiting connction from a client.')
    client_socket, addr = socket_for_clients.accept()
    threading.Thread(target=deal_with_customer, args=(client_socket, addr)).start()



