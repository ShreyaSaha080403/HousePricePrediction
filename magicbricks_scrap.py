import pandas as pd
import requests

response = requests.get(f'https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=S&propertyType=10002,10003,10021,10022,10001,10017,10000&bedrooms=11700,11701,11702,11703,11704,11705,11706,11707,11708,11709,11710&city=4320&page=2&groupstart=30&offset=0&maxOffset=248&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022,10001,10017,10000&isNRI=N&multiLang=en')
df = pd.json_normalize(response.json()['resultList'], max_level=0)
df = df.drop(columns=df.columns[df.columns.str.contains('Unnamed')])

for i in range(3, 502):
    response = requests.get(f'https://www.magicbricks.com/mbsrp/propertySearch.html?editSearch=Y&category=S&propertyType=10002,10003,10021,10022,10001,10017,10000&bedrooms=11700,11701,11702,11703,11704,11705,11706,11707,11708,11709,11710&city=4320&page={i}&groupstart={30 * (i - 1)}&offset=0&maxOffset=248&sortBy=premiumRecent&postedSince=-1&pType=10002,10003,10021,10022,10001,10017,10000&isNRI=N&multiLang=en')
    df2 = pd.json_normalize(response.json()['resultList'])
    df2 = df2.drop(columns=df2.columns[df2.columns.str.contains('Unnamed')])

    df = pd.concat([df, df2], axis=0, join='outer', ignore_index=True)

df.to_csv('property_data.csv')