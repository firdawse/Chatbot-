import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from flask_mysqldb import MySQL
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
import pymysql
from NLP import *
from mail import *
from trait_img import *
from datetime import date

db=pymysql.connect(host='localhost',user='root',password='Ihsan@123',database='ram')

app = Flask(__name__)
mysql = MySQL()
is_Fr="True"
mysql.init_app(app)
#code = None
# Keyword Matching
GREETING_INPUTS_ENG = ("hello", "hi", "greetings", "what's up","hey",)
GREETING_INPUTS_FR = ("bonjour","bonsoir","cc",)
THANKS_INPUTS = ("thank you", 'bye', "thanks","merci", "merci beacoup",)
ENDING_INPUTS = ("good bye", 'bye',)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greetingEng(sentence):
    """If user's input is a greeting, return a greeting response"""
    is_Fr='False'
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS_ENG:
            return True
    return False

def greetingFr(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS_FR:
            return True
    return False

def insertId(id):
	 cursor = db.cursor()
	 sql = "INSERT INTO code (idcode) VALUES (%s)"
	 cursor.execute(sql,str(id))
	 cursor.close()
	 db.commit()

def makeTrue():
	 cursor = db.cursor()
	 sql = "INSERT INTO bool (num) VALUES (%s)"
	 cursor.execute(sql,1)
	 cursor.close()
	 db.commit()

def makeFlase():
	 cursor = db.cursor()
	 sql = "DELETE FROM bool"
	 cursor.execute(sql)
	 cursor.close()
	 db.commit()

def isTrue():
	 cursor = db.cursor()
	 sql = "SELECT num FROM bool "
	 cursor.execute(sql)
	 code = cursor.fetchone()
	 if(code==None):
		 return False
	 else :
		 return True

def is_Fr():
	 cursor = db.cursor()
	 sql = "SELECT num FROM is_fr "
	 cursor.execute(sql)
	 code = cursor.fetchone()
	 if(code==None):
		 return False
	 else :
		 return True

def make_fr():
	 cursor = db.cursor()
	 sql = "INSERT INTO is_fr (num) VALUES (%s)"
	 cursor.execute(sql,1)
	 cursor.close()
	 db.commit()


def make_eng():
	 cursor = db.cursor()
	 sql = "DELETE FROM is_fr"
	 cursor.execute(sql)
	 cursor.close()
	 db.commit()

def codeExist():
	 cursor = db.cursor()
	 sql = "SELECT idcode FROM code"
	 cursor.execute(sql)
	 code = cursor.fetchone()
	 if(code==None):
		 return False
	 else :
		 return True

def insertDoc(id, type):
	 cursor = db.cursor()
	 sql = "INSERT INTO docs (idemp, state,type,date) VALUES (%s, %s, %s, %s)"
	 val = (id, "in process", type, date.today())
	 cursor.execute(sql, val)
	 cursor.close()
	 db.commit()

def deleteId():
	 cursor = db.cursor()
	 sql = "DELETE FROM code"
	 cursor.execute(sql)
	 cursor.close()
	 db.commit()

@app.route('/bot', methods=['POST'])
def bot():

	sender = request.form.get('From')
	media_msg = request.form.get('NumMedia')

	incoming_msg = request.values.get('Body', '').strip()

	resp = MessagingResponse()
	msg = resp.message()

	incoming_msg =incoming_msg.lower()

	if (greetingEng(incoming_msg)):
		output = 'hello '+'\U0001F603' + ' I am your bot assistant'+ ' \nPlease enter a picture of your card!'
		insertId('hi')
		deleteId()
		makeFlase()

	elif (greetingFr(incoming_msg)):
		make_fr()
		output = 'bonjour! '+'\U0001F603' + ' Je suis votre assistant virtuel'+ ' \nSVP insérer une photo de votre badge!'
		deleteId()
		makeFlase()

	elif(media_msg == '1'):
		 path = request.form.get('MediaUrl0')
		 result= recognize_text(path)
		 output = result[7][1]
		 makeFlase()
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code"
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code != None):
			 output = response(str(incoming_msg))
		 elif(not is_Fr()) :
			 insertId(output)
			 sql = "SELECT idcode FROM code "
			 cursor.execute(sql)
			 code = cursor.fetchone()
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'hi ' + str(x[0]) + ' ' + str(x[1]) 
			 output = output + '\nhow can I help you?'
		 else :
			 insertId(output)
			 sql = "SELECT idcode FROM code "
			 cursor.execute(sql)
			 code = cursor.fetchone()
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'Bonjour ' + str(x[0]) + ' ' + str(x[1]) 
			 output = output + '\nComment je peux vous aider?'


	elif(incoming_msg.lower() in ENDING_INPUTS):
	 makeFlase()
	 deleteId()
	 if(is_Fr()):
		 output='bonne journée !'
	 else :
		 output = 'Good bye , have a good day'
	 make_eng()

	elif(incoming_msg.lower() in THANKS_INPUTS):
	 makeFlase()
	 if(is_Fr()):
		 output='avec plaisir '+'\U0001F60A'+'!'
	 else : 
		 output = 'With pleasure '+'\U0001F60A'+ '!'


	elif('pdf' in incoming_msg):
		msg.media('http://www.africau.edu/images/default/sample.pdf')
		return str(resp)


	elif(response(incoming_msg)=='absence.'):
		 output = ""
		 cursor = db.cursor()
		 makeFlase()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'please enter your id'
		 else :
			 output = "Absences :\n"
			 sql = "SELECT date FROM absence WHERE idemployee =%s"
			 cursor.execute(sql,code[0])
			 x=cursor.fetchall()
			 for i in range(len(x)):
				 output = output + str(i+1) +'-  ' +str(x[i][0]).replace('((datetime.date(', '') + '\n'
			 cursor.close()

	elif(response(incoming_msg) == 'holiday vacation annual leave.'):
		 output = ""
		 cursor = db.cursor()
		 makeFlase()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'please enter your id'
		 else :
			 output = "List of holidays :\n"
			 sql = "SELECT date , durée FROM congé WHERE id_emp =%s"
			 cursor.execute(sql,code[0])
			 x=cursor.fetchall()
			 for i in range(len(x)):
				 output = output + str(i+1) +'- Start date :' +str(x[i][0]).replace('((datetime.date(', '') + '    durée : '+ str(x[i][1]) + 'days\n'
			 cursor.close()

	elif(response(incoming_msg) == 'vacances congé annuel vacance conge.'):
		 output = ""
		 cursor = db.cursor()
		 makeFlase()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'SVP entrez votre id'
		 else :
			 output = "Congés annuels :\n"
			 sql = "SELECT date , durée FROM congé WHERE id_emp =%s"
			 cursor.execute(sql,code[0])
			 x=cursor.fetchall()
			 for i in range(len(x)):
				 output = output + str(i+1) +'- Start date :' +str(x[i][0]).replace('((datetime.date(', '') + '    durée : '+ str(x[i][1]) + 'days\n'
			 cursor.close()

	elif(response(incoming_msg)=='state of administrative request.'):
		 makeFlase()
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'please enter your id'
		 else :
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'here are your requests :'
			 sql = "SELECT type, state, date FROM docs WHERE idemp =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchall()
			 for i in range(len(x)):
				 output = output + '\n-' + str(x[i][0]) +'\tstate : '+ str(x[i][1]) + '\tdate : '+ str(x[i][2]).replace('((datetime.date(', '')
			 cursor.close()

	elif(response(incoming_msg)=='état des demandes etat.'):
		 makeFlase()
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'please enter your id'
		 else :
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'Historiques de vos demandes :'
			 sql = "SELECT type, state, date FROM docs WHERE idemp =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchall()
			 for i in range(len(x)):
				 output = output + '\n-' + str(x[i][0]) +'\tétat : '+ str(x[i][1]) + '\tdate : '+ str(x[i][2]).replace('((datetime.date(', '')
			 cursor.close()

	elif(response(incoming_msg)=='administrative request.'and codeExist()):
		makeTrue()
		output = 'what type of request you are looking for :\n-work certificate\n-holiday certificate\n-Salary report' 
	elif(isTrue() and codeExist() and not is_Fr()):
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
		 cursor.execute(sql,code)
		 x = cursor.fetchone()
		 if('salary report'in incoming_msg):
			 sendmailSalary(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('work certificate'in incoming_msg):
			 sendmailWork(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('holiday certificate'in incoming_msg):
			 sendmailHoliday(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 else :
			 output = 'sorry ,I didnt understand which type of request you are looking for ! '
			 
		 cursor.close()

	elif(response(incoming_msg)=='effectuer une demande administrative.'and codeExist()):
		makeTrue()
		output = 'Quel type de demande cherchez vous :\n-Certificat de travail\n-Certificat de congé\n-Rapport de salaire' 
	elif(isTrue() and codeExist()):
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
		 cursor.execute(sql,code)
		 x = cursor.fetchone()
		 if('certificat de travail'in incoming_msg):
			 sendmailSalary(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a été bien prise en considération !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('certificat de congé'in incoming_msg.lower()):
			 sendmailWork(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a été bien prise en considération !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('rapport de salaire'in incoming_msg.lower()):
			 sendmailHoliday(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a était bien prise en considération !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 else :
			 output = 'Pouvez vous bien précisez quel type de demande voulez vous SVP ? '
			 
		 cursor.close()

	else:
		 makeFlase()
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code"
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code != None):
			 output = response(str(incoming_msg))
		 elif(not is_Fr()) :
			 insertId(incoming_msg)
			 sql = "SELECT idcode FROM code "
			 cursor.execute(sql)
			 code = cursor.fetchone()
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'hi ' + str(x[0]) + ' ' + str(x[1]) 
			 output = output + '\nhow can I help you?'
		 else :
			 insertId(incoming_msg)
			 sql = "SELECT idcode FROM code "
			 cursor.execute(sql)
			 code = cursor.fetchone()
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'Bonjour ' + str(x[0]) + ' ' + str(x[1]) 
			 output = output + '\nComment je peux vous aider?'

	msg.body(str(output))
	return str(resp)

if __name__ == '__main__':
	app.run()
