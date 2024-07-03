# connect to birdeye

#GET TOKEN PRICE 

#GET TOKEN MARKETCAP

#GET TOKEN VOLUME 

#GET TOKEN 24-HR TRADES 

# GET TVL

import requests
import pandas as pd
import pprint as pp

url = "https://public-api.birdeye.so/defi/price?address=8vCAUbxejdtaxn6jnX5uaQTyTZLmXALg9u1bvFCAjtx7"
header = {"x-chain":"solana","X-API-KEY": "e3194f932e1846429558b16dc3ef19b4"}



response = requests.get(url,headers=header)

if response.status_code == 200:
    data = response.json()
    pp.pprint(data)
    #creating a dataframe
    dataframe = pd.DataFrame(data)

    #save to csv file 
    csv_fp = 'cobain.csv'
    dataframe.to_csv(csv_fp,index=False)
    print("Data Saved to {csv_fp}")
    #print(dataframe)
else:
    print("failed to retrieve data",response.status_code)



