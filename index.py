
from cmath import log
from operator import truediv
import os
import csv
from posixpath import split

from csvLogging import writeMatchingInfo, error
from shutil import copyfile
import infoLogToJson

BEGIN_DATE_AS = '2019.06.01'
END_DATE_AS = '2022.06.30'


farmDict = {};
def configFarmInfo():
    sourceFile = "./data/farm_source_info.csv"
    matchingFile = "./data/matching_info.csv"

    if os.path.isfile(sourceFile):
        f = open(sourceFile, 'r');
        f.readline();
        
        while True:
            line = f.readline()
            if not line: break
            splitResult = line.strip('\n').split(",")
            farmDict[splitResult[1]] = splitResult[0]
        f.close()
        print("기본 phone 개수 : " + str(len(farmDict)));
    else:
        raise Exception("source 파일이 없습니다.")

    
    if os.path.isfile(matchingFile):
        f = open(matchingFile, 'r');
        while True:
            line = f.readline()
            if not line: break
            try:
                del farmDict[line.strip('\n')]
            except:
                pass
        f.close();
        print("갱신 후 phone 개수 : " + str(len(farmDict)));
    else:
        print("matchingFile 파일 없음")



def processWoosung(outcoFile, salesFile):
    try:

        gcodeDict = {}
        with open(outcoFile, newline='\n', encoding='UTF8') as csvfile:
            sparmreader = csv.reader(csvfile, delimiter=',', escapechar="\\", quotechar='"')
            headerArr = sparmreader.__next__()

            headerDict = {}
            for index, h in enumerate(headerArr):
                headerDict[h] = index;
            
            mb_hp = headerDict['mb_hp']
            mb_tel = headerDict['mb_tel']
            mb_iock = headerDict['mb_iock']
            mb_code = headerDict['mb_code']

            for row in sparmreader:
                target = row[mb_hp] if row[mb_hp] else row[mb_tel] if row[mb_tel] and row[mb_tel].startswith("010") else None
                if target:
                    target = target.replace("-", "").strip();
                    if target in farmDict:
                        # 핸드폰번호, 매입매출구분.
                        gcodeDict[row[mb_iock] + "_" + row[mb_code]] = target
            
            
        with open(salesFile, newline='\n', encoding='UTF8') as csvfile:
            sparmreader = csv.reader(csvfile, delimiter=',', escapechar="\\", quotechar='"')
            headerArr = sparmreader.__next__()

            headerDict = {}
            for index, h in enumerate(headerArr):
                headerDict[h] = index

            sa_gcode = headerDict['sa_gcode']
            sa_iock = headerDict['sa_iock']
            # 우성은 일자 제한 걸어서 내림
            #sa_datetime = headerDict['sa_datetime'];

            for row in sparmreader:
                key = row[sa_iock] + "_" + row[sa_gcode]
                if key in gcodeDict:
                    if gcodeDict[key] in farmDict:
                        logData = {"parm_id": farmDict[gcodeDict[key]], "file": outcoFile, "iock_gcode": key, "extra_info": gcodeDict[key]}
                        writeMatchingInfo(logData)

                        del farmDict[gcodeDict[key]]

                    del gcodeDict[key]
    except Exception as e:
        error({"outcoFile": outcoFile, "salesFile": salesFile})
        error(e)


def runWoosung():
    TARGET_OUTCO_PATH = "./data/woosung/outco/"
    TARGET_SALES_PATH = "./data/woosung/outsales/"
    TARGET_DATE = "202207-05"
    dbList = os.listdir(TARGET_SALES_PATH)
    for db in dbList:
        salesPath = TARGET_SALES_PATH + db + "/"+TARGET_DATE
        outcoPath = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
        salesFileList = os.listdir(salesPath)
        outcoFileList = os.listdir(outcoPath)
        for salesFile in salesFileList:
            if os.path.isfile(salesPath + "/" +salesFile + "_rcv"):
                continue

            prefix = salesFile.split("_")[0]
            
            for outcoFile in outcoFileList:
                if os.path.isfile(outcoPath + "/" +outcoFile + "_rcv"):
                    continue

                if outcoFile.startswith(prefix):
                    processWoosung(outcoPath + "/" +outcoFile, salesPath + "/" + salesFile);


def processAsanOutco(outcoFile):
    try:
        isMsg02 = outcoFile.find("msg02") >= 0

        gcodeDict = {}
        with open(outcoFile, newline='\n', encoding='UTF8') as csvfile:
            sparmreader = csv.reader(csvfile, delimiter=',', escapechar="\\", quotechar='"')
            headerArr = sparmreader.__next__()

            headerDict = {}
            for index, h in enumerate(headerArr):
                headerDict[h] = index;
            
            hphon = headerDict['hphon']
            phon = headerDict['phon']
            gbun = headerDict['gbun'] if isMsg02 else headerDict['mbun']

            maxIdx = max(hphon, phon, gbun)

            for row in sparmreader:
                if maxIdx < len(row):
                    target = row[hphon] if row[hphon] else row[phon] if row[phon] and row[phon].startswith("010") else None
                    if target:
                        target = target.replace("-", "").strip();
                        if target in farmDict:
                            gcodeDict[row[gbun]] = target
            
        return gcodeDict
    except Exception as e:
        error({"outcoFile": outcoFile})
        error(e)

    return None



def processAsanSales(outcoFile, salesFile, gcodeDict):
    try:
        with open(salesFile, newline='\n', encoding='UTF8') as csvfile:
            sparmreader = csv.reader(csvfile, delimiter=',', escapechar="\\", quotechar='"')
            headerArr = sparmreader.__next__()

            headerDict = {}
            for index, h in enumerate(headerArr):
                headerDict[h] = index

            date = headerDict['date']
            gcode = headerDict['gbun'] if salesFile.find('msg05') >= 0 else headerDict['mbun']
            
            for row in sparmreader:
                if row[date] >= BEGIN_DATE_AS and row[date] <= END_DATE_AS:
                    key = row[gcode]
                    if key in gcodeDict:
                        if gcodeDict[key] in farmDict:
                            logData = {"parm_id": farmDict[gcodeDict[key]], "file": outcoFile, "gcode": key, "extra_info": gcodeDict[key]}
                            writeMatchingInfo(logData)

                            del farmDict[gcodeDict[key]]

                        del gcodeDict[key]
    except Exception as e:
        error({"salesFile": salesFile})
        error(e)


def runAsan():
    TARGET_OUTCO_PATH = "./data/asan/outco/"
    TARGET_SALES_PATH = "./data/asan/outsales/"
    TARGET_DATE = "20220704"
    dbList = os.listdir(TARGET_SALES_PATH)
    for db in dbList:
        salesPath = TARGET_SALES_PATH + db + "/" + TARGET_DATE
        outcoPath = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
        salesFileList = os.listdir(salesPath)
        outcoFileList = os.listdir(outcoPath)
        for outcoFile in outcoFileList:
            # 복구버전 파일 있으면 이건 안한다.
            if os.path.isfile(outcoPath + "/" +outcoFile + "_rcv"):
                continue

            gcodeDict = processAsanOutco(outcoPath + "/" +outcoFile)
            if not gcodeDict:
                continue

            isMsg02 = outcoFile.startswith('msg02')
            for salesFile in salesFileList:
                if os.path.isfile(salesPath + "/" +salesFile + "_rcv"):
                    continue

                if isMsg02 and salesFile.startswith('msg05') \
                    or not isMsg02 and salesFile.startswith('msg06'):
                    processAsanSales(outcoPath + "/" +outcoFile, salesPath + "/" + salesFile,  gcodeDict)
                



def testAsan(outcoFilePath, salesFilePath):
    gcodeDict = processAsanOutco(outcoFilePath)
    if gcodeDict:
        processAsanSales(outcoFilePath, salesFilePath, gcodeDict)


configFarmInfo()
#runAsan()
runWoosung()
#infoLogToJson.makeJsonResult()
