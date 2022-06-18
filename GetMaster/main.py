import json
import urllib.request
import pandas as pd
import sys



def main(output_filepath):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    url = f'https://opendata.resas-portal.go.jp/api/v1/prefectures'

    # GET DATA
    req = urllib.request.Request(url, headers=api_key)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        
    # EDIT DATA
    d = json.loads(data.decode())['result']
    df = pd.DataFrame(d)
    print(df)

    df.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/MasterPrefectures.csv'))