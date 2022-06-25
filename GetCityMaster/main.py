import json
import urllib.request
import pandas as pd
import sys
import time


def main(output_filepath):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    
    df_cityCode = pd.DataFrame()
    for prefCode in range(1,48):
        url = f'https://opendata.resas-portal.go.jp/api/v1/cities?prefCode={prefCode}'

        req = urllib.request.Request(url, headers=api_key)

        with urllib.request.urlopen(req) as response:
            data = response.read()

        d = json.loads(data.decode())

        df_tmp =pd.DataFrame(d['result'])
        df_cityCode = pd.concat([df_cityCode, df_tmp])
        time.sleep(0.1)

    df_cityCode.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/MasterCity.csv'))