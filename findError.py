import os
import csv

def findMsg03ErrorCount():
  TARGET_OUTCO_PATH = "./data/asan/outco/"
  TARGET_DATE = "20220704"
  dbList = os.listdir(TARGET_OUTCO_PATH)

  #with open("./log/renameS3Object.txt", "w+") as writeFile:
  total = 0
  with open("./log/countMsg03.txt", "w+") as writeFile:
    for db in dbList:
      outcoPath = TARGET_OUTCO_PATH + db + "/" + TARGET_DATE
      outcoFileList = os.listdir(outcoPath)
      for outcoFile in outcoFileList:
        if not outcoFile.endswith('msg03.csv'):
          continue

        path = outcoPath+"/"+outcoFile

        try:
          with open(path, newline='\n', encoding='UTF8') as csvfile:
            sparmreader = csv.reader(csvfile, delimiter=',', escapechar="\\", quotechar='"')

            count = sum(1 for line in sparmreader if len(line) > 3) - 1
            if count:
              total += count
              writeFile.write("{0} - {1}\n".format(path, count))
        except Exception as e:
          writeFile.write("ERROR : {0} - {1}\n".format(path, e))

    writeFile.write("total count - {0}\n".format(total))

findMsg03ErrorCount()