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
GREETING_INPUTS_FR = ("bonjour","bonsoir","cc","salut",)
THANKS_INPUTS = ("thank you", 'bye', "thanks","merci", "merci beacoup",)
ENDING_INPUTS = ("good bye", 'bye','by',)
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

# This function is used to indicate the 'aministrative request'  part 
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

# this fuction is used to switch from english to french  
def make_fr():
	 cursor = db.cursor()
	 sql = "INSERT INTO is_fr (num) VALUES (%s)"
	 cursor.execute(sql,1)
	 cursor.close()
	 db.commit()

# this fuction is used to switch from french to english  
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
		make_eng()

	elif (greetingFr(incoming_msg)):
		make_eng()
		make_fr()
		output = 'bonjour! '+'\U0001F603' + ' Je suis votre assistant virtuel'+ ' \nSVP ins??rer une photo de votre badge!'
		deleteId()
		makeFlase()

# if the card is inserted 
	elif(media_msg == '1'):
		 path = request.form.get('MediaUrl0')
		 result= recognize_text(path)
		 output = result[6][1]
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
			 output = output + '\nhow can I help you?\n1 - Absence\n2 - Administrative request\n3 - Vacation'
		 else :
			 insertId(output)
			 sql = "SELECT idcode FROM code "
			 cursor.execute(sql)
			 code = cursor.fetchone()
			 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
			 cursor.execute(sql,code[0])
			 x = cursor.fetchone()
			 output = 'Bonjour ' + str(x[0]) + ' ' + str(x[1]) 
			 output = output + '\nComment je peux vous aider?\n1 - Absence\n2 - Demande Administrative \n3 - Cong??'


	elif(incoming_msg.lower() in ENDING_INPUTS):
	 makeFlase()
	 deleteId()
	 if(is_Fr()):
		 output='bonne journ??e !'
	 else :
		 output = 'Good bye , have a good day'
	 make_eng()
	elif(incoming_msg.lower() in THANKS_INPUTS):
	 makeFlase()
	 if(is_Fr()):
		 output='avec plaisir '+'\U0001F60A'+'!'
	 else : 
		 output = 'With pleasure '+'\U0001F60A'+ '!'

	elif((response(incoming_msg)=='absence.' or incoming_msg == '1')and not isTrue()):
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

	elif((response(incoming_msg) == 'holiday vacation annual leave.' or incoming_msg == '3') and not isTrue()):
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
			 sql = "SELECT date , dur??e FROM cong?? WHERE id_emp =%s"
			 cursor.execute(sql,code[0])
			 x=cursor.fetchall()
			 for i in range(len(x)):
				 output = output + str(i+1) +'- Start date :' +str(x[i][0]).replace('((datetime.date(', '') + '    dur??e : '+ str(x[i][1]) + 'days\n'
			 cursor.close()

	elif((response(incoming_msg) == 'vacances cong?? annuel vacance conge cong??s.' or incoming_msg == '3')and not isTrue()):
		 output = ""
		 cursor = db.cursor()
		 makeFlase()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 if(code==None):
			 output = 'SVP entrez votre id'
		 else :
			 output = "Cong??s annuels :\n"
			 sql = "SELECT date , dur??e FROM cong?? WHERE id_emp =%s"
			 cursor.execute(sql,code[0])
			 x=cursor.fetchall()
			 for i in range(len(x)):
				 output = output + str(i+1) +'- Start date :' +str(x[i][0]).replace('((datetime.date(', '') + '    dur??e : '+ str(x[i][1]) + 'days\n'
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

	elif(response(incoming_msg)=='??tat des demandes etat.'):
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
				 output = output + '\n-' + str(x[i][0]) +'\t??tat : '+ str(x[i][1]) + '\tdate : '+ str(x[i][2]).replace('((datetime.date(', '')
			 cursor.close()

	elif((response(incoming_msg)=='administrative request.'or incoming_msg == '2')and codeExist() and not isTrue()):
		makeTrue()
		output = 'what type of request you are looking for :\n1-work certificate\n2-holiday certificate\n3-Salary report' 
	elif(isTrue() and codeExist() and not is_Fr()):
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
		 cursor.execute(sql,code)
		 x = cursor.fetchone()
		 if('salary report'in incoming_msg or incoming_msg == '3'):
			 sendmailSalary(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('work certificate'in incoming_msg or incoming_msg == '1'):
			 sendmailWork(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('holiday certificate'in incoming_msg or incoming_msg == '2'):
			 sendmailHoliday(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'your request has been considered successfully !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 else :
			 output = 'sorry ,I didnt understand which type of request you are looking for ! '
			 
		 cursor.close()

	elif((response(incoming_msg)=='effectuer une demande administrative.' or incoming_msg == '2')and codeExist() and not isTrue()):
		makeTrue()
		output = 'Quel type de demande cherchez vous :\n1-Certificat de travail\n2-Certificat de cong??\n3-Rapport de salaire' 
	elif(isTrue() and codeExist()):
		 cursor = db.cursor()
		 sql = "SELECT idcode FROM code "
		 cursor.execute(sql)
		 code = cursor.fetchone()
		 sql = "SELECT first_name,last_name  FROM employee WHERE Id =%s"
		 cursor.execute(sql,code)
		 x = cursor.fetchone()
		 if('certificat de travail'in incoming_msg or incoming_msg == '1'):
			 sendmailSalary(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a ??t?? bien prise en consid??ration !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('certificat de cong??'in incoming_msg.lower() or incoming_msg == '2'):
			 sendmailWork(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a ??t?? bien prise en consid??ration !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 elif('rapport de salaire'in incoming_msg.lower() or incoming_msg == '3'):
			 sendmailHoliday(str(x[0]),str(x[1]),incoming_msg) 
			 output = 'Votre demande a ??tait bien prise en consid??ration !'
			 insertDoc(code,incoming_msg)
			 makeFlase()
		 else :
			 output = 'Pouvez vous bien pr??cisez quel type de demande voulez vous SVP ? '
		 cursor.close()
	elif(not is_Fr()) :
			output = "I am sorry! I don't understand you , can you specify"
	else :
			output = "Pouvez vous pr??ciser SVP  "



	msg.body(str(output))
	return str(resp)

if __name__ == '__main__':
	app.run()
