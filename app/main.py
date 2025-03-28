from fastapi import FastAPI, HTTPException
from app.classes.tools import PrettyJSONResponse
from .routers import wallet
import logging.config

logger = logging.getLogger('uvicorn.error')
logFormatter = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")
fileHandler = logging.handlers.RotatingFileHandler(filename='app/logs/camlin.log', maxBytes=1000000, backupCount=10)
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

app = FastAPI()
app.include_router(wallet.router)

@app.get("/", response_class=PrettyJSONResponse)
def read_root():
    raise HTTPException(status_code=404, detail='Not found.')
