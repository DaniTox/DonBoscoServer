import requests
import time
import hashlib
import requests
import sys


link = "http://www.donboscobrescia.it/file/orario.pdf"  


def main(argv):
    try:
        asd = open("/etc/checkOrarioPdf/md5save.txt", 'r')
        md5Attuale = asd.read()
        asd.close()
    except:
        print("Errore, il file non esiste")
        md5Attuale = ""

    while True:
        response = requests.get(link)
        with open("/tmp/orario.pdf", 'wb') as f:
            f.write(response.content)
            f.close()
            print("Orario.pdf scaricato.") 
            print("Calcolando md5...")
            md5generato = hashlib.md5(open("/tmp/orario.pdf", 'rb').read()).hexdigest()
            print("md5 calcolato = " + md5generato)
            if not(md5generato == md5Attuale):
                md5Attuale = md5generato
                print("md5 diverso. Mando notifica...")
                a = open("/etc/checkOrarioPdf/md5save.txt", 'w')
                a.write(md5Attuale)
                time.sleep(10)
            else:
                print("md5 uguali. L'orario non e stato cambiato")
                time.sleep(10)
        

if __name__ == "__main__":
    main(sys.argv)
