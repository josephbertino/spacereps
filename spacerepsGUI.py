# Python3

import os
import sys
import pickle
from datetime import date
import tkinter as tk


class byte:
    """
    This class defines a single memory index card
    """

    def __init__(self):
        self.level = 1
        self.question = ""
        self.answer = ""


zeroday = date(2019, 4, 1)
f_archive = "spacerep_tape"
f_active = "spacerep_SSD"

# A list of 64 lists, following a specific pattern of spaced repetitions
levelRing = [
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [6, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
    [2, 1],
    [3, 1],
    [2, 1],
    [4, 1],
    [2, 1],
    [3, 1],
    [2, 1],
    [7, 1],
    [2, 1],
    [3, 1],
    [6, 2, 1],
    [5, 1],
    [4, 2, 1],
    [3, 1],
    [2, 1],
    [1],
]


def getDate():
    """
    Gets today's date, returns as a datetime object
    :return: datetime object (datetime.date(YYYY, MM, DD))
    """

    return date.today()


# JBJB
def writeSSD(bytelist):
    """
    Saves all bytes in bytelist, whose level < 7, to the SSD file, by writing a pickle
    :param bytelist:
    :return: None
    """

    actives = [b for b in bytelist if b.level <= 7]

    with open(f_active, "w+b") as f:
        pickle.dump(actives, f)


def archiveBytes(bytelist):
    """
    Pushes all bytes in bytelist, whose level > 7, to the archive file, by appending a pickle
    :param bytelist: list of instances of byte
    :return: None
    """

    retireds = [b for b in bytelist if b.level > 7]

    with open(f_archive, "a+b") as f:
        if len(retireds) > 0:
            pickle.dump(retireds, f)


def readArchive():
    """
    Unpickles all archived memory bytes from the f_archive file
    :return: a list of all archived memory bytes
    """
    archive = []

    if os.path.exists(f_archive):
        with open(f_archive, "rb") as f:
            try:
                while True:
                    pickles = pickle.load(f)
                    if len(pickles) > 0:
                        archive.append(pickles)
            except EOFError:
                pass

    return archive


def newByte():
    """
    Create, initialize, and return a new byte instance
    :return: byte
    """
    newb = byte()
    newb.question = input("Enter question: ")
    newb.answer = input("Enter answer: ")
    return newb


def addBytes(bytelist):
    """
    Extend the bytelist with new questions, prompting the user for each new addition
    :param bytelist: list of byte instances
    :return: None
    """
    more = input("Would you like to add a new question? y / n\n")

    while more == "y":
        newb = newByte()
        bytelist.append(newb)

        more = input("Would you like to add another question? y / n\n")


def runMe():
    """
    The main program. First retrieves the active list of bytes. Quizzes the user on all bytes
    that are on today's schedule. Then surveys the user for new bytes to add to the active list.
    Finally, archives any 'graduated' bytes and saves the rest back to disk.
    :return: None
    """

    addBytes(bytelist)

    archiveBytes(bytelist)

    writeSSD(bytelist)

    print("See you tomorrow!")


# [] screen 1: "start quiz" button to correspond with runMe()
# [] screen 2: "add questions" button (will terminate or remove itself upon completion) ;
#       [] and "exit" button.


class SpaceRepApp(tk.Frame):
    """
    The main program. First retrieves the active list of bytes. Quizzes the user on all bytes
    that are on today's schedule. Then surveys the user for new bytes to add to the active list.
    Finally, archives any 'graduated' bytes and saves the rest back to disk.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.bytelist = []
        self.todayslvls = []

        self.getLvls(getDate())
        self.readSSD()
        self.printWelcome()
        self.arrangeMe()
        self.pack()
        self.create_widgets()

    def getLvls(self, today):
        """
        Finds difference (# of days) between 'today' and the 'zeroday' date,
        to compute which of the 64 notches from levelring to observe
        when testing the user on memory bytes
        Then uses the computed index to retrieve today's testing levels
        :param today: datetime object
        """
        idx = (today - zeroday).days % 64
        self.todayslvls = levelRing[idx]

    def readSSD(self):
        """
        Reads (unpickles) the active list of byte instances from storage
        """
        if os.path.exists(f_active):
            try:
                with open(f_active, "rb") as f:
                    self.bytelist = pickle.load(f)
            except IOError:
                print("Could not read", f_active)
                sys.exit()

    def printWelcome(self):
        msgtxt = "Welcome to the Spaced Repetition Program!"
        msg = tk.Message(
            self.master, text=msgtxt, width=400, font=("Times", 20, "bold")
        )
        msg.pack(side="top")

    def arrangeMe(self):
        self.master.geometry("500x500")  # adjust dimensions of main window
        self.master.geometry("+90+90")  # adjust position on screen
        self.master.attributes(
            "-topmost", True
        )  # bring to front of application windows

    def create_widgets(self):
        self.quizbtn = tk.Button(self, width="40")
        self.quizbtn["text"] = "Quiz Me Today!"
        self.quizbtn["command"] = self.quizMe
        self.quizbtn.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.pack(side="bottom")

    def quizMe(self):
        """
        Quiz the user on all bytes whose level is include in today's levelRing schedule
        :param bytelist: the list of bytes
        :param idx: today's levelRing index
        :return: None
        """

        todaysBytes = [b for b in self.bytelist if b.level in set(self.todayslvls)]
        bnum = len(todaysBytes)

        for i, byte in enumerate(todaysBytes):
            self.askQuest(byte, i + 1, bnum)

        # JBJB [] once all questions are asked, remove the QUIZ ME button and put the 'new questions' button

    def askQuest(self, byte, i, bnum):
        # JBJB [] implement this as a separate class instance?
        """
        Quizzes the user on a byte. If they are correct, advance its level. Otherwise demote its level to 1.
        :param byte: the class byte instance
        :param i: int, the question index
        :param bnum: int, number of questions today
        """
        win = tk.Toplevel()
        win.wm_title("Question {} of {}".format(i, bnum))
        win.geometry("500x500+100+100")
        win.attributes("-topmost", True)  # bring to front of application windows

        qlab = tk.Label(win, text=byte.question)
        qlab.pack(side="top")

        revealbtn = tk.Button(win, text="Flip Card")
        revealbtn["command"] = win.destroy
        revealbtn.pack(side="bottom")


"""
        print('[{}]: '.format(byte.level), byte.question)
        input("\nPress any key to see answer")
        print(byte.answer)
        yn = input("\nWere you correct? (y) or (n)\n")
        if yn == 'y':
            raiseByte(byte)
        else:
            lowerByte(byte)
        return
"""


root = tk.Tk()
tkgame = SpaceRepApp(master=root)
tkgame.mainloop()


def raiseByte(byte):
    """
    Increases a byte's commitment level by 1
    :param byte: the class byte instance
    :return: None
    """
    byte.level += 1


def lowerByte(byte):
    """
    Decreases a byte's commitment level back to 1, the ground floor
    :param byte: the class byte instance
    :return: None
    """
    byte.level = 1
