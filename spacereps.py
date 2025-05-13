import os
import sys
import time
import json
from datetime import date
from random import shuffle

from consts import level_rings


if len(sys.argv) != 2:
    print("\nInvocation: > python spacereps.py <quizset>")
    print("\n--- where <quizset> refers to the name of the specific question list you wish to be quizzed from.")
    input("\nPress any key to continue")
    sys.exit(0)

# Arbitrarily chosen day to anchor the spacing of bytes
ZERODAY = date(2019, 4, 1)

bytegroup = sys.argv[1]
f_active_json = bytegroup + "_active.json"
f_archive_json = bytegroup + "_archive.json"

menuopts = {1: "Quiz Me Today", 2: "Add Questions", 3: "Exit"}


class byte:
    """
    This class defines a single memory index card.
    """

    def __init__(self, level=1, question='', answer=''):
        """
        A new byte has level=1 so that you get quizzed on it most frequently,
        until you answer it correctly, at which point its level will increase and
        you will see it less often.
        """
        self.level = level
        self.question = question
        self.answer = answer


def get_level_index(today):
    """
    Finds difference (# of days) between 'today' and the 'ZERODAY' date,
    to compute which of the 64 levels from levelring to observe
    when testing the user on memory bytes

    :param datetime.date today: datetime object
    :return int: the mod(64) index into the spacelib.levelRing list
    """

    return (today - ZERODAY).days % 64


def read_bytes_from_json(archive=False):
    """
    Reads the active lists of byte instances from storage, represented as a list of dicts in JSON

    :param bool archive:    Whether to retrieve the archived questions
    :return:                list of byte instances
    """
    fp = f_archive_json if archive else f_active_json

    if os.path.exists(fp):
        with open(f_active_json, "r") as f:
            data = json.load(f)

    bytelist = [byte(d['level'], d['question'], d['answer']) for d in data]
    return bytelist


def write_bytes_to_json(bytelist, archive=False):
    """
    Saves all bytes in bytelist whose level < 7, by expanding attributes to list of dicts in JSON

    :param list bytelist:
    """
    if archive:
        fp = f_archive_json
        filtered_bytes = [b for b in bytelist if b.level > 7]
    else:
        fp = f_active_json
        filtered_bytes = [b for b in bytelist if b.level <= 7]

    filtered_bytes_expanded = [{'level': b.level, 'question': b.question, 'answer': b.answer} for b in filtered_bytes]

    with open(fp, "w") as f:
        json.dump(filtered_bytes_expanded, f)


def raise_byte_level(byte):
    """
    Increases a byte's commitment level by 1
    :param byte: the class byte instance
    :return: None
    """
    byte.level += 1


def kick_byte_level(byte):
    """
    Decreases a byte's commitment level back to 1, the ground floor
    :param byte: the class byte instance
    :return: None
    """
    byte.level = 1


def edit_byte(byte):
    """
    Allows the user to edit a byte. Automatically demotes byte to level==1

    :param byte:    a byte instance
    """
    os.system("clear")
    print("************SPACEREPS**************")
    print("------------Edit Byte--------------")
    print()

    print("Byte Question: ", byte.question)
    print()
    print("Byte Answer: ", byte.answer)
    print()
    print()
    byte.question = input("Enter new question: ")
    print()
    byte.answer = input("Enter new answer: ")
    print()
    byte.level = 1
    print("Byte Updated!")
    time.sleep(1)


def ask_question(byte, idx, total):
    """
    Quizzes the user on a byte. If they are correct, advance its level. Otherwise demote its level to 1.

    :param byte byte: the class byte instance
    :param int idx:
    :param int total:
    """
    os.system("clear")
    print("************SPACEREPS**************")
    print("-------------Quiz Me---------------")
    print()

    print(f"Question {idx} of {total}\n")
    print(f"[{byte.level}]: {byte.question}")
    input("\n(Press any key to see answer)\n")
    print(byte.answer)
    yn = input("\nWere you correct? (y) or (n): ").lower().strip()[0]

    if yn == "q":
        return False
    elif yn == "e":
        edit_byte(byte)
    elif yn == "y":
        raise_byte_level(byte)
    else:
        kick_byte_level(byte)

    return True


def quiz_me(bytelist, idx):
    """
    Quiz the user on all bytes whose level is include in today's levelRing schedule

    :param list(byte) bytelist:     the list of bytes
    :param int idx:                 today's levelRing index
    """
    todayslvls = level_rings[idx]

    todaysBytes = [b for b in bytelist if b.level in set(todayslvls)]
    shuffle(todaysBytes)
    total = len(todaysBytes)

    for idx, byte in enumerate(todaysBytes):
        if ask_question(byte, idx + 1, total) is False:
            # Terminate early
            return


def new_byte():
    """
    Create, initialize, and return a new byte instance
    :return: byte
    """
    os.system("clear")
    print("************SPACEREPS**************")
    print("----------Add Question-------------")
    print()

    newb = byte()
    newb.question = input("Enter question: ")
    print()
    newb.answer = input("Enter answer: ")
    return newb


def add_bytes(bytelist):
    """
    Extend the bytelist with new questions, prompting the user for each new addition
    :param list(byte) bytelist: list of byte instances
    """
    os.system("clear")
    print("************SPACEREPS**************")
    print("----------Add Question-------------")
    print()

    more = "y"

    while more == "y":
        newb = new_byte()
        bytelist.append(newb)
        print()
        more = input("Would you like to add another question? (y) or (n): ")


def play(bytelist):
    idx = get_level_index(date.today())

    while True:
        os.system("clear")
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
            quiz_me(bytelist, idx)
            del menuopts[1]
        elif choice == 2:
            add_bytes(bytelist)
        elif choice == 3:
            os.system("clear")
            print("Thank you for quizzing!\nSee you tomorrow!")
            time.sleep(1)
            return


def main():
    """
    First retrieves the active list of bytes. 
    Quizzes the user on all bytes that are on today's schedule. 
    Then surveys the user for new bytes to add to the active list.
    Finally, archives any 'graduated' bytes and saves the rest back to disk.
    """
    try:
        bytelist = read_bytes_from_json(archive=False)
    except IOError as e:
        raise e
    play(bytelist)
    write_bytes_to_json(bytelist, archive=True)
    write_bytes_to_json(bytelist, archive=False)


if __name__ == "__main__":
    main()
