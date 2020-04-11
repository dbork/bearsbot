# This is unused, but is a hack put in place to preserve patch stealth by
# making absolutely sure I remember to load the virtualenv before running uno
import ircmessage

import sys
import socket
import string
import random

HOST = "irc.rizon.net"
PORT = 6667
NICK = "BearsBot"
IDENT = "bearsbot"
REALNAME = "BearsBot"
CHAN = "#east"
readbuffer = ""
PW = "FelUpARl1"

s = socket.socket()
s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
#s.send("PRIVMSG %s :/msg NickServ IDENTIFY %s %s \r\n" % (CHAN, NICK, PW))
#s.send("PRIVMSG NickServ IDENTIFY %s %s" % (NICK, PW))

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
            # if bearsbot isn't joining and you're desperate, uncomment this
            s.send("JOIN %s\r\n" % CHAN)

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
                if (random.randint(1, 15) == 1):
                    greeting = "BearsBot slaps " + user + "" \
                               " around a bit with a large trout."
                    s.send("PRIVMSG %s :%s \r\n" % (CHAN, greeting))
            elif (random.randint(1, 60) == 1):
                quote = suggestions[random.randint(0, len(suggestions) - 1)]
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))                
            elif (random.randint(1, 120) == 1):
                quote = "GRAAH! A BEARS mauls you viciously!"
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))
            elif (random.randint(1, 60) == 1):
                quote = deepThoughts[random.randint(0, len(deepThoughts) - 1)]
                s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))

