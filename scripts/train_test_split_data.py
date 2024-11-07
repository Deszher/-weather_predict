import pandas as pd
import numpy as np

import mlflow
from mlflow.tracking import MlflowClient
 
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("train_test_split_data1")

train_size = 0.7

df = pd.read_csv('/home/den/project/datasets/data_processed.csv', header=1)
idxs = np.array(df.index.values)
np.random.shuffle(idxs)
l = int(len(df) * train_size)
train_idxs = idxs[:l]
test_idxs = idxs[l + 1:]

with mlflow.start_run():
    mlflow.log_param("train_size", train_size)
    mlflow.end_run()

df.loc[train_idxs, :].to_csv('/home/den/project/datasets/data_train.csv',
                             header=None,
                             index=None)
df.loc[test_idxs, :].to_csv('/home/den/project/datasets/data_test.csv',
                            header=None,
                            index=None)
