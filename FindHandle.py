import re
import json

line = []
FIND = []
with open("accounts.txt", "r") as inFile:
    for lines in inFile:
        line = str.lower(lines).split()
        print(line)
        for word in line:
            if re.search('@', word):
                FIND.append(re.sub('^.*,@', '', word))
with open("accounts.json", "w") as outFile:
    json.dump(FIND, outFile)