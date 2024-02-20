import sys
import os #necessary for Windows to deal with env variables

args = sys.argv #argv is a list. Starting from program name, all arguments will be part of this. uses space as delimiter
arg = args[1] #
prog_file = args[0] #

print(f'Hello {arg} from {prog_file}')  #prog_file will be hy.py (whatever the program file is). args [1] will be whatever we type after "python 'hw.py'" 

host = os.environ.get('HOST')  #type(os.environ)...<class 'os.Environ'>
print(f'Connecting to {host}') #f has to present to allow arguments/variables to be passed into the string


#type python 'runtime arguments example.py' World into temrinal

# reason to use runtime args/environment levels example)
    #say we have 2 different dbs and environments we use the app
        # appdev -> appdbdev (retail_db, retail_user, retaildevpassword) #server db is running
        # appuat -> appdbuat (reatil_db, retail_user, retailapppassword) #usually password is different for prod server. devs can get access (usually read-only) to see whats going on 