import smtplib
import time
import imaplib
import email
import sys, os

def clear(): 
    if os.name == 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear') 

orgEmail = "@gmail.com"
fromEmail = "bisapekok" + orgEmail
fromPWD = "rahasia"
smtpServer = "imap.gmail.com"
smtpPort = 933

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(fromEmail, fromPWD)

inbox = []

# def fetchEmails():
try:
    mail = imaplib  .IMAP4_SSL(smtpServer)
    mail.login(fromEmail, fromPWD)
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    mailIds = data[0]
    idList = mailIds.split()
    firstEmailId = int(idList[0])
    lastEmailId = int(idList[-1])

    print(len(data[0].split()))

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        inbox.append(msg)
except Exception as e:
    print(str(e))

inboxSize = len(inbox)
page = 0
while(1):
    clear()
    print("id\tfrom\tsubject")
    i=1
    for mail in inbox[page*20:(page+1)*20]:
        print(str(page*20+i)+"\t"+mail['from']+"\t"+mail['subject'])
        i+=1
    print("\n\n\n\n\nN:next;\tB:back;\t[index]:read mail")
    ch = input(">> ")
    if(ch == 'n' or ch == 'N'):
        if((page+1)*20>inboxSize):
            continue
        page += 1
    elif(ch == 'b' or ch == 'B'):
        if(page-1<0):
            continue
        page -= 1
    else:
        try:
            id = int(ch) - 1
            clear()
            print("From: "+inbox[id]['from'])
            print("Subject: "+inbox[id]['subject'])
            print('Body:')
            if inbox[id].is_multipart():
                for part in inbox[id].get_payload():
                    payload = part.get_payload(decode=True) #returns a bytes object
                    strtext = payload.decode() #utf-8 is default
                    print(strtext)
            else:
                payload = inbox[id].get_payload(decode=True)
                strtext = payload.decode()
                print(strtext)
            print("\n\n\n\n\nR:reply;\tF:Forward;\tB:back")
            ch = input(">> ")
            if(ch == "R" or ch == "r"):
                emailTo = inbox[id]['from']
                emailBody = input("Message:\n")
                server.sendmail(fromEmail, emailTo, emailBody)
            elif(ch == "F" or ch == "f"):
                emailTo = input("To: ")
                inbox[id].replace_header("From", fromEmail)
                inbox[id].replace_header("To", emailTo)
                server.sendmail(fromEmail, emailTo, inbox[id].as_string())
            else:
                continue
        except Exception as e:
            print(str(e))