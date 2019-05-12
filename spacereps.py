#Python3

import os
import sys
import time
import pickle
from datetime import date
from random import shuffle


ZERODAY = date(2019, 4, 1)
f_archive = "memory_tape"
f_active = "memory_SSD"

menuopts = {1: 'Quiz Me Today',
            2: 'Add Questions',
            3: 'Exit'}

class byte:
    '''
    This class defines a single memory index card.
    '''
    def __init__(self):
        '''
        A new byte has level=1 so that you get quizzed on it most frequently,
        until you answer it correctly, at which point its level will increase and
        you will see it less often.
        '''
        self.level = 1
        self.question = ""
        self.answer = ""

'''
A list of 64 lists, following a specific pattern of spaced repetitions.
Each index contains a subset of the 7 levels a byte can progress through.
Every day accesses a subsequent index in the levelRing (as determined by
the difference between 'today' and the constant ZERODAY), so every day
you will be quizzed on the active bytes whose levels correspond to that day's index.

i.e. if today's index is 3, you will only see bytes with levels 4 and 1.
'''
levelRing = [[2, 1], [3, 1], [2, 1], [4, 1],
             [2, 1], [3, 1], [2, 1], [1],
             [2, 1], [3, 1], [2, 1], [5, 1],
             [4, 2, 1], [3, 1], [2, 1], [1],
             [2, 1], [3, 1], [2, 1], [4, 1],
             [2, 1], [3, 1], [2, 1], [6, 1],
             [2, 1], [3, 1], [2, 1], [5, 1],
             [4, 2, 1], [3, 1], [2, 1], [1],
             [2, 1], [3, 1], [2, 1], [4, 1],
             [2, 1], [3, 1], [2, 1], [1],
             [2, 1], [3, 1], [2, 1], [5, 1],
             [4, 2, 1], [3, 1], [2, 1], [1],
             [2, 1], [3, 1], [2, 1], [4, 1],
             [2, 1], [3, 1], [2, 1], [7, 1],
             [2, 1], [3, 1], [6, 2, 1], [5, 1],
             [4, 2, 1], [3, 1], [2, 1], [1]
             ]


def getDate():
    '''
    Gets today's date, returns as a datetime object
    :return: datetime object (datetime.date(YYYY, MM, DD))
    '''

    return date.today()


def getLvlIdx(today):
    '''
    Finds difference (# of days) between 'today' and the 'ZERODAY' date,
    to compute which of the 64 notches from levelring to observe
    when testing the user on memory bytes
    :param today: datetime object
    :return: the mod(64) index into the spacelib.levelRing list
    '''

    return (today - ZERODAY).days % 64


def readSSD():
    '''
    Reads (unpickles) the active list of byte instances from storage
    :return: list of byte instances
    '''
    bytelist = []

    if os.path.exists(f_active):
        with open(f_active, 'rb') as f:
            bytelist = pickle.load(f)

    return bytelist


def writeSSD(bytelist):
    '''
    Saves all bytes in bytelist, whose level < 7, to the SSD file, by writing a pickle
    :param bytelist:
    :return: None
    '''

    actives = [b for b in bytelist if b.level <= 7]

    with open(f_active, 'w+b') as f:
        pickle.dump(actives, f)


def archiveBytes(bytelist):
    '''
    Pushes all bytes in bytelist, whose level > 7, to the archive file, by appending a pickle
    :param bytelist: list of instances of byte
    :return: None
    '''

    retireds = [b for b in bytelist if b.level > 7]

    with open(f_archive, 'a+b') as f:
        if len(retireds) > 0:
            pickle.dump(retireds,f)


def readArchive():
    '''
    Unpickles all archived memory bytes from the f_archive file
    :return: a list of all archived memory bytes
    '''
    archive = []

    if os.path.exists(f_archive):
        with open(f_archive, 'rb') as f:
            try:
                while True:
                    pickles = pickle.load(f)
                    if len(pickles) > 0:
                        archive.append(pickles)
            except EOFError:
                pass

    return archive


def raiseByte(byte):
    '''
    Increases a byte's commitment level by 1
    :param byte: the class byte instance
    :return: None
    '''
    byte.level += 1


def lowerByte(byte):
    '''
    Decreases a byte's commitment level back to 1, the ground floor
    :param byte: the class byte instance
    :return: None
    '''
    byte.level = 1


def askQuest(byte):
    '''
    Quizzes the user on a byte. If they are correct, advance its level. Otherwise demote its level to 1.
    :param byte: the class byte instance
    :return: None
    '''
    os.system('clear')
    print('[{}]: '.format(byte.level), byte.question)
    input("\nPress any key to see answer\n")
    print(byte.answer)
    yn = input ("\nWere you correct? (y) or (n)\n")

    if yn == 'q':
        return False

    if yn == 'y':
        raiseByte(byte)
    else:
        lowerByte(byte)

    return True


def quizMe(bytelist, idx):
    '''
    Quiz the user on all bytes whose level is include in today's levelRing schedule
    :param bytelist: the list of bytes
    :param idx: today's levelRing index
    :return: None
    '''
    todayslvls = levelRing[idx]

    todaysBytes = [b for b in bytelist if b.level in set(todayslvls)]
    shuffle(todaysBytes)

    for byte in todaysBytes:
        if askQuest(byte) is False:
            # Terminate early
            return


def newByte():
    '''
    Create, initialize, and return a new byte instance
    :return: byte
    '''
    newb = byte()
    newb.question = input("Enter question: ")
    newb.answer = input("Enter answer: ")
    return newb


def addBytes(bytelist):
    '''
    Extend the bytelist with new questions, prompting the user for each new addition
    :param bytelist: list of byte instances
    :return: None
    '''
    more = input("Would you like to add a new question? ")

    while more == 'y':
        newb = newByte()
        bytelist.append(newb)
        more = input("Would you like to add another question? ")


def topmenu(bytelist):
    idx = getLvlIdx(getDate())

    while True:
        os.system('clear')
        print("************SPACEREPS**************")
        print("------------Main Menu--------------")
        print()

        print("Options:")
        for key in sorted(menuopts):
            print("{}. {}".format(key, menuopts[key]))

        try:
            choice = int(input("\nEnter choice: "))
        except ValueError:
            choice = 0

        if choice not in menuopts.keys():
            print("\nPlease try again...")
            time.sleep(1)
        elif choice == 1:
            quizMe(bytelist, idx)
            del menuopts[1]
        elif choice == 2:
            addBytes(bytelist)
        elif choice == 3:
            os.system('clear')
            print("Thank you for quizzing!\nSee you tomorrow!")
            time.sleep(1)
            return



'''
The program: First retrieves the active list of bytes. Quizzes the user on all bytes
that are on today's schedule. Then surveys the user for new bytes to add to the active list.
Finally, archives any 'graduated' bytes and saves the rest back to disk.
:return: None
'''
try:
    bytelist = readSSD()
except IOError:
    print("Could not read",f_active)
    sys.exit()
topmenu(bytelist)
archiveBytes(bytelist)
writeSSD(bytelist)
exit(0)
