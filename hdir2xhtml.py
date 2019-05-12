import sys
import os
import subprocess
import shutil
from xml.dom.minidom import parseString

print("dir2html version 1.0.0")

if(len(sys.argv)!=2):
    print("Usage: # python " + sys.argv[0] + " directory name")
    quit() 

path = sys.argv[1]
if(not os.path.isdir(path)):
    print(path, "is not a directory")
    quit()

module_dir = os.path.split(os.path.normpath(sys.argv[0]))[0]
if(module_dir == ""):
    module_dir = "./"
html_string = ""

with open(module_dir + "/index_base.xhtml") as f:
    html_string = f.read()

outDir = path + ".dat"
os.makedirs(outDir, exist_ok = True)

doc = parseString(html_string)
title = doc.getElementsByTagName("title")[0]
body = doc.getElementsByTagName("body")[0]
header = doc.createElement("header")
titleText = os.path.split(os.path.normpath(path))[1]
header.appendChild(doc.createTextNode(titleText))
title.appendChild(doc.createTextNode(titleText))
body.appendChild(header)

def scan_dir(dir,head):
    ul = doc.createElement("ul")
    fileCount = 0
    dirCount = 0

    #first, parse directory
    dirList = []
    fileList = []
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):
            fileList.append(name)
        else:
            dirList.append(name)

    for pDir in dirList:
        path = os.path.join(dir, pDir)
        li = doc.createElement("li")
        li.appendChild(doc.createTextNode(pDir))
        li.appendChild(scan_dir(path,head + "d" + str(dirCount)))
        ul.appendChild(li)
        dirCount += 1

    for pFile in fileList:
        path = os.path.join(dir, pFile)
        li = doc.createElement("li")
        a = doc.createElement("a")
        ext = os.path.splitext(pFile)[1]
        dst = outDir + "/" + head + "f" + str(fileCount)  + ext
        shutil.copyfile(path, dst)
        a.setAttribute("href", dst)
        a.setAttribute("download", pFile)
        a.appendChild(doc.createTextNode(pFile))
        li.appendChild(a)
        ul.appendChild(li)
        print(path)
        fileCount += 1

    return ul
body.appendChild(scan_dir(path, ""))

with open(path + ".xhtml", "w") as f:
    doc.writexml(f)
