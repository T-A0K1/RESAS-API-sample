import json
import urllib.request
import pandas as pd
import sys

def main(output_filepath, prefCode, cityCode = '-'):
    # prefCode: 1~47 ALLの場合は全都道府県
    # cityCode: 全市町村：-
    
    # SET PARAMS
    output_filepath = 'download/population_composition_perYear.csv'
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    df_output = pd.DataFrame()
    
    # ALL処理
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]  
    
    for prefCodeTmp in prefCode_list:
        print(f'prefCode={prefCodeTmp} start', end=', ')
        url = f'https://opendata.resas-portal.go.jp/api/v1/population/composition/perYear?cityCode={cityCode}&prefCode={prefCodeTmp}'

        # GET DATA
        req = urllib.request.Request(url, headers=api_key)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # EDIT DATA
        d = json.loads(data.decode())['result']['data']
        for i in range(len(d)):
            df_tmp = pd.DataFrame(d[i]['data'])
            df_tmp['population_type'] = d[i]['label']
            df_tmp['prefCode'] = prefCodeTmp
            df_output = pd.concat([df_output, df_tmp])
        df_output = df_output.loc[:,['prefCode', 'population_type', 'year', 'value', 'rate']]
    
    df_output.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/population_composition.csv', 'ALL'))