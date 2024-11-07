import pickle

import numpy as np
import pandas as pd

# принудительно отключим предупреждения системы
#import warnings
#warnings.simplefilter(action = 'ignore', category = Warning)
 
# импортируем класс модели
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

import mlflow
from mlflow.tracking import MlflowClient
 
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("test_model_new")

train = pd.read_csv('/home/den/project/datasets/data_train.csv', header=None, index_col=0)
test = pd.read_csv('/home/den/project/datasets/data_test.csv', header=None, index_col=0)

model = SARIMAX(train, 
                order = (1, 1, 1), 
                seasonal_order = (0, 0, 0, 12))               
model = model.fit()

# тестовый прогнозный период начнется с конца обучающего периода
start = len(train)
 
# и закончится в конце тестового
end = len(train) + len(test) - 1

#with open('/home/den/project/models/data.h5', 'rb') as f:
    #model = pickle.load(f)
    
# применим метод predict
predictions = model.predict(start, end)

mae = mean_absolute_error(test, predictions)
#squared True returns MSE value, False returns RMSE value
mse = mean_squared_error(test, predictions)
rmse = mean_squared_error(test, predictions, squared=False)

with mlflow.start_run():
    mlflow.log_metric("mae", mae)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("rmse", rmse)
    mlflow.end_run()

print(test)
print(predictions)
