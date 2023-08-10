import os, json, fnmatch

def grep_file(file: str, target):
    with open("/home/kussi/.minecraft/assets/indexes/"+file, "r") as f:
        jsontext: str = f.read()
        jsondict: dict = json.loads(jsontext)
    
    keys: list = list(jsondict['objects'].keys())

    filtered: list = fnmatch.filter(keys, "*"+target+"*")
    print(filtered)



if __name__ == '__main__':
    target: str = input("What to grep for? ")
    json_files: list = os.listdir("/home/kussi/.minecraft/assets/indexes")

    for file in json_files:
        if file.endswith("3.json"):
            grep_file(file, target)
