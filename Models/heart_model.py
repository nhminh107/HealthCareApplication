import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

# --- Tải dữ liệu ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'Data', 'dataset_heart.csv')
data = pd.read_csv(DATA_FILE_PATH)
#print(data.info())

#-----Phân chia dữ liệu ----
target = 'heart disease'
data[target] = data[target].replace(1, 0)
data[target] = data[target].replace(2, 1)
X = data.drop([target,'resting electrocardiographic results', 'max heart rate','oldpeak', 'major vessels', 'thal', 'ST segment'], axis = 1)
y = data[target]

heartModel = RandomForestClassifier(random_state=200)
heartModel.fit(X, y)


