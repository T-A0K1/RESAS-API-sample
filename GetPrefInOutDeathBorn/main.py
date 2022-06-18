import json
import urllib.request
import pandas as pd
import sys

# 出生数・死亡数／転入数・転出数
# https://opendata.resas-portal.go.jp/docs/api/v1/population/sum/estimate.html

def main(output_filepath, prefCode, cityCode = '-'):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    df_output = pd.DataFrame()
    
    # TranslateprefCode
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]  
    
    for prefCodeTmp in prefCode_list:
        url = f'https://opendata.resas-portal.go.jp/api/v1/population/sum/estimate?cityCode={cityCode}&prefCode={prefCodeTmp}'
        # GET DATA
        req = urllib.request.Request(url, headers=api_key)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # EDIT DATA
        d = json.loads(data.decode())['result']['data']
        for i in range(1,5):
            df_tmp = pd.DataFrame(d[i]['data'])
            df_tmp['reason'] = d[i]['label'] #labels = ['総人口', '転入数', '転出数', '出生数', '死亡数']
            df_tmp['prefCode'] = prefCodeTmp
            df_output = pd.concat([df_output, df_tmp])
        df_output = df_output.loc[:,['prefCode', 'reason', 'year', 'value']]
    
    df_output.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/populationOutInDeathBorn.csv', 'ALL'))