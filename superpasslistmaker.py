from colorama import Fore
import os
from pathlib import Path
from itertools import product
import shutil
import threading
import time

# Define color options for later
def printblue(text, endarg="\n", reset=True):
    if reset:
        print(f"{Fore.BLUE}{text}{Fore.RESET}", end=endarg)
    else:
        print(f"{Fore.BLUE}{text}", end=endarg)

def printred(text, endarg="\n", reset=True):
    if reset:
        print(f"{Fore.RED}{text}{Fore.RESET}", end=endarg)
    else:
        print(f"{Fore.RED}{text}", end=endarg)

def printgreen(text, endarg="\n", reset=True):
    if reset:
        print(f"{Fore.GREEN}{text}{Fore.RESET}", end=endarg)
    else:
        print(f"{Fore.GREEN}{text}", end=endarg)

def printyellow(text, endarg="\n", reset=True):
    if reset:
        print(f"{Fore.YELLOW}{text}{Fore.RESET}", end=endarg)
    else:
        print(f"{Fore.YELLOW}{text}", end=endarg)

def blue(text, reset=True):
    if reset:
        return(f"{Fore.BLUE}{text}{Fore.RESET}")
    else:
        return(f"{Fore.BLUE}{text}")
    
def red(text, reset=True):
    if reset:
        return(f"{Fore.RED}{text}{Fore.RESET}")
    else:
        return(f"{Fore.RED}{text}")

def green(text, reset=True):
    if reset:
        return(f"{Fore.GREEN}{text}{Fore.RESET}")
    else:
        return(f"{Fore.GREEN}{text}")

def yellow(text, reset=True):
    if reset:
        return(f"{Fore.YELLOW}{text}{Fore.RESET}")
    else:
        return(f"{Fore.YELLOW}{text}")

reset = Fore.RESET


def loadingscreen():
    percent = 0
    while True:
        if percent < 100:
            cursize = os.path.getsize(passfile)
            percent = (cursize / estspace) * 100
            barempty = " " * 100
            bar = barempty.replace(" ", "#", int(percent))
            print(f"[{bar}] {round(percent, 1)}%", end="\r")
            time.sleep(0.2)
        else:
            exit()
    
lst = threading.Thread(target=loadingscreen)
lst.daemon = True


def main():
    
    # GET KEYWORDS FROM INPUT
    kwlist = input(blue(f"[?] Input keywords seperated by commas\n[Keywords]: {yellow('', reset=False)}", reset=False)).split(", ")
    printyellow('\n[INFO] Keywords: ', reset=False, endarg="\n=================\n")
    for kw in range(1, len(kwlist) + 1):
        print(f"[{kw}] {kwlist[kw-1]}")
    print("=================" + reset)

    # CREATE PASSWORD LIST
    savepath = input(blue(f'\n[?] In which path do you want the password list to be saved in ? (Leaving empty will save the list in the script\'s directory)\n[Path]: {yellow("", reset=False)}', reset=False))
    print(reset, end="")

    if os.path.isfile(savepath) and savepath != "":
        printred("[ERROR] Provided path is a file, not a directory")
    elif not os.path.isdir(savepath) and savepath != "":
        printred("[ERROR] Invalid path")
    else:
        resultsnum = 1

        if savepath == "":
            while True:
                newresultpath = os.path.join(os.path.abspath(__file__), "..", f"PasswordList{resultsnum}.txt")
                if Path(newresultpath).exists():
                    resultsnum += 1
                else:
                    Path(newresultpath).touch()
                    break
        else:
            while True:
                newresultpath = os.path.join(savepath, "..", f"PasswordList{resultsnum}.txt")
                if Path(newresultpath).exists():
                    resultsnum += 1
                else:
                    Path(newresultpath).touch()
                    break
        
        global passfile 
        passfile = newresultpath

        # PASSWORD MAKING FACTORY, oompa loompa whoopity doo, when we're in the factory some passwords we do...
        characters1 = "!@$ "
        characters2 =  "0123456789! "
        characters3 = "!# "

        freespace = int(shutil.disk_usage("/")[2])

        totalkwlen = 0
        for kw in kwlist:
            totalkwlen += len(kw)

        tbused = len(kwlist) * (len(characters1)) * (len(characters2)**6) * (len(characters3)) * (1 + totalkwlen + 6 + 1)
        if freespace - tbused < 1073741824: # If (the space left after operation - 1GB (just to be safe)) is less than 0, exit the program
            printred("[ERROR] Not enough space left on disk, terminating program...")
            exit()
        else:
            global estspace 
            estspace = tbused
            printred(f'[WARNING] The size of the password list will be approx. {yellow(tbused // 1024**2, reset=False)} MB')
            printred(f'[WARNING] {yellow((freespace - tbused) // 1024**2, reset=False)} MB {red("will be left on this disk after the operation")}')

        invalidapproval = True
        
        while invalidapproval:
            printred("""
                Continue operation?
            """, endarg="", reset=False)
            approval = input(f"      [Yes/No]: {yellow('', reset=False)}").lower()
            if approval == "yes":
                invalidapproval = False
                printred("\n[WARNING] Exiting the program at this time will terminate the current operation and you will have to start over again")
                printyellow("[INFO] Please wait... ")
                lst.start()
                combinations1 = [' '.join(i) for i in product(characters1, repeat=1)]
                combinations2 = [' '.join(i) for i in product(characters2, repeat=6)]
                combinations3 = [[' '.join(i) for i in product(characters3, repeat=1)]]
                for keyword in kwlist:
                    for combination1 in combinations1:
                        combination1 = combination1.replace(" ", "")
                        for combination2 in combinations2:
                            combination2 = combination2.replace(" ", "")
                            for combination3 in combinations3:
                                open(passfile, "a").write(f"{combination1}{keyword}{combination2}{combination3}\n")
                printyellow(f"[INFO] The passwords file is saved in {passfile}")
                printgreen("[SUCCESS] Press ENTER to close the program...")
                input()
            elif approval == "no":
                raise(KeyboardInterrupt)
            else:
                printred("\n[ERROR] Please answer with a Yes or a No to proceed with the operation...")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        printred("\n[ERROR] Exiting...")


""" 

TODO:
    SEMI-IMPORTANT: Add argument functionality 
        -Add an intensity level to the password making (lower might have the 2ndcomb ex. marks just in the last few digits)
    Have threads do some work simultaneously for every keyword ? - Just a suggestion

"""