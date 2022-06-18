import json
import urllib.request
import pandas as pd
import sys

# 地域ブロック別純移動数
# https://opendata.resas-portal.go.jp/docs/api/v1/population/society/forArea.html

def main(output_filepath, prefCode, cityCode = '-'):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    df_output = pd.DataFrame()
    
    # ALL処理
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]  
    
    for prefCodeTmp in prefCode_list:
        url = f'https://opendata.resas-portal.go.jp/api/v1/population/society/forArea?prefCode={prefCodeTmp}'

        # GET DATA
        req = urllib.request.Request(url, headers=api_key)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # EDIT DATA
        d = json.loads(data.decode())['result']['data']
        for i in range(len(d)):
            year = d[i]['year']
            
            # positiveAreaがない場合、キーとしてもなくてエラーになるので、例外処理
            try:
                df_tmpP = pd.DataFrame(d[i]['positiveAreas'])
            except:
                df_tmpP = pd.DataFrame()
            try:
                df_tmpN = pd.DataFrame(d[i]['negativeAreas'])
            except:
                df_tmpN = pd.DataFrame()
            
            df_tmp = pd.concat([df_tmpP, df_tmpN])
            df_tmp['prefCode'] = prefCodeTmp
            df_tmp['year'] = year
            df_output = pd.concat([df_output, df_tmp])
        df_output = df_output.loc[:,['prefCode', 'year', 'areaCode', 'areaName', 'value']]
    
    df_output.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/populationMoveForArea.csv', 'ALL'))