import pyrebase
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
import json
import datiFirebase



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
	try:
		server.sendmail(datiFirebase.mailGmail, mailReceiver, text)
	except:
		print("Error sending email")



def main(argv):
	if (len(argv) < 2):
		print("Usage: python iForgot.py [time to sleep]")
		quit()
	

	firebase = pyrebase.initialize_app(config)
	db = firebase.database()

	while True:
		allUsers = db.child("Utenti").get()
		for user in allUsers.each():
			if user.val()["iForgot"] == True and user.val()["iForgot_sent"] == False:
				mail = user.val()["E-Mail"]
				code = user.val()["Codice"]
				sendMail(mail, code)
				db.child("Utenti").child(user.val()["Username"]).child("iForgot_sent").set(True)
			else:
				pass	
		
		time.sleep(float(argv[1]))
			


			

if __name__ == "__main__":
	main(sys.argv)