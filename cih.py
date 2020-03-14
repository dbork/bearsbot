home = "./"

execfile(home + "wcards.py")
execfile(home + "bcards.py")

def cihSetup(host):
    players = [host]
    s.send("PRIVMSG %s :Cards Against Humanity \r\n" % CHAN)
    s.send("PRIVMSG %s :basically taken straight from the site \r\n" % CHAN)
    s.send("PRIVMSG %s :Host is %s. Type \"go\" to start. \r\n" % (CHAN, host))
    s.send("PRIVMSG %s :Waiting for more players... \r\n" % CHAN)

    readbuffer = ""
    
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
            elif 'PRIVMSG' in line:
                user = line[0].lstrip(':')
                user = user.split('!')[0]
                if (line[3] == ':\\play'):
                    players = players + [user]
                    current = ', '.join(players)
                    s.send("PRIVMSG %s :Players are %s \r\n" % (CHAN, current))
                elif (line[3] == ':quit') and user == host:
                    return
                elif (line[3] == ':go') and user == host:
                    cih(players)
                    return
