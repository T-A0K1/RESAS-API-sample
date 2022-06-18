import json
import urllib.request
import pandas as pd
import sys
import time

# 人口ピラミッド
# https://opendata.resas-portal.go.jp/docs/api/v1/population/composition/pyramid.html

def main(output_filepath, prefCode, yearRight, yearLeft, cityCode = '-', isReturn = False):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    # yearRight, yearLeft: １度に2年分のデータを取得する仕様。Right と Leftで違いはない。1980-2045年で5年刻みで指定
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    df_output = pd.DataFrame()
    yearDic = {'yearRight': yearRight, 'yearLeft':yearLeft}
    # ALL処理
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]  
        
    for prefCodeTmp in prefCode_list:
        url = f'https://opendata.resas-portal.go.jp/api/v1/population/composition/pyramid?cityCode={cityCode}&yearRight={yearRight}&prefCode={prefCodeTmp}&yearLeft={yearLeft}'

        # GET DATA
        time.sleep(1)
        req = urllib.request.Request(url, headers=api_key)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # EDIT DATA
        d = json.loads(data.decode())['result']
        for RL in ['yearRight', 'yearLeft']:
            df_tmp = pd.DataFrame(d[RL]['data'])
            df_tmp['prefCode'] = prefCodeTmp
            df_tmp['year'] = yearDic[RL]
            df_output = pd.concat([df_output, df_tmp])
        df_output = df_output.loc[:,['prefCode', 'year', 'class', 'man', 'manPercent', 'woman', 'womanPercent']]
    
    if isReturn:
        return df_output
    else:
        df_output.to_csv(output_filepath, index=False)
    
    
if __name__ == "__main__":
    sys.exit(main(
        output_filepath = 'download/populationPyramid.csv', 
        prefCode='1',
        yearRight = 1980,
        yearLeft = 1990))
    
    # 全ての年、全ての都道府県のデータを取得
    df = pd.DataFrame()
    for i in range(7):
        yearRight = 1980 + i*10
        yearLeft = 1985 + i*10
        df_tmp = main('download/populationPyramid.csv', 'ALL', yearRight, yearLeft, isReturn=True)
        df = pd.concat([df, df_tmp])
    df.to_csv('download/populationPyramidAll.csv', index=False)