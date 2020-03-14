import sys
import socket
import string
import random
import time

#HOST = "irc.foonetic.net"
HOST = "irc.rizon.net"
PORT = 6667
NICK = "BearsBot"
PASS = "fistsofrage"
IDENT = "BearsBot"
REALNAME = "BearsBot"
#CHAN = "#pctyd"
CHAN = "#east"
PW = "axolotl"
EMAIL = "dbork@g.hmc.edu"
readbuffer = ""

s = socket.socket()
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))

for i in range(3):
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        print line

        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])


s.send("PRIVMSG NickServ :IDENTIFY %s\r\n" % PW)
#s.send("PRIVMSG nickserv IDENTIFY axolotl")
s.send("JOIN %s %s\r\n" % (CHAN, PASS))
#s.send("PASS %s\r\n" % PASS)
# s.send("PRIVMSG nickserv REGISTER %s %s" % (PW, EMAIL))

home = "./"
execfile(home + "quotes.py")
execfile(home + "libeary.py")

while 1:
    readbuffer = readbuffer + s.recv(1024)
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        line = string.rstrip(line)
        line = string.split(line)
        print line

        if (line[0] == "PING"):
            s.send("PONG %s\r\n" % line[1])

        if 'JOIN' in line:
            user = line[0].lstrip(':')
            user = user.split('!')[0]
            if (user[0:6] == 'Indigo'):
                greeting = "Hello, " + user + " the EveryTime!"
            else:
                greeting = "Hello, " + user + " the BEARS!"
            s.send("PRIVMSG %s :%s \r\n" % (CHAN, greeting))
            
        if 'PRIVMSG' in line:
            user = line[0].lstrip(':')
            user = user.split('!')[0]
            if (line[3] == ':\\play'):
                games(line)
            elif bearSearch(line):
                if (user[0:6] == 'Indigo'):
                    greeting = "Hello, " + user + " the EveryTime!"
                else:
                    greeting = "Hello, " + user + " the BEARS!"
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, greeting))
            elif (user == "Purplatypus"):
                if (random.randint(1, 30) == 1):
                    greeting = "/me slaps" + user + "" \
                               " around a bit with a large trout."
                    s.send("PRIVMSG %s :%s \r\n" % (CHAN, greeting))
            elif (random.randint(1, 120) == 1):
                quote = suggestions[random.randint(0, len(suggestions) - 1)]
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))                
            elif (random.randint(1, 240) == 1):
                quote = "GRAAH! A BEARS mauls you viciously!"
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))
            elif (random.randint(1, 60) == 1):
                quote = deepThoughts[random.randint(0, len(deepThoughts) - 1)]
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))

