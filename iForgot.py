import pyrebase
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import datiFirebase
import os
from thread import *



config = datiFirebase.config

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(datiFirebase.mailGmail, datiFirebase.passwordGmail)



def sendMail(mailReceiver, code):
	msg = MIMEMultipart()
	msg['From'] = datiFirebase.mailGmail
	msg['To'] = mailReceiver
	msg['Subject'] = "Codice Don Bosco Studenti"
	
	body = "Ecco il codice di verifica per il cambio della password: " + str(code)
	msg.attach(MIMEText(body, 'plain'))
	
	text = msg.as_string()
#	try:
	server.sendmail(datiFirebase.mailGmail, mailReceiver, text)
#	except:
#		print("Error sending email")



def main(argv):
#	if (len(argv) < 2):
#		print("Usage: python iForgot.py [time to sleep]")
#		quit()
	

	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

	while True:
		allUsers = db.child("Utenti").get()
		for user in allUsers.each():
			if user.val()["iForgot"] == True and user.val()["iForgot_sent"] == False:
				mail = user.val()["E-Mail"]
				code = user.val()["Codice"]
				try:
					f = open(".testLog.txt", 'w')
				except:
					os.system("touch .testLog.txt")
					f = open(".testLog.txt", 'w')
				f.write(mail + " - " + str(code) + " - ")
				
				sendMail(mail, code)
				f.write("Mail inviata con successo\n\n")
				f.close()
				
				
				db.child("Utenti").child(user.val()["Username"]).child("iForgot_sent").set(True)
				time.sleep(2)
			else:
				pass	
		
		time.sleep(5)
			


			

if __name__ == "__main__":
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		print("\nRicevuto segnale di chiusura. Mi chiudo...")
		time.sleep(0.5)
		quit()
	except:
		print("Errore server. Ora aspetto 10 decondi e riprovo")
		time.sleep(10)
		main(sys.argv)
