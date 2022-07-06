
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




