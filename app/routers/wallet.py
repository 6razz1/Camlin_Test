from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.classes.tools import PrettyJSONResponse
from app.classes.filehandler import FileHandler
from pathlib import Path
import requests
import json
import logging.config
import uuid
import os

router = APIRouter()

logger = logging.getLogger('uvicorn.error')

filehandler = FileHandler()

class WalletItem(BaseModel):
    currency: str = Field(pattern=r"^[^a-z]*$")
    value: float

class WalletList(BaseModel):
    wallet: list[WalletItem]
    model_config ={
        "json_schema_extra":
        {
            "examples":
            [
                {
                    "wallet":
                    [
                        {
                            "currency": "EUR",
                            "value": 35.4
                        }
                    ]
                }
            ]
        }
    }

@router.get("/wallet/{user_id}", response_class=PrettyJSONResponse)
async def get_wallet(user_id: str):
    wallet = filehandler.file_get(user_id)
    headers = {'Content-Type': 'application/json'}
    pln_total = 0

    for k in range(len(wallet)):
        url = 'https://api.nbp.pl/api/exchangerates/rates/C/' + wallet[k]['currency'] + '/'
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            rates = json.loads(r.text)
            wallet[k]['PLN_value'] = float(wallet[k]['value'] * rates['rates'][0]['ask'])
            pln_total = pln_total + wallet[k]['PLN_value']
        else:
            wallet[k]['PLN_value'] = None

    return {"wallet": wallet, "PLN_total": pln_total}

@router.get("/wallets", response_class=PrettyJSONResponse)
async def get_wallet_list():
    file_list = os.listdir("app/storage/")

    if 'dummy' in file_list:
        file_list.remove('dummy')

    for k in range(len(file_list)):
        file_list[k] = Path(file_list[k]).stem

    return file_list

@router.post("/wallet", response_class=PrettyJSONResponse)
async def add_wallet_batch(data: WalletList):
    user_id = uuid.uuid4()

    wallet = []
    for v in data.wallet:
        wallet.append(dict(v))

    filehandler.file_put(str(user_id), wallet)

    return {"user_id": user_id, "wallet": wallet}

@router.put("/wallet/{user_id}", response_class=PrettyJSONResponse)
async def edit_wallet_batch(user_id: str, data: WalletList):
    wallet = filehandler.file_get(user_id)

    for item in data.wallet:
        exist = False
        for k in range(len(wallet)):
            if item.currency in wallet[k]['currency']:
                wallet[k]['value'] = item.value
                exist = True
                break
        if not exist:
            wallet.append(dict(item))

    filehandler.file_put(user_id, wallet)

    return {"user_id": user_id, "wallet": wallet}

@router.put("/wallet/add/{currency}/{amount}", response_class=PrettyJSONResponse)
async def edit_wallet_add(currency: str, amount: float, user_id: str | None = None):
    if user_id:
        wallet = filehandler.file_get(user_id)
        exist = False
        for k in range(len(wallet)):
            if currency.upper() == wallet[k]['currency']:
                wallet[k]['value'] = float(wallet[k]['value'] + amount)
                exist = True
                break
        if not exist:
            wallet.append({"currency": currency.upper(), "value": float(amount)})
    else:
        wallet = [{"currency": currency.upper(), "value": float(amount)}]
        user_id = uuid.uuid4()

    filehandler.file_put(str(user_id), wallet)

    return {"user_id": user_id, "wallet": wallet}

@router.put("/wallet/sub/{currency}/{amount}", response_class=PrettyJSONResponse)
async def edit_wallet_add(currency: str, amount: float, user_id: str):
    wallet = filehandler.file_get(user_id)
    exist = False
    for k in range(len(wallet)):
        if currency.upper() == wallet[k]['currency']:
            if wallet[k]['value'] < amount:
                msg = 'The subtraction amount is lower than wallet amount for the currency ' + currency.upper() + '.'
                logger.error(msg)
                raise HTTPException(status_code=400, detail=msg)
            wallet[k]['value'] = float(wallet[k]['value'] - amount)
            exist = True
            break
    if not exist:
        msg = "The currency " + currency.upper() + " doesn't exist in the wallet."
        logger.error(msg)
        raise HTTPException(status_code=404, detail=msg)

    filehandler.file_put(str(user_id), wallet)

    return {"user_id": user_id, "wallet": wallet}
