#!/usr/bin/python3

import sys
import getopt
import os
import shlex
import shutil
import re
import subprocess
import datetime



def prRed(prt): 
    print("\033[91m%s\033[00m" % prt)

def prBlue(prt):
    print("\033[94m%s\033[00m" % prt)

def prGreen(prt):
    print("\033[92m%s\033[00m" % prt)

def header():
    #print("TV SHOW SORTER")
    print("""

  _______    _______            __           
 /_  __/ |  / / ___/____  _____/ /____  _____
  / /  | | / /\__ \/ __ \/ ___/ __/ _ \/ ___/
 / /   | |/ /___/ / /_/ / /  / /_/  __/ /    
/_/    |___//____/\____/_/   \__/\___/_/     


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
""")
                                                          
    

def debug():
    print("Number of arguments: ", len(sys.argv), 'arguments.')
    print("Argument List:", str(sys.argv))

def logW(m):
    now = datetime.datetime.now()
    logdatetime = str(now.strftime("%Y-%m-%d--%H:%M:%S"))
    filedate = str(now.strftime("%Y-%m-%d"))
    LOGFILE = "/tmp/" + filedate + "-sort.log"
    log = open(LOGFILE, 'a')
    logmsg = logdatetime + " -- : " + m
    log.write(logmsg)
    log.write("\n")
    log.close
       
def validate_init(directory,target):
    print("\nChecking [%s] directory..." % directory)
    if os.path.exists(directory):
        print("\033[92m✓\033[00m OS Path specificed [%s] exists." % directory)
    else:
        print("\033[91mX\033[00m OS Path specified [%s] does not exist." % directory)
        sys.exit(0)
    print("\nChecking [%s] directory..." % target)
    if os.path.exists(target):
        print("\033[92m✓\033[00m OS Path specificed [%s] exists." % target)
    else:
        print("\033[91mX\033[00m OS Path specificed [%s] does not exist." % target)

    file_list = os.listdir(directory)
    print("")
    print("\033[90mValidating file types of files found in:\033[00m %s" % (directory))
    print("\nType:\tValid\tFilename:")
    for f in file_list:
        fextention = f.strip()[-3:].upper()
        if f.endswith(('.avi','.mkv','.mp4')):
            print("%s\t\033[92mVALID\033[00m\t%s%s" % (fextention,directory,f))
        else:
            print("%s\t\033[91mIGNORE\033[00m\t%s%s" % (fextention,directory,f))
    print("")

def validate_dest(target):
    if os.path.exists(target):
        return True
    else:
        yes = {'yes','y', ''}
        no = {'no','n'}
        quit = {'quit','q'}
        choice = input("\t\tCreate new directory? ([Y]es/[N]o/[Q]uit)\n\t\t# ").lower()
        if choice in quit:
            clean_exit()
        if choice in yes:
            try:
                os.makedirs(target)
                msg = "***CREATED \"" + target + "\" DIRECTORY***"
                logW(msg)
                print("\t\t\033[92mCreated directory: %s\033[00m\n" % (target))
            except OSError:
                if os.path.exists(target):
                    pass
                else:
                    raise
        if os.path.exists(target):
            return True
        else:
            return False


def move_files(source_file,full_dest,f,dest,AUTO):
    s = source_file
    d = full_dest
    QUIT = False
    while QUIT == False:
        yes = {'yes','y', ''}
        no = {'no','n'}
        quit = {'quit','q'}

        if AUTO == False:
            print("Suggested:\tMove \033[94m%s\033[00m to \033[94m%s\033[00m ?" % (f,dest))
            print("")
            choice = input("\t\tProceed with moving file into target directory? ([Y]es/[N]o/[Q]uit)\n\t\t# ").lower()

            if choice in yes:
                shutil.move(s,d)
                msg = "moved %s to %s" % (s,d)
                logW(msg)
                print("\n\t\tMoved %s \n\t\t\tto\t\t\n \t\t%s" % (s,d))
                return True

            elif choice in no:
                print("\t\tIgnoring file... moving on to next valid file")
                return False

            elif choice in quit:
                QUIT = True
                clean_exit()

            else:
                sys.stdout.write("Please respond with 'yes' or 'no' or 'quit'")
        else: 
            shutil.move(s,d)
            print("\n\t\tMoved %s \n\t\t\tto\t\t\n \t\t%s" % (s,d))
            msg = "moved %s to %s" % (s,d)
            logW(msg)
            return True

    
        

def sort_files(directory,target,AUTO):
    file_list = os.listdir(directory)
    for f in file_list:
        if f.endswith(('.avi','.mkv','.mp4', '.mpg')):
            # Regex for TV Show Pattern Matching - this is the magic
            tv = re.findall(r"(.*?)[ |.]S([\d+]{1,2})E([\d+]{1,2})[ |.]([\d+]{3,4}p|)", f, re.I)
            for show in tv:
                sname = show[0]
                season = show[1]
                episode = show[2]
                source_file =  directory + f
                d = target + sname.replace("."," ").title() + "/" + "Season " + season + "/"
                full_dest = d + f

                print("")
                print("Source File:\t%s" % (source_file))
                print("Destination:\t%s" % (d))
                DEST_EXIST = validate_dest(d)
                if DEST_EXIST == True:
                    print("Dir Exists?:\t\033[92mTarget Folder Exists\033[00m")
                    move_files(source_file,full_dest,f,d,AUTO)
                else:
                    print("Dir Exists?:\t\033[91mTarget Folder Doesn't Exist. Skipping...\033[00m") 
                print("")

            

def fail_out(err_msg):
    msg = "Something went wrong: " + err_msg
    prRed(msg)
    sys.exit(0)

def clean_exit():
    print("\n\n\tQuitting - Goodbye :)")
    sys.exit(0)

def main(argv):
    directory = ''    
    target = ''
    logfile = ''
    VALIDATE = False
    SORT = False
    DEBUG = False
    AUTO = False

    header()

    try:
        opts, args = getopt.getopt(argv,"hd:t:vsa",["directory=","target=", "validate","sort","auto"])
    except getopt.GetoptError:
        print(str(sys.argv))
        print("%s -d <working_directory> -t <target_base_directory>" % sys.argv[0])
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("%s -d <working_directory> -t <target_base_directory>" % sys.argv[0])
            sys.exit()
        if opt in ("-d", "--directory"):
            if os.path.exists(arg):
                if arg.strip()[-1] == "/":
                    directory = arg
                else:
                    directory = arg + "/"
            else:
                err_msg = "OS Path " + arg + " specified does not exist."
                fail_out(err_msg)
        
        if opt in ("-t","--target"):
            if os.path.exists(arg):
                if arg.strip()[-1] == "/":
                    target = arg
                else:
                    target = arg + "/"
            else:
                err_msg = "OS Path " + arg + " specified does not exist."
                fail_out(err_msg)


        if opt in ("-v","--validate"):
            VALIDATE = True

        if opt in ("-s","--sort"):
            print("Sorting directory")
            SORT = True

        if opt in ("-a","--auto"):
            print("Auto sort selected")
            AUTO = True


    if DEBUG == True:
        debug()

    if VALIDATE == True:
        validate_init(directory,target)

    if SORT == True:
        sort_files(directory,target,AUTO)

    print("\n\n")

    prGreen("Complete")
    print("\n\n")

if __name__ == '__main__':
    main(sys.argv[1:])


