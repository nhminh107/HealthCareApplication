import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

def convert(result):
    if result == 'Suicidal':
        return 7
    if result == 'Bipolar':
        return 6
    if result == 'Depression':
        return 5
    if result == 'Personality disorder':
        return 4
    if result == 'Anxiety':
        return 3
    if result == 'Stress':
        return 2
    if result == 'Normal':
        return 1


# --- Tải dữ liệu ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_FILE_PATH = os.path.join(PROJECT_ROOT, 'Data', 'Combined_Data.csv')
data = pd.read_csv(DATA_FILE_PATH)
#print(data.info())
#print(data['status'].unique())
#print(data['status'].isna().sum()

#----- Xử lí dữ liệu ---------
data.dropna(subset=['statement', 'status'], inplace=True)
data['status'] = data['status'].apply(convert)
X = data.drop(['index', 'status'], axis = 1)
y = data['status']

#print(y.unique())
X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.25, random_state=42)
X_train = X_train[:25000]
Y_train = Y_train[:25000]
X_train_statement = X_train['statement']
X_test_statement = X_test['statement']


smote = SMOTE(sampling_strategy='minority', random_state=42)

# Đưa SMOTE vào Pipeline trước mô hình RF
# Lưu ý: Bạn cần dùng Pipeline của imbalanced-learn thay vì sklearn.pipeline
combinedModel = ImbPipeline(steps=[
    ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=10000)),
    ('smote', smote),
    ('clf', RandomForestClassifier(n_estimators=100, criterion='gini', max_depth= None, max_features='sqrt', class_weight='balanced'))
])
"""
parameters = {
    "n_estimators": [100, 200],
    "criterion": ["gini"],
    "max_depth": [None, 10],
    "max_features": ["sqrt"]
} """

combinedModel.fit(X_train_statement, Y_train)
y_pred = combinedModel.predict(X_test_statement)
print(classification_report(y_true=Y_test, y_pred=y_pred))


