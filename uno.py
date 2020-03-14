import time

def draw(luck):
    default = unoBEARSdeck
    if luck[0] > 4:
        return luckPlusThree[random.randint(0, len(luckPlusThree) - 1)]
    elif luck[0] > 2:
        return luckPlusTwo[random.randint(0, len(luckPlusTwo) - 1)]
    elif luck[0] > 0:
        return luckPlusOne[random.randint(0, len(luckPlusOne) - 1)]
    elif luck[0] > -1:
        return default[random.randint(0, len(default) - 1)]
    elif luck[0] > -2:
        return luckMinusOne[random.randint(0, len(luckMinusOne) - 1)]
    else:
        return luckMinusTwo[random.randint(0, len(luckMinusTwo) - 1)]

def stripCard(card):
    return card.split('\x03')[1][5:]

def cardInHand(move, hand):
    for i in range(len(hand)):
        if stripCard(hand[i]).lower() == move:
            return i
    return -1

def stateColor(color):
    c = ""
    if color == 'r':
        c = "\x0301,04red\x03"
    if color == 'b':
        c = "\x0301,11blue\x03"
    if color == 'g':
        c = "\x0301,09green\x03"
    if color == 'y':
        c = "\x0301,08yellow\x03"
    if color == 'k':
        c = "\x0300,01black\x03"
    if color == 'p':
        c = "\x0300,06purple\x03"
    if color == 'w':
        c = "\x0300,14wild\x03"
    s.send("PRIVMSG %s :The current color is %s. \r\n" % (CHAN, c))

def stateFalseColor(color):
    c = ""
    if color == 'r':
        c = "\x0301,04red\x03"
    if color == 'b':
        c = "\x0301,11blue\x03"
    if color == 'g':
        c = "\x0301,09green\x03"
    if color == 'y':
        c = "\x0301,08yellow\x03"
    if color == 'k':
        c = "\x0300,01black\x03"
    if color == 'p':
        c = "\x0300,06purple\x03"
    if color == 'w':
        c = "\x0300,14wild\x03"
    s.send("PRIVMSG %s :The current false color is %s. \r\n" % (CHAN, c))

def stateHandSizes(players, handlist):
    s.send("PRIVMSG %s :Hand sizes are: \r\n" % CHAN)
    for i in range(len(players)):
        s.send("PRIVMSG %s :%s: %d cards " \
               "\r\n" % (CHAN, players[i], len(handlist[i])))

def colorChoice(chooser):
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
                choice = line[3].lstrip(':').lower()
                if user == chooser:
                    if choice == 'red' or choice == 'r':
                        return 'r'
                    if choice == 'blue' or choice == 'b':
                        return 'b'
                    if choice == 'green' or choice == 'g':
                        return 'g'
                    if choice == 'yellow' or choice == 'y':
                        return 'y'
                    if choice == 'black' or choice == 'k':
                        return 'k'
                    if choice == 'purple' or choice == 'p':
                        return 'p'
                    if choice == 'wild' or choice == 'w':
                        return 'w'    

def wincon(players, handlist):
    if len(handlist[0]) == 0:
        s.send("PRIVMSG %s :%s has won the game! They are eaten by " \
               "bears as congratulations! \r\n" % (CHAN, players[0]))
        return True
    return False

def chooseOne(handlist, players):
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
                move = line[3].lstrip(':').lower()
                cardloc = cardInHand(move, handlist[0])
                if user == players[0] and cardloc + 1:
                    return cardloc

def isAggressive(move):
    if move[:-1] == "bears" or move[:-1] == "d2" \
        or move[:-1] == "d3" or move[:-1] == "d4i" \
        or move[:-1] == "wht" or move[:-1] == "ccd" \
        or move[:-1] == "dre" or move[:-1] == "ou" \
        or move[:-1] == "wow" or move[:-1] == "d4" \
        or move[:-1] == "dbl" or move[:-1] == "ntrl" \
        or move[:-1] == "drde" or move[:-1] == "luv" \
        or move[:-1] == "grr" or move[:-1] == "her":
        return True
    return False
    
def selfPenalize(handlist, players):
    s.send("PRIVMSG %s :String together a penalty to apply to yourself. " \
           "The first card can be anything offensive. Type done when" \
           " finished.\r\n" % CHAN)
    selfPen = []
    last = ""
    falseColor = 'p'
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
                move = line[3].lstrip(':').lower()
                cardloc = cardInHand(move, handlist[0])
                if move == "done":
                    return selfPen
                if user == players[0] and cardloc + 1:
                    if move[:-1] == "exe":
                        s.send("PRIVMSG %s :Play an additional card."
                               "\r\n" % CHAN)
                        falseColor = 'p'
                    elif isAggressive(move) or move[:-1] == "bpl" \
                       or move[:-1] == "shld" or move[:-1] == "th" \
                       or move[:-1] == "frst":

                        if move[-1:] == 'w':
                            last = handlist[0][cardloc]
                            handlist[0] = handlist[0][0:cardloc] + \
                                          handlist[0][cardloc + 1:]
                            s.send("PRIVMSG %s :Choose the false color." \
                                   " \r\n" % CHAN)
                            falseColor = colorChoice(user)

                            if move[:-1] != "shld":
                                selfPen = selfPen + [last]

                            if move[:-1] == "frst":
                                if wincon(players, handlist):
                                    return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty

                                s.send("PRIVMSG %s :Choose one additional " \
                                       "discard \r\n" % CHAN)
                                suppLoc = chooseOne(handlist, players)
                                handlist[0] = handlist[0][0:suppLoc] + handlist[0][suppLoc + 1:]
                                selfPen = selfPen + [handlist[0][suppLoc]]

                            if move[:-1] == "th":
                                selfPen = selfPen + [players[0]]

                            if move[:-1] == "shld":
                                s.send("PRIVMSG %s :%s's shield deflected the"\
                                       " penalty! \r\n" % (CHAN, players[0]))

                                
                            s.send("PRIVMSG %s :Self-penalty is %s " \
                                   "\r\n" % (CHAN, ' '.join(selfPen)))
                            if wincon(players, handlist):
                                return ["ocanada"]
                            shownHand = handlist[0]
                            shownHand = ' '.join(shownHand)
                            stateFalseColor(falseColor)
                            s.send("PRIVMSG %s :Your hand is %s " \
                                   "\r\n" % (players[0], shownHand))
                            s.send("PRIVMSG %s :%s, what is your next card? " \
                                   "\r\n" % (CHAN, players[0]))


                        elif move[-1:] == falseColor or falseColor == 'p' or \
                           move[:-1] == stripCard(last)[:-1].lower():
                            last = handlist[0][cardloc]
                            handlist[0] = handlist[0][0:cardloc] + \
                                          handlist[0][cardloc + 1:]
                            falseColor = move[-1]
                            if move[:-1] != "shld":
                                selfPen = selfPen + [last]

                            if move[:-1] == "frst":
                                if wincon(players, handlist):
                                    return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty

                                s.send("PRIVMSG %s :Choose one additional " \
                                       "discard \r\n" % CHAN)
                                suppLoc = chooseOne(handlist, players)
                                selfPen = selfPen + [handlist[0][suppLoc]]

                            if move[:-1] == "th":
                                selfPen = selfPen + [players[0]]

                            if move[:-1] == "shld":
                                s.send("PRIVMSG %s :%s's shield deflected the"\
                                       " penalty! \r\n" % (CHAN, players[0]))

                                
                            s.send("PRIVMSG %s :Self-penalty is %s " \
                                   "\r\n" % (CHAN, ' '.join(selfPen)))
                            if wincon(players, handlist):
                                return ["ocanada"]
                            shownHand = handlist[0]
                            shownHand = ' '.join(shownHand)
                            stateFalseColor(falseColor)
                            s.send("PRIVMSG %s :Your hand is %s " \
                                   "\r\n" % (players[0], shownHand))
                            s.send("PRIVMSG %s :%s, what is your next card? " \
                                   "\r\n" % (CHAN, players[0]))

                        elif move[-1:] == 'p':
                            last = handlist[0][cardloc]
                            handlist[0] = handlist[0][0:cardloc] + \
                                          handlist[0][cardloc + 1:]
                            falseColor = move[-1]
                            if move[:-1] != "shld":
                                selfPen = selfPen + [last]

                            if move[:-1] == "frst":
                                if wincon(players, handlist):
                                    return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty

                                s.send("PRIVMSG %s :Choose one additional " \
                                       "discard \r\n" % CHAN)
                                suppLoc = chooseOne(handlist, players)
                                selfPen = selfPen + [handlist[0][suppLoc]]

                            if move[:-1] == "th":
                                selfPen = selfPen + [players[0]]

                            if move[:-1] == "shld":
                                s.send("PRIVMSG %s :%s's shield deflected the"\
                                       " penalty! \r\n" % (CHAN, players[0]))

                                
                            s.send("PRIVMSG %s :Self-penalty is %s " \
                                   "\r\n" % (CHAN, ' '.join(selfPen)))
                            if wincon(players, handlist):
                                return ["ocanada"]
                            shownHand = handlist[0]
                            shownHand = ' '.join(shownHand)
                            stateFalseColor(falseColor)
                            s.send("PRIVMSG %s :Your hand is %s " \
                                   "\r\n" % (players[0], shownHand))
                            s.send("PRIVMSG %s :%s, what is your next card? " \
                                   "\r\n" % (CHAN, players[0]))


                        else:
                            s.send("PRIVMSG %s :Invalid move. \r\n" % CHAN)
                    else:
                        s.send("PRIVMSG %s :Invalid move. \r\n" % CHAN)
                    
def plagueLower(bplLoc, hand):
    for i in range(bplLoc, -1, -1):
        if stripCard(hand[i])[-1:] != 'k' and stripCard(hand[i])[-1:] != 'w' \
           and stripCard(hand[i])[-1:] != 'p' \
            and stripCard(hand[i])[-1:] != hand[bplLoc][-2]:
            return i
        if i == 0:
            return -1
    return bplLoc

def plagueUpper(bplLoc, hand):
    for i in range(bplLoc, len(hand)):
        if stripCard(hand[i])[-1:] != 'k' and stripCard(hand[i])[-1:] != 'w' \
           and stripCard(hand[i])[-1:] != 'p' \
            and stripCard(hand[i])[-1:] != hand[bplLoc][-2]:
            return i
        if i == len(hand) - 1:
            return -1
    return bplLoc
                
def plagueCheck(handlist):
    for i in range(len(handlist[0])):
        if stripCard(handlist[0][i])[:-1] == "bpl":

            lower = plagueLower(i, handlist[0])
            upper = plagueUpper(i, handlist[0])

            if lower != -1:
                temp = list(handlist[0][lower])
                temp[-2] = handlist[0][i][-2]
                temp[2] = handlist[0][i][2]
                temp[4] = handlist[0][i][4]
                temp[5] = handlist[0][i][5]
                handlist[0][lower] = ''.join(temp)

            if upper != -1:
                temp = list(handlist[0][upper])
                temp[-2] = handlist[0][i][-2]
                temp[2] = handlist[0][i][2]
                temp[4] = handlist[0][i][4]
                temp[5] = handlist[0][i][5]
                handlist[0][upper] = ''.join(temp)

    return handlist

def isPlagued(handlist, index):
    for i in range(len(handlist[index])):
        if stripCard(handlist[index][i])[:-1] == "bpl":
            return True
    return False

def myxoCheck(handlist, myxomatosis):
    colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
    colorCodes = [['1', '1', '1'], ['1', '0', '4'], ['1', '0', '9'], \
                  ['1', '0', '8'], ['0', '1', '4'], ['0', '0', '1'], \
                  ['0', '0', '6']]
    for i in range(len(myxomatosis[0])):
        if myxomatosis[0][i] > 0:
            for j in range(0, myxomatosis[0][i]):
                k = random.randint(0, len(handlist[0]) - 1)
                handlist[0][k] = "\x030%s,%s%swht%s\x03" \
                                 "" % (colorCodes[i][0], colorCodes[i][1], \
                                       colorCodes[i][2], colors[i])
            myxomatosis[0][i] = myxomatosis[0][i] - 1
    return handlist, myxomatosis
            
def penalize (players, handlist, penalty, luck, oubliette, myxomatosis, lovers):
    ignoreNext = False
    for badThing in range(len(penalty)):
        if ignoreNext:
            ignoreNext = False
            
        elif stripCard(penalty[badThing])[:-1] == "d2":
            s.send("PRIVMSG %s :%s drew two cards! \r\n" % (CHAN, players[0]))
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1

        elif stripCard(penalty[badThing])[:-1] == "grr":
            s.send("PRIVMSG %s :%s recieved a groundswell of support! "\
                   "\r\n" % (CHAN, players[0]))
            luck[0] = luck[0] + 4
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
                
        elif stripCard(penalty[badThing])[:-1] == "d3":
            s.send("PRIVMSG %s :%s drew three cards! "\
                   "\r\n" % (CHAN, players[0]))
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
                
        elif stripCard(penalty[badThing])[:-1] == "d4":
            s.send("PRIVMSG %s :%s drew four cards! "\
                   "\r\n" % (CHAN, players[0]))
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1

        elif stripCard(penalty[badThing])[:-1] == "d4i":
            s.send("PRIVMSG %s :%s drew four cards! "\
                   "\r\n" % (CHAN, players[0]))
            replicant = draw(luck)
            handlist[0] = handlist[0] + ([replicant] * 4)
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1

        elif stripCard(penalty[badThing])[:-1] == "BEARS":
            s.send("PRIVMSG %s :GRAAH! %s was viciously mauled by a BEARS!"\
                   "\r\n" % (CHAN, players[0]))
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            handlist[0] = handlist[0] + [draw(luck)]
            if luck[0] > 0:
                luck[0] = luck[0] - 1
            if luck[0] < 0:
                luck[0] = luck[0] + 1
            rand = random.randint(0, len(handlist[0]))
            handlist[0] = handlist[0][0:rand] + \
                          handlist[0][rand + 1:]
            rand = random.randint(0, len(handlist[0]))
            handlist[0] = handlist[0][0:rand] + \
                          handlist[0][rand + 1:]
            rand = random.randint(0, len(handlist[0]))
            handlist[0] = handlist[0][0:rand] + \
                          handlist[0][rand + 1:]

        elif stripCard(penalty[badThing])[:-1] == "wht":
            s.send("PRIVMSG %s :%s is afflicted with myxomatosis!"\
                   "\r\n" % (CHAN, players[0]))
            colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
            i = colors.index(penalty[badThing][-2])
            myxomatosis[0][i] = myxomatosis[0][i] + 2

        elif stripCard(penalty[badThing])[:-1] == "ou":
            s.send("PRIVMSG %s :%s is trapped in the oubliette!"\
                   "\r\n" % (CHAN, players[0]))
            oubliette[0] = oubliette[0] + 3

        elif stripCard(penalty[badThing])[:-1] == "bpl":
            s.send("PRIVMSG %s :%s has contracted the bubonic plague!"\
                   "\r\n" % (CHAN, players[0]))
            handlist[0] = handlist[0] + [penalty[badThing]]

        elif stripCard(penalty[badThing])[:-1] == "dre":
            s.send("PRIVMSG %s :%s is overcome with a horrible sense of "\
                   "dread! \r\n" % (CHAN, players[0]))
            for index in range(len(handlist[0])):
                if handlist[0][index] == "\x0300,14w\x03":
                    handlist[0][index] = "\x030%s,%s%s1%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif handlist[0][index] == "\x0300,14ww\x03":
                    handlist[0][index] = "\x030%s,%s%s2%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif handlist[0][index] == "\x0300,14wwwww\x03":
                    handlist[0][index] = "\x030%s,%s%s5%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif handlist[0][index] == "\x0300,14d4w\x03":
                    handlist[0][index] = "\x030%s,%s%sd4%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif handlist[0][index] == "\x0300,14dblw\x03":
                    handlist[0][index] = "\x030%s,%s%sdbl%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif handlist[0][index] == "\x0300,14ntrlw\x03":
                    handlist[0][index] = "\x030%s,%s%sdre%s\x03" \
                                         "" % (penalty[badThing][2], \
                                               penalty[badThing][4], \
                                               penalty[badThing][5], \
                                               penalty[badThing][-2])
                elif list(handlist[0][index])[-2] == 'w':
                    temp = list(handlist[0][index])
                    temp[-2] = penalty[badThing][-2]
                    temp[2] = penalty[badThing][2]
                    temp[4] = penalty[badThing][4]
                    temp[5] = penalty[badThing][5]
                    handlist[0][index] = ''.join(temp)
                if list(handlist[0][index])[-2] == 'p':
                    temp = list(handlist[0][index])
                    temp[-2] = penalty[badThing][-2]
                    temp[2] = penalty[badThing][2]
                    temp[4] = penalty[badThing][4]
                    temp[5] = penalty[badThing][5]
                    handlist[0][index] = ''.join(temp)
                    

        elif stripCard(penalty[badThing])[:-1] == "wow":
            s.send("PRIVMSG %s :%s is hit by a will-o'-the-wisp!"\
                   "\r\n" % (CHAN, players[0]))
            for index in range(len(handlist[0])):
                if list(handlist[0][index])[-2] != 'k' and \
                   list(handlist[0][index])[-2] != 'w' and \
                   list(handlist[0][index])[-2] != 'p':
                    temp = list(handlist[0][index])
                    temp[-2] = penalty[badThing][-2]
                    temp[2] = penalty[badThing][2]
                    temp[4] = penalty[badThing][4]
                    temp[5] = penalty[badThing][5]
                    handlist[0][index] = ''.join(temp)

        elif stripCard(penalty[badThing])[:-1] == "ccd":
            s.send("PRIVMSG %s :%s's colony collapsed!"\
                   "\r\n" % (CHAN, players[0]))
            for index in range(len(handlist[0])):
                rand = random.randint(1, 7)
                temp = list(handlist[0][index])
                if rand == 1:
                    temp[-2] = 'k'
                    temp[2] = '0'
                    temp[4] = '0'
                    temp[5] = '1'
                    handlist[0][index] = ''.join(temp)
                if rand == 2:
                    temp[-2] = 'b'
                    temp[2] = '1'
                    temp[4] = '1'
                    temp[5] = '1'
                    handlist[0][index] = ''.join(temp)
                if rand == 3:
                    temp[-2] = 'r'
                    temp[2] = '1'
                    temp[4] = '0'
                    temp[5] = '4'
                    handlist[0][index] = ''.join(temp)
                if rand == 4:
                    temp[-2] = 'g'
                    temp[2] = '1'
                    temp[4] = '0'
                    temp[5] = '9'
                    handlist[0][index] = ''.join(temp)
                if rand == 5:
                    temp[-2] = 'y'
                    temp[2] = '1'
                    temp[4] = '0'
                    temp[5] = '8'
                    handlist[0][index] = ''.join(temp)
                if rand == 6:
                    temp[-2] = 'w'
                    temp[2] = '0'
                    temp[4] = '1'
                    temp[5] = '4'
                    handlist[0][index] = ''.join(temp)
                if rand == 7:
                    temp[-2] = 'p'
                    temp[2] = '0'
                    temp[4] = '0'
                    temp[5] = '6'
                    handlist[0][index] = ''.join(temp)
                    
        elif stripCard(penalty[badThing])[:-1] == "ntrl":
            s.send("PRIVMSG %s :A heavenly rain falls!"\
                   "\r\n" % CHAN)
            for index in range(len(handlist[0])):
                if stripCard(handlist[0][index])[:-1] == "d2" or \
                   stripCard(handlist[0][index])[:-1] == "d3" or \
                   stripCard(handlist[0][index])[:-1] == "d4" or \
                   stripCard(handlist[0][index])[:-1] == "d4i" or \
                   stripCard(handlist[0][index])[:-1] == "BEARS" or \
                   stripCard(handlist[0][index])[:-1] == "wow" or \
                   stripCard(handlist[0][index])[:-1] == "wht" or \
                   stripCard(handlist[0][index])[:-1] == "ou" or \
                   stripCard(handlist[0][index])[:-1] == "dre" or \
                   stripCard(handlist[0][index])[:-1] == "bpl" or \
                   stripCard(handlist[0][index])[:-1] == "frst" or \
                   stripCard(handlist[0][index])[:-1] == "ccd" or \
                   stripCard(handlist[0][index])[:-1] == "dbl" or \
                   stripCard(handlist[0][index])[:-1] == "grr" or \
                   stripCard(handlist[0][index])[:-1] == "luv":
                    handlist[0] = handlist[0][0:index] + \
                                  handlist[0][index + 1:]
                    handlist[0] = handlist[0] + [draw(luck)]
                    if luck[0] > 0:
                        luck[0] = luck[0] - 1
                    if luck[0] < 0:
                        luck[0] = luck[0] + 1
                    
        elif stripCard(penalty[badThing])[:-1] == "frst":
            s.send("PRIVMSG %s :A hail of meteors falls from the sky, "\
                   "igniting massive firestorms! \r\n" % CHAN)
            handlist[0] = handlist[0] + (3 * [penalty[badThing + 1]])
            ignoreNext = True
#            penalty = penalty[0:badThing + 1] + \
#                      penalty[badThing + 2:]
                
        elif stripCard(penalty[badThing])[:-1] == "th":
            s.send("PRIVMSG %s :%s trades hands with %s! "\
                   "\r\n" % (CHAN, players[0], penalty[badThing + 1]))
            temp = handlist[0]
            handlist[0] = handlist[players.index(penalty[badThing + 1])]
            handlist[players.index(penalty[badThing + 1])] = temp

            tradee = players.index(penalty[badThing + 1])
            
            shownHand = handlist[tradee]
            shownHand = ' '.join(shownHand)
                            
            s.send("PRIVMSG %s :Your hand is %s " \
                   "\r\n" % (players[tradee], shownHand))

            ignoreNext = True
#            penalty = penalty[0:badThing + 1] + \
#                      penalty[badThing + 2:]

        elif stripCard(penalty[badThing])[:-1] == "dbl":
            s.send("PRIVMSG %s :The rest of the penalties are doubled!"\
                   "\r\n" % CHAN)
            handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, penalty[badThing + 1:], luck, oubliette, myxomatosis, lovers)

        elif stripCard(penalty[badThing])[:-1] == "drde":
            s.send("PRIVMSG %s :%s was revealed! \r\n"\
                   "" % (CHAN, players[0]))
            s.send("PRIVMSG %s :%s's hand is %s! "\
                   "\r\n" % (CHAN, players[0], ' '.join(handlist[0])))

        elif stripCard(penalty[badThing])[:-1] == "her":
            quote = herringFacts[random.randint(0, len(herringFacts) - 1)]
            s.send("PRIVMSG %s :%s \r\n" % (CHAN, quote))                

        elif stripCard(penalty[badThing])[:-1] == "luv":
            if lovers == []:
                s.send("PRIVMSG %s :%s is in love! \r\n"\
                       "" % (CHAN, players[0]))
                lovers = lovers + [players[0]]
                s.send("PRIVMSG %s :The love was passed on! \r\n"\
                       "" % CHAN)
                handlist[1] = handlist[1] + [penalty[badThing]]
                s.send("PRIVMSG %s :Your hand is %s \r\n"\
                       "" % (players[1], ' '.join(handlist[1])))
            elif len(lovers) == 1:
                if players[0] == lovers[0]:
                    s.send("PRIVMSG %s :You are already in the Love "\
                           "Canal, silly. \r\n" % CHAN)
                    s.send("PRIVMSG %s :The love was passed on! \r\n"\
                           "" % CHAN)
                    handlist[1] = handlist[1] + [penalty[badThing]]
                    s.send("PRIVMSG %s :Your hand is %s \r\n"\
                           "" % (players[1], ' '.join(handlist[1])))
                else:
                    lovers = lovers + [players[0]]                
                    s.send("PRIVMSG %s :%s and %s are in the Love Canal! \r\n"\
                           "" % (CHAN, lovers[0], lovers[1]))
                    otherIndex = players.index(lovers[0])
                    colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
                    for i in range(len(colors)):
                        if myxomatosis[0][i] < myxomatosis[otherIndex][i]:
                            myxomatosis[0][i] = myxomatosis[otherIndex][i]
                            s.send("PRIVMSG %s :Myxomatosis spreads to %s! " \
                            "\r\n" % (CHAN, lovers[1]))
                        if myxomatosis[0][i] > myxomatosis[otherIndex][i]:
                            myxomatosis[otherIndex][i] = myxomatosis[0][i]
                            s.send("PRIVMSG %s :Myxomatosis spreads to %s! " \
                            "\r\n" % (CHAN, lovers[0]))
#                    if isPlagued(handlist, 0) and  \
#                       not isPlauged(handlist, otherIndex):
#                        handlist[otherIndex] = handlist[otherIndex]
            else:
                s.send("PRIVMSG %s :%s, the Love Canal is full. Please wait "\
                       "your turn.\r\n" % (CHAN, players[0]))

        time.sleep(1)
            
    return handlist, luck, oubliette, myxomatosis, lovers

def loveCheck(players, handlist, luck, shield, oubliette, myxomatosis, lovers):
    while len(lovers) == 2:
        if players[0] == lovers[1]:
            s.send("PRIVMSG %s :%s is in the Love Canal! "\
                   "\r\n" % (CHAN, players[0]))
            colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
            for i in range(len(colors)):
                if myxomatosis[0][i] > 0:
                    myxomatosis[0][i] = myxomatosis[0][i] - 1

            players = players[1:] + [players[0]]
            handlist = handlist[1:] + [handlist[0]]
            luck = luck[1:] + [luck[0]]
            shield = shield[1:] + [shield[0]]
            oubliette = oubliette[1:] + [oubliette[0]]
            myxomatosis = myxomatosis[1:] + [myxomatosis[0]]

        elif players[0] == lovers[0]:
            s.send("PRIVMSG %s :Welcome to the Love Canal, %s and %s. "\
                   "\r\n" % (CHAN, lovers[0], lovers[1]))
            s.send("PRIVMSG %s :Here, you will play a game used by lovers "\
                   "everywhere to show their undying devotion to " \
                   "one another. \r\n" % CHAN)
            s.send("PRIVMSG %s :The rules are as follows: "\
                   "\r\n" % CHAN)
            s.send("PRIVMSG %s :Both players will play a card from their "\
                   "hands.\r\n" % CHAN)
            s.send("PRIVMSG %s :If both pick a passive card, both are "\
                   "released. \r\n" % CHAN)
            s.send("PRIVMSG %s :If one picks an aggresive card, its penalty "\
                   "is applied to the other. Both are freed, but " \
                   "the attacked party, their love sadly unrequited, will "\
                   "return shortly to try again.\r\n" % CHAN)
            s.send("PRIVMSG %s :If both pick an aggresive card, both will "\
                   "be penalized, and neither will be freed; they "\
                   "will try to find love again next turn. \r\n" % CHAN)

            colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
            for i in range(len(colors)):
                if myxomatosis[0][i] > 0:
                    myxomatosis[0][i] = myxomatosis[0][i] - 1
            
            otherLoc = players.index(lovers[1])
            
            s.send("PRIVMSG %s :%s, what will you choose? " \
                   "\r\n" % (CHAN, lovers[0]))

            shownHand = handlist[0]
            shownHand = ' '.join(shownHand)
                                    
            suppLoc0 = chooseOne(handlist, players)
            card0 = handlist[0][suppLoc0]
            move0 = stripCard(card0).lower()
            pen0 = []
            
            handlist[0] = handlist[0][0:suppLoc0] + handlist[0][suppLoc0 + 1:]
#            s.send("PRIVMSG %s :Your hand is %s " \
#                   "\r\n" % (players[0], shownHand))
            
            s.send("PRIVMSG %s :%s, what will you choose? " \
                   "\r\n" % (CHAN, lovers[1]))

            shownHand = handlist[1]
            shownHand = ' '.join(shownHand)
                             
            suppLoc1 = chooseOne(handlist[otherLoc:] + \
                                 handlist[0:otherLoc], \
                                 players[otherLoc:] + \
                                 players[0:otherLoc])
            card1 = handlist[otherLoc][suppLoc1]
            move1 = stripCard(card1).lower()
            pen1 = []
            
            handlist[otherLoc] = handlist[otherLoc][0:suppLoc1] + \
                                 handlist[otherLoc][suppLoc1 + 1:]
#            s.send("PRIVMSG %s :Your hand is %s " \
#                   "\r\n" % (players[otherLoc], shownHand))

            s.send("PRIVMSG %s :%s played %s! " \
                   "\r\n" % (CHAN, lovers[0], card0))
            s.send("PRIVMSG %s :%s played %s! " \
                   "\r\n" % (CHAN, lovers[1], card1))

# frstr, th bug !!!
            
            if isAggressive(move0) or move0[:-1] == "bpl" \
               or move0[:-1] == "th" or move0[:-1] == "frst":

                if move0[:-1] == "th":
                    pen0 = [card0, players[0]]
                elif move0[:-1] == "frst":
                    s.send("PRIVMSG %s :Choose one additional " \
                           "discard \r\n" % CHAN)

                    shownHand = handlist[0]
                    shownHand = ' '.join(shownHand)
                            
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[0], shownHand))

                    frstrLoc0 = chooseOne(handlist, players)
                    pen0 = [card0, players[0][handlist[0][frstrLoc0]]]
                else:
                    pen0 = [card0]
                
                if isAggressive(move1) or move1[:-1] == "bpl" \
                   or move1[:-1] == "th" or move1[:-1] == "frst":

                    if move1[:-1] == "th":
                        pen1 = [card1, players[otherLoc]]
                    elif move1[:-1] == "frst":
                        s.send("PRIVMSG %s :Choose one additional " \
                               "discard \r\n" % CHAN)

                        shownHand = handlist[otherLoc]
                        shownHand = ' '.join(shownHand)
                            
                        s.send("PRIVMSG %s :Your hand is %s " \
                               "\r\n" % (players[otherLoc], shownHand))

                        frstrLoc1 = chooseOne(handlist, players)
                        pen1 = [card1, players[otherLoc][handlist[otherLoc][frstrLoc1]]]
                    else:
                        pen1 = [card1]

                    handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, pen1, luck, oubliette, myxomatosis, lovers)
                    handlistPrime, luckPrime, oubliettePrime, myxomatosisPrime, lovers = penalize(players[otherLoc:] + players[0:otherLoc], handlist[otherLoc:] + handlist[0:otherLoc], pen0, luck[otherLoc:] + luck[0:otherLoc], oubliette[otherLoc:] + oubliette[0:otherLoc], myxomatosis[otherLoc:] + myxomatosis[0:otherLoc], lovers)
                    handlist, luck, oubliette, myxomatosis = handlistPrime[len(players) - otherLoc:] + handlistPrime[0:len(players) - otherLoc], luckPrime[len(players) - otherLoc:] + luckPrime[0:len(players) - otherLoc], oubliettePrime[len(players) - otherLoc:] + oubliettePrime[0:len(players) - otherLoc], myxomatosisPrime[len(players) - otherLoc:] + myxomatosisPrime[0:len(players) - otherLoc]

                    if wincon(players, handlist):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers
                    if wincon(players[otherLoc:] + players[0:otherLoc], \
                              handlist[otherLoc:] + handlist[0:otherLoc]):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers

                    s.send("PRIVMSG %s :%s and %s will try again next " \
                           "round. \r\n" % (CHAN, lovers[0], lovers[1]))

                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[0], ' '.join(handlist[0])))
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[otherLoc], \
                                     ' '.join(handlist[otherLoc])))
 
                else:
                    handlistPrime, luckPrime, oubliettePrime, myxomatosisPrime, lovers = penalize(players[otherLoc:] + players[0:otherLoc], handlist[otherLoc:] + handlist[0:otherLoc], pen0, luck[otherLoc:] + luck[0:otherLoc], oubliette[otherLoc:] + oubliette[0:otherLoc], myxomatosis[otherLoc:] + myxomatosis[0:otherLoc], lovers)
                    handlist, luck, oubliette, myxomatosis = handlistPrime[len(players) - otherLoc:] + handlistPrime[0:len(players) - otherLoc], luckPrime[len(players) - otherLoc:] + luckPrime[0:len(players) - otherLoc], oubliettePrime[len(players) - otherLoc:] + oubliettePrime[0:len(players) - otherLoc], myxomatosisPrime[len(players) - otherLoc:] + myxomatosisPrime[0:len(players) - otherLoc]

                    if wincon(players, handlist):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers
                    if wincon(players[otherLoc:] + players[0:otherLoc], \
                              handlist[otherLoc:] + handlist[0:otherLoc]):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers

                    s.send("PRIVMSG %s :%s is released. %s will try again " \
                           "later. \r\n" % (CHAN, lovers[0], lovers[1]))

                    #possibly fixed luvr bug? also possibly spurious lol
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[0], ' '.join(handlist[0])))
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[otherLoc], \
                                     ' '.join(handlist[otherLoc])))
                    
                    lovers = [lovers[1]]

                    s.send("PRIVMSG %s :The love was passed on! \r\n"\
                           "" % CHAN)

                    handlist[1] = handlist[1] + ["\x0301,04luvr\x03"]
                    
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[otherLoc], \
                                     ' '.join(handlist[otherLoc])))
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[1], ' '.join(handlist[1])))
                    
            else:

                if isAggressive(move1) or move1[:-1] == "bpl" \
                   or move1[:-1] == "th" or move1[:-1] == "frst":

                    if move1[:-1] == "th":
                        pen1 = [card1, players[otherLoc]]
                    elif move1[:-1] == "frstr":
                        s.send("PRIVMSG %s :Choose one additional " \
                               "discard \r\n" % CHAN)

                        shownHand = handlist[otherLoc]
                        shownHand = ' '.join(shownHand)
                            
                        s.send("PRIVMSG %s :Your hand is %s " \
                               "\r\n" % (players[otherLoc], shownHand))

                        frstrLoc1 = chooseOne(handlist, players)
                        pen1 = [card1, players[otherLoc][handlist[otherLoc][frstrLoc1]]]
                    else:
                        pen1 = [card1]
                    
                    handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, pen1, luck, oubliette, myxomatosis, lovers)
            
                    if wincon(players, handlist):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers
                    if wincon(players[otherLoc:] + players[0:otherLoc], \
                              handlist[otherLoc:] + handlist[0:otherLoc]):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers

                    s.send("PRIVMSG %s :%s is released. %s will try again " \
                           "later. \r\n" % (CHAN, lovers[1], lovers[0]))

                    lovers = [lovers[0]]

                    s.send("PRIVMSG %s :The love was passed on! \r\n"\
                           "" % CHAN)
                    handlist[1] = handlist[1] + ["\x0301,04luvr\x03"]

                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[0], ' '.join(handlist[0])))
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[1], ' '.join(handlist[1])))
                    
                else:

                    s.send("PRIVMSG %s :%s and %s are released. " \
                           "\r\n" % (CHAN, lovers[0], lovers[1]))
                    lovers = []

                    if wincon(players, handlist):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers
                    if wincon(players[otherLoc:] + players[0:otherLoc], \
                              handlist[otherLoc:] + handlist[0:otherLoc]):
                        return players, ["ocanada"], luck, shield, oubliette, myxomatosis, lovers
                    
            players = players[1:] + [players[0]]
            handlist = handlist[1:] + [handlist[0]]
            luck = luck[1:] + [luck[0]]
            shield = shield[1:] + [shield[0]]
            oubliette = oubliette[1:] + [oubliette[0]]
            myxomatosis = myxomatosis[1:] + [myxomatosis[0]]

        else:
            break

    return players, handlist, luck, shield, oubliette, myxomatosis, lovers

def execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers):
    reverse = False
    move2 = ""

    discard = handlist[0][cardloc]
    handlist[0] = handlist[0][0:cardloc] + handlist[0][cardloc + 1:]
    s.send("PRIVMSG %s :The top of the discard pile is " \
           "%s. \r\n" % (CHAN, discard))
    stateColor(color)

    if move[:-1] == "exe":
        
        if wincon(players, handlist):
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers

        s.send("PRIVMSG %s :Choose any additional card to play" \
               " \r\n" % CHAN)

        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
                            
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))

        suppLoc = chooseOne(handlist, players)
        move2 = stripCard(handlist[0][suppLoc])

        if move2[-1:] == 'w':
            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
            color = colorChoice(user)

            if move2[:-1] == 'w':
                s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                color = colorChoice(user)

            if move2[:-1] == 'wwww':
                s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                color = colorChoice(user)
                s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                color = colorChoice(user)
                s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                color = colorChoice(user)
                s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                color = colorChoice(user)

        if move2[-1:] != 'w':
            color = move2[-1:]
        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move2, suppLoc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)
#        if wincon(players, handlist) or move == "ocanada":
#            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
        return move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
    if move[:-1] == "frst":

        if wincon(players, handlist):
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers

        s.send("PRIVMSG %s :Choose one additional " \
               "discard \r\n" % CHAN)

        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
                            
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))
        
        suppLoc = chooseOne(handlist, players)
        penalty = penalty + [discard]
        penalty = penalty + [handlist[0][suppLoc]]
        s.send("PRIVMSG %s :Penalty list is %s " \
               "\r\n" % (CHAN, ' '.join(penalty)))
        handlist[0] = handlist[0][0:suppLoc] + handlist[0][suppLoc + 1:]
                        
    elif isAggressive(move):
        penalty = penalty + [discard]
        s.send("PRIVMSG %s :Penalty list is %s " \
               "\r\n" % (CHAN, ' '.join(penalty)))

    elif move[:-1] == "th":
        penalty = penalty + [discard]
        penalty = penalty + [players[0]]
        s.send("PRIVMSG %s :Penalty list is %s " \
               "\r\n" % (CHAN, ' '.join(penalty)))
                            
    elif move[:-1] == "bpl" and len(penalty) > 0:
        penalty = penalty + [discard]
        s.send("PRIVMSG %s :Penalty list is %s " \
               "\r\n" % (CHAN, ' '.join(penalty)))

    elif move[:-1] == "shld":
        if (len(penalty) > 0):
            s.send("PRIVMSG %s :%s's shield deflected the"\
                   " penalty! \r\n" % (CHAN, players[0]))
            s.send("PRIVMSG %s :Penalty list is %s " \
                   "\r\n" % (CHAN, ' '.join(penalty)))
        else:
            s.send("PRIVMSG %s :%s is now shielded! " \
                   "\r\n" % (CHAN, players[0]))
            shield[0] = shield[0] + 1
                            
    elif shield[0] > 0 and len(penalty) > 0:
        s.send("PRIVMSG %s :%s's shield deflected the " \
               "penalty! \r\n" % (CHAN, players[0]))
        shield[0] = shield[0] - 1
        s.send("PRIVMSG %s :Penalty list is %s " \
               "\r\n" % (CHAN, ' '.join(penalty)))
                            
    elif (len(penalty) > 0):
        s.send("PRIVMSG %s :%s incurred the penalty! " \
               "\r\n" % (CHAN, players[0]))
        handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, penalty, luck, oubliette, myxomatosis, lovers)
        penalty = []

    if move[:-1] == "dall":
        s.send("PRIVMSG %s :All cards of the same color " \
               "discarded! \r\n" % CHAN)
        loc = 0
        while (loc < len(handlist[0])):
            if stripCard(handlist[0][loc])[-1:] == color:
                handlist[0] = handlist[0][0:loc] + \
                              handlist[0][loc + 1:]
                loc = loc - 1
            loc = loc + 1

    if move[:-1] == "qsu":

        if wincon(players, handlist):
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
        s.send("PRIVMSG %s :Choose one additional " \
               "discard \r\n" % CHAN)

        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
        
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))
        suppLoc = chooseOne(handlist, players)
        queue = queue + [handlist[0][suppLoc]]
        qtime = qtime + (2 * len(players) + 1 - len(queue))
        s.send("PRIVMSG %s :Job submitted. \r\n" % CHAN)
        handlist[0] = handlist[0][0:suppLoc] + \
                      handlist[0][suppLoc + 1:]

    if move[:-1] == "pur":
        if wincon(players, handlist):
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
        s.send("PRIVMSG %s :Choose one additional " \
               "card \r\n" % CHAN)

        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
        
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))

        suppLoc = chooseOne(handlist, players)

        temp = list(handlist[0][suppLoc])
        temp[-2] = discard[-2]
        temp[2] = discard[2]
        temp[4] = discard[4]
        temp[5] = discard[5]
        handlist[0][suppLoc] = ''.join(temp)
        
    if move[:-1] == "rv":
        s.send("PRIVMSG %s :Order of play reversed! " \
               "\r\n" % CHAN)

        handlist, myxomatosis = myxoCheck(handlist, myxomatosis)
        handlist = plagueCheck(handlist)
        
        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
        
        if wincon(players, handlist):
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))

        players.reverse()
        handlist.reverse()
        luck.reverse()
        shield.reverse()
        oubliette.reverse()
        myxomatosis.reverse()
        reverse = True
        
    if move[:-1] == "shd":
        s.send("PRIVMSG %s :The deck has been shuffled!" \
               "\r\n" % CHAN)
        rand = random.randint(1, 20)
        if rand < 4:
            s.send("PRIVMSG %s :You feel unlucky today" \
                   "... \r\n" % CHAN)
            luck[0] = luck[0] - 1
        elif rand < 8:
            True
        elif rand < 15:
            s.send("PRIVMSG %s :You feel somewhat lucky " \
                   "today. \r\n" % CHAN)
            luck[0] = luck[0] + 1
        else:
            s.send("PRIVMSG %s :You feel very lucky " \
                   "today! \r\n" % CHAN)
            luck[0] = luck[0] + 2

    if move[:-1] == "sap":
        
        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
                            
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))
        
        selfPen = selfPenalize(handlist, players)
        if selfPen == ["ocanada"]:
            return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        s.send("PRIVMSG %s :%s incurred the penalty! " \
               "\r\n" % (CHAN, players[0]))
        handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, selfPen, luck, oubliette, myxomatosis, lovers)

    if wincon(players, handlist):
        return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
        
    if qtime > 0:
        qtime = qtime - 1
        if qtime == 0:
            for item in queue:
                handlist[0] = handlist[0] + [item]
                s.send("PRIVMSG %s :Job complete. \r\n" % CHAN)
                queue = []


    handlist, myxomatosis = myxoCheck(handlist, myxomatosis)
    handlist = plagueCheck(handlist)
                            
    stateHandSizes(players, handlist)

    if not reverse:
        shownHand = handlist[0]
        shownHand = ' '.join(shownHand)
                            
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[0], shownHand))

    if not reverse:
        players = players[1:] + [players[0]]
        handlist = handlist[1:] + [handlist[0]]
        luck = luck[1:] + [luck[0]]
        shield = shield[1:] + [shield[0]]
        oubliette = oubliette[1:] + [oubliette[0]]
        myxomatosis = myxomatosis[1:] + [myxomatosis[0]]
    else:
        reverse = False

    if move[:-1] == "sk":
        s.send("PRIVMSG %s :%s has been skipped! "\
               "\r\n" % (CHAN, players[0]))
        players = players[1:] + [players[0]]
        handlist = handlist[1:] + [handlist[0]]
        luck = luck[1:] + [luck[0]]
        shield = shield[1:] + [shield[0]]
        oubliette = oubliette[1:] + [oubliette[0]]
        myxomatosis = myxomatosis[1:] + [myxomatosis[0]]

    while oubliette[0] > 0:
        s.send("PRIVMSG %s :%s is in the oubliette! "\
               "\r\n" % (CHAN, players[0]))
        oubliette[0] = oubliette[0] - 1
        colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
        for i in range(len(colors)):
            if myxomatosis[0][i] > 0:
                myxomatosis[0][i] = myxomatosis[0][i] - 1

        players = players[1:] + [players[0]]
        handlist = handlist[1:] + [handlist[0]]
        luck = luck[1:] + [luck[0]]
        shield = shield[1:] + [shield[0]]
        oubliette = oubliette[1:] + [oubliette[0]]
        myxomatosis = myxomatosis[1:] + [myxomatosis[0]]

    players, handlist, luck, shield, oubliette, myxomatosis, lovers =  loveCheck(players, handlist, luck, shield, oubliette, myxomatosis, lovers)
    if handlist == ["ocanada"]:
        return "ocanada", cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
                        
    s.send("PRIVMSG %s :%s, what will you play? " \
           "\r\n" % (CHAN, players[0]))

    return move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers
            
def unoBEARS(players):
    s.send("PRIVMSG %s :Welcome to UnoBEARS! Type the card you'd like " \
           "to play. \r\n" % CHAN)
    s.send("PRIVMSG %s :Type draw to draw a card. Type UNO when you or " \
           "another player has one card left. \r\n" % CHAN)

    luck = [0] * len(players)
    shield = [0] * len(players)
    colors = ['b', 'r', 'g', 'y', 'w', 'k', 'p']
    myxomatosis = []
    for i in range(len(players)):
        myxomatosis = myxomatosis + [[0] * len(colors)]
    oubliette = [0] * len(players)
    lovers = []

    queue = []
    qtime = 0
    
    discard = draw(luck)
    s.send("PRIVMSG %s :The top of the discard pile is %s. " \
           "\r\n" % (CHAN, discard))
    if stripCard(discard)[-1:] == 'w':
        rand = random.randint(1, 4)
        if rand == 1:
            color = 'b'
        if rand == 2:
            color = 'r'
        if rand == 3:
            color = 'g'
        if rand == 4:
            color = 'y'
    else:
        color = stripCard(discard)[-1:]
    stateColor(color)

    handlist = []
        
    for i in range(len(players)):
        plhand = [draw(luck)] + [draw(luck)] + [draw(luck)] + [draw(luck)]  + \
                 [draw(luck)] + [draw(luck)] + [draw(luck)]
        handlist = handlist + [plhand]
        s.send("PRIVMSG %s :Your hand is %s " \
               "\r\n" % (players[i], ' '.join(handlist[i])))

    stateHandSizes(players, handlist)
    
    s.send("PRIVMSG %s :%s, what will you play? \r\n" % (CHAN, players[0]))

    readbuffer = ""
    penalty = []
    
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
                move = line[3].lstrip(':').lower()
                
                if (user == players[0] and move == 'draw') or \
                   (user == players[0] and move == 'd'):
                    s.send("PRIVMSG %s :%s draws a card. " \
                           "\r\n" % (CHAN, players[0]))

                    if len(handlist[0]) >= 30:
                        s.send("PRIVMSG %s :%s exceeds the maximum " \
                           "hand size. \r\n" % (CHAN, players[0]))
                    
                        handlist[0] = handlist[0][0:29] + [draw(luck)]

                    else:
                        handlist[0] = handlist[0] + [draw(luck)]
                        
                    if luck[0] > 0:
                        luck[0] = luck[0] - 1
                    if luck[0] < 0:
                        luck[0] = luck[0] + 1

                    if shield[0] > 0 and len(penalty) > 0:
                        s.send("PRIVMSG %s :%s's shield deflected the " \
                               "penalty! \r\n" % (CHAN, players[0]))
                        shield[0] = shield[0] - 1
                        s.send("PRIVMSG %s :Penalty list is %s " \
                               "\r\n" % (CHAN, ' '.join(penalty)))

                        
                    elif (len(penalty) > 0):
                        s.send("PRIVMSG %s :%s incurred the penalty! " \
                               "\r\n" % (CHAN, players[0]))
                        handlist, luck, oubliette, myxomatosis, lovers = penalize(players, handlist, penalty, luck, oubliette, myxomatosis, lovers)
                        penalty = []

                    shownHand = handlist[0]
                    shownHand = ' '.join(shownHand)
                            
                    s.send("PRIVMSG %s :Your hand is %s " \
                           "\r\n" % (players[0], shownHand))

                    while oubliette[0] > 0:
                        s.send("PRIVMSG %s :%s is in the oubliette! "\
                               "\r\n" % (CHAN, players[0]))
                        oubliette[0] = oubliette[0] - 1
                        for i in range(len(colors)):
                            if myxomatosis[0][i] > 0:
                                myxomatosis[0][i] = myxomatosis[0][i] - 1     

                        players = players[1:] + [players[0]]
                        handlist = handlist[1:] + [handlist[0]]
                        luck = luck[1:] + [luck[0]]
                        shield = shield[1:] + [shield[0]]
                        oubliette = oubliette[1:] + [oubliette[0]]
                        myxomatosis = myxomatosis[1:] + [myxomatosis[0]]


                    players, handlist, luck, shield, oubliette, myxomatosis, lovers =  loveCheck(players, handlist, luck, shield, oubliette, myxomatosis, lovers)
                    if handlist == ["ocanada"]:
                        return

                    s.send("PRIVMSG %s :%s, what will you play? " \
                           "\r\n" % (CHAN, players[0]))

                cardloc = cardInHand(move, handlist[0])
                if user == players[0] and cardloc + 1:
                    if move[-1:] == 'w':
                        s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                        color = colorChoice(user)

                        if move[:-1] == 'w':
                            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                            color = colorChoice(user)

                        if move[:-1] == 'wwww':
                            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                            color = colorChoice(user)
                            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                            color = colorChoice(user)
                            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                            color = colorChoice(user)
                            s.send("PRIVMSG %s :Choose the color. \r\n" % CHAN)
                            color = colorChoice(user)

                        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)
                            
                    elif move[-1:] == color:
                        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)

                    elif move[:-1] == stripCard(discard)[:-1].lower():
                        color = move[-1:]
                        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)

                    elif color == 'p':
                        color = move[-1:]
                        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)                        

                    elif move[-1:] == 'p':
                        color = 'p'
                        s.send("PRIVMSG %s :Color forced to purple! " \
                               "\r\n" % CHAN)
                        move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers = execMove(move, cardloc, color, handlist, players, luck, shield, myxomatosis, oubliette, queue, qtime, discard, penalty, lovers)
                        
                    else:
                        s.send("PRIVMSG %s :Invalid move. \r\n" % CHAN)

                if move == "ocanada" or move == "quit":
                    s.send("PRIVMSG %s :Game quit. \r\n" % CHAN)
                    return
                    
def unoSetup(host):
    players = [host]
    s.send("PRIVMSG %s :UnoBEARS ver. &7 \r\n" % CHAN)
    s.send("PRIVMSG %s :by D. Eepthought, D. Oorbot, et al. \r\n" % CHAN)
    s.send("PRIVMSG %s :Host is %s. Type \"go\" to start. \r\n" % (CHAN, host))
    s.send("PRIVMSG %s :Type \"help\" for some documentation. \r\n" % CHAN)
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
                    s.send("PRIVMSG %s :Game quit. \r\n" % CHAN)
                    return
                elif (line[3] == ':help') and user == host:
                    s.send("PRIVMSG %s :UnoBears documentation, v1.0 \r\n" % CHAN)
                    s.send("PRIVMSG %s :UnoBears functions basically like standard Uno, but with some differences. \r\n" % CHAN)
                    s.send("PRIVMSG %s :Players start with 7 cards. BearsBot will PM you your hand whenever it changes. \r\n" % CHAN)
                    s.send("PRIVMSG %s :You can play any card that matches the color or species (the part that isn't color) of the top card. \r\n" % CHAN)
                    s.send("PRIVMSG %s :You can also play any wild or purple card at any time. Any color can be played on purple. \r\n" % CHAN)
                    s.send("PRIVMSG %s :Cards like d2 (draw 2) that affect another player in some way get added to the penalty list. \r\n" % CHAN)
                    s.send("PRIVMSG %s :If there are cards in the penalty list, you must play another such card or you take all the penalties. \r\n" % CHAN)
                    s.send("PRIVMSG %s :The cards that work are most of the ones that aren't numbers, rv (reverse), or sk (skip). \r\n" % CHAN)
                    # s.send("PRIVMSG %s :You can also play a shield to avoid taking penalties. \r\n" % CHAN)
                    s.send("PRIVMSG %s :Like in standard Uno, the cards are mostly numbers, along with skip, reverse, wild, draw 2, and draw 4. \r\n" % CHAN)
                    s.send("PRIVMSG %s :There are also some other cards, which do other things. \r\n" % CHAN)
                    s.send("PRIVMSG %s :You win if you get rid of all of your cards. Good luck! \r\n" % CHAN)
                elif (line[3] == ':go') and user == host:
                    unoBEARS(players)
                    return
