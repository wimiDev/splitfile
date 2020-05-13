# -*- coding: utf-8 -*-
import sys, os, re
import time
import shutil
import getopt
import zipfile
import hashlib
import json

PACK_SIZE = 1 * 1024 * 1024

#处理不同平台上字符串中文转码
def getCNTrueStr(badStr):
    if sys.platform == 'win32':
        badStr = unicode(badStr, "gb2312").encode("utf-8")
    return badStr

#文件拆包
def unpack(filePath):
    if filePath and os.path.exists(filePath) :
        fileObj = open(filePath, 'rb')
        fileSize = os.path.getsize(filePath)
        pointer = 0
        idx = 1
        while pointer <= fileSize :
            fileObj.seek(pointer)
            start = pointer
            readSize = PACK_SIZE
            if pointer + PACK_SIZE > fileSize:
                readSize = fileSize - pointer
            pointer = pointer + PACK_SIZE
            last = pointer
            fileData = fileObj.read(readSize)
            dest = ''
            destName = os.path.basename(filePath+ str(idx) +".doc")
            writeObj = open(destName, 'wb')
            writeObj.write(os.path.basename(filePath) + '\n')
            writeObj.write(str(start) + '\n')
            writeObj.write(str(last) + '\n')
            writeObj.write(fileData)
            writeObj.close()
            idx = idx + 1
        fileObj.close()

#文件合并
def pack(path):
    fileList = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(dirpath, filename)
            path = path.replace("\\", "/")
            fileList.append(path)
    def cmp(a, b):
        return a < b
    fileList.sort(cmp)
    for fileName in fileList:
        path = fileName
        fileObj = open(path, 'rb')
        fileSize = os.path.getsize(path)
        orgName = fileObj.readline().replace('\n','').replace('\r', '')
        start = fileObj.readline().replace('\n','').replace('\r', '')
        last = fileObj.readline().replace('\n','').replace('\r', '')
        print orgName, start, last
        data = fileObj.read()
        dest = ''
        destName = os.path.join(dest, orgName)
        orgObj = open(orgName, 'ab')
        orgObj.seek(long(start))
        orgObj.write(data)
        orgObj.close()
        fileObj.close()

def main():
    try:
        options,args = getopt.getopt(sys.argv[1:],"hupd:", ["help","unpack=","pack=", "dest="])
    except getopt.GetoptError:
        print 'get param error！'
        sys.exit()
    isPack = False
    dest = ''
    for name,value in options:
        if name in ("-h", "--help"):
            usage()
        if name in ("-u", "--unpack"):
            isPack = False
        if name in ("-p", "--pack"):
            isPack = True
        if name in ("-d", "--dest"):
            dest = value
    if isPack :
        pack(dest)
    else:
        unpack(dest)

if __name__ == "__main__":
    main()