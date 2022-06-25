import pandas as pd

df = pd.read_csv('download/populationCityALL.csv')

print(df.pivot_table(columns = 'population_type', index='prefCode', values='value', aggfunc='count'))