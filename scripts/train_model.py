# принудительно отключим предупреждения системы
import warnings
warnings.simplefilter(action = 'ignore', category = Warning)

# импортируем класс модели
from statsmodels.tsa.statespace.sarimax import SARIMAX

import pickle
import pandas as pd
import numpy as np
import os
 
import mlflow
from mlflow.tracking import MlflowClient
 
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("train_model1")
 
df = pd.read_csv('/home/den/project/datasets/data_train.csv', index_col=0)
df.index = pd.DatetimeIndex(df.index).to_period('D')

# создадим объект модели
model = SARIMAX(df, 
                order = (1, 1, 1), 
                seasonal_order = (0, 0, 0, 0))

with mlflow.start_run():
    mlflow.sklearn.log_model(model,
                             artifact_path="lr",
                             registered_model_name="lr")
    mlflow.log_artifact(local_path="/home/den/project/scripts/train_model.py",
                        artifact_path="train_model code")

result = model.fit()

with open('/home/den/project/models/data.pickle', 'wb') as f:
    pickle.dump(model, f)
