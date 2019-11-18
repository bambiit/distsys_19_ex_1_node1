import socket
import threading
from _datetime import datetime

from threading import Thread

#Class for getting return values of functions each thread runs.
class thread_rv(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    ##by running this join function, return value of the target function in thread can be obtained.
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


#This function deals with the customer request.
#It is run in a thread created at the most bottom code.
def deal_with_customer(client_socket, addr):

    time = str(datetime.now())+"\n"
    message = 'Connection created with ' + str(addr[0]) + ' : ' + str(addr[1])+"\n"
    print(time+message)
    #log_file.write(time+message)


    #receives data(price) from the socket connected with the client.
    price = client_socket.recv(4).decode()


    time = str(datetime.now())+"\n"
    message = 'received data(price) from client ' + str(addr[0]) + ' : ' + str(addr[1])+"\n"
    print(time+message)
    #log_file.write(time+message)


    #receives data(customer info) from the socket connected with the client.
    info_customer = client_socket.recv(1024).decode()

    name = info_customer.split(", ")[0]
    bank_account = info_customer.split(", ")[1]


    time = str(datetime.now())+"\n"
    message = 'received data(info of the customer) from client ' + str(addr[0]) + ' : ' + str(addr[1])+"\n"
    print(time+message)
    #log_file.write(time+message)


    if (len(str(bank_account)) == 18):

        #creates threads which call Node2 and Node3.
        thread1 = thread_rv(target=call_node2, args=(name, bank_account, price, ))
        thread2 = thread_rv(target=call_node3, args=(bank_account,))

        thread1.start()
        thread2.start()

        #Synchronization of threads. waits until both threads end.
        result1 = thread1.join()
        result2 = thread2.join()


        #sends the result to the client.
        if (result1 == 'OK'):
            if (result2 == 'OK'):
                client_socket.send("OK".encode())

                time = str(datetime.now()) + "\n"
                message = "Payment succeeded and send the result to the cleint <" + str(addr[0]) + ':' + str(addr[1]) + ">\n"
                print(time + message)
                #log_file.write(time + message)


            else:
                client_socket.send(str(result2).encode())

                time = str(datetime.now()) + "\n"
                message = "The client couldn't succeed to pay with this reason : " + str(result2) +"\n"
                print(time + message)
                #log_file.write(time + message)

        else:
            client_socket.send(str(result1).encode())

            time = str(datetime.now()) + "\n"
            message = "The client couldn't succeed to pay with this reason : " + str(result1) + "\n"
            print(time + message)
            #log_file.write(time + message)

    #sends the result to the client.
    else:
        client_socket.send("WRONG BANK ACCOUNT NUMBER".encode())

        time = str(datetime.now()) + "\n"
        message = "The client couldn't succeed to pay with this reason : WRONG BANK ACCOUNT NUMBER\n"
        print(time + message)
        #log_file.write(time + message)


#Communication with the Node2
def call_node2(name, bankaccount, amount):
    try:
        #connects with the Node2.
        sock_for_N2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_for_N2.connect(("localhost", 8002))

        time = str(datetime.now()) + "\n"
        message = "Node 2 connected\n"
        print(time + message)
        #log_file.write(time + message)


        #forwards requests to the Node2.
        sock_for_N2.send(str(bankaccount+"\n"+amount+name+"\n").encode())

        time = str(datetime.now()) + "\n"
        message = "Info sent to Node 2\n"
        print(time + message)
        #log_file.write(time + message)

    except:
        return ("SERVER ERROR FOR CHECKING YOUR INFO FROM BANK\n")

    else:
        data = sock_for_N2.recv(1024).decode()

        time = str(datetime.now()) + "\n"
        message = data
        print(time + message)
        #log_file.write(time + message)

        return message

#Communication with the Node3
def call_node3(bankaccount):
    try:
        #connects with the Node3.
        sock_for_N3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_for_N3.connect(("localhost", 8003))

        time = str(datetime.now()) + "\n"
        message = "Node 3 connected\n"
        print(time + message)
        #log_file.write(time + message)


        #forwards requests to the Node3.
        sock_for_N3.send(str(bankaccount).encode())

        time = str(datetime.now()) + "\n"
        message = "Info sent to Node 3\n"
        print(time + message)
        #log_file.write(time + message)

    except:
        return ("SERVER ERROR FOR CHECKING YOUR INFO FROM FRAUD DB\n")

    else:
        data = sock_for_N3.recv(1024).decode()

        time = str(datetime.now()) + "\n"
        message = data
        print(time + message)
        #log_file.write(time + message)

        return message



#creates a socket for connecting with clients.
socket_for_clients = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_for_clients.bind(("localhost", 8001))
socket_for_clients.listen()

#log_file = open("log.log", 'a')

time = str(datetime.now()) + "\n"
message = 'Server started.\n'
print(time + message)
#log_file.write(time + message)


#receives multiple clients with multithreads.
while True:
    client_socket, addr = socket_for_clients.accept()
    threading.Thread(target=deal_with_customer, args=(client_socket, addr)).start()



