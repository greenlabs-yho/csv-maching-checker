import json

def makeJsonResult():
    KEYWORD = ' - root - INFO - '
    startPosition = len('2022-07-06 11:10:43,979 - root - INFO - ')

    BEGIN_FORMAT = '''{
        "_comment": {
            "parm_id": "팜모닝 아이디",
            "file": "원본 우성 데이터 경로",
            "iock_gcode": "우성 ERP 고객 코드",
            "extra_info": "핸드폰번호 (매칭키)"
        },
        "data": [
    '''

    END_FORMAT = '''
        ]
    }
    '''


    with open("./log/info.log", 'r', newline='\n', encoding='UTF8') as readFile:
        with open("./log/target_matching_result.json", 'w', newline='\n', encoding='UTF8') as writeFile:
            writeFile.write(BEGIN_FORMAT)
            while True:
                line = readFile.readline()
                if not line: break
                if line.find(KEYWORD) > 0:
                    loadData = json.loads(line.strip('\r\n')[startPosition:])
                    splitStrs = json.dumps(loadData, sort_keys=True, indent=4).split('\n')

                    newData = ''
                    for itemline in splitStrs:
                        newData += " "*8 + itemline + "\n"
                    
                    writeFile.write(newData[:-1] + ",\n")

            writeFile.seek(writeFile.tell() - 2)
            writeFile.write(END_FORMAT)