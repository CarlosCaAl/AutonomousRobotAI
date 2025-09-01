import os
import json

PATH = os.path.dirname(__file__) + "/files/"

def read(file):
    file = PATH + file
    with open(file,"r+",encoding="utf-8") as f: content = f.read()
    if ".json" in file: 
        content = json.loads(content)
    return content
    
def write(content,file):
    file = PATH + file
    if not os.path.exists(file): os.system(f"touch {file}")
    with open(file,"r+") as f:
        if type(content) != type(""): json.dump(content,f)
        else: f.write(content)
    