from ftplib import FTP

f=FTP('10.151.254.2')

print('welcome' + f.getwelcome())

f.login('bagus')
fd = open('dbir.pdf', 'wb')
f.retrbinary('RETR ' + 'dbir.pdf', fd.write, 1024)
fd.close()
f.quit()