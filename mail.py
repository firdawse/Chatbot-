import smtplib


def sendmailWork ( first_name, last_name, type):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('firdawse.guerbouzi1@gmail.com','Password')
    subject = 'Administrative request'
    body = first_name + ' '+last_name + ' is asking for '+type
    msg = f'Subject:  {subject}\n\n{body}'
    server.sendmail('firdawse.guerbouzi1@gmail.com','firdawse.guerbouzi1@gmail.com' ,msg )
    print("login success")

def sendmailSalary ( first_name, last_name, type):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('firdawse.guerbouzi1@gmail.com','Password')
    subject = 'Administrative request'
    body = first_name + ' '+last_name + ' is asking for '+type
    msg = f'Subject:  {subject}\n\n{body}'
    server.sendmail('firdawse.guerbouzi1@gmail.com','firdawse.guerbouzi1@gmail.com' ,msg )
    print("login success")

def sendmailHoliday ( first_name, last_name, type):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login('firdawse.guerbouzi1@gmail.com','Password')
    subject = 'Administrative request'
    body = first_name + ' '+last_name + ' is asking for '+type
    msg = f'Subject:  {subject}\n\n{body}'
    server.sendmail('firdawse.guerbouzi1@gmail.com','firdawse.guerbouzi1@gmail.com' ,msg )
    print("login success")

