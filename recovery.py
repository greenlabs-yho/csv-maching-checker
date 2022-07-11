import os;


def recoveryCSVPattern():
    TARGET_OUTCO_PATH = "./data/asan/outco/"
    TARGET_DATE = "20220704"
    dbList = os.listdir(TARGET_OUTCO_PATH)
    for db in dbList:
        outcoPath = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
        outcoFileList = os.listdir(outcoPath)
        for outcoFile in outcoFileList:
            if outcoFile.find("msg03") >= 0:
                with open(outcoPath+"/"+outcoFile, newline='\n', encoding='UTF8') as csvfile:
                    line = csvfile.read()
                    if line.find("?,") >= 0:
                        newLine = line.replace('?,', '?",')
                        with open(outcoPath+"/"+outcoFile+"_rcv", "w+", newline='\n', encoding='UTF8') as writeFile:
                            writeFile.write(newLine)



def recoveryCSVPatternToFileList(fileList):
    for file in fileList:
        with open(file, newline='\n', encoding='UTF8') as csvfile:
            data = csvfile.read()
            if data.find("?,") >= 0:
                newData = data.replace('?,', '?",')
                with open(file + "_rcv", "w+", newline='\n', encoding='UTF8') as writeFile:
                    writeFile.write(newData)




def recoveryNullBytes():
    recoveryFiles = [{'outcoFile': './data/asan/outco/erp_bjb2308/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_bu2020/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_chi2409/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_jang8080/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_jjh8211/20220704/msg03.csv_rcv'}
    ,{'outcoFile': './data/asan/outco/erp_jsw02381/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_ksc40233/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_kyh8677/20220704/msg02.csv'}
    ,{'outcoFile': './data/asan/outco/erp_man7048/20220704/msg02.csv'}
    ]

    for obj in recoveryFiles:
        f1 = open(obj["outcoFile"], 'rb')
        data = f1.read()
        f2 = open(obj["outcoFile"] + "_rcv", 'wb')
        f2.write(data.replace(b'\0', b''))
        f2.close()

        if 'salesFile' in obj:
            f1 = open(obj["salesFile"], 'rb')
            data = f1.read()
            f2 = open(obj["salesFile"] + "_rcv", 'wb')
            f2.write(data.replace(b'\0', b''))
            f2.close()



def deleteFiles(basePath, targetDate):
    dbList = os.listdir(basePath)
    for db in dbList:
        datePath = basePath + db + "/" + targetDate
        fileList = os.listdir(datePath)
        for file in fileList:
            if file.endswith('_recover'):
                os.remove(datePath + "/" + file)



def makeCLIRecoveryFiles():
    TARGET_OUTCO_PATH = "./data/asan/outco/"
    TARGET_SALES_PATH = "./data/asan/outsales/"
    TARGET_DATE = "20220704"
    dbList = os.listdir(TARGET_SALES_PATH)

    #with open("./log/renameS3Object.txt", "w+") as writeFile:
    with open("./log/uploadS3Object.txt", "w+") as writeFile:
        for db in dbList:
            salesPath = TARGET_SALES_PATH + db + "/" + TARGET_DATE
            outcoPath = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
            salesFileList = os.listdir(salesPath)
            outcoFileList = os.listdir(outcoPath)
            for outcoFile in outcoFileList:
                if os.path.isfile(outcoPath + "/" +outcoFile + "_rcv"):
                    continue

                if outcoFile.endswith("_rcv"):
                    #tmp = (outcoPath + "/" +outcoFile).replace("_rcv", "").replace('./data', 's3://ws-pipeline-bucket-b2b-temp')
                    #writeFile.write("aws s3 mv {0} {1}\r\n".format(tmp, tmp+".20220707_105100"))
                    #writeFile.write("aws s3 cp {0} {1}\r\n".format(outcoPath + "/" +outcoFile, tmp))
                    csvName = (outcoPath + "/" +outcoFile).replace("_rcv", "")
                    timeName = (outcoPath + "/" +outcoFile).replace("_rcv", "") + ".20220707_170200"
                    os.rename(csvName, timeName)
                    os.rename(outcoPath + "/" + outcoFile, csvName)
                    print(csvName)

            for salesFile in salesFileList:
                if os.path.isfile(salesPath + "/" +salesFile + "_rcv"):
                    continue

                if salesFile.endswith("_rcv"):
                    #tmp = (salesPath + "/" +salesFile).replace("_rcv", "").replace('./data', 's3://ws-pipeline-bucket-b2b-temp')
                    #writeFile.write("aws s3 mv {0} {1}\r\n".format(tmp, tmp+".20220707_105100"))
                    #writeFile.write("aws s3 cp {0} {1}\r\n".format(outcoPath + "/" +outcoFile, tmp))
                    csvName = (salesPath + "/" +salesFile).replace("_rcv", "")
                    timeName = (salesPath + "/" +salesFile).replace("_rcv", "") + ".20220707_170200"
                    os.rename(csvName, timeName)
                    os.rename(salesPath + "/" + salesFile, csvName)
                    print(csvName, timeName, salesPath + "/" + salesFile)


def checkCSVPattern():
    TARGET_OUTCO_PATH = "./data/asan/outsales/"
    TARGET_DATE = "20220704"
    dbList = os.listdir(TARGET_OUTCO_PATH)
    for db in dbList:
        path = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
        fileList = os.listdir(path)
        for file in fileList:
            if os.path.isfile(path + "/" + file + "_rcv"):
                continue

            with open(path+"/"+file, newline='\n', encoding='UTF8') as csvfile:
                line = csvfile.read()
                if line.find("?,") >= 0:
                    print(path+"/"+file)




makeCLIRecoveryFiles()


