#Python3

import os
import sys
import pickle
from datetime import date

class byte:
    def __init__(self):
        self.level = 1
        self.question = ""
        self.answer = ""

zeroday = date(2019, 4, 1)
f_archive = "spacerep_tape"
f_active = "spacerep_SSD"

# A list of 64 lists, following a specific pattern of spaced repetitions
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
        Inputs: None
        return: datetime object (datetime.date(YYYY, MM, DD))
    '''

    return date.today()


def getLvlCubby(today):
    '''
    Finds difference (# of days) between 'today' and the 'zeroday' date,
    to compute which of the 64 notches from levelring to observe
    when testing the user on memory bytes
    :param today: datetime object
    :return: the mod(64) index into the spacelib.levelRing list
    '''

    return (today - zeroday).days % 64


def writeSSD(bytelist):
    '''
    Pickles the active list of byte instances to storage
    :param bytelist: list of class byte instances
    :return: None
    '''
    with open(f_active, 'w+b') as f:
        pickle.dump(bytelist, f)


def readSSD():
    '''
    Reads (unpickles) the active list of byte instances from storage
    :return: list of byte instances
    '''
    bytelist = []

    if os.path.exists(f_active):
        with open(f_active, 'ab') as f:
            bytelist = pickle.load(f)

    return bytelist



def raiseByte(byte):
    byte.level += 1


def lowerByte(byte):
    byte.level = 1


def askQuest(byte):
    print(byte.question)
    input("\nPress any key to see answer")
    print(byte.answer)
    yn = input ("\nWere you correct? (y) or (n)")
    if yn == 'y':
        raiseByte(byte)
    else:
        lowerByte(byte)
    return


def archiveBytes(bytelist):
    '''
    Pushes all bytes in bytelist, whose level > 7, to the archive file, by appending a pickle
    :param bytelist: list of instances of byte
    :return: None
    '''

    retireds = [b for b in bytelist if b.level > 7]

    with open(f_archive, 'a+b') as f:
        pickle.dump(retireds,f)


def flashBytes(bytelist):
    '''
    Saves all bytes in bytelist, whose level < 7, to the SSD file, by writing a pickle
    :param bytelist:
    :return: None
    '''

    actives = [b for b in bytelist if b.level <= 7]

    with open(f_active, 'w+b') as f:
        pickle.dump(actives, f)


def quizMe(bytelist, lvl):

    todayslvls = levelRing[lvl]

    todaysBytes = [b for b in bytelist if b.level in set(todayslvls)]

    for byte in todaysBytes:
        askQuest(byte)


def askQuestions():
    pass


def runMe():
    lvl = getLvlCubby(getDate())

    try:
        bytelist = readSSD()
    except IOError:
        print("Could not read",f_active)
        sys.exit()

    quizMe(bytelist,lvl)

    print("See you tomorrow!")


