# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QegXMTOEBZ1Da0Ge532eFrRp7U2udvpx
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv

df=pd.read_csv('/content/Final Data.csv')
df.head()

df.info()

df.columns

df.rename(columns = {'Total greenhouse gas emissions (kt of CO2 equivalent)':'GHG_India'}, inplace = True)
df.rename(columns = {'Total greenhouse gas emissions (kt of CO2 equivalent).1':'GHG_USA'}, inplace = True)
df.head(5)

import matplotlib.pyplot as plt


plt.figure(figsize=(12, 6))

plt.plot(df['Date'], df['GHG_India'], marker='o', color='red', label='India')

plt.plot(df['Date'], df['GHG_USA'], marker='o', color='green', label='USA')


plt.title('GHG Emissions: India vs USA')
plt.xlabel('Years')
plt.ylabel('GHG Emissions (kt of CO2 equivalent)')
plt.legend()


plt.grid(True)
plt.show()

import matplotlib.pyplot as plt


plt.figure(figsize=(12, 6))


plt.plot(df['Date'], df['Inflation_India'], marker='o', color='red', label='India')

plt.plot(df['Date'], df['Inflation_USA'], marker='o', color='green', label='USA')

plt.title('Inflation: India vs USA')
plt.xlabel('Years')
plt.ylabel('Inflation')
plt.legend()


plt.grid(True)
plt.show()

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load your data into a pandas DataFrame
data = {
    'Year': range(1990, 2021),
    'GHG_India': [
        1237962.799, 1292414.844, 1317324.226, 1350479.311, 1395751.177,
        1462173.984, 1514073.876, 1574518.527, 1604186.819, 1680581.157,
        1719664.722, 1742348.302, 1762141.225, 1803992.147, 1892154.676,
        1966216.303, 2064473.083, 2209296.069, 2310910.823, 2457277.941,
        2569051.744, 2681723.455, 2832703.035, 2900894.985, 3083573.891,
        3104049.558, 3147642.844, 3269577.732, 3436071.569, 3412419.303,
        3200820.626
    ],
    'GHG_USA': [
        5855541.47, 5810376.768, 5894661.485, 6006008.717, 6100512.901,
        6168767.255, 6338951.954, 6600798.258, 6646954.438, 6647798.804,
        6810655.857, 6759405.527, 6605762.539, 6670155.705, 6752991.006,
        6772890.756, 6683781.075, 6787855.005, 6601049.857, 6184149.347,
        6454244.95, 6254958.264, 6036576.77, 6177416.993, 6224268.726,
        6112057.281, 6003240.816, 5947835.047, 6154645.789, 6039739.492,
        5505180.89
    ],
    'Inflation_India': [
        8.971, 13.870, 11.788, 6.327, 10.248, 10.225, 8.977, 7.164, 13.231,
        4.670, 4.009, 3.779, 4.297, 3.806, 3.767, 4.246, 5.797, 6.373, 8.349,
        10.882, 11.989, 8.912, 9.479, 10.018, 6.666, 4.907, 4.948, 3.328,
        3.939, 3.730, 6.623
    ],
    'Inflation_USA': [
        5.398, 4.235, 3.029, 2.952, 2.607, 2.805, 2.931, 2.338, 1.552, 2.188,
        3.377, 2.826, 1.586, 2.270, 2.677, 3.393, 3.226, 2.853, 3.839, -0.356,
        1.640, 3.157, 2.069, 1.465, 1.622, 0.119, 1.262, 2.130, 2.443, 1.812,
        1.234
    ]
}

df = pd.DataFrame(data)

# Normalize
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['GHG_India', 'GHG_USA', 'Inflation_India', 'Inflation_USA']])


def create_sequences(data, n_steps):
    X, y = [], []
    for i in range(len(data) - n_steps):
        seq_x = data[i:i + n_steps, :]
        seq_y = data[i + n_steps, 0]  # Predicting 'GHG_India'
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

n_steps = 3  # Number of time steps
X, y = create_sequences(scaled_data, n_steps)

print(X.shape, y.shape)
# Split
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
optimizer = Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False)


input_shape = (X_train.shape[1], X_train.shape[2])  # (timesteps, features)

model = Sequential()
model.add(LSTM(100, activation='relu', input_shape=input_shape))
model.add(Dropout(0.1))
model.add(Dense(80, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1, activation='linear'))
model.compile(optimizer=optimizer, loss='mse')

model.summary()

df_GHG_India = df.drop(columns ='GHG_India')
df_Inflation_India = df['Inflation_India']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.4)

history = model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

history = model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))
result = model.evaluate(X_test, y_test)
accuracy_ANN = 1 - result
print("Accuracy : {}".format(accuracy_ANN))
history.history.keys()
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train_loss','val_loss'], loc = 'upper right')
plt.show()

output_model= model.predict(X_test)
y_predict_NN = output_model
#y_test_orig = scaler_y.inverse_transform(y_test.reshape(-1, 1))
y_test_orig_NN= y_test

plt.plot(y_test_orig_NN, y_predict_NN, "^", color='r')
plt.xlabel('Model Predictions')
plt.ylabel('True Values')
plt.show()
print('Model Predictions:', y_predict_NN)
print('True Values:', y_test_orig_NN)



from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from math import sqrt
y_test_orig_NN.reshape(-1, 1)
print(y_predict_NN)
k = X_test.shape[0]
n = len(X_test)
RMSE = float(format(np.sqrt(mean_squared_error(y_test_orig_NN, y_predict_NN )),'.3f'))
MSE = mean_squared_error(y_test_orig_NN, y_predict_NN )
MAE = mean_absolute_error(y_test_orig_NN, y_predict_NN )
r2 = r2_score(y_test_orig_NN, y_predict_NN )
adj_r2 = 1-(1-r2)*(n-1)/(n-k-1)
print('RMSE =',RMSE, '\nMSE =',MSE, '\nMAE =',MAE, '\nR2 =', r2, '\nAdjusted R2 =',adj_r2) #Vlaue of Adjjusted R2?

print(f"y_test_orig_NN shape: {y_test_orig_NN.shape}")
print(f"y_predict_NN shape: {y_predict_NN.shape}")

print(y_test_orig_NN)
print(y_predict_NN)

