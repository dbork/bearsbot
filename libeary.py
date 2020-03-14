home = "./"
execfile(home + "uno.py")
execfile(home + "cih.py")

def bearSearch(line):
    for word in line:
        if "bearsbot" in word.lower():
            return True
    return False

def hangBEARS(players, hard):
    while 1:
        if hard == 1:
            #f = open('/usr/share/dict/words') # hard mode starts here
            f = open('./words')
            words = f.read().splitlines() 
            word = list(words[random.randint(0, len(words) - 1)].upper())
            f.close() # and ends here
        else:
            word = list(hangBEARSlib[random.randint(0, len(hangBEARSlib) - 1)])
    
        known = ""
        for i in word:
            known = known + "_"
        known = list(known)
        roster = ', '.join(players)
        s.send("PRIVMSG %s :Players are %s \r\n" % (CHAN, roster))
        s.send("PRIVMSG %s :The word is %s \r\n" % (CHAN, ' '.join(known)))
        s.send("PRIVMSG %s :%s's guess? \r\n" % (CHAN, players[0]))

        guesses = []
        wrong = 0
    
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
                    guess = line[3].lstrip(':').upper()

                    if guess == "QUIT":
                        return
                
                    if user == players[0] and len(guess) == 1 and guess.isalpha():
                        if guess in guesses:
                            s.send("PRIVMSG %s :That has already been guessed " \
                               "\r\n" % CHAN)
                        else:
                            guesses = guesses + [guess]
                            if guess in word:
                                for i in range(len(word)):
                                    if word[i] == guess:
                                        known[i] = guess
                                s.send("PRIVMSG %s :CORRECT \r\n" % CHAN)
                                s.send("PRIVMSG %s :The word is %s " \
                                   "\r\n" % (CHAN, ' '.join(known)))
                                if word == known:
                                    s.send("PRIVMSG %s :GRAAH! You win! The " \
                                       "bear escapes and mauls several!" \
                                       " \r\n" % CHAN)
                                    return
                                s.send("PRIVMSG %s :Guesses so far are " \
                                   "%s \r\n" % (CHAN, ', '.join(guesses)))
                            else:
                                wrong = wrong + 1
                                s.send("PRIVMSG %s :INCORRECT \r\n" % CHAN)
                                s.send("PRIVMSG %s :The word is %s " \
                                   "\r\n" % (CHAN, ' '.join(known)))
                                s.send("PRIVMSG %s :Guesses so far are " \
                                   "%s \r\n" % (CHAN, ', '.join(guesses)))
                                s.send("PRIVMSG %s :Wrong guesses: %d" \
                                   " \r\n" % (CHAN, wrong))
                                if wrong == 8:
                                    s.send("PRIVMSG %s :GRAAH! You lose! The " \
                                       "bear is hung :( but thankfully not "\
                                       "before mauling everyone! \r\n" % CHAN)
                                    s.send("PRIVMSG %s :The word was " % CHAN + ""\
                                       "" + "".join(word) + ". \r\n")
                                    return

                            players = players[1:] + [players[0]]
                            s.send("PRIVMSG %s :%s's guess? " \
                               "\r\n" % (CHAN, players[0]))
                        

def hbSetup(host):
    players = [host]
    s.send("PRIVMSG %s :HangBEARS ver. 2.0 \r\n" % CHAN)
    s.send("PRIVMSG %s :by C. Olin, P. Davis, Z. Vavok \r\n" % CHAN)
    s.send("PRIVMSG %s :Host is %s. Type \"go\" to start. Type \"hard\" for hard mode. Type \"quit\" to quit. \r\n" % (CHAN, host))
    s.send("PRIVMSG %s :Waiting for more players... \r\n" % CHAN)

    readbuffer = ""
    hard = 0
    
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
                elif (line[3] == ':hard'):
                    hard = 1
                    s.send("PRIVMSG %s :Hard mode engaged. \r\n" % CHAN)
                elif (line[3] == ':go'):
                    hangBEARS(players, hard)
                    return

def games(line):
    host = line[0].lstrip(':')
    host = user.split('!')[0]
    if (len(line) <= 4):
        return
    if (line[4].lower() == 'hangbears'):
        hbSetup(host)
    if (line[4].lower() == 'unobears'):
        unoSetup(host)
    if (line[4].lower() == 'cih'):
        cihSetup(host)
    return
