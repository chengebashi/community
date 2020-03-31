import os,time
PAHT = r'static\uploads\filedownAndup'

def filesshow():
    '展示当前目录下所有的文件'
    fileList = os.listdir(PAHT)
    fileSize = []
    fileTime = []
    FILE = []
    for i in fileList:
        size = os.path.getsize(os.path.join(PAHT,i))
        if size/1024 > 1024:
            size = str(round((size/1024/1024),2))+'MB'
        else:
            size = str(round((size / 1024), 2)) + 'KB'
        fileSize.append(size)
        createTime = os.path.getctime(os.path.join(PAHT,i))
        createTime = time.strftime("%Y-%m-%d",time.localtime(createTime))
        fileTime.append(createTime)
    fileNum = len(fileList)
    for i in range(fileNum):
        fileDict = {'name':fileList[i], 'size':fileSize[i], 'time':fileTime[i]}
        FILE.append(fileDict)
    return FILE

