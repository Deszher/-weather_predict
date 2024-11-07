import pandas as pd

df = pd.read_csv('/home/kat/project/datasets/data.csv')

df["date"] = pd.to_datetime(df["date"], format='%d.%m.%Y')
df = df.set_index('date')
df.index = pd.DatetimeIndex(df.index).to_period('D')

# converting degrees Celsius to Fahrenheit
def converttemp(x):
	try:
	    x = (int(x) * 1.8) + 32
	    return float(x)
	except:
	    x = (-int(x.replace(x[0], '')) * 1.8) + 32
	    return float(x)

df["temp"] = df["temp"].apply(converttemp)

with open('/home/kat/project/datasets/data_processed.csv', 'w') as f:
    df.to_csv(f, index=True)
