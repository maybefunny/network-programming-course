from ftplib import FTP

f=FTP('10.151.254.2')

print('welcome' + f.getwelcome())

f.login('bagus')
print('cur dir: ' + f.pwd())
names = f.nlst()
print('list of dir: ' + str(names))
f.quit()