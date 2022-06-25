import json
import urllib.request
import pandas as pd
import sys
import time

# 人口構成一覧
# https://opendata.resas-portal.go.jp/docs/api/v1/population/composition/perYear.html

def main(output_filepath, prefCode):
    # prefCode: 1~47 ALLの場合は全都道府県
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    df_output = pd.DataFrame()
    
    # ALL処理
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]
        
    df_cityCode = pd.read_csv("download/MasterCity.csv", dtype={'cityCode': 'str'})
    print(df_cityCode.head(4))
    print(prefCode_list)
    
    df = pd.DataFrame()
    population_type_list = ['総人口', '年少人口', '生産年齢人口', '老年人口']
    
    for prefCodeTmp in prefCode_list:
        print(prefCodeTmp)
        for cityCodeTmp in df_cityCode.query("prefCode==@prefCodeTmp").cityCode:
            
            url = f'https://opendata.resas-portal.go.jp/api/v1/population/composition/perYear?cityCode={cityCodeTmp}&prefCode={prefCodeTmp}'

            req = urllib.request.Request(url, headers=api_key)
            with urllib.request.urlopen(req) as response: 
                data = response.read()

            d = json.loads(data.decode())
            
            print(cityCodeTmp, prefCodeTmp)
            
            
            for i in range(4):
                if d['result'] is None:
                    print('None!!', cityCodeTmp, prefCode)
                    df_tmp = pd.DataFrame([prefCodeTmp, cityCodeTmp, population_type_list[i], None, None, None], 
                                          index=['prefCode','cityCode','population_type','year','value','rate']).T
                    df = pd.concat([df, df_tmp])
                    pass # データが取得できない市がある
                else:
                    df_tmp =pd.DataFrame(d['result']['data'][i]['data'])                
                    df_tmp['population_type'] = d['result']['data'][i]['label']
                    df_tmp['prefCode'] = prefCodeTmp
                    df_tmp['cityCode'] = cityCodeTmp
                    df = pd.concat([df, df_tmp])
            time.sleep(1)

    df_output = df.loc[:,['prefCode', 'cityCode', 'population_type', 'year', 'value', 'rate']]
    df_output.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    sys.exit(main('download/populationCityALL.csv', 'ALL'))