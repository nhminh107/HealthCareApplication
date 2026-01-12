import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import confusion_matrix
# import matplotlib.pyplot as plt
# import seaborn as sn


# --- Tải dữ liệu ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'Data', 'diabetes.csv')
data = pd.read_csv(DATA_FILE_PATH)

# --- Xử lý giá trị 0 thành NaN ---
# Các cột này không thể có giá trị 0 trong thực tế y tế, nên 0 được coi là giá trị thiếu
cols_to_replace = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
data[cols_to_replace] = data[cols_to_replace].replace(0, np.nan)

# --- Phân tách features và target ---
target = "Outcome"
x = data.drop(columns="Outcome", axis=1)
y = data[target]

# Split data
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# --- Xây dựng Pipeline tiền xử lý và mô hình ---
imputer = SimpleImputer(missing_values=np.nan, strategy='median')

# 2. Scaler: Chuẩn hóa dữ liệu
scaler = StandardScaler()

# 3. Model: Hỗ trợ Vector Machine
model = RandomForestClassifier(random_state=42, n_estimators=250, criterion='gini', max_depth=10, max_features='log2')

# Tạo Pipeline: Imputer -> Scaler -> Model
# Pipeline đảm bảo thứ tự xử lý và áp dụng nhất quán trên cả train và test
diabetesModel = Pipeline(steps=[
    ('imputer', imputer),
    ('scaler', scaler),
    ('svm', model)
])

# --- Huấn luyện mô hình bằng Pipeline ---
diabetesModel.fit(X_train, Y_train)


"""
# --- Dự đoán ---
y_predict = pipeline.predict(X_test)

# --- Đánh giá kết quả ---
count_wrong = 0
for i, j in zip(Y_test, y_predict):
    print("Actual {} Predicted {}".format(i, j))
    if(i != j):
        count_wrong += 1

print("\n--- Báo cáo Phân loại sau khi xử lý Nan ---")
print(classification_report(y_true=Y_test, y_pred=y_predict))

print(f"\nTổng số dự đoán sai: {count_wrong}")

"""


"""
cm = np.array(confusion_matrix(Y_test, y_predict, labels=[0, 1]))
confusion = pd.DataFrame(cm, index=['Not Diabetic', 'Diabetic'], columns=["Not Diabetic", "Diabetic"])
sn.heatmap(confusion, annot = True)
plt.savefig("diabetes_prediction.jpg") 

param_grid = {
    "n_estimators": [50, 100, 200, 250],
    "criterion": ["gini", "entropy", "log_loss"],
    "max_depth": [None, 5, 10],
    "max_features": ["sqrt", "log2"]
}

cls2 = GridSearchCV(RandomForestClassifier(), param_grid, scoring='precision', cv=6, verbose=1, n_jobs=-1)
cls2.fit(X_train, Y_train)
y_pred = cls2.predict(X_test)
print(classification_report(y_true=Y_test, y_pred=y_pred)) """