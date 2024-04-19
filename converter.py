from os import getenv
import requests
import aiohttp
from fastapi import HTTPException

ALPHAVANTAGE_APIKEY = getenv('ALPHAVANTAGE_APIKEY')

#chamada sync
def sync_converter(from_currency: str, to_currency: str, price: float):
  url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}'
  
  try:
    response = requests.get(url=url)
  except Exception as error:
    raise HTTPException(status_code=400, detail=error)
  
  data = response.json()
  
  if "Realtime Currency Exchange Rate" not in data:
    raise HTTPException(status_code=400, detail= f'Realtime Currency Exchange Rate not in response {data}')
  
  exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
  return {to_currency: price * exchange_rate}

#chamada assync
async def async_converter(from_currency: str, to_currency: str, price: float):
  url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}'
  
  try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                data = await response.json()
                
                if "Realtime Currency Exchange Rate" not in data:
                    raise HTTPException(status_code=400, detail='Invalid response from API')
                
                exchange_rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
                return {to_currency: price * exchange_rate}
                
  except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))