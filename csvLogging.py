import logging
import json
import os

# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력 - info level
info_handler = logging.FileHandler('./log/info.log')
info_handler.setFormatter(formatter)
info_handler.setLevel(logging.INFO)
logger.addHandler(info_handler)

error_handler = logging.FileHandler('./log/error.log')
error_handler.setFormatter(formatter)
error_handler.setLevel(logging.ERROR)
logger.addHandler(error_handler)



def error(logData):
    logger.error(logData)


def writeMatchingInfo(logData):
    if type(logData) is dict:
        logger.info(json.dumps(logData));
        with open("./data/matching_info.csv", 'a+') as f:
            f.write(logData["extra_info"]+"\n");
    else:
        logger.info(logData)

