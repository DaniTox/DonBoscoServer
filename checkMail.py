import socket
import sys
from thread import *
from validate_email import validate_email
import datiFirebase

HOST = datiFirebase.HOST
PORT = datiFirebase.PORT

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket creato")

    try:
	   s.bind((HOST, PORT))
    except socket.error as msg:
	   print("Failed. Error Code: " + str(msg[0]) + msg[1])
	   sys.exit()

    print "Socket Bind Completato"

    s.listen(5)
    print("Il Socket sta ascoltando...")

    def clientthread(conn): 
        data = conn.recv(1024)
        print(data)

        if data == "ping\n":
            reply = "True\n"
        else:
            is_valid = validate_email(data,verify=True)
            reply = is_valid
        
        with open(".mail.log", 'w') as f:
            f.write("\n\nData ricevuto: " + data +  "Risposta: " + str(reply))

        conn.sendall(str(reply))
        conn.close()
 
    while 1:
        conn, addr = s.accept()
        print 'Connesso con ' + addr[0] + ':' + str(addr[1])
     
        start_new_thread(clientthread ,(conn,))
 
    s.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMi chiudo...\n")
