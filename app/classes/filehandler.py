from fastapi import HTTPException
import logging.config
import json
import os

logger = logging.getLogger('uvicorn.error')

class FileHandler:

    def __init__(self):
        self.storage = 'storage/'

    def file_get(self, user_id):

        path = self.storage + user_id + '.json'

        try:
            f = open(path)

        except FileNotFoundError:
            msg = 'File not found...' + path
            logger.error(msg)
            raise HTTPException(status_code=404, detail=msg)

        else:
            with f:
                return json.load(f)

    def file_put(self, user_id, wallet):

        path = self.storage + user_id + '.json'

        try:
            f = open(path, 'w', encoding='utf-8')

        except FileNotFoundError:
            msg = 'File not found...' + path
            logger.error(msg)
            raise HTTPException(status_code=404, detail=msg)

        else:
            with f:
                json.dump(wallet, f, ensure_ascii=False)
                logger.info("The JSON file for user id " + user_id + " is updated.")
                return True
    def file_check(self, user_id):
        path = self.storage + user_id + '.json'
        if os.path.exists(path):
            return True
        else:
            return False
