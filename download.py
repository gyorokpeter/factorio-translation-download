import requests
import json
import os

language="hu"

def getCfgFiles(d):
    result={}
    files=os.listdir(d)
    if d.endswith('locale/'+language):
        result.update({x:d+'/'+x for x in files if x.endswith('.cfg')})
    for f in files:
        fp=d+'/'+f
        if os.path.isdir(fp):
            result.update(getCfgFiles(fp))
    return result

cfgFiles=getCfgFiles("D:/Program Files/Steam/steamapps/common/Factorio")
if 0 == len(cfgFiles):
    print("no .cfg files - is path correct?")
    exit(1)


userConfig=json.load(open("config.json"))
auth={"Authorization": "Bearer "+userConfig["token"]}

print("get files")
res=json.loads(requests.get("https://crowdin.com/api/v2/projects/58156/files", headers=auth).content)
files={x["data"]["id"]:x["data"]["name"] for x in res["data"]}

print("get source strings")
allStrings={}
def addStrings(strs):
    for x in strs["data"]:
        allStrings[x["data"]["id"]]={"strId":x["data"]["identifier"], "fileId":x["data"]["fileId"]}

print("offset=0")
strs=json.loads(requests.get("https://crowdin.com/api/v2/projects/58156/strings?limit=500", headers=auth).content)
addStrings(strs)

offset=0
while 0<len(strs["data"]):
    offset+=500
    print("offset="+str(offset))
    strs=json.loads(requests.get("https://crowdin.com/api/v2/projects/58156/strings?limit=500&offset="+str(offset), headers=auth).content)
    addStrings(strs)

print("get translations")
allTrans={}
def addTranslations(trans):
    for x in trans["data"]:
        allTrans[x["data"]["stringId"]]=x["data"]["text"]

print("offset=0")
trans=json.loads(requests.get("https://crowdin.com/api/v2/projects/58156/languages/"+language+"/translations?limit=500", headers=auth).content)
addTranslations(trans)
offset=0
while 0<len(trans["data"]):
    offset+=500
    print("offset="+str(offset))
    trans=json.loads(requests.get("https://crowdin.com/api/v2/projects/58156/languages/"+language+"/translations?limit=500&offset="+str(offset), headers=auth).content)
    addTranslations(trans)

content={}
for k,v in allTrans.items():
    sd=allStrings[k]
    file=files[sd["fileId"]]
    loc=sd["strId"].split(":")
    if 1==len(loc):
        loc=['']+loc
    heading=loc[0].split("\n")[0]
    ky=loc[1].split("\n")[0]
    if not file in content:
        content[file]={}
    if not heading in content[file]:
        content[file][heading]={}
    content[file][heading][ky]=v

def iniSection(cont):
    result=[]
    kys=list(cont.keys())
    kys.sort()
    for ky in kys:
        result.append(ky+"="+cont[ky])
    result.append('')
    return result

def getFileContent(cont):
    output=[]
    if '' in cont:
        output += iniSection(cont[''])
        del cont['']
    sections=list(cont.keys())
    sections.sort()
    for k in sections:
        output += ["["+k+"]"]+iniSection(cont[k])
    return output

for file,cont in content.items():
    cfgFileName=cfgFiles[file.split(".")[0]+".cfg"]
    print("saving "+cfgFileName)
    output=getFileContent(cont)
    outstr="\n".join(output)
    open(cfgFileName, "w", encoding="utf-8").write(outstr)
