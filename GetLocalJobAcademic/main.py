import json
import urllib.request
import pandas as pd
import sys
import time

# 就職者数・進学者数の推移
# https://opendata.resas-portal.go.jp/docs/api/v1/employEducation/localjobAcademic/toTransition.html

def main(output_filepath, prefCode, displayMethod, matter, classification, displayType, gender, cityCode = '-', return_=False):
    # prefCode: 1~47 ALLの場合は全都道府県
    # matter: 0-3
    # classifcation: 1,2(0:就職・進学の合計)
    # displayType: 11,12,20(00:全ての就職進学, 10:全ての進学)
    # gender:1,2 (0:総数)
    
    # SET PARAMS
    with open('setting/api_key_sample.json') as f:
        api_key = json.load(f)
    displayMethod_dic = {'0':'実数', '1':'就職率・進学率'}
    matter_dic = {'0': '地元就職', '1': '流出', '2':'流入', '3':'純流入'}
    classification_dic = {'0':'就職・進学の合計', '1':'進学', '2':'就職'}
    displayType_dic = {'00': '全ての就職・進学', '10':'全ての進学', '11':'大学進学', '12':'短期大学進学', '20':'就職'}
    gender_dic = {'0':'総数', '1':'男性', '2':'女性'}
    
    # ALL処理
    if prefCode == 'ALL':
        prefCode_list = range(1,48)
    else:
        prefCode_list = [prefCode]  
        
    df_out = pd.DataFrame()
    
    for prefCodeTmp in prefCode_list:
        print(prefCodeTmp, end=' ')
        url_base = f'https://opendata.resas-portal.go.jp/api/v1/employEducation/localjobAcademic/toTransition'
        url_condition = f'?prefecture_cd={prefCodeTmp}&displayMethod={displayMethod}&matter={matter}&classification={classification}&displayType={displayType}&gender={gender}'
        url = url_base + url_condition
        
        # GET DATA
        req = urllib.request.Request(url, headers=api_key)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            
        # EDIT DATA
        d = json.loads(data.decode())['result']
        df_tmp = pd.DataFrame(d['changes'][0]['data'])
    
        df_tmp['prefCode'] = prefCodeTmp
        df_tmp['表示方法'] = displayMethod_dic[displayMethod]
        df_tmp['表示内容'] = matter_dic[matter]
        df_tmp['表示分類'] = classification_dic[classification]
        df_tmp['表示区分'] = displayType_dic[displayType]
        df_tmp['性別'] = gender_dic[gender]
        
        df_tmp = df_tmp.loc[:,['prefCode', 'year', '表示方法', '表示内容', '表示分類', '表示区分', '性別', 'value']]
        df_out = pd.concat([df_out, df_tmp])
        time.sleep(1)
    
    if return_:
        return df_out
    else:
        df_out.to_csv(output_filepath, index=False)
    
if __name__ == "__main__":
    # sys.exit(main(
    #     'download/localJobAcademic.csv', 
    #     prefCode='1', 
    #     displayMethod='1',
    #     matter='0',
    #     classification='0',
    #     displayType='00',
    #     gender='0'))
    
    import itertools
    displayMethod_list = ['0', '1']
    matter_list = ['0', '1', '2', '3']
    classification_list = ['0'] #おそらく0以外不可
    displayType_list = ['00'] #おそらく00以外不可
    gender_list = ['1', '2']

    # パラメータの直積
    param_list = itertools.product(displayMethod_list, matter_list, classification_list, displayType_list, gender_list)
    
    df_out = pd.DataFrame()
    for displayMethod, matter, classfification, displayType, gender in param_list:
        print(displayMethod, matter, classfification, displayType, gender)
        df_tmp = main(
            '***', 
            prefCode='ALL', 
            displayMethod=displayMethod,
            matter=matter,
            classification=classfification,
            displayType=displayType,
            gender=gender,
            return_=True)

        df_out = pd.concat([df_out, df_tmp])
    
    df_out.to_csv('download/localJobAcademic.csv', index=False)