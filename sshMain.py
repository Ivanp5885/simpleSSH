import subprocess
import os

def loadCfg():
    current_script = os.path.abspath(__file__) #current dir
    parent_directory = os.path.dirname(current_script) #parent dir
    directory_path = f'{parent_directory}/configs' #config dir

    #SELECT CONFIG
    entries = os.listdir(directory_path)
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory_path, entry))] #get configs
    
    cfgName=""
    if len(files) < 1:
        print("No configs in parentDir/configs/*\n") #error if no config found
    elif len(files) == 1:
        print("Only 1 file found in configs folder. Automatically selecting it...") #auto-choose if only 1 config is in configs dir
        cfgName=files[0]
    else:
        print("Please select the index number of the config file you want to use.")
        for i in range(len(files)): #user chooses
            print(str(str(i+1) + ". " + files[i]))
        cfgName=str(files[int(input())-1])
    print("Successfully selected "+cfgName+" as config file.")
    return(f'{directory_path}/{cfgName}')

def selectHost():
    cfgPath=loadCfg()
    names=[]
    hostName = ""
    verbose = ""
    with open(cfgPath, "r") as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"): #ignore comments
                verbose=verbose+"\n"+line
                if line[:5] == "NAME=":
                    names.append((line[5:])[:-1])# [:-1] to remove \n

    while hostName=="":
        if len(names) < 1:
            print("No names in config\n") #error if no name found
            return "ERROR"
        elif len(names) == 1:
            print("Only 1 file found in config. Automatically selecting it...") #auto-choose if only 1 name is in config
            hostName=names[0]
        else:
            print("Please select the index number of the name you want to use. TYPE -v FOR VERBOSE OUTPUT (ignoring comments).")
            for i in range(len(names)): #user chooses
                print(str(str(i+1) + ". " + names[i]))
            choice = input()
            if choice == "-v":
                print(verbose)
            else:
                choice=int(choice)
                hostName=str(names[int(choice)-1])
                choice-=1
        print("Successfully selected "+hostName+" as name.") #SELECTED NAME, now load ip,port etc.
        
        count=1
        start=0
        HOST=""
        USER=""
        PORT=0
        KEY=""
        with open(cfgPath, "r") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"): #ignore comments
                    if line[:5] == "NAME=":
                        if start !=0:
                            break #dont check unnecesarry lines
                        if line.split("=", 1)[1].strip() == hostName:
                            start=count
                    if start !=0:
                        if line[:9] == "    HOST=":
                            print(f"IP FOUND. -> {line.split("=", 1)[1].strip()}")
                            HOST = line.split("=", 1)[1].strip()
                        if line[:9] == "    USER=":
                            print(f"USERNAME FOUND. -> {line.split("=", 1)[1].strip()}")
                            USER = line.split("=", 1)[1].strip()
                        if line[:9] == "    PORT=":
                            print(f"PORT FOUND -> {line.split("=", 1)[1].strip()}")
                            PORT = line.split("=", 1)[1].strip()
                        if line[:8] == "    KEY=":
                            print(f"KEY FOUND -> {line.split("=", 1)[1].strip()}")
                            KEY = line.split("=", 1)[1].strip()
                count = count + 1
    return HOST, USER, PORT, KEY

def ssh():
    returned = selectHost()
    HOST, USER, PORT, KEY = returned
    if HOST=="":
        print("IP NOT FOUND!")
        print("####################")
        print("# CODE DID NOT RUN #")
        print("####################")
        print("\nIts really important to use correct indent/tabulation in the config file.")
        return "ERROR"
    if USER=="":
        print("USERNAME NOT FOUND, USING DEFAULT. -> root")
        USER = "root"
    if PORT==0:
        print("PORT NOT SPECIFIED. USING 22.")
        port = 22

    if KEY != "":
        print("Attempting authentication using key.")
        sshKey = f'ssh -i {KEY} {USER}@{HOST} -p {PORT}'
        cmd_command = f'start cmd.exe /K "{sshKey}"'
        subprocess.Popen(cmd_command, shell=True)

    if KEY=="":
        print("NO KEY FOUND, UNABLE TO INITIATE PASSWORDLESS AUTHENTICATION. Trying regular connection.")
        sshKey = f'ssh {USER}@{HOST} -p {PORT}'
        cmd_command = f'start cmd.exe /K "{sshKey}"'
        subprocess.Popen(cmd_command, shell=True)

#MAIN
ssh()
