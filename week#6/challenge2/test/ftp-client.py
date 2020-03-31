from ftplib import FTP
from zipfile import ZipFile
import getpass
import os

user = input('username: ')
pswd = getpass.getpass('password: ')
addr = input('ipaddr: ')

f = FTP(addr)
f.login(user, pswd)

while(1):
    command = input('>> ')
    command = command.split(' ')
    if(command[0] == 'dl'):
        fd = open(command[1], 'wb')
        f.retrbinary('RETR ' + command[1], fd.write, 1024)
        fd.close()
    elif(command[0] == 'up'):
        fd = open(command[1], 'rb')
        f.storbinary('STOR ' + command[1], fd, 1024)
    elif(command[0] == 'ls'):
        print('list: ' + str(f.nlst()))
    elif(command[0] == 'mkdir'):
        try:
            f.mkd(command[1])
        except:
            print('failed to make directory.')
    elif(command[0] == 'pwd'):
        print('current directory: ' + f.pwd())
    elif(command[0] == 'cwd'):
        try:
            f.cwd(command[1])
            print('current directory: ' + f.pwd())
        except:
            print('failed to change directory.')
    elif(command[0] == 'UPTRACT'):
        os.mkdir(command[1][:-4])
        os.chdir(command[1][:-4])
        fd = ZipFile(command[1], 'r')
        fd.extractall()
        for root, dirs, files in os.walk('.', topdown=True):
            for name in files:
                print(os.path.join(root, name))
                fd = open (os.path.join(root, name), 'rb')
                f.storbinary('STOR ' + os.path.join(root, name), fd, 1024)
            for name in dirs:
                print(os.path.join(root, name))
                f.mkd(os.path.join(root, name))
    elif(command[0] == 'quit'):
        f.quit()
        exit(0)
