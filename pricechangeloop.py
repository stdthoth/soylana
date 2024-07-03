import requests
import json
import pandas as pd
import datetime


url = "https://public-api.birdeye.so/defi/tokenlist"
header = {"x-chain":"solana","X-API-KEY": "e3194f932e1846429558b16dc3ef19b4"}

tokens = []
offset = 0
limit = 50
total_tokens = 0
num_tokens = 1000

while total_tokens < num_tokens:
    print("looooopinggg")
    query_params = {"sort_by":"v24hChangePercent","sort_type":"desc","offset":offset ,"limit":limit}
    
    resp = requests.get(url,headers=header,params=query_params)
    if resp.status_code == 200:
        resp_data = resp.json()
        new_tokies = resp_data.get('data',{}).get('tokens',[])
        tokens.extend(new_tokies)
        total_tokens += len(new_tokies)
        offset += limit
    else:
        print("failed to retrieve data",resp.status_code)
        break

df = pd.DataFrame(tokens)

min_liquidity = 2000
min_vol_24h = 2000

df = df.dropna(subset=['liquidity','v24hUSD'])
df = df[(df['liquidity'] >= min_liquidity) & (df['v24hUSD'] >= min_vol_24h)]

drop_columns = ['logoURI']
df =df.drop(columns=drop_columns)

#convert unix time to dd-mm-yy (WAT(West African Time) and create new column
df['lastTradeUnixTime'] = pd.to_datetime(df['lastTradeUnixTime'],unit='s').dt.tz_localize('UTC')

#Move to last column
df = df[[col for col in df if col != 'lastTradeUnixTime'] + ['lastTradeUnixTime']]

#filter out tokies who do not have a trade in the last 1hr
current_time_west_africa = datetime.datetime.now(datetime.timezone.utc)+ datetime.timedelta(hours=1)
one_hour_ago = current_time_west_africa - datetime.timedelta(hours=1)
df = df[df['lastTradeUnixTime'] >= one_hour_ago]

df.to_csv("priceChange_loop.csv")
pd.set_option('display.max_columns',None)
print(df)




