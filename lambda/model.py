import pandas as pd
import pickle
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

with open(r'pickle\onehotencoder.pkl', 'rb') as file:
    encoder = pickle.load(file)

with open(r'pickle\xgbreg.pkl', 'rb') as file:
    model = pickle.load(file)

def preprocess(powerStatusD, furnishedD, bathD, transactionTypeD, propTypeD, bedroomD, waterStatus, isPrimeLocProp, floorNo, floors, amenitiesCount):
    df = pd.DataFrame({'powerStatusD' : pd.Series(dtype='object'),
                   'furnishedD' : pd.Series(dtype='object'),
                   'bathD' : pd.Series(dtype='int64'),
                   'transactionTypeD' : pd.Series(dtype='object'),
                   'propTypeD' : pd.Series(dtype='object'),
                   'bedroomD' : pd.Series(dtype='int64'),
                   'waterStatus' : pd.Series(dtype='object'),
                   'isPrimeLocProp' : pd.Series(dtype='object'),
                   'floorNo' : pd.Series(dtype='float'),
                   'floors' : pd.Series(dtype='float'),
                   'amenitiesCount' : pd.Series(dtype='float'),
                   'floorRatio' : pd.Series(dtype='float')})
    
    add = {'powerStatusD' : powerStatusD,
           'furnishedD' : furnishedD,
           'bathD' : bathD,
           'transactionTypeD' : transactionTypeD,
           'propTypeD' : propTypeD,
           'bedroomD' : bedroomD,
           'waterStatus' : waterStatus,
           'isPrimeLocProp' : isPrimeLocProp,
           'floorNo' : floorNo,
           'floors' : floors,
           'amenitiesCount' : amenitiesCount,
           'floorRatio' : (floorNo/floors)}

    # df = df.append(add, ignore_index=True)
    df = pd.concat([df, pd.DataFrame.from_records([add])])

    df_encoded = encoder.transform(df[['powerStatusD', 'furnishedD', 'transactionTypeD', 'propTypeD', 'waterStatus', 'isPrimeLocProp']])
    df_encoded = pd.DataFrame(df_encoded.toarray(), columns= encoder.get_feature_names_out(['powerStatusD', 'furnishedD', 'transactionTypeD', 'propTypeD', 'waterStatus', 'isPrimeLocProp']))
    df = pd.concat([df, df_encoded], axis=1)
    df.drop(['powerStatusD', 'furnishedD', 'transactionTypeD', 'propTypeD', 'waterStatus', 'isPrimeLocProp'], axis = 1, inplace = True)

    return df

powerStatusD = '2 To 4 Hours Powercut'
furnishedD = 'Unfurnished'
transactionTypeD = 'Resale'
bathD = 2
propTypeD = 'Apartment'
bedroomD = 2
waterStatus = 'Water Availability 24 Hours Available'
isPrimeLocProp = 'Y'
floorNo = 5
floors = 7
amenitiesCount = 13

@app.get('/')
def my_function(powerStatusD:str, furnishedD:str, bathD:int, transactionTypeD:str, propTypeD:str, bedroomD:int, waterStatus:str, isPrimeLocProp:str, floorNo:int, floors:int, amenitiesCount:int):
    final = preprocess(powerStatusD, furnishedD, bathD, transactionTypeD, propTypeD, bedroomD, waterStatus, isPrimeLocProp, floorNo, floors, amenitiesCount)
    prediction = str(model.predict(final)[0])
    return JSONResponse({"prediction": prediction})

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

# final = preprocess(powerStatusD, furnishedD, bathD, transactionTypeD, propTypeD, bedroomD, waterStatus, isPrimeLocProp, floorNo, floors, amenitiesCount)
# print(model.predict(final)[0])